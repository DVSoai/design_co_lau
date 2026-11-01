#!/usr/bin/env python3
"""Register independently drawn chest carry poses and three grounded attack stances."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
from build_run_cycle_v3 import clean,components
from build_carry_v4 import position,source_origin
from weapon_v5_scope import HELD

R=Path(__file__).resolve().parents[1];D=R/'prototype/pose_rig/data';ART=R/'prototype/pose_rig/art/lv1_30';OUT=R/'art/sprites/characters/lv1_30';SRC=OUT/'sources'

def run():
    p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text())
    old_fall_id=f['frames'][12]['layers']['legs'].get('asset',p['levels']['1']['legs'][f['frames'][12]['layers']['legs']['image']])
    fall_world_hips={school:position(f,f['frames'][12],school,'legs')+np.array(p['assets'][old_fall_id]['anchors']['hip'])*.5 for school in ['kiem','cung']}
    def save(id,im,anchors,source):
        im=clean(im)
        for folder in [ART,OUT]:im.save(folder/(id+'.png'))
        p['assets'][id]={'file':id+'.png','size':list(im.size),'anchors':anchors,'source':source,'status':'drawn_unapproved'}
        (OUT/(id+'.prompt.txt')).write_text('Normalization of original chest/stance art: '+json.dumps(source,ensure_ascii=False)+'\n')
    sheet=clean(Image.open(SRC/'carry_chest_run.png'));pieces=components(sheet,6,2)
    # Source marks are for authoring registration only. Acceptance uses rendered ablations.
    marks=[((330,116),(280,320),(460,164),(285,250)),((810,116),(780,320),(950,164),(770,284)),((1315,117),(1280,320),(1452,164),(1085,365)),((385,568),(340,770),(471,610),(54,650)),((808,570),(775,770),(976,615),(611,570)),((1330,570),(1280,770),(1452,615),(1080,820))]
    def torso(id,index,lean):
        neck,hip,grip,free=map(lambda x:np.array(x,float),marks[index]);v=neck-hip;C=np.array([160.,150.]);dx=50*math.sin(math.radians(lean));dy=-50*math.cos(math.radians(lean));sx=50/np.linalg.norm(v)
        A=np.array([[sx,(dx-sx*v[0])/v[1]],[0,dy/v[1]]]);inv=np.linalg.inv(A);off=hip-inv@C
        im=pieces[index][1].transform((320,256),Image.Transform.AFFINE,tuple(inv[0])+tuple([off[0]])+tuple(inv[1])+tuple([off[1]]),Image.Resampling.BICUBIC)
        anchors={k:list(C+A@(point-hip)) for k,point in [('neck',neck),('hip',hip),('grip',grip),('near_hand',grip),('far_hand',free),('free_hand',free),('back',hip+[-30,-30])]}
        save(id,im,anchors,{'sheet':'carry_chest_run','phase':index,'lean_offline_degrees':lean,'original_hem':True,'source_marks':marks[index]})
    for i in range(6):torso('chest_run_%d'%i,i,12)
    torso('chest_stand',2,0);torso('chest_fall',4,12)
    fall=p['assets']['fall_legs_0'];fall_scale=65/(fall['anchors']['sole'][1]-fall['anchors']['hip'][1]);fall_image=Image.open(ART/fall['file'])
    save('chest_fall_legs',fall_image.resize(tuple(round(v*fall_scale) for v in fall_image.size),Image.Resampling.LANCZOS),{k:list(np.array(v)*fall_scale) for k,v in fall['anchors'].items()},{'own_asset':'fall_legs_0','uniform_scale':fall_scale,'hip_to_sole_source':65})
    f['frames'][12]['layers']['legs']['asset']='chest_fall_legs'
    stance_sheet=clean(Image.open(SRC/'attack_stances_three.png'))
    for i,(box,full) in enumerate(components(stance_sheet,3,1)):
        im=full.crop(box);a=np.array(im);ys,xs=np.where(a[:,:,3]>=128);top=ys.min();bottom=ys.max();band=np.where(a[min(top+10,im.height-1),:,3]>=128)[0];hx=float((band.min()+band.max())*.5);hy=float(top+10)
        scale=65/(bottom-hy);im=im.resize(tuple(round(v*scale) for v in im.size),Image.Resampling.LANCZOS)
        save('attack_stance_%d'%i,im,{'hip':[hx*scale,hy*scale],'sole':[hx*scale,(bottom+.5)*scale]}, {'sheet':'attack_stances_three','phase':i,'crop':list(box),'uniform_scale':scale})
    for frame in HELD:
        row=f['frames'][frame];id='chest_stand' if frame in [0,1] else ('chest_fall' if frame in [12,21] else 'chest_run_%d'%(frame-2))
        row['layers']['body'].update(asset=id,cung_asset=id);row['held_hand']='grip';row.pop('held_hand_by_school',None);row.pop('held_lower_leg_foreground',None)
        if frame in [6,7,21]:row['held_lower_leg_foreground']={'cung':30}
    for frame in range(13,30):
        row=f['frames'][frame];group=0 if frame<=20 else (1 if frame<=25 else 2)
        row['layers']['legs']['asset']='attack_stance_%d'%group;row['layers']['legs'].pop('stance',None);row['layers']['legs'].pop('lunge',None)
        if frame==22:row['layers']['body']['image']=9
    for row in f['frames']:
        frame=row['id']
        if frame not in HELD and frame not in range(13,30):continue
        for school in ['kiem','cung']:
            ids={}
            for layer in ['head','body','legs']:
                data=row['layers'][layer];idx=data.get('cung_image',data['image']) if layer=='body' and school=='cung' else data['image']
                ids[layer]=data.get('asset',p['levels']['1'][layer][idx])
                if layer=='body' and school=='cung':ids[layer]=data.get('cung_asset',ids[layer])
            anchor=lambda layer,key:np.array(p['assets'][ids[layer]]['anchors'][key])*.5
            if frame in range(13,30):
                # Same source table, explicit crop registration to a shared ground plane.
                x=(row['reference']['chan'][1]-f['frames'][0]['reference']['chan'][1])*3
                legs=np.array([x,0.])-anchor('legs','sole');hip=legs+anchor('legs','hip')
            else:
                if frame==12:legs=fall_world_hips[school]-anchor('legs','hip')
                else:legs=position(f,row,school,'legs')
                hip=legs+anchor('legs','hip')
            own={'legs':legs,'body':hip-anchor('body','hip')};own['head']=own['body']+anchor('body','neck')-anchor('head','neck')
            if frame in HELD:
                wid=p['levels']['1']['weapons'][school];own['weapon']=own['body']+anchor('body','grip')-np.array(p['assets'][wid]['anchors']['grip'])*.5
            for layer,placed in own.items():row['registrations'][school][layer]=list(placed-source_origin(f,row,school,layer))
    p['attack_stance_groups']=[{'frames':[13,20],'asset':'attack_stance_0','reference_leg_icon':31},{'frames':[21,25],'asset':'attack_stance_1','reference_leg_icon':30},{'frames':[26,29],'asset':'attack_stance_2','reference_leg_icon':29}]
    for name,data in [('parts',p),('frames30',f)]: (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Chest carry v7: eight torso poses; front chest fist; three shared grounded attack stances13–20/21–25/26–29; raw reference rows and all skill timing retained. Acceptance requires rendered ablations.')

if __name__=='__main__':run()
