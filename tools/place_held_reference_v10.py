#!/usr/bin/env python3
"""Use frame0 origin + exact reference deltas; redraw only the following front arm."""
from pathlib import Path
import json,copy,math,subprocess,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from build_carry_v4 import position,source_origin
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'prototype/pose_rig/data';ART=ROOT/'prototype/pose_rig/art/lv1_30';OUT=ROOT/'art/sprites/characters/lv1_30';SRC=OUT/'sources';HELD=[0,1,2,3,4,5,6,7,12,21]
ET.register_namespace('','http://www.w3.org/2000/svg')
def run():
    p=json.loads((DATA/'parts.json').read_text());f=json.loads((DATA/'frames30.json').read_text());before=copy.deepcopy(f);factor=p['presentation']['display_factor'];screen_unit=128/131*4;logic_unit=screen_unit/factor
    if 'held_reference_base_v10' not in f:
        f['held_reference_base_v10']={'anchor_frame':0,'display_pixels_per_reference_unit':screen_unit,'origins':{school:position(f,f['frames'][0],school,'weapon').tolist() for school in ['kiem','cung']},'body_assets':{str(i):f['frames'][i]['layers']['body']['asset'] for i in HELD}}
    saved=f['held_reference_base_v10'];base_ref=np.array(f['frames'][0]['reference']['vu_khi'][1:],float)
    def raster(svg_path,stem):
        tmp=Path('/tmp')/(stem+'.png');subprocess.run(['inkscape',str(svg_path),'--export-type=png','--export-filename='+str(tmp),'--export-width=1280'],check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);return Image.open(tmp).convert('RGBA').resize((320,256),Image.Resampling.LANCZOS)
    for frame in HELD:
        row=f['frames'][frame];delta=np.array(row['reference']['vu_khi'][1:],float)-base_ref;delta[1]*=-1;delta*=logic_unit
        targets={}
        for school in ['kiem','cung']:
            top=np.array(saved['origins'][school])+delta;row['registrations'][school]['weapon']=(top-source_origin(f,row,school,'weapon')).tolist()
            grip=top+np.array(p['assets'][school+'_lv1']['anchors']['grip'])*.5;targets[school]=(grip-position(f,row,school,'body'))*2
        assert np.allclose(targets['kiem'],targets['cung'],atol=1e-9)
        if frame==0:continue
        base=saved['body_assets'][str(frame)];a=copy.deepcopy(p['assets'][base]);im=Image.open(ART/a['file']).convert('RGBA');arr=np.array(im);old_roi=np.array(Image.open(ROOT/a['source']['roi']))>0;arr[old_roi]=0
        nx,ny=a['anchors']['neck'];h=targets['kiem'];shoulder=np.array([nx+13,ny+11]);v=h-shoulder;distance=np.linalg.norm(v);length=max(24.,distance*.5+3);mid=(shoulder+h)*.5;normal=np.array([-v[1],v[0]])/max(distance,1e-9);height=math.sqrt(max(0,length*length-distance*distance*.25));candidates=[mid+normal*height,mid-normal*height]
        elbow=max(candidates,key=lambda q:q[0]) if h[0]<shoulder[0]-4 else max(candidates,key=lambda q:q[1]);toward=(elbow-h)/np.linalg.norm(elbow-h);side=np.array([-toward[1],toward[0]])
        start=f'<svg xmlns="http://www.w3.org/2000/svg" width="320" height="256" viewBox="0 0 320 256"><g stroke-linejoin="round" stroke-linecap="round">'
        curve=f'M{shoulder[0]} {shoulder[1]} L{elbow[0]} {elbow[1]} L{h[0]} {h[1]}'
        content=f'<path d="{curve}" stroke="#2b1b12" stroke-width="11.5" fill="none"/><path d="{curve}" stroke="#ec984e" stroke-width="8" fill="none"/>'
        shifted=[q+[-1,-1] for q in [shoulder,elbow,h]];lit='M'+' L'.join(f'{q[0]} {q[1]}' for q in shifted);content+=f'<path d="{lit}" stroke="#ffc076" stroke-width="3" fill="none"/>'
        corners=[h+toward*5+side*5,h+toward*15+side*5,h+toward*15-side*5,h+toward*5-side*5];poly='M'+' L'.join(f'{q[0]} {q[1]}' for q in corners)+' Z';content+=f'<path d="{poly}" fill="#724330" stroke="#2b1b12" stroke-width="1.5"/>'
        for d in [7,10,13]:
            q=h+toward*d;l=q+side*4;r=q-side*4;content+=f'<path d="M{l[0]} {l[1]} L{r[0]} {r[1]}" stroke="#a2673b" stroke-width="1"/>'
        # Reuse precisely the existing original fist drawing, translated, not redesigned.
        old_svg=ET.parse(ROOT/a['source']['svg']).getroot();group=list(old_svg)[0];old_hand=np.array(a['anchors']['grip']);shift=h-old_hand
        fist='<g stroke="#2b1b12" stroke-width="1.7" stroke-linejoin="round" transform="translate('+str(shift[0])+' '+str(shift[1])+')">'+''.join(ET.tostring(e,encoding='unicode') for e in list(group)[-2:])+'</g>'
        stem=f'held_ref_{frame:02d}_v10';svg_path=SRC/(stem+'.svg');svg_path.write_text(start+content+fist+'</g></svg>');arm=raster(svg_path,stem);paint=np.array(arm);roi=old_roi|(paint[:,:,3]>0)
        result=Image.fromarray(arr);result.alpha_composite(arm);rgba=np.array(result);assert np.array_equal(rgba[~roi],np.array(im)[~roi])
        hand_path=SRC/(stem+'_hand.svg');hand_path.write_text(start+fist+'</g></svg>');hand=np.array(raster(hand_path,stem+'_hand'));rr,gg,bb=hand[:,:,:3].astype(int).transpose(2,0,1);hand[(rr<153)|(gg<76)|(rr-gg<20)]=0;hand[hand[:,:,3]==0,:3]=0
        for folder in [ART,OUT]:result.save(folder/(stem+'.png'));Image.fromarray(hand).save(folder/(stem+'_hand.png'))
        Image.fromarray((roi*255).astype('uint8')).save(SRC/(stem+'_roi.png'))
        a['file']=stem+'.png';a['anchors']['grip']=h.tolist();a['anchors']['near_hand']=h.tolist();a['source']={'own_base':base,'authorized_front_arm_only':True,'svg':str(svg_path.relative_to(ROOT)),'roi':str((SRC/(stem+'_roi.png')).relative_to(ROOT)),'held_hand_overlay':stem+'_hand.png','reference_frame':frame,'palm_target_source':h.tolist()};p['assets'][stem]=a
        (OUT/(stem+'.prompt.txt')).write_text('Original front-arm-only SVG; reference-delta placement relative to unchanged frame0. Fist reuses original own art by translation. See sources/'+stem+'.svg.\n')
        row['layers']['body']['asset']=stem;row['layers']['body']['cung_asset']=stem
        print(f'frame{frame:02d}: reference dx/dy={row["reference"]["vu_khi"][1:]}, delta display={(delta*factor).tolist()}, desired source palm={h.tolist()}')
    assert all(f['frames'][i]==before['frames'][i] for i in range(30) if i not in HELD)
    for name,data in [('parts',p),('frames30',f)]:(DATA/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print('Reference held positions: frame0 preserved;10 frames x2 schools use exact delta128/131*4 and root mirroring; weapon art unchanged.')
if __name__=='__main__':run()
