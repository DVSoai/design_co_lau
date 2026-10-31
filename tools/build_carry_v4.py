#!/usr/bin/env python3
"""Normalize original edited art; fix only run frame3 and held-bow registrations."""
from pathlib import Path
import copy,json
import numpy as np
from PIL import Image
from build_run_cycle_v3 import clean,components

R=Path(__file__).resolve().parents[1];D=R/'prototype/pose_rig/data'
ART=R/'prototype/pose_rig/art/lv1_30';OUT=R/'art/sprites/characters/lv1_30';SRC=OUT/'sources'
HELD=[0,1,2,3,4,5,6,7,12,21]

def run():
    p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text())
    before=copy.deepcopy(f)
    old_leg=p['assets'][f['frames'][3]['layers']['legs']['asset']]
    leg_world_hips={school:position(f,f['frames'][3],school,'legs')+np.array(old_leg['anchors']['hip'])*.5 for school in ['kiem','cung']}
    def save(id,im,anchors,source):
        im=clean(im)
        for folder in [ART,OUT]:im.save(folder/(id+'.png'))
        p['assets'][id]={'file':id+'.png','size':list(im.size),'anchors':anchors,'source':source,'status':'drawn_unapproved'}
        (OUT/(id+'.prompt.txt')).write_text('Original edited artwork normalization: '+json.dumps(source,ensure_ascii=False)+'\n')
    sheet=clean(Image.open(SRC/'carry_v4_leg_shoes.png'))
    box,full=components(sheet,2,1)[0];cut=full.crop(box)
    # Independently marked belt joint and both sole points, in the original sheet.
    hip=np.array([675.,115.]);rear=np.array([205.,520.]);front=np.array([680.,620.])
    scale=65/(float(box[3])-hip[1]);origin=np.array(box[:2])
    anchors={k:list((v-origin)*scale) for k,v in [('hip',hip),('foot_left',rear),('foot_right',front)]}
    size=tuple(round(v*scale) for v in cut.size);anchors['sole']=[anchors['hip'][0],size[1]]
    save('carry_v4_legs_3',cut.resize(size,Image.Resampling.LANCZOS),anchors,
         {'sheet':'carry_v4_leg_shoes','candidate':0,'crop':list(box),'scale':scale,'marked_joint':hip.tolist()})
    row=f['frames'][3];old_id=row['layers']['legs']['asset'];row['layers']['legs']['asset']='carry_v4_legs_3'
    for school in ['kiem','cung']:
        # Keep the old world hip exactly; only the independently drawn leg crop changes.
        world_hip=leg_world_hips[school]
        row['registrations'][school]['legs']=list(world_hip-np.array(anchors['hip'])*.5-source_origin(f,row,school,'legs'))
    bow=clean(Image.open(SRC/'carry_v4_bow.png'));box,full=components(bow,2,1)[0]
    top=np.array([731.,127.]);bottom=np.array([214.,718.]);grip=np.array([562.,482.])
    midpoint=(top+bottom)*.5;axis=(top-bottom)/np.linalg.norm(top-bottom);perp=np.array([-axis[1],axis[0]])
    # Normalize length and shallow curvature offline; the middle wrap remains the grip.
    # No runtime rotations, no moving the anchor onto a lower limb.
    scale=150/np.linalg.norm(top-bottom);A=scale*(np.outer(axis,axis)+.4*np.outer(perp,perp))
    centre=np.array([128.,128.]);inverse=np.linalg.inv(A);offset=midpoint-inverse@centre
    im=full.transform((256,256),Image.Transform.AFFINE,tuple(inverse[0])+tuple([offset[0]])+tuple(inverse[1])+tuple([offset[1]]),Image.Resampling.BICUBIC)
    anchors={k:list(centre+A@(v-midpoint)) for k,v in [('top',top),('bottom',bottom),('grip',grip),('belly',grip),('string',midpoint)]}
    save('carry_v4_bow',im,anchors,{'sheet':'carry_v4_bow','candidate':0,'crop':list(box),'length_source':150,'perpendicular_normalization':.4,'grip':'center_wrapped_handle','marked_grip':grip.tolist(),'marked_tips':[top.tolist(),bottom.tolist()]})
    for frame in HELD:
        row=f['frames'][frame];row['layers']['weapon']['cung_asset']='carry_v4_bow'
        bid=row['layers']['body'].get('cung_asset',p['levels']['1']['body'][row['layers']['body'].get('cung_image',row['layers']['body']['image'])])
        body_anchor=p['assets'][bid]['anchors'];grip_key='grip' if row.get('held_hand')=='grip' or body_anchor['grip'][0]>=body_anchor['far_hand'][0] else 'far_hand'
        hand=position(f,row,'cung','body')+np.array(body_anchor[grip_key])*.5
        row['registrations']['cung']['weapon']=list(hand-np.array(anchors['grip'])*.5-source_origin(f,row,'cung','weapon'))
    # The lifted front boot at frame6 is nearer than the carried bow's lower limb.
    # Keep the same fist/position; let that boot occlude the far-side bow naturally.
    f['frames'][6]['held_weapon_z']['cung']=-1
    assert all(row==before['frames'][i] for i,row in enumerate(f['frames']) if i not in HELD)
    for name,data in [('parts',p),('frames30',f)]: (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Carry v4: frame3 leg crop, held bow0–7/12/21; original hips, torsos, hands, source rows and skill poses unchanged.')

def source_origin(f,row,school,layer):
    key={'head':'dau','body':'than','legs':'chan','weapon':'vu_khi'}[layer];idx,dx,dy=row['reference'][key]
    ox,oy=f['reference']['image_offsets'][school if layer=='weapon' else key][idx]
    return np.array([dx+ox,-dy+oy])*3

def position(f,row,school,layer):return source_origin(f,row,school,layer)+row['registrations'][school][layer]

if __name__=='__main__':run()
