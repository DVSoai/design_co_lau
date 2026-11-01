extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func alpha_at(im: Image,at: Vector2) -> float:
	if not Rect2(Vector2.ZERO,im.get_size()).has_point(at):return 0
	return im.get_pixelv(Vector2i(at)).a
func core_mask(im: Image,school: String,blade_root: Vector2,tip: Vector2) -> Image:
	var mask:=Image.create(im.get_width(),im.get_height(),false,Image.FORMAT_RGBA8)
	var axis: Vector2=(tip-blade_root).normalized();var warm: Dictionary={}
	if school=="cung":
		for y in im.get_height():
			for x in im.get_width():
				var c:=im.get_pixel(x,y)
				if c.a>.05 and c.r-c.g>12.0/255 and c.g-c.b>5.0/255 and c.r>55.0/255:warm[Vector2i(x,y)]=true
	for y in im.get_height():
		for x in im.get_width():
			var c:=im.get_pixel(x,y);var selected:=false
			if school=="kiem":selected=(Vector2(x+.5,y+.5)-blade_root).dot(axis)>=0
			elif minf(c.r,minf(c.g,c.b))<=.8:
				for dy in range(-2,3):
					for dx in range(-2,3):
						if warm.has(Vector2i(x+dx,y+dy)):selected=true
			if selected:mask.set_pixel(x,y,Color(1,1,1,c.a))
	return mask
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate();root.add_child(a);a.autoplay=false;a.set_process(false)
	var cases:=0
	for school in ["kiem","cung"]:
		a.set_school(school);a.sample_frame(0)
		var id: String=a.parts.levels["1"].weapons[school];var im: Image=a.sprites.weapon.texture.get_image()
		var blade_root: Vector2=a.anchor(id,"blade_root")*2 if school=="kiem" else Vector2.ZERO
		var tip: Vector2=a.anchor(id,"tip")*2 if school=="kiem" else Vector2.RIGHT
		var mask:=core_mask(im,school,blade_root,tip);var axis: Vector2=(tip-blade_root).normalized()
		for direction in [-1,1]:
			a.set_facing(direction)
			for frame in [0,1,2,3,4,5,6,7,12,21]:
				a.sample_frame(frame);cases+=1
				var weapon: Sprite2D=a.sprites.weapon;var occluders: Array[Dictionary]=[]
				for s: Sprite2D in a.all_visual_sprites():
					if s!=weapon and s.visible and s.texture!=null and (s.z_index>weapon.z_index or (s.z_index==weapon.z_index and s.get_index()>weapon.get_index())):occluders.append({"sprite":s,"image":s.texture.get_image()})
				check(weapon.visible and weapon.z_index>a.sprites.body.z_index and weapon.z_index>a.sprites.legs.z_index,"%s frame%d dir%d held weapon above torso/legs; actual z=%d" % [school,frame,direction,weapon.z_index])
				check(a.held_fingers.visible and a.held_fingers.z_index>weapon.z_index,"painted fingers remain above the real handle")
				var total:=0.0;var visible:=0.0;var core:=0.0;var core_visible:=0.0;var across_body:=0.0
				var length_bins: Dictionary={};var visible_bins: Dictionary={}
				for y in im.get_height():
					for x in im.get_width():
						var alpha:=im.get_pixel(x,y).a
						if alpha<.05:continue
						var at:=Vector2(x+.5,y+.5);var world:=weapon.to_global(at);var survives:=1.0
						for layer: Dictionary in occluders:survives*=1-alpha_at(layer.image,layer.sprite.to_local(world))
						var ca:=mask.get_pixel(x,y).a;total+=alpha;visible+=alpha*survives;core+=ca;core_visible+=ca*survives
						if school=="kiem" and frame in [0,1] and ca>.05:
							var body: Sprite2D=a.sprites.body;var head: Sprite2D=a.sprites.head
							across_body+=ca*maxf(alpha_at(body.texture.get_image(),body.to_local(world)),alpha_at(head.texture.get_image(),head.to_local(world)))
							if ca>=.5:
								var bin:=int(floor((at-blade_root).dot(axis)));length_bins[bin]=true
								if survives>=.5:visible_bins[bin]=true
				check(total>0 and core>0 and visible/total>=.70 and core_visible/core>=.70,"%s frame%d dir%d actual alpha-area visible: whole=%.6f%% blade/wood+outline=%.6f%% >=70" % [school,frame,direction,100*visible/total,100*core_visible/core])
				var grip:=weapon.to_global(a.anchor(id,"grip")*2);var hand: Vector2=a.to_global(a.landmarks.held_hand)
				check(grip.distance_to(hand)<=1,"foreground grip remains wrapped by actual palm <=1px")
				if school=="kiem" and frame in [0,1]:
					var length_visible:=float(visible_bins.size())/maxi(1,length_bins.size())
					var vector:=weapon.to_global(tip)-grip
					check(length_visible>=.70 and across_body/core<=.30,"standing blade visible length=%.6f%% >=70; geometric head/torso overlap=%.6f%% <=30" % [100*length_visible,100*across_body/core])
					check(direction*vector.x<0 and vector.y>0,"standing blade still points down and behind")
	print("Foreground weapon checks cases=%d failures=%d" % [cases,failures]);a.free();quit(1 if failures else 0)
