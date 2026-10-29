extends SceneTree
## Evaluate the real rig scene with Godot; export its transformed polygons, not poses reconstructed in Python.
func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var rig = load("res://rig/rig.tscn").instantiate()
	root.add_child(rig)
	var output := {}
	var art := "--art" in OS.get_cmdline_user_args()
	rig.set_art_enabled(art)
	for name in Array(rig.clips.keys()) + ["run_left", "shoot_left"]:
		var key: String = name.trim_suffix("_left")
		rig.scale.x = -1.0 if name.ends_with("_left") else 1.0
		rig.set_weapon(rig.clips[key].weapon)
		var frames: Array = []
		var time := 0.0
		for frame in rig.clips[key].frames:
			rig.sample(key, time)
			frames.append({"time": time, "duration": frame.duration, "geometry": rig.geometry(), "joints": _joints(rig), "weapon_axes": _weapon_axes(rig)})
			time += float(frame.duration)
		output[name] = {"frames": frames, "duration": time, "status": rig.clips[key].status}
	if art:
		rig.scale.x = 1.0
		rig.set_weapon("dao")
		rig.sample("idle", 0)
		for id in rig.joints:
			rig.joints[id].rotation = 0.0
		rig.joints.body.position = Vector2.ZERO
		rig.pivot_root.position = Vector2(rig.definition.rotation_center[0],rig.definition.rotation_center[1])
		rig.pivot_root.rotation = 0.0
		output["standing_neutral"] = {"frames": [{"time":0,"duration":0,"geometry":rig.geometry(),"joints":_joints(rig)}],"status":"measurement pose only"}
	var file := FileAccess.open("res://rig/reports/evaluated_art_frames.json" if art else "res://rig/reports/evaluated_frames.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(output) + "\n")
	file.close()
	print("Exported actual rig scene: %d clips; art=%s" % [output.size(), art])
	rig.free()
	quit()

func _joints(rig: Node2D) -> Dictionary:
	var result := {}
	for id in rig.joints:
		var joint: Node2D = rig.joints[id]
		var point := joint.global_position-rig.global_position
		result[id] = [point.x, point.y]
	return result

# Export real scene axes even for a weapon hidden by the preview selector.
func _weapon_axes(rig: Node2D) -> Dictionary:
	var result := {}
	var points := {
		"dao_grip": rig.joints.dao.global_position,
		"dao_tip": rig.sprites.dao.to_global(Vector2(7.0, 0.5)),
		"near_elbow": rig.joints.forearm_near.global_position,
		"near_wrist": rig.joints.hand_near.global_position,
		"bow_grip": rig.joints.bow.global_position,
		"far_grip": rig.joints.hand_far.to_global(Vector2(rig.definition.bow_string.hand_anchor[0], rig.definition.bow_string.hand_anchor[1])),
		"bow_top": rig.joints.bow.to_global(Vector2(rig.definition.bow_string.top[0], rig.definition.bow_string.top[1])),
		"bow_bottom": rig.joints.bow.to_global(Vector2(rig.definition.bow_string.bottom[0], rig.definition.bow_string.bottom[1])),
		"far_elbow": rig.joints.forearm_far.global_position,
		"far_wrist": rig.joints.hand_far.global_position,
	}
	for key in points:
		var point: Vector2 = points[key] - rig.global_position
		result[key] = [point.x, point.y]
	return result
