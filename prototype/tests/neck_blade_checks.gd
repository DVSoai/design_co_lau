extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok:failures+=1
func point(a: Node2D,s: Sprite2D,id: String,key: String) -> Vector2:
	return s.to_global(a.anchor(id,key)*2-(s.texture.get_size()/2 if s.centered else Vector2.ZERO))
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate()
	root.add_child(a)
	a.autoplay=false
	a.set_process(false)
	var reference: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(ProjectSettings.globalize_path("res://")+"../docs/ref/so_lieu_tham_khao.json"))
	for row in 30:check(a.frames_data.frames[row].reference==reference.bang_30_khung[row],"frame%02d retains exact source row" % row)
	var cases:=0
	for school in ["kiem","cung"]:
		a.set_school(school)
		for direction in [-1,1]:
			a.set_facing(direction)
			for frame in 30:
				a.sample_frame(frame)
				var h:=point(a,a.sprites.head,a.landmarks.head_asset,"neck")
				var b:=point(a,a.sprites.body,a.landmarks.body_asset,"neck")
				check(h.distance_to(b)<=1,"%s frame%02d dir%d actual neck gap=%.6f px" % [school,frame,direction,h.distance_to(b)])
				var hip:=point(a,a.sprites.body,a.landmarks.body_asset,"hip")
				var leg:=point(a,a.sprites.legs,a.landmarks.legs_asset,"hip")
				check(hip.distance_to(leg)<=1,"actual body/legs hip joint <=1 px")
				cases+=1
	# Independently inspect painted flesh around the calibrated collar, not only JSON equality.
	for i in [11,13,15,16,17]:
		var id:="body_%d" % i
		var im: Image=load("res://pose_rig/art/lv1_30/"+a.parts.assets[id].file).get_image()
		var x:=int(a.anchor(id,"neck").x*2)
		var skin:=false
		for y in range(2,8):
			var c:=im.get_pixel(x,y)
			if c.a>.7 and c.r>.6 and c.g>.3 and c.r-c.g>.1:skin=true
		check(skin,"%s collar anchor lies on observed exposed neck pixels" % id)
	a.set_school("kiem")
	for skill in ["slash","tram_kiem"]:
		a.action=skill
		for air in [false,true]:
			a.airborne=air
			for direction in [-1,1]:
				a.set_facing(direction)
				for i in [2,3,4]:
					a.sample_beat(i)
					var id: String=a.effects_data[a.beats()[i].effects[0].id].frames[0].asset
					var sprite: Sprite2D=a.effect_sprites[0]
					var g:=point(a,sprite,id,"blade_root")
					var t:=point(a,sprite,id,"tip")
					var ratio:=g.distance_to(t)/float(a.parts.presentation.standing_height_logic)
					check(ratio>=.75 and ratio<=.8,"%s air%s dir%d beat%d full blade/H=%.6f" % [skill,air,direction,i,ratio])
	for school in ["kiem","cung"]:
		a.set_school(school)
		for skill in (["slash","tram_kiem"] if school=="kiem" else ["shoot","xa_tien"]):
			a.action=skill
			for mode in ["ground","air"]:
				a.airborne=mode=="air"
				var source: Array=reference.chieu[a.skills_data[skill].reference_skill][mode]
				check(a.beats().size()==source.size(),skill+" "+mode+" exact source beat count")
				for i in source.size():
					check(a.beats()[i].reference==source[i] and int(a.beats()[i].frame)==int(source[i].khung_than),"exact source body/effect/projectile beat row")
					a.sample_beat(i)
					for fx in a.reference_effects:
						var offset: Array=fx.offsets[0]
						check(fx.sprite.position.distance_to(fx.origin+Vector2(offset[0],offset[1])*3)<.001,"actual numeric effect uses source offset and centered image")
	print("Neck/blade checks: poses=%d failures=%d" % [cases,failures])
	a.free()
	quit(1 if failures else 0)
