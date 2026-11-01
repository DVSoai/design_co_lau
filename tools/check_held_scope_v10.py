#!/usr/bin/env python3
"""Verify immutable weapon art, body placement and non-front-arm pixels."""
from pathlib import Path
import json,subprocess
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE='f485a07';failures=[]
def old(path):return subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT)
def check(ok,msg):
 print(('PASS: ' if ok else 'FAIL: ')+msg)
 if not ok:failures.append(msg)
def main():
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'art/sprites/weapons/lv1','prototype/pose_rig/art/lv1_30'],cwd=ROOT,text=True).splitlines();paths=[p for p in paths if not p.endswith('/review_lv1.png')]
 check(all(old(p)==(ROOT/p).read_bytes() for p in paths),f'ALL{len(paths)} existing weapon/source actor files byte-identical: no redrawing sword/bow or original head/body/legs')
 before=json.loads(old('prototype/pose_rig/data/frames30.json'));after=json.loads((ROOT/'prototype/pose_rig/data/frames30.json').read_text());p=json.loads((ROOT/'prototype/pose_rig/data/parts.json').read_text());oldp=json.loads(old('prototype/pose_rig/data/parts.json'))
 check(all(p[k]==v for k,v in oldp.items() if k!='assets'),'parts metadata, levels, presentation and weapon grip anchors unchanged')
 check(all(p['assets'][k]==v for k,v in oldp['assets'].items()),'all original asset records untouched')
 for i,(a,b) in enumerate(zip(before['frames'],after['frames'])):
  a=json.loads(json.dumps(a));b=json.loads(json.dumps(b))
  if i in [1,2,3,4,5,6,7,12,21]:
   for school in ['kiem','cung']:a['registrations'][school].pop('weapon');b['registrations'][school].pop('weapon')
   for key in ['asset','cung_asset']:a['layers']['body'].pop(key,None);b['layers']['body'].pop(key,None)
  check(a==b,f'frame{i}: every field outside authorized body selection and weapon placement unchanged')
 for id,a in p['assets'].items():
  if not id.startswith('held_ref_'):continue
  base=p['assets'][a['source']['own_base']];source=np.array(Image.open(ROOT/'prototype/pose_rig/art/lv1_30'/base['file']));current=np.array(Image.open(ROOT/'prototype/pose_rig/art/lv1_30'/a['file']));roi=np.array(Image.open(ROOT/a['source']['roi']))>0
  check(np.array_equal(source[~roi],current[~roi]),id+' all pixels outside front-arm change ROI unchanged')
  for key in ['neck','hip','free_hand','far_hand']:check(a['anchors'][key]==base['anchors'][key],id+' '+key+' unchanged authoring registration')
 for name in ['skills','effects']:check(old('prototype/pose_rig/data/'+name+'.json')==(ROOT/'prototype/pose_rig/data'/f'{name}.json').read_bytes(),name+' bytes unchanged')
 print('Held reference scope failures='+str(len(failures)));return bool(failures)
if __name__=='__main__':raise SystemExit(main())
