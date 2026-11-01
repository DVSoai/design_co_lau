#!/usr/bin/env python3
"""Measure actual authored RGBA, not bounds claimed by the generator."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from PIL import Image

R=Path(__file__).resolve().parents[2];D=R/'prototype/pose_rig/data';ART=R/'prototype/pose_rig/art/lv1_30'
p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text());H=p['presentation']['standing_height_source'];fail=0
def check(ok,message):
    global fail
    print(('PASS: ' if ok else 'FAIL: ')+message);fail+=not ok
def array(id):return np.array(Image.open(ART/p['assets'][id]['file']).convert('RGBA'))
hashes=[];wide=0
for i in range(6):
    id=f['frames'][i+2]['layers']['legs']['asset'];a=array(id);h=hashlib.sha256(a.tobytes()).hexdigest();hashes.append(h)
    left,right=[np.array(p['assets'][id]['anchors'][k]) for k in ['foot_left','foot_right']]
    span=np.linalg.norm(left-right)/H;wide+=span>=.3
    print(f'{id} RGBA_SHA256={h} feet/H={span:.9f}')
    for at in [left,right]:
        x,y=np.rint(at).astype(int);region=a[max(0,y-2):y+3,max(0,x-2):x+3,3]
        check(region.size>0 and region.max()>127,id+' measured foot lands on actual boot pixels')
check(len(set(hashes))==6,'all15 run-frame hash pairs differ')
check(wide>=4,f'wide strides={wide}/6, threshold .30H')
for action in ['slash','tram_kiem']:
    for eid,ids in p['numeric_trails'][action].items():
        for i,id in enumerate(ids):
            a=array(id);alpha=a[:,:,3];opaque=int((alpha>=204).sum());visible=int((alpha>12).sum());core=float(np.quantile(alpha[alpha>12],.90))/255
            print(f'{id} opaque_area/H2={opaque/H**2:.9f} visible_area/H2={visible/H**2:.9f} core_alpha_p90={core:.9f}')
            if eid=='16' and i in [1,2]:
                check(opaque/H**2>=.25 and core>=.8,id+' sweep opaque area>=.25H2 and core>=.8')
blade=array('attack_blade_only');ys,xs=np.where(blade[:,:,3]>=128);length=(xs.max()-xs.min()+1)/H
check(.75<=length<=.8,f'actual blade excluding hilt/H={length:.9f}')
for frame in range(4):
    image=Image.new('RGBA',(224,224))
    for layer in ['legs','body','head']:image.alpha_composite(Image.fromarray(array(f'roll_{layer}_{frame}')))
    box=image.getbbox();width,height=box[2]-box[0],box[3]-box[1]
    check(.6<=width/height<=1.7,f'tucked{frame} actual human silhouette={width}x{height}, compact aspect={width/height:.6f}')
f=json.loads((D/'frames30.json').read_text())
check(f['clips']['jump']['frames']==[7] and f['clips']['apex_flip']['frames']==[8,9,10,11] and f['clips']['fall']['frames']==[12],'clip source mapping rise7 / roll8..11 / fall12')
print(f'Motion real-RGBA checks failures={fail}')
sys.exit(bool(fail))
