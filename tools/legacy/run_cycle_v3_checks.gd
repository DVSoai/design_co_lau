extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func hash_image(im: Image) -> String:
	var h:=HashingContext.new();h.start(HashingContext.HASH_SHA256);h.update(im.get_data());return h.finish().hex_encode()
func point(a: Node2D,s: Sprite2D,id: String,key: String) -> Vector2:
	return s.to_global(a.anchor(id,key)*2)
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate();root.add_child(a)
	a.autoplay=false;a.set_process(false)
	var H: float=a.parts.presentation.standing_height_logic
	for school in ["kiem","cung"]:
		a.set_school(school)
		for direction in [-1,1]:
			a.set_facing(direction)
			var wide:=0;var hands: Array[Vector2]=[];var torso_hashes: Dictionary={};var leg_hashes: Dictionary={}
			for frame in range(2,8):
				a.sample_frame(frame)
				var leg: Sprite2D=a.sprites.legs;var body: Sprite2D=a.sprites.body;var weapon: Sprite2D=a.sprites.weapon
				var left:=point(a,leg,a.landmarks.legs_asset,"foot_left");var right:=point(a,leg,a.landmarks.legs_asset,"foot_right")
				var stride:=left.distance_to(right)/H
				if stride>=.3:wide+=1
				hands.append(a.to_global(a.landmarks.free_hand)-a.to_global(a.landmarks.hip))
				torso_hashes[hash_image(body.texture.get_image())]=true;leg_hashes[hash_image(leg.texture.get_image())]=true
				var axis: Vector2=a.landmarks.neck-a.landmarks.hip
				var lean:=rad_to_deg(atan2(absf(axis.x),absf(axis.y)))
				check(lean>=10 and lean<=15,"%s frame%d dir%d torso lean=%.6f deg; feet/H=%.6f" % [school,frame,direction,lean,stride])
				var li: Image=leg.texture.get_image();var wi: Image=weapon.texture.get_image()
				var total:=0.0;var geometric:=0.0;var occluded:=0.0
				for y in li.get_height():
					for x in li.get_width():
						var alpha:=li.get_pixel(x,y).a
						if alpha<.05:continue
						total+=alpha
						var at: Vector2=weapon.to_local(leg.to_global(Vector2(x+.5,y+.5)))
						if Rect2(Vector2.ZERO,wi.get_size()).has_point(at):
							var coverage:=minf(alpha,wi.get_pixelv(Vector2i(at)).a)
							geometric+=coverage
							if weapon.z_index>leg.z_index:
								if a.held_lower_legs.visible:coverage*=1-a.held_lower_legs.texture.get_image().get_pixel(x,y).a
								occluded+=coverage
				check(total>0 and occluded/total<=.15,"%s frame%d dir%d actual weapon-over-legs=%.6f%%; raw overlap=%.6f%%; weapon_z=%d legs_z=%d" % [school,frame,direction,100*occluded/total,100*geometric/total,weapon.z_index,leg.z_index])
				if school=="kiem":check(weapon.z_index>body.z_index,"held sword is drawn above the torso under the current draw-order rule")
				# Foot landmarks are on actual painted shoes and remain below the short coat.
				for foot in [left,right]:
					var at: Vector2=body.to_local(foot)
					var covered:=0.0
					if Rect2(Vector2.ZERO,body.texture.get_size()).has_point(at):covered=body.texture.get_image().get_pixelv(Vector2i(at)).a
					check(covered<.5,"shoe sole remains visible below the moving coat")
				var grip:=point(a,weapon,a.landmarks.weapon_asset,"grip")
				check(grip.distance_to(a.to_global(a.landmarks.held_hand))<=1,"actual grip stays inside painted holding fist")
			var travel:=0.0
			for i in hands.size():
				for j in range(i+1,hands.size()):travel=maxf(travel,hands[i].distance_to(hands[j])/H)
			check(wide>=4,"%s dir%d strides>=.30H: %d/6" % [school,direction,wide])
			check(travel>=.15,"%s dir%d free-hand travel relative to hip/H=%.6f >=.15" % [school,direction,travel])
			check(torso_hashes.size()==6 and leg_hashes.size()==6,"six distinct painted torsos and six distinct painted legs")
	print("Run cycle v3 checks failures=%d" % failures)
	a.free();quit(1 if failures else 0)
