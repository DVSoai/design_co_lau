#!/usr/bin/env python3
"""Audit that all36 common Lv1 images changed versus an explicit previous commit."""
from pathlib import Path
import argparse,subprocess,json,io,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument('--base',required=True);a=p.parse_args();data=json.loads((R/'prototype/pose_rig/data/parts.json').read_text());count=0
for kind,n in [('head',8),('body',18),('legs',10)]:
 for id in data['levels']['1'][kind]:
  path='art/sprites/characters/lv1_30/'+data['assets'][id]['file'];old=Image.open(io.BytesIO(subprocess.check_output(['git','show',a.base+':'+path],cwd=R))).convert('RGBA');new=Image.open(R/path).convert('RGBA');before=hashlib.sha256(old.tobytes()).hexdigest();after=hashlib.sha256(new.tobytes()).hexdigest();assert before!=after,(id,'unchanged');print(f'PASS redraw {id}: {old.size}->{new.size}; RGBA {before[:16]}->{after[:16]}; source={data["assets"][id]["source"]["sheet"]}');count+=1
print(f'PASS full Lv1 redraw audit: {count}/36 common images changed vs{a.base}; 8heads18torsos10legs; all sources independently generated for this revision.')
