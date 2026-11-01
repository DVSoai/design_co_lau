#!/usr/bin/env python3
"""One shared held texture per school, normalized from original detailed master art."""
from pathlib import Path
import copy,json,math
import numpy as np
from PIL import Image,ImageFilter
from scipy.ndimage import label,binary_dilation
from build_carry_v4 import position,source_origin
from weapon_v5_scope import RETIRED,HELD
from held_weapon_pose import hand_key

R=Path(__file__).resolve().parents[1];D=R/'prototype/pose_rig/data';ART=R/'prototype/pose_rig/art/lv1_30'
OUT=R/'art/sprites/weapons/lv1';SRC=OUT/'sources';LEGACY=R/'art/sprites/characters/lv1_30'
INK=(35,22,16)

def clean(im):
    a=np.array(im.convert('RGBA'));a[a[:,:,3]<12]=0;a[a[:,:,3]==0,:3]=0
    return Image.fromarray(a)

def ink(im,width):
    # Deterministic outline preservation during sprite reduction, not new concept art.
    pad=width+1;canvas=Image.new('RGBA',(im.width+2*pad,im.height+2*pad));canvas.alpha_composite(im,(pad,pad))
    alpha=canvas.getchannel('A').filter(ImageFilter.MaxFilter(2*width+1));under=Image.new('RGBA',canvas.size,INK+(0,));under.putalpha(alpha);under.alpha_composite(canvas)
    box=under.getbbox();return clean(under.crop(box)),np.array([pad-box[0],pad-box[1]])

def original_master(stem,points,rotation,sort_axis):
    a=np.array(Image.open(SRC/(stem+'.png')).convert('RGBA'));labs,n=label(a[:,:,3]>=220);sizes=np.bincount(labs.ravel());ids=np.argsort(sizes[1:])[-2:]+1
    ids=sorted(ids,key=lambda i:np.where(labs==i)[sort_axis].min());a[labs!=ids[0]]=0;a[a[:,:,3]>0,3]=255
    im=Image.fromarray(a);angle=math.radians(rotation);A=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
    C=np.array([1024.,1024.]);g=np.array(points['grip']);inv=np.linalg.inv(A);off=g-inv@C
    im=im.transform((2048,2048),Image.Transform.AFFINE,tuple(inv[0])+tuple([off[0]])+tuple(inv[1])+tuple([off[1]]),Image.Resampling.BICUBIC)
    box=im.getbbox();im=im.crop(box);factor=508/max(im.size);size=tuple(round(v*factor) for v in im.size)
    anchors={k:(C+A@(np.array(v)-g)-np.array(box[:2]))*factor for k,v in points.items()}
    im=im.resize(size,Image.Resampling.LANCZOS);im,delta=ink(im,2);anchors={k:v+delta for k,v in anchors.items()}
    factor2=512/max(im.size);im=im.resize(tuple(round(v*factor2) for v in im.size),Image.Resampling.LANCZOS)
    return clean(im),{k:list(v*factor2) for k,v in anchors.items()}

def run():
    p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text());before=copy.deepcopy(f)
    H=p['presentation']['standing_height_source'];p['weapon_masters']={}
    config={
      'kiem':('sword_candidates',{'grip':[1100.,210.],'blade_root':[960.,260.],'tip':[222.,525.],'pommel':[1230.,155.]},155-math.degrees(math.atan2(265,-738)),0),
      'cung':('bow_double_recurve',{'grip':[525.,460.],'top':[155.,802.],'bottom':[861.,32.],'belly':[525.,460.],'string':[575.,450.]},180+22-math.degrees(math.atan2(706,770)),1)}
    masters={}
    for school,(stem,points,rotation,sort_axis) in config.items():
        master,anchors=original_master(stem,points,rotation,sort_axis);masters[school]=(master,anchors)
        master.save(OUT/(school+'_lv1_master.png'));(OUT/(school+'_lv1_master.prompt.txt')).write_text((SRC/(stem+'.prompt.txt')).read_text())
        if school=='kiem':scale=.77*H/max(master.size)
        else:
            a=np.array(master);ys,xs=np.where(a[:,:,3]>=128);axis=np.array(anchors['top'])-anchors['bottom'];axis/=np.linalg.norm(axis)
            span=np.ptp(np.column_stack([xs,ys])@axis)+1;scale=1.08*H/span
        size=tuple(round(v*scale) for v in master.size);im=master.resize(size,Image.Resampling.LANCZOS)
        if school=='cung':
            # Keep the originally painted white string at least one screen pixel wide.
            ar=np.array(im);white=(ar[:,:,3]>127)&(ar[:,:,:3].min(axis=2)>215)
            mask=Image.fromarray((white*255).astype('uint8')).filter(ImageFilter.MaxFilter(3));white_layer=Image.new('RGBA',im.size,(250,248,235,0));white_layer.putalpha(mask);im.alpha_composite(white_layer)
        im,delta=ink(im,1);draw_anchors={k:list(np.array(v)*scale+delta) for k,v in anchors.items()}
        # A cord crease may pass through the geometric center after reduction.
        # Snap within two source pixels onto the adjacent painted leather, never a limb.
        ar=np.array(im);yy,xx=np.indices(ar.shape[:2]);rr,gg,bb=ar[:,:,:3].astype(int).transpose(2,0,1);g=np.array(draw_anchors['grip'])
        mask=(ar[:,:,3]>=230)&(rr>=80)&(rr<160)&(gg>=38)&(rr-gg>20)&(bb<90)&((xx-g[0])**2+(yy-g[1])**2<=4)
        ys,xs=np.where(mask);j=np.argmin((xs-g[0])**2+(ys-g[1])**2);draw_anchors['grip']=[int(xs[j]),int(ys[j])]
        if school=='cung':
            # Register the actual middle leather between its painted brass collars.
            ay,ax=np.where(ar[:,:,3]>127);span=ay.max()-ay.min()
            gold=(ar[:,:,3]>127)&(rr>150)&(gg>100)&(bb<180)&(gg>1.15*bb)&(yy>ay.min()+.3*span)&(yy<ay.min()+.7*span)
            labs,n=label(binary_dilation(gold));collars=[]
            for lab in range(1,n+1):
                region=(labs==lab)&gold
                if region.sum()>=3:
                    cy,cx=np.where(region);collars.append((int(region.sum()),np.array([cx.mean(),cy.mean()])))
            collars=sorted(collars,key=lambda v:v[0],reverse=True)[:2];middle=(collars[0][1]+collars[1][1])*.5
            brown=(ar[:,:,3]>=230)&(rr>=60)&(rr<170)&(gg>=25)&(bb<100)&(rr-gg>15)
            cy,cx=np.where(brown);j=np.argmin((cx-middle[0])**2+(cy-middle[1])**2);draw_anchors['grip']=[int(cx[j]),int(cy[j])]
        id=school+'_lv1';im.save(ART/(id+'.png'));im.save(OUT/(id+'.png'))
        (OUT/(id+'.prompt.txt')).write_text((SRC/(stem+'.prompt.txt')).read_text())
        p['assets'][id]={'file':id+'.png','size':list(im.size),'anchors':draw_anchors,'source':{'master':'art/sprites/weapons/lv1/'+school+'_lv1_master.png','export':'art/sprites/weapons/lv1/'+id+'.png','uniform_scale':scale,'outline_source_px':1,'white_string_dilation_source_px':1 if school=='cung' else 0},'status':'drawn_unapproved'}
        p['weapon_masters'][school]={'asset':id,'master':'art/sprites/weapons/lv1/'+school+'_lv1_master.png','master_size':list(master.size),'master_anchors':anchors,'source_sheet':stem,'source_points':points,'offline_rotation_degrees':rotation}
    p['levels']['1']['weapons']={'kiem':'kiem_lv1','cung':'cung_lv1'};p['levels']['1']['run_weapon']='kiem_lv1'
    for frame in HELD:
        row=f['frames'][frame];row['layers']['weapon'].pop('cung_asset',None);row['held_weapon_z']={'kiem':3,'cung':3}
        row.pop('held_hand_by_school',None);row.pop('held_lower_leg_foreground',None)
        for school in ['kiem','cung']:
            layer=row['layers']['body'];bid=layer.get('cung_asset' if school=='cung' else 'asset',p['levels']['1']['body'][layer.get('cung_image',layer['image'])] if school=='cung' else p['levels']['1']['body'][layer['image']])
            anchors=p['assets'][bid]['anchors'];key=hand_key(row,school,anchors)
            hand=position(f,row,school,'body')+np.array(anchors[key])*.5
            own=hand-np.array(p['assets'][school+'_lv1']['anchors']['grip'])*.5
            row['registrations'][school]['weapon']=list(own-source_origin(f,row,school,'weapon'))
    # The action blade is sampled from the SAME silver/blue-grey master, with old anchors
    # retained so the approved trailing masks, hit timing and tip connection do not move.
    master,anchors=masters['kiem'];g=np.array(anchors['grip']);root=np.array(anchors['blade_root']);tip=np.array(anchors['tip']);u=(tip-root)/np.linalg.norm(tip-root);v=np.array([-u[1],u[0]])
    across=150/np.linalg.norm(tip-root);hilt=25/np.dot(root-g,u)
    def transform(along):
        x=u/along;y=v/across;off=root-x*201-y*160
        return master.transform((512,384),Image.Transform.AFFINE,(x[0],y[0],off[0],x[1],y[1],off[1]),Image.Resampling.BICUBIC)
    blade=transform(across);blade_only=Image.new('RGBA',blade.size);blade_only.alpha_composite(blade.crop((201,0,351,384)),(201,0))
    full=Image.new('RGBA',blade.size);full.alpha_composite(transform(hilt).crop((0,0,201,384)),(0,0));full.alpha_composite(blade_only)
    def save_action(id,im):
        # Preserve all approved trail alpha values, including the fading edge.
        ar=np.array(im);rr,gg,bb=ar[:,:,:3].astype(int).transpose(2,0,1)
        ar[(gg>1.18*np.maximum(rr,bb))&(gg>90)]=0;im=Image.fromarray(ar)
        for folder in [ART,LEGACY]:im.save(folder/(id+'.png'))
        p['assets'][id]['source']={'master':'art/sprites/weapons/lv1/kiem_lv1_master.png','blade_length_H':150/H,'offline_axis':'horizontal','preserved_grip':[176,160],'preserved_tip':[350,160]}
    save_action('attack_blade',full);save_action('attack_blade_only',blade_only)
    for prefix in ['swing','swing_skill']:
        for i in range(5):
            id=f'{prefix}_{i}';im=Image.open(ART/(p['assets'][id]['trail_mask']+'.png')).convert('RGBA');im.alpha_composite(full);save_action(id,im)
    for id in RETIRED:
        p['assets'].pop(id,None)
        for folder in [ART,LEGACY]:
            for suffix in ['.png','.png.import','.prompt.txt']:(folder/(id+suffix)).unlink(missing_ok=True)
    assert all(row==before['frames'][i] for i,row in enumerate(f['frames']) if i not in HELD)
    for name,data in [('parts',p),('frames30',f)]: (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Shared Lv1 weapon masters:512px, one held texture per school0–7/12/21; old variants removed; action blade samples identical master materials; anatomy/trails/timings unchanged.')

if __name__=='__main__':run()
