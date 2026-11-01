extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate();root.add_child(a);a.autoplay=false;a.set_process(false)
	var H: float=a.parts.presentation.standing_height_logic
	for school in ["kiem","cung"]:
		a.set_school(school)
		var texture_rid:=RID();var count:=0
		for direction in [-1,1]:
			a.set_facing(direction)
			for frame in [0,1,2,3,4,5,6,7,12,21]:
				a.sample_frame(frame);count+=1
				var w: Sprite2D=a.sprites.weapon;var id: String=a.parts.levels["1"].weapons[school]
				if not texture_rid.is_valid():texture_rid=w.texture.get_rid()
				check(w.visible and w.texture.get_rid()==texture_rid and a.landmarks.weapon_asset==id,"%s frame%d dir%d SAME held texture RID=%s" % [school,frame,direction,str(texture_rid)])
				check(w.rotation==0 and w.scale==Vector2(.5,.5) and w.z_index==-1,"held art uses fixed angle/scale/depth; only translation and root facing change")
				check(not a.frames_data.frames[frame].layers.weapon.has("cung_asset"),"no per-frame bow texture override")
				var grip:=w.to_global(a.anchor(id,"grip")*2);var hand: Vector2=a.to_global(a.landmarks.held_hand)
				check(grip.distance_to(hand)<=1,"grip coincides with actual painted fist gap=%.9f" % grip.distance_to(hand))
				var im: Image=w.texture.get_image();var at: Vector2=a.anchor(id,"grip")*2
				check(im.get_pixelv(Vector2i(at)).a>.8,"grip is on real opaque wrap pixels")
		var id: String=a.parts.levels["1"].weapons[school];var im: Image=a.sprites.weapon.texture.get_image();var box:=im.get_used_rect()
		if school=="kiem":
			var ratio:=maxf(box.size.x,box.size.y)*.5/H
			check(ratio>=.75 and ratio<=.8,"held sword real longest alpha side/H=%.9f [.75,.8]" % ratio)
		else:
			var axis: Vector2=(a.anchor(id,"top")-a.anchor(id,"bottom")).normalized();var lo:=INF;var hi:=-INF
			for y in im.get_height():
				for x in im.get_width():
					if im.get_pixel(x,y).a>=.5:
						var projected:=Vector2(x,y).dot(axis);lo=minf(lo,projected);hi=maxf(hi,projected)
			var ratio:=(hi-lo+1)*.5/H
			check(ratio>=.9 and ratio<=1,"held bow opaque axial span/H=%.9f [.9,1]" % ratio)
		check(count==20,"20 direction/frame samples use one texture")
		var master: Dictionary=a.parts.weapon_masters[school]
		check(maxf(master.master_size[0],master.master_size[1])==512,"master long side exactly512px")
	for id in ["attack_blade","attack_blade_only","swing_0","swing_1","swing_2","swing_3","swing_4","swing_skill_0","swing_skill_1","swing_skill_2","swing_skill_3","swing_skill_4"]:
		check(a.parts.assets[id].source.master==a.parts.weapon_masters.kiem.master,"%s derives steel directly from the same detailed sword master" % id)
	for retired in ["sword_hold","sword_run","bow_hold","run_v3_bow","carry_v4_bow"]:check(not a.parts.assets.has(retired),"obsolete held variant removed: "+retired)
	print("Shared weapon master checks failures=%d" % failures);a.free();quit(1 if failures else 0)
