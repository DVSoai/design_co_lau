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

	var map_button := Button.new()
	map_button.text = "Đào Úc greybox"
	map_button.focus_mode = Control.FOCUS_NONE
	map_button.custom_minimum_size = Vector2(190,44)
	add_child(map_button)
	var map_layout := func() -> void:
		map_button.position = Vector2(get_viewport().get_visible_rect().size.x/2-95,80)
	get_viewport().size_changed.connect(map_layout)
	map_layout.call()
	map_button.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://dao_uc/dao_uc.tscn"))

	var pose_button := Button.new()
	pose_button.text = "Nhân vật tư thế (thử)"
	pose_button.focus_mode = Control.FOCUS_NONE
	pose_button.custom_minimum_size = Vector2(220,44)
	add_child(pose_button)
	var pose_layout := func() -> void:
		pose_button.position = Vector2(get_viewport().get_visible_rect().size.x/2-110,136)
	get_viewport().size_changed.connect(pose_layout)
	pose_layout.call()
	pose_button.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://pose_rig/pose_rig.tscn"))
