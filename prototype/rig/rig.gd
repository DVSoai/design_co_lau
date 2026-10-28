extends Node2D
## Visual-only rig. All dimensions, pivots, angles, frames and timings are data.
var definition: Dictionary
var clips: Dictionary
var joints: Dictionary = {}
var shapes: Dictionary = {}
var paths: Dictionary = {}
var player: AnimationPlayer
var pivot_root: Node2D
var weapon := "dao"
var current_clip := ""
var debug_joints := false
var bow_string: Line2D
var sprites: Dictionary = {}
var art_enabled := true
var joint_fill: Dictionary = {}

func _ready() -> void:
	definition = JSON.parse_string(FileAccess.get_file_as_string("res://rig/data/parts.json"))
	clips = JSON.parse_string(FileAccess.get_file_as_string("res://rig/data/animations.json"))["clips"]
	pivot_root = Node2D.new()
	pivot_root.name = "PoseRoot"
	# Rotation centre at torso centre, not at the feet.
	pivot_root.position = Vector2(definition.rotation_center[0], definition.rotation_center[1])
	add_child(pivot_root)
	var fills: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://rig/art_parts/joint_fill.json"))
	for part in definition.parts:
		var joint := Node2D.new()
		joint.name = part.id
		var parent_node: Node2D = pivot_root if part.parent == "" else joints[part.parent]
		parent_node.add_child(joint)
		joint.position = Vector2(part.attach[0], part.attach[1])
		if part.parent == "":
			joint.position -= pivot_root.position
		joints[part.id] = joint
		paths[part.id] = str(get_path_to(joint))
		var shape := Polygon2D.new()
		var size := Vector2(part.size[0], part.size[1])
		var pivot := Vector2(part.pivot[0], part.pivot[1])
		shape.polygon = PackedVector2Array([-pivot, Vector2(size.x, 0)-pivot, size-pivot, Vector2(0, size.y)-pivot])
		shape.color = Color(part.color)
		shape.z_as_relative = false
		shape.z_index = int(part.z)
		joint.add_child(shape)
		shapes[part.id] = shape
		if fills.has(part.id):
			var cap := Polygon2D.new()
			var points := PackedVector2Array()
			for i in 32:
				points.append(Vector2.from_angle(TAU * i / 32) * float(fills[part.id].radius))
			cap.polygon = points
			cap.color = Color(fills[part.id].color)
			shape.add_child(cap)
			joint_fill[part.id] = cap
		var art := Sprite2D.new()
		art.texture = load("res://rig/art_parts/%s.png" % part.id)
		art.centered = false
		art.position = -pivot
		art.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
		shape.add_child(art)
		sprites[part.id] = art
	bow_string = Line2D.new()
	bow_string.z_as_relative = false
	bow_string.z_index = int(definition.bow_string.z)
	bow_string.width = float(definition.bow_string.width)
	bow_string.default_color = Color(definition.bow_string.color)
	add_child(bow_string)
	player = AnimationPlayer.new()
	player.name = "AnimationPlayer"
	add_child(player)
	var library := AnimationLibrary.new()
	for key in clips:
		library.add_animation(key, _make_animation(clips[key]))
	player.add_animation_library("", library)
	set_art_enabled(true)
	set_weapon("dao")
	play_clip("idle")

func _make_animation(clip: Dictionary) -> Animation:
	var anim := Animation.new()
	var duration := 0.0
	for frame in clip.frames:
		duration += float(frame.duration)
	anim.length = duration
	anim.loop_mode = Animation.LOOP_LINEAR if clip.loop else Animation.LOOP_NONE
	for part in definition.parts:
		var layer_track := anim.add_track(Animation.TYPE_VALUE)
		anim.track_set_path(layer_track, NodePath(str(get_path_to(shapes[part.id])) + ":z_index"))
		anim.track_insert_key(layer_track, 0, int(clip.get("layer_overrides", {}).get(part.id, part.z)))
	for id in joints:
		var track := anim.add_track(Animation.TYPE_VALUE)
		anim.track_set_path(track, NodePath(paths[id] + ":rotation"))
		anim.value_track_set_update_mode(track, Animation.UPDATE_DISCRETE)
		var time := 0.0
		for frame in clip.frames:
			anim.track_insert_key(track, time, deg_to_rad(float(frame.angles[id])))
			time += float(frame.duration)
	var body_track := anim.add_track(Animation.TYPE_VALUE)
	anim.track_set_path(body_track, NodePath(paths.body + ":position"))
	anim.value_track_set_update_mode(body_track, Animation.UPDATE_DISCRETE)
	var root_track := anim.add_track(Animation.TYPE_VALUE)
	anim.track_set_path(root_track, NodePath("PoseRoot:position"))
	anim.value_track_set_update_mode(root_track, Animation.UPDATE_DISCRETE)
	var flip_track := anim.add_track(Animation.TYPE_VALUE)
	anim.track_set_path(flip_track, NodePath("PoseRoot:rotation"))
	# Root rotation interpolates through an unwrapped turn; limbs use discrete poses.
	var time := 0.0
	for frame in clip.frames:
		anim.track_insert_key(root_track, time, Vector2(frame.root_position[0], frame.root_position[1]))
		anim.track_insert_key(body_track, time, Vector2(frame.body_position[0], frame.body_position[1]) - pivot_root.position)
		anim.track_insert_key(flip_track, time, deg_to_rad(float(frame.root_angle)))
		time += float(frame.duration)
	anim.track_insert_key(flip_track, duration, deg_to_rad(float(clip.end_root_angle)))
	return anim

func set_art_enabled(value: bool) -> void:
	art_enabled = value
	for id in shapes:
		shapes[id].self_modulate.a = 0.0 if value else 1.0
		sprites[id].visible = value
		if joint_fill.has(id):
			joint_fill[id].visible = value

func set_weapon(value: String) -> void:
	weapon = value
	if not shapes.is_empty():
		shapes.dao.visible = value == "dao"
		shapes.bow.visible = value == "bow"
		_update_string()

func play_clip(value: String, restart := false) -> void:
	if current_clip != value or restart:
		current_clip = value
		player.play(value)
		player.advance(0)

func sample(value: String, time: float) -> void:
	play_clip(value, true)
	player.pause()
	player.seek(time, true)
	_update_string()
	queue_redraw()

func geometry() -> Array:
	# Used by the contact-sheet exporter: actual evaluated scene polygons/transforms.
	_update_string()
	var result: Array = []
	for id in shapes:
		var shape: Polygon2D = shapes[id]
		if not shape.visible:
			continue
		if art_enabled:
			if joint_fill.has(id):
				var cap: Polygon2D = joint_fill[id]
				var points: Array = []
				for vertex in cap.polygon:
					var point := cap.to_global(vertex)-global_position
					points.append([point.x,point.y])
				result.append({"id": id+"_joint_fill", "owner": id, "kind": "fill", "z": shape.z_index, "color": cap.color.to_html(), "points": points})
			var sprite: Sprite2D = sprites[id]
			var transform := sprite.global_transform
			var origin := transform.origin - global_position
			result.append({"id": id, "kind": "sprite", "z": shape.z_index, "source": sprite.texture.resource_path, "transform": [transform.x.x, transform.x.y, transform.y.x, transform.y.y, origin.x, origin.y]})
			continue
		var points: Array = []
		for vertex in shape.polygon:
			var point := shape.to_global(vertex) - global_position
			points.append([point.x, point.y])
		result.append({"id": id, "z": shape.z_index, "color": shape.color.to_html(), "points": points})
	if bow_string.visible:
		var points: Array = []
		for vertex in bow_string.points:
			var point := bow_string.to_global(vertex) - global_position
			points.append([point.x, point.y])
		result.append({"id": "bow_string", "kind": "line", "width": bow_string.width, "z": bow_string.z_index, "color": bow_string.default_color.to_html(), "points": points})
	return result

func _process(_delta: float) -> void:
	_update_string()

func _update_string() -> void:
	if bow_string == null:
		return
	bow_string.visible = weapon == "bow"
	if not bow_string.visible:
		return
	var data: Dictionary = definition.bow_string
	var top := Vector2(data.top[0], data.top[1])
	var bottom := Vector2(data.bottom[0], data.bottom[1])
	var anchor := Vector2(data.hand_anchor[0], data.hand_anchor[1])
	var hand: Vector2 = joints.hand_near.to_global(anchor)
	bow_string.points = PackedVector2Array([to_local(joints.bow.to_global(top)), to_local(hand), to_local(joints.bow.to_global(bottom))])

func _draw() -> void:
	if debug_joints:
		for id in joints:
			draw_circle(to_local(joints[id].global_position), 1.5, Color.WHITE)
