#!/usr/bin/env python3
"""PIL/NumPy measurements on actual run2..7 textures, with baseline scope checks."""
from pathlib import Path
import argparse,copy,hashlib,itertools,json,math,subprocess,sys
import numpy as np
from PIL import Image
from weapon_v5_scope import RETIRED,REPAINTED,frame_without_weapon,asset_is_unchanged

R=Path(__file__).resolve().parents[2];D=R/'prototype/pose_rig/data';ART=R/'prototype/pose_rig/art/lv1_30'
parser=argparse.ArgumentParser();parser.add_argument('--baseline',default='ae1327c');args=parser.parse_args()
p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text());H=p['presentation']['standing_height_logic'];fail=0
def old(path):return subprocess.check_output(['git','show',args.baseline+':'+path],cwd=R)
def check(ok,message):
    global fail
    print(('PASS: ' if ok else 'FAIL: ')+message);fail+=not ok
base_p=json.loads(old('prototype/pose_rig/data/parts.json'));base_f=json.loads(old('prototype/pose_rig/data/frames30.json'))
check(all(frame_without_weapon(row)==frame_without_weapon(base_f['frames'][i]) for i,row in enumerate(f['frames'])),'all30 anatomy/frame rows unchanged outside authorized shared weapon placement/depth')
check({k:v for k,v in f.items() if k!='frames'}=={k:v for k,v in base_f.items() if k!='frames'},'clip/frame mapping and numeric reference table unchanged')
check(all(asset_is_unchanged(id,data,p['assets']) for id,data in base_p['assets'].items()),'all non-weapon asset registrations unchanged; authorized retired/repainted IDs explicit')
old_images=subprocess.check_output(['git','ls-tree','-r','--name-only',args.baseline,'--','prototype/pose_rig/art','art/sprites'],cwd=R,text=True).splitlines()
for path in old_images:
    if path.endswith('.png') and Path(path).stem not in RETIRED|REPAINTED:check((R/path).read_bytes()==old(path),'unchanged baseline image '+path)
for path in ['prototype/pose_rig/data/skills.json','prototype/pose_rig/data/effects.json','prototype/config/tuning.gd','prototype/config/runtime_tuning.gd','prototype/scripts/player.gd']:
    check((R/path).read_bytes()==old(path),'unchanged '+path)
def image(id):return np.array(Image.open(ART/p['assets'][id]['file']).convert('RGBA'))
def anchor(id,key):return np.array(p['assets'][id]['anchors'][key],float)*.5
def pos(row,school,layer):
    key={'head':'dau','body':'than','legs':'chan','weapon':'vu_khi'}[layer];idx,dx,dy=row['reference'][key]
    ox,oy=f['reference']['image_offsets'][school if layer=='weapon' else key][idx]
    return np.array([dx+ox,-dy+oy])*3+row['registrations'][school][layer]
for school in ['kiem','cung']:
    wide=0;free=[];body_hash=[];leg_hash=[]
    for i in range(6):
        row=f['frames'][i+2];body_id=row['layers']['body']['asset' if school=='kiem' else 'cung_asset'];leg_id=row['layers']['legs']['asset'];weapon_id=p['levels']['1']['run_weapon'] if school=='kiem' else p['levels']['1']['weapons']['cung']
        body,leg,weapon=[image(id) for id in [body_id,leg_id,weapon_id]]
        bh=hashlib.sha256(body.tobytes()).hexdigest();lh=hashlib.sha256(leg.tobytes()).hexdigest();body_hash.append(bh);leg_hash.append(lh)
        stride=np.linalg.norm(anchor(leg_id,'foot_left')-anchor(leg_id,'foot_right'))/H;wide+=stride>=.3
        free.append(anchor(body_id,'free_hand')-anchor(body_id,'hip'))
        axis=anchor(body_id,'neck')-anchor(body_id,'hip');lean=math.degrees(math.atan2(abs(axis[0]),abs(axis[1])))
        check(10<=lean<=15,f'{school} frame{i+2} torso lean={lean:.9f}deg; foot span/H={stride:.9f}')
        # Skin landmarks must be on real opaque artwork, not just claimed in JSON.
        for key in ['grip','free_hand']:
            x,y=np.rint(anchor(body_id,key)*2).astype(int);r,g,b,a=body[y,x]
            check(a>=204 and r>=153 and g>=76,f'{school} frame{i+2} {key} painted skin RGBA={tuple(map(int,[r,g,b,a]))}')
        yy,xx=np.indices(leg.shape[:2]);delta=(pos(row,school,'legs')-pos(row,school,'weapon'))*2
        wx=np.floor(xx+.5+delta[0]).astype(int);wy=np.floor(yy+.5+delta[1]).astype(int)
        valid=(wx>=0)&(wx<weapon.shape[1])&(wy>=0)&(wy<weapon.shape[0]);la=leg[:,:,3].astype(float)/255
        wa=np.zeros_like(la);wa[valid]=weapon[wy[valid],wx[valid],3]/255
        visible=la>=.05;overlap=np.minimum(la,wa)[visible].sum()/la[visible].sum()
        foreground=np.zeros_like(la)
        if school in row.get('held_lower_leg_foreground',{}):
            foreground=la*(yy>=np.ceil(p['assets'][leg_id]['anchors']['hip'][1]+row['held_lower_leg_foreground'][school]))
        covered=(np.minimum(la,wa)*(1-foreground))[visible].sum()/la[visible].sum() if row['held_weapon_z'][school]>0 else 0
        check(covered<=.15,f'{school} frame{i+2} rendered weapon cover={covered:.9%}, raw silhouette overlap={overlap:.9%}, z={row["held_weapon_z"][school]}')
        print(f'RGBA hashes {school} frame{i+2}: torso={bh}, legs={lh}')
        for layer in ['head','body','legs','weapon']:print(f'PLACEMENT {school} frame{i+2} {layer} source={row["reference"][{"head":"dau","body":"than","legs":"chan","weapon":"vu_khi"}[layer]]} own_top_left={pos(row,school,layer).tolist()} registration={row["registrations"][school][layer]}')
    travel=max(np.linalg.norm(a-b) for a,b in itertools.combinations(free,2))/H
    check(wide>=4,f'{school}: >=.30H strides={wide}/6')
    check(travel>=.15,f'{school}: free hand movement relative to hip/H={travel:.9f}')
    check(len(set(body_hash))==6 and len(set(leg_hash))==6,f'{school}: all15 torso pairs and all15 leg pairs have distinct RGBA hashes')
print(f'Run-only real-file checks failures={fail}')
sys.exit(bool(fail))
