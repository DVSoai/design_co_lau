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
# The latest horizontal-trail rule replaces the older whole-swing1.6H cap:
# trail alone is1.2..1.6H from the sword tip; sword is a further0.78H.
from scipy.ndimage import label
for prefix in ['swing','swing_skill']:
 for i in range(5):
  id=f'{prefix}_{i}';a,ps=points(id)
  mask_image=np.array(Image.open(P/A[A[id]['trail_mask']]['file']).convert('RGBA'))
  mask=mask_image[:,:,3]>32
  blade=np.array(Image.open(P/A[A[id]['blade_asset']]['file']).convert('RGBA'))
  expected=mask_image.copy()
  if prefix=='swing_skill':
   yy=np.indices(expected.shape[:2])[0];v=np.clip(np.abs(yy-A[id]['anchors']['tip'][1])/29,0,1)
   for c,(lo,hi) in enumerate([(245,48),(255,180),(255,255)]):expected[:,:,c]=(lo+(hi-lo)*v).astype('uint8')
   expected[expected[:,:,3]==0,:3]=0
  expected=Image.fromarray(expected);expected.alpha_composite(Image.fromarray(blade))
  check(np.array_equal(np.array(expected),a),id+' actual single-texture sword+horizontal brush composite')
  if A[id]['has_trail']:
   yy,xx=np.where(mask);w=xx.max()-xx.min()+1;h=yy.max()-yy.min()+1;_,components=label(mask)
   upper=1.6 if prefix=='swing' else 1.8
   check(1.2<=w/H<=upper and h/H<=.35 and components==1,f'{id} visible trail width/H={w/H:.6f} height/H={h/H:.6f} connected_components={components}')
   visible=mask & (blade[:,:,3]<128);edge=visible & ~binary_erosion(visible);y,x=np.where(edge);tip=np.array(A[id]['anchors']['tip']);gap=np.linalg.norm(np.column_stack([x,y])-tip,axis=1).min()/2
   check(gap<=2,f'{id} actual tip-to-visible-trail-edge={gap:.6f} logic px')
   alpha=mask_image[:,:,3];left=alpha[:,xx.min():xx.min()+int(w*.2)].max();right=alpha[:,xx.max()-int(w*.2):xx.max()].max()
   check(left>right and right>0,f'{id} leading alpha={left} fading tail alpha={right}; no abrupt missing tail')
  else:check(not mask.any(),id+' guard/recovery blade only, no detached trail')
print(f'Lv1 ratio/continuous swing failures={failures}')
sys.exit(bool(failures))
