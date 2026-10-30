#!/usr/bin/env python3
"""Temporary three-way comparisons of real captures. Never save foreign art in repo."""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--reference-dir',type=Path,default=Path('/tmp/ref_render'));p.add_argument('--own-dir',type=Path,default=Path('/tmp/ref_render/own'));p.add_argument('--out',type=Path,default=Path('/tmp/ref_render/comparisons'));a=p.parse_args()
assert not a.out.resolve().is_relative_to(R),'Comparison output must stay OUTSIDE the repository'
a.out.mkdir(parents=True,exist_ok=True)
# Reference renderer contract: body-only standing frame determines scale/baseline,
# so gear/effects retain their actual size and are never independently stretched.
base=Image.open(a.reference_dir/'ref_30_khung.png').convert('RGB').crop((0,0,280,248));ar=np.array(base);ys,xs=np.where(np.any(ar!=ar[0,0],axis=2));ref_h=int(ys.max()-ys.min()+1);ref_foot=int(ys.max()+1);ref_scale=128/ref_h
board=Image.open(R/'art/reference/chr_dbl_board_trang_bi.png').crop((99,353,144,420)).convert('RGBA');board=board.resize((round(board.width*128/board.height),128),Image.Resampling.NEAREST)
manifest=json.loads((a.own_dir/'own_render_manifest.json').read_text());count=0
for school in ['kiem','cung']:
 body=Image.open(a.own_dir/f'{school}_body00.png').convert('RGBA');bb=body.getbbox();own_h=bb[3]-bb[1];own_foot=bb[3];own_scale=128/own_h
 print(f'{school}: actual Godot human-alpha H={own_h}px; comparison normalization={own_scale:.9f}; reference H={ref_h}px ->128; board crop H=67px ->128')
 for name in manifest['files']:
  if not name.startswith(school+'_') or '_body00' in name:continue
  own=Image.open(a.own_dir/name).convert('RGBA');stem=Path(name).stem
  if '_frame' in stem:
   idx=int(stem.rsplit('frame',1)[1]);ref=Image.open(a.reference_dir/f'ref_cam_{school}.png').crop((280*idx,0,280*(idx+1),248));ref_rootfoot=ref_foot
  else:
   idx=int(stem.rsplit('_',1)[1]);ref=Image.open(a.reference_dir/f'ref_don_{school}.png').crop((440*idx,0,440*(idx+1),280));ref_rootfoot=ref_foot+16 # renderer CY58Z vs54Z
  # Same standing-body scale for every pose. Crouching remains naturally shorter.
  own=own.resize((round(own.width*own_scale),round(own.height*own_scale)),Image.Resampling.NEAREST)
  ref=ref.resize((round(ref.width*ref_scale),round(ref.height*ref_scale)),Image.Resampling.NEAREST).convert('RGBA')
  out=Image.new('RGBA',(1260,280),'#202833');baseline=220
  out.alpha_composite(own,(round(210-240*own_scale),round(baseline-own_foot*own_scale)))
  out.alpha_composite(board,(420+(420-board.width)//2,baseline-128))
  out.alpha_composite(ref,(round(840+210-(100 if '_frame' in stem else 120)*ref_scale),round(baseline-ref_rootfoot*ref_scale)))
  out.convert('RGB').save(a.out/(stem+'_own_board_reference.png'));count+=1
print(f'Generated{count} TEMPORARY comparisons: left=own actual scene, centre=own Lv1 Total board, right=reference renderer. Standing-body height128px for all3; no added text or invented graphics.')
print('Output:',a.out)
