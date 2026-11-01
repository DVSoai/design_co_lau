#!/usr/bin/env python3
"""Register our painted anatomy and adapt the approved numeric reference (no foreign pixels)."""
from pathlib import Path
import json, math
import numpy as np
from PIL import Image, ImageDraw

R = Path(__file__).resolve().parents[1]
D = R / 'prototype/pose_rig/data'
ART = R / 'prototype/pose_rig/art/lv1_30'
OUT = R / 'art/sprites/characters/lv1_30'

def main():
    load = lambda name: json.loads((D / (name + '.json')).read_text())
    p, f, s = [load(n) for n in ['parts', 'frames30', 'skills']]
    ref = json.loads((R / 'docs/ref/so_lieu_tham_khao.json').read_text())
    # Centers of the exposed painted neck, measured on our RGBA at the collar.
    neck_x = [56,54,82,85,88,79,None,None,None,69,65,59,49,56,59,65,59.5,62]
    for i, x in enumerate(neck_x):
        if x is not None:
            p['assets'][f'body_{i}']['anchors']['neck'][0] = x
    heads={0:0,1:1,2:7,3:3,4:0,5:4,6:5,7:6}
    bodies={0:6,1:0,2:2,3:3,4:4,5:2,6:3,7:4,8:5,10:9,11:10,12:11,13:12,14:12,15:16,16:17,17:15}
    legs={0:7,1:0,2:1,3:2,4:3,5:4,6:5,7:6,8:6,9:0}
    for row in f['frames']:
        r=ref['bang_30_khung'][row['id']]
        row['reference'] = r
        row['layers']['head'].update(image=heads[r['dau'][0]],dx=0,dy=0)
        row['layers']['body'].update(image=bodies[r['than'][0]],dx=0,dy=0)
        row['layers']['legs'].update(image=legs[r['chan'][0]],dx=(r['chan'][1]+7)*3,dy=(7-r['chan'][2])*3)
        row['layers']['body'].pop('cung_image',None)
        row['layers']['legs'].pop('stance',None);row['layers']['legs'].pop('lunge',None)
        if row['id'] in range(8) or row['id']==12:row['layers']['body']['cung_image']=12
        if row['id'] in [14,23]:row['layers']['body']['cung_image']=15
        if row['id'] in [18,27]:row['layers']['body']['cung_image']=16
        if row['id'] in [17,26]:row['layers']['body']['cung_image']=17
        if row['id'] in [13,14,15,16]:row['layers']['legs']['stance']=True
        if row['id']==15:row['layers']['legs']['lunge']=True
        if row['id'] in [8,9,10,11]:
            row['layers']['body']['image']=[5,6,7,8][row['id']-8]
            row['layers']['legs'].update(image=[6,7,8,9][row['id']-8],dx=0,dy=0)
        if row['id']==22:row['layers']['body']['image']=5
        row['held_visible']=row['id'] in ref['cong_thuc']['vu_khi_cam_tay_hien_o_khung']
        row['attack']=not row['held_visible'] and row['id'] not in [8,9,10,11,22]
    f['clips']['fall']['frames']=[22]
    f['reference'] = {'path': 'docs/ref/so_lieu_tham_khao.json', 'logic_per_reference_px': 3,
                      'formula': ref['cong_thuc']['vi_tri_lop'],
                      'image_offsets': ref['do_lech_hinh_bo_mac_dinh'],
                      'effect_offsets':ref['hieu_ung']}
    from refresh_character_motion import refresh
    refresh(p,f,ref)
    # Keep source origins verbatim and make the conversion to our cropped drawings explicit.
    for row in f['frames']:
        row['registrations']={}
        for school in ['kiem','cung']:
            layers=row['layers']; ids={}
            for layer in ['legs','body','head']:
                index=layers[layer].get('cung_image',layers[layer]['image']) if school=='cung' and layer=='body' else layers[layer]['image']
                ids[layer]=p['levels']['1'][layer][index]
                ids[layer]=layers[layer].get('asset',ids[layer])
                if school=='cung' and layer=='body':ids[layer]=layers[layer].get('cung_asset',ids[layer])
            if layers['legs'].get('stance'):ids['legs']='legs_guard'
            if layers['legs'].get('lunge'):ids['legs']='legs_lunge'
            anchor=lambda layer,key:np.array(p['assets'][ids[layer]]['anchors'][key])*.5
            pos={'legs':np.array([layers['legs']['dx'],layers['legs']['dy']])-anchor('legs','sole')}
            if row['id'] in [9,10,11]:pos['legs']=np.array([0,-45])-anchor('legs','hip')
            pos['body']=pos['legs']+anchor('legs','hip')-anchor('body','hip')
            pos['head']=pos['body']+anchor('body','neck')-anchor('head','neck')
            if row['id'] in range(2,8):
                # The source torso row drives the run bob, not the old crouched
                # leg crop height. Our redrawn legs register to that moving hip.
                neutral=p['assets'][p['levels']['1']['legs'][0]]['anchors']
                standing_hip=(np.array(neutral['hip'])-neutral['sole'])*.5
                raw=row['reference']['than'];base=ref['bang_30_khung'][0]['than']
                moving_hip=standing_hip+np.array([raw[1]-base[1],base[2]-raw[2]])*3
                pos['legs']=moving_hip-anchor('legs','hip')
                pos['body']=moving_hip-anchor('body','hip')
                pos['head']=pos['body']+anchor('body','neck')-anchor('head','neck')
            if 'roll_origin' in row:pos={layer:np.array(row['roll_origin'],float) for layer in ['legs','body','head']}
            corrections={}
            for layer,key in [('legs','chan'),('body','than'),('head','dau')]:
                image,dx,dy=row['reference'][key]
                ox,oy=ref['do_lech_hinh_bo_mac_dinh'][key][image]
                raw=np.array([dx+ox,-dy+oy])*3
                corrections[layer]=list(pos[layer]-raw)
            bp=p['assets'][ids['body']]['anchors']
            hand=np.array(bp['grip'] if bp['grip'][0]>=bp['far_hand'][0] else bp['far_hand'])*.5+pos['body']
            weapon=p['levels']['1']['weapons'][school]
            if school=='kiem' and row['id'] in range(2,8):weapon=p['levels']['1']['run_weapon']
            wi,wx,wy=row['reference']['vu_khi'];ox,oy=ref['do_lech_hinh_bo_mac_dinh'][school][wi]
            raw=np.array([wx+ox,-wy+oy])*3
            corrections['weapon']=list(hand-np.array(p['assets'][weapon]['anchors']['grip'])*.5-raw)
            row['registrations'][school]=corrections
    # A full blade from our independently drawn sword, baked horizontal offline.
    asset = p['assets']['sword']
    image = Image.open(ART / asset['file']).convert('RGBA')
    grip, tip = [np.array(asset['anchors'][k], float) for k in ['grip', 'tip']]
    u = (tip - grip) / np.linalg.norm(tip - grip)
    factor = .78 * p['presentation']['standing_height_source'] / np.linalg.norm(tip-grip)
    canvas = Image.new('RGBA', (512,384))
    origin = np.array([176.,160.])
    # Inverse affine: final horizontal source pixels -> the original painted sword.
    coeff = (u[0]/factor,-u[1]/factor,grip[0]-(u[0]*origin[0]-u[1]*origin[1])/factor,
             u[1]/factor,u[0]/factor,grip[1]-(u[1]*origin[0]+u[0]*origin[1])/factor)
    blade = image.transform(canvas.size, Image.Transform.AFFINE, coeff, Image.Resampling.BICUBIC)
    length = .78 * p['presentation']['standing_height_source']
    ar=np.array(blade);red,green,blue,alpha=ar.astype(int).transpose(2,0,1)
    yy,xx=np.indices(alpha.shape)
    steel=(alpha>127)&(red>120)&(green>120)&(blue>120)&(abs(red-blue)<55)&(abs(yy-origin[1])<10)&(xx>origin[0])
    bx=np.where(steel)[1];start,end=int(bx.min()),int(bx.max())+1
    cut=blade.crop((start,0,end,blade.height))
    stretched=cut.resize((round(length),blade.height),Image.Resampling.BICUBIC)
    blade_only=Image.new('RGBA',canvas.size);blade_only.alpha_composite(stretched,(start,0))
    full=Image.new('RGBA',canvas.size);full.alpha_composite(blade.crop((0,0,start,blade.height)),(0,0));full.alpha_composite(stretched,(start,0));blade=full
    anchors = {'grip': list(origin), 'blade_root':[start,origin[1]], 'tip':[start+round(length)-1,origin[1]]}
    def save(id, im, metadata=None):
        ar=np.array(im);red,green,blue=ar[:,:,:3].astype(int).transpose(2,0,1)
        ar[(green>1.18*np.maximum(red,blue))&(green>90)]=0
        im=Image.fromarray(ar)
        im.save(ART / (id+'.png')); im.save(OUT / (id+'.png'))
        p['assets'].setdefault(id, {}).update(file=id+'.png', size=list(im.size), anchors=anchors,
            source={'own_asset':'sword.png','offline_axis':'horizontal','blade_length_H':.78},status='drawn_unapproved')
        if metadata: p['assets'][id].update(metadata)
        (OUT/(id+'.prompt.txt')).write_text('Offline numeric registration of existing independently drawn Cờ Lau sword; no new generated or reference pixels.\n')
    save('attack_blade', blade)
    save('attack_blade_only',blade_only)
    blade=Image.open(ART/'attack_blade.png').convert('RGBA')
    flash=Image.new('RGBA',(24,24));draw=ImageDraw.Draw(flash)
    draw.polygon([(12,1),(15,9),(23,12),(15,15),(12,23),(9,15),(1,12),(9,9)],fill=(225,245,255,210))
    save('pose_flash',flash)
    # Tapered sweep painted from the actual tip back toward the hand; same canvas/anchor.
    for prefix, blue in [('swing',False),('swing_skill',True)]:
        for i in range(5):
            trail=Image.new('RGBA',canvas.size)
            if i in [1,2,3]:
                draw=ImageDraw.Draw(trail)
                color=(105,210,255) if blue else (245,248,255)
                tx,ty=anchors['tip']
                for step in range(64):
                    t=step/63
                    x=tx-(length+105)*t
                    y=ty+math.sin(t*math.pi)*(18 if i==2 else 12)
                    radius=(1-t)*(5 if blue else 3)+.5
                    draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(*color,round(235*(1-t)**.7)))
            save(f'{prefix}_mask_{i}',trail)
            composed=Image.open(ART/f'{prefix}_mask_{i}.png').convert('RGBA');composed.alpha_composite(blade)
            save(f'{prefix}_{i}',composed,{'trail_mask':f'{prefix}_mask_{i}','blade_asset':'attack_blade',
                 'has_trail':i in [1,2,3],'pose_role':['guard','pull','sweep','hold','recover'][i]})
    # Source frame IDs map onto our already painted pose slots, not copied artwork.
    for action in ['slash','tram_kiem','shoot','xa_tien']:
        school=s['skills'][action]['school']; key='kiem_1' if school=='kiem' else 'cung_28'
        for mode in ['ground','air']:
            rows=[]
            for i, b in enumerate(ref['chieu'][key][mode]):
                frame=b['khung_than']
                if school=='kiem':
                    fx=min(i,4); fx=3 if i in [3,4] else fx
                    prefix='swing_skill' if action=='tram_kiem' else 'swing'
                    effects=[{'id':f'{prefix}_{fx}','dx':0,'dy':0}]
                    proj=None; nocked=False; ready=None
                else:
                    bow='bow_draw' if i<2 else ('bow_draw_hold' if i<4 else 'bow_release')
                    effects=[{'id':bow,'dx':0,'dy':0}]
                    proj={'id':'skill_arrow' if action=='xa_tien' else 'arrow','dx':b['dan']['dx']*3,'dy':b['dan']['dy']*3,'register_to_string':True} if b['dan'] else None
                    nocked=i<4;ready=('arrow_draw_15' if i<2 else 'arrow_draw_16') if nocked else None
                rows.append({'frame':frame,'duration':.05,'effects':effects,'projectile':proj,
                             'nocked':nocked,'nocked_asset':ready,'reference':b})
            s['skills'][action][mode]=rows
        s['skills'][action]['reference_skill']=key
    for name,data in [('parts',p),('frames30',f),('skills',s)]:
        (D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Registered painted necks; 30 numeric reference rows; full .78H blades; Kiếm6 / Cung8-ground,7-air reference beats.')

if __name__=='__main__':
    main()
    from build_run_cycle_v3 import run as update_running
    update_running()
    from build_carry_v4 import run as update_carry
    update_carry()
    from build_weapon_masters_v5 import run as update_weapon_masters
    update_weapon_masters()
    from build_chest_carry_v7 import run as update_chest_carry
    update_chest_carry()

    from raise_held_arms_v8 import run as raise_held_arms
    raise_held_arms()
    from build_held_props_v8 import run as update_held_props
    update_held_props()
