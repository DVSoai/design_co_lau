extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func alpha_at(im: Image,at: Vector2) -> float:
	if not Rect2(Vector2.ZERO,im.get_size()).has_point(at):return 0
	return im.get_pixelv(Vector2i(at)).a
func largest_component(mask: Dictionary) -> Dictionary:
	var todo:=mask.duplicate();var largest: Dictionary={}
	while not todo.is_empty():
		var seed: Vector2i=todo.keys()[0];var queue: Array[Vector2i]=[seed];var component: Dictionary={seed:true};todo.erase(seed)
		while not queue.is_empty():
			var at: Vector2i=queue.pop_back()
			for delta in [Vector2i(-1,0),Vector2i(1,0),Vector2i(0,-1),Vector2i(0,1)]:
				var next: Vector2i=at+delta
				if todo.has(next):todo.erase(next);component[next]=true;queue.append(next)
		if component.size()>largest.size():largest=component
	return largest
func run() -> void:
	var regions: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/foot_regions_v4.json")).polygons
	var a=load("res://pose_rig/rig_frames.tscn").instantiate();root.add_child(a);a.autoplay=false;a.set_process(false)
	var H: float=a.parts.presentation.standing_height_logic
	for school in ["kiem","cung"]:
		a.set_school(school)
		for direction in [-1,1]:
			a.set_facing(direction)
			for frame in range(2,8):
				a.sample_frame(frame)
				var leg: Sprite2D=a.sprites.legs;var im: Image=leg.texture.get_image()
				var layers: Array[Dictionary]=[]
				for sprite: Sprite2D in a.all_visual_sprites():
					if sprite==a.held_lower_legs:continue # Same painted leg restored in front, not an occluder.
					if sprite!=leg and sprite.visible and sprite.texture!=null and (sprite.z_index>leg.z_index or (sprite.z_index==leg.z_index and sprite.get_index()>leg.get_index())):
						layers.append({"sprite":sprite,"image":sprite.texture.get_image()})
				var centres: Array[Vector2]=[];var components: Array[Dictionary]=[]
				for foot in 2:
					var polygon:=PackedVector2Array()
					for pair: Array in regions[a.landmarks.legs_asset][foot]:polygon.append(Vector2(pair[0],pair[1]))
					var area:=0.0;var covered:=0.0;var visible: Dictionary={};var centre:=Vector2.ZERO
					for y in im.get_height():
						for x in im.get_width():
							var at:=Vector2(x+.5,y+.5);var alpha:=im.get_pixel(x,y).a
							if alpha<.05 or not Geometry2D.is_point_in_polygon(at,polygon):continue
							var survives:=1.0;var world:=leg.to_global(at)
							for layer: Dictionary in layers:
								var coverage:=alpha_at(layer.image,layer.sprite.to_local(world))
								if layer.sprite==a.sprites.weapon and a.held_lower_legs.visible:coverage*=1-alpha_at(a.held_lower_legs.texture.get_image(),a.held_lower_legs.to_local(world))
								survives*=1-coverage
							area+=alpha;covered+=alpha*(1-survives)
							if alpha>=.5 and survives>=.5:visible[Vector2i(x,y)]=true;centre+=world
					var biggest:=largest_component(visible);components.append(biggest)
					centres.append(centre/maxi(1,visible.size()))
					check(area>=20 and covered/area<=.30,"%s frame%d dir%d foot%d whole-shoe source_area=%.3f occluded=%.6f%% <=30" % [school,frame,direction,foot,area,covered/area*100])
					check(biggest.size()>=10 and float(biggest.size())/maxi(1,visible.size())>=.7,"whole visible foot forms a substantial connected region: %d/%d pixels" % [biggest.size(),visible.size()])
				var separate:=true
				for key: Vector2i in components[0]:
					for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
						if components[1].has(key+delta):separate=false
				check(separate and centres[0].distance_to(centres[1])>=.06*H,"%s frame%d dir%d TWO separately visible feet, centroid gap/H=%.6f" % [school,frame,direction,centres[0].distance_to(centres[1])/H])
			if school!="cung":continue
			for frame in [0,1,2,3,4,5,6,7,12,21]:
				a.sample_frame(frame)
				var bow: Sprite2D=a.sprites.weapon;var id: String=a.landmarks.weapon_asset
				var top:=bow.to_global(a.anchor(id,"top")*2);var bottom:=bow.to_global(a.anchor(id,"bottom")*2)
				var hand: Vector2=a.to_global(a.landmarks.held_hand);var grip:=bow.to_global(a.anchor(id,"grip")*2)
				var midpoint_gap:=hand.distance_to((top+bottom)*.5)/H
				var upper:=hand.distance_to(top);var lower:=hand.distance_to(bottom)
				var imbalance:=absf(upper-lower)/minf(upper,lower)
				check(midpoint_gap<=.05 and imbalance<=.15,"bow frame%d dir%d hand-midpoint/H=%.9f <=.05; tip distance imbalance=%.6f%% <=15 (shorter limb denominator)" % [frame,direction,midpoint_gap,100*imbalance])
				var rgba: Color=bow.texture.get_image().get_pixelv(Vector2i(a.anchor(id,"grip")*2))
				check(grip.distance_to(hand)<=1 and rgba.a>.8 and rgba.r>.3,"grip is on opaque middle wrapping, inside actual painted fist")
	print("Carry/whole-foot v4 failures=%d" % failures);a.free();quit(1 if failures else 0)
