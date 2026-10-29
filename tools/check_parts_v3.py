"""Regression gate and comparison assembled exclusively from real PNG/scene exports."""
from pathlib import Path
import io,json,subprocess
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def main():
 base=ROOT/'prototype/rig/reports/v3_baseline';old=json.loads((base/'animations.json').read_text());new=json.loads((ROOT/'prototype/rig/data/animations.json').read_text())
 oldparts=json.loads((base/'parts.json').read_text());parts=json.loads((ROOT/'prototype/rig/data/parts.json').read_text())
 errors=[]
 def check(ok,label):
  print(('OK' if ok else 'FAIL')+': '+label)
  if not ok:errors.append(label)
 op={p['id']:p for p in oldparts['parts']};np_={p['id']:p for p in parts['parts']}
 canonical='art/sprites/characters/chr_dbl_parts/head.png';source=Image.open(io.BytesIO(subprocess.check_output(['git','show','main:'+canonical],cwd=ROOT))).convert('RGBA')
 for path in [canonical,'prototype/rig/art_parts/head.png']:
  check(np.array_equal(np.array(source),np.array(Image.open(ROOT/path).convert('RGBA'))),path+' RGBA identical to main')
 check(op['head']==np_['head'],'head pivot/attach/all metadata identical')
 for name,clip in new['clips'].items():
  before=old['clips'][name];check(len(clip['frames'])==len(before['frames']) and [f['duration'] for f in clip['frames']]==[f['duration'] for f in before['frames']] and clip.get('events')==before.get('events'),name+' counts/timing/events unchanged')
  if name not in ['idle','turn','land']:check(clip==before,name+' entire animation data unchanged')
  elif name in ['turn','land']:check(clip['frames'][:-1]==before['frames'][:-1],name+' only final standing frame edited')
 oldframes=json.loads((base/'evaluated_art_frames.json').read_text());frames=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());count=0
 for name,clip in new['clips'].items():
  if name in ['idle','turn','land']:continue
  for f,g in zip(oldframes[name]['frames'],frames[name]['frames']):
   for id,point in f['joints'].items():
    check_ok=np.allclose(point,g['joints'][id],atol=.0001)
    if not check_ok:errors.append(f'{name} joint {id} moved')
    count+=1
 print(f'Unchanged-action actual-scene joint comparisons: {count}; failures={len(errors)}')
 idle=[f for f in frames['idle']['frames']]
 for id in ['thigh_near','thigh_far','shin_near','shin_far','foot_near','foot_far']:
  check(all(np.allclose(idle[0]['joints'][id],f['joints'][id],atol=.0001) for f in idle),id+' planted across all idle frames')
 for id in ['body','head','upper_arm_near','upper_arm_far','forearm_near','forearm_far','hand_near','hand_far']:
  check(all(np.allclose(np.array(f['joints'][id])-idle[0]['joints'][id],[0,bob],atol=.0001) for f,bob in zip(idle,[0,-1,-2,-1])),id+' idle breath offsets 0,-1,-2,-1')
 after=Image.open(ROOT/'prototype/rig/contact_sheets/art/chr_dbl_idle_art_1x.png').convert('RGBA');bounds=after.getbbox()
 check(after.size==(128,128) and bounds[3]==120 and bounds[3]-bounds[1]==96,'standing frame128x128; nominal silhouette96; bottom margin8')
 # Keep original before raster unchanged: its actual height is 95, disclosed in report.
 reference=Image.open(ROOT/'art/reference/ref_dinh_bo_linh.png').convert('RGBA');arr=np.array(reference);crop=arr[20:570,610:780].copy();green=(crop[:,:,1]>240)&(crop[:,:,0]<20)&(crop[:,:,2]<20);crop[green]=0
 ref=Image.fromarray(crop);ref=ref.crop(ref.getbbox());ref=ref.resize((round(ref.width*96/ref.height),96),Image.Resampling.BOX)
 canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(ref,((256-ref.width)//2,24))
 before=Image.open(ROOT/'docs/reports/g1_parts_v3_before_idle_1x.png').convert('RGBA');canvas.alpha_composite(before,(0,128));canvas.alpha_composite(after,(128,128))
 canvas.resize((1024,1024),Image.Resampling.NEAREST).save(ROOT/'docs/reports/g1_parts_v3_compare.png')
 print('Comparison: reference side view normalized to96px at top; original-before/after saved scene PNGs at bottom; whole composite x4NEAREST; no text/drawing/imagegen')
 print(f'V3 regression failures: {len(errors)}',errors)
 raise SystemExit(bool(errors))
if __name__=='__main__':main()
