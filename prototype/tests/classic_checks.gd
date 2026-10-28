extends RefCounted

const T = preload("res://config/tuning.gd")
var tree: SceneTree
var world: Node
var p: CharacterBody2D
var verify: Callable
const DT := 1.0 / 60.0

func steps(count: int) -> void:
	for index in count:
		await p.physics_stepped

func reset_player() -> void:
	p.set_physics_process(false)
	world.touch_controls.release_all()
	for action in ["left", "right", "jump", "touch_jump", "touch_left", "touch_right", "touch_diagonal_left", "touch_diagonal_right"]:
		Input.action_release(action)
	await tree.physics_frame
	await tree.physics_frame
	p.position = T.SPAWN
	p.velocity = Vector2.ZERO
	p.facing = 1
	p.buffered_jump = 0.0
	p.coyote = 0.0
	p.was_jump_held = false
	p.turn_remaining = 0.0
	p.braking = false
	p._clear_classic_air()
	p.set_physics_process(true)
	await steps(5)

func near_apex() -> bool:
	for index in range(80):
		if p.velocity.y < 0 and absf(p.velocity.y) <= T.AIR_JUMP_WINDOW_RATIO * absf(world.tuning.jump_speed()):
			return true
		if p.is_on_floor():
			return false
		await steps(1)
	return false

func run(scene_tree: SceneTree, scene: Node, check: Callable) -> void:
	tree = scene_tree
	world = scene
	p = world.player
	verify = check
	world.tuning_panel.panel.hide()
	world.tuning_panel.switches["CLASSIC_CONTROLS"].button_pressed = true
	world.tuning_panel.switches["AIR_JUMP_ENABLED"].button_pressed = true
	world.tuning_panel.switches["HOLD_AUTO_JUMP"].button_pressed = false
	world.tuning_panel.switches["VARIABLE_JUMP"].button_pressed = false
	world.tuning.set_value("JUMP_HEIGHT", T.JUMP_HEIGHT)
	world.tuning.set_value("TIME_TO_APEX", T.TIME_TO_APEX)
	world.tuning.set_value("RUN_SPEED", T.RUN_SPEED)
	world.tuning.set_value("ACCELERATION", T.ACCELERATION)
	verify.call(world.tuning_panel.sliders.has("STOP_TIME") and world.tuning_panel.sliders.has("TURN_TIME") and world.tuning_panel.sliders.has("APEX_FLIP_TIME"), "gear exposes all three classic timing sliders")
	await reset_player()
	Input.action_press("right")
	await steps(1)
	verify.call(is_equal_approx(p.velocity.x, T.RUN_SPEED), "classic reaches RUN_SPEED on first physics frame")
	await steps(3)
	Input.action_release("right")
	await steps(1)
	verify.call(p.velocity.x > 0 and p.velocity.x < T.RUN_SPEED, "classic release begins gradual braking")
	await steps(4)
	verify.call(is_zero_approx(p.velocity.x), "classic braking stops within STOP_TIME plus one frame")
	Input.action_press("right")
	await steps(3)
	Input.action_release("right")
	Input.action_press("left")
	await steps(1)
	verify.call(p.facing == -1 and is_zero_approx(p.velocity.x), "classic reverse first frame changes face and stands still")
	await steps(2)
	verify.call(is_zero_approx(p.velocity.x), "classic turn pause lasts configured TURN_TIME")
	await steps(1)
	verify.call(is_equal_approx(p.velocity.x, -T.RUN_SPEED), "classic starts reverse run after turn pause")
	await reset_player()
	var tap_x := p.position.x
	Input.action_press("left")
	await steps(1)
	Input.action_release("left")
	await steps(5)
	verify.call(p.facing == -1 and is_equal_approx(p.position.x, tap_x), "short opposite tap only turns face")

	await reset_player()
	var flips_before: int = p.flip_completion_count
	Input.action_press("jump")
	var apex_frame := 0
	var land_frame := 0
	var completed_in_air := false
	var full_rotation := false
	var zero_vertical_frames := 0
	for frame in range(1, 100):
		await steps(1)
		if apex_frame == 0 and p.velocity.y >= 0:
			apex_frame = frame
		if not p.is_on_floor() and is_zero_approx(p.velocity.y):
			zero_vertical_frames += 1
		full_rotation = full_rotation or absf(p.apex_flip_angle) >= TAU - 0.00001
		if p.flip_completion_count > flips_before and not p.is_on_floor():
			completed_in_air = true
		if frame > 1 and p.is_on_floor():
			land_frame = frame
			break
	Input.action_release("jump")
	print("Classic flight: ascent=", apex_frame, " frames; descent=", land_frame - apex_frame, " frames")
	verify.call(apex_frame > 0 and land_frame > 0 and absi(apex_frame - (land_frame - apex_frame)) <= 1, "classic ascent and descent differ by at most one frame")
	verify.call(zero_vertical_frames <= 1, "classic has no artificial apex hang")
	verify.call(full_rotation and completed_in_air and p.flip_completion_count == flips_before + 1 and is_zero_approx(p.rotation), "apex flip completes 360 degrees before landing without body rotation")

	await reset_player()
	p.facing = -1
	Input.action_press("jump")
	for frame in range(40):
		await steps(1)
		if p.apex_flip_angle != 0:
			break
	verify.call(p.apex_flip_angle < 0 and is_zero_approx(p.rotation), "left-facing apex flip rotates sprite left without rotating hitbox")
	await reset_player()
	Input.action_press("jump")
	await steps(2)
	Input.action_press("left")
	await steps(1)
	verify.call(is_equal_approx(p.velocity.x, -T.RUN_SPEED), "classic air direction reaches full speed immediately without turn pause")
	await reset_player()
	Input.action_press("touch_left")
	Input.action_press("touch_diagonal_left")
	Input.action_press("touch_jump")
	await steps(1)
	verify.call(is_equal_approx(p.velocity.x, -T.RUN_SPEED * 0.8) and is_zero_approx(p.spin_direction if not world.tuning.flag("CLASSIC_CONTROLS") else p.apex_flip_angle), "classic diagonal starts at 0.8 RUN_SPEED and avoids slow full-flight spin")

	await reset_player()
	var extra_before: int = p.extra_jump_count
	flips_before = p.flip_completion_count
	Input.action_press("jump")
	await steps(6)
	Input.action_release("jump")
	await steps(1)
	Input.action_press("jump")
	await steps(1)
	verify.call(p.extra_jump_count == extra_before, "air jump cannot activate early in ascent")
	var found := await near_apex()
	verify.call(found and p.extra_jump_count == extra_before, "holding jump into near-apex window never counts as a second press")
	Input.action_release("jump")
	await steps(1)
	Input.action_press("jump")
	await steps(1)
	var expected: float = T.AIR_JUMP_SPEED_RATIO * world.tuning.jump_speed() + world.tuning.gravity() * DT
	verify.call(p.extra_jump_count == extra_before + 1 and is_equal_approx(p.velocity.y, expected), "fresh near-apex press launches exactly 0.7 JUMP_SPEED before gravity")
	found = await near_apex()
	Input.action_release("jump")
	await steps(1)
	Input.action_press("jump")
	await steps(1)
	verify.call(found and p.extra_jump_count == extra_before + 1, "second near-apex press cannot grant another air jump")
	var flips_done_before_land := false
	for frame in range(100):
		await steps(1)
		if p.flip_completion_count == flips_before + 2 and not p.is_on_floor():
			flips_done_before_land = true
		if p.is_on_floor():
			break
	Input.action_release("jump")
	verify.call(flips_done_before_land and p.flip_completion_count == flips_before + 2, "normal jump and air jump each finish one apex flip before landing")
	verify.call(p.is_on_floor() and not p.extra_jump_used, "landing naturally resets the one-air-jump allowance")

	world.tuning_panel.switches["AIR_JUMP_ENABLED"].button_pressed = false
	await reset_player()
	extra_before = p.extra_jump_count
	Input.action_press("jump")
	await steps(1)
	found = await near_apex()
	Input.action_release("jump")
	await steps(1)
	Input.action_press("jump")
	await steps(1)
	verify.call(found and p.extra_jump_count == extra_before, "Khinh cong switch disables the extra jump")
	world.tuning_panel.switches["AIR_JUMP_ENABLED"].button_pressed = true
	await reset_player()
	var cap: float = T.FALL_SPEED_MULTIPLIER * absf(world.tuning.jump_speed())
	p.position = Vector2(100, -1000)
	p.velocity = Vector2(0, cap * 3)
	var fall_start := p.position.y
	await steps(1)
	verify.call(p.velocity.y <= cap and p.position.y - fall_start <= cap * DT + 0.01, "classic fall velocity and displacement respect 2x jump speed cap")

	world.tuning_panel.switches["CLASSIC_CONTROLS"].button_pressed = false
	await reset_player()
	verify.call(is_equal_approx(world.tuning.value("JUMP_HEIGHT"), T.LEGACY_JUMP_HEIGHT), "disabling classic restores legacy 80 px jump default")
	Input.action_press("right")
	await steps(1)
	verify.call(is_equal_approx(p.velocity.x, T.ACCELERATION * DT), "legacy first frame retains acceleration")
	await steps(20)
	Input.action_release("right")
	Input.action_press("left")
	await steps(1)
	verify.call(p.facing == -1 and p.velocity.x > 0 and p.velocity.x < T.RUN_SPEED, "legacy reversal keeps acceleration instead of classic turn pause")
	Input.action_release("left")
	p.position = Vector2(100, -1000)
	p.velocity = Vector2(0, cap * 3)
	await steps(1)
	verify.call(p.velocity.y > cap, "legacy mode retains its previous uncapped fall behavior")
	world.touch_controls.release_all()
	world.tuning_panel.switches["CLASSIC_CONTROLS"].button_pressed = true
	verify.call(is_equal_approx(world.tuning.value("JUMP_HEIGHT"), T.JUMP_HEIGHT), "switching back recalls classic 96 px height")
