extends SceneTree
var failures:=0
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func ticks(n: int) -> void:
	for i in n:await physics_frame;await process_frame
func run() -> void:
	var scene=load("res://pose_rig/play_test.tscn").instantiate();root.add_child(scene)
	await ticks(10)
	var p=scene.player
	for school in ["kiem","cung"]:
		if p.school!=school:p.switch_school()
		for direction in [-1,1]:
			p.position=Vector2(200,460);p.velocity=Vector2.ZERO;p.facing=direction
			await ticks(10)
			Input.action_press("jump");await ticks(2);Input.action_release("jump");await ticks(2)
			check(p.actor.action=="jump" and p.actor.frame_index==7,"%s dir%d actual upward input -> frame7" % [school,direction])
			var waited:=0
			while p.velocity.y<-absf(p.tuning.jump_speed())*.28 and waited<35:
				await ticks(1);waited+=1
			var extras: int=p.extra_jump_count
			Input.action_press("jump");await ticks(1);Input.action_release("jump")
			var seen: Dictionary={};var fall_seen:=false
			for i in 80:
				await ticks(1)
				if p.actor.action=="apex_flip":seen[p.actor.frame_index]=true
				if p.actor.action=="fall" and p.actor.frame_index==12:fall_seen=true
			check(p.extra_jump_count==extras+1,"fresh near-apex press performs A0 extra jump")
			check(seen.has(8) and seen.has(9) and seen.has(10) and seen.has(11),"%s dir%d extra jump displays all tucked frames8..11" % [school,direction])
			check(fall_seen,"%s dir%d actual descent -> frame12; never guard13" % [school,direction])
			check(p.tuning.value("TIME_TO_APEX")==.38 and p.tuning.value("APEX_FLIP_TIME")==.20,"unchanged A0 .38s apex / .20s roll")
	scene.queue_free();await process_frame
	print("Live air-frame checks failures=%d" % failures)
	quit(1 if failures else 0)
