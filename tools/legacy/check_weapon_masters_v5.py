#!/usr/bin/env python3
"""Measure real master/runtime PNGs and real H128 Godot GPU contour pixels."""
from pathlib import Path
import json,subprocess,sys
import numpy as np
from PIL import Image
from build_carry_v4 import position
from held_weapon_pose import hand_key
from weapon_v5_scope import RETIRED,REPAINTED,HELD,frame_without_weapon,asset_is_unchanged

R=Path(__file__).resolve().parents[2];D=R/'prototype/pose_rig/data';ART=R/'prototype/pose_rig/art/lv1_30';OUT=R/'art/sprites/weapons/lv1';REPORT=R/'prototype/pose_rig/reports'
p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text());H=p['presentation']['standing_height_source'];fail=0
def check(ok,message):
    global fail
    print(('PASS: ' if ok else 'FAIL: ')+message);fail+=not ok
def rgba(path):return np.array(Image.open(path).convert('RGBA'))
def old(path):return subprocess.check_output(['git','show','ae1327c:'+path],cwd=R)
old_f=json.loads(old('prototype/pose_rig/data/frames30.json'));old_p=json.loads(old('prototype/pose_rig/data/parts.json'))
check(all(frame_without_weapon(row)==frame_without_weapon(old_f['frames'][i]) for i,row in enumerate(f['frames'])),'all30 anatomy/source frame rows unchanged; only held weapon registration/depth changed')
check(all(asset_is_unchanged(k,v,p['assets']) for k,v in old_p['assets'].items()),'only explicit old held variants retired and12 action blade composites repainted; all other asset metadata unchanged')
check(p['levels']['1']['run_weapon']==p['levels']['1']['weapons']['kiem'],'run weapon alias is the SAME canonical sword asset')
for id in sorted(RETIRED):
    check(id not in p['assets'] and not (ART/(id+'.png')).exists() and not (R/'art/sprites/characters/lv1_30'/(id+'.png')).exists(),'obsolete held texture physically removed: '+id)
for school in ['kiem','cung']:
    id=p['levels']['1']['weapons'][school];a=p['assets'][id];image=rgba(ART/a['file']);master=rgba(OUT/(school+'_lv1_master.png'))
    check(max(master.shape[:2])==512 and np.any(master[:,:,3]==0) and np.any(master[:,:,3]>=250),school+' master has512px long side, real transparency and opaque painted core')
    check((ART/a['file']).read_bytes()==(OUT/(school+'_lv1.png')).read_bytes(),school+' engine texture is byte-identical to canonical exported sprite')
    alpha=image[:,:,3];ys,xs=np.where(alpha>0);span=max(np.ptp(xs)+1,np.ptp(ys)+1)
    if school=='cung':
        axis=np.array(a['anchors']['top'])-a['anchors']['bottom'];axis/=np.linalg.norm(axis);ys,xs=np.where(alpha>=128);span=np.ptp(np.column_stack([xs,ys])@axis)+1
    ratio=span/H;check((.75<=ratio<=.8) if school=='kiem' else (.9<=ratio<=1),f'{school} real opaque span/H={ratio:.9f}; sword longest alpha side, bow opaque axial span')
    grip=np.array(a['anchors']['grip']);sample=image[round(grip[1]),round(grip[0])];check(sample[3]>=230 and sample[0]>=80,f'{school} middle cord/leather grip at actual RGBA={sample.tolist()}')
    for frame in HELD:
        row=f['frames'][frame];check('cung_asset' not in row['layers']['weapon'],f'{school} frame{frame}: no per-frame texture override')
        bid=row['layers']['body'].get('cung_asset' if school=='cung' else 'asset',p['levels']['1']['body'][row['layers']['body'].get('cung_image',row['layers']['body']['image']) if school=='cung' else row['layers']['body']['image']])
        ba=p['assets'][bid]['anchors'];key=hand_key(row,school,ba)
        hand=position(f,row,school,'body')+np.array(ba[key])*.5;placed=position(f,row,school,'weapon')+grip*.5;gap=np.linalg.norm(hand-placed)
        check(gap<=1,f'{school} frame{frame} grip-to-painted-hand={gap:.9f}logic px')
        print(f'PLACEMENT {school} frame{frame}: source [image,dx,dy]={row["reference"]["vu_khi"]}; own_registration={row["registrations"][school]["weapon"]}; own_top_left={position(f,row,school,"weapon").tolist()}; shared_texture={a["file"]}')
    rr,gg,bb=image[:,:,:3].astype(int).transpose(2,0,1);opaque=alpha>=204
    bright=opaque&(rr>190)&(gg>190)&(bb>190);dark=opaque&(rr<80)&(gg<70)&(bb<70);brass=opaque&(rr>150)&(gg>90)&(gg<225)&(bb<160)
    check(dark.sum()>=30 and brass.sum()>=8,f'{school} dark outline pixels={dark.sum()}; brass cap/guard pixels={brass.sum()}')
    if school=='kiem':
        steel_shadow=opaque&(rr>=70)&(rr<180)&(bb>rr+5);red=opaque&(rr>150)&(gg<95)&(bb<95)
        check(bright.sum()>=25 and steel_shadow.sum()>=25 and red.sum()>=8,f'held sword bright/reflected steel={bright.sum()}, blue-grey shadow steel={steel_shadow.sum()}, red tassel={red.sum()} real opaque pixels')
    else:check(bright.sum()>=30,f'held bow WHITE STRING opaque light pixels={bright.sum()}')
    # Read the real GPU PNG rendered at the same scale as H128 actors, not a magnified mockup.
    gpu=rgba(REPORT/f'weapon_v5_{school}_128.png');factor=.5*p['presentation']['display_factor'];gpu_grip=np.array([128.,128.])
    def point(key):return gpu_grip+(np.array(a['anchors'][key])-grip)*factor
    lo,hi=(point('blade_root'),point('tip')) if school=='kiem' else (point('bottom'),point('top'))
    axis=(hi-lo)/np.linalg.norm(hi-lo);normal=np.array([-axis[1],axis[0]])
    def at_pixel(v):
        x,y=np.floor(v).astype(int)
        return gpu[y,x] if 0<=x<gpu.shape[1] and 0<=y<gpu.shape[0] else np.zeros(4,dtype='uint8')
    minimum=999
    for t in [.2,.35,.65,.8]:
        centre=lo+(hi-lo)*t;values=[]
        for n in np.arange(-32,32.001,.125):
            q=centre+normal*n;color=at_pixel(q);values.append((n,tuple(np.floor(q).astype(int)),color))
        if school=='kiem':warm=[n for n,_,c in values if c[3]>=204 and c[:3].min()>90]
        else:warm=[n for n,_,c in values if c[3]>=204 and int(c[0])-int(c[1])>15 and int(c[1])-int(c[2])>8 and c[0]>75]
        check(bool(warm),f'{school} GPU cross-section{t}: painted material detected')
        if not warm:continue
        left,right=min(warm),max(warm)
        counts=[]
        for side,start,end in [('left',left-4,left),('right',right,right+4)]:
            pixels={xy for n,xy,c in values if start<=n<=end and c[3]>=204 and c[0]<80 and c[1]<70 and c[2]<70}
            count=len(pixels);counts.append(count);minimum=min(minimum,count)
            check(count>=1,f'{school} GPU H128 section{t} {side}: opaque DARK contour pixel cells={count} >=1px')
    print(f'{school} minimum measured opaque dark contour pixel cells per sampled side={minimum}; real GPU render factor={factor:.9f}')
    if school=='cung':
        rgb=gpu[:,:,:3];white=(gpu[:,:,3]>=204)&(rgb.min(axis=2)>215)
        check(white.sum()>=20,f'GPU H128 white string core pixels={white.sum()} (not a grey subpixel line)')
for id in sorted(REPAINTED):check(p['assets'][id]['source']['master']==p['weapon_masters']['kiem']['master'],id+' steel material derives from same detailed sword master')
blade=rgba(ART/'attack_blade_only.png');mask=blade[:,:,3]>=204;rgb=blade[:,:,:3].astype(int);light=mask&(rgb.min(axis=2)>190);shadow=mask&(rgb[:,:,0]>65)&(rgb[:,:,0]<180)&(rgb[:,:,2]>rgb[:,:,0]+5)
check(light.sum()>=100 and shadow.sum()>=100,f'action blade retains bright ridge/reflection={light.sum()} and blue-grey shadow face={shadow.sum()} opaque pixels')
check((OUT/'review_lv1.png').read_bytes()==(REPORT/'weapon_v5_review.png').read_bytes(),'review_lv1.png is the actual Godot master+frame0/frame4 capture')
print(f'Weapon master/source/actual H128 pixel checks failures={fail}');sys.exit(bool(fail))
