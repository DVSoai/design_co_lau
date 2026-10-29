extends "res://scripts/world.gd"
## Disposable G1 map viewer: no quests, enemy AI, boss combat, inventory or saves.
signal map_loaded(key: String)
signal respawned(reason: String, destination: Vector2)
const Loader = preload("res://dao_uc/layout_loader.gd")
const LayoutPlayer = preload("res://dao_uc/layout_player.gd")
const TILE := Loader.TILE
const COLORS := {"#":Color("7d5537"),"=":Color("d9b25f"),"^":Color("b23a2e"),
	"~":Color("4f8fa6"),"L":Color("5e9441"),"S":Color("2e4fa3"),"R":Color("3cbebe"),
	"E":Color("6b4a8c"),"N":Color("d9a520"),"m":Color("e68c78"),"M":Color("c8503c"),
	"B":Color("781414"),"D":Color("5a3c28"),"G":Color("3c3c46"),"c":Color("ffd700")}
var maps: Dictionary = {}
var map_key := "field"
var map_size := Vector2.ZERO
var data: Dictionary
var terrain: Node2D
var ladders: Array[Rect2] = []
var water: Array[Rect2] = []
var hazards: Array[Rect2] = []
var mannequins: Array[StaticBody2D] = []
var marker_label: Label
var notice: Label
var down_button: Button
var leave_button: Button
var transition_pending := false
var reset_count := 0
var transition_count := 0
var current_checkpoint := Vector2.ZERO
var input_lock_frames := 0

func _ready() -> void:
	maps = {"field":Loader.load_map("field"),"boss":Loader.load_map("boss")}
	map_size = maps.field.size
	super._ready()
	# Discard only the temporary A0 terrain/player made by base ready; reuse its
	# tuning, Camera2D, touch controls, gear and input registration without forks.
	for child in get_children():
		if child is StaticBody2D:
			child.free()
	player.free()
	player = LayoutPlayer.new()
	player.layout_world = self
	player.tuning = tuning
	add_child(player)
	terrain = Node2D.new()
	terrain.name = "LayoutCells"
	add_child(terrain)
	_register_input("climb_up",[KEY_UP,KEY_W])
	_register_input("climb_down",[KEY_DOWN,KEY_S])
	_register_input("ladder_jump",[KEY_SPACE])
	var hud := CanvasLayer.new()
	add_child(hud)
	marker_label = Label.new()
	marker_label.position = Vector2(250,82)
	hud.add_child(marker_label)
	notice = Label.new()
	notice.position = Vector2(250,108)
	hud.add_child(notice)
	var back := Button.new()
	back.text = "Về A0"
	back.focus_mode = Control.FOCUS_NONE
	back.position = Vector2(250,24)
	back.custom_minimum_size = Vector2(100,44)
	hud.add_child(back)
	back.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://main.tscn"))
	down_button = _ladder_button(hud,"↓",Vector2(24,250),"climb_down")
	leave_button = _ladder_button(hud,"Nhảy",Vector2(104,250),"ladder_jump")
	load_map("field")

func _ladder_button(hud: CanvasLayer, caption: String, point: Vector2, action: String) -> Button:
	var button := Button.new()
	button.text = caption
	button.position = point
	button.custom_minimum_size = Vector2(72,56)
	button.focus_mode = Control.FOCUS_NONE
	button.add_theme_font_size_override("font_size",22)
	hud.add_child(button)
	button.button_down.connect(func() -> void: Input.action_press(action))
	button.button_up.connect(func() -> void: Input.action_release(action))
	return button

func _camera_world_size() -> Vector2:
	return map_size

func load_map(key: String, returning := false) -> void:
	player.set_physics_process(false)
	for child in terrain.get_children():
		child.free()
	ladders.clear()
	water.clear()
	hazards.clear()
	mannequins.clear()
	map_key = key
	data = maps[key]
	map_size = data.size
	# Merge runs only for collider efficiency; counts and drawing still use every
	# canonical grid cell. Collision top always equals row*32.
	for y in data.rows.size():
		var x := 0
		while x < data.rows[y].length():
			var symbol: String = data.rows[y].substr(x,1)
			if symbol == "#" or symbol == "=":
				var start := x
				while x < data.rows[y].length() and data.rows[y].substr(x,1) == symbol:
					x += 1
				_solid(Rect2(start*TILE,y*TILE,(x-start)*TILE,TILE),symbol == "=")
			else:
				x += 1
	for symbol in data.points:
		for cell: Vector2i in data.points[symbol]:
			var rect := Rect2(Vector2(cell)*TILE,Vector2.ONE*TILE)
			if symbol == "~":
				water.append(rect)
			elif symbol == "^":
				hazards.append(rect)
				var area := Area2D.new()
				area.collision_layer = 0
				area.collision_mask = 2
				area.position = rect.get_center()
				var shape := CollisionShape2D.new()
				var box := RectangleShape2D.new()
				box.size = rect.size
				shape.shape = box
				area.add_child(shape)
				terrain.add_child(area)
				area.body_entered.connect(func(body: Node2D) -> void:
					if body == player and not transition_pending and player.is_physics_processing():
						player.set_physics_process(false)
						call_deferred("respawn","spikes"))
			elif symbol in ["N","M","m","B"]:
				var figure := Dummy.new()
				figure.position = Loader.feet(cell)
				figure.self_modulate = COLORS[symbol]
				terrain.add_child(figure)
				mannequins.append(figure)
				var label := Label.new()
				label.text = "%s (%d,%d) — hình nộm" % [symbol,cell.x,cell.y]
				label.position = Vector2(-20,-T.DUMMY_BOX.y-22)
				figure.add_child(label)
			elif symbol not in [".","#","=","L"]:
				var label := Label.new()
				label.text = "%s (%d,%d)" % [symbol,cell.x,cell.y]
				label.position = Vector2(cell)*TILE
				terrain.add_child(label)
	# Group ladder cells by column, respecting breaks rather than inventing links.
	for x in data.rows[0].length():
		var y := 0
		while y < data.rows.size():
			if data.rows[y].substr(x,1) != "L":
				y += 1
				continue
			var start := y
			while y < data.rows.size() and data.rows[y].substr(x,1) == "L":
				y += 1
			ladders.append(Rect2(x*TILE,start*TILE,TILE,(y-start)*TILE))
	dummy = mannequins[0]
	player.facing = -1 if returning else 1
	var destination: Vector2 = Loader.feet(data.points["S"][0])
	if returning:
		destination = Loader.feet(data.points["R"][-1])
	_teleport(destination)
	transition_pending = false
	notice.text = "D mở sẵn; hình nộm không đánh trả; chưa có nhiệm vụ/AI"
	map_loaded.emit(key)
	queue_redraw()

func _solid(rect: Rect2, one_way: bool) -> void:
	var body := StaticBody2D.new()
	body.position = rect.get_center()
	body.collision_layer = 1
	var shape := CollisionShape2D.new()
	var box := RectangleShape2D.new()
	box.size = rect.size
	shape.shape = box
	shape.one_way_collision = one_way
	body.add_child(shape)
	terrain.add_child(body)

func _teleport(destination: Vector2) -> void:
	player.set_physics_process(false)
	player.position = destination
	player.clear_layout_state()
	current_checkpoint = destination
	camera_anchor = destination
	camera.position = camera_target()
	camera.reset_smoothing()
	input_lock_frames = 2

func checkpoint_before(point: Vector2) -> Vector2:
	var result: Vector2 = Loader.feet(data.points["S"][0])
	var best := -INF
	for cell: Vector2i in data.points.get("R",[]):
		var candidate := Loader.feet(cell)
		if candidate.x <= point.x and candidate.x > best:
			best = candidate.x
			result = candidate
	return result

func respawn(reason: String) -> void:
	if transition_pending:
		return
	reset_count += 1
	var destination := checkpoint_before(player.position)
	_teleport(destination)
	respawned.emit(reason,destination)

func in_water(point: Vector2) -> bool:
	for rect in water:
		if rect.has_point(point-Vector2(0,1)):
			return true
	return false

func ladder_at(point: Vector2) -> Rect2:
	var body := Rect2(point-Vector2(T.PLAYER_BOX.x/2,T.PLAYER_BOX.y),T.PLAYER_BOX)
	for ladder in ladders:
		if body.intersects(ladder) and absf(point.x-ladder.get_center().x) <= (TILE+T.PLAYER_BOX.x)/2:
			return ladder
	return Rect2()

func _physics_process(_delta: float) -> void:
	if input_lock_frames > 0:
		input_lock_frames -= 1
		if input_lock_frames == 0:
			player.set_physics_process(true)
		return
	if transition_pending:
		return
	for cell: Vector2i in data.points["E"]:
		if not Rect2(Vector2(cell)*TILE,Vector2.ONE*TILE).has_point(player.position-Vector2(0,1)):
			continue
		if map_key == "field" and cell.x == data.rows[0].length()-1:
			transition_pending = true
			transition_count += 1
			player.set_physics_process(false)
			call_deferred("load_map","boss")
		elif map_key == "boss" and cell.x == 0:
			transition_pending = true
			transition_count += 1
			player.set_physics_process(false)
			call_deferred("load_map","field",true)
		else:
			notice.text = "Tràng An ↔ Đào Úc" if map_key == "field" else "E → Đầm lầy Đại Hoàng sau thắng/CS06 (ngoài bản thử)"

func _process(delta: float) -> void:
	super._process(delta)
	var cell := Vector2i(floori(player.position.x/TILE),floori((player.position.y-0.1)/TILE))
	marker_label.text = "%s — chân (c%d,r%d), px(%.1f,%.1f) — F1 hitbox" % [map_key,cell.x,cell.y,player.position.x,player.position.y]
	var near := ladder_at(player.position).has_area()
	down_button.visible = near or player.climbing
	leave_button.visible = near or player.climbing
	for figure in mannequins:
		figure.debug_enabled = debug_enabled
		figure.queue_redraw()

func _draw() -> void:
	if data.is_empty():
		return
	for y in data.rows.size():
		for x in data.rows[y].length():
			var symbol: String = data.rows[y].substr(x,1)
			if COLORS.has(symbol):
				draw_rect(Rect2(x*TILE,y*TILE,TILE,TILE),COLORS[symbol])

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		_release_ladder_input()

func _exit_tree() -> void:
	_release_ladder_input()

func _release_ladder_input() -> void:
	for action in ["climb_up","climb_down","ladder_jump"]:
		if InputMap.has_action(action):
			Input.action_release(action)
