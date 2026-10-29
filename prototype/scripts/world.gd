extends Node2D

const T = preload("res://config/tuning.gd")
const Player = preload("res://scripts/player.gd")
const RuntimeTuning = preload("res://config/runtime_tuning.gd")
const TuningPanel = preload("res://scripts/tuning_panel.gd")
const TouchControls = preload("res://scripts/touch_controls.gd")
const Dummy = preload("res://scripts/dummy.gd")
var tuning := RuntimeTuning.new()
var tuning_panel: Control
var player: CharacterBody2D
var dummy: StaticBody2D
var camera: Camera2D
var debug_label: Label
var debug_enabled := false
var camera_anchor := T.SPAWN
var touch_buttons: Dictionary = {}
var touch_controls: Control

func _ready() -> void:
	_register_input("left", [KEY_A, KEY_LEFT])
	_register_input("right", [KEY_D, KEY_RIGHT])
	_register_input("jump", [KEY_SPACE, KEY_W, KEY_UP])
	_register_input("slash", [KEY_J, KEY_X])
	_register_input("debug", [KEY_F1])
	for rect: Rect2 in T.TERRAIN:
		var body := StaticBody2D.new()
		body.position = rect.get_center()
		var shape := CollisionShape2D.new()
		var rectangle := RectangleShape2D.new()
		rectangle.size = rect.size
		shape.shape = rectangle
		body.add_child(shape)
		add_child(body)
	player = Player.new()
	player.tuning = tuning
	player.position = T.SPAWN
	add_child(player)
	dummy = Dummy.new()
	dummy.position = T.DUMMY_POSITION
	add_child(dummy)
	camera = Camera2D.new()
	camera.position = get_viewport().get_visible_rect().size / 2
	add_child(camera)
	var layer := CanvasLayer.new()
	add_child(layer)
	debug_label = Label.new()
	debug_label.position = Vector2(12, 8)
	debug_label.add_theme_font_size_override("font_size", 14)
	debug_label.visible = false
	layer.add_child(debug_label)
	tuning_panel = TuningPanel.new()
	tuning_panel.tuning = tuning
	layer.add_child(tuning_panel)
	touch_controls = TouchControls.new()
	touch_controls.tuning = tuning
	touch_controls.tuning_panel = tuning_panel
	layer.add_child(touch_controls)
	touch_buttons = touch_controls.buttons

func camera_target() -> Vector2:
	var half := get_viewport().get_visible_rect().size / 2
	var target := camera_anchor + Vector2(player.facing * tuning.value("CAMERA_LOOK_AHEAD"), 0)
	# Nếu viewport rộng/cao hơn bản đồ, căn giữa thay vì clamp với min > max.
	target.x = clampf(target.x, half.x, _camera_world_size().x - half.x) if half.x * 2 < _camera_world_size().x else _camera_world_size().x / 2
	target.y = clampf(camera_anchor.y, half.y, _camera_world_size().y - half.y) if half.y * 2 < _camera_world_size().y else _camera_world_size().y / 2
	return target

func _register_input(action: String, keys: Array) -> void:
	if InputMap.has_action(action):
		return
	InputMap.add_action(action)
	for key in keys:
		var event := InputEventKey.new()
		event.physical_keycode = key
		InputMap.action_add_event(action, event)

func _process(delta: float) -> void:
	if Input.is_action_just_pressed("debug"):
		debug_enabled = not debug_enabled
		debug_label.visible = debug_enabled
		player.debug_enabled = debug_enabled
		dummy.debug_enabled = debug_enabled
		dummy.queue_redraw()
	touch_controls.set_debug_enabled(debug_enabled)
	# Vùng chết quanh anchor; look-ahead tiến mượt, không giật khi đổi hướng.
	var difference: Vector2 = player.position - camera_anchor
	camera_anchor.x += signf(difference.x) * maxf(0, absf(difference.x) - tuning.value("CAMERA_DEAD_ZONE.x"))
	camera_anchor.y += signf(difference.y) * maxf(0, absf(difference.y) - T.CAMERA_DEAD_ZONE.y)
	var target := camera_target()
	camera.position = camera.position.lerp(target, 1 - exp(-T.CAMERA_RESPONSE * delta))
	# Sau đổi tỉ lệ/viewport, clamp cả vị trí camera hiện tại ngay lập tức.
	var half := get_viewport().get_visible_rect().size / 2
	camera.position.x = clampf(camera.position.x, half.x, _camera_world_size().x - half.x) if half.x * 2 < _camera_world_size().x else _camera_world_size().x / 2
	camera.position.y = clampf(camera.position.y, half.y, _camera_world_size().y - half.y) if half.y * 2 < _camera_world_size().y else _camera_world_size().y / 2
	if debug_enabled:
		var lines := PackedStringArray([tuning_panel.display_info(), "F1: debug | Cyan: player | Red: active slash | Yellow: dummy"])
		# Hiển thị tất cả hằng số cấu hình, kể cả thông số suy ra.
		var tuning_script: Script = load("res://config/tuning.gd")
		var constants := tuning_script.get_script_constant_map()
		for key in constants:
			if key != "TERRAIN":
				lines.append("%s = %s" % [key, str(tuning.current_value(key, constants[key]))])
		debug_label.text = "\n".join(lines)
		debug_label.scale = Vector2(0.75, 0.75)
	queue_redraw()

func _draw() -> void:
	for rect: Rect2 in T.TERRAIN:
		draw_rect(rect, Color(0.36, 0.46, 0.30) if rect.size.y >= 32 else Color(0.62, 0.55, 0.34))
	if debug_enabled:
		draw_rect(Rect2(camera_anchor - Vector2(tuning.value("CAMERA_DEAD_ZONE.x"), T.CAMERA_DEAD_ZONE.y), Vector2(tuning.value("CAMERA_DEAD_ZONE.x"), T.CAMERA_DEAD_ZONE.y) * 2), Color(0.8, 0.8, 1, 0.7), false, 1)

# Layout scenes override bounds without replacing A0 camera/dead-zone behaviour.
func _camera_world_size() -> Vector2:
	return T.WORLD_SIZE
