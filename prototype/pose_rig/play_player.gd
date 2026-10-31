extends "res://scripts/player.gd"
## The original A0 controller remains the authority for movement and hit geometry.
var actor: Node2D
var school := "kiem"
var selected_skill := ""
var projectiles: Array[Sprite2D] = []
var attacks_started := 0
var projectile_hits := 0

func _ready() -> void:
	super._ready()
	sprite.visible=false
	slash_effect.visible=false
	actor=load("res://pose_rig/rig_frames.tscn").instantiate()
	add_child(actor)
	actor.set_process(false)
	actor.autoplay=true

func switch_school() -> void:
	school="cung" if school=="kiem" else "kiem"
	actor.set_school(school)
	attack_time=-1
	selected_skill=""
	for arrow in projectiles:arrow.queue_free()
	projectiles.clear()

func request_skill(id: String) -> void:
	if (id=="tram_kiem" and school!="kiem") or (id=="xa_tien" and school!="cung"):return
	if attack_time>=0 or cooldown_elapsed<tuning.value("ATTACK_COOLDOWN"):return
	selected_skill=id
	Input.action_press("pose_skill")

func _physics_process(delta: float) -> void:
	if Input.is_action_just_pressed("pose_switch"):switch_school()
	if Input.is_action_just_pressed("pose_tram"):request_skill("tram_kiem")
	if Input.is_action_just_pressed("pose_xa"):request_skill("xa_tien")
	var before:=attack_time
	if Input.is_action_pressed("pose_skill") and attack_time<0:
		attack_time=0
		hits.clear()
	Input.action_release("pose_skill")
	var start_skill:=before<0 and attack_time==0
	super._physics_process(delta)
	actor.set_facing(int(facing))
	actor.airborne=not is_on_floor()
	if (before<0 and attack_time>=0) or start_skill:
		attacks_started+=1
		actor.play(selected_skill if selected_skill!="" else ("slash" if school=="kiem" else "shoot"))
		selected_skill=""
	# The visual beats use the reference; collision/cooldown retain A0 values.
	if actor.action not in actor.skills_data:
		var clip: String="idle" if is_on_floor() else ("jump" if velocity.y<0 else "fall")
		if is_on_floor() and absf(velocity.x)>1:clip="run"
		if flip_running:clip="apex_flip"
		if clip!=actor.action:actor.play(clip)
	actor._process(delta)
	for arrow: Sprite2D in actor.arrows.duplicate():
		actor.arrows.erase(arrow)
		arrow.set_meta("tail",actor.anchor("skill_arrow" if actor.action=="xa_tien" else "arrow","tail")*2)
		arrow.reparent(get_parent(),true)
		arrow.set_meta("direction",facing)
		arrow.set_meta("life",0.0)
		projectiles.append(arrow)
	for arrow in projectiles.duplicate():
		var start: Vector2=arrow.to_global(arrow.get_meta("tail"))
		var finish: Vector2=start+Vector2(240*float(arrow.get_meta("direction"))*delta,0)
		var query:=PhysicsRayQueryParameters2D.create(start,finish,4)
		var hit:=get_world_2d().direct_space_state.intersect_ray(query)
		var life: float=float(arrow.get_meta("life"))+delta
		arrow.set_meta("life",life)
		if not hit.is_empty() and hit.collider.has_method("take_hit"):
			hit.collider.take_hit(T.DAMAGE)
			projectile_hits+=1
			projectiles.erase(arrow)
			arrow.queue_free()
		elif life>4:
			projectiles.erase(arrow)
			arrow.queue_free()
		else:arrow.global_position+=finish-start

func is_hit_active() -> bool:
	return school=="kiem" and super.is_hit_active()

func _exit_tree() -> void:
	for arrow in projectiles:
		if is_instance_valid(arrow):arrow.queue_free()
