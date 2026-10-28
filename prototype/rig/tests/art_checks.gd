extends SceneTree
func _initialize() -> void:
	call_deferred("run")
func run() -> void:
	var rig = load("res://rig/rig.tscn").instantiate()
	root.add_child(rig)
	var ok: bool = rig.sprites.size() == 16
	for part in rig.definition.parts:
		var sprite: Sprite2D = rig.sprites[part.id]
		ok = ok and sprite.texture_filter == CanvasItem.TEXTURE_FILTER_NEAREST
		ok = ok and not sprite.centered and sprite.position == -Vector2(part.pivot[0],part.pivot[1])
		ok = ok and sprite.texture.get_size() == Vector2(part.size[0],part.size[1])
	rig.set_art_enabled(false)
	for id in rig.sprites:
		ok = ok and not rig.sprites[id].visible and rig.shapes[id].self_modulate.a == 1.0
	rig.set_art_enabled(true)
	for id in rig.sprites:
		ok = ok and rig.sprites[id].visible and rig.shapes[id].self_modulate.a == 0.0
	print(("PASS" if ok else "FAIL") + ": 16 Sprite2D; exact dimensions/pivots; nearest; art/greybox toggle")
	rig.free()
	quit(0 if ok else 1)
