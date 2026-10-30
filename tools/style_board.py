#!/usr/bin/env python3
"""Build style review from real generated PNGs only. No image generation here.
Source and manual landmarks are retained; uniform scaling never alters proportions.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];S=R/'art/concept/style_v2';OUT=R/'docs/reports';CUT=S/'cut'
POSES=['idle','run','raise','slash','bow','face']
BG=(36,48,59);EARTH=(125,85,55) # project clear color & dao_uc_world.gd COLORS['#']
BASE=[f'v{i}_{v}' for i in [1,2,3] for v in 'abc'];EXTRA=['v1_c_r1','v2_c_r1']
def font(size):return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',size)
def key(image):
 a=np.asarray(image.convert('RGBA')).copy();rgb=a[:,:,:3].astype(float);other=np.maximum(rgb[:,:,0],rgb[:,:,2]);excess=rgb[:,:,1]-other
 alpha=np.clip(1-(excess-16)/100,0,1);alpha[excess>100]=0
 rgb[:,:,1]=np.minimum(rgb[:,:,1],other);a[:,:,:3]=np.rint(rgb).astype('uint8');a[:,:,3]=np.rint(alpha*255).astype('uint8');a[a[:,:,3]==0]=0
 return a
def label_mask(image):
 a=np.asarray(image.convert('RGB')).astype(int)
 return ~((a[:,:,1]>a[:,:,0]+40)&(a[:,:,1]>a[:,:,2]+40))
def crop_layer(image,ids,split=None,index=None):
 a=key(image);labels,n=ndimage.label(label_mask(image));mask=np.isin(labels,ids if isinstance(ids,list) else [ids])
 if split and index in [2,3]:
  yy,xx=np.indices(mask.shape);line=np.interp(yy,[split['y_upper'],split['y_lower']],[split['upper_x'],split['lower_x']]);mask&=(xx<line) if index==2 else (xx>=line)
 mask=ndimage.binary_dilation(mask,iterations=2);ys,xs=np.where(mask);box=(max(0,int(xs.min())),max(0,int(ys.min())),min(image.width,int(xs.max())+1),min(image.height,int(ys.max())+1))
 a[~mask]=0;part=Image.fromarray(a).crop(box);return part,box

def paste_character(canvas,image,box,top,sole,xcentre,ground,target):
 # Human landmark span, not blade/arc bounding box, sets display scale.
 factor=target/(sole-top);w=max(1,round(image.width*factor));h=max(1,round(image.height*factor));scaled=image.resize((w,h),Image.Resampling.LANCZOS)
 a=np.array(scaled);visible=a[:,:,3]>0;a[:,:,1][visible]=np.minimum(a[:,:,1][visible],np.maximum(a[:,:,0][visible],a[:,:,2][visible]));a[~visible]=0;scaled=Image.fromarray(a)
 y=round(ground-(sole-box[1])*factor);x=round(xcentre-w/2)
 canvas.alpha_composite(scaled,(x,y));return {'source_box':box,'human_top_y':top,'sole_y':sole,'source_human_height':sole-top,'target_human_height':target,'scale':factor,'display_size':[w,h],'paste':[x,y]}

def main():
 OUT.mkdir(exist_ok=True);CUT.mkdir(exist_ok=True);regions=json.loads((S/'regions.json').read_text());crops={};info={}
 for name in BASE+EXTRA:
  source=Image.open(S/(name+'.png'));e=regions[name];crops[name]=[]
  for i,id in enumerate(e['components']):
   part,box=crop_layer(source,id,e.get('touching_split'),i);part.save(CUT/(name+'_'+POSES[i]+'.png'));crops[name].append((part,box))
  human=e['sole_y'][0]-e['human_top_y'][0];head=e['idle_chin_y']-e['human_top_y'][0];ratio=human/head
  info[name]={'source_size':list(source.size),'source_sha256':hashlib.sha256((S/(name+'.png')).read_bytes()).hexdigest(),'source_height_idle':human,'head_including_bun':head,'measured_heads_tall':ratio,'target_heads_tall':{'1':3,'2':3.5,'3':4}[name[1]],'display':{}}
  # Three shin rows: horizontal dark-edge run is a disclosed local probe,
  # not a proof of uniform stroke width around the entire silhouette.
  idle=np.array(crops[name][0][0]);box=crops[name][0][1];runs=[];probes=[]
  for fraction in [.80,.84,.88]:
   y=round(e['human_top_y'][0]+human*fraction)-box[1];xs=np.where(idle[y,:,3]>127)[0];run=0
   for x in range(int(xs.min()),int(xs.max())+1):
    if idle[y,x,3]>127 and idle[y,x,:3].max()<100:run+=1
    else:break
   runs.append(run);probes.append(y+box[1])
  info[name]['outline_probe']={'method':'leading dark run along3 horizontal shin rows, alpha>127/maxRGB<100; projected width only, not global uniformity','source_rows':probes,'runs_px':runs,'median_px':float(np.median(runs)),'fraction_of_idle_height':float(np.median(runs))/human}

 # Actual project reference side view, not generated again.
 ref_source=Image.open(R/'art/reference/ref_dinh_bo_linh.png').crop((610,20,780,570));ref=Image.fromarray(key(ref_source));ref=ref.crop(ref.getbbox());ref.save(CUT/'reference_v9_side.png')
 names=BASE+EXTRA;row_h=300;header=55;width=2220;board=Image.new('RGBA',(width,header+row_h*len(names)),BG+(255,));draw=ImageDraw.Draw(board)
 draw.text((15,12),'STYLE V2 | source keyed + 5 poses at 160px / 96px | v9 160px | originals9 + replacements2',font=font(22),fill='white')
 for row,name in enumerate(names):
  y=header+row*row_h;ground=y+253;draw.rectangle((300,ground,width,y+row_h-1),fill=EARTH)
  e=regions[name];draw.text((10,y+8),f'{name}  {info[name]["measured_heads_tall"]:.2f} heads (manual)',font=font(17),fill='white')
  source=Image.fromarray(key(Image.open(S/(name+'.png'))));source.thumbnail((280,100),Image.Resampling.LANCZOS);board.alpha_composite(source,(10,y+38))
  face=crops[name][5][0].copy();face.thumbnail((100,115),Image.Resampling.LANCZOS);board.alpha_composite(face,(95,y+157))
  draw.text((12,y+row_h-22),'source keyed / face',font=font(14),fill='white')
  for i in range(5):
   part,box=crops[name][i];cell_x=300+i*350
   draw.text((cell_x+12,y+14),POSES[i]+' 160 / 96',font=font(17),fill='white')
   for target,centre in [(160,cell_x+105),(96,cell_x+280)]:
    desc=paste_character(board,part,box,e['human_top_y'][i],e['sole_y'][i],centre,ground,target)
    info[name]['display'][POSES[i]+'_'+str(target)]=desc
  vr=ref.resize((round(ref.width*160/ref.height),160),Image.Resampling.LANCZOS);board.alpha_composite(vr,(2080,ground-160));draw.text((2070,y+14),'v9 160',font=font(18),fill='white')
 board.convert('RGB').save(OUT/'style_v2_board.png')
 # Exactly9 choices, with explicit replacement ids in the two original positions.
 choices=[n+'_r1' if n in ['v1_c','v2_c'] else n for n in BASE];quick=Image.new('RGBA',(9*180,260),BG+(255,));d=ImageDraw.Draw(quick);d.rectangle((0,225,quick.width,259),fill=EARTH)
 for i,n in enumerate(choices):
  part,box=crops[n][0];e=regions[n];paste_character(quick,part,box,e['human_top_y'][0],e['sole_y'][0],i*180+90,225,160);d.text((i*180+9,15),n,font=font(19),fill='white');d.text((i*180+40,239),'160 px',font=font(13),fill='white')
 quick.convert('RGB').save(OUT/'style_v2_160.png')
 (S/'measurements.json').write_text(json.dumps({'method':'Manual source landmarks, uniform LANCZOS downsample; blade/arc excess kept; no redraw/rotation/shape edits','background_sources':{'sky':'prototype/project.godot environment/defaults/default_clear_color','earth':'prototype/dao_uc/dao_uc_world.gd COLORS #'},'original_count':9,'replacement_count':2,'quick_choices':choices,'images':info},indent=2)+'\n')
 print(f'Original sheets={len(BASE)}; replacement sheets={len(EXTRA)}; total={len(names)}; retained all originals')
 print(f'Transparent extracted PNGs={len(list(CUT.glob("*.png")))}; 5poses+face per sheet, plus reference')
 print(f'style_v2_board.png {board.width}x{board.height}; rows={len(names)}; human spans160/96px from recorded source landmarks')
 print(f'style_v2_160.png {quick.width}x{quick.height}; choices9 at human height160; ids={choices}')
 for n in names:print(f'{n}: source={info[n]["source_size"]}; idle_h={info[n]["source_height_idle"]}; head+bun={info[n]["head_including_bun"]}; measured={info[n]["measured_heads_tall"]:.4f} heads; requested={info[n]["target_heads_tall"]}')
 for n in names:print(n,'shin outline probe',info[n]['outline_probe'])
 print('No imagegen used for board/labels/comparison; only real source PNGs cropped/keyed/scaled/composited by this script. Raster PNG concept, not editable SVG.')
if __name__=='__main__':main()
