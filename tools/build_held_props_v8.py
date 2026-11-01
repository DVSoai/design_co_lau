#!/usr/bin/env python3
"""Original editable vector props; fixed-size exports and raised front-arm registration.
SVG drawing is authorized by the user. Existing action paint is preserved byte-for-byte.
"""
from pathlib import Path
import json,math,subprocess,copy
import numpy as np
from PIL import Image
from build_carry_v4 import position,source_origin
from weapon_v5_scope import HELD
R=Path(__file__).resolve().parents[1];D=R/'prototype/pose_rig/data';ART=R/'prototype/pose_rig/art/lv1_30';OUT=R/'art/sprites/weapons/lv1';CHAR=R/'art/sprites/characters/lv1_30'
INK='#201810'
def document(content):return '<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="-130 -150 280 280">'+content+'</svg>'
def sword_svg():
    s='<g transform="rotate(-30)" stroke="'+INK+'" stroke-width="2" stroke-linejoin="round">'
    s+='<path d="M0 0 L16 -8.5 L85 -8.5 L85 8.5 L16 8.5 Z" fill="#d9e3ed"/>'
    s+='<path d="M1 0 L16 0 L85 0 L85 7.5 L16 7.5 Z" fill="#667c93" stroke="none"/>'
    s+='<path d="M3 -1 L18 -6.5 L83 -6.5 L73 -3 L19 -2 Z" fill="#fffef5" stroke="none"/>'
    s+='<path d="M18 1 L82 1 L82 3 L23 3 Z" fill="#a4b7c9" stroke="none"/>'
    s+='<path d="M16 0 L84 0" fill="none" stroke="#405269" stroke-width=".7"/>'
    s+='<path d="M86 -3 L101 -3 L101 3 L86 3 Z" fill="#805035"/>'
    s+='<path d="M87 -2 L100 -2 L100 0 L87 0 Z" fill="#ac7650" stroke="none"/>'
    for i in range(5):
        x=87+i*2.7;s+=f'<path d="M{x} -3 L{x+2.8} 3 M{x} -2 L{x+1.2} -3" stroke="#38241c" stroke-width=".85" fill="none"/>'
    s+='<path d="M84 -11 Q86 -12 87 -9 L87 9 Q85 12 83 10 L81 -8 Z" fill="#ba8538"/>'
    s+='<path d="M83 -9 Q85 -11 86 -8 L86 5 L84 7 Z" fill="#f8d88a" stroke="none"/>'
    s+='<path d="M100 -3 L103 -3 L104 1 L102 3 L100 3 Z" fill="#d6a348"/>'
    s+='<path d="M103 0 Q108 -5 112 -3 L111 0 L113 2 Q107 4 103 1 Z" fill="#b72d27" stroke-width="1"/>'
    s+='<path d="M105 0 L110 -2" stroke="#f25d41" stroke-width=".7"/>'
    return document(s+'</g>')
def bow_svg():
    # Local tip axis is vertical. One offline rotation makes top forward/right.
    s='<g transform="rotate(23)" stroke="'+INK+'" stroke-linejoin="round">'
    s+='<path d="M0 -66 L0 66" stroke="#352b26" stroke-width=".75" fill="none"/>'
    # Deep C, slim limbs, with tiny counter-curled ends.
    s+='<path d="M-3 -65 Q-8 -71 -1 -69 Q0 -63 7 -59 C35 -47 52 -26 52 0 C52 26 35 47 7 59 Q0 63 -1 69 Q-8 71 -3 65" stroke-width="5.2" stroke-linecap="round" fill="none"/>'
    s+='<path d="M-3 -65 Q-7 -69 -1 -68 Q0 -62 7 -59 C35 -47 52 -26 52 0 C52 26 35 47 7 59 Q0 62 -1 68 Q-7 69 -3 65" stroke="#9c6851" stroke-width="1.7" stroke-linecap="round" fill="none"/>'
    s+='<path d="M4 -60 C34 -46 51 -25 51 -7 M51 7 C51 25 34 46 4 60" stroke="#dfb47c" stroke-width=".8" fill="none"/>'
    s+='<path d="M51.8 -51 C55 -42 45 -35 45 -28" stroke="none" fill="none"/>'
    # Centre leather wraps and brass collars, visibly distinct from wood.
    s+='<path d="M49 -7 Q52 -8 55 -7 L55 7 Q52 8 49 7 Z" fill="#714334" stroke-width="1.2"/>'
    for y in [-5,-2,1,4]:s+=f'<path d="M49 {y} L55 {y+2}" stroke="#2c2020" stroke-width=".65"/>'
    for y in [-9,7]:s+=f'<path d="M49 {y} Q52 {y-1} 55 {y} L55 {y+2} L49 {y+2} Z" fill="#e3b658" stroke-width=".8"/>'
    for sign in [-1,1]:
        s+=f'<path d="M0 {sign*61} L3 {sign*63} L-1 {sign*68} L-4 {sign*66} Z" fill="#d4a24c" stroke-width="1"/>'
        s+=f'<path d="M0 {sign*62} L1 {sign*64}" stroke="#fff0ad" stroke-width=".6"/>'
    return document(s+'</g>')
def raster_svg(name,svg):
    path=OUT/(name+'_master.svg');path.write_text(svg)
    tmp=Path('/tmp')/(name+'_vector_raw.png')
    subprocess.run(['inkscape',str(path),'--export-type=png','--export-filename='+str(tmp),'--export-width=2048'],check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    im=Image.open(tmp).convert('RGBA');box=im.getbbox();return im.crop(box),np.array(box[:2],float)
def run():
    p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text())
    # Preserve accurate provenance of unchanged action paint from the previous stage.
    old=OUT/'kiem_action_material_v5.png'
    if not old.exists():old.write_bytes((OUT/'kiem_lv1_master.png').read_bytes())
    for id in ['attack_blade','attack_blade_only']+[f'{prefix}_{i}' for prefix in ['swing','swing_skill'] for i in range(5)]:p['assets'][id]['source']['master']='art/sprites/weapons/lv1/kiem_action_material_v5.png'
    for school,size,svg in [('kiem',(100,59),sword_svg()),('cung',(85,129),bow_svg())]:
        name=school+'_lv1';im,offset=raster_svg(name,svg)
        # SVG view box -> raster coordinate before crop, then exact display bbox.
        def locate(point,rotation):
            a=math.radians(rotation);v=np.array([[math.cos(a),-math.sin(a)],[math.sin(a),math.cos(a)]])@np.array(point)
            return (v+np.array([130,150]))*(2048/280)-offset
        points={'grip':locate([93,0],-30),'blade_root':locate([84,0],-30),'tip':locate([0,0],-30)} if school=='kiem' else {'grip':locate([52,0],23),'top':locate([-1,-68],23),'bottom':locate([-1,68],23),'belly':locate([52,0],23),'string':locate([0,0],23)}
        master_size=(512,round(512*size[1]/size[0])) if size[0]>=size[1] else (round(512*size[0]/size[1]),512)
        master=im.resize(master_size,Image.Resampling.LANCZOS);master.save(OUT/(name+'_master.png'))
        factor=.5*p['presentation']['display_factor'];export_size=tuple(round(v/factor) for v in size);export=im.resize(export_size,Image.Resampling.LANCZOS)
        a=np.array(export);a[a[:,:,3]<12]=0;a[a[:,:,3]==0,:3]=0;export=Image.fromarray(a)
        export.save(ART/(name+'.png'));export.save(OUT/(name+'.png'))
        anchors={k:list(v*np.array(export_size)/np.array(im.size)) for k,v in points.items()}
        if school=='kiem':
            rr,gg,bb=a[:,:,:3].astype(int).transpose(2,0,1)
            leather=(a[:,:,3]>127)&(rr>=70)&(rr<160)&(gg>=35)&(gg<115)&(rr-gg>20)&(gg-bb>10)
            hy,hx=np.where(leather);anchors['grip']=[float(hx.mean())+.5,float(hy.mean())+.5]

        p['assets'][name]={'file':name+'.png','size':list(export_size),'anchors':anchors,'source':{'master':'art/sprites/weapons/lv1/'+name+'_master.png','svg':'art/sprites/weapons/lv1/'+name+'_master.svg','export':'art/sprites/weapons/lv1/'+name+'.png','uniform_scale':export_size[0]/master_size[0],'outline_source_px':1,'display_bbox_target':list(size)},'status':'drawn_unapproved'}
        p['weapon_masters'][school]={'asset':name,'master':'art/sprites/weapons/lv1/'+name+'_master.png','master_size':list(master_size),'master_anchors':{k:list(v*np.array(master_size)/np.array(im.size)) for k,v in points.items()},'source_sheet':'original_svg_v8','offline_rotation_degrees':-30 if school=='kiem' else 23}
        (OUT/(name+'_master.prompt.txt')).write_text('Original editable SVG, user-authorized fallback B. Source: '+name+'_master.svg. Broad silver two-plane blade / slender deep C recurve with dark string. Deterministic anti-aliased export. See SVG and build_held_props_v8.py for exact construction.\n')
        (OUT/(name+'.prompt.txt')).write_text((OUT/(name+'_master.prompt.txt')).read_text())
    # Only weapon placement changes here; raised arm assets are handled separately.
    for frame in HELD:
        row=f['frames'][frame]
        for school in ['kiem','cung']:
            layer=row['layers']['body'];bid=layer.get('cung_asset' if school=='cung' else 'asset',layer.get('asset'))
            hand=position(f,row,school,'body')+np.array(p['assets'][bid]['anchors']['grip'])*.5
            own=hand-np.array(p['assets'][school+'_lv1']['anchors']['grip'])*.5
            row['registrations'][school]['weapon']=list(own-source_origin(f,row,school,'weapon'))
    for name,data in [('parts',p),('frames30',f)]:(D/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Original SVG held props: exact target display bboxes100x59 and85x129; fixed offline angles; one texture per school; action paint unchanged.')
if __name__=='__main__':run()
