extends CanvasLayer
func _ready() -> void:
	var button:=Button.new()
	button.text="Thử nhân vật mới"
	button.focus_mode=Control.FOCUS_NONE
	button.custom_minimum_size=Vector2(220,44)
	add_child(button)
	var layout:=func() -> void:button.position=Vector2(get_viewport().get_visible_rect().size.x/2-110,192)
	get_viewport().size_changed.connect(layout)
	layout.call()
	button.pressed.connect(func() -> void:get_tree().change_scene_to_file("res://pose_rig/play_test.tscn"))
