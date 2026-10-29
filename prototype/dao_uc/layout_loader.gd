extends RefCounted
## Runtime JSON generated from canonical design/maps Markdown; no copied Markdown.
const FILES := {"field":"lay_dao_uc_v1.json", "boss":"lay_dao_uc_boss_v1.json"}
const TILE := 32

static func load_map(key: String) -> Dictionary:
	var path: String = "res://dao_uc/layouts/" + FILES[key]
	var document: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	assert(document.get("version",0) == 1, "Unsupported layout JSON version")
	assert(int(document.meta.tile_px) == TILE, "Unexpected layout tile size")
	var rows := PackedStringArray(document.rows)
	assert(not rows.is_empty(), "Empty JSON layout")
	var counts := {}
	var points := {}
	for y in rows.size():
		assert(rows[y].length() == rows[0].length(), "Nonrectangular grid")
		for x in rows[y].length():
			var symbol: String = rows[y].substr(x,1)
			counts[symbol] = int(counts.get(symbol,0)) + 1
			if not points.has(symbol):
				points[symbol] = []
			points[symbol].append(Vector2i(x,y))
	return {"key":key,"path":path,"rows":rows,"counts":counts,"points":points,
		"size":Vector2(rows[0].length()*TILE,rows.size()*TILE),
		"source":document.source,"meta":document.meta,"hud":document.hud}

static func feet(cell: Vector2i) -> Vector2:
	return Vector2((cell.x+0.5)*TILE,(cell.y+1)*TILE)
