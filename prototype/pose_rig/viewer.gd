extends Node2D
var actor: Node2D
var samples: Array = []
var direction := 1
var capture := false
func _ready() -> void:
	capture = "--capture-poses" in OS.get_cmdline_user_args()
	direction = -1 if "--left" in OS.get_cmdline_user_args() else 1
	RenderingServer.set_default_clear_color(Color("202833"))
	var title := Label.new()
	title.text = "Bộ tư thế vẽ trọn — bản thử chưa duyệt | Ảnh gốc / idle / run 1–6 / jump / slash 1–4"
	title.position = Vector2(24,20)
	add_child(title)
	actor = load("res://pose_rig/rig_frames.tscn").instantiate()
	add_child(actor)
	actor.position = Vector2(460,285)
	actor.set_facing(direction)
	var reference := Sprite2D.new()
	reference.texture = load("res://pose_rig/art/reference_side.png")
	reference.centered = false
	reference.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
	reference.scale = Vector2(.5,.5)
	reference.position = Vector2(260,189)
	add_child(reference)
	var controls := HBoxContainer.new()
	controls.position = Vector2(24,66)
	add_child(controls)
	for name_ in ["idle","run","jump","fall","slash"]:
		var button := Button.new()
		button.text = name_
		button.focus_mode = Control.FOCUS_NONE
		controls.add_child(button)
		button.pressed.connect(func() -> void: actor.elapsed=0;actor.sample(name_,0))
	var flip := Button.new()
	flip.text = "Đổi hướng"
	controls.add_child(flip)
	flip.pressed.connect(func() -> void:
		direction *= -1
		actor.set_facing(direction)
		for item in samples: item.set_facing(direction))
	var weapon := CheckButton.new()
	weapon.text = "Đao"
	weapon.button_pressed = true
	controls.add_child(weapon)
	weapon.toggled.connect(func(value: bool) -> void: actor.weapon_enabled=value;actor.sprites.weapon.visible=value)
	var back := Button.new()
	back.text = "Về A0"
	controls.add_child(back)
	back.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://main.tscn"))
	var frames: Array = [["idle",0],["run",0],["run",1],["run",2],["run",3],["run",4],["run",5],["jump",0],["slash",0],["slash",1],["slash",2],["slash",3]]
	for i in frames.size():
		var item = load("res://pose_rig/rig_frames.tscn").instantiate()
		add_child(item)
		item.autoplay = false
		item.position = Vector2(50+i*77,460)
		item.sample(frames[i][0],frames[i][1])
		item.set_facing(direction)
		samples.append(item)
		var label := Label.new()
		label.text = "%s %d" % [frames[i][0],frames[i][1]+1]
		label.position = item.position + Vector2(-22,14)
		label.add_theme_font_size_override("font_size",12)
		add_child(label)
	if capture:
		actor.autoplay=false
		actor.sample("idle",0)
		capture_view.call_deferred()
func capture_view() -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var image := get_viewport().get_texture().get_image()
	var path := "res://pose_rig/reports/scene_%s.png" % ("left" if direction<0 else "right")
	DirAccess.make_dir_recursive_absolute("res://pose_rig/reports")
	var error := image.save_png(path)
	print("Actual Godot viewport capture: %s %dx%d error=%d" % [path,image.get_width(),image.get_height(),error])
	get_tree().quit(error)
