extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate();root.add_child(a);a.autoplay=false;a.set_process(false)
	for school in ["kiem","cung"]:
		a.set_school(school)
		for direction in [-1,1]:
			a.set_facing(direction);var textures: Dictionary={};var groups: Dictionary={}
			for frame in range(13,30):
				a.sample_frame(frame)
				var group: int=0 if frame<=20 else (1 if frame<=25 else 2)
				var path: String=a.sprites.legs.texture.resource_path;var rid: RID=a.sprites.legs.texture.get_rid()
				textures[path]=true
				if not groups.has(group):groups[group]=rid
				check(path.ends_with("attack_stance_%d.png" % group) and rid==groups[group],"%s dir%d frame%d exact shared stance group%d texture=%s" % [school,direction,frame,group,path.get_file()])
			check(textures.size()==3,"exactly THREE actual attack-leg textures across13–29")
			var running_bodies: Dictionary={};var running_legs: Dictionary={}
			for frame in range(2,8):
				a.sample_frame(frame)
				for layer in ["body","legs"]:
					var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(a.sprites[layer].texture.get_image().get_data());var key:=hash.finish().hex_encode()
					if layer=="body":running_bodies[key]=true
					else:running_legs[key]=true
			check(running_bodies.size()==6 and running_legs.size()==6,"run asset contract: six distinct body and six distinct leg RGBA textures")
	print("Attack stance texture contracts failures=%d; foot contact/visibility/seams are separate rendered-image tests" % failures);a.free();quit(1 if failures else 0)
