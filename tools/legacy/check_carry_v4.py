#!/usr/bin/env python3
"""Independent PIL whole-shoe occlusion, connected feet, bow and narrow-scope checks."""
from pathlib import Path
import copy,io,json,subprocess,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
from build_carry_v4 import position
from held_weapon_pose import hand_key
from weapon_v5_scope import frame_without_weapon,parts_without_weapon,asset_is_unchanged

R=Path(__file__).resolve().parents[2];D=R/'prototype/pose_rig/data';ART=R/'prototype/pose_rig/art/lv1_30'
p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text());H=p['presentation']['standing_height_logic']
regions=json.loads((D/'foot_regions_v4.json').read_text())['polygons'];fail=0;HELD=[0,1,2,3,4,5,6,7,12,21]
def check(ok,message):
    global fail
    print(('PASS: ' if ok else 'FAIL: ')+message);fail+=not ok
def baseline(path):return subprocess.check_output(['git','show','cc2a04a:'+path],cwd=R)
old_f=json.loads(baseline('prototype/pose_rig/data/frames30.json'));old_p=json.loads(baseline('prototype/pose_rig/data/parts.json'))
def invariant(row,i):
    row=frame_without_weapon(row)
    if i==3:
        row['layers']['legs'].pop('asset',None)
        for school in ['kiem','cung']:row['registrations'][school].pop('legs',None)
    if i==6:row.get('held_weapon_z',{}).pop('cung',None)
    return row
check(all(invariant(row,i)==invariant(old_f['frames'][i],i) for i,row in enumerate(f['frames'])),'all30 frame rows unchanged outside approved frame3 leg and shared held-weapon placement/depth')
check({k:v for k,v in f.items() if k!='frames'}=={k:v for k,v in old_f.items() if k!='frames'},'all clip mappings/timings and source reference tables unchanged')
check(parts_without_weapon(p)==parts_without_weapon(old_p),'all anatomy mappings/presentation unchanged outside shared-weapon aliases/master metadata')
check(all(asset_is_unchanged(k,v,p['assets']) for k,v in old_p['assets'].items()),'every preexisting non-weapon asset metadata unchanged; retired/repainted weapon IDs are explicit')
for path in ['prototype/pose_rig/data/skills.json','prototype/pose_rig/data/effects.json','prototype/pose_rig/player_controller.gd','prototype/config/tuning.gd','prototype/config/runtime_tuning.gd']:
    if (R/path).exists():check((R/path).read_bytes()==baseline(path),'unchanged '+path)
def pixels(id,parts=p):
    source=ART/parts['assets'][id]['file'] if parts is p else io.BytesIO(baseline('prototype/pose_rig/art/lv1_30/'+parts['assets'][id]['file']))
    return np.array(Image.open(source).convert('RGBA'))
def ids(row,school,parts=p):
    return {'legs':row['layers']['legs'].get('asset',parts['levels']['1']['legs'][row['layers']['legs']['image']]),
            'body':row['layers']['body'].get('cung_asset' if school=='cung' else 'asset',parts['levels']['1']['body'][row['layers']['body'].get('cung_image',row['layers']['body']['image'])] if school=='cung' else row['layers']['body']['asset']),
            'head':parts['levels']['1']['head'][row['layers']['head']['image']],
            'weapon':parts['levels']['1']['run_weapon'] if school=='kiem' and 2<=row['id']<=7 else (row['layers']['weapon'].get('cung_asset',parts['levels']['1']['weapons']['cung']) if school=='cung' else parts['levels']['1']['weapons']['kiem'])}
def foot_metrics(data,row,school,direction,parts=p):
    names=ids(row,school,parts);leg=pixels(names['legs'],parts);yy,xx=np.indices(leg.shape[:2]);alpha=leg[:,:,3]/255.;survives=np.ones_like(alpha)
    world_x=direction*(position(data,row,school,'legs')[0]+(xx+.5)*.5);world_y=position(data,row,school,'legs')[1]+(yy+.5)*.5
    for layer in ['body','head','weapon']:
        if layer=='weapon' and row.get('held_weapon_z',{}).get(school,3)<0:continue
        im=pixels(names[layer],parts);at=position(data,row,school,layer)
        sx=np.floor((direction*world_x-at[0])*2).astype(int);sy=np.floor((world_y-at[1])*2).astype(int)
        valid=(sx>=0)&(sy>=0)&(sx<im.shape[1])&(sy<im.shape[0]);cover=np.zeros_like(alpha);cover[valid]=im[sy[valid],sx[valid],3]/255.;
        if layer=='weapon' and school in row.get('held_lower_leg_foreground',{}):
            cutoff=parts['assets'][names['legs']]['anchors']['hip'][1]+row['held_lower_leg_foreground'][school]
            cover*=1-alpha*(yy>=np.ceil(cutoff))
        survives*=1-cover
    result=[]
    for polygon in regions[names['legs']]:
        mask=Image.new('L',(leg.shape[1],leg.shape[0]));ImageDraw.Draw(mask).polygon([tuple(pt) for pt in polygon],fill=255)
        area=alpha*(np.array(mask)>0)*(alpha>=.05);total=area.sum();occluded=(area*(1-survives)).sum()/total
        visible=(area>=.5)&(survives>=.5);labs,n=label(visible);sizes=np.bincount(labs.ravel());sizes[0]=0
        component=labs==int(sizes.argmax());result.append((total,occluded,visible,component))
    return result
max_cover=0
for school in ['kiem','cung']:
    for direction in [-1,1]:
        for frame in range(2,8):
            row=f['frames'][frame];metrics=foot_metrics(f,row,school,direction)
            for foot,(area,covered,visible,component) in enumerate(metrics):
                max_cover=max(max_cover,covered)
                check(area>=20 and covered<=.30,f'{school} frame{frame} dir{direction} foot{foot}: whole shoe area={area:.6f}, covered={covered:.9%} <=30%')
                check(component.sum()>=10 and component.sum()/max(1,visible.sum())>=.7,f'whole visible shoe connected pixels={component.sum()}/{visible.sum()}')
            first,second=metrics[0][3],metrics[1][3]
            check(not np.any(binary_dilation(first)&second),f'{school} frame{frame} dir{direction}: TWO separate connected visible shoes')
    for frame in HELD:
        row=f['frames'][frame]
        for layer in (['head','body','legs','weapon'] if frame==3 else ['weapon']):
            key={'head':'dau','body':'than','legs':'chan','weapon':'vu_khi'}[layer]
            print(f'PLACEMENT {school} frame{frame} {layer}: source [image,dx,dy]={row["reference"][key]}; image_offset={f["reference"]["image_offsets"][school if layer=="weapon" else key][row["reference"][key][0]]}; own_registration={row["registrations"][school][layer]}; own_top_left={position(f,row,school,layer).tolist()}')
        if school!='cung':continue
        bow=p['assets'][p['levels']['1']['weapons']['cung']];a={k:np.array(v)*.5 for k,v in bow['anchors'].items()}
        body_id=ids(row,school)['body'];ba=p['assets'][body_id]['anchors'];key=hand_key(row,school,ba)
        hand=position(f,row,school,'body')+np.array(ba[key])*.5;origin=position(f,row,school,'weapon')
        gap=np.linalg.norm(hand-(origin+(a['top']+a['bottom'])*.5))/H
        lengths=[np.linalg.norm(hand-(origin+a[k])) for k in ['top','bottom']];imbalance=abs(lengths[0]-lengths[1])/min(lengths)
        check(gap<=.05 and imbalance<=.15 and np.linalg.norm(hand-origin-a['grip'])<=1,f'bow frame{frame} hand-midpoint/H={gap:.9f}; tip distances={lengths}; imbalance(shorter denominator)={imbalance:.9%}; true middle grip={bow["anchors"]["grip"]}')
# Check why the former point-only foot check could not validate two painted feet.
old_metrics=foot_metrics(old_f,old_f['frames'][3],'kiem',1,old_p)
print(f'Old frame3 rear shoe-only covered={old_metrics[0][1]:.9%}; this does not measure its hidden calf or silhouette readability.')
old_anchors=old_p['assets']['run_v3_legs_1']['anchors'];front=Image.new('L',tuple(old_p['assets']['run_v3_legs_1']['size']))
ImageDraw.Draw(front).polygon([tuple(pt) for pt in regions['run_v3_legs_1'][1]],fill=255)
check(all(front.getpixel(tuple(round(v) for v in old_anchors[key]))>0 for key in ['foot_left','foot_right']),'negative control: BOTH former sole landmarks land on the SAME front shoe; whole-shoe polygons now select the real rear shoe independently')
for id in ['bow_hold','run_v3_bow']:
    a=old_p['assets'][id]['anchors'];mid=(np.array(a['top'])+a['bottom'])*.5;gap=np.linalg.norm(np.array(a['grip'])-mid)*.5/H
    check(gap>.05,f'negative control: old {id} midpoint gap/H={gap:.9f}, correctly rejected')
print(f'Maximum whole-foot covered area={max_cover:.9%};24 frame/school/direction cases,48 shoes; failures={fail}')
sys.exit(bool(fail))
