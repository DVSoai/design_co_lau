extends CanvasLayer
## The only addition to the original A0 scene is this navigation child.
func _ready() -> void:
	var button := Button.new()
	button.text = "Mở rig greybox"
	button.focus_mode = Control.FOCUS_NONE
	button.custom_minimum_size = Vector2(190, 44)
	add_child(button)
	var layout := func() -> void:
		button.position = Vector2(get_viewport().get_visible_rect().size.x / 2 - 95, 24)
	get_viewport().size_changed.connect(layout)
	layout.call()
	button.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://rig/rig_greybox.tscn"))
