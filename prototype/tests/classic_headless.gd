extends SceneTree
## CLI wrapper only; execute the existing unchanged RefCounted classic_checks.gd.
var failures := 0
func check(ok: bool, message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:
		failures += 1
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var scene = load("res://main.tscn").instantiate()
	root.add_child(scene)
	for i in 10:
		await physics_frame
		await process_frame
	await load("res://tests/classic_checks.gd").new().run(self,scene,check)
	scene.queue_free()
	await process_frame
	print("Classic checks failures: %d" % failures)
	quit(1 if failures else 0)
