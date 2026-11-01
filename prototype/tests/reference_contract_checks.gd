extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok:failures+=1
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate()
	root.add_child(a)
	a.autoplay=false
	a.set_process(false)
	var reference: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(ProjectSettings.globalize_path("res://")+"../docs/ref/so_lieu_tham_khao.json"))
	for row in 30:check(a.frames_data.frames[row].reference==reference.bang_30_khung[row],"frame%02d retains exact source row" % row)
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
						var offset: Array=fx.offsets[int((fx.elapsed+.000000001)/.05)]
						check(fx.sprite.position.distance_to(fx.origin+Vector2(offset[0],offset[1])*3)<.001,"actual numeric effect uses source offset and centered image")
	print("Reference frame/skill/effect numeric contracts failures=%d (not visual acceptance)" % failures)
	a.free()
	quit(1 if failures else 0)
