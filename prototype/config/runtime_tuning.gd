extends RefCounted

const Defaults = preload("res://config/tuning.gd")
# key, minimum, maximum, step, đơn vị. Không ghi cấu hình ra đĩa.
const SLIDERS := [
	["RUN_SPEED", 50.0, 500.0, 1.0, "px/s"],
	["ACCELERATION", 100.0, 3000.0, 10.0, "px/s²"],
	["STOP_TIME", 0.0, 0.3, 0.01, "s"],
	["TURN_TIME", 0.0, 0.2, 0.01, "s"],
	["APEX_FLIP_TIME", 0.05, 0.3, 0.01, "s"],
	["JUMP_HEIGHT", 20.0, 200.0, 1.0, "px"],
	["TIME_TO_APEX", 0.15, 0.8, 0.01, "s"],
	["COYOTE_TIME", 0.0, 0.3, 0.01, "s"],
	["JUMP_BUFFER", 0.0, 0.3, 0.01, "s"],
	["CAMERA_DEAD_ZONE.x", 0.0, 250.0, 1.0, "px"],
	["CAMERA_LOOK_AHEAD", 0.0, 300.0, 1.0, "px"],
	# Luôn giữ duration lớn hơn cửa sổ trúng mặc định HIT_END.
	["ATTACK_DURATION", 0.22, 1.2, 0.01, "s"],
	["ATTACK_COOLDOWN", 0.0, 1.0, 0.01, "s"],
]
var values: Dictionary = {}
var mode_heights := {true: Defaults.JUMP_HEIGHT, false: Defaults.LEGACY_JUMP_HEIGHT}

func _init() -> void:
	var source: Script = Defaults
	var defaults := source.get_script_constant_map()
	values["FAKE_MOTION_ENABLED"] = Defaults.FAKE_MOTION_ENABLED
	for key in ["HOLD_AUTO_JUMP", "VARIABLE_JUMP", "DIAGONAL_SPIN_ENABLED", "HUD_VISIBLE", "CLASSIC_CONTROLS", "AIR_JUMP_ENABLED"]:
		values[key] = defaults[key]
	for row in SLIDERS:
		values[row[0]] = Defaults.CAMERA_DEAD_ZONE.x if row[0] == "CAMERA_DEAD_ZONE.x" else defaults[row[0]]

func value(key: String) -> float:
	return float(values[key])

func fake_motion_enabled() -> bool:
	return bool(values["FAKE_MOTION_ENABLED"])

func set_fake_motion_enabled(enabled: bool) -> void:
	values["FAKE_MOTION_ENABLED"] = enabled

func set_value(key: String, number: float) -> void:
	for row in SLIDERS:
		if row[0] == key:
			values[key] = clampf(snappedf(number, row[3]), row[1], row[2])
			return

func gravity() -> float:
	return 2.0 * value("JUMP_HEIGHT") / pow(value("TIME_TO_APEX"), 2)

func jump_speed() -> float:
	return -2.0 * value("JUMP_HEIGHT") / value("TIME_TO_APEX")

func current_value(key: String, fallback: Variant) -> Variant:
	if key == "FALL_SPEED_MAX":
		return Defaults.FALL_SPEED_MULTIPLIER * absf(jump_speed())
	if key == "GRAVITY":
		return gravity()
	if key == "JUMP_SPEED":
		return jump_speed()
	if key == "CAMERA_DEAD_ZONE":
		return Vector2(value("CAMERA_DEAD_ZONE.x"), Defaults.CAMERA_DEAD_ZONE.y)
	return values.get(key, fallback)

func as_text() -> String:
	var source: Script = Defaults
	var defaults := source.get_script_constant_map()
	var lines := PackedStringArray(["A0 runtime tuning (temporary; not saved)"])
	for key in defaults:
		lines.append("%s = %s" % [key, str(current_value(key, defaults[key]))])
	return "\n".join(lines)

func flag(key: String) -> bool:
	return bool(values[key])

func set_flag(key: String, enabled: bool) -> void:
	if key == "CLASSIC_CONTROLS" and enabled != flag(key):
		mode_heights[flag(key)] = value("JUMP_HEIGHT")
		values["JUMP_HEIGHT"] = mode_heights[enabled]
	values[key] = enabled
