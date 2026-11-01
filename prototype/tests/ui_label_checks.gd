extends SceneTree
const T=preload("res://config/tuning.gd")
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func run() -> void:
	var scene=load("res://pose_rig/play_test.tscn").instantiate();root.add_child(scene)
	await process_frame
	for dimensions in [Vector2i(960,540),Vector2i(1200,540)]:
		root.size=dimensions;scene.touch_controls.layout()
		for key in ["skill_1","skill_2"]:
			var button: Control=scene.touch_buttons[key];var font:=ThemeDB.fallback_font
			for row: String in button.caption.split("\n"):
				check(font.get_string_size(row,HORIZONTAL_ALIGNMENT_LEFT,-1,T.TOUCH_FONT_SIZE).x+8<=button.size.x,"%s label '%s' fits width at %s" % [key,row,str(dimensions)])
			check(font.get_height(T.TOUCH_FONT_SIZE)*2+8<=button.size.y,"two skill text lines fit height with padding")
	scene.queue_free();await process_frame
	print("UI label checks failures=%d" % failures)
	quit(1 if failures else 0)
