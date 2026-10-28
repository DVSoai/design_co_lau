extends HSlider

# Native HSlider không nhận input; overlay chỉ cho kéo từ vùng núm.
# PASS giữ cử chỉ dọc/con lăn đi tiếp tới ScrollContainer.
var surface: Control
var pointer := -2 # -2: không có, -1: chuột, >= 0: ngón tay
var origin := Vector2.ZERO
var initial_value := 0.0
var horizontal := false
var vertical := false
const DIRECTION_THRESHOLD := 8.0 # px logic trước khi xác định hướng vuốt

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	focus_mode = Control.FOCUS_NONE
	scrollable = false
	surface = Control.new()
	surface.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	surface.mouse_filter = Control.MOUSE_FILTER_PASS
	surface.focus_mode = Control.FOCUS_NONE
	surface.gui_input.connect(_surface_input)
	add_child(surface)

func thumb_center() -> Vector2:
	var width := float(get_theme_icon("grabber").get_width())
	return Vector2(width / 2 + ratio * (size.x - width), size.y / 2)

func _begin(point: Vector2, id: int) -> void:
	# Vùng chạm của núm rộng tối thiểu 32 px, cao đủ 44 px; track không nhận.
	var hit_size := Vector2(maxf(32, get_theme_icon("grabber").get_width()), size.y)
	if pointer == -2 and Rect2(thumb_center() - hit_size / 2, hit_size).has_point(point):
		pointer = id
		origin = point
		initial_value = value
		horizontal = false
		vertical = false

func _drag(point: Vector2) -> void:
	var movement := point - origin
	if not horizontal and not vertical and movement.length() >= DIRECTION_THRESHOLD:
		horizontal = absf(movement.x) > absf(movement.y)
		vertical = not horizontal
	if horizontal:
		var travel := maxf(1, size.x - get_theme_icon("grabber").get_width())
		value = initial_value + movement.x / travel * (max_value - min_value)
		surface.accept_event()

func _surface_input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		if event.pressed:
			_begin(event.position, event.index)
		elif pointer == event.index:
			if horizontal:
				surface.accept_event()
			pointer = -2
	elif event is InputEventScreenDrag and pointer == event.index:
		_drag(event.position)
	elif event is InputEventMouseButton:
		if event.device == -1: # bỏ chuột giả từ touch, tránh xử lý một ngón hai lần
			return
		if event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				_begin(event.position, -1)
			elif pointer == -1:
				if horizontal:
					surface.accept_event()
				pointer = -2
	elif event is InputEventMouseMotion and pointer == -1:
		_drag(event.position)
