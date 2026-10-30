extends Node2D
var actor: Node2D
var samples: Array = []
var direction := 1
var capture := false
var actions: OptionButton
func _ready() -> void:
	capture="--capture-weapons" in OS.get_cmdline_user_args()
	direction=-1 if "--left" in OS.get_cmdline_user_args() else 1
	RenderingServer.set_default_clear_color(Color("202833"))
	var title := Label.new()
	title.text="Kiếm / Cung — bản thử chưa duyệt | chuôi ở tay, hình vung vẽ sẵn, không xoay"
	title.position=Vector2(24,20)
	add_child(title)
	actor=load("res://pose_rig/rig_frames.tscn").instantiate()
	add_child(actor)
	actor.position=Vector2(460,270)
	actor.set_facing(direction)
	var reference := Sprite2D.new()
	reference.texture=load("res://pose_rig/art/reference_side.png")
	reference.centered=false
	reference.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
	reference.scale=Vector2(.5,.5)
	reference.position=Vector2(260,174)
	add_child(reference)
	var controls := HBoxContainer.new()
	controls.position=Vector2(24,66)
	add_child(controls)
	var classes := OptionButton.new()
	classes.add_item("Phái Kiếm")
	classes.add_item("Phái Cung")
	controls.add_child(classes)
	actions=OptionButton.new()
	controls.add_child(actions)
	refresh_actions()
	classes.item_selected.connect(func(index: int) -> void:
		actor.set_school("kiem" if index==0 else "cung")
		refresh_actions())
	actions.item_selected.connect(func(index: int) -> void:
		actor.clear_arrows()
		actor.elapsed=0
		actor.sample(actions.get_item_text(index),0))
	var flip := Button.new()
	flip.text="Đổi hướng"
	controls.add_child(flip)
	flip.pressed.connect(func() -> void:
		direction*=-1
		actor.set_facing(direction)
		for item in samples:item.set_facing(direction))
	var weapon := CheckButton.new()
	weapon.text="Vũ khí"
	weapon.button_pressed=true
	controls.add_child(weapon)
	weapon.toggled.connect(func(value: bool) -> void:actor.weapon_enabled=value;actor.sprites.weapon.visible=value)
	var back := Button.new()
	back.text="Về A0"
	controls.add_child(back)
	back.pressed.connect(func() -> void:get_tree().change_scene_to_file("res://main.tscn"))
	var frames: Array = [["kiem","idle",0],["kiem","slash",0],["kiem","slash",1],["kiem","slash",2],["kiem","slash",3],["kiem","thrust",0],["kiem","thrust",1],["cung","idle",0],["cung","shoot",0],["cung","shoot",1],["cung","shoot",2]]
	for i in frames.size():
		var item=load("res://pose_rig/rig_frames.tscn").instantiate()
		add_child(item)
		item.autoplay=false
		item.set_process(false)
		item.position=Vector2(48+i*100,465)
		item.set_school(frames[i][0])
		item.sample(frames[i][1],frames[i][2])
		item.set_facing(direction)
		samples.append(item)
		var label := Label.new()
		label.text="%s %s %d" % [frames[i][0],frames[i][1],frames[i][2]+1]
		label.position=item.position+Vector2(-28,16)
		label.add_theme_font_size_override("font_size",11)
		add_child(label)
	if capture:
		actor.autoplay=false
		actor.sample("idle",0)
		capture_view.call_deferred()
func refresh_actions() -> void:
	actions.clear()
	for name_ in actor.clips:actions.add_item(name_)
func capture_view() -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var image:=get_viewport().get_texture().get_image()
	var path:="res://pose_rig/reports/kiem_cung_%s.png" % ("left" if direction<0 else "right")
	DirAccess.make_dir_recursive_absolute("res://pose_rig/reports")
	var error:=image.save_png(path)
	print("Actual Godot Kiếm/Cung viewport: %s %dx%d error=%d" % [path,image.get_width(),image.get_height(),error])
	get_tree().quit(error)
