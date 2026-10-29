#!/usr/bin/env python3
"""Reproducible v3 authoring from committed main-baseline fixtures, no imagegen.
Only body pixels and standing poses change; head metadata/RGBA are immutable.
"""
from pathlib import Path
import json,math,shutil,subprocess
import numpy as np
from PIL import Image
from snap_pixel import load_groups,nearest
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'prototype/rig/reports/v3_baseline'
BASE_COMMIT='8bd5876'

def main():
 parts=json.loads((BASE/'parts.json').read_text());clips=json.loads((BASE/'animations.json').read_text())
 p={x['id']:x for x in parts['parts']};body=p['body'];old_pivot=body['pivot'].copy()
 data=subprocess.check_output(['git','show',BASE_COMMIT+':art/sprites/characters/chr_dbl_parts/body.png'],cwd=ROOT)
 import io
 old=np.array(Image.open(io.BytesIO(data)).convert('RGBA'));groups=load_groups(ROOT/'art/reference/palette.gpl')
 clean=old.copy();outline=groups['outline'];allowed=groups['fabric']+groups['belt']
 # Remove only previous generated stroke from the editable body; repaint the
 # standing silhouette after Godot export. Head is never read for editing.
 for y,x in zip(*np.where(clean[:,:,3]>0)):
  if tuple(clean[y,x,:3]) in outline:
   candidates=[(abs(yy-y)+abs(xx-x),clean[yy,xx,:3]) for yy,xx in zip(*np.where(old[:,:,3]>0)) if tuple(old[yy,xx,:3]) in allowed]
   clean[y,x,:3]=min(candidates,key=lambda item:item[0])[1]
 new=np.zeros((29,23,4),np.uint8)
 # Row widths fitted to manually declared shoulder/chest/hip reference bands;
 # longitudinal pixels, neck/hem heights and all joint coordinates stay fixed.
 for y in range(29):
  xs=np.where(clean[y,:,3]>0)[0]
  if not len(xs):continue
  target=round(np.interp(y,[0,4,5,11,24,26],[len(xs) if y==0 else 5,13,14,17,19,19])) if y<=26 else max(1,round(len(xs)*19/16))
  centre=(int(xs[0])+int(xs[-1]))/2+4
  start=round(centre-(target-1)/2)
  samples=clean[y,xs[0]:xs[-1]+1]
  for xx in range(target):
   region=samples[math.floor(xx*len(samples)/target):max(math.floor(xx*len(samples)/target)+1,math.ceil((xx+1)*len(samples)/target))]
   valid=region[region[:,3]>0]
   if not len(valid):valid=samples[samples[:,3]>0]
   new[y,start+xx]=[*nearest(np.median(valid[:,:3],axis=0),allowed),255]
 body['size']=[23,29];body['pivot'][0]+=4
 # Logical torso/hip separation: 16 visual parts remain; hip is a helper node.
 for side in ['near','far']:
  p['thigh_'+side]['parent']='hip';p['thigh_'+side]['art_parent']='body'
 # Solve exact straight-chain standing height; local leg angles cancel the
 # measured off-axis attach vectors, not a visual knee cheat.
 v1=np.array(p['shin_near']['attach']);v2=np.array(p['foot_near']['attach'])
 a1=math.atan2(-v1[0],v1[1]);a2=math.atan2(-v2[0],v2[1])
 hip_y=-(np.linalg.norm(v1)+np.linalg.norm(v2)+p['foot_near']['size'][1]-p['foot_near']['pivot'][1])
 targets=[('idle',i,bob) for i,bob in enumerate([0,-1,-2,-1])]+[('turn',len(clips['clips']['turn']['frames'])-1,0),('land',len(clips['clips']['land']['frames'])-1,0)]
 for name,i,bob in targets:
  f=clips['clips'][name]['frames'][i];f['body_position']=[0,float(hip_y+bob)];f['hip_position']=[0,float(hip_y)];f['angles']['body']=0
  for side in ['near','far']:
   f['angles']['thigh_'+side]=-math.degrees(a1)
   f['angles']['shin_'+side]=math.degrees(a1-a2)
   f['angles']['foot_'+side]=math.degrees(a2)
 parts['version']=3;parts['neutral_clip']='idle';parts['status']='v3 — chưa duyệt, head immutable; separate hip helper for standing breath'
 out=ROOT/'art/sprites/characters/chr_dbl_parts/body.png';Image.fromarray(new).save(out);shutil.copyfile(out,ROOT/'prototype/rig/art_parts/body.png')
 raw=ROOT/'prototype/rig/art_parts/v3_body_unoutlined.png';Image.fromarray(new).save(raw)
 (ROOT/'prototype/rig/data/parts.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'prototype/rig/data/animations.json').write_text(json.dumps(clips,ensure_ascii=False,indent=2)+'\n')
 print(f'Body only: 17x29 -> 23x29; pivot {old_pivot} -> {body["pivot"]}; no head/arm/leg PNG edits; row targets shoulder14 chest17 hip19')
 print(f'Straight hip y={hip_y:.9f}; knee flexion=0; torso bob [0,-1,-2,-1]; 13 clip counts/times retained')
if __name__=='__main__':main()
