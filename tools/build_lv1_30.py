#!/usr/bin/env python3
"""Normalize independently generated Lv1 sheets; registration authored on source pixels.
No reference-board pixels are used in sprite textures. Offline transforms only.
"""
from pathlib import Path
import json, math, shutil, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label as components
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'art/sprites/characters/lv1_30'; SRC=BASE/'sources'
OUT=ROOT/'prototype/pose_rig/art/lv1_30';OUT.mkdir(parents=True,exist_ok=True)
DATA=ROOT/'prototype/pose_rig/data'
assets={}
def key(im):
 a=np.array(im.convert('RGBA')).astype(float);r,g,b=a[:,:,:3].transpose(2,0,1)
 alpha=np.clip(1-(g-np.maximum(r,b))/np.maximum(g,1),0,1);alpha[(g>1.18*np.maximum(r,b))&(g>90)]=0
 a[:,:,3]=alpha*255;a[:,:,1]=np.minimum(g,np.maximum(r,b)+15);a[alpha==0,:3]=0
 return Image.fromarray(a.astype('uint8'))
def save(id,im,points,source=None):
 im=im.convert('RGBA');a=np.array(im);r,g,b=a[:,:,:3].transpose(2,0,1);bad=(g>1.18*np.maximum(r,b))&(g>90)&(a[:,:,3]>0);a[bad]=0;im=Image.fromarray(a)
 im.save(BASE/(id+'.png'));shutil.copyfile(BASE/(id+'.png'),OUT/(id+'.png'))
 prompt_sheet=source.get('sheet') if isinstance(source,dict) else ('legs' if id.startswith('legs_') else 'weapons')
 prompt=(SRC/(prompt_sheet+'.prompt.txt')).read_text() if prompt_sheet else ''
 (BASE/(id+'.prompt.txt')).write_text(prompt+'\nProcessing: tools/build_lv1_30.py; '+str(source)+'\n')
 assets[id]={'file':id+'.png','size':list(im.size),'anchors':points,'source':source,'status':'drawn_unapproved'}
def piece(sheet,i,cols,rows,id,points,scale,box_override=None):
 im=Image.open(SRC/(sheet+'.png'));w,h=im.size
 box=[round((i%cols)*w/cols),round((i//cols)*h/rows),round((i%cols+1)*w/cols),round((i//cols+1)*h/rows)]
 if box_override:box=box_override
 cut=key(im.crop(box))
 if True:
  ar=np.array(cut);labels,count=components(ar[:,:,3]>16);sizes=np.bincount(labels.ravel());sizes[0]=0
  if count:ar[labels!=sizes.argmax()]=0
  cut=Image.fromarray(ar)
 bb=cut.getbbox();assert bb,(sheet,i)
 cut=cut.crop(bb);origin=(box[0]+bb[0],box[1]+bb[1]);size=[max(1,round(x*scale)) for x in cut.size]
 pts={k:[round((v[0]-origin[0])*scale,3),round((v[1]-origin[1])*scale,3)] for k,v in points.items()}
 save(id,cut.resize(size,Image.Resampling.LANCZOS),pts,{'sheet':sheet,'cell':i,'crop':box,'bounds':bb,'scale':scale})
# Latest decision: bare head+hair0.40H, NO HAT. Earlier50%/hat sources are history.
head_boxes=[(0,0,465,402),(470,0,910,402),(920,0,1330,434),(1335,0,1774,390),(0,444,465,800),(470,444,910,802),(920,444,1330,800),(1335,444,1774,818)]
neck_x=[278,708,1155,1595,275,708,1155,1595]
for i,box in enumerate(head_boxes):
 raw=key(Image.open(SRC/'heads_50.png').crop(box));bb=raw.getbbox();factor=77/(bb[3]-bb[1])
 piece('heads_50',i,4,2,f'head_without_hat_{i}',{'neck':(neck_x[i],box[3])},factor,box)
 bare=Image.open(BASE/f'head_without_hat_{i}.png');bp=assets[f'head_without_hat_{i}']['anchors'];bp['neck'][1]=bare.height
 save(f'head_without_hat_{i}',bare,bp,assets[f'head_without_hat_{i}']['source'])
 composite=bare;neck=bp['neck']
 if i in [4,5,6]:
  deg={4:90,5:180,6:270}[i];canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(composite,(round(128-neck[0]),round(128-neck[1])));composite=canvas.rotate(-deg,Image.Resampling.BICUBIC,center=(128,128));neck=[128,128]
 save(f'head_{i}',composite,{'neck':neck},{'sheet':'heads_50','bare_asset':f'head_without_hat_{i}','hat':False,'target_ratio':.40,'offline_angle':{4:90,5:180,6:270}.get(i,0)})
# short broad torso: neutral neck-to-hip40source pixels =20logic pixels.
A=[((280,66),(270,214),(399,266),(143,265)),((750,66),(747,216),(882,270),(631,267)),((1290,74),(1239,224),(1455,142),(1061,220)),((282,404),(238,551),(466,450),(71,530)),((805,415),(760,552),(954,510),(591,484)),((1287,413),(1241,556),(1085,528),(1465,468)),((413,836),(236,810),(294,767),(243,892)),((789,920),(786,735),(634,778),(919,775)),((1350,843),(1197,813),(1272,734),(1184,824))]
B=[((332,78),(270,234),(204,246),(409,224)),((790,67),(752,234),(585,206),(866,279)),((1285,88),(1225,247),(1488,171),(1032,194)),((266,390),(251,557),(345,447),(198,564)),((793,397),(758,559),(1004,458),(619,497)),((1271,394),(1241,559),(1210,569),(1346,570)),((268,713),(259,865),(166,729),(499,762)),((786,716),(779,866),(684,731),(986,760)),((1285,716),(1273,867),(1132,703),(1492,760))]
for i,(n,h,g,f) in enumerate(A+B):
 factor=50/(h[1]-n[1]) if i in [0,12] else 50/math.dist(n,h)
 piece('bodies_a_board40' if i<9 else 'bodies_b_board40',i if i<9 else i-9,3,3,f'body_{i}',{'neck':n,'hip':h,'grip':g,'far_hand':f,'near_hand':g,'back':(h[0]-65,h[1]-80)},factor)
# Ten new short-leg drawings; common slots7..9 are offline somersault views.
legpoints=[((196,80),(196,362)),((586,83),(454,365)),((976,82),(883,366)),((1371,75),(1568,319)),((1853,82),(1901,362)),((192,469),(99,719)),((593,457),(592,683)),((981,479),(982,717)),((1430,472),(1409,716)),((1852,489),(1860,708))]
for i,(hip,sole) in enumerate(legpoints):
 factor=65/(sole[1]-hip[1]) if i==0 else 65/math.dist(hip,sole)
 piece('legs_board40',i,5,2,f'legs_{i}',{'hip':hip,'sole':sole},factor)
 im=Image.open(BASE/f'legs_{i}.png');ar=np.array(im)
 points=assets[f'legs_{i}']['anchors']
 if i in [0,1,4,5,7,8]:points['sole'][1]=im.height
 save(f'legs_{i}',Image.fromarray(ar),points,assets[f'legs_{i}']['source'])
# Auxiliary guard/lunge preserve the ten movement slots while allowing a long step.
for id,slot,height in [('legs_guard',7,57),('legs_lunge',8,57)]:
 im=Image.open(BASE/f'legs_{slot}.png');e=assets[f'legs_{slot}'];factor=height/(e['anchors']['sole'][1]-e['anchors']['hip'][1]);size=(round(im.width*factor),round(im.height*factor))
 save(id,im.resize(size,Image.Resampling.LANCZOS),{k:[v[0]*factor,v[1]*factor] for k,v in e['anchors'].items()},{'sheet':'legs_board40','cell':slot,'stance_height_source':height})
base=Image.open(BASE/'legs_6.png');bp=assets['legs_6']['anchors']
for i,degrees in [(7,90),(8,180),(9,270)]:
 canvas=Image.new('RGBA',(192,192));hx,hy=bp['hip'];canvas.alpha_composite(base,(round(96-hx),round(96-hy)));canvas=canvas.rotate(-degrees,Image.Resampling.BICUBIC,center=(96,96));vx,vy=bp['sole'][0]-hx,bp['sole'][1]-hy;r=math.radians(degrees)
 save(f'legs_{i}',canvas,{'hip':[96,96],'sole':[96+vx*math.cos(r)-vy*math.sin(r),96+vx*math.sin(r)+vy*math.cos(r)]},{'sheet':'legs_board40','cell':6,'offline_angle':degrees})
# Weapon sheet1983x793. All points measured from its source, then normalized uniformly.
W=[('sword',0,{'grip':(137,352),'tip':(405,95)},.23),('bow_idle',1,{'grip':(692,232),'belly':(711,232),'string':(599,232),'top':(600,55),'bottom':(603,417)},.25),('bow_draw',2,{'grip':(1107,231),'belly':(1127,231),'string':(900,231),'top':(1022,55),'bottom':(1023,418)},.25),('bow_release',3,{'grip':(1480,232),'belly':(1498,232),'string':(1395,232),'top':(1396,55),'bottom':(1395,416)},.25),('quiver',4,{'back':(1804,263)},.20),('arrow',5,{'tail':(46,618),'tip':(423,619)},.24),('white_a',6,{'centre':(608,613)},.4),('white_b',7,{'centre':(975,615)},.4),('skill_slash',8,{'centre':(1389,614)},.4),('skill_arrow',9,{'tail':(1634,618),'tip':(1947,618)},.32)]
weapon_crops=[(30,70,430,475),(560,0,770,460),(860,0,1250,460),(1345,0,1550,460),(1680,40,1920,465),(20,565,440,665),(470,490,750,730),(785,480,1160,755),(1190,480,1580,755),(1600,560,1975,675)]
for name,i,p,s in W:
 if name not in ['white_a','white_b','skill_slash']:piece('weapons',i,5,2,name,p,s,weapon_crops[i])
# Normalize weapon dimensions against logical H=96 (source H=192).
def resize_asset(id,factor):
 im=Image.open(BASE/(id+'.png'));e=assets[id]
 save(id,im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS),{k:[x*factor for x in v] for k,v in e['anchors'].items()},e['source'])
im=Image.open(BASE/'sword.png');a=np.array(im);yy,xx=np.where(a[:,:,3]>127);gp=np.array(assets['sword']['anchors']['grip']);tp=np.array(assets['sword']['anchors']['tip']);u=(tp-gp)/np.linalg.norm(tp-gp);axis=np.column_stack([xx,yy])@u
resize_asset('sword',(.775*192)/(axis.max()-axis.min()))
for id in ['bow_idle','bow_release']:resize_asset(id,185/Image.open(BASE/(id+'.png')).height)
for id in ['arrow','skill_arrow']:resize_asset(id,123/Image.open(BASE/(id+'.png')).width)
# Arrow artwork axes are baked before runtime. All variants share the same tail.
def arrow_variant(source,id,angle):
 im=Image.open(BASE/(source+'.png'));e=assets[source];tail=np.array(e['anchors']['tail']);tip=np.array(e['anchors']['tip']);old=math.degrees(math.atan2(*(tip-tail)[::-1]));C=np.array([32.,64.]);length=math.dist(tail,tip)
 canvas=Image.new('RGBA',(256,128));canvas.alpha_composite(im,(round(C[0]-tail[0]),round(C[1]-tail[1])));canvas=canvas.rotate(-(angle-old),Image.Resampling.BICUBIC,center=tuple(C));u=np.array([math.cos(math.radians(angle)),math.sin(math.radians(angle))])
 save(id,canvas,{'tail':list(C),'tip':list(C+length*u)},{'sheet':'weapons','arrow_source':source,'offline_angle':angle})
def calibrate_canonical_arrow(id):
 # Fit the actual painted shaft, not the old approximate tail/point registration.
 for iteration in range(2):
  im=Image.open(BASE/(id+'.png'));ar=np.array(im);r,g,b=ar[:,:,:3].astype(int).transpose(2,0,1);yy,xx=np.indices(ar.shape[:2]);e=assets[id];tail=np.array(e['anchors']['tail']);tip=np.array(e['anchors']['tip']);mask=(xx>tail[0]+.22*(tip[0]-tail[0]))&(xx<tail[0]+.74*(tip[0]-tail[0]))&(ar[:,:,3]>127)
  color=((r>205)&(g>220)&(b>230)) if id=='skill_arrow' else ((r>45)&(r-g>10)&(g-b>5)&(b<170))
  y,x=np.where(mask&color);assert len(x)>20
  m,c=np.polyfit(x,y,1);theta=math.atan(m);C=tail;T=np.array([tail[0],m*tail[0]+c]);co=math.cos(theta);si=math.sin(theta)
  coefficients=(co,-si,T[0]-co*C[0]+si*C[1],si,co,T[1]-si*C[0]-co*C[1])
  corrected=im.transform(im.size,Image.Transform.AFFINE,coefficients,Image.Resampling.BICUBIC)
  source=dict(e['source']);source['shaft_calibration_iteration']=iteration;source['measured_slope_before']=float(m);source['measured_tail_dy_before']=float(T[1]-C[1])
  save(id,corrected,e['anchors'],source)
arrow_variant('arrow','arrow',0)
arrow_variant('skill_arrow','skill_arrow',0)
calibrate_canonical_arrow('arrow')
calibrate_canonical_arrow('skill_arrow')
for body_id in [15,16]:
 bp=assets[f'body_{body_id}']['anchors'];v=np.array(bp['far_hand'])-bp['near_hand'];angle=math.degrees(math.atan2(v[1],v[0]));arrow_variant('arrow',f'arrow_draw_{body_id}',angle)
# Use only the clean idle bow wood for all three phases: the generated drawn
# source contained a baked arrow and is retained as source, never used directly.
bow=Image.open(BASE/'bow_idle.png');p=assets['bow_idle']['anchors'];a=np.array(bow)
yy,xx=np.indices(a.shape[:2]);top=p['top'][1];bottom=p['bottom'][1]
curve=p['top'][0]+(p['grip'][0]-p['top'][0])*np.sin(np.clip((yy-top)/(bottom-top),0,1)*math.pi)
a[(xx<curve-5)&(yy>top+5)&(yy<bottom-5)]=0
bow=Image.fromarray(a)
save('bow_draw',bow,p,'clean own idle bow wood; no baked arrow')
# Two draw phases share wood silhouette but have individually registered V strings.
for body_id in [15,16]:
 original=Image.open(BASE/'bow_draw.png');p=dict(assets['bow_draw']['anchors']);bp=assets[f'body_{body_id}']['anchors']
 dx=bp['near_hand'][0]-bp['far_hand'][0];dy=bp['near_hand'][1]-bp['far_hand'][1]
 # Canvas large enough to contain string pulled to the actual near hand.
 shift=max(0,math.ceil(-(p['grip'][0]+dx))+4)
 canvas=Image.new('RGBA',(original.width+shift,original.height+20));canvas.alpha_composite(original,(shift,10))
 a=np.array(canvas);light=(a[:,:,0]>150)&(a[:,:,1]>140)&(a[:,:,2]>110)&(np.max(a[:,:,:3],axis=2)-np.min(a[:,:,:3],axis=2)<90)
 # Remove old pale string only left of wood, retain the brown bow body.
 gx=p['grip'][0]+shift
 xx=np.indices(a.shape[:2])[1];a[light&(xx<gx-5)]=0
 canvas=Image.fromarray(a);p={k:[v[0]+shift,v[1]+10] for k,v in p.items()};p['string']=[p['grip'][0]+dx,p['grip'][1]+dy]
 ImageDraw.Draw(canvas).line([tuple(p['top']),tuple(p['string']),tuple(p['bottom'])],fill='#EAD8B8',width=2)
 save(f'bow_draw_{body_id}',canvas,p,'own bow source, V-string to measured near hand')
# Bake held sword and bow directions once in tools, never at runtime.
def held_variant(source,id,angle):
 im=Image.open(BASE/(source+'.png'));e=assets[source];g=np.array(e['anchors']['grip']);centre=np.array([192.,192.])
 old=math.degrees(math.atan2(*(np.array(e['anchors']['tip'])-g)[::-1])) if source=='sword' else 0
 turn=angle-old;r=math.radians(turn);rot=np.array([[math.cos(r),-math.sin(r)],[math.sin(r),math.cos(r)]])
 canvas=Image.new('RGBA',(384,384));canvas.alpha_composite(im,(round(192-g[0]),round(192-g[1])));canvas=canvas.rotate(-turn,Image.Resampling.BICUBIC,center=(192,192))
 save(id,canvas,{k:list(centre+rot@(np.array(v)-g)) for k,v in e['anchors'].items()},'own held weapon offline bake')
probe=Image.open(BASE/'sword.png');pg=np.array(assets['sword']['anchors']['grip']);pt=np.array(assets['sword']['anchors']['tip']);pa=math.degrees(math.atan2(*(pt-pg)[::-1]));canvas=Image.new('RGBA',(384,384));canvas.alpha_composite(probe,(round(192-pg[0]),round(192-pg[1])));canvas=canvas.rotate(-(160-pa),Image.Resampling.BICUBIC,center=(192,192));bb=canvas.getbbox();factor=(.765*192)/max(bb[2]-bb[0],bb[3]-bb[1]);resize_asset('sword',factor)
held_variant('sword','sword_hold',160)
held_variant('sword','sword_run',163)
held_variant('bow_idle','bow_hold',20)
# NEW compact painted VFX. Full held swords are never reused by an attack.
raw=Image.open(SRC/'compact_swings_50.png')
fragment=key(raw.crop((110,335,345,425)));bb=fragment.getbbox();fragment=fragment.crop(bb)
fg=np.array([163-(110+bb[0]),386-(335+bb[1])],float);ft=np.array([318-(110+bb[0]),362-(335+bb[1])],float)
factor=70/fragment.width;fragment=fragment.resize((round(fragment.width*factor),round(fragment.height*factor)),Image.Resampling.LANCZOS);fg*=factor;ft*=factor
# Bake the small fragment horizontally; this is not the normal long held sword.
C=np.array([192.,160.]);base=Image.new('RGBA',(512,384));base.alpha_composite(fragment,(round(C[0]-fg[0]),round(C[1]-fg[1])))
angle=math.degrees(math.atan2(ft[1]-fg[1],ft[0]-fg[0]));base=base.rotate(angle,Image.Resampling.BICUBIC,center=tuple(C));tip=C+np.array([math.dist(fg,ft),0.])
points={'grip':list(C),'tip':list(tip)}
save('attack_fragment',base,points,{'sheet':'compact_swings_50','crop':[110,335,345,425],'short_width_source':70,'offline_angle':angle})
boxes=[(100,260,370,500),(435,250,750,520),(820,220,1320,570),(1320,260,1810,550),(1820,280,2150,500)]
grips=[(163,386),(545,394),(948,393),(1477,392),(1932,391)]
weapon_poly=[(-55,-25),(12,-30),(20,-42),(40,-42),(45,-24),(155,-37),(177,-27),(161,-13),(45,14),(40,27),(23,27),(18,14),(-55,18)]
curves={}
for i in [1,2,3]:
 box=boxes[i];grip=np.array(grips[i],float)-box[:2];cut=key(raw.crop(box));remove=Image.new('L',cut.size);ImageDraw.Draw(remove).rectangle((grip[0]-65,grip[1]-45,grip[0]+178,grip[1]+35),fill=255)
 ar=np.array(cut);ar[np.array(remove)>0]=0;cut=Image.fromarray(ar)
 # Discard single-pixel sampling noise, retain the actual intentionally torn tails.
 labs,count=components(ar[:,:,3]>16);sizes=np.bincount(labs.ravel());sizes[0]=0
 ar[(sizes[labs]<5)]=0;cut=Image.fromarray(ar)
 width={1:146,2:222,3:212}[i];bb=cut.getbbox();factor=width/(bb[2]-bb[0]);sx=factor;sy=factor*{1:.70,2:.55,3:.55}[i]
 full=cut.resize((round(cut.width*sx),round(cut.height*sy)),Image.Resampling.LANCZOS)
 at=C-np.array([grip[0]*sx,grip[1]*sy])+np.array([0.,12.])
 canvas=Image.new('RGBA',(512,384));canvas.alpha_composite(full,(round(at[0]),round(at[1])))
 if i==3:
  ar=np.array(canvas);ar[:,:,3]=(ar[:,:,3]*.48).astype('uint8');canvas=Image.fromarray(ar)
 curves[i]=canvas
# A separately painted short torn tip, plus a small backward sweep for the hold beat.
surge=key(raw.crop((1600,475,1690,520)));bb=surge.getbbox();surge=surge.crop(bb);surge=surge.resize((36,14),Image.Resampling.LANCZOS)
back=curves[1].crop(curves[1].getbbox());back=back.transpose(Image.Transpose.FLIP_LEFT_RIGHT).resize((48,22),Image.Resampling.LANCZOS)
def tinted(im,blue=False,alpha=1.):
 ar=np.array(im);rgb=ar[:,:,:3].astype(int);lit=(rgb.min(axis=2)>125)&(ar[:,:,3]>0)
 if blue:
  lum=rgb.mean(axis=2)/255
  ar[lit,0]=(70+180*lum[lit]**3).astype('uint8');ar[lit,1]=(190+65*lum[lit]).astype('uint8');ar[lit,2]=255
 ar[:,:,3]=(ar[:,:,3]*alpha).astype('uint8');ar[ar[:,:,3]==0,:3]=0
 return Image.fromarray(ar)
for prefix,blue in [('swing',False),('swing_skill',True)]:
 for i in range(5):
  vfx=curves.get(i,Image.new('RGBA',(512,384)))
  # A thicker halo uses the same painted contour rather than a larger detached shape.
  if blue and i in [1,2,3]:
   from PIL import ImageFilter
   halo=vfx.copy();ha=np.array(halo);ha[:,:,:3]=[55,170,255];ha[:,:,3]=np.array(vfx.getchannel('A').filter(ImageFilter.MaxFilter(3)))*.55;ha=ha.astype('uint8');halo=Image.fromarray(ha);halo.alpha_composite(tinted(vfx,True));vfx=halo
  else:vfx=tinted(vfx,blue)
  mask_id=f'{prefix}_mask_{i}';save(mask_id,vfx,points,{'sheet':'compact_swings_50','phase':i,'paint_layer':'curve','blue':blue})
  composite=Image.open(BASE/(mask_id+'.png')).copy();composite.alpha_composite(Image.open(BASE/'attack_fragment.png'))
  save(f'{prefix}_{i}',composite,points,{'sheet':'compact_swings_50','phase':i,'short_fragment':'attack_fragment'})
  assets[f'{prefix}_{i}'].update({'trail_mask':mask_id,'blade_asset':'attack_fragment','has_trail':i in [1,2,3],'pose_role':['guard','pull','sweep','hold','recover'][i]})
 for kind,i,small,pos,alpha in [('surge',2,surge,(168,-3),.88),('surge',3,surge,(117,5),.30),('reverse',3,back,(-64,8),.35)]:
  canvas=Image.new('RGBA',(512,384));canvas.alpha_composite(tinted(small,blue,alpha),(round(C[0]+pos[0]),round(C[1]+pos[1])))
  save(f'{prefix}_{kind}_{i}',canvas,points,{'sheet':'compact_swings_50','paint_layer':kind,'phase':i,'blue':blue})
parts={'schema':1,'status':'Lv1 unapproved','scale':.5,'levels':{'1':{'head':[f'head_{i}' for i in range(8)],'body':[f'body_{i}' for i in range(18)],'legs':[f'legs_{i}' for i in range(10)],'weapons':{'kiem':'sword_hold','cung':'bow_hold'},'run_weapon':'sword_run','combat_stance':'legs_guard','combat_lunge':'legs_lunge'}},'assets':assets,'references':[{'path':'art/reference/'+n,'sha256':hashlib.sha256((ROOT/'art/reference'/n).read_bytes()).hexdigest()} for n in ['chr_dbl_board_trang_bi.png','chr_dbl_board_animation.png','ref_dinh_bo_linh.png']]}
leg=assets['legs_0'];body=assets['body_0'];head=assets['head_0']
positions={};positions['legs_0']=-np.array(leg['anchors']['sole'])
hip=positions['legs_0']+leg['anchors']['hip'];positions['body_0']=hip-body['anchors']['hip'];neck=positions['body_0']+body['anchors']['neck'];positions['head_0']=neck-head['anchors']['neck']
ys=[]
for id,at in positions.items():
 bb=Image.open(BASE/(id+'.png')).getbbox();ys += [at[1]+bb[1],at[1]+bb[3]]
H=max(ys)-min(ys);bare=Image.open(BASE/'head_without_hat_0.png').getbbox();head_height=bare[3]-bare[1]
parts['presentation']={'standing_height_source':H,'standing_height_logic':H*.5,'head_without_hat_source':head_height,'head_ratio_target':.40,'head_ratio_measured':head_height/H,'display_height':128,'display_factor':128/(H*.5),'hat_excluded_asset':'head_without_hat_0'}
(DATA/'parts.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2)+'\n')
# Four entries per frame, independently composed registrations. Origins relative to feet.
combos=[(0,0,0),(1,1,0)]+[(0,2+i%3,1+i%5) for i in range(6)]+[(0,5,6),(4,6,7),(5,7,8),(6,8,9),(3,5,6),(2,5,6)]+[(7,b,l) for b,l in [(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(9,6),(10,6),(11,6),(12,6),(15,6),(16,6),(17,6)]]
# Attack14/15/16/17/18/19=body9..14;20/21/22=bowdraw/draw/release.
frames=[]
for i,(h,b,l) in enumerate(combos):
 layers={k:{'image':idx,'dx':0,'dy':0} for k,idx in [('head',h),('body',b),('legs',l),('weapon',0)]}
 if i==1:layers['body']['dy']=-1;layers['head']['dy']=-1
 if i in [14,15,16,17,18,19]:layers['legs']['stance']=True
 if i==16:layers['legs']['lunge']=True
 if i in list(range(8))+[12,13]:layers['body']['cung_image']=12
 frames.append({'id':i,'layers':layers,'attack':i>=14,'held_visible':i in list(range(8))+[12,13],'nocked':i in [20,21]})
(DATA/'frames30.json').write_text(json.dumps({'schema':1,'frames':frames,'clips':{'idle':{'frames':[0,1],'durations':[.6,.6],'loop':True},'run':{'frames':list(range(2,8)),'durations':[1/12]*6,'loop':True},'apex_flip':{'frames':list(range(8,12)),'durations':[.05]*4,'loop':False},'jump':{'frames':[12],'durations':[.38],'loop':False},'fall':{'frames':[13],'durations':[1/12],'loop':True}}},ensure_ascii=False,indent=2)+'\n')
effects={'schema':1,'palette_slots':{'lv1':{'core':'#FFFFFF','edge':'#E4EBF0'},'future_orange':{'core':'#FFF0C0','edge':'#FF8A30','status':'not_drawn'},'future_red':{'core':'#FFE0B0','edge':'#E54430','status':'not_drawn'}},'effects':{}}
for i in range(5):effects['effects'][f'swing_{i}']={'frames':[{'asset':f'swing_{i}','duration':.05,'anchor':'grip'}],'placement':'grip','z':6}
for i in range(5):effects['effects'][f'swing_skill_{i}']={'frames':[{'asset':f'swing_skill_{i}','duration':.05,'anchor':'grip'}],'placement':'grip','z':6}
for prefix in ['swing','swing_skill']:
 for kind,i in [('surge',2),('surge',3),('reverse',3)]:effects['effects'][f'{prefix}_{kind}_{i}']={'frames':[{'asset':f'{prefix}_{kind}_{i}','duration':.05}],'placement':'grip','z':7}
effects['effects']['bow_draw']={'frames':[{'asset':'bow_draw_15','duration':.1}],'placement':'far_hand','z':5}
effects['effects']['bow_draw_hold']={'frames':[{'asset':'bow_draw_16','duration':.1}],'placement':'far_hand','z':5}
effects['effects']['bow_release']={'frames':[{'asset':'bow_release','duration':.1}],'placement':'far_hand','z':5}
(DATA/'effects.json').write_text(json.dumps(effects,ensure_ascii=False,indent=2)+'\n')
def beat(frame,duration,fx=None,proj=None,nocked=False):return {'frame':frame,'duration':duration,'effects':fx or [],'projectile':proj,'nocked':nocked,'nocked_asset':('arrow_draw_15' if frame==20 else 'arrow_draw_16') if nocked else None}
slash=[beat(frame,d,[{'id':f'swing_{fx}','dx':0,'dy':0}]+([{'id':'swing_surge_2','dx':0,'dy':0}] if fx==2 else ([{'id':'swing_surge_3','dx':0,'dy':0},{'id':'swing_reverse_3','dx':0,'dy':0}] if fx==3 else []))) for frame,fx,d in [(14,0,.05),(15,1,.05),(16,2,.10),(16,3,.05),(17,4,.05)]]
shoot=[beat(20,.05,[{'id':'bow_draw','dx':0,'dy':0}],nocked=True),beat(20,.05,[{'id':'bow_draw','dx':0,'dy':0}],nocked=True),beat(21,.05,[{'id':'bow_draw_hold','dx':0,'dy':0}],nocked=True),beat(21,.05,[{'id':'bow_draw_hold','dx':0,'dy':0}],nocked=True),beat(22,.05,[{'id':'bow_release','dx':0,'dy':0}],{'id':'arrow','dx':0,'dy':0})]+[beat(22,.05,[{'id':'bow_release','dx':0,'dy':0}]) for _ in range(3)]
tram=json.loads(json.dumps(slash))
for b in tram:
 for fx in b['effects']:fx['id']=fx['id'].replace('swing_','swing_skill_')
xa=json.loads(json.dumps(shoot));xa[4]['projectile']['id']='skill_arrow'
skills={'schema':1,'skills':{}}
for id,school,beats in [('slash','kiem',slash),('shoot','cung',shoot),('tram_kiem','kiem',tram),('xa_tien','cung',xa)]:skills['skills'][id]={'school':school,'ground':beats,'air':[{**b,'frame':{14:23,15:24,16:25,17:26,20:27,21:28,22:29}.get(b['frame'],b['frame'])} for b in json.loads(json.dumps(beats))],'hit_window':[.1,.2] if school=='kiem' else None,'status':'visual prototype, gameplay numbers unchanged'}
(DATA/'skills.json').write_text(json.dumps(skills,ensure_ascii=False,indent=2)+'\n')
print(f'Lv1 built: head8 body18 legs10 common +2 combat stances; {len(assets)} transparent PNGs; frames30=30; skills4 ground+air. References never sliced into textures.')

# Remove obsolete displaced standalone-trail outputs from the previous prototype.
for i in range(5):
 for folder in [BASE,OUT]:
  for suffix in ['.png','.prompt.txt','.png.import']:
   old=folder/(f'trail_{i}'+suffix)
   if old.exists():old.unlink()

for folder in [BASE,OUT]:
 for suffix in ['.png','.prompt.txt','.png.import']:
  old=folder/('hat_art'+suffix)
  if old.exists():old.unlink()

for old_id in ['blade_'+str(i) for i in range(5)]+['white_a','white_b','skill_slash']:
 for folder in [BASE,OUT]:
  for suffix in ['.png','.prompt.txt','.png.import']:
   old=folder/(old_id+suffix)
   if old.exists():old.unlink()

# Apply the current source-number/paint-registration stage after rebuilding sheets.
from update_pose_playtest import main as register_playtest
register_playtest()
