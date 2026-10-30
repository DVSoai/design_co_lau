extends Node2D
## Independently authored whole poses: no runtime rotation.
var anchors: Dictionary
var schools: Dictionary
var clips: Dictionary
var sprites: Dictionary = {}
var frame_index := 0
var action := "idle"
var school := "kiem"
var elapsed := 0.0
var autoplay := true
var facing := 1
var weapon_enabled := true
var landmarks: Dictionary = {}
var arrows: Array[Sprite2D] = []
var arrow_speed := 240.0 # logic px/s; preview only, not an A0 tuning change
var arrow_asset := "arrow_1"
var swing_data: Dictionary
var weapon_level := 1
var blade_sprite: Sprite2D
var trail_sprite: Sprite2D
var nocked_arrow: Sprite2D
func _ready() -> void:
	swing_data=JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/swing.json"))
	anchors = JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/anchors.json")).assets
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/frames.json"))
	schools = data.schools
	for attack_name in ["slash","thrust"]:schools.kiem[attack_name]=swing_data.clips[attack_name]
	clips = schools[school]
	arrow_speed = float(data.arrow_speed)
	arrow_asset = data.arrow_asset
	for id in ["legs", "body", "head", "weapon"]:
		var sprite := Sprite2D.new()
		sprite.name = id
		sprite.centered = false
		sprite.scale = Vector2(.5,.5)
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		add_child(sprite)
		sprites[id] = sprite
	for id in ["blade","trail","nocked"]:
		var sprite := Sprite2D.new()
		sprite.name=id
		sprite.centered=id=="trail"
		sprite.scale=Vector2(.5,.5)
		sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
		sprite.z_index=6 if id=="trail" else 5
		add_child(sprite)
		if id=="blade":blade_sprite=sprite
		elif id=="trail":trail_sprite=sprite
		else:nocked_arrow=sprite
	sample("idle",0)
func set_weapon_level(level: int) -> void:
	assert(str(level) in swing_data.levels and swing_data.levels[str(level)].status=="drawn_unapproved")
	weapon_level=level
	if school=="kiem":sample(action,frame_index)
func point_asset_path(id: String) -> String:
	return "res://pose_rig/art/swing/"+swing_data.arrow.file if id=="ready_arrow" else "res://pose_rig/art/"+anchors[id].file
func all_visual_sprites() -> Array:
	return sprites.values()+[blade_sprite,trail_sprite,nocked_arrow]+arrows
func _process(delta: float) -> void:
	advance_arrows(delta)
	if not autoplay:return
	elapsed+=delta
	var duration: float=clips[action].frames[frame_index].duration
	while elapsed+0.000000001>=duration:
		elapsed=maxf(0,elapsed-duration)
		var next:=frame_index+1
		if next>=clips[action].frames.size():
			if clips[action].loop:next=0
			else:
				if action in ["slash","thrust","shoot"]:sample("idle",0)
				elapsed=0
				return
		sample(action,next)
		duration=clips[action].frames[frame_index].duration
func point(id: String, key: String) -> Vector2:
	var p: Array = swing_data.arrow[key] if id=="ready_arrow" else anchors[id].anchors[key]
	return Vector2(p[0],p[1])*.5
func set_school(value: String) -> void:
	school=value
	clips=schools[school]
	clear_arrows()
	elapsed=0
	sample("idle",0)
func sample(name_: String, index: int) -> void:
	action=name_
	frame_index=index
	var f: Dictionary = clips[action].frames[index]
	assert(f.weapon.begins_with("kiem_") if school=="kiem" else f.weapon.begins_with("cung_"))
	for id in sprites:
		var sprite: Sprite2D = sprites[id]
		sprite.texture=load("res://pose_rig/art/"+anchors[f[id]].file)
		sprite.rotation=0
		sprite.scale=Vector2(.5,.5)
	sprites.legs.position=-point(f.legs,"sole")
	var hip: Vector2 = sprites.legs.position+point(f.legs,"hip")
	sprites.body.position=hip-point(f.body,"hip")
	var neck: Vector2 = sprites.body.position+point(f.body,"neck")
	sprites.head.position=neck-point(f.head,"neck")
	var key := "back"
	if f.attack: key="far_hand" if school=="cung" else "grip"
	var grip: Vector2 = sprites.body.position+point(f.body,key)
	sprites.weapon.position=grip-point(f.weapon,"grip")
	sprites.weapon.z_index=3 if f.attack else -1
	sprites.weapon.visible=weapon_enabled
	landmarks={"sole":Vector2.ZERO,"hip":hip,"neck":neck,"grip":grip,"weapon_grip":sprites.weapon.position+point(f.weapon,"grip")}
	if school=="kiem":landmarks.tip=sprites.weapon.position+point(f.weapon,"tip")
	else:
		landmarks.belly=sprites.weapon.position+point(f.weapon,"belly")
		landmarks.string=sprites.weapon.position+point(f.weapon,"string")
		if f.attack:
			landmarks.near_hand=sprites.body.position+point(f.body,"near_hand")
			landmarks.far_hand=sprites.body.position+point(f.body,"far_hand")
	blade_sprite.visible=false
	trail_sprite.visible=false
	nocked_arrow.visible=false
	if school=="kiem" and f.attack and f.has("swing_angle"):
		var blade: Dictionary=swing_data.levels[str(weapon_level)].blades[f.swing_angle]
		blade_sprite.texture=load("res://pose_rig/art/swing/"+blade.file)
		blade_sprite.position=grip-Vector2(blade.grip[0],blade.grip[1])*.5
		blade_sprite.rotation=0
		blade_sprite.visible=weapon_enabled
		sprites.weapon.visible=false
		landmarks.weapon_grip=blade_sprite.position+Vector2(blade.grip[0],blade.grip[1])*.5
		landmarks.tip=blade_sprite.position+Vector2(blade.tip[0],blade.tip[1])*.5
		if f.trail!=null:
			var trail: Dictionary=swing_data.trails[f.trail]
			trail_sprite.texture=load("res://pose_rig/art/swing/"+trail.file)
			trail_sprite.position=Vector2(f.trail_offset[0],f.trail_offset[1])
			trail_sprite.rotation=0
			trail_sprite.visible=weapon_enabled
			landmarks.trail_centre=trail_sprite.position
	if school=="cung" and f.get("nocked",false):
		nocked_arrow.texture=load(point_asset_path(arrow_asset))
		nocked_arrow.position=landmarks.string-point(arrow_asset,"tail")
		nocked_arrow.rotation=0
		nocked_arrow.visible=weapon_enabled
	scale=Vector2(facing,1)
	if f.get("spawn",false): spawn_arrow()
func spawn_arrow() -> void:
	var arrow := Sprite2D.new()
	arrow.texture=load(point_asset_path(arrow_asset))
	arrow.centered=false
	arrow.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	arrow.scale=Vector2(.5,.5)
	arrow.rotation=0
	arrow.z_index=5
	arrow.position=landmarks.string-point(arrow_asset,"tail")
	add_child(arrow)
	arrows.append(arrow)
func advance_arrows(delta: float) -> void:
	for arrow in arrows.duplicate():
		arrow.position.x+=arrow_speed*delta
		if arrow.position.x>500:
			arrows.erase(arrow)
			arrow.queue_free()
func clear_arrows() -> void:
	for arrow in arrows:
		arrow.visible=false
		arrow.queue_free()
	arrows.clear()
func set_facing(direction: int) -> void:
	facing=1 if direction>=0 else -1
	scale=Vector2(facing,1)
