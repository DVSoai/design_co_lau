#!/usr/bin/env python3
"""Current compact-sweep and weapon ratios, measured from real RGBA pixels."""
from pathlib import Path
import json,sys,hashlib
import numpy as np
from PIL import Image
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parents[1];D=R/'prototype/pose_rig/data';P=json.loads((D/'parts.json').read_text());A=P['assets'];F=json.loads((D/'frames30.json').read_text())['frames'];S=json.loads((D/'skills.json').read_text())['skills'];E=json.loads((D/'effects.json').read_text())['effects'];ART=R/'prototype/pose_rig/art/lv1_30';H=float(P['presentation']['standing_height_source']);failures=0

def check(ok,msg):
 global failures
 print(('PASS: ' if ok else 'FAIL: ')+msg);failures+=not ok

def rgba(id):return np.array(Image.open(ART/A[id]['file']).convert('RGBA'))
def points(id,threshold=32):
 y,x=np.where(rgba(id)[:,:,3]>threshold);return np.column_stack([x,y]).astype(float)
def anchor(id,key):return np.array(A[id]['anchors'][key],float)
def pose(frame):
 f=F[frame];layers=f['layers'];leg=P['levels']['1']['legs'][layers['legs']['image']]
 if layers['legs'].get('stance'):leg=P['levels']['1']['combat_stance']
 if layers['legs'].get('lunge'):leg=P['levels']['1']['combat_lunge']
 body=P['levels']['1']['body'][layers['body']['image']];lp=np.array([layers['legs']['dx'],layers['legs']['dy']])*2-anchor(leg,'sole');hip=lp+anchor(leg,'hip');bp=hip+np.array([layers['body']['dx'],layers['body']['dy']])*2-anchor(body,'hip')
 return body,bp,bp+anchor(body,'grip')
# Anatomical decision: actual bare-head height, no hat/chop approximation.
head=points('head_without_hat_0',0);head_h=np.ptp(head[:,1])+1
check(abs(head_h/H-.40)<=.03,f'frame00 bare head/hair={head_h:.3f} source pixels H={H:.6f} ratio={head_h/H:.6f}, target.40 +/- .03')
check(all(A[f'head_{i}']['source'].get('hat') is False for i in range(8)),'all8 active heads have no hat')
check(np.array_equal(rgba('head_0'),rgba('head_without_hat_0')),'frame00 head RGBA exactly equals bare-head asset; no hat hidden in measurement')
# Full held sword and actual held bow remain independent of the short attack fragment.
for id in [P['levels']['1']['weapons']['kiem']]:
 ps=points(id,0);span=max(np.ptp(ps[:,0])+1,np.ptp(ps[:,1])+1)
 check(.75<=span/H<=.8,f'{id} longest alpha side/H={span/H:.6f} (same metric as ref_render, not axial length)')
for id in ['bow_idle','bow_release','bow_draw_15','bow_draw_16',P['levels']['1']['weapons']['cung']]:
 ps=points(id,127)
 if id==P['levels']['1']['weapons']['cung']:
  axis=anchor(id,'top')-anchor(id,'bottom');axis/=np.linalg.norm(axis);height=np.ptp(ps@axis)+1
 else:height=np.ptp(ps[:,1])+1
 check((1.0<=height/H<=1.1) if id==P['levels']['1']['weapons']['cung'] else (.9<=height/H<=1.0),f'{id} actual opaque axial span={height:.3f}, ratio={height/H:.6f}H (held1.0–1.1; shooting.9–1.0)')
for id in ['arrow','skill_arrow']:
 ps=points(id,127);length=np.ptp(ps[:,0])+1;check(.55<=length/H<=.65,f'{id} actual length/H={length/H:.6f}')
hashes={id:hashlib.sha256(rgba(id).tobytes()).hexdigest() for id in ['body_9','body_10','body_11','body_12']}
for id,h in hashes.items():print('BODY RGBA SHA256',id,h)
check(len(set(hashes.values()))==4,'four genuinely different torso RGBA hashes')
fragment=rgba('attack_blade');short=np.linalg.norm(anchor('attack_blade','tip')-anchor('attack_blade','blade_root'))
check(.75<=short/H<=.8,f'full attack blade length/H={short/H:.6f}, target .75..8')
for prefix in ['swing','swing_skill']:
 for i in range(5):
  id=f'{prefix}_{i}';mask_id=A[id]['trail_mask'];expected=Image.fromarray(rgba(mask_id));expected.alpha_composite(Image.fromarray(fragment))
  clean=np.array(expected);rr,gg,bb=clean[:,:,:3].astype(int).transpose(2,0,1);clean[(gg>1.18*np.maximum(rr,bb))&(gg>90)]=0
  check(np.array_equal(clean,rgba(id)),id+' real single-texture full blade + tip-connected painted trail, final key cleanup')
for skill in ['slash','tram_kiem']:
 beats=S[skill]['ground'];check(len(beats)==6 and abs(sum(b['duration'] for b in beats)-.30)<1e-9 and S[skill]['hit_window']==[.1,.2],skill+' six reference beats total.30s hit.10-.20')
 for i,beat in enumerate(beats):
  body,bp,grip=pose(beat['frame']);all_vfx=[]
  for spec in beat['effects']:
   id=E[spec['id']]['frames'][0]['asset'];paint=A[id].get('trail_mask',id);ps=points(paint)
   if len(ps):all_vfx.append(ps-anchor(id,'grip')+grip+np.array([spec['dx'],spec['dy']])*2)
  if not all_vfx:continue
  vfx=np.concatenate(all_vfx);span=np.ptp(vfx[:,0])+1
  check(span/H<=1.6,f'{skill} beat{i+1} combined visible VFX length/H={span/H:.6f} including forward/reverse layers')
  if i in [2,3,4]:
   primary=A[E[beat['effects'][0]['id']]['frames'][0]['asset']]['trail_mask']
   gap=cKDTree(points(primary)).query(anchor('attack_blade','tip'))[0]/2
   check(gap<=1,f'{skill} beat{i+1} actual trail-to-blade-tip gap={gap:.6f} logic px')
blade_pixels=points('attack_blade_only',127)
blade_span=np.ptp(blade_pixels[:,0])+1
check(.75<=blade_span/H<=.8,f'actual opaque blade (excluding handle) span/H={blade_span/H:.6f}')
print(f'Lv1 compact/proportion/weapon checks failures={failures}')
sys.exit(bool(failures))
