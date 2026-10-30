#!/usr/bin/env python3
"""Fit the actual painted shaft, then measure nock/rest alignment; no anchor-only pass."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];P=json.loads((R/'prototype/pose_rig/data/parts.json').read_text())['assets'];D=R/'prototype/pose_rig/art/lv1_30';fail=0

def fit(id):
 e=P[id];a=np.array(Image.open(D/e['file']).convert('RGBA'));r,g,b=a[:,:,:3].astype(int).transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);t=np.array(e['anchors']['tail']);tip=np.array(e['anchors']['tip']);shaft=(xx>t[0]+.22*(tip[0]-t[0]))&(xx<t[0]+.74*(tip[0]-t[0]))&(a[:,:,3]>127)
 if id=='skill_arrow':color=(r>205)&(g>220)&(b>230)
 else:color=(r>45)&(r-g>10)&(g-b>5)&(b<170)
 y,x=np.where(shaft&color);assert len(x)>20,(id,len(x));m,c=np.polyfit(x,y,1);return m,c

def check(id,rest):
 global fail
 m,c=fit(id);tail=np.array(P[id]['anchors']['tail']);gap=lambda v:abs(m*v[0]-v[1]+c)/(np.sqrt(1+m*m)*2)
 a=gap(tail);b=gap(rest);ok=a<=1 and b<=1;fail+=not ok
 print(f'{"PASS" if ok else "FAIL"}: {id} actual shaft slope={m:.6f}; nock gap={a:.6f} logic px; bow-rest gap={b:.6f} logic px')
for body in [15,16]:
 id=f'arrow_draw_{body}';tail=np.array(P[id]['anchors']['tail']);bp=P[f'body_{body}']['anchors'];rest=tail+np.array(bp['far_hand'])-bp['near_hand'];check(id,rest)
for id in ['arrow','skill_arrow']:
 tail=np.array(P[id]['anchors']['tail']);bow=P['bow_release']['anchors'];rest=tail+np.array(bow['grip'])-bow['string'];check(id,rest)
print(f'Actual painted-shaft alignment failures={fail}')
sys.exit(bool(fail))
