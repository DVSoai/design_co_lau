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

func _ready() -> void:
	definition = JSON.parse_string(FileAccess.get_file_as_string("res://rig/data/parts.json"))
	clips = JSON.parse_string(FileAccess.get_file_as_string("res://rig/data/animations.json"))["clips"]
	pivot_root = Node2D.new()
	pivot_root.name = "PoseRoot"
	# Rotation centre at torso centre, not at the feet.
	pivot_root.position = Vector2(definition.rotation_center[0], definition.rotation_center[1])
	add_child(pivot_root)
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
	player = AnimationPlayer.new()
	player.name = "AnimationPlayer"
	add_child(player)
	var library := AnimationLibrary.new()
	for key in clips:
		library.add_animation(key, _make_animation(clips[key]))
	player.add_animation_library("", library)
	set_weapon("dao")
	play_clip("idle")

func _make_animation(clip: Dictionary) -> Animation:
	var anim := Animation.new()
	var duration := 0.0
	for frame in clip.frames:
		duration += float(frame.duration)
	anim.length = duration
	anim.loop_mode = Animation.LOOP_LINEAR if clip.loop else Animation.LOOP_NONE
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

func set_weapon(value: String) -> void:
	weapon = value
	if not shapes.is_empty():
		shapes.dao.visible = value == "dao"
		shapes.bow.visible = value == "bow"

func play_clip(value: String, restart := false) -> void:
	if current_clip != value or restart:
		current_clip = value
		player.play(value)
		player.advance(0)

func sample(value: String, time: float) -> void:
	play_clip(value, true)
	player.pause()
	player.seek(time, true)
	queue_redraw()

func geometry() -> Array:
	# Used by the contact-sheet exporter: actual evaluated scene polygons/transforms.
	var result: Array = []
	for id in shapes:
		var shape: Polygon2D = shapes[id]
		if not shape.visible:
			continue
		var points: Array = []
		for vertex in shape.polygon:
			var point := to_local(shape.to_global(vertex))
			points.append([point.x, point.y])
		result.append({"id": id, "z": shape.z_index, "color": shape.color.to_html(), "points": points})
	return result

func _draw() -> void:
	if debug_joints:
		for id in joints:
			draw_circle(to_local(joints[id].global_position), 1.5, Color.WHITE)
