#!/usr/bin/env python3
"""Checks real RGBA files, source hashes, frame indices and JSON contracts."""
from pathlib import Path
import json, hashlib,sys
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'prototype/pose_rig/data';P=json.loads((D/'parts.json').read_text());F=json.loads((D/'frames30.json').read_text());E=json.loads((D/'effects.json').read_text())['effects'];S=json.loads((D/'skills.json').read_text())['skills'];fail=0

def check(ok,msg):
 global fail
 print(('PASS: ' if ok else 'FAIL: ')+msg);fail+=not ok
check(set(P['levels'])=={'1'},'only Lv1 implemented; no new Lv10..60 completion claims')
for group,n in [('head',8),('body',18),('legs',10)]:
 ids=P['levels']['1'][group];check(len(ids)==n and len(set(ids))==n,f'{group} unique assets={len(set(ids))}/{n}')
for id,item in P['assets'].items():
 a=ROOT/'art/sprites/characters/lv1_30'/item['file'];b=ROOT/'prototype/pose_rig/art/lv1_30'/item['file'];im=Image.open(a).convert('RGBA');ar=np.array(im).astype(int);r,g,bl,alpha=ar.transpose(2,0,1);green=int(((g>1.18*np.maximum(r,bl))&(g>90)&(alpha>0)).sum());hasalpha=int((alpha==0).sum());check(list(im.size)==item['size'] and a.read_bytes()==b.read_bytes() and green==0 and hasalpha>0 and a.with_suffix('.prompt.txt').exists(),f'{id} {im.width}x{im.height} green={green} transparent={hasalpha} copy/prompt OK')
check(len(F['frames'])==30,'30 rows')
for f in F['frames']:
 check(set(f['layers'])=={'head','body','legs','weapon'},f'frame{f["id"]} four layers')
 for k in ['head','body','legs']:check(0<=f['layers'][k]['image']<len(P['levels']['1'][k]),f'frame{f["id"]} valid {k} index')
for id,s in S.items():
 for mode in ['ground','air']:
  for b in s[mode]:
   check(14<=b['frame']<30 and len(b['effects'])<=3 and all(x['id'] in E for x in b['effects']),f'{id}/{mode} frame{b["frame"]} valid beat')
 check(sum(x['duration'] for x in s['ground'])<.40000001,f'{id} visual duration={sum(x["duration"] for x in s["ground"]):.6f}s')
check(abs(sum(x['duration'] for x in S['slash']['ground'])-.3)<1e-9 and S['slash']['hit_window']==[.1,.2],'slash .30s, hit .10-.20')
for ref in P['references']:check(hashlib.sha256((ROOT/ref['path']).read_bytes()).hexdigest()==ref['sha256'],'reference unchanged hash '+ref['path'])
# Actual assembled RGBA bounds for the neutral Lv1 pose, in logical pixels.
positions={}
leg=P['assets']['legs_0'];positions['legs_0']=[-v*.5 for v in leg['anchors']['sole']]
hip=[positions['legs_0'][i]+leg['anchors']['hip'][i]*.5 for i in [0,1]]
body=P['assets']['body_0'];positions['body_0']=[hip[i]-body['anchors']['hip'][i]*.5 for i in [0,1]]
neck=[positions['body_0'][i]+body['anchors']['neck'][i]*.5 for i in [0,1]]
head=P['assets']['head_0'];positions['head_0']=[neck[i]-head['anchors']['neck'][i]*.5 for i in [0,1]]
ys=[]
for id,at in positions.items():
 box=Image.open(ROOT/'prototype/pose_rig/art/lv1_30'/P['assets'][id]['file']).getbbox()
 ys += [at[1]+box[1]*.5,at[1]+box[3]*.5]
height=max(ys)-min(ys)
check(abs(height-96)<.5 and abs(max(ys))<.5,'idle actual RGBA height=%.3f logic px sole=%.3f; preview1600x720 height=%.3f px' % (height,max(ys),height*P['presentation']['display_factor']))
print(f'Lv1 real-file checks failures={fail}; assets={len(P["assets"])} frames=30 skills=4')
sys.exit(bool(fail))
