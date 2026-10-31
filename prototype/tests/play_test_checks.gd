extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,text: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+text)
	if not ok:failures+=1
func ticks(n: int) -> void:
	for i in n:await physics_frame;await process_frame
func press(action: String,n: int) -> void:
	Input.action_press(action)
	await ticks(n)
	Input.action_release(action)
	await ticks(2)
func run() -> void:
	var scene=load("res://pose_rig/play_test.tscn").instantiate()
	root.add_child(scene)
	await ticks(8)
	var p=scene.player
	check(p.is_on_floor(),"new pose player lands on flat greybox")
	for school in ["kiem","cung"]:
		if p.school!=school:p.switch_school()
		p.position=Vector2(200,460)
		p.velocity=Vector2.ZERO
		await ticks(8)
		var start: Vector2=p.position
		await press("right",12)
		check(p.position.x>start.x+20,"%s walks via actual input and inherited A0 physics" % school)
		await press("jump",4)
		check(p.position.y<start.y-10 and not p.is_on_floor(),"%s jumps via actual input" % school)
		await ticks(18)
		check(p.actor.action=="apex_flip","%s shows baked apex somersault using A0 timing" % school)
		await ticks(47)
		p.position=Vector2(440,460)
		p.velocity=Vector2.ZERO
		p.facing=1
		p.cooldown_elapsed=INF
		await ticks(6)
		var hits: int=scene.dummy.hit_count
		await press("slash",1)
		await ticks(25)
		var number_visible:=false
		for child in scene.dummy.get_children():
			if child is Label and child.text==str(preload("res://config/tuning.gd").DAMAGE):number_visible=true
		check(number_visible,"%s hit displays the actual A0 damage number" % school)
		await ticks(40)
		check(scene.dummy.hit_count==hits+1,"%s normal attack hits dummy once and uses damage label" % school)
		if school=="cung":check(p.projectile_hits>0,"Cung damage comes from separate projectile collision")
		p.cooldown_elapsed=INF
		hits=scene.dummy.hit_count
		await press("pose_tram" if school=="kiem" else "pose_xa",1)
		await ticks(65)
		check(scene.dummy.hit_count==hits+1,"%s skill hits dummy once" % school)
		p.position=Vector2(540,460)
		p.velocity=Vector2.ZERO
		p.facing=-1
		p.cooldown_elapsed=INF
		await ticks(6)
		hits=scene.dummy.hit_count
		await press("slash",1)
		await ticks(65)
		check(scene.dummy.hit_count==hits+1,"%s left-facing attack hits dummy once" % school)
	# Touch route, including independent two-finger movement+jump.
	scene.touch_controls._set_pointer(10,"right")
	scene.touch_controls._set_pointer(11,"jump")
	await ticks(3)
	check(Input.is_action_pressed("touch_right") and Input.is_action_pressed("touch_jump"),"multitouch d-pad keeps independent movement and jump actions")
	scene.touch_controls.release_all()
	var previous: String=p.school
	scene.touch_controls._activate_placeholder("target")
	check(p.school!=previous,"touch PHÁI switches school")
	check(scene.touch_buttons.skill_1.visible and scene.touch_buttons.skill_2.visible,"two skill slots visible")
	print("Pose play-test checks failures=%d" % failures)
	scene.queue_free()
	await process_frame
	quit(1 if failures else 0)
