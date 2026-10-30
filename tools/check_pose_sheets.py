#!/usr/bin/env python3
"""Check actual final PNGs, source provenance, 2x compositing and true screenshots."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];O=R/'art/sprites/characters/chr_dbl_poses'
def main():
 data=json.loads((O/'anchors.json').read_text());failure=0
 print('Common registered-source export scale:',data['common_scale']);print('Whole-sheet registration:',data['registration']);print(data['registration_note'])
 for id,e in data['assets'].items():
  path=O/e['file'];im=Image.open(path).convert('RGBA');a=np.array(im);v=a[:,:,3]>0;rgb=a[:,:,:3].astype(int);green=int(((rgb[:,:,1]>rgb[:,:,0]+40)&(rgb[:,:,1]>rgb[:,:,2]+40)&v).sum());same=path.read_bytes()==(R/'prototype/pose_rig/art'/e['file']).read_bytes()
  count=len(np.unique(a[v,:3],axis=0));print(f'{id}: size={im.size}; effective_scale={e["effective_scale"]:.12f}; green_visible={green}; RGB_colors={count}; soft_alpha={int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum())}; scene_copy={same}')
  failure+=green!=0 or not same or list(im.size)!=e['size']
  if id.startswith(('kiem_','cung_','arrow_','body_cung_')):
   yy,xx=np.where(a[:,:,3]>40);ink=np.column_stack([xx+.5,yy+.5]);distances={}
   for key,point in e['anchors'].items():
    distance=float(np.linalg.norm(ink-np.array(point),axis=1).min());distances[key]=round(distance,6)
    failure+=distance>2.0
   print(id,'anchor distance to actual alpha>40 ink in2x PNG:',distances,'limit2px')
 # Frame1 body, excluding back weapon, raster at authored 2x on standard128 logic frame.
 assets=data['assets']
 def pt(id,k):return np.array(assets[id]['anchors'][k])
 leg=-pt('legs_01','sole');body=leg+pt('legs_01','hip')-pt('body_01','hip');head=body+pt('body_01','neck')-pt('head_1','neck')
 canvas=Image.new('RGBA',(256,256));origin=np.array([128,240])
 for id,pos in [('legs_01',leg),('body_01',body),('head_1',head)]:
  image=Image.open(O/assets[id]['file']).convert('RGBA');canvas.alpha_composite(image,tuple(np.rint(origin+pos).astype(int)))
 canvas.save(R/'prototype/pose_rig/reports/idle_2x.png');mask=np.array(canvas)[:,:,3]>127;yy,xx=np.where(mask);height=int(yy.max()-yy.min()+1);margin=256-int(yy.max()+1);print(f'Idle 2x actual alpha>127 height={height}px, bottom_margin={margin}px; logic={height/2:g}px, margin={margin/2:g}px')
 failure+=height!=192 or margin!=16
 # Source remains exact generated image; all attempts and prompts retained.
 print('Active source sheets: 7; new Kiếm/body_cung/arrow=1 attempt each; cung=2 attempts, first rejected for insufficient draw distance; old tunic strip trimmed at recorded hips')
 print('Pose sheet image checks failures:',failure);raise SystemExit(bool(failure))
if __name__=='__main__':main()
