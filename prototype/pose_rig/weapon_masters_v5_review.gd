extends Node2D
func caption(text: String,at: Vector2,size: int=22) -> void:
	var label:=Label.new();label.text=text;label.position=at;label.add_theme_font_size_override("font_size",size);add_child(label)
func _ready() -> void:
	get_window().content_scale_size=Vector2i(1600,720);RenderingServer.set_default_clear_color(Color("202833"))
	var p: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/parts.json"))
	caption("Vũ khí Lv1 — bản gốc512px và nhân vật chuẩn H128px — CHƯA DUYỆT",Vector2(30,10),25)
	var viewports: Dictionary={}
	for school in ["kiem","cung"]:
		var master_path: String=ProjectSettings.globalize_path("res://").path_join("../"+p.weapon_masters[school].master).simplify_path()
		var master:=Sprite2D.new();master.centered=false;master.texture=ImageTexture.create_from_image(Image.load_from_file(master_path));master.position=Vector2(60,145) if school=="kiem" else Vector2(1000,65);add_child(master)
		if school=="cung":master.scale=Vector2.ONE*.85
		caption("Kiếm Lv1 • bản gốc" if school=="kiem" else "Cung Lv1 • bản gốc",Vector2(60,100) if school=="kiem" else Vector2(1000,40))
		var vp:=SubViewport.new();vp.size=Vector2i(256,256);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;add_child(vp)
		var id: String=p.levels["1"].weapons[school];var s:=Sprite2D.new();s.centered=false;s.texture=load("res://pose_rig/art/lv1_30/"+p.assets[id].file);s.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
		var factor: float=.5*p.presentation.display_factor;s.scale=Vector2.ONE*factor;s.position=Vector2(128,128)-Vector2(p.assets[id].anchors.grip[0],p.assets[id].anchors.grip[1])*factor;vp.add_child(s);viewports[school]=vp
		for i in 2:
			var holder:=Node2D.new();holder.position=Vector2((220 if school=="kiem" else 1000)+i*380,690);holder.scale=Vector2.ONE*p.presentation.display_factor;add_child(holder)
			var actor=load("res://pose_rig/rig_frames.tscn").instantiate();holder.add_child(actor);actor.autoplay=false;actor.set_process(false);actor.set_school(school);actor.sample_frame(0 if i==0 else 4)
			caption("%s • khung%d • H128" % ["Kiếm" if school=="kiem" else "Cung",0 if i==0 else 4],Vector2(holder.position.x-110,520),20)
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var failures:=0
	for school: String in viewports:
		var path:="res://pose_rig/reports/weapon_v5_%s_128.png" % school
		var err: int=viewports[school].get_texture().get_image().save_png(path);print("Actual Godot isolated weapon H128 %s 256x256 error=%d" % [path,err]);failures+=int(err!=OK)
	var path:="res://pose_rig/reports/weapon_v5_review.png";var err:=get_viewport().get_texture().get_image().save_png(path);print("Actual Godot master/character review %s 1600x720 error=%d" % [path,err]);failures+=int(err!=OK)
	get_tree().quit(1 if failures else 0)
