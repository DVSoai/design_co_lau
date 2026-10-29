extends "res://scripts/player.gd"
## Only new environmental rules; run/jump/slash remain the A0 implementation.
var layout_world: Node2D
var climbing := false
var ladder_detached := false
const WATER_MULTIPLIER := 0.7 # shallow water only; no A0 configuration change

func _level_width() -> float:
	return layout_world.map_size.x

func _fall_limit() -> float:
	return layout_world.map_size.y + T.PLAYER_BOX.y

func _reset_after_fall() -> void:
	layout_world.respawn("fall")

func _speed_multiplier() -> float:
	return WATER_MULTIPLIER if layout_world.in_water(position) else 1.0

func _physics_process(delta: float) -> void:
	var ladder: Rect2 = layout_world.ladder_at(position)
	var up := Input.is_action_pressed("climb_up") or Input.is_action_pressed("touch_jump")
	var down := Input.is_action_pressed("climb_down")
	var axis := clampf(Input.get_axis("left","right")+Input.get_axis("touch_left","touch_right"),-1,1)
	var leave_jump := Input.is_action_just_pressed("ladder_jump")
	if not up and not down:
		ladder_detached = false
	if climbing and (axis != 0 or leave_jump or not ladder.has_area()):
		climbing = false
		ladder_detached = true
		if leave_jump:
			# Ask the original A0 jump resolver to perform a normal jump.
			buffered_jump = tuning.value("JUMP_BUFFER")
			coyote = tuning.value("COYOTE_TIME")
	if not climbing and not ladder_detached and ladder.has_area() and (up or down) and axis == 0:
		climbing = true
		_clear_classic_air()
	if climbing:
		position.x = ladder.get_center().x
		velocity = Vector2(0,(float(down)-float(up))*T.RUN_SPEED/2)
		move_and_slide()
		position.y = clampf(position.y,ladder.position.y,ladder.end.y)
		coyote = 0
		buffered_jump = 0
		was_jump_held = up
		_update_sprite_motion(delta,false,false)
		physics_stepped.emit()
		return
	super._physics_process(delta)

func clear_layout_state() -> void:
	velocity = Vector2.ZERO
	climbing = false
	ladder_detached = false
	buffered_jump = 0
	coyote = 0
	was_jump_held = false
	turn_remaining = 0
	braking = false
	pulse_elapsed = T.SPRITE_SCALE_RECOVERY
	spin_direction = 0
	_clear_classic_air()
