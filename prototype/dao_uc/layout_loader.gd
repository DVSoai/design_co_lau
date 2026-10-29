extends RefCounted
## No hard-coded terrain: parse the build-time byte-identical Markdown copies.
const FILES := {"field":"lay_dao_uc_v1.md", "boss":"lay_dao_uc_boss_v1.md"}
const TILE := 32

static func load_map(key: String) -> Dictionary:
	var path: String = "res://dao_uc/layouts/" + FILES[key]
	var bytes := FileAccess.get_file_as_bytes(path)
	var text := bytes.get_string_from_utf8()
	var expression := RegEx.new()
	expression.compile("(?m)^```layout[ \\t]*\\r?\\n([\\s\\S]*?)^```")
	var found := expression.search(text)
	assert(found != null, "Missing canonical layout block: " + path)
	var rows := PackedStringArray()
	for line in found.get_string(1).strip_edges().split("\n"):
		rows.append(line.trim_suffix("\r"))
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
		"size":Vector2(rows[0].length()*TILE,rows.size()*TILE)}

static func feet(cell: Vector2i) -> Vector2:
	return Vector2((cell.x+0.5)*TILE,(cell.y+1)*TILE)
