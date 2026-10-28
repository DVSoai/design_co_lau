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
	await test_tuning_input(world)
	await test_android_layout(world)
	await test_touch_slider(world)
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
		for button: TouchScreenButton in world.touch_buttons.values():
			controls_inside = controls_inside and visible.encloses(Rect2(button.position - T.TOUCH_BUTTON_SIZE / 2, T.TOUCH_BUTTON_SIZE))
		check(controls_inside, "touch controls, gear and panel stay inside %s" % physical)
		var slash_edge: Vector2 = world.touch_buttons["slash"].position + T.TOUCH_BUTTON_SIZE / 2
		var left_edge: Vector2 = world.touch_buttons["left"].position - T.TOUCH_BUTTON_SIZE / 2
		check(slash_edge.is_equal_approx(visible.end - Vector2.ONE * T.TOUCH_MARGIN) and is_equal_approx(left_edge.x, visible.position.x + T.TOUCH_MARGIN) and is_equal_approx(world.tuning_panel.toggle.get_global_rect().end.x, visible.end.x - 12), "buttons remain anchored to live viewport corners at %s" % physical)
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
