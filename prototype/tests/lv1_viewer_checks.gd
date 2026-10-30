extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok:failures+=1
func run() -> void:
	var viewer=load("res://pose_rig/pose_rig.tscn").instantiate()
	root.add_child(viewer)
	check(viewer.samples.size()==31,"30 static frames plus independent live preview")
	for direction in [1,-1]:
		viewer.direction=direction
		viewer.rebuild()
		var boxes: Array[Rect2]=[]
		for i in 30:
			var a: Node2D=viewer.samples[i]
			var box: Rect2=viewer.actor_bounds(a)
			check(Rect2(0,70,1600,650).encloses(box),"dir%d frame%d bounds=%s inside strip" % [direction,i,str(box)])
			for j in boxes.size():check(not boxes[j].intersects(box),"dir%d frames%d/%d no overlap" % [direction,j,i])
			boxes.append(box)
	for school in ["kiem","cung"]:
		viewer.school=school
		viewer.page="compare"
		viewer.rebuild()
		var a: Node2D=viewer.actor
		var top:=INF
		var bottom:=-INF
		for id in ["head","body","legs"]:
			var s: Sprite2D=a.sprites[id]
			var r:=Rect2(s.texture.get_image().get_used_rect())
			top=minf(top,s.to_global(r.position).y)
			bottom=maxf(bottom,s.to_global(r.end).y)
		check(absf(bottom-top-128)<.1,"%s actual viewer human alpha height=%.6f px, target128" % [school,bottom-top])
	for school in ["kiem","cung"]:
		for direction in [1,-1]:
			viewer.school=school
			viewer.direction=direction
			viewer.page="attacks"
			viewer.rebuild()
			for a in viewer.samples:
				a.set_process(false)
				if a.autoplay:
					for i in a.skills_data[a.action].ground.size():
						a.clear_arrows()
						a.sample_beat(i,true)
						check(Rect2(0,70,1600,650).encloses(viewer.actor_bounds(a)),"%s dir%d live %s beat%d fits viewport" % [school,direction,a.action,i])
				else:
					check(Rect2(0,70,1600,650).encloses(viewer.actor_bounds(a)),"%s dir%d static attack fits viewport" % [school,direction])
	print("Lv1 viewer checks failures=%d" % failures)
	viewer.free()
	quit(1 if failures else 0)
