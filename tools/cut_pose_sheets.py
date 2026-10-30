#!/usr/bin/env python3
"""Reproducible soft chroma key, whole-sheet registration, connected silhouette cuts.
No palette quantization or joint rotation. Original generated sheets remain intact.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy import ndimage
R=Path(__file__).resolve().parents[1];C=R/'art/concept/characters/chr_dbl_poses';O=R/'art/sprites/characters/chr_dbl_poses';D=R/'prototype/pose_rig/data'
BODY=[((225,73),(230,272),(231,299)),((573,73),(572,273),(578,298)),((934,72),(936,274),(1062,150)),((1318,73),(1325,275),(1449,171)),((227,400),(229,604),(353,482)),((573,400),(574,604),(709,480)),((937,402),(937,604),(1068,490)),((1327,402),(1326,604),(1452,490)),((226,748),(230,956),(68,865)),((574,747),(576,956),(712,847)),((938,752),(939,956),(975,691)),((1328,752),(1328,956),(1477,783))]
# Coordinates selected visually on original source, not inferred from code of another game.
HIPS=[(184,125),(620,125),(1020,125),(1420,125),(1820,125),(223,486),(620,486),(1010,486),(1325,486),(1810,505)]
HEAD=[(419,513),(1011,513),(1615,513)]
GRIPS=[(385,135),(904,368),(1110,160),(86,713),(674,627),(1170,650)]
TIPS=[(87,452),(558,49),(1480,405),(568,695),(982,910),(1460,909)]
# Head and weapon generators used larger native artwork. Register each ENTIRE
# sheet uniformly before the single common export factor, never stretch axes/poses.
REG={'body':1.0,'legs':1.0,'head':130/420,'kiem':.5,'cung':.63,'arrow':.2,'body_cung':.9}
COMMON=192/(199+230+130)
def key(image):
 a=np.asarray(image.convert('RGBA')).copy();rgb=a[:,:,:3].astype(float);g=rgb[:,:,1];other=np.maximum(rgb[:,:,0],rgb[:,:,2]);excess=g-other
 alpha=np.clip(1-(excess-16)/100,0,1);alpha[excess>100]=0
 # Remove chroma spill on every visible edge, including faint antialiased green.
 spill=(excess>0);rgb[:,:,1][spill]=np.minimum(g[spill],other[spill])
 a[:,:,:3]=np.rint(rgb).astype('uint8');a[:,:,3]=np.rint(alpha*255).astype('uint8');a[a[:,:,3]==0]=0
 return a

def main():
 O.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True);entries={};meta={}
 for kind,file,cols,rows,count in [('body','poses_body',4,3,12),('legs','poses_legs',5,2,10),('head','poses_head',3,1,3)]:
  src=Image.open(C/(file+'.png'));a=key(src);labels,n=ndimage.label(a[:,:,3]>80);objects=ndimage.find_objects(labels)
  components=[]
  for i,sl in enumerate(objects,1):
   if sl is None:continue
   if np.count_nonzero(labels[sl]==i)>100:components.append((i,sl))
  # Identify principal silhouettes by centroid cell. Preserve nearby trail islands
  # within each cell, but use connected component itself across grid boundaries.
  for index in range(count):
   col=index%cols;row=index//cols;x0=round(col*src.width/cols);x1=round((col+1)*src.width/cols);y0=round(row*src.height/rows);y1=round((row+1)*src.height/rows)
   candidates=[(i,sl) for i,sl in components if x0<=(sl[1].start+sl[1].stop)/2<x1 and y0<=(sl[0].start+sl[0].stop)/2<y1]
   assert candidates,(kind,index)
   primary=max(candidates,key=lambda pair:np.count_nonzero(labels[pair[1]]==pair[0]));sl=primary[1]
   bx0=max(0,sl[1].start-3);bx1=min(src.width,sl[1].stop+3);by0=max(0,sl[0].start-3);by1=min(src.height,sl[0].stop+3)
   if kind=='legs':by0=max(by0,HIPS[index][1]) # Remove accidentally generated tunic strip, not pants.
   crop=a[by0:by1,bx0:bx1].copy()
   # Separate detached white physical slash trail in the same cell.
   if kind=='dao' and index in [2,3]:
    bx0=min(bx0,x0);bx1=max(bx1,x1);by0=min(by0,y0);by1=max(by1,y1);crop=a[by0:by1,bx0:bx1].copy()
   f=COMMON*REG[kind];im=Image.fromarray(crop).resize((max(1,round(crop.shape[1]*f)),max(1,round(crop.shape[0]*f))),Image.Resampling.LANCZOS)
   # Interpolation can introduce tiny spill; clamp green only, no palette loss.
   out=np.array(im);visible=out[:,:,3]>0;out[:,:,1][visible]=np.minimum(out[:,:,1][visible],np.maximum(out[:,:,0][visible],out[:,:,2][visible]));out[~visible]=0;im=Image.fromarray(out)
   id=f'{kind}_{index+1:02}' if kind in ['body','legs'] else f'{kind}_{index+1}'
   im.save(O/(id+'.png'))
   def point(p):return [round((p[0]-bx0)*f,6),round((p[1]-by0)*f,6)]
   e={'file':id+'.png','source':file+'.png','source_box':[bx0,by0,bx1,by1],'registration_scale':REG[kind],'common_export_scale':COMMON,'effective_scale':f,'size':list(im.size),'anchors':{}}
   if kind=='body':
    neck,hip,grip=BODY[index];e['anchors']={'neck':point(neck),'hip':point(hip),'grip':point(grip),'back':point((neck[0]-17,neck[1]+28))}
   elif kind=='legs':
    yy,xx=np.where(out[:,:,3]>127);e['anchors']={'hip':point(HIPS[index]),'sole':[round(float(np.median(xx[yy==yy.max()]))+.5,6),int(yy.max())+1]}
   elif kind=='head':e['anchors']={'neck':point(HEAD[index])}
   else:e['anchors']={'grip':point(GRIPS[index]),'tip':point(TIPS[index])}
   entries[id]=e
  meta[kind]={'source_sha256':hashlib.sha256((C/(file+'.png')).read_bytes()).hexdigest(),'components':len(components),'count':count}
 append_weapons(entries,meta)
 data={'version':2,'status':'pilot, not approved','common_scale':COMMON,'registration':REG,'registration_note':'Source sheets NOT natively same anatomical scale. Uniform whole-sheet head/weapon registration disclosed; one common export factor after registration. No per-pose or nonuniform resize.','assets':entries,'sources':meta}
 (O/'anchors.json').write_text(json.dumps(data,indent=2)+'\n');(D/'anchors.json').write_text(json.dumps(data,indent=2)+'\n')
 for id,e in entries.items():
  dest=R/'prototype/pose_rig/art'/e['file'];dest.parent.mkdir(exist_ok=True);dest.write_bytes((O/e['file']).read_bytes())
 print('Whole-sheet registration:',REG,'; common export scale=',COMMON)
 for id,e in entries.items():print(id,e['size'],'effective scale=',e['effective_scale'],'anchors=',e['anchors'])
 # Faithful unquantized reference for engine comparison.
 ref=Image.open(R/'art/reference/ref_dinh_bo_linh.png');arr=key(ref.crop((610,20,780,570)));ri=Image.fromarray(arr);ri=ri.crop(ri.getbbox());ri=ri.resize((round(ri.width*192/ri.height),192),Image.Resampling.LANCZOS);ri.save(R/'prototype/pose_rig/art/reference_side.png')
 build_frames()

def append_weapons(entries,meta):
 regions=json.loads((D/'source_regions.json').read_text())['parts']
 cache={}
 for region in regions:
  name=region['source']
  if name not in cache:
   image=Image.open(C/name);a=key(image);labels,n=ndimage.label(a[:,:,3]>80);objects=ndimage.find_objects(labels)
   cache[name]=(a,labels,objects)
  a,labels,objects=cache[name];x0,y0,x1,y1=region['box'];chosen=[]
  for i,sl in enumerate(objects,1):
   if sl is not None and np.count_nonzero(labels[sl]==i)>30 and x0<=(sl[1].start+sl[1].stop)/2<x1 and y0<=(sl[0].start+sl[0].stop)/2<y1:chosen.append(i)
  assert chosen,region['id']
  mask=ndimage.binary_dilation(np.isin(labels,chosen),iterations=3);ys,xs=np.where(mask)
  bx0=max(0,int(xs.min()));by0=max(0,int(ys.min()));bx1=min(a.shape[1],int(xs.max())+1);by1=min(a.shape[0],int(ys.max())+1)
  crop=a[by0:by1,bx0:bx1].copy();crop[~mask[by0:by1,bx0:bx1]]=0
  f=COMMON*region['registration_scale'];image=Image.fromarray(crop).resize((max(1,round(crop.shape[1]*f)),max(1,round(crop.shape[0]*f))),Image.Resampling.LANCZOS)
  out=np.array(image);visible=out[:,:,3]>0;out[:,:,1][visible]=np.minimum(out[:,:,1][visible],np.maximum(out[:,:,0][visible],out[:,:,2][visible]));out[~visible]=0
  id=region['id'];Image.fromarray(out).save(O/(id+'.png'))
  anchors={k:[round((point[0]-bx0)*f,6),round((point[1]-by0)*f,6)] for k,point in region['anchors'].items()}
  entries[id]={'file':id+'.png','source':name,'source_box':[bx0,by0,bx1,by1],'registration_scale':region['registration_scale'],'common_export_scale':COMMON,'effective_scale':f,'size':[out.shape[1],out.shape[0]],'anchors':anchors}
  meta[name]={'source_sha256':hashlib.sha256((C/name).read_bytes()).hexdigest(),'manual_regions':sum(r['source']==name for r in regions)}

def build_frames():
 def frame(body,legs,head=1,weapon='kiem_1',duration=1/6,attack=False,spawn=False):
  return {'body':body,'legs':f'legs_{legs:02}','head':f'head_{head}','weapon':weapon,'duration':duration,'attack':attack,'spawn':spawn}
 def base(weapon):return {
  'idle':{'loop':True,'frames':[frame(f'body_{b:02}',1,weapon=weapon) for b in [1,2,1,2]]},
  'run':{'loop':True,'frames':[frame(f'body_{b:02}',l,weapon=weapon,duration=1/12) for b,l in zip(range(3,9),range(2,8))]},
  'jump':{'loop':False,'frames':[frame('body_09',8,weapon=weapon,duration=.19) for _ in range(2)]},
  'fall':{'loop':True,'frames':[frame('body_10',9,weapon=weapon,duration=1/12) for _ in range(2)]}}
 kiem=base('kiem_1');cung=base('cung_1')
 kiem['slash']={'loop':False,'frames':[frame(b,10,2,w,.075,True) for b,w in [('body_11','kiem_2'),('body_12','kiem_3'),('body_12','kiem_4'),('body_12','kiem_5')]]}
 kiem['thrust']={'loop':False,'frames':[frame('body_12',10,2,'kiem_6',.05,True),frame('body_12',10,2,'kiem_6',.05,True)]}
 # Three authored shooting phases retain five15fps timing slots (ready2/draw1/release2).
 cung['shoot']={'loop':False,'frames':[frame('body_cung_1',1,1,'cung_2',2/15,True),frame('body_cung_2',1,1,'cung_3',1/15,True),frame('body_cung_3',1,1,'cung_4',2/15,True,True)]}
 # Two running phases retain six12fps timing slots; release starts at original slot3.
 cung['run_shoot']={'loop':True,'frames':[frame('body_cung_4',3,1,'cung_3',2/12,True),frame('body_cung_3',4,1,'cung_4',4/12,True,True)]}
 (D/'frames.json').write_text(json.dumps({'status':'pilot; Kiếm/Cung; five15fps shoot slots compressed to3 painted phases; six12fps run-shoot slots compressed to2 phases; thrust2frames .10s proposed, no standalone thrust timing in09; slash .30s unchanged','arrow_speed':240,'arrow_asset':'arrow_1','schools':{'kiem':kiem,'cung':cung},'clips':kiem},indent=2)+'\n')
if __name__=='__main__':main()
