extends SceneTree

const T = preload("res://config/tuning.gd")
var failures := 0

func check(ok: bool, message: String) -> void:
	print(("PASS: " if ok else "FAIL: ") + message)
	if not ok:
		failures += 1

func _initialize() -> void:
	call_deferred("run")

func frames(count: int) -> void:
	for i in count:
		await physics_frame

func run() -> void:
	var gap_width: float = T.TERRAIN[1].position.x - T.TERRAIN[0].end.x
	var jump_range: float = T.RUN_SPEED * 2 * T.TIME_TO_APEX
	print("Jump range: %.1f px; gap: %.1f px; required: %.1f px" % [jump_range, gap_width, 1.5 * gap_width])
	assert(jump_range >= 1.5 * gap_width, "Jump range must cover at least 1.5 × gap width")
	check(jump_range >= 1.5 * gap_width, "default horizontal jump range has 1.5x gap margin")
	var world = load("res://main.tscn").instantiate()
	root.add_child(world)
	await frames(10)
	var p = world.player
	check(p.is_on_floor(), "player lands on ground")
	Input.action_press("right")
	await frames(20)
	Input.action_release("right")
	check(p.position.x > T.SPAWN.x + 15, "keyboard action moves player")
	await frames(12)
	var start_y: float = p.position.y
	Input.action_press("jump")
	await frames(2)
	Input.action_release("jump")
	await frames(16)
	check(p.position.y < start_y - 50, "jump rises toward configured apex")
	await frames(70)
	check(p.is_on_floor(), "player falls and lands")
	p.position = T.DUMMY_POSITION - Vector2(38, 0)
	p.velocity = Vector2.ZERO
	p.facing = 1
	await frames(10)
	Input.action_press("slash")
	await frames(2)
	Input.action_release("slash")
	await frames(24)
	check(world.dummy.hit_count == 1, "Area2D slash hits dummy exactly once")
	check(world.dummy.get_child_count() > 1, "damage label is spawned")
	Input.action_press("debug")
	await process_frame
	await process_frame
	Input.action_release("debug")
	check(world.debug_enabled and world.debug_label.visible, "F1 action enables hitboxes and values")
	p.position = Vector2(750, T.FALL_RESET_Y + 10)
	await frames(2)
	check(p.position.distance_to(T.SPAWN) < 5, "fall resets player")
	await frames(10)
	p.position = Vector2(725, 460)
	p.velocity = Vector2.ZERO
	await frames(2)
	Input.action_press("jump")
	await frames(2)
	Input.action_release("jump")
	check(p.velocity.y < 0, "coyote jump works just after leaving ledge")
	p.position = Vector2(100, 446)
	p.velocity = Vector2(0, 180)
	p.coyote = 0
	await frames(1)
	Input.action_press("jump")
	await frames(2)
	Input.action_release("jump")
	await frames(8)
	check(p.velocity.y < 0 and p.position.y < 440, "buffered jump fires on landing")
	Input.action_press("debug")
	await process_frame
	await process_frame
	Input.action_release("debug")
	check(not world.debug_enabled and not world.debug_label.visible, "F1 action disables debug")
	world.tuning_panel.toggle.pressed.emit()
	check(world.tuning_panel.panel.visible, "gear opens tuning panel")
	world.tuning_panel.sliders["RUN_SPEED"].value = 300.0
	check(is_equal_approx(world.tuning.value("RUN_SPEED"), 300.0), "slider updates live run speed")
	p.position = T.SPAWN
	p.velocity = Vector2.ZERO
	Input.action_press("right")
	await frames(30)
	Input.action_release("right")
	check(p.velocity.x > T.RUN_SPEED, "player consumes live speed instead of default")
	world.tuning_panel.sliders["JUMP_HEIGHT"].value = 100.0
	world.tuning_panel.sliders["TIME_TO_APEX"].value = 0.5
	check(is_equal_approx(world.tuning.gravity(), 800.0) and is_equal_approx(world.tuning.jump_speed(), -400.0), "jump gravity and velocity recalculate immediately")
	var fresh = load("res://config/runtime_tuning.gd").new()
	check(is_equal_approx(fresh.value("RUN_SPEED"), T.RUN_SPEED), "runtime edits leave tuning defaults unchanged")
	check("RUN_SPEED = 300" in world.tuning.as_text() and "GRAVITY = 800" in world.tuning.as_text(), "clipboard text contains current and derived values")
	world.tuning_panel.toggle.pressed.emit()
	check(not world.tuning_panel.panel.visible, "gear closes tuning panel")
	# Đo transform sprite độc lập, giữ trạng thái vật lý đứng trên đất.
	p.position = T.SPAWN
	p.velocity = Vector2.ZERO
	await frames(10)
	p.set_physics_process(false)
	p.attack_time = -1
	p.pulse_elapsed = T.SPRITE_SCALE_RECOVERY
	p.idle_phase = 0.0
	var body_transform: Transform2D = p.transform
	var body_shape = p.get_child(0)
	var hitbox_transform: Transform2D = body_shape.transform
	var slash_transform: Transform2D = p.slash.transform
	p._update_sprite_motion(T.IDLE_BOB_PERIOD / 4, false, false)
	check(is_equal_approx(p.sprite.position.y - T.SPRITE_OFFSET.y, 1.0), "idle bob reaches +1 px at quarter period")
	p._update_sprite_motion(T.IDLE_BOB_PERIOD / 2, false, false)
	check(is_equal_approx(p.sprite.position.y - T.SPRITE_OFFSET.y, -1.0), "idle bob reaches -1 px at three-quarter period")
	p.velocity.x = 100.0
	p.run_phase = 0.0
	p._update_sprite_motion(0.1, false, false)
	var slow_phase: float = p.run_phase
	check(is_equal_approx(rad_to_deg(p.sprite.rotation), 4.0), "running leans 4 degrees right")
	p.velocity.x = -200.0
	p.run_phase = 0.0
	p._update_sprite_motion(0.1, false, false)
	check(is_equal_approx(p.run_phase, slow_phase * 2) and is_equal_approx(rad_to_deg(p.sprite.rotation), -4.0), "step frequency scales with speed and lean follows left movement")
	p.velocity = Vector2.ZERO
	p._update_sprite_motion(0.0, true, false)
	check(p.sprite.scale.is_equal_approx(Vector2(0.9, 1.1)), "takeoff stretches sprite to 0.9 x 1.1")
	p._update_sprite_motion(T.SPRITE_SCALE_RECOVERY, false, false)
	p._update_sprite_motion(0.0, false, false)
	check(p.sprite.scale.is_equal_approx(Vector2.ONE), "takeoff scale recovers in 0.1 seconds")
	p._update_sprite_motion(0.0, false, true)
	check(p.sprite.scale.is_equal_approx(Vector2(1.15, 0.85)), "landing squashes sprite to 1.15 x 0.85")
	p._update_sprite_motion(T.SPRITE_SCALE_RECOVERY, false, false)
	p._update_sprite_motion(0.0, false, false)
	check(p.sprite.scale.is_equal_approx(Vector2.ONE), "landing scale recovers in 0.1 seconds")
	p.attack_time = (T.HIT_START + T.HIT_END) / 2
	p.facing = -1
	p._update_sprite_motion(0.0, false, false)
	check(is_equal_approx(p.sprite.position.x - T.SPRITE_OFFSET.x, -4.0), "slash shifts sprite 4 px toward facing inside hit window")
	p.attack_time = T.HIT_END
	p._update_sprite_motion(0.0, false, false)
	check(is_equal_approx(p.sprite.position.x, T.SPRITE_OFFSET.x), "slash shift stops outside hit window")
	check(p.transform == body_transform and body_shape.transform == hitbox_transform and p.slash.transform == slash_transform and body_shape.shape.size == T.PLAYER_BOX, "sprite motion leaves body and hitbox transforms and dimensions unchanged")
	world.tuning_panel.motion_toggle.button_pressed = false
	p._update_sprite_motion(0.0, true, false)
	check(not world.tuning.fake_motion_enabled() and p.sprite.position == T.SPRITE_OFFSET and p.sprite.scale == Vector2.ONE and is_zero_approx(p.sprite.rotation), "gear switch disables all fake motion and restores neutral transform")
	check("FAKE_MOTION_ENABLED = false" in world.tuning.as_text(), "clipboard text includes live motion switch")
	world.tuning_panel.motion_toggle.button_pressed = true
	p.idle_phase = 0.0
	p._update_sprite_motion(T.IDLE_BOB_PERIOD / 4, false, false)
	check(world.tuning.fake_motion_enabled() and not p.sprite.position.is_equal_approx(T.SPRITE_OFFSET), "gear switch re-enables fake motion")
	print("A0 smoke failures: ", failures)
	quit(0 if failures == 0 else 1)
