"""Measure actual Godot scene weapon axes, including hidden dao in shoot frames."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def angle(a,b):
 return math.degrees(math.acos(float(np.clip(a@b/(np.linalg.norm(a)*np.linalg.norm(b)),-1,1))))
def main():
 data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());definition=json.loads((ROOT/'prototype/rig/data/parts.json').read_text());parts={p['id']:p for p in definition['parts']};errors=[];rows=[]
 tex=np.array(Image.open(ROOT/'prototype/rig/art_parts/dao.png').convert('RGBA'));ys,xs=np.where(tex[:,:,3]>0)
 # Actual topmost blade pixels x=6,7 at y=0; their centre is (7,.5).
 if ys.min()!=0 or set(xs[ys==0])!={6,7}:errors.append('tip landmark no longer matches actual PNG')
 pivot=parts['dao']['pivot'];grip=tex[round(pivot[1]),round(pivot[0])]
 if grip[3]!=255:errors.append('grip outside solid hilt')
 for name,clip in data.items():
  if name=='standing_neutral':continue
  for index,frame in enumerate(clip['frames']):
   p={k:np.array(v,float) for k,v in frame['weapon_axes'].items()};fore=p['near_wrist']-p['near_elbow'];blade=p['dao_tip']-p['dao_grip'];deg=angle(blade,fore)
   t=float((p['dao_tip']-p['near_elbow'])@fore/(fore@fore));between=0<=t<=1
   rest=name in ['idle','turn'];forward=blade[0]*(-1 if name.endswith('_left') else 1)
   ok=(not between) and (deg<=30.001 if not rest else blade[1]>0 and forward>0)
   if not ok:errors.append(f'{name}/{index+1} dao axis')
   row={'clip':name,'frame':index+1,'dao_angle_deg':round(deg,4),'tip_projection_elbow_to_wrist':round(t,4),'tip_between_elbow_wrist':between,'rest_down_forward':bool(rest and blade[1]>0 and forward>0),'ok':bool(ok)};rows.append(row)
   print(f'{"PASS" if ok else "FAIL"}: {name} frame={index+1}: dao vs forearm={deg:.3f}deg; tip projection={t:.3f}; between={between}; rest={rest}')
   if name in ['shoot','shoot_left']:
    bow=p['bow_bottom']-p['bow_top'];far=p['far_wrist']-p['far_elbow'];bow_angle=angle(bow,far);distance=float(np.linalg.norm(p['bow_grip']-p['far_grip']))
    good=abs(bow_angle-90)<=1.0 and distance<.001
    row.update(bow_angle_deg=round(bow_angle,4),bow_grip_error_px=round(distance,6))
    print(f'{"PASS" if good else "FAIL"}: {name} frame={index+1}: bow vs forearm={bow_angle:.3f}deg; grip error={distance:.6f}px')
    if not good:errors.append(f'{name}/{index+1} bow axis')
 (ROOT/'prototype/rig/reports/weapon_axes_checks.json').write_text(json.dumps({'method':'Godot evaluated node/Sprite2D transforms; actual PNG tip centre (7,.5), existing hilt pivot; projection t in [0,1] is between elbow/wrist','frames':len(rows),'failures':len(errors),'details':rows},indent=2)+'\n')
 print('Weapon axis failures:',len(errors),errors);raise SystemExit(bool(errors))
if __name__=='__main__':main()
