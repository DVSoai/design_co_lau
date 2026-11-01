#!/usr/bin/env python3
"""Verify bow-only scope against the incoming branch and real layer renders."""
from pathlib import Path
from io import BytesIO
import subprocess,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE='f6b9316';failures=[]
def original(path):return subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT)
def check(ok,msg):
 print(('PASS: ' if ok else 'FAIL: ')+msg)
 if not ok:failures.append(msg)
def tile(im,i):return im[(i//4)*256:(i//4+1)*256,(i%4)*256:(i%4+1)*256]
def same_rgba(a,b):
 if not np.array_equal(a[:,:,3],b[:,:,3]):return False
 visible=np.maximum(a[:,:,3],b[:,:,3])>0;return np.array_equal(a[visible],b[visible])
def main():
 paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'prototype/pose_rig/art/lv1_30'],cwd=ROOT,text=True).splitlines();images=[p for p in paths if p.endswith('.png') and not p.endswith('/cung_lv1.png')]
 check(all(original(p)==(ROOT/p).read_bytes() for p in images),f'ALL {len(images)} existing non-bow engine PNGs byte-identical (sword, action art, body/head/legs/free arm)')
 for path in (ROOT/'art/sprites/weapons/lv1').glob('kiem*'):
  if path.is_file():check(original(path.relative_to(ROOT))==path.read_bytes(),path.name+' unchanged')
 for name in ['parts','frames30','skills','effects']:
  path=Path('prototype/pose_rig/data')/(name+'.json');check(original(path)==(ROOT/path).read_bytes(),name+' exact byte identity: grip, angle, placement, motion/timing untouched')
 path=Path('prototype/pose_rig/art/lv1_30/cung_lv1.png');old=Image.open(BytesIO(original(path))).convert('RGBA');new=Image.open(ROOT/path).convert('RGBA')
 check(old.size==new.size and old.getbbox()==new.getbbox(),'bow source size and complete alpha bbox unchanged')
 old_dir=ROOT/'prototype/pose_rig/reports/ablation_v8';new_dir=ROOT/'prototype/pose_rig/reports/ablation_v9';old_manifest=json.loads((old_dir/'manifest.json').read_text());new_manifest=json.loads((new_dir/'manifest.json').read_text());variants=new_manifest['variants']
 comparisons=0;bad=[]
 for entry in old_manifest['entries']:
  a=np.array(Image.open(old_dir/entry['file']).convert('RGBA'));b=np.array(Image.open(new_dir/entry['file']).convert('RGBA'))
  names=old_manifest['variants'] if entry['school']=='kiem' else ['no_weapon','body_only','legs_only','head_only','fingers_only']
  for name in names:
   comparisons+=1
   if not same_rgba(tile(a,old_manifest['variants'].index(name)),tile(b,variants.index(name))):bad.append(entry['file']+':'+name)
 check(not bad,f'{comparisons} real render comparisons: ALL sword layers and bow actor without held bow unchanged; changed='+repr(bad))
 print('Bow-only scope failures='+str(len(failures)));return bool(failures)
if __name__=='__main__':raise SystemExit(main())
