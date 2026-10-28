extends SceneTree
## Evaluate the real rig scene with Godot; export its transformed polygons, not poses reconstructed in Python.
func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	var rig = load("res://rig/rig.tscn").instantiate()
	root.add_child(rig)
	var output := {}
	for key in rig.clips:
		rig.set_weapon(rig.clips[key].weapon)
		var frames: Array = []
		var time := 0.0
		for frame in rig.clips[key].frames:
			rig.sample(key, time)
			frames.append({"time": time, "duration": frame.duration, "geometry": rig.geometry()})
			time += float(frame.duration)
		output[key] = {"frames": frames, "duration": time, "status": rig.clips[key].status}
	var file := FileAccess.open("res://rig/reports/evaluated_frames.json", FileAccess.WRITE)
	file.store_string(JSON.stringify(output) + "\n")
	file.close()
	print("Exported actual rig scene: %d clips -> rig/reports/evaluated_frames.json" % output.size())
	rig.free()
	quit()
