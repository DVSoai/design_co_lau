extends CharacterBody2D

signal physics_stepped

const SlashEffect = preload("res://scripts/slash_effect.gd")
const T = preload("res://config/tuning.gd")
var tuning: RefCounted
var facing := 1.0
var coyote := 0.0
var buffered_jump := 0.0
var attack_time := -1.0
var cooldown_elapsed := INF
var hits: Array[Node] = []
var slash: Area2D
var sprite: Sprite2D
var slash_effect: Node2D
var was_jump_held := false
var spin_direction := 0.0
var spin_elapsed := 0.0
var spin_duration := 1.0
var jump_count := 0
var extra_jump_count := 0
var flip_completion_count := 0
var turn_remaining := 0.0
var braking := false
var brake_speed := 0.0
var classic_previous := T.CLASSIC_CONTROLS
var extra_jump_used := false
var air_cycle_active := false
var phase_needs_flip := false
var flip_queue: Array[float] = []
var flip_running := false
var flip_elapsed := 0.0
var flip_direction := 1.0
var apex_flip_angle := 0.0
var debug_enabled := false
var idle_phase := 0.0
var run_phase := 0.0
var pulse_scale := Vector2.ONE
var pulse_elapsed := T.SPRITE_SCALE_RECOVERY

func _ready() -> void:
	collision_layer = 2
	collision_mask = 1
	var shape := CollisionShape2D.new()
	var rectangle := RectangleShape2D.new()
	rectangle.size = T.PLAYER_BOX
	shape.shape = rectangle
	shape.position.y = -T.PLAYER_BOX.y / 2
	add_child(shape)
	sprite = Sprite2D.new()
	sprite.texture = preload("res://assets/chr_dbl_idle_side_96.png")
	sprite.position = T.SPRITE_OFFSET
	sprite.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var shader := Shader.new()
	shader.code = "shader_type canvas_item; void fragment(){ vec4 c=texture(TEXTURE,UV); if(c.g>0.99 && c.r<0.01 && c.b<0.01){c.a=0.0;} COLOR=c; }"
	var material := ShaderMaterial.new()
	material.shader = shader
	sprite.material = material
	add_child(sprite)
	slash = Area2D.new()
	slash.collision_layer = 0
	slash.collision_mask = 4
	var hit_shape := CollisionShape2D.new()
	var hit_rect := RectangleShape2D.new()
	hit_rect.size = T.SLASH_BOX
	hit_shape.shape = hit_rect
	slash.add_child(hit_shape)
	add_child(slash)
	slash_effect = SlashEffect.new()
	slash_effect.player = self
	slash_effect.z_as_relative = false
	slash_effect.z_index = T.COMBAT_EFFECT_Z
	add_child(slash_effect)

func _physics_process(delta: float) -> void:
	var was_grounded := is_on_floor()
	var jumped := false
	var classic: bool = tuning.flag("CLASSIC_CONTROLS")
	if classic != classic_previous:
		classic_previous = classic
		turn_remaining = 0.0
		braking = false
		_clear_classic_air()
	if was_grounded:
		extra_jump_used = false
		air_cycle_active = false
	var axis := clampf(Input.get_axis("left", "right") + Input.get_axis("touch_left", "touch_right"), -1.0, 1.0)
	if classic:
		_classic_horizontal(axis, delta)
	else:
		if axis != 0:
			facing = signf(axis)
		velocity.x = move_toward(velocity.x, axis * tuning.value("RUN_SPEED"), tuning.value("ACCELERATION") * delta)
	sprite.flip_h = facing < 0
	coyote = tuning.value("COYOTE_TIME") if is_on_floor() else maxf(0, coyote - delta)
	buffered_jump = maxf(0, buffered_jump - delta)
	var jump_held := Input.is_action_pressed("jump") or Input.is_action_pressed("touch_jump")
	var jump_pressed := Input.is_action_just_pressed("jump") or Input.is_action_just_pressed("touch_jump")
	if classic:
		jump_pressed = jump_held and not was_jump_held
	if jump_pressed:
		buffered_jump = tuning.value("JUMP_BUFFER")
	if (jump_pressed or buffered_jump > 0 or (tuning.flag("HOLD_AUTO_JUMP") and jump_held and is_on_floor())) and (is_on_floor() or coyote > 0):
		velocity.y = tuning.jump_speed()
		jumped = true
		jump_count += 1
		if classic:
			air_cycle_active = true
			extra_jump_used = false
			phase_needs_flip = true
			flip_queue.clear()
			flip_running = false
			apex_flip_angle = 0.0
			turn_remaining = 0.0
			if axis != 0:
				facing = signf(axis)
				velocity.x = axis * tuning.value("RUN_SPEED") * (T.CLASSIC_DIAGONAL_SPEED_RATIO if _diagonal_held() else 1.0)
		spin_direction = (-1.0 if Input.is_action_pressed("touch_diagonal_left") else 1.0) if (Input.is_action_pressed("touch_diagonal_left") or Input.is_action_pressed("touch_diagonal_right")) else 0.0
		spin_elapsed = 0.0
		spin_duration = 2.0 * tuning.value("TIME_TO_APEX")
		buffered_jump = 0
		coyote = 0
	if classic:
		_queue_apex_if_ready()
		if jump_pressed and not was_grounded and air_cycle_active and not extra_jump_used and tuning.flag("AIR_JUMP_ENABLED") and velocity.y < 0 and absf(velocity.y) <= T.AIR_JUMP_WINDOW_RATIO * absf(tuning.jump_speed()):
			velocity.y = T.AIR_JUMP_SPEED_RATIO * tuning.jump_speed()
			extra_jump_used = true
			extra_jump_count += 1
			phase_needs_flip = true
			buffered_jump = 0.0
			jumped = true
	if tuning.flag("VARIABLE_JUMP") and was_jump_held and not jump_held and velocity.y < 0:
		velocity.y *= T.JUMP_RELEASE_MULTIPLIER
	was_jump_held = jump_held
	if classic:
		# Tích phân midpoint cho vị trí, giữ velocity là vận tốc cuối bước.
		var cap: float = T.FALL_SPEED_MULTIPLIER * absf(tuning.jump_speed())
		velocity.y = minf(velocity.y, cap)
		var next_vertical := minf(velocity.y + tuning.gravity() * delta, cap)
		velocity.y = (velocity.y + next_vertical) / 2
		move_and_slide()
		if not is_on_floor() and not is_on_ceiling():
			velocity.y = next_vertical
	else:
		velocity.y += tuning.gravity() * delta
		move_and_slide()
	position.x = clampf(position.x, T.PLAYER_BOX.x / 2, T.WORLD_SIZE.x - T.PLAYER_BOX.x / 2)
	if position.y > T.FALL_RESET_Y:
		position = T.SPAWN
		velocity = Vector2.ZERO
		buffered_jump = 0
		coyote = 0
		pulse_elapsed = T.SPRITE_SCALE_RECOVERY
		spin_direction = 0.0
		_clear_classic_air()
	if is_on_floor():
		spin_direction = 0.0
		_clear_classic_air()
	elif not jumped:
		spin_elapsed += delta
	if classic and not is_on_floor():
		_queue_apex_if_ready()
		_advance_apex_flip(delta)
	cooldown_elapsed += delta
	if (Input.is_action_just_pressed("slash") or Input.is_action_just_pressed("touch_slash")) and attack_time < 0 and cooldown_elapsed >= tuning.value("ATTACK_COOLDOWN"):
		attack_time = 0
		hits.clear()
	if attack_time >= 0:
		attack_time += delta
		if attack_time >= tuning.value("ATTACK_DURATION"):
			attack_time = -1
			cooldown_elapsed = 0.0
	slash.position = Vector2(T.SLASH_OFFSET.x * facing, T.SLASH_OFFSET.y)
	if is_hit_active():
		for body in slash.get_overlapping_bodies():
			if body.has_method("take_hit") and not hits.has(body):
				hits.append(body)
				body.take_hit(T.DAMAGE)
	_update_sprite_motion(delta, jumped, not was_grounded and is_on_floor())
	slash_effect.queue_redraw()
	queue_redraw()
	physics_stepped.emit()

func _update_sprite_motion(delta: float, jumped: bool, landed: bool) -> void:
	# Sprite là sibling của các CollisionShape2D/Area2D: không truyền transform.
	if not tuning.fake_motion_enabled():
		idle_phase = 0.0
		run_phase = 0.0
		pulse_elapsed = T.SPRITE_SCALE_RECOVERY
		sprite.position = T.SPRITE_OFFSET
		sprite.rotation = 0.0
		sprite.scale = Vector2.ONE
		return
	if jumped or landed:
		pulse_scale = T.JUMP_SPRITE_SCALE if jumped else T.LAND_SPRITE_SCALE
		pulse_elapsed = 0.0
	var weight := clampf(pulse_elapsed / T.SPRITE_SCALE_RECOVERY, 0.0, 1.0)
	sprite.scale = pulse_scale.lerp(Vector2.ONE, weight)
	pulse_elapsed += delta
	sprite.rotation = 0.0
	var bob := 0.0
	if is_on_floor():
		if absf(velocity.x) > T.RUN_MOTION_THRESHOLD:
			run_phase = fmod(run_phase + TAU * absf(velocity.x) * delta / T.RUN_STEP_DISTANCE, TAU)
			bob = sin(run_phase) * T.RUN_BOB_AMPLITUDE
			sprite.rotation = deg_to_rad(T.RUN_LEAN_DEGREES) * signf(velocity.x)
			idle_phase = 0.0
		else:
			idle_phase = fmod(idle_phase + TAU * delta / T.IDLE_BOB_PERIOD, TAU)
			bob = sin(idle_phase) * T.IDLE_BOB_AMPLITUDE
			run_phase = 0.0
	# Dời tâm ảnh theo scale/rotation để giữ mốc chân khi squash/lean.
	sprite.position = (T.SPRITE_OFFSET * sprite.scale).rotated(sprite.rotation) + Vector2(0, bob)
	if is_hit_active():
		sprite.position.x += facing * T.SLASH_SPRITE_SHIFT
	if tuning.flag("CLASSIC_CONTROLS"):
		sprite.rotation += apex_flip_angle
	elif tuning.flag("DIAGONAL_SPIN_ENABLED") and spin_direction != 0 and not is_on_floor():
		# Xoay quanh tâm ảnh, không xoay quanh chân hay bất kỳ hitbox nào.
		sprite.rotation += spin_direction * TAU * T.DIAGONAL_SPIN_TURNS * clampf(spin_elapsed / spin_duration, 0.0, 1.0)

func is_hit_active() -> bool:
	return attack_time >= T.HIT_START and attack_time < T.HIT_END

func _draw() -> void:
	if debug_enabled:
		draw_rect(Rect2(Vector2(-T.PLAYER_BOX.x / 2, -T.PLAYER_BOX.y), T.PLAYER_BOX), Color.CYAN, false, 1)
		draw_rect(Rect2(slash.position - T.SLASH_BOX / 2, T.SLASH_BOX), Color.RED if is_hit_active() else Color(0.6, 0.4, 0.2), false, 1)

func _diagonal_held() -> bool:
	return Input.is_action_pressed("touch_diagonal_left") or Input.is_action_pressed("touch_diagonal_right")

func _classic_horizontal(axis: float, delta: float) -> void:
	if axis != 0:
		braking = false
		if not is_on_floor():
			facing = signf(axis)
			turn_remaining = 0.0
			velocity.x = axis * tuning.value("RUN_SPEED") * (T.CLASSIC_DIAGONAL_SPEED_RATIO if _diagonal_held() else 1.0)
			return
		if signf(axis) != facing:
			facing = signf(axis)
			turn_remaining = tuning.value("TURN_TIME")
			velocity.x = 0.0
			return # khung đầu chỉ quay mặt, kể cả TURN_TIME = 0
		if turn_remaining > 0:
			turn_remaining = maxf(0.0, turn_remaining - delta)
			if turn_remaining > 0.000001:
				velocity.x = 0.0
				return
		velocity.x = axis * tuning.value("RUN_SPEED")
	else:
		if turn_remaining > 0:
			turn_remaining = 0.0
			velocity.x = 0.0 # nhả trong nhịp quay: chỉ đổi mặt
		if not braking:
			brake_speed = absf(velocity.x)
			braking = true
		var stop: float = tuning.value("STOP_TIME")
		velocity.x = move_toward(velocity.x, 0.0, brake_speed * delta / stop) if stop > 0 else 0.0

func _clear_classic_air() -> void:
	extra_jump_used = false
	air_cycle_active = false
	phase_needs_flip = false
	flip_running = false
	flip_queue.clear()
	apex_flip_angle = 0.0

func _queue_apex_if_ready() -> void:
	if phase_needs_flip and air_cycle_active and velocity.y <= 0 and velocity.y >= T.AIR_JUMP_WINDOW_RATIO * tuning.jump_speed():
		flip_queue.append(facing)
		phase_needs_flip = false

func _advance_apex_flip(delta: float) -> void:
	if not flip_running:
		if flip_queue.is_empty():
			apex_flip_angle = 0.0
			return
		flip_direction = flip_queue.pop_front()
		flip_elapsed = 0.0
		flip_running = true
	var duration: float = tuning.value("APEX_FLIP_TIME")
	flip_elapsed = minf(flip_elapsed + delta, duration)
	apex_flip_angle = flip_direction * TAU * flip_elapsed / duration
	if flip_elapsed >= duration:
		flip_running = false
		flip_completion_count += 1
