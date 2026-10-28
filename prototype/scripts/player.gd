extends CharacterBody2D

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
	var axis := clampf(Input.get_axis("left", "right") + Input.get_axis("touch_left", "touch_right"), -1.0, 1.0)
	if axis != 0:
		facing = signf(axis)
	sprite.flip_h = facing < 0
	velocity.x = move_toward(velocity.x, axis * tuning.value("RUN_SPEED"), tuning.value("ACCELERATION") * delta)
	coyote = tuning.value("COYOTE_TIME") if is_on_floor() else maxf(0, coyote - delta)
	buffered_jump = maxf(0, buffered_jump - delta)
	var jump_held := Input.is_action_pressed("jump") or Input.is_action_pressed("touch_jump")
	var jump_pressed := Input.is_action_just_pressed("jump") or Input.is_action_just_pressed("touch_jump")
	if jump_pressed:
		buffered_jump = tuning.value("JUMP_BUFFER")
	if (jump_pressed or buffered_jump > 0 or (tuning.flag("HOLD_AUTO_JUMP") and jump_held and is_on_floor())) and (is_on_floor() or coyote > 0):
		velocity.y = tuning.jump_speed()
		jumped = true
		jump_count += 1
		spin_direction = (-1.0 if Input.is_action_pressed("touch_diagonal_left") else 1.0) if (Input.is_action_pressed("touch_diagonal_left") or Input.is_action_pressed("touch_diagonal_right")) else 0.0
		spin_elapsed = 0.0
		spin_duration = 2.0 * tuning.value("TIME_TO_APEX")
		buffered_jump = 0
		coyote = 0
	if tuning.flag("VARIABLE_JUMP") and was_jump_held and not jump_held and velocity.y < 0:
		velocity.y *= T.JUMP_RELEASE_MULTIPLIER
	was_jump_held = jump_held
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
	if is_on_floor():
		spin_direction = 0.0
	elif not jumped:
		spin_elapsed += delta
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
	if tuning.flag("DIAGONAL_SPIN_ENABLED") and spin_direction != 0 and not is_on_floor():
		# Xoay quanh tâm ảnh, không xoay quanh chân hay bất kỳ hitbox nào.
		sprite.rotation += spin_direction * TAU * T.DIAGONAL_SPIN_TURNS * clampf(spin_elapsed / spin_duration, 0.0, 1.0)

func is_hit_active() -> bool:
	return attack_time >= T.HIT_START and attack_time < T.HIT_END

func _draw() -> void:
	if debug_enabled:
		draw_rect(Rect2(Vector2(-T.PLAYER_BOX.x / 2, -T.PLAYER_BOX.y), T.PLAYER_BOX), Color.CYAN, false, 1)
		draw_rect(Rect2(slash.position - T.SLASH_BOX / 2, T.SLASH_BOX), Color.RED if is_hit_active() else Color(0.6, 0.4, 0.2), false, 1)
