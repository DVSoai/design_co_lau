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
	var grip: Vector2=sprites.body.position+anchor(body,"grip")
	var far_hand: Vector2=sprites.body.position+anchor(body,"far_hand")
	var near_hand: Vector2=sprites.body.position+anchor(body,"near_hand")
	var back: Vector2=sprites.body.position+anchor(body,"back")
	var weapon: String=parts.levels["1"].weapons[school]
	var wo: Dictionary=f.layers.weapon
	put(sprites.weapon,weapon,(grip if school=="kiem" else far_hand)+Vector2(wo.dx,wo.dy),"grip")
	sprites.weapon.z_index=3
	sprites.weapon.visible=not f.attack
	quiver.visible=school=="cung"
	if school=="cung":put(quiver,"quiver",back,"back")
	else:quiver.texture=null
	nocked_arrow.visible=false
	landmarks={"hip":hip,"neck":neck,"grip":grip,"far_hand":far_hand,"near_hand":near_hand}
	hit_active=false
func beats() -> Array:
	return skills_data[action]["air" if airborne else "ground"]
func play(id: String) -> void:
	assert(id in frames_data.clips or (id in skills_data and skills_data[id].school==school))
	action=id
	elapsed=0
	beat_index=0
	effect_elapsed=0
	if id in skills_data:sample_beat(0,true)
	else:sample_frame(int(frames_data.clips[id].frames[0]))
func sample_beat(index: int, emit_projectile: bool=false) -> void:
	beat_index=index
	effect_elapsed=0
	var beat: Dictionary=beats()[index]
	sample_frame(int(beat.frame))
	sprites.weapon.visible=false
	for spec in beat.effects:
		var s:=make_sprite("effect_"+spec.id)
		s.z_index=int(effects_data[spec.id].z)
		effect_sprites.append(s)
	update_effects()
	if beat.nocked:
		put(nocked_arrow,"arrow",landmarks.string,"tail")
	if emit_projectile and beat.projectile!=null:
		var s:=make_sprite("projectile_"+beat.projectile.id)
		s.z_index=9
		put(s,beat.projectile.id,landmarks.far_hand+Vector2(beat.projectile.dx,beat.projectile.dy),"tail")
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
	return sprites.values()+[quiver,nocked_arrow]+effect_sprites+arrows
