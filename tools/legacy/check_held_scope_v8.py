#!/usr/bin/env python3
"""Pixel scope and provenance checks for the authorized front-arm-only change."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];D=R/'prototype/pose_rig/data';P=json.loads((D/'parts.json').read_text());F=json.loads((D/'frames30.json').read_text());fails=[]
def check(ok,msg):
 print(('PASS: ' if ok else 'FAIL: ')+msg)
 if not ok:fails.append(msg)
for base in ['chest_stand']+[f'chest_run_{i}' for i in range(6)]+['chest_fall']:
 id=base+'_raised_v8';a=P['assets'][id];src=a['source'];old=np.array(Image.open(R/'prototype/pose_rig/art/lv1_30'/P['assets'][base]['file']).convert('RGBA'));new=np.array(Image.open(R/'prototype/pose_rig/art/lv1_30'/a['file']).convert('RGBA'));roi=np.array(Image.open(R/src['roi']))>0
 check(np.array_equal(old[~roi],new[~roi]),id+' EVERY pixel outside authorized front-arm ROI unchanged (incl torso and free arm)')
 check(np.any(old[roi]!=new[roi]),id+' actual arm paint changed inside ROI')
for school in ['kiem','cung']:
 for frame in [0,1,2,3,4,5,6,7,12,21]:
  row=F['frames'][frame];check(row['layers']['body']['asset'].endswith('_raised_v8'),f'{school} held frame{frame} uses authorized raised arm')
for school in ['kiem','cung']:
 path=R/P['weapon_masters'][school]['master'];svg=path.with_suffix('.svg');check(svg.exists(),school+' editable original SVG master preserved')
 im=Image.open(path);check(max(im.size)>=512,school+' master long side>=512')
for id in ['attack_blade','attack_blade_only']+[f'{prefix}_{i}' for prefix in ['swing','swing_skill'] for i in range(5)]:
 path='prototype/pose_rig/art/lv1_30/'+P['assets'][id]['file'];old=subprocess.check_output(['git','show','89256e7:'+path],cwd=R)
 check(old==(R/path).read_bytes(),id+' complete action PNG byte-for-byte unchanged from incoming branch')
print('Authorized image scope failures='+str(len(fails)));raise SystemExit(bool(fails))
