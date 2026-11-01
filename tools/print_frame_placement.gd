extends SceneTree
## Raw numeric evidence is deliberately printed for the requested commit message.
func _initialize() -> void:call_deferred("run")
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate();root.add_child(a)
	a.autoplay=false;a.set_process(false)
	var rows:=0
	for school in ["kiem","cung"]:
		a.set_school(school)
		for direction in [-1,1]:
			a.set_facing(direction)
			for frame in 30:
				a.sample_frame(frame)
				var f: Dictionary=a.frames_data.frames[frame]
				for layer in ["head","body","legs","weapon"]:
					var key: String={"head":"dau","body":"than","legs":"chan","weapon":"vu_khi"}[layer]
					var src: Array=f.reference[key]
					var offsets: Array=a.frames_data.reference.image_offsets[school if layer=="weapon" else key][int(src[0])]
					var origin:=Vector2(src[1]+offsets[0],-src[2]+offsets[1])*3
					var registration: Array=f.registrations[school][layer]
					var own: Vector2=a.sprites[layer].position
					var expected:=origin+Vector2(registration[0],registration[1])
					var world: Vector2=a.sprites[layer].to_global(Vector2.ZERO)
					print("PLACEMENT %s dir%d frame%02d %s ref(image,dx,dy)=%s image_offset=%s source_origin_3x=%s crop_joint_registration=%s OWN_TOP_LEFT=%s OWN_WORLD=%s own_asset=%s" % [school,direction,frame,layer,str(src),str(offsets),str(origin),str(registration),str(own),str(world),a.sprites[layer].texture.resource_path.get_file()])
					rows+=1
		for skill in (["slash","tram_kiem"] if school=="kiem" else ["shoot","xa_tien"]):
			a.action=skill
			for direction in [-1,1]:
				a.set_facing(direction)
				for air in [false,true]:
					a.airborne=air
					for i in a.beats().size():
						a.sample_beat(i)
						print("BEAT %s air%s index%d source=%s OWN_FRAME=%d OWN_DURATION=%.6f DIR=%d" % [skill,air,i,str(a.beats()[i].reference),a.frame_index,a.beats()[i].duration,direction])
						for fx in a.reference_effects:
							var index:=int((fx.elapsed+.000000001)/.05)
							print("EFFECT %s air%s beat%d id%d source_base_3x=%s source_frame%d_offset=%s OWN_CENTER=%s OWN_WORLD=%s OWN_Z=%d" % [skill,air,i,fx.effect_id,str(fx.origin),index,str(fx.offsets[index]),str(fx.sprite.position),str(fx.sprite.global_position),fx.sprite.z_index])
	print("Printed frame-placement rows=%d (diagnostic only, not a test)" % rows)
	a.free();quit(0)
