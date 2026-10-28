extends Node2D

const T = preload("res://config/tuning.gd")
const Player = preload("res://scripts/player.gd")
const RuntimeTuning = preload("res://config/runtime_tuning.gd")
const TuningPanel = preload("res://scripts/tuning_panel.gd")
const Dummy = preload("res://scripts/dummy.gd")
var tuning := RuntimeTuning.new()
var tuning_panel: Control
var player: CharacterBody2D
var dummy: StaticBody2D
var camera: Camera2D
var debug_label: Label
var debug_enabled := false
var camera_anchor := T.SPAWN

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
	camera.position = T.VIEWPORT / 2
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
	# TouchScreenButton giữ action theo từng ngón, hỗ trợ chạy + nhảy/chém.
	var size: Vector2 = T.TOUCH_BUTTON_SIZE
	var margin: float = T.TOUCH_MARGIN
	var stride: float = size.x + T.TOUCH_GAP
	var y: float = T.VIEWPORT.y - size.y - margin
	_touch_button(layer, "left", "←", Vector2(margin, y))
	_touch_button(layer, "right", "→", Vector2(margin + stride, y))
	_touch_button(layer, "jump", "NHẢY", Vector2(T.VIEWPORT.x - margin - stride - size.x, y))
	_touch_button(layer, "slash", "CHÉM", Vector2(T.VIEWPORT.x - margin - size.x, y))

func _register_input(action: String, keys: Array) -> void:
	if InputMap.has_action(action):
		return
	InputMap.add_action(action)
	for key in keys:
		var event := InputEventKey.new()
		event.physical_keycode = key
		InputMap.action_add_event(action, event)

func _touch_button(layer: CanvasLayer, action: String, caption: String, pos: Vector2) -> void:
	var button := TouchScreenButton.new()
	button.action = action
	button.position = pos + T.TOUCH_BUTTON_SIZE / 2
	button.visibility_mode = TouchScreenButton.VISIBILITY_TOUCHSCREEN_ONLY
	var shape := RectangleShape2D.new()
	shape.size = T.TOUCH_BUTTON_SIZE
	button.shape = shape
	button.shape_centered = false
	var panel := Polygon2D.new()
	var size: Vector2 = T.TOUCH_BUTTON_SIZE
	panel.polygon = PackedVector2Array([Vector2.ZERO, Vector2(size.x, 0), size, Vector2(0, size.y)])
	panel.position = -size / 2
	panel.color = Color(0.1, 0.12, 0.15, 0.55)
	button.add_child(panel)
	var label := Label.new()
	label.text = caption
	label.position = Vector2(22, 30) - size / 2
	button.add_child(label)
	layer.add_child(button)

func _process(delta: float) -> void:
	if Input.is_action_just_pressed("debug"):
		debug_enabled = not debug_enabled
		debug_label.visible = debug_enabled
		player.debug_enabled = debug_enabled
		dummy.debug_enabled = debug_enabled
		dummy.queue_redraw()
	# Vùng chết quanh anchor; look-ahead tiến mượt, không giật khi đổi hướng.
	var difference: Vector2 = player.position - camera_anchor
	camera_anchor.x += signf(difference.x) * maxf(0, absf(difference.x) - tuning.value("CAMERA_DEAD_ZONE.x"))
	camera_anchor.y += signf(difference.y) * maxf(0, absf(difference.y) - T.CAMERA_DEAD_ZONE.y)
	var target := camera_anchor + Vector2(player.facing * tuning.value("CAMERA_LOOK_AHEAD"), 0)
	target.x = clampf(target.x, T.VIEWPORT.x / 2, T.WORLD_SIZE.x - T.VIEWPORT.x / 2)
	target.y = T.VIEWPORT.y / 2 # Bản đồ A0 cao đúng một viewport.
	camera.position = camera.position.lerp(target, 1 - exp(-T.CAMERA_RESPONSE * delta))
	if debug_enabled:
		var lines := PackedStringArray(["F1: debug | Cyan: player | Red: active slash | Yellow: dummy"])
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
