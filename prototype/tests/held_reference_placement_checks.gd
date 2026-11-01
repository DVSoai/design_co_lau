extends SceneTree
var failures:=0
const HELD=[0,1,2,3,4,5,6,7,12,21]
func _initialize() -> void:call_deferred("run")
func check(ok: bool,message: String) -> void:
	print(("PASS: " if ok else "FAIL: ")+message)
	if not ok:failures+=1
func run() -> void:
	var a=load("res://pose_rig/rig_frames.tscn").instantiate();root.add_child(a);a.autoplay=false;a.set_process(false)
	var source: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(ProjectSettings.globalize_path("res://").path_join("../docs/ref/so_lieu_tham_khao.json")))
	var factor: float=a.parts.presentation.display_factor
	for school in ["kiem","cung"]:
		a.set_school(school)
		for direction in [-1,1]:
			a.set_facing(direction);a.sample_frame(0)
			var original: Vector2=a.sprites.weapon.position
			var texture: RID=a.sprites.weapon.texture.get_rid()
			var r0: Array=source.bang_30_khung[0].vu_khi
			for frame: int in HELD:
				a.sample_frame(frame);var r: Array=source.bang_30_khung[frame].vu_khi
				var delta:=Vector2(r[1]-r0[1],-(r[2]-r0[2]))*(128.0/131.0*4.0)
				var actual: Vector2=(a.sprites.weapon.position-original)*factor
				check(actual.distance_to(delta)<=.0001,"%s dir%d frame%d exact frame0+reference delta actual=%s expected=%s" % [school,direction,frame,actual,delta])
				check(a.sprites.weapon.texture.get_rid()==texture and a.sprites.weapon.rotation==0,"one unchanged held texture, rotation0")
				var mirror: Vector2=actual*Vector2(direction,1)
				if frame in range(2,7):check(-mirror.x*direction>=10 and -mirror.y>=6,"run2–6 retreat>=10px rise>=6px, mirrored facing")
	print("Held reference-placement contracts failures=%d; visual grip tests measure actual rendered pixels separately" % failures);a.free();quit(1 if failures else 0)
