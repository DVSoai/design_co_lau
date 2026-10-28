"""Author new art pose data from old timing/poses and newly measured bones; no A0 physics edits."""
from pathlib import Path
import json,math,copy
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def rotate(v,a):
 t=math.radians(a);return np.array([v[0]*math.cos(t)-v[1]*math.sin(t),v[0]*math.sin(t)+v[1]*math.cos(t)])
def leg_solve(frame,p,side,target):
 b=frame['angles']['body'];hip=np.array(frame['body_position'])+rotate(p['thigh_'+side]['attach'],b)
 v1=np.array(p['shin_'+side]['attach']);v2=np.array(p['foot_'+side]['attach']);l1=np.linalg.norm(v1);l2=np.linalg.norm(v2)
 foot=p['foot_'+side];ankle=np.array([target[0],target[1]-(foot['size'][1]-foot['pivot'][1])]);dx,dy=ankle-hip;dist=math.hypot(dx,dy)
 if dist>l1+l2+.001:raise ValueError(('unreachable',side,dist,l1+l2))
 k=-math.acos(max(-1,min(1,(dist*dist-l1*l1-l2*l2)/(2*l1*l2))));q=math.atan2(-dx,dy)-math.atan2(l2*math.sin(k),l1+l2*math.cos(k));a1=math.atan2(-v1[0],v1[1]);a2=math.atan2(-v2[0],v2[1])
 frame['angles']['thigh_'+side]=math.degrees(q-a1)-b;frame['angles']['shin_'+side]=math.degrees(k+a1-a2);frame['angles']['foot_'+side]=-math.degrees(q+k-a2)
def old_foot(f,side):
 a=f['angles'];b=a['body'];hip=np.array(f['body_position'])+rotate([-2 if side=='far' else 2,0],b);t=b+a['thigh_'+side];s=t+a['shin_'+side];v=hip+rotate([0,22],t)+rotate([0,22],s);return [float(v[0]),float(v[1]+4)]
def main():
 data=json.loads((ROOT/'prototype/rig/data/animations_greybox.json').read_text());d=json.loads((ROOT/'prototype/rig/data/parts.json').read_text());p={x['id']:x for x in d['parts']};base=-p['body']['attach'][1]
 for name,c in data['clips'].items():
  for f in c['frames']:
   old=copy.deepcopy(f);f['body_position'][1]+=48-base;f['root_position'][1]+=48-base
   if name in ['idle','land','run','slash_1','slash_2','slash_3'] or (name=='jump_up' and f is c['frames'][0]):
    for side in ['near','far']:leg_solve(f,p,side,old_foot(old,side))
  if name=='shoot':
   arm=np.array(p['forearm_far']['attach']);fore=np.array(p['hand_far']['attach']);a1=math.atan2(-arm[0],arm[1]);a2=math.atan2(-fore[0],fore[1])
   near1=np.array(p['forearm_near']['attach']);near2=np.array(p['hand_near']['attach']);l1=np.linalg.norm(near1);l2=np.linalg.norm(near2);n1=math.atan2(-near1[0],near1[1]);n2=math.atan2(-near2[0],near2[1])
   for i,f in enumerate(c['frames']):
    f['angles'].update(upper_arm_far=-90-math.degrees(a1),forearm_far=math.degrees(a1-a2),hand_far=math.degrees(a2),bow=90)
    dx=[.94,.65,.23,.94,.8][i]*(l1+l2);dy=[0,-5,-10,0,1][i];k=-math.acos(max(-1,min(1,(dx*dx+dy*dy-l1*l1-l2*l2)/(2*l1*l2))));q=math.atan2(-dx,dy)-math.atan2(l2*math.sin(k),l1+l2*math.cos(k))
    f['angles'].update(upper_arm_near=math.degrees(q-n1),forearm_near=math.degrees(k+n1-n2),hand_near=max(-90,min(90,-90-math.degrees(q+k-n2))))
 data['status']='Đề xuất — retarget geometry only; original frame counts/timings retained'
 (ROOT/'prototype/rig/data/animations.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Retargeted art poses: 13 clips/48 frames; unchanged duration/events; foot targets retained; geometry from common-scale parts')
if __name__=='__main__':main()
