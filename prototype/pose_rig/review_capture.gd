extends Node
## Actual Godot offscreen renders for temporary three-way comparison, no foreign art.
var out_dir:="/tmp/ref_render/own"
var view: SubViewport
var holder: Node2D
var actor: Node2D
var files: Array=[]
var human_bounds: Dictionary={}
func _ready() -> void:
	var args:=OS.get_cmdline_user_args()
	if "--out" in args:out_dir=args[args.find("--out")+1]
	assert(out_dir.begins_with("/tmp/"))
	DirAccess.make_dir_recursive_absolute(out_dir)
	view=SubViewport.new()
	view.size=Vector2i(640,480)
	view.transparent_bg=true
	view.render_target_update_mode=SubViewport.UPDATE_ALWAYS
	add_child(view)
	holder=Node2D.new()
	holder.position=Vector2(240,280)
	var p: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/parts.json"))
	holder.scale=Vector2.ONE*float(p.presentation.display_factor)
	view.add_child(holder)
	actor=load("res://pose_rig/rig_frames.tscn").instantiate()
	holder.add_child(actor)
	actor.autoplay=false
	actor.set_process(false)
	for school in ["kiem","cung"]:
		actor.set_school(school)
		actor.sample_frame(0)
		actor.sprites.weapon.visible=false
		actor.quiver.visible=false
		await save_image(school+"_body00")
		var im:=view.get_texture().get_image()
		human_bounds[school]=var_to_str(im.get_used_rect())
		for frame in 30:
			actor.clear_arrows()
			actor.sample_frame(frame)
			await save_image("%s_frame%02d" % [school,frame])
		for skill in (["slash","tram_kiem"] if school=="kiem" else ["shoot","xa_tien"]):
			actor.action=skill
			for index in actor.skills_data[skill].ground.size():
				actor.clear_arrows()
				actor.sample_beat(index,true)
				await save_image("%s_%s_%02d" % [school,skill,index])
	var f:=FileAccess.open(out_dir+"/own_render_manifest.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"human_bounds":human_bounds,"actor_origin":[240,280],"files":files,"source":"actual Godot scene textures; no UI/no imagegen result"},"\t"))
	f.close()
	print("Temporary actual Godot review renders=%d; output=%s; standing body bounds=%s" % [files.size(),out_dir,str(human_bounds)])
	get_tree().quit()
func save_image(name_: String) -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var im:=view.get_texture().get_image()
	var path:=out_dir+"/"+name_+".png"
	var err:=im.save_png(path)
	assert(err==OK)
	files.append(name_+".png")
