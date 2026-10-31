extends SceneTree
const T=preload("res://config/tuning.gd")
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func point(a: Node2D,s: Sprite2D,id: String,key: String) -> Vector2:
	return s.to_global(a.anchor(id,key)*2-(s.texture.get_size()/2 if s.centered else Vector2.ZERO))
func hash_image(im: Image) -> String:
	var h:=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(im.get_data());return h.finish().hex_encode()
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate()
	root.add_child(a)
	a.autoplay=false;a.set_process(false)
	var H: float=a.parts.presentation.standing_height_logic
	for school in ["kiem","cung"]:
		a.set_school(school)
		for direction in [-1,1]:
			a.set_facing(direction);a.sample_frame(0)
			var standing: float=a.landmarks.hip.y-a.sprites.head.to_global(Vector2(0,a.sprites.head.texture.get_image().get_used_rect().position.y)).y
			var standing_hip: Vector2=a.landmarks.hip
			var hashes: Dictionary={};var wide:=0
			for frame in range(2,8):
				a.sample_frame(frame)
				hashes[hash_image(a.sprites.legs.texture.get_image())]=true
				var id: String=a.landmarks.legs_asset
				var left:=point(a,a.sprites.legs,id,"foot_left")
				var right:=point(a,a.sprites.legs,id,"foot_right")
				var span:=left.distance_to(right)/H
				if span>=.25:wide+=1
				var height: float=a.landmarks.hip.y-a.sprites.head.to_global(Vector2(0,a.sprites.head.texture.get_image().get_used_rect().position.y)).y
				check(absf(height-standing)<=.05*H,"%s dir%d run%d head-to-hip delta/H=%.6f <=.05; feet/H=%.6f" % [school,direction,frame,absf(height-standing)/H,span])
				var src: Array=a.frames_data.frames[frame].reference.than
				var base: Array=a.frames_data.frames[0].reference.than
				var bob:=Vector2(src[1]-base[1],base[2]-src[2])*3
				check(a.landmarks.hip.distance_to(standing_hip+bob)<.001,"run hip bob follows exact source torso dx/dy delta %s" % str(bob))
			check(hashes.size()==6,"six run RGBA hashes are pairwise distinct")
			check(wide>=4,"at least four running strides separate feet by >=.25H; got%d" % wide)
			for frame in [0,1,2,3,4,5,6,7,12,21]:
				a.sample_frame(frame)
				var id: String=a.parts.levels["1"].weapons[school]
				if school=="kiem" and frame in range(2,8):id=a.parts.levels["1"].run_weapon
				var grip:=point(a,a.sprites.weapon,id,"grip")
				var hand: Vector2=a.to_global(a.landmarks.held_hand)
				var pixel: Vector2=a.sprites.body.to_local(hand)
				var im: Image=a.sprites.body.texture.get_image()
				var skin:=im.get_pixelv(Vector2i(pixel.round()))
				check(grip.distance_to(hand)<=1 and skin.a>.8 and skin.r>.6 and skin.g>.3,"%s frame%d dir%d actual grip in painted fist, gap=%.6f" % [school,frame,direction,grip.distance_to(hand)])
				if school=="kiem":
					var mask: Image=a.held_fingers.texture.get_image()
					check(mask.get_pixelv(Vector2i(pixel.round())).a>.8 and a.held_fingers.z_index>a.sprites.weapon.z_index,"painted fingers cover the handle in foreground")
				else:
					var bow: Sprite2D=a.sprites.weapon
					var top:=point(a,bow,id,"top");var bottom:=point(a,bow,id,"bottom")
					var angle:=rad_to_deg(atan2(absf(top.x-bottom.x),absf(top.y-bottom.y)))
					var centre:=bow.to_global(Rect2(bow.texture.get_image().get_used_rect()).get_center())
					var torso: Vector2=a.sprites.body.to_global(Rect2(a.sprites.body.texture.get_image().get_used_rect()).get_center())
					check(direction*(centre.x-torso.x)>0 and angle>=20 and angle<=60,"bow centre ahead of torso; actual axis=%.6f degrees" % angle)
					var crossings:=0
					var hip: Vector2=a.anchor(a.landmarks.body_asset,"hip")*2
					var neck: Vector2=a.anchor(a.landmarks.body_asset,"neck")*2
					for step in 41:
						var at: Vector2=a.sprites.body.to_local(top.lerp(bottom,float(step)/40))
						if absf(at.x-hip.x)<H*.25 and at.y>neck.y and at.y<hip.y and Rect2(Vector2.ZERO,im.get_size()).has_point(at):
							if im.get_pixelv(Vector2i(at)).a>.8:crossings+=1
					check(crossings==0,"held bow/string axis stays outside central torso pixels")
			for frame in range(8,12):
				a.sample_frame(frame)
				check(a.roll_wind.visible and a.roll_wind.centered and a.roll_wind.rotation==0,"tucked roll%d uses separate centered wind; runtime rotation0" % frame)
				check(a.sprites.head.texture.get_size()==Vector2(224,224),"new compact quarter-turn pose, not the legacy straight-body spin")
	# Opaque trail area is measured from the actual independent rendered textures, never the sword.
	var white_area:=0.0
	for skill in ["slash","tram_kiem"]:
		a.set_school("kiem");a.action=skill;a.airborne=false;a.sample_beat(2)
		var seen: Dictionary={}
		for fx in a.reference_effects:
			seen[fx.effect_id]=true
			check(fx.sprite.centered and fx.sprite.z_index>a.sprites.body.z_index,"source%d effect centered above character" % fx.effect_id)
			if fx.effect_id!=16:continue
			var im: Image=fx.sprite.texture.get_image();var opaque:=0;var ink:=0;var dark:=0
			for y in im.get_height():
				for x in im.get_width():
					var c:=im.get_pixel(x,y)
					if c.a>.05:ink+=1
					if c.a>=.8:opaque+=1
					if c.a>.8 and maxf(c.r,maxf(c.g,c.b))<.45:dark+=1
			var area: float=opaque*.25/(H*H)
			check(area>=.25 and float(opaque)/ink>=.8,"%s sweep opaque(alpha>=.8) area/H2=%.6f, opaque/ink=%.6f" % [skill,area,float(opaque)/ink])
			check(dark>20,"visible thin dark contour pixels=%d" % dark)
			if skill=="slash":white_area=area
			else:check(area>white_area,"Trảm Kiếm blue trail is thicker than white normal trail")
		check(seen.has(16) and seen.has(39),"lia reconstructs continuing source16 plus short forward source39")
	a.autoplay=true;a.set_school("kiem");a.play("slash");a._process(.10)
	check(a.reference_effects.size()==2,"timed lia retains both overlapping effects")
	a._process(.10)
	var faded:=false
	for fx in a.reference_effects:
		var im: Image=fx.sprite.texture.get_image()
		var peak:=0.0
		for y in im.get_height():
			for x in im.get_width():peak=maxf(peak,im.get_pixel(x,y).a)
		if fx.effect_id==16 and peak<.6:faded=true
	check(faded,"hold phase fades broad white trail")
	a.free()
	var scene=load("res://pose_rig/play_test.tscn").instantiate();root.add_child(scene)
	await process_frame
	for dimensions in [Vector2i(960,540),Vector2i(1200,540)]:
		root.size=dimensions;scene.touch_controls.layout()
		for key in ["skill_1","skill_2"]:
			var button: Control=scene.touch_buttons[key];var font:=ThemeDB.fallback_font
			for row: String in button.caption.split("\n"):
				check(font.get_string_size(row,HORIZONTAL_ALIGNMENT_LEFT,-1,T.TOUCH_FONT_SIZE).x+8<=button.size.x,"%s label '%s' fits width at %s" % [key,row,str(dimensions)])
			check(font.get_height(T.TOUCH_FONT_SIZE)*2+8<=button.size.y,"two skill text lines fit height with padding")
	scene.queue_free();await process_frame
	print("Motion/art/skill-label checks failures=%d" % failures)
	quit(1 if failures else 0)
