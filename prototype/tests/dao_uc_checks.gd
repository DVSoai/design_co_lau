extends SceneTree
## Real physics/input walk-through, not coordinate teleports along the required route.
const Loader = preload("res://dao_uc/layout_loader.gd")
const T = preload("res://config/tuning.gd")
var failures := 0
var world: Node2D
var tick_count := 0

func check(ok: bool, message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:
		failures += 1

func _initialize() -> void:
	call_deferred("run")

func tick(count: int) -> void:
	for i in count:
		await physics_frame
		await process_frame
		tick_count += 1

func release() -> void:
	for action in ["left","right","jump","climb_up","climb_down","ladder_jump","touch_left","touch_right","touch_jump","touch_diagonal_left","touch_diagonal_right"]:
		Input.action_release(action)

func settle_at(point: Vector2) -> void:
	release()
	world._teleport(point)
	world.player.facing = 1
	await tick(8)

func json_checks() -> void:
	for key in Loader.FILES:
		var map: Dictionary = world.maps[key]
		var source: String = ProjectSettings.globalize_path("res://").path_join("../"+str(map.source.file)).simplify_path()
		var originals := PackedStringArray()
		if FileAccess.file_exists(source):
			var source_bytes := FileAccess.get_file_as_bytes(source)
			check(FileAccess.get_sha256(source) == str(map.source.sha256),"%s JSON source SHA256 matches canonical Markdown" % key)
			var regex := RegEx.new()
			regex.compile("(?m)^```layout[ \\t]*\\r?\\n([\\s\\S]*?)^```")
			var found := regex.search(source_bytes.get_string_from_utf8())
			check(found != null,"%s original Markdown layout block found" % key)
			if found == null:
				continue
			var lines := found.get_string(1).split("\n")
			if lines[-1].is_empty():
				lines.remove_at(lines.size()-1)
			for line in lines:
				originals.append(line.trim_suffix("\r"))
			var same: bool = originals.size() == map.rows.size()
			var tested := 0
			for y in originals.size():
				if y >= map.rows.size() or originals[y].length()!=map.rows[y].length():
					same = false
					continue
				for x in originals[y].length():
					tested += 1
					same = same and originals[y].substr(x,1)==map.rows[y].substr(x,1)
			check(same,"%s JSON matches every original cell (%d compared)" % [key,tested])
		else:
			print("INFO: %s original design/maps not available (exported runtime); source comparison skipped, export_layout_json.py --check must run before build" % key)
			originals = map.rows
		for symbol in ["#","=","^","~","L"]:
			var original_count := 0
			for line in originals:
				original_count += line.count(symbol)
			var count := int(map.counts.get(symbol,0))
			print("GRID %s '%s': original=%d loaded=%d" % [key,symbol,original_count,count])
			check(count == original_count,"%s '%s' counts match original grid" % [key,symbol])

func walk_to(exit_x: float, stop_on_map := "") -> bool:
	var original_map: String = world.map_key
	var resets_before: int = world.reset_count
	var start_x: float = world.player.position.x
	Input.action_press("right")
	var jumps := 0
	var frames := 0
	while frames < 2400:
		if stop_on_map != "" and world.map_key == stop_on_map:
			break
		if world.map_key == original_map and world.player.position.x >= exit_x:
			break
		if world.reset_count != resets_before:
			break
		var p = world.player
		if p.is_on_floor():
			# Determine imminent gaps/steps/spikes from parsed cells, not a hand-coded
			# list. Start 56px before steps, 24px before gaps, 32px before spikes.
			var support_row := roundi(p.position.y/Loader.TILE)
			var current_col := floori(p.position.x/Loader.TILE)
			var obstacle := false
			for ahead in range(current_col+1,mini(current_col+4,world.data.rows[0].length())):
				var edge: float = ahead*Loader.TILE
				if support_row>=world.data.rows.size():
					continue
				var floor_cell: String = world.data.rows[support_row].substr(ahead,1)
				var above: String = world.data.rows[support_row-1].substr(ahead,1)
				if floor_cell == "." and edge-p.position.x <= 24:
					obstacle = true
				elif above == "#" and edge-p.position.x <= 56:
					obstacle = true
				elif above == "^" and edge-p.position.x <= 32:
					obstacle = true
			if obstacle:
				Input.action_press("jump")
				jumps += 1
			else:
				Input.action_release("jump")
		else:
			# Retain the same press until grounded; no fresh near-apex press.
			pass
		await tick(1)
		frames += 1
	release()
	print("WALK %s: x%.2f -> map=%s x%.2f; frames=%d jumps=%d resets=%d" % [original_map,start_x,world.map_key,world.player.position.x,frames,jumps,world.reset_count-resets_before])
	return world.reset_count == resets_before and ((stop_on_map != "" and world.map_key == stop_on_map) or (world.map_key == original_map and world.player.position.x>=exit_x))

func run() -> void:
	world = load("res://dao_uc/dao_uc.tscn").instantiate()
	root.add_child(world)
	world.map_loaded.connect(func(key: String) -> void:
		check(not world.player.is_physics_processing() and world.input_lock_frames>0 and world.camera.position.distance_to(world.camera_target())<0.001,"%s map switch camera snapped while player input locked" % key))
	world.respawned.connect(func(reason: String, _destination: Vector2) -> void:
		check(not world.player.is_physics_processing() and world.input_lock_frames>0 and world.camera.position.distance_to(world.camera_target())<0.001,"%s respawn camera snapped before input unlock" % reason))
	await tick(5)
	await hud_checks()
	json_checks()
	var spawn: Vector2 = Loader.feet(world.data.points.S[0])
	check(world.player.position.distance_to(spawn)<0.1,"field appears at canonical S")
	await tick(60)
	check(world.player.is_on_floor() and world.player.position.distance_to(spawn)<0.2,"field S stays grounded and still after 1 second")
	check(world.camera.position.is_equal_approx(world.camera_target()),"spawn camera reset before player input")
	var extra_before: int = world.player.extra_jump_count
	check(await walk_to(INF,"boss"),"S -> field E right -> boss using real right/jump input, no falls")
	await tick(65)
	var boss_spawn: Vector2 = Loader.feet(world.data.points.S[0])
	check(world.map_key=="boss" and world.player.is_on_floor() and world.player.position.distance_to(boss_spawn)<0.2,"boss appears at S and stays grounded after 1 second")
	check(await walk_to(58.2*Loader.TILE),"walk to rampart foot and climb the 32px steps from the grid")
	var rampart_y: float = Loader.feet(world.data.points.m[0]).y
	check(world.player.is_on_floor() and absf(world.player.position.y-rampart_y)<0.2,"player reaches top rampart at canonical y%.0f" % rampart_y)
	check(world.player.extra_jump_count==extra_before,"required route never uses khinh cong")
	# Return through actual boss-left portal; positioning here starts a separate
	# test, it does not contribute to the forward traversal assertion above.
	await settle_at(Vector2(60,288))
	Input.action_press("left")
	await tick(30)
	release()
	check(world.map_key=="field","boss left E returns to field right-side R")
	check(world.camera.position.x>=world.map_size.x-root.get_visible_rect().size.x/2-1,"return portal resets camera at right map clamp")
	await settle_at(Vector2(44.5*Loader.TILE,288))
	var before: int = world.reset_count
	for i in 120:
		await tick(1)
		if world.reset_count>before:break
	check(world.reset_count==before+1 and world.player.position.distance_to(Vector2(432,288))<0.2,"fall into c44-45 -> preceding R c13, not A0 SPAWN")
	await tick(10)
	await settle_at(Vector2(85.5*Loader.TILE,288))
	before = world.reset_count
	Input.action_press("right")
	for i in 40:
		await tick(1)
		if world.reset_count>before:break
	release()
	check(world.reset_count==before+1 and world.player.position.distance_to(Vector2(432,288))<0.2,"spikes reset to preceding R without HP system")
	await tick(8)
	# Shallow water uses 0.7 multiplier; A0 tuning itself remains 200.
	await settle_at(Vector2(81*Loader.TILE+16,288))
	Input.action_press("right")
	await tick(2)
	check(is_equal_approx(world.player.velocity.x,140.0) and is_equal_approx(world.tuning.value("RUN_SPEED"),200.0),"water speed 140=0.7*200 while A0 RUN_SPEED stays 200")
	release()
	# One-way shelf: rise from below, pass through, land on top after apex.
	await settle_at(Vector2(36.5*Loader.TILE,288))
	Input.action_press("jump")
	await tick(1)
	Input.action_release("jump")
	await tick(55)
	check(world.player.is_on_floor() and absf(world.player.position.y-224)<0.2,"one-way shelf passed from below and landed on top")
	await settle_at(Vector2(109.5*Loader.TILE,288))
	Input.action_press("touch_jump") # same action as the on-screen ↑
	await tick(86)
	release()
	check(world.player.climbing and world.player.position.y<160,"hold touch ↑ climbs ladder c109 above r4 shelf height")
	Input.action_press("climb_down")
	var climb_y: float = world.player.position.y
	await tick(10)
	release()
	check(world.player.position.y>climb_y+10,"hold down descends ladder")
	Input.action_press("climb_up")
	await tick(16)
	release()
	Input.action_press("left")
	await tick(12)
	release()
	await tick(40)
	check(not world.player.climbing and world.player.is_on_floor() and absf(world.player.position.y-160)<0.2,"leave ladder left and stand at r4 feet on upper shelf y160")
	await settle_at(Vector2(109.5*Loader.TILE,288))
	Input.action_press("climb_up")
	Input.action_press("jump") # keyboard ↑ is also bound to A0 jump
	await tick(30)
	var jump_before: int = world.player.jump_count
	Input.action_press("ladder_jump")
	await tick(2)
	check(not world.player.climbing and world.player.jump_count==jump_before+1 and world.player.velocity.y<0,"Space/context jump leaves ladder using original A0 jump resolver")
	release()
	# Dummies remain A0 hittable bodies; no enemy attack loop.
	var figure: StaticBody2D = world.mannequins[0]
	var initial_hits: int = figure.hit_count
	await settle_at(figure.position-Vector2(36,0))
	world.player.facing = 1
	Input.action_press("slash")
	await tick(20)
	Input.action_release("slash")
	check(figure.hit_count==initial_hits+1,"canonical N dummy accepts A0 slash damage")
	release()
	world.queue_free()
	await tick(3)
	print("Dao Uc checks failures: %d; physics frames=%d" % [failures,tick_count])
	quit(1 if failures else 0)

func hud_checks() -> void:
	var original := root.size
	for key in ["field","boss"]:
		world.load_map(key)
		for width in [960,1200]:
			root.size = Vector2i(width,540)
			await tick(5)
			var expected: Dictionary = world.data.hud.expected_top_rects[str(width)]
			for name in expected:
				var box: Array = expected[name]
				var wanted := Rect2(box[0],box[1],box[2]-box[0],box[3]-box[1])
				var actual := Rect2()
				if name == "gear":
					actual = world.tuning_panel.toggle.get_global_rect()
				elif name == "menu":
					actual = world.touch_controls.buttons.menu.get_global_rect()
				elif name == "boss_hp":
					actual = world.boss_bar.get_global_rect()
				else:
					actual = world.touch_controls.hud_rects["map" if name=="minimap" else name]
				check(actual.is_equal_approx(wanted),"%s %d top HUD %s actual rectangle matches Python checker" % [key,width,name])
			check(world.boss_bar.visible == (key=="boss"),"%s boss bar visibility" % key)
			if key=="boss":
				check(not world.touch_controls.hud_rects.map.has_area(),"SCR-06 minimap hidden (A)")
				world.tuning.set_flag("HUD_VISIBLE",false)
				await tick(2)
				world.tuning.set_flag("HUD_VISIBLE",true)
				await tick(1)
				check(not world.touch_controls.hud_rects.map.has_area(),"SCR-06 minimap stays hidden immediately after HUD toggle")
	root.size = original
	world.load_map("field")
	await tick(5)
