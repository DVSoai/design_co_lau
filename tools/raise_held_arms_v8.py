#!/usr/bin/env python3
"""Draw only the authorized front arm, preserving every pixel outside its ROI."""
from pathlib import Path
import json,copy,subprocess
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'prototype/pose_rig/data';ART=R/'prototype/pose_rig/art/lv1_30';OUT=R/'art/sprites/characters/lv1_30';SRC=OUT/'sources'
def run():
    p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text())
    for base in ['chest_stand']+[f'chest_run_{i}' for i in range(6)]+['chest_fall']:
        a=copy.deepcopy(p['assets'][base]);old=Image.open(ART/a['file']).convert('RGBA');arr=np.array(old)
        nx,ny=a['anchors']['neck'];gx,gy=a['anchors']['grip'];gy-=10
        yy,xx=np.indices(arr.shape[:2]);edge=nx+12+np.maximum(0,yy-ny-16)*.20
        roi=(xx>=edge)&(yy>=ny-20)&(yy<ny+44)&(xx<gx+18)
        # Forearm curls up from the original shoulder seam; palette sampled from own Lv1.
        s=f'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="256" viewBox="0 0 320 256"><g stroke="#2b1b12" stroke-width="1.7" stroke-linejoin="round">'
        s+=f'<path d="M{nx+11} {ny+10} Q{nx+19} {ny+12} {gx-10} {ny+25} Q{gx-4} {ny+32} {gx+3} {ny+28} Q{gx+9} {ny+23} {gx+5} {gy+6} L{gx-4} {gy+5} L{gx-7} {ny+21} Q{nx+18} {ny+15} {nx+13} {ny+12} Z" fill="#ec984e"/>'
        s+=f'<path d="M{nx+14} {ny+13} Q{nx+22} {ny+15} {gx-10} {ny+24} Q{gx-4} {ny+28} {gx+1} {ny+25} L{gx+2} {gy+9} L{gx-2} {gy+8} L{gx-5} {ny+21} Z" fill="#ffc076" stroke="none"/>'
        s+=f'<path d="M{gx-5.5} {gy+5} L{gx+5.5} {gy+6} L{gx+6} {gy+16} L{gx-5} {gy+15} Z" fill="#724330"/>'
        s+=f'<path d="M{gx-3.5} {gy+7} L{gx+3.5} {gy+8} L{gx+4} {gy+13} L{gx-3} {gy+12} Z" fill="#a2673b" stroke="none"/>'
        for i in [8,11,14]:s+=f'<path d="M{gx-4} {gy+i} L{gx+4.5} {gy+i+1}" fill="none" stroke="#462b20" stroke-width=".65"/>'
        s+=f'<path d="M{gx-6} {gy+3} Q{gx-8} {gy-2} {gx-3} {gy-6} Q{gx} {gy-8} {gx+3} {gy-4} L{gx+6} {gy-2} Q{gx+8} {gy+2} {gx+4} {gy+5} L{gx-1} {gy+6} Z" fill="#ffb767"/>'
        s+=f'<path d="M{gx-3} {gy-3} L{gx+1} {gy+1} M{gx} {gy-5} L{gx+4} {gy-1} M{gx-5} {gy+1} Q{gx-1} {gy-1} {gx+2} {gy+3}" stroke-width=".7" fill="none"/>'
        s+='</g></svg>'
        id=base+'_raised_v8';svg=SRC/(id+'.svg');svg.write_text(s);tmp=Path('/tmp')/(id+'.png')
        subprocess.run(['inkscape',str(svg),'--export-type=png','--export-filename='+str(tmp),'--export-width=1280'],check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        arm=Image.open(tmp).convert('RGBA').resize(old.size,Image.Resampling.LANCZOS);new=np.array(arm);arr[roi]=0
        # Restrict modifications exactly to the authorized arm region, including its raised fist.
        new[~roi]=0;im=Image.fromarray(arr);im.alpha_composite(Image.fromarray(new));result=np.array(im)
        assert np.array_equal(result[~roi],np.array(old)[~roi])
        for folder in [ART,OUT]:im.save(folder/(id+'.png'))
        Image.fromarray((roi*255).astype('uint8')).save(SRC/(id+'_roi.png'))
        skin=(result[:,:,3]>127)&(result[:,:,0]>=200)&(result[:,:,1]>=100)&(result[:,:,2]>=45)&((xx-gx)**2+(yy-gy)**2<=64)&(yy<=gy+4)
        sy,sx=np.where(skin);palm=[float(sx.mean())+.5,float(sy.mean())+.5]
        a['file']=id+'.png';a['anchors']['grip']=palm;a['anchors']['near_hand']=palm;a['source']={'own_base':base,'authorized_front_arm_only':True,'palm_shift_source_px':[0,-10],'svg':str(svg.relative_to(R)),'roi':str((SRC/(id+'_roi.png')).relative_to(R))};p['assets'][id]=a
        (OUT/(id+'.prompt.txt')).write_text('User-authorized front-arm-only SVG edit; exact drawing in sources/'+id+'.svg; unchanged pixels outside saved ROI. Original own torso '+base+'; palm raised10 source pixels.\n')
    for frame in [0,1,2,3,4,5,6,7,12,21]:
        row=f['frames'][frame];base='chest_stand' if frame in [0,1] else ('chest_fall' if frame in [12,21] else f'chest_run_{frame-2}')
        row['layers']['body']['asset']=base+'_raised_v8';row['layers']['body']['cung_asset']=base+'_raised_v8'
    for name,data in [('parts',p),('frames30',f)]:(D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Raised only front arm in held frames0–7,12,21, both schools; other-arm, torso and all outside-ROI pixels identical.')
if __name__=='__main__':run()
