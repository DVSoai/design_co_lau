extends Control

const T = preload("res://config/tuning.gd")
var caption := ""
var round_shape := false
var held := false
var tint := Color(0.08, 0.1, 0.14)

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	focus_mode = Control.FOCUS_NONE

func contains(point: Vector2) -> bool:
	var local := point - position
	if round_shape:
		return local.distance_to(size / 2) <= size.x / 2
	return Rect2(Vector2.ZERO, size).has_point(local)

func set_held(active: bool) -> void:
	held = active
	pivot_offset = size / 2
	scale = Vector2.ONE * (T.TOUCH_PRESSED_SCALE if held else 1.0)
	queue_redraw()

func _draw() -> void:
	var fill := Color(tint, T.TOUCH_FILL_ALPHA)
	var border: Color = T.TOUCH_PRESSED_BORDER if held else T.TOUCH_BORDER
	if round_shape:
		draw_circle(size / 2, size.x / 2, fill)
		draw_arc(size / 2, size.x / 2 - T.TOUCH_BORDER_WIDTH / 2, 0, TAU, 64, border, T.TOUCH_BORDER_WIDTH, true)
	else:
		draw_rect(Rect2(Vector2.ZERO, size), fill)
		draw_rect(Rect2(Vector2.ZERO, size).grow(-T.TOUCH_BORDER_WIDTH / 2), border, false, T.TOUCH_BORDER_WIDTH)
	var font := ThemeDB.fallback_font
	var rows := caption.split("\n")
	var line_height := float(T.TOUCH_FONT_SIZE)
	for i in rows.size():
		var text_size := font.get_string_size(rows[i], HORIZONTAL_ALIGNMENT_LEFT, -1, T.TOUCH_FONT_SIZE)
		var baseline := size.y / 2 - (rows.size() - 1) * line_height / 2 + i * line_height + font.get_ascent(T.TOUCH_FONT_SIZE) - font.get_height(T.TOUCH_FONT_SIZE) / 2
		draw_string(font, Vector2((size.x - text_size.x) / 2, baseline), rows[i], HORIZONTAL_ALIGNMENT_LEFT, -1, T.TOUCH_FONT_SIZE, border)
