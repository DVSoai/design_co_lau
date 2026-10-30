extends SceneTree
var failures:=0
var pixels: Dictionary={}
func _initialize() -> void:call_deferred("run")
func check(ok: bool,text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok:failures+=1
func mask_pixels(a: Node2D,id: String) -> PackedVector2Array:
	if pixels.has(id):return pixels[id]
	var im: Image=load("res://pose_rig/art/lv1_30/"+a.parts.assets[id].file).get_image()
	var out:=PackedVector2Array()
	for y in im.get_height():
		for x in im.get_width():
			if im.get_pixel(x,y).a>.125:out.append(Vector2(x,y))
	pixels[id]=out
	return out
func hash_image(im: Image) -> String:
	var h:=HashingContext.new()
	h.start(HashingContext.HASH_SHA256)
	h.update(im.get_data())
	return h.finish().hex_encode()
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate()
	root.add_child(a)
	a.autoplay=false
	a.set_process(false)
	a.set_school("kiem")
	a.sample_frame(0)
	var top:=INF
	var bottom:=-INF
	for id in ["head","body","legs"]:
		var s: Sprite2D=a.sprites[id]
		var r:=Rect2(s.texture.get_image().get_used_rect())
		top=minf(top,s.to_global(r.position).y)
		bottom=maxf(bottom,s.to_global(r.end).y)
	var height:=bottom-top
	var bare: Image=load("res://pose_rig/art/lv1_30/head_without_hat_0.png").get_image()
	var ratio:=bare.get_used_rect().size.y*.5/height
	check(absf(ratio-.40)<=.03,"frame00 actual bare-head/hair ratio=%.6f H=%.6f logic, target.40 +/- .03" % [ratio,height])
	check(hash_image(a.sprites.head.texture.get_image())==hash_image(bare),"actual displayed head00 RGBA equals bare head: no hat included")
	for dir in [-1,1]:
		a.set_facing(dir)
		for skill in ["slash","tram_kiem"]:
			a.action=skill
			a.airborne=false
			check(a.beats().size()==5,"%s five beats guard/pull/sweep/hold/recover" % skill)
			var body_hashes: Dictionary={}
			for i in a.beats().size():
				a.sample_beat(i,false)
				check(not a.sprites.weapon.visible,"%s dir%d beat%d held weapon hidden" % [skill,dir,i])
				body_hashes[hash_image(a.sprites.body.texture.get_image())]=true
				if i not in [2,3]:continue
				var min_x:=INF
				var max_x:=-INF
				var primary_points:=PackedVector2Array()
				for index in a.effect_sprites.size():
					var s: Sprite2D=a.effect_sprites[index]
					var beat: Dictionary=a.beats()[i]
					var asset: String=a.effects_data[beat.effects[index].id].frames[0].asset
					var paint: String=a.parts.assets[asset].get("trail_mask",asset)
					for p in mask_pixels(a,paint):
						var world:=s.to_global(p-s.texture.get_size()/2)
						min_x=minf(min_x,world.x)
						max_x=maxf(max_x,world.x)
						if index==0:primary_points.append(world)
				var span:=max_x-min_x+.5
				check(span/height<=1.3,"%s dir%d beat%d actual combined VFX length/H=%.6f <=1.3" % [skill,dir,i,span/height])
				# Central brown shirt only, excluding distant hands and wrist wraps.
				var body_id: String=a.parts.levels["1"].body[int(a.frames_data.frames[a.frame_index].layers.body.image)]
				var body: Sprite2D=a.sprites.body
				var image:=body.texture.get_image()
				var mid: float=(a.anchor(body_id,"hip").x+a.anchor(body_id,"neck").x)
				var shirt: Dictionary={}
				for y in image.get_height():
					for x in image.get_width():
						var c:=image.get_pixel(x,y)
						var r:=c.r*255
						var g:=c.g*255
						var b:=c.b*255
						if c.a>.5 and r>55 and r<225 and r-g>10 and r-g<70 and g-b<65 and absf(x-mid)<35 and y>=a.anchor(body_id,"neck").y*2 and y<a.anchor(body_id,"hip").y*2+45:
							var world:=body.to_global(Vector2(x,y))
							shirt[Vector2i(round(world.x*2),round(world.y*2))]=world
				var found_gap:=INF
				for point in primary_points:
					var key:=Vector2i(round(point.x*2),round(point.y*2))
					for dy in range(-8,9):
						for dx in range(-8,9):
							var k:=key+Vector2i(dx,dy)
							if shirt.has(k):found_gap=minf(found_gap,point.distance_to(shirt[k]))
					if found_gap<=4:break
				check(found_gap<=4,"%s dir%d beat%d observed actual curve/shirt contact upper-bound=%.6f px <=4 (not a hand contact)" % [skill,dir,i,found_gap])
			check(body_hashes.size()==4,"%s dir%d exactly4 distinct displayed torso RGBA hashes" % [skill,dir])
	print("Compact anatomy/sweep checks failures=%d" % failures)
	a.free()
	quit(1 if failures else 0)
