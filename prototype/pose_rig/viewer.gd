extends Node2D
var actor: Node2D
var samples: Array = []
var school := "kiem"
var direction := 1
var page := "frames"
var air_mode:=false
var action_option: OptionButton
var old_size: Vector2i
func _ready() -> void:
	old_size=get_window().content_scale_size
	get_window().content_scale_size=Vector2i(1600,720)
	RenderingServer.set_default_clear_color(Color("202833"))
	var args:=OS.get_cmdline_user_args()
	if "--cung" in args:school="cung"
	if "--left" in args:direction=-1
	if "--attacks" in args:page="attacks"
	if "--compare" in args:page="compare"
	build()
	if "--capture-lv1" in args:capture.call_deferred()
func label_at(text: String, at: Vector2, size: int=18) -> Label:
	var l:=Label.new()
	l.text=text
	l.position=at
	l.add_theme_font_size_override("font_size",size)
	add_child(l)
	return l
func make_actor(at: Vector2, factor: float=1.0, moving: bool=false) -> Node2D:
	var holder:=Node2D.new()
	holder.position=at
	holder.scale=Vector2.ONE*factor
	add_child(holder)
	var a=load("res://pose_rig/rig_frames.tscn").instantiate()
	holder.add_child(a)
	a.set_school(school)
	a.airborne=air_mode
	a.set_facing(direction)
	a.autoplay=moving
	if not moving:a.set_process(false)
	samples.append(a)
	return a
func build() -> void:
	label_at("Lv1 — 4 lớp / 30 khung | Mỗi người chỉ Kiếm HOẶC Cung | CHƯA DUYỆT",Vector2(20,8),22)
	var controls:=HBoxContainer.new()
	controls.position=Vector2(20,40)
	add_child(controls)
	var pick:=OptionButton.new()
	pick.add_item("Kiếm")
	pick.add_item("Cung")
	pick.select(0 if school=="kiem" else 1)
	controls.add_child(pick)
	pick.item_selected.connect(func(i: int) -> void:
		school="kiem" if i==0 else "cung"
		rebuild())
	action_option=OptionButton.new()
	controls.add_child(action_option)
	for id in ["idle","run","jump","fall","apex_flip"]:action_option.add_item(id)
	for id in (["slash","tram_kiem"] if school=="kiem" else ["shoot","xa_tien"]):action_option.add_item(id)
	action_option.item_selected.connect(func(i: int) -> void:actor.clear_arrows();actor.play(action_option.get_item_text(i)))
	var air:=CheckButton.new()
	air.text="Trên không"
	air.button_pressed=air_mode
	controls.add_child(air)
	air.toggled.connect(func(on: bool) -> void:
		air_mode=on
		actor.airborne=on
		actor.clear_arrows()
		actor.play(action_option.get_item_text(action_option.selected)))
	for title in ["Chạy lại","Đổi hướng","30 khung","Các đòn/chiêu","So cạnh bảng","Về A0"]:
		var b:=Button.new()
		b.text=title
		controls.add_child(b)
		b.pressed.connect(button_pressed.bind(title))
	if page=="frames":
		for i in 30:
			var cell:=Rect2(12+(i%6)*264,78+(i/6)*128,252,120)
			var a=make_actor(cell.get_center(),128.0/96.204)
			a.sample_frame(i)
			var box: Rect2=actor_bounds(a)
			var factor:=minf(1.0,minf(236.0/box.size.x,102.0/box.size.y))
			a.get_parent().scale*=factor
			box=actor_bounds(a)
			a.get_parent().position+=cell.get_center()-box.get_center()+Vector2(0,-5)
			label_at("%02d" % i,cell.position+Vector2(2,101),14)

		actor=make_actor(Vector2(1490,96),.3,true)
	elif page=="attacks":
		var ids: Array=["slash","tram_kiem"] if school=="kiem" else ["shoot","xa_tien"]
		for row in 2:
			var a=make_actor(Vector2(100,360+row*310),(128.0/96.204),true)
			a.play(ids[row])
			if row==0:actor=a
			label_at(ids[row]+" / tốc độ thật",Vector2(24,110+row*310),20)
			for i in a.skills_data[ids[row]].ground.size():
				var columns:=3 if school=="kiem" else 4
				var step:=360 if school=="kiem" else 275
				var at:=Vector2(500+(i%columns)*step,210+row*310+(i/columns)*140)
				var s=make_actor(at,(128.0/96.204))
				s.action=ids[row]
				s.sample_beat(i,true)
				label_at("Nhịp%d" % i,at+Vector2(-90,-110),16)
	else:
		label_at("Mẫu Lv1 từ bảng — chỉ để đối chiếu",Vector2(60,100),22)
		var t:=Sprite2D.new()
		t.texture=load("res://pose_rig/reports/reference_lv1.png")
		t.texture_filter=CanvasItem.TEXTURE_FILTER_NEAREST
		t.position=Vector2(250,350)
		t.scale=Vector2.ONE*4
		add_child(t)
		label_at("Lv1 mới — Kiếm" if school=="kiem" else "Lv1 mới — Cung",Vector2(680,100),22)
		actor=make_actor(Vector2(850,430),(128.0/96.204),true)
		var close=make_actor(Vector2(1250,570),4.0)
		close.sample_frame(0)
		label_at("Cỡ 128 px",Vector2(760,460),18)
		label_at("Phóng để so nét",Vector2(1140,600),18)
func rebuild() -> void:
	for c in get_children():
		remove_child(c)
		c.queue_free()
	samples.clear()
	build()
func capture() -> void:
	await RenderingServer.frame_post_draw
	await RenderingServer.frame_post_draw
	var im:=get_viewport().get_texture().get_image()
	var path:="res://pose_rig/reports/lv1_%s_%s_%s.png" % [school,page,"left" if direction<0 else "right"]
	var err:=im.save_png(path)
	print("Actual Godot capture %s %dx%d error=%d" % [path,im.get_width(),im.get_height(),err])
	get_tree().quit(err)

func button_pressed(title: String) -> void:
	if title=="Chạy lại":
		actor.clear_arrows()
		actor.play(action_option.get_item_text(action_option.selected))
	elif title=="Đổi hướng":
		direction*=-1
		for a in samples:a.set_facing(direction)
	elif title=="Về A0":
		get_window().content_scale_size=old_size
		get_tree().change_scene_to_file("res://main.tscn")
	else:
		page={"30 khung":"frames","Các đòn/chiêu":"attacks","So cạnh bảng":"compare"}[title]
		rebuild()

func actor_bounds(a: Node2D) -> Rect2:
	var result:=Rect2()
	var first:=true
	for sprite: Sprite2D in a.all_visual_sprites():
		if not sprite.visible or sprite.texture==null:continue
		var rect:=Rect2(sprite.texture.get_image().get_used_rect())
		if sprite.centered:rect.position-=sprite.texture.get_size()/2
		var corners: Array=[sprite.to_global(rect.position),sprite.to_global(rect.end),sprite.to_global(Vector2(rect.position.x,rect.end.y)),sprite.to_global(Vector2(rect.end.x,rect.position.y))]
		for point: Vector2 in corners:
			if first:result=Rect2(point,Vector2.ZERO);first=false
			else:result=result.expand(point)
	return result
