#!/usr/bin/env python3
"""Measure actual alpha geometry, not canvas dimensions or declared lengths."""
from pathlib import Path
import json,math,sys
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, binary_erosion
R=Path(__file__).resolve().parents[1];D=json.loads((R/'prototype/pose_rig/data/parts.json').read_text());A=D['assets'];P=R/'prototype/pose_rig/art/lv1_30';H=192.;failures=0

def check(ok,msg):
 global failures
 print(('PASS: ' if ok else 'FAIL: ')+msg);failures+=not ok

def points(id):
 a=np.array(Image.open(P/A[id]['file']).convert('RGBA'));y,x=np.where(a[:,:,3]>127);return a,np.column_stack([x,y])
a,ps=points('sword');u=np.array(A['sword']['anchors']['tip'])-A['sword']['anchors']['grip'];u/=np.linalg.norm(u);span=np.ptp(ps@u);check(.75<=span/H<=.8,f'held sword actual axial length={span/2:.4f} logic px ratio={span/H:.6f}H')
for id in ['bow_idle','bow_release','bow_draw_15','bow_draw_16']:
 a,ps=points(id);span=np.ptp(ps[:,1])+1;check(.35<=span/H<=.4,f'{id} actual height={span/2:.4f} ratio={span/H:.6f}H')
for id in ['arrow','skill_arrow']:
 a,ps=points(id);span=np.ptp(ps[:,0])+1;check(.55<=span/H<=.65,f'{id} actual length={span/2:.4f} ratio={span/H:.6f}H')
for prefix in ['swing','swing_skill']:
 for i in range(5):
  id=f'{prefix}_{i}';a,ps=points(id);w,h=np.ptp(ps,axis=0)+1
  check(w/H<=1.6 and h/H<=1.1,f'{id} opaque width/H={w/H:.6f} height/H={h/H:.6f}')
  mask=np.array(Image.open(P/A[A[id]['trail_mask']]['file']).convert('RGBA'))[:,:,3]>127
  blade=np.array(Image.open(P/A[A[id]['blade_asset']]['file']).convert('RGBA'))
  expected=Image.fromarray(np.array(Image.open(P/A[A[id]['trail_mask']]['file']).convert('RGBA')))
  if prefix=='swing_skill':
   ar=np.array(expected);ar[:,:,:3]=[90,205,255];ar[ar[:,:,3]==0,:3]=0;expected=Image.fromarray(ar)
  expected.alpha_composite(Image.fromarray(blade));check(np.array_equal(np.array(expected),a),id+' actual runtime texture equals blade+unique mask composite')
  if i:
   visible=mask & (blade[:,:,3]<128);edge=visible & ~binary_erosion(visible);y,x=np.where(edge);tip=np.array(A[id]['anchors']['tip']);gap=np.linalg.norm(np.column_stack([x,y])-tip,axis=1).min()/2
   check(gap<=2,f'{id} tip-to-actual-trail-edge={gap:.6f} logic px (limit2)')
  else:check(not mask.any(),id+' preparation: no detached trail')
check(len({(P/A[f'swing_mask_{i}']['file']).read_bytes() for i in range(1,5)})==4,'four independently shaped swept masks, not translated copies')
print(f'Lv1 ratio/continuous swing failures={failures}')
sys.exit(bool(failures))
