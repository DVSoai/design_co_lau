extends Node2D
## Whole painted poses only. Runtime never rotates or stretches a layer.
var anchors: Dictionary
var clips: Dictionary
var sprites: Dictionary = {}
var frame_index := 0
var action := "idle"
var elapsed := 0.0
var autoplay := true
var facing := 1
var weapon_enabled := true
var landmarks: Dictionary = {}
func _ready() -> void:
	anchors = JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/anchors.json")).assets
	clips = JSON.parse_string(FileAccess.get_file_as_string("res://pose_rig/data/frames.json")).clips
	for id in ["legs", "body", "head", "weapon"]:
		var sprite := Sprite2D.new()
		sprite.name = id
		sprite.centered = false
		sprite.scale = Vector2(0.5, 0.5)
		sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
		add_child(sprite)
		sprites[id] = sprite
	sample("idle", 0)
func _process(delta: float) -> void:
	if not autoplay: return
	elapsed += delta
	var duration: float = clips[action].frames[frame_index].duration
	if elapsed >= duration:
		elapsed = fmod(elapsed,duration)
		var next := frame_index + 1
		if next >= clips[action].frames.size(): next = 0 if clips[action].loop else frame_index
		sample(action,next)
func point(id: String, key: String) -> Vector2:
	var p: Array = anchors[id].anchors[key]
	return Vector2(p[0],p[1]) * 0.5
func sample(name_: String, index: int) -> void:
	action = name_
	frame_index = index
	var f: Dictionary = clips[action].frames[index]
	for id in sprites:
		var sprite: Sprite2D = sprites[id]
		sprite.texture = load("res://pose_rig/art/" + anchors[f[id]].file)
		sprite.rotation = 0
		sprite.scale = Vector2(0.5,0.5)
	sprites.legs.position = -point(f.legs,"sole")
	var hip: Vector2 = sprites.legs.position + point(f.legs,"hip")
	sprites.body.position = hip - point(f.body,"hip")
	var neck: Vector2 = sprites.body.position + point(f.body,"neck")
	sprites.head.position = neck - point(f.head,"neck")
	var grip: Vector2 = sprites.body.position + point(f.body,"grip" if f.attack else "back")
	sprites.weapon.position = grip - point(f.weapon,"grip")
	sprites.weapon.z_index = 3 if f.attack else -1
	sprites.weapon.visible = weapon_enabled
	landmarks = {"sole":Vector2.ZERO,"hip":hip,"neck":neck,"grip":grip,"tip":sprites.weapon.position+point(f.weapon,"tip")}
	scale = Vector2(facing,1)
func set_facing(direction: int) -> void:
	facing = 1 if direction >= 0 else -1
	scale = Vector2(facing,1)
