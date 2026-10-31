extends "res://scripts/world.gd"
## A separate flat greybox with A0 physics, touch routing, camera and damage text.
const PosePlayer=preload("res://pose_rig/play_player.gd")
const PoseControls=preload("res://pose_rig/play_controls.gd")
var terrain: Array[Rect2]=[]
func _ready() -> void:
	for spec in [["left",[KEY_A,KEY_LEFT]],["right",[KEY_D,KEY_RIGHT]],["jump",[KEY_SPACE,KEY_W,KEY_UP]],["slash",[KEY_J,KEY_X]],["debug",[KEY_F1]],["pose_switch",[KEY_TAB]],["pose_tram",[KEY_1]],["pose_xa",[KEY_2]],["pose_skill",[]]]:
		_register_input(spec[0],spec[1])
	terrain=[Rect2(0,460,T.WORLD_SIZE.x,80),Rect2(680,396,150,16),Rect2(900,364,150,16),Rect2(1150,396,150,16)]
	for rect in terrain:
		var body:=StaticBody2D.new()
		body.position=rect.get_center()
		var shape:=CollisionShape2D.new()
		var rectangle:=RectangleShape2D.new()
		rectangle.size=rect.size
		shape.shape=rectangle
		body.add_child(shape)
		add_child(body)
	player=PosePlayer.new()
	player.tuning=tuning
	player.position=T.SPAWN
	add_child(player)
	dummy=Dummy.new()
	dummy.position=T.DUMMY_POSITION
	add_child(dummy)
	camera=Camera2D.new()
	camera.position=get_viewport_rect().size/2
	add_child(camera)
	var layer:=CanvasLayer.new()
	add_child(layer)
	debug_label=Label.new()
	debug_label.visible=false
	layer.add_child(debug_label)
	tuning_panel=TuningPanel.new()
	tuning_panel.tuning=tuning
	layer.add_child(tuning_panel)
	touch_controls=PoseControls.new()
	touch_controls.tuning=tuning
	touch_controls.tuning_panel=tuning_panel
	touch_controls.player=player
	layer.add_child(touch_controls)
	touch_buttons=touch_controls.buttons
	var back:=Button.new()
	back.text="Về A0"
	back.position=Vector2(300,16)
	back.focus_mode=Control.FOCUS_NONE
	layer.add_child(back)
	back.pressed.connect(func() -> void:get_tree().change_scene_to_file("res://main.tscn"))
	var help:=Label.new()
	help.text="Thử nhân vật mới | Tab/PHÁI: Kiếm ↔ Cung | 1: Trảm Kiếm | 2: Xạ Tiễn"
	help.position=Vector2(12,78)
	layer.add_child(help)
	if "--capture-play" in OS.get_cmdline_user_args():capture_play.call_deferred()
func capture_play() -> void:
	var args:=OS.get_cmdline_user_args()
	if "--cung" in args:player.switch_school()
	player.position=Vector2(390,460)
	player.facing=-1 if "--left" in args else 1
	# Keep the running review clear of the dummy; normal gameplay is unaffected.
	if "--run" in args and player.facing>0:player.position.x=300
	for i in 5:await get_tree().physics_frame
	if "--run" in args:
		Input.action_press("left" if player.facing<0 else "right")
		for i in 20:await get_tree().physics_frame
	if "--attack" in args:
		if "--skill" in args:player.request_skill("tram_kiem" if player.school=="kiem" else "xa_tien")
		else:Input.action_press("slash")
		await get_tree().physics_frame
		Input.action_release("slash")
		for i in 6:await get_tree().physics_frame
	await RenderingServer.frame_post_draw
	var path:="res://pose_rig/reports/play_%s_%s%s.png" % [player.school,"left" if player.facing<0 else "right","_run_v3" if "--run" in args else ("_skill" if "--skill" in args else "")]
	var err:=get_viewport().get_texture().get_image().save_png(path)
	print("Actual Godot play-test capture %s 1600x720 error=%d" % [path,err])
	get_tree().quit(0 if err==OK else 1)
func _draw() -> void:
	for rect in terrain:draw_rect(rect,Color("56604f"))
