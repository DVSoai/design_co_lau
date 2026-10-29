"""Check polished materials and actual Godot-evaluated knee/sole geometry."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
from snap_pixel import load_groups
ROOT=Path(__file__).resolve().parents[1]
def main():
 data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text())
 poses=json.loads((ROOT/'prototype/rig/data/animations.json').read_text())
 source=json.loads((ROOT/'prototype/rig/data/animations_greybox.json').read_text())
 checks=json.loads((ROOT/'prototype/rig/reports/leg_polish.json').read_text());failures=0;errors=[]
 for row in checks:
  name=row['clip'];i=row['frame']-1;frame=data[name]['frames'][i];j=frame['joints'];angles=[];feet=[]
  for side in ['near','far']:
   hip=np.array(j['thigh_'+side]);knee=np.array(j['shin_'+side]);ankle=np.array(j['foot_'+side]);v=knee-hip;w=ankle-knee
   bend=math.degrees(math.acos(np.clip(v@w/(np.linalg.norm(v)*np.linalg.norm(w)),-1,1)))
   reduction=1-bend/abs(row['old_knee_degrees'][side]);angles.append(round(100*reduction,3))
   if not .30<=reduction<=.40:errors.append(f'{name}/{i}/{side} knee reduction')
   foot=next(p for p in frame['geometry'] if p['id']=='foot_'+side and p['kind']=='sprite');a,b,c,d,tx,ty=foot['transform'];size=Image.open(ROOT/'prototype'/foot['source'].removeprefix('res://')).size
   bottom=max(b*x+d*y+ty for x,y in [(0,0),(size[0],0),size,(0,size[1])]);feet.append(round(bottom,5))
   if abs(bottom-row['foot_targets'][side][1])>.001:errors.append(f'{name}/{i}/{side} sole target')
   if bottom>.001:errors.append(f'{name}/{i}/{side} underground')
  rise=row['old_hip'][1]-j['body'][1]
  if rise<=0:errors.append(f'{name}/{i} hip not raised')
  print(f'{name} frame={i+1}: knee reduction near/far={angles}%; hip rise={rise:.3f}px; sole y near/far={feet}')
 for name,clip in poses['clips'].items():
  old=source['clips'][name]
  if len(clip['frames'])!=len(old['frames']):errors.append(name+' count')
  for f,g in zip(clip['frames'],old['frames']):
   if f['duration']!=g['duration']:errors.append(name+' timing')
  if clip.get('events')!=old.get('events'):errors.append(name+' events')
 print('13 clip frame counts, durations and events retained')
 g=load_groups(ROOT/'art/reference/palette.gpl')
 for id in ['dao','bow','thigh_near','thigh_far']:
  a=np.array(Image.open(ROOT/f'art/sprites/characters/chr_dbl_parts/{id}.png').convert('RGBA'));opaque=a[:,:,3]>0
  counts={name:int(sum(tuple(px) in colours for px in a[:,:,:3][opaque])) for name,colours in g.items()};counts={k:v for k,v in counts.items() if v}
  if id.startswith('thigh') and any(k not in ['outline','pants'] for k in counts):errors.append(id+' exposed skin')
  if id=='bow' and any(k not in ['outline','belt','limestone'] for k in counts):errors.append('bow material')
  print(id,'material pixel counts:',counts)
 if poses['clips']['shoot']['frames'][0]['angles']['bow']!=90:errors.append('bow orientation')
 definition=json.loads((ROOT/'prototype/rig/data/parts.json').read_text())
 if definition['bow_string']['color']!='#D9DDD0':errors.append('string colour')
 sheets=ROOT/'prototype/rig/contact_sheets/art'
 for name,clip in data.items():
  if name=='standing_neutral':continue
  size=Image.open(sheets/f'chr_dbl_anim_{name}_art.png').size
  if size!=(160*len(clip['frames']),160):errors.append(name+' sheet size')
 idle=Image.open(sheets/'chr_dbl_idle_art_1x.png').convert('RGBA');x4=Image.open(sheets/'chr_dbl_idle_art_4x.png').convert('RGBA')
 if not np.array_equal(np.array(idle.resize((512,512),Image.Resampling.NEAREST)),np.array(x4)):errors.append('idle x4')
 print('15 art contact sheets: frame dimensions correct; idle x4 equals saved 1x resized NEAREST')
 for name in ['run','shoot']:
  for right,left in zip(data[name]['frames'],data[name+'_left']['frames']):
   by_id={p['id']:p for p in left['geometry'] if p['kind']=='sprite'}
   for part in right['geometry']:
    if part['kind']!='sprite':continue
    other=by_id[part['id']];a=np.array(part['transform']);b=np.array(other['transform']);a[[0,2,4]]*=-1
    if not np.allclose(a,b,atol=.001) or part['z']!=other['z']:errors.append(name+' art mirror/layers')
 print('Art run/shoot: both directions reflect actual sprite transforms, near/far layers unchanged')
 failures=len(errors);print('Polish failures:',failures,errors);raise SystemExit(bool(failures))
if __name__=='__main__':main()
