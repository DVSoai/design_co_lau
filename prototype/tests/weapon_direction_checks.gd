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
		var expected: Dictionary = {"idle":4,"run":6,"jump":2,"fall":2,"slash":4,"thrust":2} if school=="kiem" else {"idle":4,"run":6,"jump":2,"fall":2,"shoot":3,"run_shoot":2}
		check(rig.clips.size()==expected.size(),school+" exact action set")
		for action_name in expected:check(rig.clips[action_name].frames.size()==expected[action_name],school+" "+action_name+" exact frame count")
		for name_ in rig.clips:
			for index in rig.clips[name_].frames.size():
				for direction in [1,-1]:
					rig.clear_arrows()
					rig.set_facing(direction)
					rig.sample(name_,index)
					var valid: bool = rig.rotation==0 and rig.scale==Vector2(direction,1)
					for sprite: Sprite2D in rig.sprites.values():valid=valid and sprite.rotation==0 and sprite.scale==Vector2(.5,.5)
					for arrow: Sprite2D in rig.arrows:valid=valid and arrow.rotation==0 and arrow.scale==Vector2(.5,.5)
					check(valid,"%s %s/%d dir%d all Sprite2D rotation0, only root flip" % [school,name_,index+1,direction])
					var f: Dictionary=rig.clips[name_].frames[index]
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
	print("Weapon-direction sampled frame/direction pairs=%d; failures=%d" % [sampled,failures])
	rig.free()
	quit(1 if failures else 0)
