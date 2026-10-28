extends Control

const RuntimeTuning = preload("res://config/runtime_tuning.gd")
var tuning: RefCounted
var panel: PanelContainer
var toggle: Button
var sliders: Dictionary = {}

func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	toggle = Button.new()
	toggle.text = "⚙"
	toggle.tooltip_text = "Chỉnh thông số A0"
	toggle.position = Vector2(904, 8)
	toggle.size = Vector2(44, 40)
	add_child(toggle)
	panel = PanelContainer.new()
	panel.position = Vector2(510, 54)
	panel.size = Vector2(438, 366)
	panel.visible = false
	add_child(panel)
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.custom_minimum_size = Vector2(438, 366)
	panel.add_child(scroll)
	var column := VBoxContainer.new()
	column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(column)
	var title := Label.new()
	title.text = "A0 — chỉnh trực tiếp (không lưu)"
	column.add_child(title)
	for row in RuntimeTuning.SLIDERS:
		var key: String = row[0]
		var label := Label.new()
		column.add_child(label)
		var slider := HSlider.new()
		slider.min_value = row[1]
		slider.max_value = row[2]
		slider.step = row[3]
		slider.value = tuning.value(key)
		slider.custom_minimum_size = Vector2(400, 28)
		sliders[key] = slider
		var unit: String = row[4]
		label.text = "%s: %.2f %s" % [key, slider.value, unit]
		slider.value_changed.connect(func(number: float) -> void:
			tuning.set_value(key, number)
			label.text = "%s: %.2f %s" % [key, tuning.value(key), unit]
		)
		column.add_child(slider)
	var copy := Button.new()
	copy.text = "Sao chép"
	copy.custom_minimum_size.y = 40
	copy.pressed.connect(func() -> void: DisplayServer.clipboard_set(tuning.as_text()))
	column.add_child(copy)
	toggle.pressed.connect(func() -> void: panel.visible = not panel.visible)
