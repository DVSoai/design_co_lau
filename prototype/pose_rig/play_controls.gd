extends "res://scripts/touch_controls.gd"
var player: CharacterBody2D
func layout() -> void:
	super.layout()
	# Only two skills in this scene: use full A0 button width for the two-line names.
	var rect:=get_viewport().get_visible_rect()
	var side: float=T.TOUCH_BUTTON_SIZE.x
	var width: float=2*side+T.SKILL_GAP
	for i in 2:
		_place("skill_%d" % (i+1),Vector2(rect.get_center().x-width/2+i*(side+T.SKILL_GAP),rect.end.y-T.TOUCH_MARGIN-side),Vector2.ONE*side)
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
