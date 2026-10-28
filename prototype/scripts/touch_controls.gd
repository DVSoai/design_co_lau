extends Control

const T = preload("res://config/tuning.gd")
const DrawnButton = preload("res://scripts/drawn_button.gd")
var tuning: RefCounted
var tuning_panel: Control
var buttons: Dictionary = {}
var fingers: Dictionary = {} # pointer id → nút; nhiều ngón không nhả action của nhau
var active_actions: Dictionary = {}
var hud_rects: Dictionary = {}
var health_count := T.POTION_INITIAL_COUNT
var mana_count := T.POTION_INITIAL_COUNT
var previous_hud := true
const ACTIONS := {
	"left": ["touch_left"], "right": ["touch_right"], "jump": ["touch_jump"],
	"diag_left": ["touch_left", "touch_jump", "touch_diagonal_left"],
	"diag_right": ["touch_right", "touch_jump", "touch_diagonal_right"],
	"slash": ["touch_slash"],
}

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	for action in ["touch_left", "touch_right", "touch_jump", "touch_slash", "touch_diagonal_left", "touch_diagonal_right"]:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
	for key in ["left", "right", "jump", "diag_left", "diag_right", "slash", "target", "health", "mana", "menu"]:
		_add_button(key)
	for index in T.SKILL_COUNT:
		_add_button("skill_%d" % (index + 1))
	buttons.left.caption = "←"
	buttons.right.caption = "→"
	buttons.jump.caption = "↑"
	for key in ["diag_left", "diag_right"]:
		buttons[key].hit_only = true
		buttons[key].visible = false
	buttons.slash.caption = "CHÉM"
	buttons.target.caption = "ĐỔI"
	buttons.menu.caption = "≡"
	for key in ["slash", "target", "health", "mana"]:
		buttons[key].round_shape = true
	buttons.health.tint = Color(0.5, 0.08, 0.08)
	buttons.mana.tint = Color(0.08, 0.15, 0.5)
	for index in T.SKILL_COUNT:
		buttons["skill_%d" % (index + 1)].caption = str(index + 1)
	_update_counts()
	get_viewport().size_changed.connect(layout)
	layout()

func _add_button(key: String) -> void:
	var button := DrawnButton.new()
	buttons[key] = button
	add_child(button)

func _place(key: String, point: Vector2, dimensions: Vector2) -> void:
	var button: Control = buttons[key]
	button.position = point
	button.size = dimensions
	button.pivot_offset = dimensions / 2
	button.queue_redraw()

func layout() -> void:
	var rect := get_viewport().get_visible_rect()
	var d: float = T.TOUCH_BUTTON_SIZE.x
	var gap: float = T.TOUCH_GAP
	var margin: float = T.TOUCH_MARGIN
	var bottom: float = rect.end.y - margin
	var x: float = rect.position.x + margin
	var lower_y := bottom - d
	var upper_y := lower_y - T.DPAD_UP_OFFSET_RATIO * d
	_place("left", Vector2(x, lower_y), Vector2.ONE * d)
	_place("right", Vector2(x + T.DPAD_RIGHT_OFFSET_RATIO * d, lower_y), Vector2.ONE * d)
	_place("jump", Vector2(x + T.DPAD_RIGHT_OFFSET_RATIO * d / 2, upper_y), Vector2.ONE * d)
	var diagonal := Vector2(d * T.DIAGONAL_WIDTH_RATIO, d)
	_place("diag_left", buttons.jump.position - Vector2(diagonal.x, 0), diagonal)
	_place("diag_right", buttons.jump.position + Vector2(d, 0), diagonal)
	var slash_size := Vector2.ONE * d * T.SLASH_BUTTON_RATIO
	var slash_pos := Vector2(rect.end.x - margin - slash_size.x, bottom - slash_size.y)
	_place("slash", slash_pos, slash_size)
	var small := Vector2.ONE * d * T.SMALL_BUTTON_RATIO
	_place("target", Vector2(slash_pos.x + (slash_size.x - small.x) / 2, slash_pos.y - gap - small.y), small)
	_place("health", slash_pos - Vector2(gap + small.x, gap + small.y), small)
	_place("mana", Vector2(slash_pos.x - gap - small.x, slash_pos.y + (slash_size.y - small.y) / 2), small)
	var skill_size := Vector2.ONE * d * T.SKILL_BUTTON_RATIO
	var row_width: float = T.SKILL_COUNT * skill_size.x + (T.SKILL_COUNT - 1) * T.SKILL_GAP
	for index in T.SKILL_COUNT:
		_place("skill_%d" % (index + 1), Vector2(rect.get_center().x - row_width / 2 + index * (skill_size.x + T.SKILL_GAP), bottom - skill_size.y), skill_size)
	var top := rect.position + Vector2.ONE * margin
	hud_rects = {
		"level": Rect2(top, T.HUD_LEVEL_SIZE),
		"hp": Rect2(top + Vector2(T.HUD_LEVEL_SIZE.x + gap, 0), T.HUD_BAR_SIZE),
		"mp": Rect2(top + Vector2(T.HUD_LEVEL_SIZE.x + gap, T.HUD_BAR_SIZE.y + T.HUD_BAR_GAP), T.HUD_BAR_SIZE),
		"map": Rect2(Vector2(rect.end.x - margin - T.HUD_MAP_SIZE.x, top.y), T.HUD_MAP_SIZE),
	}
	_place("menu", Vector2(hud_rects.map.position.x - gap - T.HUD_MENU_SIZE.x, top.y), T.HUD_MENU_SIZE)
	buttons.menu.visible = tuning.flag("HUD_VISIBLE")
	queue_redraw()

func set_debug_enabled(enabled: bool) -> void:
	for key in ["diag_left", "diag_right"]:
		if buttons[key].visible != enabled:
			buttons[key].visible = enabled
			buttons[key].queue_redraw()

func _hit(point: Vector2) -> String:
	# Thứ tự tường minh; vùng vô hình vẫn bắt chạm dù CanvasItem đang ẩn.
	var priority := ["jump", "diag_left", "diag_right", "left", "right"]
	for key in priority:
		if (buttons[key].hit_only or buttons[key].visible) and buttons[key].contains(point):
			return key
	for key in buttons:
		if key not in priority and buttons[key].visible and buttons[key].contains(point):
			return key
	return ""

func _set_pointer(id: int, key: String, activate: bool = true) -> void:
	var old: String = fingers.get(id, "")
	if old == key:
		return
	if key.is_empty():
		fingers.erase(id)
	else:
		fingers[id] = key
		if activate and not ACTIONS.has(key):
			_activate_placeholder(key)
	_sync_actions()

func _sync_actions() -> void:
	var desired: Dictionary = {}
	for key in fingers.values():
		for action in ACTIONS.get(key, []):
			desired[action] = true
	for action in active_actions:
		if not desired.has(action):
			Input.action_release(action)
	for action in desired:
		if not active_actions.has(action):
			Input.action_press(action)
	active_actions = desired
	var feedback := {"left": "touch_left", "right": "touch_right", "jump": "touch_jump", "slash": "touch_slash"}
	for key in buttons:
		buttons[key].set_held(desired.has(feedback[key]) if feedback.has(key) else key in fingers.values())

func _activate_placeholder(key: String) -> void:
	if key == "health":
		health_count = maxi(0, health_count - 1)
		print("A0 placeholder: health bottle count=", health_count)
	elif key == "mana":
		mana_count = maxi(0, mana_count - 1)
		print("A0 placeholder: mana bottle count=", mana_count)
	else:
		print("A0 placeholder: ", key)
	_update_counts()

func _update_counts() -> void:
	buttons.health.caption = "HP\n%d" % health_count
	buttons.mana.caption = "MP\n%d" % mana_count
	buttons.health.queue_redraw()
	buttons.mana.queue_redraw()

func _blocked(point: Vector2) -> bool:
	return is_instance_valid(tuning_panel) and tuning_panel.panel.visible and tuning_panel.panel.get_global_rect().has_point(point)

func _input(event: InputEvent) -> void:
	if event is InputEventScreenTouch:
		if event.pressed:
			if not _blocked(event.position):
				var key := _hit(event.position)
				if not key.is_empty():
					_set_pointer(event.index, key)
					get_viewport().set_input_as_handled()
		elif fingers.has(event.index):
			_set_pointer(event.index, "")
			get_viewport().set_input_as_handled()
	elif event is InputEventScreenDrag and fingers.has(event.index):
		_set_pointer(event.index, "" if _blocked(event.position) else _hit(event.position), false)
		get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton and event.device != -1 and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed and not _blocked(event.position):
			var key := _hit(event.position)
			if not key.is_empty():
				_set_pointer(-1, key)
				get_viewport().set_input_as_handled()
		elif not event.pressed and fingers.has(-1):
			_set_pointer(-1, "")
			get_viewport().set_input_as_handled()
	elif event is InputEventMouseMotion and event.device != -1 and fingers.has(-1):
		_set_pointer(-1, "" if _blocked(event.position) else _hit(event.position), false)
		get_viewport().set_input_as_handled()

func release_all() -> void:
	fingers.clear()
	_sync_actions()

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT and is_node_ready():
		release_all()

func _exit_tree() -> void:
	for action in active_actions:
		Input.action_release(action)

func _process(_delta: float) -> void:
	if previous_hud != tuning.flag("HUD_VISIBLE"):
		previous_hud = tuning.flag("HUD_VISIBLE")
		layout()

func _draw() -> void:
	if not tuning.flag("HUD_VISIBLE"):
		return
	var fill := Color(0.08, 0.1, 0.14, T.TOUCH_FILL_ALPHA)
	var level: Rect2 = hud_rects.get("level", Rect2())
	draw_circle(level.get_center(), level.size.x / 2, fill)
	draw_arc(level.get_center(), level.size.x / 2, 0, TAU, 64, T.TOUCH_BORDER, T.TOUCH_BORDER_WIDTH, true)
	for key in ["hp", "mp", "map"]:
		var rect: Rect2 = hud_rects.get(key, Rect2())
		draw_rect(rect, Color(0.7, 0.1, 0.1) if key == "hp" else (Color(0.1, 0.25, 0.8) if key == "mp" else fill))
		draw_rect(rect, T.TOUCH_BORDER, false, T.TOUCH_BORDER_WIDTH)
