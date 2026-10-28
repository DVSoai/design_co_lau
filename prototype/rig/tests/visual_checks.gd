extends SceneTree
var failures := 0
func check(ok: bool, message: String) -> void:
	print(("PASS: " if ok else "FAIL: ") + message)
	if not ok:
		failures += 1
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var rig = load("res://rig/rig.tscn").instantiate()
	root.add_child(rig)
	for direction in [1.0, -1.0]:
		rig.scale.x = direction
		var correct_layers := true
		var attached := true
		var grounded := true
		var bow_correct := true
		var string_correct := true
		var planted := true
		for key in rig.clips:
			rig.set_weapon(rig.clips[key].weapon)
			var time := 0.0
			for frame in rig.clips[key].frames:
				rig.sample(key, time)
				for stem in ["upper_arm", "forearm", "hand", "thigh", "shin", "foot"]:
					correct_layers = correct_layers and rig.shapes[stem+"_near"].z_index > rig.shapes[stem+"_far"].z_index
				for part in rig.definition.parts:
					if part.parent != "":
						var parent: Node2D = rig.joints[part.parent]
						var node: Node2D = rig.joints[part.id]
						attached = attached and node.global_position.distance_to(parent.to_global(Vector2(part.attach[0], part.attach[1]))) < 0.001
				for side in ["near", "far"]:
					var shape: Polygon2D = rig.shapes["foot_"+side]
					var bottom := -INF
					for point in shape.polygon:
						bottom = maxf(bottom, (shape.to_global(point)-rig.global_position).y)
					if key in ["idle", "land", "slash_1", "slash_2", "slash_3"]:
						grounded = grounded and absf(bottom) < 0.001
					if key == "run":
						var ankle: Vector2 = rig.joints["foot_"+side].global_position-rig.global_position
						if absf(bottom) < 0.001:
							planted = planted and is_equal_approx(ankle.y, -4.0)
						planted = planted and bottom <= 0.001
				if key == "shoot":
					var bow: Node2D = rig.joints.bow
					var hand: Node2D = rig.joints.hand_far
					var shoulder: Vector2 = rig.joints.upper_arm_far.global_position
					var axis := bow.to_global(Vector2(0,19))-bow.to_global(Vector2(0,-19))
					bow_correct = bow_correct and absf(axis.x) < 0.001 and bow.global_position.distance_to(hand.global_position) < 0.001 and is_equal_approx(hand.global_position.y,shoulder.y) and (hand.global_position.x-shoulder.x)*direction > 27.9
					var anchor: Vector2 = rig.joints.hand_near.to_global(Vector2(0,1))
					string_correct = string_correct and rig.bow_string.visible and rig.bow_string.to_global(rig.bow_string.points[1]).distance_to(anchor) < 0.001
				time += float(frame.duration)
		check(correct_layers, "direction %+.0f: near layers remain above far in every clip" % direction)
		check(attached, "direction %+.0f: all parent anchors stay connected" % direction)
		check(grounded, "direction %+.0f: idle/land/slashes feet touch ground" % direction)
		check(planted, "direction %+.0f: run contact feet stay on ground, swing clears it" % direction)
		check(bow_correct, "direction %+.0f: bow vertical, centred on far hand; far arm horizontal" % direction)
		check(string_correct, "direction %+.0f: bow string follows near pulling hand" % direction)
	rig.free()
	print("Rig visual failures: %d" % failures)
	quit(1 if failures else 0)
