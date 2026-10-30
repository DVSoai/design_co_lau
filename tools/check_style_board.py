#!/usr/bin/env python3
"""Verify keyed PNGs/boards and genuine-source provenance; no generated results."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'art/concept/style_v2'
def main():
 errors=[];paths=sorted((S/'cut').glob('*.png'))+[R/'docs/reports/style_v2_board.png',R/'docs/reports/style_v2_160.png'];total=0
 for p in paths:
  im=Image.open(p).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(int);visible=a[:,:,3]>0
  green=int(((rgb[:,:,1]>rgb[:,:,0]+40)&(rgb[:,:,1]>rgb[:,:,2]+40)&visible).sum());total+=green
  print(f'{p.relative_to(R)}: {im.width}x{im.height}; green_visible={green}')
  if green:errors.append(str(p))
 data=json.loads((S/'measurements.json').read_text());assert data['original_count']==9 and data['replacement_count']==2
 for name,row in data['images'].items():
  p=S/(name+'.png');assert hashlib.sha256(p.read_bytes()).hexdigest()==row['source_sha256'];assert (S/(name+'.prompt.txt')).exists()
  for pose in ['idle','run','raise','slash','bow']:
   for target in [160,96]:
    d=row['display'][pose+'_'+str(target)];assert abs(d['scale']*d['source_human_height']-target)<1e-9
 print('OK: all11 original source hashes match; all prompts retained; all5pose landmark spans160/96 from uniform scaling')
 assert Image.open(R/'docs/reports/style_v2_board.png').size==(2220,3355)
 assert Image.open(R/'docs/reports/style_v2_160.png').size==(1620,260)
 assert len(data['quick_choices'])==9 and 'v1_c_r1' in data['quick_choices'] and 'v2_c_r1' in data['quick_choices']
 print(f'Checked extracted PNGs={len(paths)-2}, boards=2; total residual visible green pixels={total}; failures={len(errors)}')
 print('Landmark checks verify display scale only; they do not certify anatomy, outfit, weapon direction or vector path editing.')
 raise SystemExit(bool(errors))
if __name__=='__main__':main()
