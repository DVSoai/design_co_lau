extends Node2D
## Lv1 four painted layers. JSON owns frame selection, anchors and skill beats.
var parts: Dictionary
var frames_data: Dictionary
var effects_data: Dictionary
var skills_data: Dictionary
var sprites: Dictionary = {}
var effect_sprites: Array[Sprite2D] = []
var arrows: Array[Sprite2D] = []
var quiver: Sprite2D
var nocked_arrow: Sprite2D
var school := "kiem"
var facing := 1
var autoplay := true
var action := "idle"
var frame_index := 0
var beat_index := 0
var elapsed := 0.0
var effect_elapsed := 0.0
var airborne := false
var landmarks: Dictionary = {}
var hit_active := false
var release_count := 0
var reference_effects: Array[Dictionary] = []
var held_fingers: Sprite2D
var roll_wind: Sprite2D
var hand_masks: Dictionary={}
func _ready() -> void:
	parts=read_data("parts")
	frames_data=read_data("frames30")
	effects_data=read_data("effects").effects
	skills_data=read_data("skills").skills
	for id in ["legs","body","head","weapon"]:
		sprites[id]=make_sprite(id)
	quiver=make_sprite("quiver")
	quiver.z_index=-1
	nocked_arrow=make_sprite("nocked_arrow")
	nocked_arrow.z_index=8
	held_fingers=make_sprite("held_fingers")
	held_fingers.z_index=4
	roll_wind=make_sprite("roll_wind")
	roll_wind.centered=true
	roll_wind.z_index=preload("res://config/tuning.gd").COMBAT_EFFECT_Z
	sample_frame(0)
func read_data(id: String) -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/"+id+".json"))
func make_sprite(id: String) -> Sprite2D:
	var s:=Sprite2D.new()
	s.name=id
	s.centered=false
	s.scale=Vector2(.5,.5)
	s.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	add_child(s)
	return s
func anchor(id: String, key: String) -> Vector2:
	var p: Array=parts.assets[id].anchors[key]
	return Vector2(p[0],p[1])*.5
func put(s: Sprite2D,id: String, at: Vector2, key: String="") -> void:
	s.texture=load("res://pose_rig/art/lv1_30/"+parts.assets[id].file)
	s.rotation=0
	s.position=at-(anchor(id,key) if key!="" else Vector2.ZERO)
	s.visible=true
func clear_effects() -> void:
	for s in effect_sprites:
		s.visible=false
		s.queue_free()
	effect_sprites.clear()
func clear_arrows() -> void:
	for s in arrows:
		s.visible=false
		s.queue_free()
	arrows.clear()
func clear_reference_effects() -> void:
	for fx in reference_effects:fx.sprite.queue_free()
	reference_effects.clear()
func set_school(id: String) -> void:
	assert(id in ["kiem","cung"])
	school=id
	clear_arrows()
	play("idle")
func set_facing(dir: int) -> void:
	facing=1 if dir>=0 else -1
	scale=Vector2(facing,1)
func sample_frame(index: int) -> void:
	frame_index=index
	clear_effects()
	var f: Dictionary=frames_data.frames[index]
	var ids: Dictionary={}
	for layer in ["legs","body","head"]:ids[layer]=parts.levels["1"][layer][int(f.layers[layer].image)]
	if school=="cung" and f.layers.body.has("cung_image"):ids.body=parts.levels["1"].body[int(f.layers.body.cung_image)]
	for layer in ["legs","body","head"]:ids[layer]=f.layers[layer].get("asset",ids[layer])
	if school=="cung":ids.body=f.layers.body.get("cung_asset",ids.body)
	if f.layers.legs.get('stance',false):ids.legs=parts.levels['1'].combat_stance
	if f.layers.legs.get('lunge',false):ids.legs=parts.levels['1'].combat_lunge
	var legs: String=ids.legs
	var body: String=ids.body
	var head: String=ids.head
	var lo: Dictionary=f.layers.legs
	put(sprites.legs,legs,Vector2(lo.dx,lo.dy),"sole")
	if index in [9,10,11]:
		sprites.legs.position=Vector2(0,-45)-anchor(legs,"hip")
	var hip: Vector2=sprites.legs.position+anchor(legs,"hip")
	var bo: Dictionary=f.layers.body
	put(sprites.body,body,hip+Vector2(bo.dx,bo.dy),"hip")
	var neck: Vector2=sprites.body.position+anchor(body,"neck")
	var ho: Dictionary=f.layers.head
	put(sprites.head,head,neck+Vector2(ho.dx,ho.dy),"neck")
	# Source formula and offsets are untouched. Crop/anatomy registration is explicit
	# per painted pose, so copied numeric origins cannot pull apart our neck/hip joints.
	if f.has("registrations"):
		for layer in ["legs","body","head"]:
			var key: String={"legs":"chan","body":"than","head":"dau"}[layer]
			var raw: Array=f.reference[key]
			var image_offset: Array=frames_data.reference.image_offsets[key][int(raw[0])]
			var origin:=Vector2(raw[1]+image_offset[0],-raw[2]+image_offset[1])*float(frames_data.reference.logic_per_reference_px)
			var correction: Array=f.registrations[school][layer]
			sprites[layer].position=origin+Vector2(correction[0],correction[1])
		hip=sprites.legs.position+anchor(legs,"hip")
		neck=sprites.body.position+anchor(body,"neck")
	var grip: Vector2=sprites.body.position+anchor(body,"grip")
	var far_hand: Vector2=sprites.body.position+anchor(body,"far_hand")
	var near_hand: Vector2=sprites.body.position+anchor(body,"near_hand")
	var back: Vector2=sprites.body.position+anchor(body,"back")
	var held_hand: Vector2=grip if grip.x>=far_hand.x else far_hand
	if f.get("held_hand","")=="grip":held_hand=grip
	var weapon: String=parts.levels["1"].weapons[school]
	var wo: Dictionary=f.layers.weapon
	put(sprites.weapon,weapon,held_hand+Vector2(wo.dx,wo.dy),"grip")
	if f.has("registrations") and f.registrations[school].has("weapon"):
		var raw: Array=f.reference.vu_khi
		var offsets: Array=frames_data.reference.image_offsets[school][int(raw[0])]
		var registration: Array=f.registrations[school].weapon
		sprites.weapon.position=Vector2(raw[1]+offsets[0],-raw[2]+offsets[1])*3+Vector2(registration[0],registration[1])
	sprites.weapon.z_index=int(f.get("held_weapon_z",{}).get(school,3))
	sprites.weapon.visible=f.get("held_visible",not f.attack)
	held_fingers.visible=sprites.weapon.visible
	if held_fingers.visible:
		var key:=body+str(held_hand-sprites.body.position)
		if not hand_masks.has(key):
			var im: Image=sprites.body.texture.get_image().duplicate()
			var centre: Vector2=(held_hand-sprites.body.position)*2
			if index in range(2,8):
				# The new run canvases are larger: build only the small finger region
				# on first use instead of scanning80k pixels during each new run pose.
				var source:=im
				im=Image.create(source.get_width(),source.get_height(),false,Image.FORMAT_RGBA8)
				for y in range(maxi(0,int(floor(centre.y-9))),mini(im.get_height(),int(ceil(centre.y+9))+1)):
					for x in range(maxi(0,int(floor(centre.x-9))),mini(im.get_width(),int(ceil(centre.x+9))+1)):
						var c:=source.get_pixel(x,y)
						if Vector2(x,y).distance_to(centre)<=9 and c.r>=.6 and c.g>=.3 and c.r-c.g>=.08:im.set_pixel(x,y,c)
			else:
				for y in im.get_height():
					for x in im.get_width():
						var c:=im.get_pixel(x,y)
						if Vector2(x,y).distance_to(centre)>9 or c.r<.6 or c.g<.3 or c.r-c.g<.08:im.set_pixel(x,y,Color.TRANSPARENT)
			hand_masks[key]=ImageTexture.create_from_image(im)
		held_fingers.texture=hand_masks[key]
		held_fingers.position=sprites.body.position
	roll_wind.visible=index in range(8,12) and parts.has("roll_winds")
	if roll_wind.visible:
		roll_wind.texture=load("res://pose_rig/art/lv1_30/"+parts.assets[parts.roll_winds[index-8]].file)
		roll_wind.position=sprites.legs.position+sprites.legs.texture.get_size()*.25
	quiver.visible=school=="cung"
	if school=="cung":put(quiver,"quiver",back,"back")
	else:quiver.texture=null
	nocked_arrow.visible=false
	landmarks={"hip":hip,"neck":neck,"grip":grip,"far_hand":far_hand,"near_hand":near_hand,"held_hand":held_hand,"head_asset":head,"body_asset":body,"legs_asset":legs,"weapon_asset":weapon,"free_hand":sprites.body.position+anchor(body,"free_hand") if parts.assets[body].anchors.has("free_hand") else far_hand}
	hit_active=false
func beats() -> Array:
	return skills_data[action]["air" if airborne else "ground"]
func play(id: String) -> void:
	assert(id in frames_data.clips or (id in skills_data and skills_data[id].school==school))
	action=id
	clear_reference_effects()
	elapsed=0
	beat_index=0
	effect_elapsed=0
	if id in skills_data:sample_beat(0,true)
	else:sample_frame(int(frames_data.clips[id].frames[0]))
func sample_beat(index: int, emit_projectile: bool=false) -> void:
	beat_index=index
	effect_elapsed=0
	var beat: Dictionary=beats()[index]
	if not autoplay:clear_reference_effects()
	sample_frame(int(beat.frame))
	sprites.weapon.visible=false
	held_fingers.visible=false
	for spec in beat.effects:
		var s:=make_sprite("effect_"+spec.id)
		s.z_index=int(effects_data[spec.id].z)
		effect_sprites.append(s)
	update_effects()
	if not autoplay:
		# A frozen review beat must include the effect born in an earlier beat.
		for previous in range(index+1):
			var age:=0.0
			for j in range(previous,index):age+=float(beats()[j].duration)
			spawn_reference_effects(beats()[previous],age)
	else:
		var start:=0.0
		for j in range(index):start+=float(beats()[j].duration)
		spawn_reference_effects(beat,maxf(0,elapsed-start))
	update_reference_effects(0)
	if beat.nocked:
		put(nocked_arrow,beat.get("nocked_asset","arrow"),landmarks.string,"tail")
	if emit_projectile and beat.projectile!=null:
		var s:=make_sprite("projectile_"+beat.projectile.id)
		s.z_index=9
		var origin:=Vector2(beat.projectile.dx,beat.projectile.dy)
		var correction: Vector2=landmarks.string-origin if beat.projectile.get("register_to_string",false) else landmarks.string
		landmarks.projectile_source_origin=origin
		landmarks.projectile_registration=correction
		put(s,beat.projectile.id,origin+correction,"tail")
		arrows.append(s)
		release_count+=1
func update_effects() -> void:
	var beat: Dictionary=beats()[beat_index]
	for i in beat.effects.size():
		var spec: Dictionary=beat.effects[i]
		var def: Dictionary=effects_data[spec.id]
		var sequence: Array=def.frames
		var t:=effect_elapsed
		var key: Dictionary=sequence[-1]
		for item in sequence:
			if t<float(item.duration):
				key=item
				break
			t-=float(item.duration)
		var s: Sprite2D=effect_sprites[i]
		var offset:=Vector2(spec.dx+key.get("dx",0),spec.dy+key.get("dy",0))
		if def.placement=="grip":
			put(s,key.asset,landmarks.grip+offset,"grip")
			landmarks.weapon_grip=s.position+anchor(key.asset,"grip")
			landmarks.tip=s.position+anchor(key.asset,"tip")
		elif def.placement=="far_hand":
			put(s,key.asset,landmarks.far_hand+offset,"grip")
			landmarks.belly=s.position+anchor(key.asset,"belly")
			landmarks.string=s.position+anchor(key.asset,"string")
		else:
			s.centered=true
			put(s,key.asset,offset)
		if def.placement!="centre":
			s.centered=true
			s.position+=s.texture.get_size()*.25
func _process(delta: float) -> void:
	update_reference_effects(delta)
	for s in arrows.duplicate():
		s.position.x+=240*delta
		if s.position.x>500:
			arrows.erase(s)
			s.queue_free()
	if not autoplay:return
	elapsed+=delta
	effect_elapsed+=delta
	if action in skills_data:
		var total:=0.0
		var next:=0
		for beat in beats():
			total+=float(beat.duration)
			if elapsed+0.000000001>=total:next+=1
		while beat_index<mini(next,beats().size()-1):sample_beat(beat_index+1,true)
		if next>=beats().size():
			play("idle")
			return
		update_effects()
		var window=skills_data[action].hit_window
		hit_active=window!=null and elapsed+0.000000001>=window[0] and elapsed+0.000000001<window[1]
	else:
		var clip: Dictionary=frames_data.clips[action]
		var total:=0.0
		var next:=0
		for d in clip.durations:
			total+=float(d)
			if elapsed+0.000000001>=total:next+=1
		if next>=clip.frames.size():
			if clip.loop:
				elapsed=fmod(elapsed,total)
				next=0
			else:
				if action=="apex_flip":
					play("fall")
					return
				next=clip.frames.size()-1
		var id:=int(clip.frames[next])
		if id!=frame_index:sample_frame(id)
func all_visual_sprites() -> Array:
	var out: Array=sprites.values()+[quiver,nocked_arrow,held_fingers,roll_wind]+effect_sprites+arrows
	for fx in reference_effects:out.append(fx.sprite)
	return out
func spawn_reference_effects(beat: Dictionary,age: float) -> void:
	if not beat.has("reference"):return
	for spec in beat.reference.hieu_ung:
		var offsets: Array=frames_data.reference.effect_offsets[str(int(spec.id))].do_lech
		if int((age+.000000001)/.05)>=offsets.size():continue
		var flash:=make_sprite("numeric_effect_%d" % int(spec.id))
		flash.centered=true
		flash.z_index=preload("res://config/tuning.gd").COMBAT_EFFECT_Z
		var assets: Array=[]
		if parts.get("numeric_trails",{}).has(action):assets=parts.numeric_trails[action].get(str(int(spec.id)),[])
		reference_effects.append({"sprite":flash,"offsets":offsets,"elapsed":age,"origin":Vector2(spec.dx,spec.dy)*3,"assets":assets,"effect_id":int(spec.id)})
func update_reference_effects(delta: float) -> void:
	for fx in reference_effects.duplicate():
		fx.elapsed+=delta
		var index:=int((fx.elapsed+.000000001)/.05)
		if index>=fx.offsets.size():
			fx.sprite.queue_free()
			reference_effects.erase(fx)
		else:
			var file: String=parts.assets[fx.assets[index]].file if not fx.assets.is_empty() else "pose_flash.png"
			fx.sprite.texture=load("res://pose_rig/art/lv1_30/"+file)
			var offset: Array=fx.offsets[index]
			fx.sprite.position=fx.origin+Vector2(offset[0],offset[1])*3
