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
func _ready() -> void:
	anchors = JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/anchors.json")).assets
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/frames.json"))
	schools = data.schools
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
	sample("idle",0)
func _process(delta: float) -> void:
	advance_arrows(delta)
	if not autoplay: return
	elapsed += delta
	var duration: float = clips[action].frames[frame_index].duration
	if elapsed >= duration:
		elapsed = fmod(elapsed,duration)
		var next := frame_index+1
		if next >= clips[action].frames.size(): next=0 if clips[action].loop else frame_index
		if next!=frame_index or clips[action].frames.size()==1: sample(action,next)
func point(id: String, key: String) -> Vector2:
	var p: Array = anchors[id].anchors[key]
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
	scale=Vector2(facing,1)
	if f.get("spawn",false): spawn_arrow()
func spawn_arrow() -> void:
	var arrow := Sprite2D.new()
	arrow.texture=load("res://pose_rig/art/"+anchors[arrow_asset].file)
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
	for arrow in arrows:arrow.queue_free()
	arrows.clear()
func set_facing(direction: int) -> void:
	facing=1 if direction>=0 else -1
	scale=Vector2(facing,1)
