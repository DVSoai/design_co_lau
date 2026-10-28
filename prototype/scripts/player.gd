extends CharacterBody2D

const T = preload("res://config/tuning.gd")
var facing := 1.0
var coyote := 0.0
var buffered_jump := 0.0
var attack_time := -1.0
var cooldown := 0.0
var hits: Array[Node] = []
var slash: Area2D
var sprite: Sprite2D
var debug_enabled := false

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

func _physics_process(delta: float) -> void:
	var axis := Input.get_axis("left", "right")
	if axis != 0:
		facing = signf(axis)
	sprite.flip_h = facing < 0
	velocity.x = move_toward(velocity.x, axis * T.RUN_SPEED, T.ACCELERATION * delta)
	coyote = T.COYOTE_TIME if is_on_floor() else maxf(0, coyote - delta)
	buffered_jump = maxf(0, buffered_jump - delta)
	if Input.is_action_just_pressed("jump"):
		buffered_jump = T.JUMP_BUFFER
	if buffered_jump > 0 and coyote > 0:
		velocity.y = T.JUMP_SPEED
		buffered_jump = 0
		coyote = 0
	velocity.y += T.GRAVITY * delta
	move_and_slide()
	position.x = clampf(position.x, T.PLAYER_BOX.x / 2, T.WORLD_SIZE.x - T.PLAYER_BOX.x / 2)
	if position.y > T.FALL_RESET_Y:
		position = T.SPAWN
		velocity = Vector2.ZERO
		buffered_jump = 0
		coyote = 0
	cooldown = maxf(0, cooldown - delta)
	if Input.is_action_just_pressed("slash") and attack_time < 0 and cooldown <= 0:
		attack_time = 0
		hits.clear()
	if attack_time >= 0:
		attack_time += delta
		if attack_time >= T.ATTACK_DURATION:
			attack_time = -1
			cooldown = T.ATTACK_COOLDOWN
	slash.position = Vector2(T.SLASH_OFFSET.x * facing, T.SLASH_OFFSET.y)
	if is_hit_active():
		for body in slash.get_overlapping_bodies():
			if body.has_method("take_hit") and not hits.has(body):
				hits.append(body)
				body.take_hit(T.DAMAGE)
	queue_redraw()

func is_hit_active() -> bool:
	return attack_time >= T.HIT_START and attack_time < T.HIT_END

func _draw() -> void:
	if attack_time >= 0:
		draw_arc(Vector2(0, T.SLASH_OFFSET.y), T.SLASH_ARC_RADIUS, -1.2 if facing > 0 else 1.9, 1.2 if facing > 0 else 4.3, 12, Color(0.95, 0.85, 0.62), 3)
	if debug_enabled:
		draw_rect(Rect2(Vector2(-T.PLAYER_BOX.x / 2, -T.PLAYER_BOX.y), T.PLAYER_BOX), Color.CYAN, false, 1)
		draw_rect(Rect2(slash.position - T.SLASH_BOX / 2, T.SLASH_BOX), Color.RED if is_hit_active() else Color(0.6, 0.4, 0.2), false, 1)
