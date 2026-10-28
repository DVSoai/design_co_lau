extends "res://scripts/world.gd"
## Inherits the A0 world and player unchanged. Adapter only reads player state.
const RigScene = preload("res://rig/rig.tscn")
var rig: Node2D
var rig_toggle: CheckButton
var bow_toggle: CheckButton
var preview: OptionButton
var enabled := true
var previous_floor := false
var previous_jump := 0
var previous_flip := 0
var flip_active := false
var land_remaining := 0.0
var flip_remaining := 0.0
var flip_sign := 1.0
var previous_flip_running := false
var view_elapsed := 0.0

func _ready() -> void:
	super._ready()
	rig = RigScene.instantiate()
	player.add_child(rig)
	var column: VBoxContainer = tuning_panel.scroll.get_child(0)
	rig_toggle = CheckButton.new()
	rig_toggle.text = "Rig greybox"
	rig_toggle.button_pressed = true
	rig_toggle.focus_mode = Control.FOCUS_NONE
	column.add_child(rig_toggle)
	column.move_child(rig_toggle, 1)
	rig_toggle.toggled.connect(func(value: bool) -> void:
		enabled = value
		rig.visible = value
		player.sprite.visible = not value
	)
	bow_toggle = CheckButton.new()
	bow_toggle.text = "Vũ khí cung (chỉ xem, không đổi hitbox)"
	bow_toggle.focus_mode = Control.FOCUS_NONE
	column.add_child(bow_toggle)
	column.move_child(bow_toggle, 2)
	bow_toggle.toggled.connect(func(value: bool) -> void: rig.set_weapon("bow" if value else "dao"))
	preview = OptionButton.new()
	preview.focus_mode = Control.FOCUS_NONE
	preview.add_item("Theo trạng thái thật A0")
	for key in rig.clips:
		preview.add_item(key)
	column.add_child(preview)
	column.move_child(preview, 3)
	preview.item_selected.connect(func(_index: int) -> void: view_elapsed = 0.0)
	var back := Button.new()
	back.text = "Về A0 gốc"
	back.focus_mode = Control.FOCUS_NONE
	column.add_child(back)
	column.move_child(back, 4)
	back.pressed.connect(func() -> void: get_tree().change_scene_to_file("res://main.tscn"))
	player.sprite.visible = false
	player.physics_stepped.connect(_sync_rig)

func _sync_rig() -> void:
	var delta := get_physics_process_delta_time()
	var floor_now: bool = player.is_on_floor()
	land_remaining = maxf(0, land_remaining - delta)
	if floor_now and not previous_floor:
		land_remaining = rig.player.get_animation("land").length
	if player.jump_count != previous_jump:
		flip_active = false
		flip_remaining = 0.0
	# Use the real A0 flip phase, including queued khinh-cong turns.
	if player.flip_running and (not previous_flip_running or player.flip_completion_count != previous_flip):
		flip_active = true
		flip_sign = player.flip_direction
		flip_remaining = player.tuning.value("APEX_FLIP_TIME")
	if player.flip_completion_count != previous_flip:
		flip_remaining = 0.0
		flip_active = false
	var clip := "idle"
	if player.attack_time >= 0:
		clip = "shoot" if bow_toggle.button_pressed else "slash_1"
	elif not floor_now:
		clip = "apex_flip" if flip_active else ("jump_up" if player.velocity.y < 0 else "fall")
	elif land_remaining > 0:
		clip = "land"
	elif player.turn_remaining > 0:
		clip = "turn"
	elif absf(player.velocity.x) > 1:
		clip = "run"
	view_elapsed += delta
	rig.scale.x = player.facing
	if preview.selected > 0:
		clip = preview.get_item_text(preview.selected)
		rig.set_weapon("bow" if clip == "shoot" else ("bow" if bow_toggle.button_pressed else "dao"))
		var duration: float = rig.player.get_animation(clip).length
		rig.sample(clip, fmod(view_elapsed, duration))
	elif clip == "apex_flip":
		# Sync visual time to the existing flip, never hold the player in the air.
		var length: float = rig.player.get_animation(clip).length
		rig.sample(clip, player.flip_elapsed / player.tuning.value("APEX_FLIP_TIME") * length)
		# Horizontal mirroring already supplies facing direction.
		rig.pivot_root.rotation *= flip_sign * player.facing
	elif player.attack_time >= 0:
		var length: float = rig.player.get_animation(clip).length
		rig.sample(clip, player.attack_time / player.tuning.value("ATTACK_DURATION") * length)
	else:
		rig.play_clip(clip)
	rig.debug_joints = debug_enabled
	rig.queue_redraw()
	previous_floor = floor_now
	previous_jump = player.jump_count
	previous_flip = player.flip_completion_count
	previous_flip_running = player.flip_running
