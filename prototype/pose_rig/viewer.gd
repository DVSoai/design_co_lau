extends Node2D
var actor: Node2D
var samples: Array = []
var direction := 1
var capture := false
var actions: OptionButton
var school_option: OptionButton
var levels: OptionButton
var old_content_size := Vector2i(960,540)
func _ready() -> void:
	old_content_size=get_window().content_scale_size
	get_window().content_scale_size=Vector2i(1600,720)
	capture="--capture-swing" in OS.get_cmdline_user_args()
	direction=-1 if "--left" in OS.get_cmdline_user_args() else 1
	RenderingServer.set_default_clear_color(Color("202833"))
	label_at("Mỗi mẫu chỉ Kiếm HOẶC Cung | Lưỡi theo cấp + vệt chung | CHƯA DUYỆT",Vector2(24,12),22)
	actor=load("res://pose_rig/rig_frames.tscn").instantiate()
	add_child(actor)
	actor.position=Vector2(430,194)
	actor.set_facing(direction)
	var controls := HBoxContainer.new()
	controls.position=Vector2(24,46)
	add_child(controls)
	school_option=OptionButton.new()
	school_option.add_item("Kiếm")
	school_option.add_item("Cung")
	controls.add_child(school_option)
	actions=OptionButton.new()
	controls.add_child(actions)
	refresh_actions()
	school_option.item_selected.connect(func(index: int) -> void:
		actor.set_school("kiem" if index==0 else "cung")
		levels.disabled=index==1
		refresh_actions())
	actions.item_selected.connect(func(index: int) -> void:
		actor.clear_arrows()
		actor.elapsed=0
		actor.autoplay=true
		actor.sample(actions.get_item_text(index),0))
	levels=OptionButton.new()
	for level in [1,30,60]:levels.add_item("Cấp%d" % level,level)
	controls.add_child(levels)
	levels.item_selected.connect(func(index: int) -> void:actor.set_weapon_level(levels.get_item_id(index)))
	var play := Button.new()
	play.text="Chạy slash —0,30s thật"
	controls.add_child(play)
	play.pressed.connect(func() -> void:
		actor.set_school("kiem")
		school_option.select(0)
		levels.disabled=false
		refresh_actions()
		actor.elapsed=0
		actor.autoplay=true
		actor.sample("slash",0))
	var flip := Button.new()
	flip.text="Đổi hướng"
	controls.add_child(flip)
	flip.pressed.connect(func() -> void:
		direction*=-1
		actor.set_facing(direction)
		for item in samples:item.set_facing(direction))
	var back := Button.new()
	back.text="VềA0"
	controls.add_child(back)
	back.pressed.connect(func() -> void:
		get_window().content_scale_size=old_content_size
		get_tree().change_scene_to_file("res://main.tscn"))
	label_at("Xem chuyển động / chọn phái và cấp",Vector2(200,204),14)
	for i in 2:
		var bow=load("res://pose_rig/rig_frames.tscn").instantiate()
		add_child(bow)
		bow.set_school("cung")
		bow.autoplay=false
		bow.set_process(false)
		bow.position=Vector2(890+i*260,194)
		bow.sample("shoot",i+1)
		bow.set_facing(direction)
		samples.append(bow)
		label_at("Cung: tên trên dây" if i==0 else "Buông: tên bay riêng",bow.position+Vector2(-90,10),14)
	for row in 3:
		var level: int=[1,30,60][row]
		for index in 5:
			var item=load("res://pose_rig/rig_frames.tscn").instantiate()
			add_child(item)
			item.autoplay=false
			item.set_process(false)
			item.position=Vector2(80+index*300,335+row*172)
			item.set_weapon_level(level)
			item.sample("slash",index)
			item.set_facing(direction)
			samples.append(item)
			label_at("Cấp%d | nhịp%d" % [level,index+1],item.position+Vector2(-35,12),14)
	if capture:
		actor.autoplay=false
		actor.sample("slash",2)
		capture_view.call_deferred()
func label_at(text: String, at: Vector2, size: int) -> void:
	var label := Label.new()
	label.text=text
	label.position=at
	label.add_theme_font_size_override("font_size",size)
	add_child(label)
func refresh_actions() -> void:
	actions.clear()
	for name_ in actor.clips:actions.add_item(name_)
func capture_view() -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var image:=get_viewport().get_texture().get_image()
	var path:="res://pose_rig/reports/swing_%s.png" % ("left" if direction<0 else "right")
	var error:=image.save_png(path)
	print("Actual Godot swing capture: %s %dx%d error=%d; 3levels x5static beats" % [path,image.get_width(),image.get_height(),error])
	get_tree().quit(error)
