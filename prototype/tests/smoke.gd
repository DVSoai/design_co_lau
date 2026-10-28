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
	print("A0 smoke failures: ", failures)
	quit(0 if failures == 0 else 1)
