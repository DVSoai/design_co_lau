extends SceneTree
var failures := 0
func _initialize() -> void:call_deferred("run")
func check(ok: bool, text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok:failures+=1
func world_point(rig: Node2D, point: Vector2) -> Vector2:
	return rig.to_global(point)-rig.global_position
func run() -> void:
	var rig=load("res://pose_rig/rig_frames.tscn").instantiate()
	root.add_child(rig)
	rig.autoplay=false
	rig.set_process(false)
	var sampled := 0
	for school in ["kiem","cung"]:
		rig.set_school(school)
		var expected: Dictionary = {"idle":4,"run":6,"jump":2,"fall":2,"slash":5,"thrust":2} if school=="kiem" else {"idle":4,"run":6,"jump":2,"fall":2,"shoot":3,"run_shoot":2}
		check(rig.clips.size()==expected.size(),school+" exact action set")
		for action_name in expected:check(rig.clips[action_name].frames.size()==expected[action_name],school+" "+action_name+" exact frame count")
		for name_ in rig.clips:
			for index in rig.clips[name_].frames.size():
				for direction in [1,-1]:
					rig.clear_arrows()
					rig.set_facing(direction)
					rig.sample(name_,index)
					var valid: bool = rig.rotation==0 and rig.scale==Vector2(direction,1)
					for sprite: Sprite2D in rig.all_visual_sprites():valid=valid and sprite.rotation==0 and sprite.scale==Vector2(.5,.5)
					for arrow: Sprite2D in rig.arrows:valid=valid and arrow.rotation==0 and arrow.scale==Vector2(.5,.5)
					check(valid,"%s %s/%d dir%d all Sprite2D rotation0, only root flip" % [school,name_,index+1,direction])
					var f: Dictionary=rig.clips[name_].frames[index]
					var nocked_expected: bool=school=="cung" and name_ in ["shoot","run_shoot"] and f.weapon=="cung_3"
					check(rig.nocked_arrow.visible==nocked_expected,"%s %s/%d dir%d nocked arrow only during pull" % [school,name_,index+1,direction])
					if nocked_expected:
						var tail_raw: Array=rig.swing_data.arrow.tail
						var tip_raw: Array=rig.swing_data.arrow.tip
						var actual_tail: Vector2=rig.nocked_arrow.to_global(Vector2(tail_raw[0],tail_raw[1]))-rig.global_position
						var actual_tip: Vector2=rig.nocked_arrow.to_global(Vector2(tip_raw[0],tip_raw[1]))-rig.global_position
						var string_at: Vector2=world_point(rig,rig.landmarks.string)
						var bow_at: Vector2=world_point(rig,rig.landmarks.weapon_grip)
						check(actual_tail.distance_to(string_at)<=1 and direction*(actual_tip.x-bow_at.x)>0,"nocked dir%d tail=%s string=%s tip=%s bow=%s" % [direction,str(actual_tail),str(string_at),str(actual_tip),str(bow_at)])
					if school=="kiem" and name_ in ["slash","thrust"]:
						var hand: Vector2=world_point(rig,rig.sprites.body.position+rig.point(f.body,"grip"))
						var grip: Vector2=world_point(rig,rig.landmarks.weapon_grip)
						var tip: Vector2=world_point(rig,rig.landmarks.tip)
						var forward: float=direction*(tip.x-grip.x)
						var raised: bool=name_=="slash" and index==0
						check(grip.distance_to(hand)<=2 and ((tip.y<grip.y) if raised else forward>0),"%s/%d dir%d hand=%s grip=%s tip=%s gap=%.6f forward=%.3f raised=%s" % [name_,index+1,direction,str(hand),str(grip),str(tip),grip.distance_to(hand),forward,str(raised)])
					if school=="cung" and name_ in ["shoot","run_shoot"]:
						var release_expected: bool = (name_=="shoot" and index==2) or (name_=="run_shoot" and index==1)
						check(f.spawn==release_expected and rig.arrows.size()==(1 if release_expected else 0),"%s/%d dir%d arrow spawn only on release" % [name_,index+1,direction])
						var grip: Vector2=world_point(rig,rig.landmarks.weapon_grip)
						var hand: Vector2=world_point(rig,rig.landmarks.far_hand)
						var belly: Vector2=world_point(rig,rig.landmarks.belly)
						var string: Vector2=world_point(rig,rig.landmarks.string)
						var front: float=direction*(belly.x-string.x)
						check(front>0 and grip.distance_to(hand)<=2,"%s/%d dir%d bow grip=%s far_hand=%s belly=%s string=%s grip_gap=%.6f front=%.3f" % [name_,index+1,direction,str(grip),str(hand),str(belly),str(string),grip.distance_to(hand),front])
						if f.weapon=="cung_3":
							var near_hand: Vector2=world_point(rig,rig.landmarks.near_hand)
							check(string.distance_to(near_hand)<=3,"%s/%d dir%d drawn string=%s near_hand=%s gap=%.6f" % [name_,index+1,direction,str(string),str(near_hand),string.distance_to(near_hand)])
						if f.spawn:
							check(rig.arrows.size()==1,"release spawns exactly one separate arrow")
							var arrow: Sprite2D=rig.arrows[0]
							var tail: Vector2=world_point(rig,arrow.position+rig.point(rig.arrow_asset,"tail"))
							var tip: Vector2=world_point(rig,arrow.position+rig.point(rig.arrow_asset,"tip"))
							var before: float=direction*tip.x
							rig.advance_arrows(.1)
							var after: Vector2=world_point(rig,arrow.position+rig.point(rig.arrow_asset,"tip"))
							check(direction*(tip.x-tail.x)>0 and direction*after.x>before,"arrow dir%d tail=%s tip=%s tip_after0.1s=%s forward_travel=%.3f" % [direction,str(tail),str(tip),str(after),direction*after.x-before])
					sampled+=1
	# All3levels x all attack beats x both directions, measured from Sprite2D transforms.
	rig.set_school("kiem")
	var body_states: Dictionary={}
	var template_checks:=0
	for level in [1,30,60]:
		rig.set_weapon_level(level)
		for clip_name in ["slash","thrust"]:
			for index in rig.clips[clip_name].frames.size():
				for direction in [1,-1]:
					rig.set_facing(direction)
					rig.sample(clip_name,index)
					var f: Dictionary=rig.clips[clip_name].frames[index]
					var b: Dictionary=rig.swing_data.levels[str(level)].blades[f.swing_angle]
					var grip: Vector2=rig.blade_sprite.to_global(Vector2(b.grip[0],b.grip[1]))-rig.global_position
					var tip: Vector2=rig.blade_sprite.to_global(Vector2(b.tip[0],b.tip[1]))-rig.global_position
					var raw: Array=rig.anchors[f.body].anchors.grip
					var hand: Vector2=rig.sprites.body.to_global(Vector2(raw[0],raw[1]))-rig.global_position
					var raised: bool=clip_name=="slash" and index==0
					var ok: bool=grip.distance_to(hand)<=1 and ((tip.y<grip.y) if raised else direction*(tip.x-grip.x)>0)
					check(ok,"level%d %s/%d dir%d actual grip=%s hand=%s tip=%s gap=%.6f" % [level,clip_name,index+1,direction,str(grip),str(hand),str(tip),grip.distance_to(hand)])
					check(not rig.sprites.weapon.visible and rig.blade_sprite.visible,"held weapon hidden, selected baked blade visible")
					if f.trail!=null:
						var centre: Vector2=rig.trail_sprite.global_position-rig.global_position
						check(rig.trail_sprite.visible and rig.trail_sprite.centered and direction*(centre.x-grip.x)>0,"shared trail%s dir%d centre=%s grip=%s; centred and forward" % [f.trail,direction,str(centre),str(grip)])
					else:check(not rig.trail_sprite.visible,"no trail on preparation/thrust")
					var rotations_ok: bool=rig.rotation==0 and rig.scale==Vector2(direction,1)
					for sprite: Sprite2D in rig.all_visual_sprites():rotations_ok=rotations_ok and sprite.rotation==0 and sprite.scale==Vector2(.5,.5)
					check(rotations_ok,"all Sprite2Drotation0, static2xscale; root flip only")
					var key: String=clip_name+str(index)+str(direction)
					var state: Array=[rig.sprites.body.position,rig.sprites.head.position,rig.sprites.legs.position]
					if level==1:body_states[key]=state
					else:check(state==body_states[key],"body/head/legs transforms identical across levels")
					template_checks+=1
	rig.set_facing(1)
	rig.sample("slash",0)
	rig.elapsed=0
	rig.autoplay=true
	for tick in 18:rig._process(1.0/60)
	check(rig.action=="idle" and not rig.blade_sprite.visible and not rig.trail_sprite.visible and rig.sprites.weapon.visible,"slash completes in18ticks/60fps=.30s, returns idle and clears blade/trail")
	# Switching class must never leave both weapon families equipped/visible.
	rig.autoplay=false
	rig.set_school("kiem")
	rig.sample("slash",2)
	rig.set_school("cung")
	check(not rig.blade_sprite.visible and not rig.trail_sprite.visible and rig.sprites.weapon.visible and rig.sprites.weapon.texture.resource_path.ends_with("cung_1.png"),"switch Kiếm attack -> Cung: no sword or sword trail remains; bow only")
	rig.sample("shoot",2)
	check(rig.arrows.size()==1,"Cung release creates separate arrow before switch")
	rig.set_school("kiem")
	check(rig.arrows.is_empty() and not rig.nocked_arrow.visible and not rig.blade_sprite.visible and rig.sprites.weapon.visible and rig.sprites.weapon.texture.resource_path.ends_with("kiem_1.png"),"switch Cung release -> Kiếm: bow/nocked/flying arrows cleared; sword only")
	print("Template attack frame/level/direction checks=%d" % template_checks)
	print("Weapon-direction sampled frame/direction pairs=%d; failures=%d" % [sampled,failures])
	rig.free()
	quit(1 if failures else 0)
