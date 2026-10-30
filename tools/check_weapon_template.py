#!/usr/bin/env python3
"""Check fixed canvas/grip AND actual opaque blade axes from final PNG pixels."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];P=R/'prototype/pose_rig';O=R/'art/sprites/weapons/swing'
def main():
 data=json.loads((P/'data/swing.json').read_text());errors=[];levels=[k for k,v in data['levels'].items() if v['status']=='drawn_unapproved'];measure={}
 for angle,expected in data['angles'].items():
  group=[]
  for level in levels:
   e=data['levels'][level]['blades'][angle];path=O/e['file'];image=Image.open(path).convert('RGBA');a=np.array(image);ys,xs=np.where(a[:,:,3]>127);points=np.column_stack([xs+.5,ys+.5]);grip=np.array(e['grip']);tip=np.array(e['tip']);guard=np.array(e['guard']);u=(tip-grip)/np.linalg.norm(tip-grip);v=np.array([-u[1],u[0]]);t=(points-grip)@u;gt=(guard-grip)@u
   blade=points[(t>gt+4)&(t<np.linalg.norm(tip-grip)-2)];assert len(blade)>20
   eig,vec=np.linalg.eigh(np.cov(blade.T));axis=vec[:,-1]
   if axis@u<0:axis=-axis
   deviation=math.degrees(math.atan2(float(u[0]*axis[1]-u[1]*axis[0]),u@axis));actual_length=float(t.max()-gt);grip_to_ink=float(np.linalg.norm(points-grip,axis=1).min());tip_to_ink=float(np.linalg.norm(points-tip,axis=1).min())
   rgb=a[:,:,:3].astype(int);green=int(((rgb[:,:,1]>rgb[:,:,0]+40)&(rgb[:,:,1]>rgb[:,:,2]+40)&(a[:,:,3]>0)).sum());same=path.read_bytes()==(P/'art/swing'/e['file']).read_bytes()
   ok=image.size==tuple(data['canvas']) and e['grip']==data['grip'] and all(float(x).is_integer() for x in e['grip']) and abs(deviation)<=3 and grip_to_ink<=2 and tip_to_ink<=2 and green==0 and same
   if not ok:errors.append(level+'/'+angle)
   group.append((level,deviation,actual_length));print(f'{"PASS" if ok else "FAIL"} level{level}/{angle}: canvas={image.size}, grip={e["grip"]}, actual_axis_error={deviation:.4f}deg, blade_length={actual_length:.4f}px2x, grip_to_ink={grip_to_ink:.4f}, tip_to_ink={tip_to_ink:.4f}, green={green}, runtime_copy={same}')
  reference=next(length for level,deviation,length in group if level=='30');axis_spread=max(x[1] for x in group)-min(x[1] for x in group);length_errors=[abs(x[2]/reference-1) for x in group];pair=max(x[2] for x in group)/min(x[2] for x in group)-1
  ok=axis_spread<=3 and max(length_errors)<=.15 and pair<=.15
  if not ok:errors.append(angle+' cross-level')
  print(f'{"PASS" if ok else "FAIL"} {angle}: cross-level axes spread={axis_spread:.4f}deg; max length change vslevel30={100*max(length_errors):.4f}%; pairwise max={100*pair:.4f}% (limits3deg/15%)')
  measure[angle]={'actual':group,'axis_spread_degrees':axis_spread,'max_length_change':max(length_errors),'max_pairwise_length_change':pair}
 for id,entry in data['trails'].items():
  a=np.array(Image.open(O/entry['file']).convert('RGBA'));rgb=a[:,:,:3].astype(int);green=int(((rgb[:,:,1]>rgb[:,:,0]+40)&(rgb[:,:,1]>rgb[:,:,2]+40)&(a[:,:,3]>0)).sum());assert list(a.shape[:2][::-1])==entry['canvas'];assert (O/entry['file']).read_bytes()==(P/'art/swing'/entry['file']).read_bytes();assert green==0
  print(f'PASS shared trail{id}: canvas={entry["canvas"]}, centre={entry["centre"]}, alpha_max={int(a[:,:,3].max())}, green={green}; one asset shared by all levels')
 total=sum(f['duration'] for f in data['clips']['slash']['frames']);assert abs(total-.3)<1e-9
 print('PASS slash5beats total=',total,'seconds; no A0/config changes')
 pending=[level for level,e in data['levels'].items() if e['status']=='not_drawn'];print('Drawn levels:',levels,'; future template slots not yet drawn:',pending,'; no claim of35completed blades')
 (P/'reports/template_checks.json').write_text(json.dumps({'measurements':measure,'failures':errors,'scope':'actual pixels at15baked images; not final aesthetic approval'},indent=2)+'\n')
 print('Weapon template failures:',len(errors),errors);raise SystemExit(bool(errors))
if __name__=='__main__':main()
