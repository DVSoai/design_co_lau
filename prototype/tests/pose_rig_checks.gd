extends SceneTree
var failures := 0
func _initialize() -> void: call_deferred("run")
func check(ok: bool, text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok: failures+=1
func opaque_bounds(sprite: Sprite2D) -> Rect2:
	var image := sprite.texture.get_image()
	var low := Vector2(image.get_width(),image.get_height())
	var high := Vector2.ZERO
	for y in image.get_height():
		for x in image.get_width():
			if image.get_pixel(x,y).a > .5:
				low = low.min(Vector2(x,y))
				high = high.max(Vector2(x+1,y+1))
	return Rect2(sprite.position+low*.5,(high-low)*.5)
func run() -> void:
	var rig = load("res://pose_rig/rig_frames.tscn").instantiate()
	root.add_child(rig)
	rig.autoplay=false
	var expected := {"idle":4,"run":6,"jump":2,"fall":2,"slash":4}
	var total := 0
	for action in expected:
		check(rig.clips[action].frames.size()==expected[action],"%s exact frame count %d" % [action,expected[action]])
		for index in expected[action]:
			for direction in [1,-1]:
				rig.set_facing(direction)
				rig.sample(action,index)
				var transforms_ok: bool = rig.rotation==0 and rig.scale==Vector2(direction,1)
				for sprite: Sprite2D in rig.sprites.values():
					transforms_ok=transforms_ok and sprite.rotation==0 and sprite.scale==Vector2(.5,.5) and sprite.texture_filter==CanvasItem.TEXTURE_FILTER_LINEAR
				check(transforms_ok,"%s/%d dir%d zero rotation; 2x image scale .5; flip root only; linear" % [action,index+1,direction])
				var f: Dictionary = rig.clips[action].frames[index]
				var hip_gap: float = (rig.sprites.body.position+rig.point(f.body,"hip")).distance_to(rig.sprites.legs.position+rig.point(f.legs,"hip"))
				var neck_gap: float = (rig.sprites.head.position+rig.point(f.head,"neck")).distance_to(rig.sprites.body.position+rig.point(f.body,"neck"))
				check(hip_gap<=1 and neck_gap<=1,"%s/%d dir%d hip_gap=%.6f neck_gap=%.6f" % [action,index+1,direction,hip_gap,neck_gap])
				if action in ["idle","run"]:
					var ground := opaque_bounds(rig.sprites.legs).end.y
					check(absf(ground)<.001,"%s/%d dir%d support sole_y=%.6f" % [action,index+1,direction,ground])
				if action=="slash" and index>=2:
					var tip: Vector2 = rig.landmarks.tip
					var face_x: float = opaque_bounds(rig.sprites.head).end.x
					check(tip.x>face_x,"slash/%d dir%d sword tip relative centre=(%.3f,%.3f), face_front=%.3f; forward=%s" % [index+1,direction,tip.x*direction,tip.y,face_x*direction,str(tip.x>face_x)])
				total+=1
	rig.set_facing(1)
	rig.sample("idle",0)
	var bounds: Rect2 = opaque_bounds(rig.sprites.legs).merge(opaque_bounds(rig.sprites.body)).merge(opaque_bounds(rig.sprites.head))
	check(absf(bounds.size.y-96)<.1 and absf(bounds.end.y)<.001,"idle silhouette height=%.6fpx (~96, source-anchor tolerance .1); sole0; frame128 bottom margin8" % bounds.size.y)
	var duration := 0.0
	for f in rig.clips.slash.frames: duration+=f.duration
	check(absf(duration-.30)<.000001,"slash total .30s")
	var rates_ok := true
	for f in rig.clips.idle.frames: rates_ok = rates_ok and absf(f.duration-1.0/6)<.000001
	for f in rig.clips.run.frames: rates_ok = rates_ok and absf(f.duration-1.0/12)<.000001
	for f in rig.clips.fall.frames: rates_ok = rates_ok and absf(f.duration-1.0/12)<.000001
	check(rates_ok and rig.clips.fall.loop,"idle6fps run12fps fall12fps/loop per09")
	var jump_time := 0.0
	for f in rig.clips.jump.frames: jump_time += f.duration
	check(absf(jump_time-.38)<.000001,"jump two frames total .38s per09/A0")
	# Geometry mirror of every actual layer corner must match across both directions.
	var corners: Array = []
	for direction in [1,-1]:
		rig.set_facing(direction)
		var current: Array = []
		for sprite: Sprite2D in rig.sprites.values(): current.append(sprite.to_global(Vector2.ZERO)-rig.global_position)
		corners.append(current)
	var mirrored := true
	for i in corners[0].size():mirrored=mirrored and corners[1][i].is_equal_approx(Vector2(-corners[0][i].x,corners[0][i].y))
	check(mirrored,"left/right actual layer corners mirror exactly; grip anchor follows same root")
	print("Pose rig: %d action/frame/direction checks; failures=%d" % [total,failures])
	rig.free()
	quit(1 if failures else 0)
