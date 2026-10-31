extends "res://scripts/touch_controls.gd"
var player: CharacterBody2D
func _ready() -> void:
	super._ready()
	buttons.skill_1.caption="Trảm\nKiếm"
	buttons.skill_2.caption="Xạ\nTiễn"
	buttons.target.caption="PHÁI"
	buttons.slash.caption="ĐÁNH"
	_simplify()
func _simplify() -> void:
	for key in ["health","mana","menu","skill_3","skill_4","skill_5"]:buttons[key].visible=false
func _process(delta: float) -> void:
	super._process(delta)
	_simplify()
func _activate_placeholder(key: String) -> void:
	if key=="target":player.switch_school()
	elif key=="skill_1":player.request_skill("tram_kiem")
	elif key=="skill_2":player.request_skill("xa_tien")
