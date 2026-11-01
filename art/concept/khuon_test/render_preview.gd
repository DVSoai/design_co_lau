extends Node
func _ready() -> void:
	var args=OS.get_cmdline_user_args()
	var input: String=args[0]
	var output: String=args[1]
	var source:=Image.load_from_file(input)
	var bounds:=source.get_used_rect()
	var viewport:=SubViewport.new();viewport.size=Vector2i(200,200);viewport.transparent_bg=true;viewport.render_target_update_mode=SubViewport.UPDATE_ALWAYS;add_child(viewport)
	var holder:=Node2D.new();holder.position=Vector2(100,170);viewport.add_child(holder)
	var sprite:=Sprite2D.new();sprite.centered=false;sprite.texture=ImageTexture.create_from_image(source);sprite.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR;holder.add_child(sprite)
	var scale_factor:=128.0/bounds.size.y
	sprite.scale=Vector2.ONE*scale_factor;sprite.position=-Vector2(bounds.position+Vector2i(bounds.size.x/2,bounds.size.y))*scale_factor
	for direction in [1,-1]:
		holder.scale=Vector2(direction,1)
		await RenderingServer.frame_post_draw
		await RenderingServer.frame_post_draw
		var image:=viewport.get_texture().get_image()
		var path:=output+('_right.png' if direction>0 else '_left.png')
		var error:=image.save_png(path)
		print('ACTUAL GODOT full-sprite preview source=',input,' direction=',direction,' source_bbox=',bounds,' scale=',scale_factor,' output=',path,' output_bbox=',image.get_used_rect(),' error=',error)
		if error!=OK:get_tree().quit(1);return
	get_tree().quit(0)
