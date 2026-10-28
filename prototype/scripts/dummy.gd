extends StaticBody2D

const T = preload("res://config/tuning.gd")
var hit_count := 0
var debug_enabled := false

func _ready() -> void:
	collision_layer = 4
	collision_mask = 0
	var shape := CollisionShape2D.new()
	var rectangle := RectangleShape2D.new()
	rectangle.size = T.DUMMY_BOX
	shape.shape = rectangle
	shape.position.y = -T.DUMMY_BOX.y / 2
	add_child(shape)

func take_hit(damage: int) -> void:
	hit_count += 1
	var label := Label.new()
	label.text = str(damage)
	label.position = Vector2(-12, -T.DUMMY_BOX.y - 22)
	add_child(label)
	var tween := create_tween().set_parallel(true)
	tween.tween_property(label, "position:y", label.position.y - T.DAMAGE_FLOAT_DISTANCE, T.DAMAGE_FLOAT_TIME)
	tween.tween_property(label, "modulate:a", 0.0, T.DAMAGE_FLOAT_TIME)
	tween.chain().tween_callback(label.queue_free)
	queue_redraw()

func _draw() -> void:
	draw_rect(Rect2(Vector2(-T.DUMMY_BOX.x / 2, -T.DUMMY_BOX.y), T.DUMMY_BOX), Color(0.65, 0.43, 0.24))
	draw_line(Vector2(-30, T.SLASH_OFFSET.y), Vector2(30, T.SLASH_OFFSET.y), Color(0.8, 0.65, 0.4), 8)
	if debug_enabled:
		draw_rect(Rect2(Vector2(-T.DUMMY_BOX.x / 2, -T.DUMMY_BOX.y), T.DUMMY_BOX), Color.YELLOW, false, 2)
