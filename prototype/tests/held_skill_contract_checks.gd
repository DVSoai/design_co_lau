extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate();root.add_child(a);a.autoplay=false;a.set_process(false)
	for school in ["kiem","cung"]:
		a.set_school(school)
		for direction in [-1,1]:
			a.set_facing(direction)
			for frame in 30:
				a.sample_frame(frame)
				check(a.sprites.weapon.visible==(frame in range(8) or frame in [12,21]),"%s frame%d dir%d held-state contract" % [school,frame,direction])
			if school=="kiem":
				for action in ["slash","tram_kiem"]:
					a.action=action
					for airborne in [false,true]:
						a.airborne=airborne;var total:=0.0
						for i in a.beats().size():
							total+=float(a.beats()[i].duration);a.sample_beat(i,false)
						check(absf(total-.3)<.000001 and a.skills_data[action].hit_window==[.1,.2],"six source beats .30s; hit .10–.20 unchanged")
	a.set_school("cung");a.action="shoot";a.airborne=false
	check(a.beats().size()==8,"bow eight source beats")
	for i in 8:
		a.clear_arrows();a.sample_beat(i,true)
		check(a.arrows.size()==(1 if i==4 else 0),"bow beat%d projectile only at fifth beat" % (i+1))
	print("Held-state/skill timing contracts failures=%d (visual acceptance uses ablation images)" % failures);a.free();quit(1 if failures else 0)
