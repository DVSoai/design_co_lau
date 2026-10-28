extends SceneTree
var failures := 0

func check(ok: bool, message: String) -> void:
	print(("PASS: " if ok else "FAIL: ") + message)
	if not ok:
		failures += 1

func _initialize() -> void:
	call_deferred("run")

func tick(count: int) -> void:
	for i in count:
		await physics_frame
		await process_frame

func action(name: String, pressed: bool) -> void:
	if pressed:
		Input.action_press(name)
	else:
		Input.action_release(name)

func run() -> void:
	var world = load("res://rig/rig_greybox.tscn").instantiate()
	root.add_child(world)
	await tick(12)
	var rig = world.rig
	rig.player.pause()
	var counts := {"idle":4,"run":6,"jump_up":2,"apex_flip":6,"fall":2,"land":2,"turn":2,"slash_1":4,"slash_2":4,"slash_3":5,"shoot":5,"hurt":2,"knockdown":4}
	var all_attached := true
	var all_limits := true
	for key in counts:
		check(rig.clips[key].frames.size() == counts[key], "%s has %d frames" % [key, counts[key]])
		var time := 0.0
		for frame in rig.clips[key].frames:
			rig.sample(key, time)
			for part in rig.definition.parts:
				var node: Node2D = rig.joints[part.id]
				if part.parent != "":
					var parent_joint: Node2D = rig.joints[part.parent]
					var expected := parent_joint.to_global(Vector2(part.attach[0], part.attach[1]))
					all_attached = all_attached and node.global_position.distance_to(expected) < 0.001
				var angle := float(frame.angles[part.id])
				all_limits = all_limits and angle >= float(part.angle_limit[0]) and angle <= float(part.angle_limit[1])
			if key in ["idle", "land"]:
				for id in ["foot_near", "foot_far"]:
					var shape: Polygon2D = rig.shapes[id]
					var bottom := -INF
					for point in shape.polygon:
						bottom = maxf(bottom, rig.to_local(shape.to_global(point)).y)
					check(absf(bottom) < 0.001, "%s frame at %.3f: %s touches baseline" % [key,time,id])
			time += float(frame.duration)
	check(all_attached, "all joints stay at authored parent anchors in every frame")
	check(all_limits, "all local angles stay within proposed joint limits")
	rig.sample("apex_flip", 0.2)
	check(is_equal_approx(rig.pivot_root.rotation, TAU), "apex clip completes exactly 360 degrees at 0.20 s")
	check(is_equal_approx(rig.player.get_animation("turn").length, 0.05), "turn stays within A0 0.05 s")
	check(is_equal_approx(rig.player.get_animation("slash_1").length, 0.3), "basic slash keeps A0 0.30 s")
	var p = world.player
	check(p.is_on_floor(), "real A0 player starts grounded")
	world.rig_toggle.button_pressed = false
	check(not rig.visible and p.sprite.visible, "toggle off restores original A0 sprite")
	world.rig_toggle.button_pressed = true
	check(rig.visible and not p.sprite.visible, "toggle on replaces only the sprite")
	world.bow_toggle.button_pressed = true
	check(rig.shapes.bow.visible and not rig.shapes.dao.visible, "bow toggle swaps weapon")
	world.bow_toggle.button_pressed = false
	world._sync_rig()
	check(rig.current_clip == "idle", "real idle state selects idle")
	action("right",true)
	await tick(3)
	check(rig.current_clip == "run", "real movement selects run")
	action("right",false)
	await tick(8)
	action("left",true)
	await tick(1)
	check(rig.current_clip == "turn", "real reversal selects turn")
	action("left",false)
	await tick(5)
	action("slash",true)
	await tick(2)
	check(rig.current_clip == "slash_1", "real slash selects basic dao clip")
	action("slash",false)
	await tick(30)
	world.bow_toggle.button_pressed = true
	action("slash",true)
	await tick(2)
	check(rig.current_clip == "shoot", "real slash input with bow selects shoot preview")
	action("slash",false)
	await tick(30)
	world.bow_toggle.button_pressed = false
	var initial_flips: int = p.flip_completion_count
	action("jump",true)
	await tick(1)
	action("jump",false)
	check(rig.current_clip == "jump_up", "real jump selects ascent")
	var saw_flip := false
	var saw_fall := false
	var flip_in_air := false
	for i in 65:
		await tick(1)
		saw_flip = saw_flip or rig.current_clip == "apex_flip"
		saw_fall = saw_fall or rig.current_clip == "fall"
		if p.flip_completion_count > initial_flips and not p.is_on_floor():
			flip_in_air = true
	check(saw_flip and saw_fall, "real flight selects apex flip then fall")
	check(flip_in_air and p.is_on_floor(), "real 360 flip completes before same-height landing")
	# Khinh cong: fresh press only in the existing A0 window, no controller changes.
	var initial_extra: int = p.extra_jump_count
	initial_flips = p.flip_completion_count
	action("jump",true)
	await tick(1)
	action("jump",false)
	for i in 35:
		if p.velocity.y < 0 and absf(p.velocity.y) <= absf(p.tuning.jump_speed()) * 0.28:
			break
		await tick(1)
	action("jump",true)
	await tick(1)
	action("jump",false)
	check(p.extra_jump_count == initial_extra+1, "real khinh cong activates unchanged")
	var completed_air := false
	for i in 95:
		await tick(1)
		if p.flip_completion_count >= initial_flips+2 and not p.is_on_floor():
			completed_air = true
	check(completed_air and p.is_on_floor(), "both khinh-cong flips finish before landing")
	check(p.rotation == 0 and p.scale == Vector2.ONE and p.slash.rotation == 0, "visual rig never rotates/scales body or slash hitbox")
	world.queue_free()
	await tick(2)
	print("Rig smoke failures: %d" % failures)
	quit(1 if failures else 0)
