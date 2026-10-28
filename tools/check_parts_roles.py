"""Check immutable Claude head, material groups, shirt budget and evaluated fingertip height."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from cut_parts import claude_head
from snap_pixel import load_groups
from render_parts_scene import sprite_layer
ROOT=Path(__file__).resolve().parents[1]
def main():
 g=load_groups(ROOT/'art/reference/palette.gpl');outline=g['outline'];errors=[];report={}
 for p in json.loads((ROOT/'prototype/rig/data/parts.json').read_text())['parts']:
  id=p['id'];a=np.array(Image.open(ROOT/f'art/sprites/characters/chr_dbl_parts/{id}.png').convert('RGBA'))
  allowed=outline+(g['pants']+g['skin'] if id.startswith('thigh_') else g['skin'] if id.startswith(('forearm_','hand_','shin_','foot_')) else g['fabric']+g['skin'] if id.startswith('upper_arm_') else g['fabric']+g['belt'])
  if id=='head':allowed=outline+[g['pants'][1]]+g['skin'];same=np.array_equal(a,claude_head());print('Head exact Claude matrix:',same);errors+=[] if same else ['head changed']
  bad=[(int(x),int(y)) for y,x in zip(*np.where(a[:,:,3]>0)) if tuple(a[y,x,:3]) not in allowed]
  report[id]={'forbidden_group_pixels':len(bad)};print(f'{id}: forbidden group pixels={len(bad)}');errors+=bad
  if id=='body' or id.startswith('upper_arm_'):
   counts={('#'+''.join(f'{v:02X}' for v in c)):int((np.all(a[:,:,:3]==c,axis=2)&(a[:,:,3]>0)).sum()) for c in g['fabric']};total=sum(counts.values());ratio=counts['#EAD8B8']/max(1,total);dominant=max(counts,key=counts.get)
   report[id]['shirt_counts']=counts;report[id]['shirt_percent']={k:round(100*v/max(1,total),3) for k,v in counts.items()};print(id,'shirt counts/percent:',counts,report[id]['shirt_percent'])
   if ratio>.15 or dominant!='#C3A98A':errors.append(f'{id} shirt budget')
 data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());tips={}
 for name in ['idle','standing_neutral']:
  for item in data[name]['frames'][0]['geometry']:
   if item['id'] not in ['hand_near','hand_far']:continue
   mask=np.array(sprite_layer(item,(160,160),(80,126)))[:,:,3]>0;ys,xs=np.where(mask);tip=int(ys.max())+1-126;tips[name+'_'+item['id']]=tip
   print(f'{name} {item["id"]}: fingertip bottom y={tip} px from feet')
   if not -34<=tip<=-30:errors.append(f'{name} fingertip {tip}')
 report['fingertips']=tips;report['failures']=len(errors);(ROOT/'prototype/rig/reports/material_checks.json').write_text(json.dumps(report,indent=2)+'\n');print('Material/Claude/arm failures:',len(errors));raise SystemExit(1 if errors else 0)
if __name__=='__main__':main()
