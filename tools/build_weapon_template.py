#!/usr/bin/env python3
"""Register original generated swords onto a fixed2x template and bake angles ONCE.
Runtime uses staticPNG only. Own source, offline supersampling, no reference-game data.
"""
from pathlib import Path
import json,math,copy,hashlib
import numpy as np
from PIL import Image
from scipy import ndimage
R=Path(__file__).resolve().parents[1];O=R/'art/sprites/weapons/swing';P=R/'prototype/pose_rig';GRIP=np.array([96.,144.]);SIZE=(256,256)
ANGLES={'gio_sau':-135,'vung_len':-45,'ngang':0,'bo_xuong':45,'dam':0}
SOURCE={1:{'component':2,'grip':[125,144],'guard':[214,144],'tip':[714,143],'length':90},30:{'component':3,'grip':[851,144],'guard':[943,144],'tip':[1436,143],'length':96},60:{'component':1,'grip':[1578,144],'guard':[1661,144],'tip':[2143,143],'length':100}}
def chroma(image):
 a=np.array(image.convert('RGBA'));rgb=a[:,:,:3].astype(float);other=np.maximum(rgb[:,:,0],rgb[:,:,2]);excess=rgb[:,:,1]-other
 alpha=np.clip(1-(excess-16)/100,0,1);alpha[excess>100]=0;spill=excess>35;rgb[:,:,1][spill]=np.minimum(rgb[:,:,1][spill],other[spill]);a[:,:,:3]=np.rint(rgb).astype('uint8');a[:,:,3]=np.rint(alpha*255).astype('uint8');a[a[:,:,3]==0]=0;return a

def main():
 srcpath=O/'sources/straight_tiers.png';src=Image.open(srcpath);a=chroma(src);rgb=np.array(src.convert('RGB')).astype(int);mask=~((rgb[:,:,1]>rgb[:,:,0]+40)&(rgb[:,:,1]>rgb[:,:,2]+40));labels,n=ndimage.label(mask)
 dest=P/'art/swing';dest.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
 template={'status':'unapproved pilot','scale':.5,'canvas':list(SIZE),'grip':GRIP.tolist(),'angles':ANGLES,'levels':{},'planned_levels':[1,10,20,30,40,50,60],'source_sha256':hashlib.sha256(srcpath.read_bytes()).hexdigest(),'source_landmarks':SOURCE,'trails':{}}
 for level in template['planned_levels']:
  if level not in SOURCE:
   template['levels'][str(level)]={'status':'not_drawn','blades':{angle:{'file':None,'expected_file':f'lv{level}_{angle}.png'} for angle in ANGLES}};continue
  info=SOURCE[level];piece=a.copy();piece[~ndimage.binary_dilation(labels==info['component'],iterations=3)]=0;image=Image.fromarray(piece);sg=np.array(info['grip'],float);tip=np.array(info['tip'],float);length=np.linalg.norm(tip-sg);scale=info['length']/length;axis=math.atan2(*(tip-sg)[::-1]);entries={}
  for name,degrees in ANGLES.items():
   theta=math.radians(degrees)-axis;c=math.cos(theta);s=math.sin(theta);rot=np.array([[c,-s],[s,c]]);inv=rot.T/scale;shift=sg-inv@GRIP;ss=4
   coeff=(inv[0,0]/ss,inv[0,1]/ss,shift[0],inv[1,0]/ss,inv[1,1]/ss,shift[1])
   output=image.transform((SIZE[0]*ss,SIZE[1]*ss),Image.Transform.AFFINE,coeff,resample=Image.Resampling.BICUBIC).resize(SIZE,Image.Resampling.LANCZOS)
   out=np.array(output);visible=out[:,:,3]>0;green=(out[:,:,1].astype(int)>np.maximum(out[:,:,0],out[:,:,2]).astype(int)+35)&visible;out[:,:,1][green]=np.maximum(out[:,:,0],out[:,:,2])[green];out[~visible]=0
   file=f'lv{level}_{name}.png';Image.fromarray(out).save(O/file);(dest/file).write_bytes((O/file).read_bytes())
   target_tip=GRIP+scale*rot@(tip-sg);guard=GRIP+scale*rot@(np.array(info['guard'])-sg)
   entries[name]={'file':file,'grip':GRIP.tolist(),'guard':guard.tolist(),'tip':target_tip.tolist(),'axis_degrees':degrees,'source_registration_scale':scale,'pixel_sha256':hashlib.sha256((O/file).read_bytes()).hexdigest()}
  template['levels'][str(level)]={'status':'drawn_unapproved','blades':entries}
 # Independent shared crescent art; fade tails toward back (left) and fade final frame.
 for index,component,height,opacity in [(1,91,132,1),(2,4,184,1),(3,6,160,.85),(4,7,144,.35)]:
  selected=ndimage.binary_dilation(labels==component,iterations=3);ys,xs=np.where(selected);box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1);part=a.copy();part[~selected]=0;im=Image.fromarray(part).crop(box);factor=height/im.height;im=im.resize((round(im.width*factor),height),Image.Resampling.LANCZOS)
  ar=np.array(im);vg=(ar[:,:,1].astype(int)>np.maximum(ar[:,:,0],ar[:,:,2]).astype(int)+35)&(ar[:,:,3]>0);ar[:,:,1][vg]=np.maximum(ar[:,:,0],ar[:,:,2])[vg];fade=np.clip(.15+1.2*np.linspace(0,1,im.width),0,1)**.65;ar[:,:,3]=np.rint(ar[:,:,3]*fade[None,:]*opacity).astype('uint8');ar[ar[:,:,3]==0]=0
  canvas=Image.new('RGBA',(320,208));canvas.alpha_composite(Image.fromarray(ar),(round((320-im.width)/2),round((208-im.height)/2)));file=f'trail_{index}.png';canvas.save(O/file);(dest/file).write_bytes((O/file).read_bytes());template['trails'][str(index)]={'file':file,'canvas':[320,208],'centre':[160,104],'opacity_baked':opacity,'source_component':component,'source_box':box}

 # Extend only the wooden shaft offline; feather/head dimensions stay unchanged.
 original_arrow=Image.open(P/'art/arrow_1.png').convert('RGBA');aa=np.array(original_arrow);middle=round(original_arrow.width*.5);extra=52
 long=np.concatenate([aa[:,:middle],np.repeat(aa[:,middle:middle+1],extra,axis=1),aa[:,middle:]],axis=1)
 Image.fromarray(long).save(O/'arrow_ready.png');(dest/'arrow_ready.png').write_bytes((O/'arrow_ready.png').read_bytes())
 old_anchors=json.loads((P/'data/anchors.json').read_text())['assets']['arrow_1']['anchors'];tail=old_anchors['tail'];tip=old_anchors['tip'].copy();tip[0]+=extra
 template['arrow']={'file':'arrow_ready.png','size':[long.shape[1],long.shape[0]],'tail':tail,'tip':tip,'shaft_extension_px':extra,'notes':'Own existing arrow art; only shaft lengthened offline, feather and point unchanged; same image used on string and separate flying sprite'}
 phases=[('gio_sau',None,[0,0],.05,0),('vung_len','1',[90,-78],.05,1),('ngang','2',[100,-48],.075,2),('bo_xuong','3',[85,-38],.075,3),('bo_xuong','4',[87,-36],.05,3)]
 frames=json.loads((P/'data/frames.json').read_text());old=frames['schools']['kiem']['slash']['frames'];slash=[]
 for angle,trail,offset,duration,source_index in phases:
  f=copy.deepcopy(old[source_index]);f['swing_angle']=angle;f['trail']=trail;f['trail_offset']=offset;f['duration']=duration;slash.append(f)
 thrust=copy.deepcopy(frames['schools']['kiem']['thrust']['frames'])
 for f in thrust:f['swing_angle']='dam';f['trail']=None;f['trail_offset']=[0,0]
 template['clips']={'slash':{'loop':False,'frames':slash},'thrust':{'loop':False,'frames':thrust}}
 template['notes']='5own beats use existing body poses; last beat holds followthrough; trails centre offsets in actor logic pixels; no runtime rotation;4planned levels not drawn'
 frames['swing_owner']='swing.json owns Kiếm slash/thrust; frames copies generated only for compatibility';frames['arrow_asset']='ready_arrow';frames['schools']['kiem']['slash']['frames']=slash;frames['schools']['kiem']['thrust']['frames']=thrust;frames['clips']=frames['schools']['kiem']
 for clip in frames['schools']['cung'].values():
  for f in clip['frames']:f['nocked']=f['attack'] and f['weapon']=='cung_3'
 (P/'data/swing.json').write_text(json.dumps(template,ensure_ascii=False,indent=2)+'\n');(P/'data/frames.json').write_text(json.dumps(frames,ensure_ascii=False,indent=2)+'\n')
 print('Own generated source SHA256:',template['source_sha256']);print('Baked15 static sword PNGs; angles=',ANGLES,'; canvas256x256; shared grip(96,144);2x')
 print('Drawn levels1/30/60; planned10/20/40/50 explicitly not_drawn; shared trails4; no runtime rotation')
 print('Slash5beats total:',sum(f['duration'] for f in slash),'s; source body IDs:',[f['body'] for f in slash]);print('Nocked arrow flags enabled only on drawn-string frames; source body PNGs unchanged')
if __name__=='__main__':main()
