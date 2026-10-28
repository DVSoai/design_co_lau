extends Node2D

const T = preload("res://config/tuning.gd")
var player: CharacterBody2D

func _draw() -> void:
	if player.attack_time >= 0:
		var facing: float = player.facing
		draw_arc(Vector2(0, T.SLASH_OFFSET.y), T.SLASH_ARC_RADIUS,
			-1.2 if facing > 0 else 1.9, 1.2 if facing > 0 else 4.3,
			12, Color(0.95, 0.85, 0.62), 3)
