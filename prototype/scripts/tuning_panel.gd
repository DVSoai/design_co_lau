extends Control

const T = preload("res://config/tuning.gd")
const ThumbSlider = preload("res://scripts/thumb_slider.gd")
const RuntimeTuning = preload("res://config/runtime_tuning.gd")
var tuning: RefCounted
var panel: PanelContainer
var toggle: Button
var sliders: Dictionary = {}
var motion_toggle: CheckButton
var scale_toggle: CheckButton
var info_label: Label
var scroll: ScrollContainer
var switches: Dictionary = {}
var previous_hud := true

func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	toggle = Button.new()
	toggle.focus_mode = Control.FOCUS_NONE
	toggle.text = "⚙"
	toggle.tooltip_text = "Chỉnh thông số A0"
	toggle.position = Vector2(904, 8)
	toggle.custom_minimum_size = T.GEAR_SIZE
	toggle.size = T.GEAR_SIZE
	toggle.add_theme_font_size_override("font_size", T.TOUCH_FONT_SIZE)
	for state in ["normal", "hover", "pressed"]:
		var style := StyleBoxFlat.new()
		style.bg_color = Color(0.08, 0.1, 0.14, T.TOUCH_FILL_ALPHA)
		style.border_color = T.TOUCH_PRESSED_BORDER if state == "pressed" else T.TOUCH_BORDER
		style.set_border_width_all(int(T.TOUCH_BORDER_WIDTH))
		toggle.add_theme_stylebox_override(state, style)
	toggle.button_down.connect(func() -> void: toggle.scale = Vector2.ONE * T.TOUCH_PRESSED_SCALE)
	toggle.button_up.connect(func() -> void: toggle.scale = Vector2.ONE)
	add_child(toggle)
	panel = PanelContainer.new()
	panel.position = Vector2(510, 54)
	panel.size = Vector2(438, 366)
	panel.visible = false
	add_child(panel)
	scroll = ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.custom_minimum_size = Vector2(438, 366)
	panel.add_child(scroll)
	var column := VBoxContainer.new()
	column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(column)
	var title := Label.new()
	title.text = "A0 — chỉnh trực tiếp (không lưu)"
	column.add_child(title)
	info_label = Label.new()
	info_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	info_label.custom_minimum_size.x = 400
	info_label.add_theme_font_size_override("font_size", 12)
	column.add_child(info_label)
	scale_toggle = CheckButton.new()
	scale_toggle.focus_mode = Control.FOCUS_NONE
	scale_toggle.text = "Phóng nguyên/lẻ (bật = nguyên)"
	scale_toggle.button_pressed = get_window().content_scale_stretch == Window.CONTENT_SCALE_STRETCH_INTEGER
	scale_toggle.toggled.connect(func(integer: bool) -> void:
		get_window().content_scale_stretch = Window.CONTENT_SCALE_STRETCH_INTEGER if integer else Window.CONTENT_SCALE_STRETCH_FRACTIONAL
	)
	column.add_child(scale_toggle)
	motion_toggle = CheckButton.new()
	motion_toggle.focus_mode = Control.FOCUS_NONE
	motion_toggle.text = "Chuyển động giả"
	motion_toggle.button_pressed = tuning.fake_motion_enabled()
	motion_toggle.toggled.connect(tuning.set_fake_motion_enabled)
	column.add_child(motion_toggle)
	for row in [["HOLD_AUTO_JUMP", "Giữ để nhảy lại"], ["VARIABLE_JUMP", "Giữ lâu nhảy cao"], ["DIAGONAL_SPIN_ENABLED", "Xoay khi nhảy chéo"], ["HUD_VISIBLE", "Hiện HUD giữ chỗ"]]:
		var key: String = row[0]
		var check := CheckButton.new()
		check.focus_mode = Control.FOCUS_NONE
		check.text = row[1]
		check.button_pressed = tuning.flag(key)
		check.toggled.connect(func(enabled: bool) -> void: tuning.set_flag(key, enabled))
		switches[key] = check
		column.add_child(check)
	for row in RuntimeTuning.SLIDERS:
		var key: String = row[0]
		var label := Label.new()
		column.add_child(label)
		var slider := ThumbSlider.new()
		slider.focus_mode = Control.FOCUS_NONE
		slider.scrollable = false
		slider.min_value = row[1]
		slider.max_value = row[2]
		slider.step = row[3]
		slider.value = tuning.value(key)
		slider.custom_minimum_size = Vector2(400, 44)
		sliders[key] = slider
		var unit: String = row[4]
		label.text = "%s: %.2f %s" % [key, slider.value, unit]
		slider.value_changed.connect(func(number: float) -> void:
			tuning.set_value(key, number)
			label.text = "%s: %.2f %s" % [key, tuning.value(key), unit]
		)
		column.add_child(slider)
	var copy := Button.new()
	copy.focus_mode = Control.FOCUS_NONE
	copy.text = "Sao chép"
	copy.custom_minimum_size.y = 40
	copy.pressed.connect(func() -> void: DisplayServer.clipboard_set(tuning.as_text()))
	column.add_child(copy)
	toggle.pressed.connect(func() -> void: panel.visible = not panel.visible)
	get_viewport().size_changed.connect(_layout)
	_layout()

func _layout() -> void:
	var rect := get_viewport().get_visible_rect()
	var margin: float = T.TOUCH_MARGIN
	var gap: float = T.TOUCH_GAP
	var reserve: float = T.HUD_MAP_SIZE.x + T.HUD_MENU_SIZE.x + 2 * gap if tuning.flag("HUD_VISIBLE") else 0.0
	toggle.position = Vector2(rect.end.x - margin - reserve - toggle.size.x, rect.position.y + margin)
	toggle.pivot_offset = toggle.size / 2
	var panel_y: float = rect.position.y + margin + (maxf(T.HUD_MAP_SIZE.y, T.GEAR_SIZE.y) if tuning.flag("HUD_VISIBLE") else T.GEAR_SIZE.y) + gap
	var controls_top: float = rect.end.y - margin - 2 * T.TOUCH_BUTTON_SIZE.y - gap
	var height := maxf(T.TUNING_PANEL_MIN_HEIGHT, minf(T.TUNING_PANEL_MAX_HEIGHT, controls_top - gap - panel_y))
	scroll.custom_minimum_size = Vector2(T.TUNING_PANEL_WIDTH, height)
	panel.size = Vector2(T.TUNING_PANEL_WIDTH, height)
	panel.position = Vector2(rect.end.x - panel.size.x - margin, panel_y)

func display_info() -> String:
	var viewport_size := get_viewport().get_visible_rect().size
	var window_size := Vector2(get_window().size)
	var screen_size := window_size if DisplayServer.get_name() == "headless" else Vector2(DisplayServer.screen_get_size())
	var scale := get_viewport().get_stretch_transform().get_scale()
	return "Screen %d×%d | Window %d×%d | Viewport %.1f×%.1f | Scale %.3f×%.3f" % [screen_size.x, screen_size.y, window_size.x, window_size.y, viewport_size.x, viewport_size.y, scale.x, scale.y]

func _process(_delta: float) -> void:
	info_label.text = display_info()
	if previous_hud != tuning.flag("HUD_VISIBLE"):
		previous_hud = tuning.flag("HUD_VISIBLE")
		_layout()
