extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok:failures+=1
func actual_shaft(a: Node2D,s: Sprite2D,id: String) -> Vector2:
	var im:=s.texture.get_image()
	var t: Vector2=a.anchor(id,"tail")*2
	var tip: Vector2=a.anchor(id,"tip")*2
	var n:=0.0
	var sx:=0.0
	var sy:=0.0
	var sxx:=0.0
	var sxy:=0.0
	for y in im.get_height():
		for x in im.get_width():
			if x<=t.x+.22*(tip.x-t.x) or x>=t.x+.74*(tip.x-t.x):continue
			var c:=im.get_pixel(x,y)
			var color: bool=(c.r>205.0/255 and c.g>220.0/255 and c.b>230.0/255) if id=="skill_arrow" else (c.r>45.0/255 and c.r-c.g>10.0/255 and c.g-c.b>5.0/255 and c.b<170.0/255)
			if c.a>.5 and color:
				n+=1
				sx+=x
				sy+=y
				sxx+=x*x
				sxy+=x*y
	assert(n>20)
	var m: float=(n*sxy-sx*sy)/(n*sxx-sx*sx)
	return Vector2(m,(sy-m*sx)/n)
func line_gap(s: Sprite2D,line: Vector2,world: Vector2) -> float:
	var p:=s.to_local(world)
	return absf(line.x*p.x-p.y+line.y)/sqrt(1+line.x*line.x)*.5
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate()
	root.add_child(a)
	a.autoplay=false
	a.set_process(false)
	a.set_school("cung")
	for dir in [-1,1]:
		a.set_facing(dir)
		for skill in ["shoot","xa_tien"]:
			a.action=skill
			for i in a.beats().size():
				a.clear_arrows()
				a.sample_beat(i,true)
				var beat: Dictionary=a.beats()[i]
				var bow: Sprite2D=a.effect_sprites[0]
				var bid: String=a.effects_data[beat.effects[0].id].frames[0].asset
				var rest: Vector2=bow.to_global(a.anchor(bid,"grip")*2-bow.texture.get_size()/2)
				var string: Vector2=bow.to_global(a.anchor(bid,"string")*2-bow.texture.get_size()/2)
				if beat.nocked:
					var id: String=beat.nocked_asset
					var line:=actual_shaft(a,a.nocked_arrow,id)
					var gap:=line_gap(a.nocked_arrow,line,rest)
					var tail: Vector2=a.nocked_arrow.to_global(a.anchor(id,"tail")*2)
					check(gap<=1 and tail.distance_to(string)<=1,"%s dir%d beat%d actual shaft/rest gap=%.6f nock/string gap=%.6f" % [skill,dir,i+1,gap,tail.distance_to(string)])
				if beat.projectile!=null:
					var id: String=beat.projectile.id
					var arrow: Sprite2D=a.arrows[0]
					var line:=actual_shaft(a,arrow,id)
					var gap:=line_gap(arrow,line,rest)
					var tail: Vector2=arrow.to_global(a.anchor(id,"tail")*2)
					check(gap<=1 and tail.distance_to(string)<=1,"%s dir%d release actual shaft/rest gap=%.6f tail starts at released string, gap=%.6f" % [skill,dir,gap,tail.distance_to(string)])
					check(arrow.rotation==0 and a.nocked_arrow.rotation==0,"pre-baked axes, every Sprite2Drotation0")
	print("Arrow actual shaft/nock checks failures=%d" % failures)
	a.free()
	quit(1 if failures else 0)
