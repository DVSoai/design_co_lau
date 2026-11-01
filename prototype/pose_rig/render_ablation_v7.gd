extends Node
const VARIANTS=["full","no_weapon","no_body","no_legs","no_head","weapon_only","legs_only","body_only","head_only","fingers_only","no_fingers"]
func configure(a: Node2D,variant: String) -> void:
	var lower_visible: bool=a.held_lower_legs.visible
	var fingers_visible: bool=a.held_fingers.visible
	if variant.ends_with("_only"):
		for s: Sprite2D in a.all_visual_sprites():s.visible=false
		if variant=="fingers_only":a.held_fingers.visible=a.frames_data.frames[a.frame_index].held_visible
		else:
			var key: String={"weapon_only":"weapon","legs_only":"legs","body_only":"body","head_only":"head"}[variant]
			a.sprites[key].visible=true if key!="weapon" else a.frames_data.frames[a.frame_index].held_visible
			if key=="legs":a.held_lower_legs.visible=lower_visible
			if key=="body":a.held_fingers.visible=fingers_visible
	elif variant=="no_weapon":a.sprites.weapon.visible=false
	elif variant=="no_body":a.sprites.body.visible=false;a.held_fingers.visible=false
	elif variant=="no_legs":a.sprites.legs.visible=false;a.held_lower_legs.visible=false
	elif variant=="no_head":a.sprites.head.visible=false
	elif variant=="no_fingers":a.held_fingers.visible=false
func _ready() -> void:
	var out:="res://pose_rig/reports/ablation_v7"
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(out))
	var rigs: Array[Node2D]=[];var viewports: Array[SubViewport]=[]
	for variant: String in VARIANTS:
		var vp:=SubViewport.new();vp.size=Vector2i(256,256);vp.transparent_bg=true;vp.render_target_update_mode=SubViewport.UPDATE_ALWAYS;add_child(vp);viewports.append(vp)
		var holder:=Node2D.new();holder.position=Vector2(128,210);vp.add_child(holder)
		var actor=load("res://pose_rig/rig_frames.tscn").instantiate();holder.add_child(actor);holder.scale=Vector2.ONE*actor.parts.presentation.display_factor
		actor.autoplay=false;actor.set_process(false);rigs.append(actor)
	var entries: Array[Dictionary]=[];var failures:=0
	for school in ["kiem","cung"]:
		for direction in [-1,1]:
			for frame in 30:
				for i in rigs.size():
					var a=rigs[i];a.set_school(school);a.set_facing(direction);a.sample_frame(frame);configure(a,VARIANTS[i])
				await RenderingServer.frame_post_draw
				await RenderingServer.frame_post_draw
				var atlas:=Image.create(1024,768,false,Image.FORMAT_RGBA8)
				for i in viewports.size():atlas.blit_rect(viewports[i].get_texture().get_image(),Rect2i(0,0,256,256),Vector2i((i%4)*256,(i/4)*256))
				var file:="%s_%s_%02d.png" % [school,"left" if direction<0 else "right",frame]
				var err:=atlas.save_png(out.path_join(file));failures+=int(err!=OK)
				entries.append({"file":file,"school":school,"direction":direction,"frame":frame,"legs_texture":rigs[0].sprites.legs.texture.resource_path.get_file()})
				if frame%10==0:print("Actual Godot ablation %s dir%d frame%d;11 independently rendered variants error=%d" % [school,direction,frame,err])
	var manifest={"tile_size":256,"columns":4,"variants":VARIANTS,"entries":entries,"description":"Real Godot transparent RGBA, full actor and removal/isolation of every main layer; no claimed image landmarks."}
	var file:=FileAccess.open(out.path_join("manifest.json"),FileAccess.WRITE);file.store_string(JSON.stringify(manifest,"\t")+"\n");file.close()
	print("Actual ablation export:120 poses x11 variants=1320 renders in120 atlases; failures=%d" % failures);get_tree().quit(1 if failures else 0)
