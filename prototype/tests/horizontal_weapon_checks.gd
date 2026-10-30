extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok:failures+=1
func asset_point(a: Node2D,s: Sprite2D,id: String,key: String) -> Vector2:
	return s.to_global(a.anchor(id,key)*2-(s.texture.get_size()/2 if s.centered else Vector2.ZERO))
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate()
	root.add_child(a)
	a.autoplay=false
	a.set_process(false)
	for school in ["kiem","cung"]:
		a.set_school(school)
		for dir in [-1,1]:
			a.set_facing(dir)
			for frame in 30:
				a.sample_frame(frame)
				var held: Sprite2D=a.sprites.weapon
				var expected: bool=frame in range(8) or frame in [12,13]
				check(held.visible==expected,"%s dir%d frame%d held-visible=%s; hide flip/attack" % [school,dir,frame,held.visible])
				if not expected:continue
				var id: String=a.parts.levels["1"].weapons[school]
				if school=="kiem" and frame in range(2,8):id=a.parts.levels["1"].run_weapon
				var grip: Vector2=asset_point(a,held,id,"grip")
				var hand: Vector2=a.to_global(a.landmarks.held_hand)
				check(grip.distance_to(hand)<=1,"held grip at actual front hand gap=%.6f" % grip.distance_to(hand))
				if school=="kiem":
					var tip: Vector2=asset_point(a,held,id,"tip")
					check(tip.y>grip.y and dir*(tip.x-grip.x)<0,"held sword dir%d frame%d tip behind/down vector=%s" % [dir,frame,str(tip-grip)])
				else:
					var body: Sprite2D=a.sprites.body
					var centre: Vector2=held.to_global(Rect2(held.texture.get_image().get_used_rect()).get_center())
					var body_centre: Vector2=body.to_global(Rect2(body.texture.get_image().get_used_rect()).get_center())
					var top: Vector2=asset_point(a,held,id,"top")
					var bottom: Vector2=asset_point(a,held,id,"bottom")
					check(dir*(centre.x-body_centre.x)>0 and dir*(top.x-bottom.x)>0,"held bow dir%d frame%d centre forward=%.3f top forward of bottom=%.3f" % [dir,frame,dir*(centre.x-body_centre.x),dir*(top.x-bottom.x)])
			if school=="kiem":
				for action in ["slash","tram_kiem"]:
					a.action=action
					for airborne in [false,true]:
						a.airborne=airborne
						var total:=0.0
						for i in a.beats().size():
							var beat: Dictionary=a.beats()[i]
							total+=beat.duration
							a.sample_beat(i,false)
							var s: Sprite2D=a.effect_sprites[0]
							var id: String=a.effects_data[beat.effects[0].id].frames[0].asset
							var g: Vector2=asset_point(a,s,id,"grip")
							var tip: Vector2=asset_point(a,s,id,"tip")
							var hand: Vector2=a.to_global(a.landmarks.grip)
							var h: float=a.global_position.y-tip.y
							check(dir*(tip.x-g.x)>0 and absf(tip.y-g.y)<.1 and g.distance_to(hand)<=1,"%s air%s dir%d beat%d horizontal actual grip gap=%.6f" % [action,airborne,dir,i,g.distance_to(hand)])
							if a.parts.assets[id].get("pose_role","") in ["sweep","hold"]:check(h>=.35*96 and h<=.65*96,"lia tip height=%.6f H=%.6f (range.35-.65H)" % [h,h/96])
						check(absf(total-.3)<.000001 and a.skills_data[action].hit_window==[.1,.2],"five compact beats .30s hit.10-.20")
	a.set_school("cung")
	a.action="shoot"
	a.airborne=false
	check(a.beats().size()==8,"bow eight beats: draw2 hold2 release1 recover3")
	for i in 8:
		a.clear_arrows()
		a.sample_beat(i,true)
		check(a.arrows.size()==(1 if i==4 else 0),"bow beat%d projectile only at fifth beat" % (i+1))
	print("Horizontal/held weapon checks failures=%d" % failures)
	a.free()
	quit(1 if failures else 0)
