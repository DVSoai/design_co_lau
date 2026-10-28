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
	check(world.tuning.flag("CLASSIC_CONTROLS") and world.tuning.flag("AIR_JUMP_ENABLED") and is_equal_approx(world.tuning.value("JUMP_HEIGHT"), 96.0), "classic controls and air jump default on with 96 px jump")
	world.tuning_panel.switches["CLASSIC_CONTROLS"].button_pressed = false
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
	await test_tuning_input(world)
	await test_android_layout(world)
	await test_touch_slider(world)
	await test_dpad_and_jump(world)
	await load("res://tests/classic_checks.gd").new().run(self, world, check)
	print("A0 smoke failures: ", failures)
	quit(0 if failures == 0 else 1)

func mouse_button_at(point: Vector2, button: MouseButton, pressed: bool) -> void:
	var event := InputEventMouseButton.new()
	event.position = point
	event.global_position = point
	event.button_index = button
	event.pressed = pressed
	root.push_input(event, true)

func test_tuning_input(world: Node) -> void:
	var ui = world.tuning_panel
	ui.panel.show()
	await process_frame
	await process_frame
	# Click thanh trượt trước khi thử phím, tái hiện tình huống vừa chỉnh số.
	var first: HSlider = ui.sliders["RUN_SPEED"]
	var first_scroll := first.get_parent().get_parent() as ScrollContainer
	first_scroll.ensure_control_visible(first)
	await process_frame
	var thumb := first.global_position + Vector2(8 + (first.size.x - 16) * first.ratio, first.size.y / 2)
	mouse_button_at(thumb, MOUSE_BUTTON_LEFT, true)
	mouse_button_at(thumb, MOUSE_BUTTON_LEFT, false)
	var before: Dictionary = world.tuning.values.duplicate(true)
	var arrows_unchanged := true
	for repeat in range(6):
		for key in [KEY_UP, KEY_LEFT, KEY_RIGHT, KEY_DOWN]:
			var event := InputEventKey.new()
			event.keycode = key
			event.physical_keycode = key
			event.pressed = true
			event.echo = repeat > 0
			root.push_input(event, true)
			await process_frame
			arrows_unchanged = arrows_unchanged and world.tuning.values == before
			event = event.duplicate()
			event.pressed = false
			root.push_input(event, true)
	check(arrows_unchanged and world.tuning.values == before, "repeated arrow keys leave all tuning values unchanged while panel is open")
	var sliders_safe := true
	var wheels_unchanged := true
	for slider: HSlider in ui.sliders.values():
		sliders_safe = sliders_safe and slider.focus_mode == Control.FOCUS_NONE and not slider.scrollable
		var scroll := slider.get_parent().get_parent() as ScrollContainer
		scroll.ensure_control_visible(slider)
		await process_frame
		var point := slider.get_global_rect().get_center()
		var motion := InputEventMouseMotion.new()
		motion.position = point
		root.push_input(motion, true)
		for repeat in range(4):
			for button in [MOUSE_BUTTON_WHEEL_UP, MOUSE_BUTTON_WHEEL_DOWN]:
				mouse_button_at(point, button, true)
				mouse_button_at(point, button, false)
				wheels_unchanged = wheels_unchanged and world.tuning.values == before
		await process_frame
	check(sliders_safe and wheels_unchanged and world.tuning.values == before, "wheel events over every slider leave all tuning values unchanged")
	var controls_safe: bool = ui.toggle.focus_mode == Control.FOCUS_NONE and ui.motion_toggle.focus_mode == Control.FOCUS_NONE
	var column = ui.sliders["RUN_SPEED"].get_parent()
	for child in column.get_children():
		if child is Button:
			controls_safe = controls_safe and child.focus_mode == Control.FOCUS_NONE
	check(controls_safe, "gear, checkbox and copy button cannot take keyboard focus")
	var slider: HSlider = ui.sliders["RUN_SPEED"]
	var scroll := slider.get_parent().get_parent() as ScrollContainer
	scroll.ensure_control_visible(slider)
	await process_frame
	var start := slider.global_position + Vector2(8 + (slider.size.x - 16) * slider.ratio, slider.size.y / 2)
	var finish := start + Vector2(50, 0)
	mouse_button_at(start, MOUSE_BUTTON_LEFT, true)
	var drag := InputEventMouseMotion.new()
	drag.position = finish
	drag.relative = finish - start
	drag.button_mask = MOUSE_BUTTON_MASK_LEFT
	root.push_input(drag, true)
	mouse_button_at(finish, MOUSE_BUTTON_LEFT, false)
	await process_frame
	check(not is_equal_approx(world.tuning.value("RUN_SPEED"), before["RUN_SPEED"]), "mouse drag still updates slider with focus disabled")

func test_android_layout(world: Node) -> void:
	var original_size := root.size
	root.content_scale_stretch = Window.CONTENT_SCALE_STRETCH_FRACTIONAL
	for physical in [Vector2i(1920, 1080), Vector2i(2400, 1080), Vector2i(1600, 720)]:
		root.size = physical
		await process_frame
		await process_frame
		var visible := root.get_visible_rect()
		var coverage: Rect2 = root.get_stretch_transform() * visible
		print("Android layout: ", physical, " viewport=", visible.size, " stretch=", root.get_stretch_transform().get_scale())
		check(coverage.position.is_zero_approx() and coverage.size.is_equal_approx(Vector2(physical)), "fractional expand fills %s without letterbox" % physical)
		var controls_inside := visible.encloses(world.tuning_panel.toggle.get_global_rect()) and visible.encloses(world.tuning_panel.panel.get_global_rect())
		for button: Control in world.touch_buttons.values():
			controls_inside = controls_inside and visible.encloses(button.get_global_rect())
		check(controls_inside, "touch controls, gear and panel stay inside %s" % physical)
		var slash_edge: Vector2 = world.touch_buttons["slash"].get_global_rect().end
		var left_edge: Vector2 = world.touch_buttons["left"].position
		check(slash_edge.is_equal_approx(visible.end - Vector2.ONE * T.TOUCH_MARGIN) and is_equal_approx(left_edge.x, visible.position.x + T.TOUCH_MARGIN) and is_equal_approx(world.tuning_panel.toggle.get_global_rect().end.x, world.touch_buttons["menu"].position.x - T.TOUCH_GAP), "buttons remain anchored to live viewport corners at %s" % physical)
		var bounds: Array[Rect2] = [world.tuning_panel.toggle.get_global_rect()]
		for button: Control in world.touch_buttons.values():
			if button.visible:
				bounds.append(button.get_global_rect())
		for hud_rect: Rect2 in world.touch_controls.hud_rects.values():
			bounds.append(hud_rect)
		var no_overlap := true
		var within_margin := true
		var safe := visible.grow(-T.TOUCH_MARGIN)
		for i in bounds.size():
			within_margin = within_margin and safe.encloses(bounds[i])
			for j in range(i + 1, bounds.size()):
				no_overlap = no_overlap and not bounds[i].intersects(bounds[j])
		check(no_overlap and within_margin, "all controls and HUD stay 24 px inside viewport without overlap at %s" % physical)
		var half := visible.size / 2
		world.camera_anchor = Vector2.ZERO
		var left: Vector2 = world.camera_target()
		world.camera_anchor = T.WORLD_SIZE
		var right: Vector2 = world.camera_target()
		check(left.x >= half.x and right.x <= T.WORLD_SIZE.x - half.x, "camera limits use live viewport at %s" % physical)
	world.tuning_panel.scale_toggle.button_pressed = true
	await process_frame
	check(root.content_scale_stretch == Window.CONTENT_SCALE_STRETCH_INTEGER, "gear switches live stretch to integer")
	world.tuning_panel.scale_toggle.button_pressed = false
	await process_frame
	check(root.content_scale_stretch == Window.CONTENT_SCALE_STRETCH_FRACTIONAL, "gear switches live stretch back to fractional")
	root.size = original_size
	await process_frame
	await process_frame
	check("Screen" in world.tuning_panel.info_label.text and "Viewport" in world.tuning_panel.info_label.text and "Scale" in world.tuning_panel.info_label.text, "gear shows physical screen, viewport and current scale")
	world.debug_enabled = true
	world._process(0.0)
	check(world.debug_label.text.begins_with("Screen") and "Viewport" in world.debug_label.text and "Scale" in world.debug_label.text, "F1 debug includes the same live display diagnostics")
	world.debug_enabled = false

func screen_touch(point: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = 0
	event.position = root.get_stretch_transform() * point
	event.pressed = pressed
	Input.parse_input_event(event)
	Input.flush_buffered_events()

func screen_drag(point: Vector2, relative: Vector2) -> void:
	var event := InputEventScreenDrag.new()
	event.index = 0
	event.position = root.get_stretch_transform() * point
	event.relative = root.get_stretch_transform().basis_xform(relative)
	Input.parse_input_event(event)
	Input.flush_buffered_events()

func test_touch_slider(world: Node) -> void:
	# Headless không có thiết bị touch: bật hint để native ScrollContainer xử lý.
	var old_touch := Input.emulate_touch_from_mouse
	var old_mouse := Input.emulate_mouse_from_touch
	Input.emulate_touch_from_mouse = true
	Input.emulate_mouse_from_touch = true
	var ui = world.tuning_panel
	ui.panel.show()
	var slider: HSlider = ui.sliders["RUN_SPEED"]
	ui.scroll.ensure_control_visible(slider)
	await process_frame
	await process_frame
	var before: Dictionary = world.tuning.values.duplicate(true)
	var start := slider.global_position + Vector2(slider.size.x * 0.1, slider.size.y / 2)
	# Kéo ngang từ rãnh (ngoài núm) cũng không được đổi giá trị.
	screen_touch(start, true)
	screen_drag(start + Vector2(50, 0), Vector2(50, 0))
	screen_touch(start + Vector2(50, 0), false)
	check(world.tuning.values == before, "horizontal touch starting on track cannot change slider value")
	var scroll_before: int = ui.scroll.scroll_vertical
	screen_touch(start, true)
	for step in range(1, 5):
		screen_drag(start - Vector2(0, step * 15), Vector2(0, -15))
		await process_frame
	screen_touch(start - Vector2(0, 60), false)
	check(world.tuning.values == before, "vertical touch swipe across slider track never changes tuning")
	check(ui.scroll.scroll_vertical > scroll_before, "vertical touch swipe scrolls the tuning panel")
	await frames(20)
	ui.scroll.ensure_control_visible(slider)
	await process_frame
	start = slider.global_position + slider.thumb_center()
	screen_touch(start, true)
	screen_drag(start + Vector2(0, -40), Vector2(0, -40))
	screen_touch(start + Vector2(0, -40), false)
	check(world.tuning.values == before, "vertical gesture starting on thumb does not drift its value")
	await frames(20)
	ui.scroll.ensure_control_visible(slider)
	await process_frame
	start = slider.global_position + slider.thumb_center()
	screen_touch(start, true)
	screen_drag(start + Vector2(60, 0), Vector2(60, 0))
	screen_touch(start + Vector2(60, 0), false)
	check(not is_equal_approx(world.tuning.value("RUN_SPEED"), before["RUN_SPEED"]), "horizontal touch drag starting on thumb adjusts value")
	check(slider.size.y >= 44, "slider touch area is at least 44 px high")

	Input.emulate_touch_from_mouse = old_touch
	Input.emulate_mouse_from_touch = old_mouse

func control_touch(id: int, point: Vector2, pressed: bool) -> void:
	var event := InputEventScreenTouch.new()
	event.index = id
	event.position = point
	event.pressed = pressed
	root.push_input(event, true)

func settle_player(world: Node) -> void:
	world.player.set_physics_process(false)
	world.touch_controls.release_all()
	Input.action_release("jump")
	Input.action_release("left")
	Input.action_release("right")
	await frames(2) # kết thúc các cạnh press/release từ ca trước
	world.player.buffered_jump = 0.0
	world.player.coyote = 0.0
	world.player.spin_direction = 0.0
	world.player.position = T.SPAWN
	world.player.velocity = Vector2.ZERO
	world.player.was_jump_held = false
	world.player.set_physics_process(true)
	await frames(8)

func measure_jump(world: Node, early_release: bool, variable: bool) -> float:
	world.tuning.set_flag("HOLD_AUTO_JUMP", false)
	world.tuning.set_flag("VARIABLE_JUMP", variable)
	await settle_player(world)
	var start_y: float = world.player.position.y
	var min_y := start_y
	var airborne := false
	Input.action_press("jump")
	for index in range(100):
		await physics_frame
		if index == 2 and early_release:
			Input.action_release("jump")
		min_y = minf(min_y, world.player.position.y)
		airborne = airborne or not world.player.is_on_floor()
		if airborne and world.player.is_on_floor():
			break
	Input.action_release("jump")
	await frames(2)
	return start_y - min_y

func test_dpad_and_jump(world: Node) -> void:
	world.tuning_panel.panel.hide()
	world.touch_controls.release_all()
	world.tuning.set_value("JUMP_HEIGHT", T.LEGACY_JUMP_HEIGHT)
	world.tuning.set_value("TIME_TO_APEX", T.TIME_TO_APEX)
	world.tuning.set_value("RUN_SPEED", T.RUN_SPEED)
	world.tuning.set_flag("HOLD_AUTO_JUMP", true)
	world.tuning.set_flag("VARIABLE_JUMP", false)
	var buttons: Dictionary = world.touch_buttons
	world.debug_enabled = false
	world._process(0.0)
	var visible_movement := 0
	for key in ["left", "right", "jump", "diag_left", "diag_right"]:
		if buttons[key].visible:
			visible_movement += 1
	check(visible_movement == 3 and buttons.diag_left.hit_only and buttons.diag_right.hit_only and buttons.diag_left.caption.is_empty() and buttons.diag_right.caption.is_empty(), "only three movement buttons are drawn; diagonal zones have no normal drawing")
	var d: float = T.TOUCH_BUTTON_SIZE.x
	check(is_equal_approx(buttons.right.position.x - buttons.left.position.x, 2.2 * d) and is_equal_approx(buttons.left.position.y - buttons.jump.position.y, 1.35 * d) and is_equal_approx(buttons.jump.position.x, (buttons.left.position.x + buttons.right.position.x) / 2), "d-pad follows 2.2d spacing and 1.35d jump height with centered up button")
	check(is_equal_approx(buttons.diag_left.position.x + buttons.diag_left.size.x, buttons.jump.position.x) and is_equal_approx(buttons.diag_right.position.x, buttons.jump.position.x + d) and is_equal_approx(buttons.diag_left.position.y, buttons.jump.position.y) and is_equal_approx(buttons.diag_right.position.y, buttons.jump.position.y), "invisible zones are adjacent to both sides of up on the same row")
	var saved_position: Vector2 = buttons.diag_left.position
	buttons.diag_left.position = buttons.jump.position
	check(world.touch_controls._hit(buttons.jump.position + Vector2.ONE * d / 3) == "jump", "up button wins hit priority when a diagonal region overlaps")
	buttons.diag_left.position = saved_position
	for side in ["left", "right"]:
		var zone: Control = buttons["diag_" + side]
		var saved: Vector2 = zone.position
		zone.position = buttons[side].position
		check(world.touch_controls._hit(zone.position + zone.size / 2) == "diag_" + side, "diagonal wins hit priority over lower direction " + side)
		zone.position = saved
	world.debug_enabled = true
	world._process(0.0)
	check(buttons.diag_left.visible and buttons.diag_right.visible and buttons.diag_left.hit_only and buttons.diag_right.hit_only, "F1 enables outline-only diagonal diagnostics")
	world.debug_enabled = false
	world._process(0.0)
	check(not buttons.diag_left.visible and not buttons.diag_right.visible and world.touch_controls._hit(buttons.diag_left.position + buttons.diag_left.size / 2) == "diag_left", "diagonal zones remain touchable with debug drawing hidden")
	check(buttons.diag_left.position.x < buttons.jump.position.x and buttons.diag_right.position.x > buttons.jump.position.x and is_equal_approx(buttons.diag_left.size.x, T.TOUCH_BUTTON_SIZE.x * 0.9), "diagonal jump regions are on matching sides and 0.9x wide")
	for direction in [-1, 1]:
		await settle_player(world)
		var key := "diag_left" if direction < 0 else "diag_right"
		var center: Vector2 = buttons[key].get_global_rect().get_center()
		control_touch(0, center, true)
		await frames(3)
		check(world.player.velocity.x * direction > 0 and world.player.velocity.y < 0 and Input.is_action_pressed("touch_jump"), "diagonal region jumps and holds direction %d" % direction)
		var side: String = "left" if direction < 0 else "right"
		var opposite: String = "right" if direction < 0 else "left"
		check(buttons.jump.held and buttons[side].held and not buttons[opposite].held and buttons.jump.scale.is_equal_approx(Vector2.ONE * 0.95) and buttons[side].scale.is_equal_approx(Vector2.ONE * 0.95), "invisible diagonal lights up and shrinks jump plus matching direction")
		var body_rotation: float = world.player.rotation
		world.player.set_physics_process(false)
		world.player.spin_elapsed = world.player.spin_duration / 4
		world.player._update_sprite_motion(0.0, false, false)
		check(is_equal_approx(world.player.sprite.rotation, direction * PI / 2), "diagonal fake spin follows direction at quarter flight")
		world.player.spin_elapsed = world.player.spin_duration
		world.player._update_sprite_motion(0.0, false, false)
		check(is_equal_approx(world.player.sprite.rotation, direction * TAU) and is_equal_approx(world.player.rotation, body_rotation) and is_zero_approx(world.player.get_child(0).rotation), "diagonal completes 360 degrees without rotating body or hitbox")
		world.tuning_panel.switches["DIAGONAL_SPIN_ENABLED"].button_pressed = false
		world.player._update_sprite_motion(0.0, false, false)
		check(is_zero_approx(world.player.sprite.rotation), "gear disables diagonal spin")
		world.tuning_panel.switches["DIAGONAL_SPIN_ENABLED"].button_pressed = true
		control_touch(0, center, false)
		check(not Input.is_action_pressed("touch_left") and not Input.is_action_pressed("touch_right") and not Input.is_action_pressed("touch_jump"), "releasing diagonal clears its held actions")
	# Vuốt cùng một ngón qua các vùng không làm mất action đang dùng chung.
	control_touch(0, buttons.diag_left.position + buttons.diag_left.size / 2, true)
	var drag := InputEventScreenDrag.new()
	drag.index = 0
	drag.position = buttons.jump.position + buttons.jump.size / 2
	root.push_input(drag, true)
	check(Input.is_action_pressed("touch_jump") and not Input.is_action_pressed("touch_left") and buttons.jump.held and not buttons.left.held, "sliding from diagonal to up keeps jump and releases direction feedback")
	drag = drag.duplicate()
	drag.position = buttons.diag_right.position + buttons.diag_right.size / 2
	root.push_input(drag, true)
	check(Input.is_action_pressed("touch_jump") and Input.is_action_pressed("touch_right") and buttons.jump.held and buttons.right.held, "sliding to opposite diagonal updates direction and both visible highlights")
	drag = drag.duplicate()
	drag.position = buttons.right.position + buttons.right.size / 2
	root.push_input(drag, true)
	check(not Input.is_action_pressed("touch_jump") and Input.is_action_pressed("touch_right") and not buttons.jump.held, "sliding down to right retains direction without jump")
	drag = drag.duplicate()
	drag.position = Vector2.ZERO
	root.push_input(drag, true)
	check(not Input.is_action_pressed("touch_right") and not buttons.right.held, "sliding outside all regions releases actions and feedback")
	control_touch(0, Vector2.ZERO, false)
	# Một ngón ở vùng chéo, ngón thứ hai ở trái: nhả vùng chéo vẫn giữ trái.
	control_touch(0, buttons.diag_left.get_global_rect().get_center(), true)
	control_touch(1, buttons.left.get_global_rect().get_center(), true)
	control_touch(0, Vector2.ZERO, false)
	check(Input.is_action_pressed("touch_left") and not Input.is_action_pressed("touch_jump"), "multitouch release preserves another finger's direction")
	control_touch(1, Vector2.ZERO, false)
	await settle_player(world)
	var count: int = world.player.jump_count
	var up: Vector2 = buttons.jump.get_global_rect().get_center()
	control_touch(0, up, true)
	await frames(110)
	check(world.player.jump_count >= count + 2, "holding up repeats jump after landing")
	control_touch(0, up, false)
	world.tuning_panel.switches["HOLD_AUTO_JUMP"].button_pressed = false
	await settle_player(world)
	count = world.player.jump_count
	control_touch(0, up, true)
	await frames(110)
	check(world.player.jump_count == count + 1, "auto-jump switch off permits only one jump per hold")
	control_touch(0, up, false)
	var full_height := await measure_jump(world, false, true)
	var short_height := await measure_jump(world, true, true)
	print("Variable jump: held height=", full_height, " early-release height=", short_height)
	check(short_height < full_height * 0.75, "early release gives lower jump when variable jump is enabled")
	var default_height := await measure_jump(world, true, false)
	check(default_height > short_height * 1.3, "variable jump off retains full-height early-release jump")
	world.tuning_panel.switches["HOLD_AUTO_JUMP"].button_pressed = true
	world.tuning_panel.switches["VARIABLE_JUMP"].button_pressed = false
	check(world.tuning.flag("HOLD_AUTO_JUMP") and not world.tuning.flag("VARIABLE_JUMP"), "jump toggle defaults are auto-repeat on and variable height off")
	var initial_count: int = world.touch_controls.health_count
	control_touch(0, buttons.health.get_global_rect().get_center(), true)
	control_touch(0, Vector2.ZERO, false)
	check(world.touch_controls.health_count == initial_count - 1, "health placeholder decrements count on press")
	control_touch(0, buttons.target.get_global_rect().get_center(), true)
	control_touch(0, Vector2.ZERO, false)
	control_touch(0, buttons.skill_1.get_global_rect().get_center(), true)
	control_touch(0, Vector2.ZERO, false)
	world.tuning_panel.switches["HUD_VISIBLE"].button_pressed = false
	await process_frame
	await process_frame
	check(not buttons.menu.visible and is_equal_approx(world.tuning_panel.toggle.get_global_rect().end.x, root.get_visible_rect().end.x - T.TOUCH_MARGIN), "HUD switch hides menu and frees top-right space")
	world.tuning_panel.switches["HUD_VISIBLE"].button_pressed = true
	await process_frame
	await process_frame
	check(buttons.menu.visible and world.tuning_panel.toggle.size.x >= 56 and world.tuning_panel.toggle.size.y >= 56, "HUD can be restored and gear is at least 56x56")
	world.dummy.take_hit(T.DAMAGE)
	var damage_label: Label = world.dummy.get_child(world.dummy.get_child_count() - 1)
	check(world.player.slash_effect.z_index > world.dummy.z_index and damage_label.z_index > world.dummy.z_index and not damage_label.z_as_relative, "slash trail and damage text render above dummy")
	world.touch_controls.release_all()
