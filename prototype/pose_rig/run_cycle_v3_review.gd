extends Node2D
func _ready() -> void:
	get_window().content_scale_size=Vector2i(1600,720)
	RenderingServer.set_default_clear_color(Color("202833"))
	var args:=OS.get_cmdline_user_args()
	var school:="cung" if "--cung" in args else "kiem"
	var direction: int=-1 if "--left" in args else 1
	var data: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/parts.json"))
	var label:=Label.new();label.position=Vector2(24,20);label.add_theme_font_size_override("font_size",24)
	label.text="Chạy2–7 / %s / %s / cỡ chuẩn128px / CHƯA DUYỆT" % [school,"trái" if direction<0 else "phải"]
	add_child(label)
	for row in 2:
		for i in 6:
			var holder:=Node2D.new();holder.position=Vector2(150+i*250,300+row*270);holder.scale=Vector2.ONE*float(data.presentation.display_factor);add_child(holder)
			var actor=load("res://pose_rig/rig_frames.tscn").instantiate();holder.add_child(actor)
			actor.set_school(school);actor.set_facing(direction);actor.autoplay=false;actor.set_process(false);actor.sample_frame(i+2)
			if row==1:
				for layer in ["head","body","weapon"]:actor.sprites[layer].visible=false
				actor.held_fingers.visible=false;actor.quiver.visible=false
			var caption:=Label.new();caption.position=Vector2(100+i*250,320+row*270);caption.text="Khung%d%s" % [i+2," / lớp chân" if row==1 else ""]
			add_child(caption)
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var path:="res://pose_rig/reports/run_v3_%s_%s.png" % [school,"left" if direction<0 else "right"]
	var err:=get_viewport().get_texture().get_image().save_png(path)
	print("Actual Godot run review %s 1600x720 error=%d" % [path,err]);get_tree().quit(0 if err==OK else 1)
