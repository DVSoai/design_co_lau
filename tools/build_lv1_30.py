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
# Source-pixel registration; all output pixels are 2x logical scale.
heads=[(214,420),(596,421),(962,423),(1349,410),(85,746),(570,591),(1059,745),(1353,867)]
for i,n in enumerate(heads):
 # Upright idle head from source top124..436, registered neck420: top 284px => 68 output px.
 piece('heads',i,4,2,f'head_{i}',{'neck':n},68/284)
# neck, hip, near grip, far grip. Neck and hip are measured drawing landmarks, not grid centres.
A=[((275,65),(266,280),(405,305),(153,304)),((750,65),(750,280),(886,307),(640,306)),((1290,76),(1237,275),(1465,151),(1057,240)),((275,403),(240,590),(452,447),(67,586)),((797,414),(760,587),(953,523),(594,489)),((1280,404),(1240,589),(1083,542),(1450,469)),((415,837),(235,817),(294,764),(249,875)),((790,921),(785,737),(635,791),(914,787)),((1350,846),(1190,818),(1261,737),(1189,828))]
B=[((294,136),(277,309),(212,85),(446,317)),((803,147),(785,309),(729,52),(920,316)),((1260,146),(1240,307),(1481,201),(1200,254)),((267,428),(231,597),(343,627),(166,536)),((771,430),(749,595),(999,495),(665,543)),((1269,427),(1245,599),(1332,613),(1393,610)),((281,740),(274,925),(183,764),(478,783)),((796,745),(779,924),(689,765),(989,780)),((1300,744),(1286,926),(1139,755),(1490,790))]
for i,(n,h,g,f) in enumerate(A+B):
 scale=56/math.dist(n,h)
 piece('bodies_a' if i<9 else 'bodies_b',i if i<9 else i-9,3,3,f'body_{i}',{'neck':n,'hip':h,'grip':g,'far_hand':f,'near_hand':g,'back':(h[0]-70,h[1]-100)},scale)
# Legs source is1774x887.
legpoints=[((162,142),(180,392)),((520,148),(617,392)),((855,155),(803,390)),((1216,141),(1380,348)),((1590,150),(1694,383)),((194,552),(315,795)),((554,537),(503,738)),((879,554),(898,751)),((1224,755),(1240,535)),((1508,672),(1700,637))]
for i,(hip,sole) in enumerate(legpoints):
 piece('legs',i,5,2,f'legs_{i}',{'hip':hip,'sole':sole},68/math.dist(hip,sole))
# Three somersault leg images are baked offline from the tucked painting,
# around a fixed canvas pivot; no runtime rotation, no rescaling of anatomy.
base=Image.open(BASE/'legs_6.png');bp=assets['legs_6']['anchors']
for i,degrees in [(7,90),(8,180),(9,270)]:
 canvas=Image.new('RGBA',(192,192));hx,hy=bp['hip'];canvas.alpha_composite(base,(round(96-hx),round(96-hy)))
 canvas=canvas.rotate(-degrees,Image.Resampling.BICUBIC,center=(96,96))
 vx,vy=bp['sole'][0]-hx,bp['sole'][1]-hy;r=math.radians(degrees)
 save(f'legs_{i}',canvas,{'hip':[96,96],'sole':[96+vx*math.cos(r)-vy*math.sin(r),96+vx*math.sin(r)+vy*math.cos(r)]},'offline rotation of own legs painting')
# Weapon sheet1983x793. All points measured from its source, then normalized uniformly.
W=[('sword',0,{'grip':(137,352),'tip':(405,95)},.23),('bow_idle',1,{'grip':(692,232),'belly':(711,232),'string':(599,232),'top':(600,55),'bottom':(603,417)},.25),('bow_draw',2,{'grip':(1107,231),'belly':(1127,231),'string':(900,231),'top':(1022,55),'bottom':(1023,418)},.25),('bow_release',3,{'grip':(1480,232),'belly':(1498,232),'string':(1395,232),'top':(1396,55),'bottom':(1395,416)},.25),('quiver',4,{'back':(1804,263)},.20),('arrow',5,{'tail':(46,618),'tip':(423,619)},.24),('white_a',6,{'centre':(608,613)},.4),('white_b',7,{'centre':(975,615)},.4),('skill_slash',8,{'centre':(1389,614)},.4),('skill_arrow',9,{'tail':(1634,618),'tip':(1947,618)},.32)]
weapon_crops=[(30,70,430,475),(560,0,770,460),(860,0,1250,460),(1345,0,1550,460),(1680,40,1920,465),(20,565,440,665),(470,490,750,730),(785,480,1160,755),(1190,480,1580,755),(1600,560,1975,675)]
for name,i,p,s in W:piece('weapons',i,5,2,name,p,s,weapon_crops[i])
# Normalize weapon dimensions against logical H=96 (source H=192).
def resize_asset(id,factor):
 im=Image.open(BASE/(id+'.png'));e=assets[id]
 save(id,im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.LANCZOS),{k:[x*factor for x in v] for k,v in e['anchors'].items()},e['source'])
im=Image.open(BASE/'sword.png');a=np.array(im);yy,xx=np.where(a[:,:,3]>127);gp=np.array(assets['sword']['anchors']['grip']);tp=np.array(assets['sword']['anchors']['tip']);u=(tp-gp)/np.linalg.norm(tp-gp);axis=np.column_stack([xx,yy])@u
resize_asset('sword',(.775*192)/(axis.max()-axis.min()))
for id in ['bow_idle','bow_release']:resize_asset(id,72/Image.open(BASE/(id+'.png')).height)
for id in ['arrow','skill_arrow']:resize_asset(id,115/Image.open(BASE/(id+'.png')).width)
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
# Five unique combined swings: independently swept tip sectors for each beat.
# Preparation has no trail. These offline rasters are rendered as ONE centred image.
sword=Image.open(BASE/'sword.png');grip=assets['sword']['anchors']['grip'];tip=assets['sword']['anchors']['tip'];old=math.degrees(math.atan2(tip[1]-grip[1],tip[0]-grip[0]));length=math.dist(tip,grip)
for i,angle in enumerate([-75,-35,0,35,60]):
 centre=np.array([192.,192.]);canvas=Image.new('RGBA',(384,384));canvas.alpha_composite(sword,(round(192-grip[0]),round(192-grip[1])));canvas=canvas.rotate(-(angle-old),Image.Resampling.BICUBIC,center=(192,192))
 tp=centre+length*np.array([math.cos(math.radians(angle)),math.sin(math.radians(angle))])
 points={'grip':list(centre),'tip':list(tp)}
 save(f'blade_{i}',canvas,points,'offline rotation of own sword')
 trail=Image.new('RGBA',canvas.size)
 if i:
  # Independently authored curved sweeps with a sharp tip junction and tapering tail.
  reach,tail,depth=[(0,0,0),(22,92,72),(35,132,96),(42,116,84),(27,98,64)][i]
  def curve(p0,p1,p2,p3):
   return [(1-t)**3*np.array(p0)+3*(1-t)**2*t*np.array(p1)+3*(1-t)*t*t*np.array(p2)+t**3*np.array(p3) for t in np.linspace(0,1,90)]
  local=curve((length,0),(length+reach,-depth*.45),(length-tail*.4,-depth),(length-tail,-depth))
  local+=curve((length-tail,-depth),(length-tail*.35,-depth*.45),(length-12,-12),(length,0))
  r=math.radians(angle);rotation=np.array([[math.cos(r),-math.sin(r)],[math.sin(r),math.cos(r)]])
  polygon=[tuple((centre+rotation@v)*4) for v in local]
  big=Image.new('RGBA',(1536,1536));ImageDraw.Draw(big).polygon(polygon,fill='#FFFFFF')
  trail=big.resize((384,384),Image.Resampling.LANCZOS)
 save(f'swing_mask_{i}',trail,points,'own independently swept tip-sector mask')
 combined=trail.copy();combined.alpha_composite(canvas)
 save(f'swing_{i}',combined,points,'own sword + unique continuous white tip sweep; single runtime texture')
 assets[f'swing_{i}']['trail_mask']=f'swing_mask_{i}'
 assets[f'swing_{i}']['blade_asset']=f'blade_{i}'
 assets[f'swing_{i}']['has_trail']=bool(i)
 blue=np.array(trail);blue[:,:,:3]=[90,205,255];blue[blue[:,:,3]==0,:3]=0
 skill=Image.fromarray(blue);skill.alpha_composite(canvas)
 save(f'swing_skill_{i}',skill,points,'own sword + unique blue skill sweep; single runtime texture')
 assets[f'swing_skill_{i}'].update({'trail_mask':f'swing_mask_{i}','blade_asset':f'blade_{i}','has_trail':bool(i)})
parts={'schema':1,'status':'Lv1 unapproved','scale':.5,'levels':{'1':{'head':[f'head_{i}' for i in range(8)],'body':[f'body_{i}' for i in range(18)],'legs':[f'legs_{i}' for i in range(10)],'weapons':{'kiem':'sword','cung':'bow_idle'}}},'assets':assets,'references':[{'path':'art/reference/'+n,'sha256':hashlib.sha256((ROOT/'art/reference'/n).read_bytes()).hexdigest()} for n in ['chr_dbl_board_trang_bi.png','chr_dbl_board_animation.png','ref_dinh_bo_linh.png']]}
(DATA/'parts.json').write_text(json.dumps(parts,ensure_ascii=False,indent=2)+'\n')
# Four entries per frame, independently composed registrations. Origins relative to feet.
combos=[(0,0,0),(1,1,0)]+[(0,2+i%3,1+i%5) for i in range(6)]+[(0,5,6),(4,6,7),(5,7,8),(6,8,9),(3,5,6),(2,5,6)]+[(7,b,l) for b,l in [(9,0),(10,0),(11,0),(12,0),(13,0),(14,0),(15,0),(16,0),(17,0),(9,6),(10,6),(11,6),(12,6),(15,6),(16,6),(17,6)]]
# Attack14/15/16/17/18/19=body9..14;20/21/22=bowdraw/draw/release.
frames=[]
for i,(h,b,l) in enumerate(combos):
 layers={k:{'image':idx,'dx':0,'dy':0} for k,idx in [('head',h),('body',b),('legs',l),('weapon',0)]}
 if i==1:layers['body']['dy']=-1;layers['head']['dy']=-1
 frames.append({'id':i,'layers':layers,'attack':i>=14,'nocked':i in [20,21]})
(DATA/'frames30.json').write_text(json.dumps({'schema':1,'frames':frames,'clips':{'idle':{'frames':[0,1],'durations':[.6,.6],'loop':True},'run':{'frames':list(range(2,8)),'durations':[1/12]*6,'loop':True},'apex_flip':{'frames':list(range(8,12)),'durations':[.05]*4,'loop':False},'jump':{'frames':[12],'durations':[.38],'loop':False},'fall':{'frames':[13],'durations':[1/12],'loop':True}}},ensure_ascii=False,indent=2)+'\n')
effects={'schema':1,'effects':{}}
for i in range(5):effects['effects'][f'swing_{i}']={'frames':[{'asset':f'swing_{i}','duration':.05,'anchor':'grip'}],'placement':'grip','z':6}
for i in range(5):effects['effects'][f'swing_skill_{i}']={'frames':[{'asset':f'swing_skill_{i}','duration':.05,'anchor':'grip'}],'placement':'grip','z':6}
effects['effects']['tram_kiem']={'frames':[{'asset':'skill_slash','duration':.05,'dx':j*3,'dy':0} for j in range(4)],'placement':'centre','z':8}
effects['effects']['bow_draw']={'frames':[{'asset':'bow_draw_15','duration':.1}],'placement':'far_hand','z':5}
effects['effects']['bow_draw_hold']={'frames':[{'asset':'bow_draw_16','duration':.1}],'placement':'far_hand','z':5}
effects['effects']['bow_release']={'frames':[{'asset':'bow_release','duration':.1}],'placement':'far_hand','z':5}
(DATA/'effects.json').write_text(json.dumps(effects,ensure_ascii=False,indent=2)+'\n')
def beat(frame,duration,fx=None,proj=None,nocked=False):return {'frame':frame,'duration':duration,'effects':fx or [],'projectile':proj,'nocked':nocked}
slash=[beat([14,15,16,16,16][i],dur,[{'id':f'swing_{i}','dx':0,'dy':0}]) for i,dur in enumerate([.05,.05,.075,.075,.05])]
shoot=[beat(20,.1,[{'id':'bow_draw','dx':0,'dy':0}],nocked=True),beat(21,.1,[{'id':'bow_draw_hold','dx':0,'dy':0}],nocked=True),beat(22,.1,[{'id':'bow_release','dx':0,'dy':0}],{'id':'arrow','dx':0,'dy':0})]
tram=json.loads(json.dumps(slash))
for i,b in enumerate(tram):
 b['effects']=[{'id':f'swing_skill_{i}','dx':0,'dy':0}]
xa=json.loads(json.dumps(shoot));xa[-1]['projectile']['id']='skill_arrow'
skills={'schema':1,'skills':{}}
for id,school,beats in [('slash','kiem',slash),('shoot','cung',shoot),('tram_kiem','kiem',tram),('xa_tien','cung',xa)]:skills['skills'][id]={'school':school,'ground':beats,'air':[{**b,'frame':{14:23,15:24,16:25,17:26,20:27,21:28,22:29}.get(b['frame'],b['frame'])} for b in json.loads(json.dumps(beats))],'hit_window':[.1,.2] if school=='kiem' else None,'status':'visual prototype, gameplay numbers unchanged'}
(DATA/'skills.json').write_text(json.dumps(skills,ensure_ascii=False,indent=2)+'\n')
print(f'Lv1 built: head8 body18 legs10; {len(assets)} transparent PNGs; frames30=30; skills4 ground+air. References never sliced into textures.')

# Remove obsolete displaced standalone-trail outputs from the previous prototype.
for i in range(5):
 for folder in [BASE,OUT]:
  for suffix in ['.png','.prompt.txt','.png.import']:
   old=folder/(f'trail_{i}'+suffix)
   if old.exists():old.unlink()
