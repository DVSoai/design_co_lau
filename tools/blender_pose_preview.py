"""Blender 4.3+ authoring preview: four textured 2D planes, NOT a 3D character.
Run: blender --background --factory-startup --python tools/blender_pose_preview.py
"""
from pathlib import Path
import json
import bpy
R=Path(__file__).resolve().parents[1];data=json.loads((R/'art/sprites/characters/chr_dbl_poses/anchors.json').read_text())['assets']
bpy.context.preferences.filepaths.save_version=0
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def pt(id,k):return [v*.5 for v in data[id]['anchors'][k]]
def add(a,b):return [a[0]+b[0],a[1]+b[1]]
def sub(a,b):return [a[0]-b[0],a[1]-b[1]]
leg=sub([0,0],pt('legs_01','sole'));hip=add(leg,pt('legs_01','hip'));body=sub(hip,pt('body_01','hip'));neck=add(body,pt('body_01','neck'));head=sub(neck,pt('head_1','neck'));weapon=sub(add(body,pt('body_01','back')),pt('kiem_1','grip'))
for id,pos,z in [('kiem_1',weapon,-.03),('legs_01',leg,0),('body_01',body,.01),('head_1',head,.02)]:
 w,h=[v*.5 for v in data[id]['size']];x,y=pos;y=-y
 mesh=bpy.data.meshes.new(id);mesh.from_pydata([(x,y-h,z),(x+w,y-h,z),(x+w,y,z),(x,y,z)],[],[(0,1,2,3)]);mesh.update()
 ob=bpy.data.objects.new(id,mesh);bpy.context.collection.objects.link(ob)
 uv=mesh.uv_layers.new(name='UVMap')
 for loop,coord in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=coord
 mat=bpy.data.materials.new(id);mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear();tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/'art/sprites/characters/chr_dbl_poses'/data[id]['file']));tex.interpolation='Linear';em=nodes.new('ShaderNodeEmission');tr=nodes.new('ShaderNodeBsdfTransparent');mix=nodes.new('ShaderNodeMixShader');out=nodes.new('ShaderNodeOutputMaterial');links=mat.node_tree.links
 links.new(tex.outputs['Color'],em.inputs['Color']);links.new(tex.outputs['Alpha'],mix.inputs[0]);links.new(tr.outputs[0],mix.inputs[1]);links.new(em.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],out.inputs['Surface']);ob.data.materials.append(mat)
 ob['layer_rule']='whole painted pose, translation/flip only; no skeletal rotation'
bpy.ops.object.camera_add(location=(0,48,300));cam=bpy.context.object;cam.name='Orthographic_96px';cam.data.type='ORTHO';cam.data.ortho_scale=128;bpy.context.scene.camera=cam
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=8;scene.cycles.use_denoising=False;scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.view_settings.view_transform='Standard';scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.filepath=str(R/'docs/reports/g1_kiem_cung_blender_idle.png')
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(R/'art/concept/characters/chr_dbl_poses/kiem_cung_authoring_2d.blend'));bpy.ops.render.render(write_still=True)
print('BLENDER PREVIEW OK: 4 painted 2D planes, packed source images, orthographic camera; NOT a 3D model/sculpt or new hand drawing')
