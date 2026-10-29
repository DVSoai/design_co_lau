"""Outline editable v3 body only against actual scene silhouette. Head untouched."""
from pathlib import Path
import json, math, shutil
import numpy as np
from PIL import Image
from render_parts_scene import layers
ROOT=Path(__file__).resolve().parents[1]
def main():
 data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text())
 frame=data['idle']['frames'][0];owner=np.full((128,128),'',object);mask=np.zeros((128,128),bool)
 for id,layer in layers(frame,(128,128),(64,120)):
  opaque=np.array(layer)[:,:,3]>0;owner[opaque]=id;mask|=opaque
 pad=np.pad(mask,1);edge=mask&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
 raw=np.array(Image.open(ROOT/'prototype/rig/art_parts/v3_body_unoutlined.png').convert('RGBA'));body=raw.copy()
 item=next(i for i in frame['geometry'] if i['id']=='body' and i['kind']=='sprite');a,b,c,d,tx,ty=item['transform'];count=0
 for y,x in zip(*np.where(body[:,:,3]>0)):
  gx=math.floor(a*(x+.5)+c*(y+.5)+tx+64);gy=math.floor(b*(x+.5)+d*(y+.5)+ty+120)
  # Top neck cut and lower attachment cap stay material, never ink.
  if y<3 or y>26:continue
  if 0<=gx<128 and 0<=gy<128 and owner[gy,gx]=='body' and edge[gy,gx]:
   body[y,x,:3]=[23,21,26];count+=1
 path=ROOT/'art/sprites/characters/chr_dbl_parts/body.png';Image.fromarray(body).save(path);shutil.copyfile(path,ROOT/'prototype/rig/art_parts/body.png')
 print(f'V3 body-only external outline: {count} pixels; neck/joint caps unoutlined; no other PNG edited')
if __name__=='__main__':main()
