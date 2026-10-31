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
	check(a.frames_data.frames.size()==30,"exactly30 frame rows")
	for layer in ["head","body","legs"]:
		check(a.parts.levels["1"][layer].size()==({"head":8,"body":18,"legs":10}[layer]),"Lv1 "+layer+" exact common-layer count")
	var cases:=0
	for school in ["kiem","cung"]:
		a.set_school(school)
		for dir in [-1,1]:
			a.set_facing(dir)
			for i in 30:
				a.sample_frame(i)
				var f: Dictionary=a.frames_data.frames[i]
				var ok: bool=f.layers.size()==4 and a.scale==Vector2(dir,1)
				for s: Sprite2D in a.all_visual_sprites():ok=ok and s.rotation==0
				check(ok,"%s frame%d dir%d four layers, rotation0 root flip" % [school,i,dir])
				check(a.quiver.visible==(school=="cung") and a.sprites.weapon.texture.resource_path.ends_with("sword_run.png" if school=="kiem" and i in range(2,8) else ("sword_hold.png" if school=="kiem" else "bow_hold.png")),"exclusive class weapon/quiver")
				cases+=1
		for id in a.skills_data:
			if a.skills_data[id].school!=school:continue
			for air in [false,true]:
				a.airborne=air
				for dir in [-1,1]:
					a.set_facing(dir)
					a.action=id
					for i in a.beats().size():
						a.clear_arrows()
						a.sample_beat(i,true)
						var beat: Dictionary=a.beats()[i]
						check(beat.effects.size()<=3 and not a.sprites.weapon.visible,"%s air%s dir%d beat%d <=3fx held weapon hidden" % [id,air,dir,i])
						var rotation_ok:=true
						for s: Sprite2D in a.all_visual_sprites():rotation_ok=rotation_ok and s.rotation==0
						check(rotation_ok,"all skill sprites rotation0")
						if school=="kiem":
							var gap: float=a.landmarks.weapon_grip.distance_to(a.landmarks.grip)
							var forward: float=a.landmarks.tip.x-a.landmarks.grip.x
							var centre: Vector2=a.effect_sprites[0].position
							var blade: Sprite2D=a.effect_sprites[0]
							var asset: String=a.effects_data[beat.effects[0].id].frames[0].asset
							var grip_world: Vector2=blade.to_global(a.anchor(asset,"grip")*2-blade.texture.get_size()/2)
							var hand_world: Vector2=a.to_global(a.landmarks.grip)
							check(grip_world.distance_to(hand_world)<=1 and blade.centered,"actual centred Sprite2D grip-to-hand <=1")
							check(gap<=1 and forward>0,"sword actual grip gap=%.6f tip_forward=%.3f composite_centre_offset=%.3f" % [gap,forward,centre.x-a.landmarks.grip.x])
						else:
							check(a.landmarks.belly.x>a.landmarks.string.x,"bow belly forward, string behind")
							check(a.nocked_arrow.visible==beat.nocked and a.arrows.size()==(1 if beat.projectile!=null else 0),"nocked only draw; separate projectile only release")
							if beat.nocked:
								var ready: String=beat.get("nocked_asset","arrow")
								var tail: Vector2=a.nocked_arrow.position+a.anchor(ready,"tail")
								check(tail.distance_to(a.landmarks.string)<=1,"nocked tail on string")
								var tip: Vector2=a.nocked_arrow.position+a.anchor(ready,"tip")
								check(tip.x>a.landmarks.far_hand.x,"nocked arrow tip beyond bow")
								check(a.landmarks.string.distance_to(a.landmarks.near_hand)<=1,"V string meets actual near-hand anchor")
						cases+=1
	# Actual timed playback, including exact hit interval and spawn edges.
	a.airborne=false
	a.set_school("kiem")
	a.autoplay=true
	a.play("slash")
	for tick in 30:
		a._process(.01)
		var t: float=(tick+1)*.01
		if tick<29:check(a.hit_active==(t>=.1-0.000001 and t<.2-0.000001),"slash t=%.2f hit=%s window .10-.20" % [t,a.hit_active])
	check(a.action=="idle" and not a.hit_active,"slash exactly .30s and clears hit")
	a.set_school("cung")
	a.play("shoot")
	var releases: int=a.release_count
	for tick in 19:a._process(.01)
	check(a.release_count==releases,"no projectile before release .20s")
	a._process(.01)
	check(a.release_count==releases+1 and not a.nocked_arrow.visible,"one separate projectile at release .20s")
	a.set_school("kiem")
	check(a.arrows.is_empty() and not a.quiver.visible and not a.nocked_arrow.visible,"switch clears Cung accessories and projectiles")
	a.play("apex_flip")
	for tick in 4:
		check(a.frame_index==8+tick,"baked somersault phase %d, zero runtime rotation" % tick)
		a._process(.05)
	check(a.action=="fall" and a.frame_index==22,"360 cycle completes at .20s and returns upright fall")
	print("Frames30 checks cases=%d failures=%d" % [cases,failures])
	a.free()
	quit(1 if failures else 0)
