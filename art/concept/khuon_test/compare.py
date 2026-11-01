#!/usr/bin/env python3
"""Actual-file comparison only: guide | generated concept in Godot | existing Lv1 in Godot."""
from pathlib import Path
from io import BytesIO
import argparse,json,subprocess,os,time,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent

def subject(im):
    box=im.getchannel('A').getbbox()
    if box is None:raise ValueError('empty image')
    return im.crop(box),box

def cell(im,opaque=False):
    if not opaque:im,_=subject(im)
    # All displayed enlargements are exact NEAREST copies of 1x128-height images.
    one=im.resize((max(1,round(im.width*128/im.height)),128),Image.Resampling.NEAREST)
    tile=Image.new('RGBA',(200,200),(24,28,36,255));tile.alpha_composite(one,((200-one.width)//2,42))
    return tile.resize((400,400),Image.Resampling.NEAREST)

def capture(attempt,godot):
    project=ROOT.parent/'.setup/khuon_preview';project.mkdir(parents=True,exist_ok=True)
    (project/'preview.gd').write_text((OUT/'render_preview.gd').read_text())
    (project/'preview.tscn').write_text('[gd_scene load_steps=2 format=3]\n[ext_resource type="Script" path="res://preview.gd" id="1"]\n[node name="Preview" type="Node"]\nscript = ExtResource("1")\n')
    (project/'project.godot').write_text('config_version=5\n[application]\nconfig/name="Pose experiment preview"\nrun/main_scene="res://preview.tscn"\n[display]\nwindow/size/viewport_width=400\nwindow/size/viewport_height=400\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n')
    command=['docker','exec','onboarding-capture','Xvfb',':124','-screen','0','400x400x24','-nolisten','tcp','-ac'];print('$',' '.join(command),flush=True)
    server=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);env=dict(os.environ,DISPLAY=':124',LIBGL_ALWAYS_SOFTWARE='1')
    try:
        for _ in range(50):
            if subprocess.run(['docker','exec','-e','DISPLAY=:124','onboarding-capture','xdpyinfo'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
            time.sleep(.1)
        else:raise RuntimeError('Xvfb not ready')
        for frame in [0,4]:
            source=OUT/f'khung_{frame:02d}_v{attempt}.png';dest=OUT/f'godot_{frame:02d}_v{attempt}'
            cmd=['docker','exec','-e','DISPLAY=:124','-e','LIBGL_ALWAYS_SOFTWARE=1','onboarding-capture',godot,'--audio-driver','Dummy','--fixed-fps','60','--path',str(project),'--windowed','--resolution','400x400','--quit-after','60','--',str(source),str(dest)];print('$',' '.join(cmd),flush=True)
            result=subprocess.run(cmd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90);print(result.stdout,end='',flush=True);print('exit='+str(result.returncode),flush=True)
            if result.returncode or 'ERROR:' in result.stdout:raise RuntimeError('Godot preview failed')
    finally:
        subprocess.run(['docker','exec','onboarding-capture','pkill','-f','^Xvfb :124 '],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        server.wait(timeout=10)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--attempt',type=int);ap.add_argument('--godot',default='/workspace/.setup/tools/godot');ap.add_argument('--selected',default='selected.json');args=ap.parse_args()
    if args.attempt:capture(args.attempt,args.godot)
    picks={str(f):args.attempt for f in [0,4]} if args.attempt else json.loads((OUT/args.selected).read_text())['selected_attempts']
    guide=json.loads(Path('/tmp/ref_pose/khuon.json').read_text());boards=[];rows=[]
    for direction in [1,-1]:
        board=Image.new('RGB',(1200,800),(24,28,36))
        for j,frame in enumerate([0,4]):
            key=f'khung_{frame:02d}_kiem';boxes=guide['khung'][key];human=[boxes[k] for k in ['dau','than','chan']];allparts=list(boxes.values());x0=min(b['x'] for b in allparts)+200;x1=max(b['x']+b['w'] for b in allparts)+200;y0=min(b['y'] for b in human)+340;y1=max(b['y']+b['h'] for b in human)+340
            pose=Image.open('/tmp/ref_pose/'+key+'.png').convert('RGBA').crop((x0,y0,x1,y1))
            if direction<0:pose=pose.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            attempt=picks[str(frame)];name=f'godot_{frame:02d}_v{attempt}_{"right" if direction>0 else "left"}.png';new=Image.open(OUT/name).convert('RGBA')
            baseline=f'prototype/pose_rig/reports/ablation_v10/kiem_{"right" if direction>0 else "left"}_{frame:02d}.png';raw=subprocess.check_output(['git','show','769be38:'+baseline],cwd=ROOT);old=Image.open(BytesIO(raw)).convert('RGBA').crop((0,0,256,256))
            for col,im in enumerate([cell(pose,True),cell(new),cell(old)]):board.paste(im,(col*400,j*400))
            rawfile=OUT/f'khung_{frame:02d}_v{attempt}.png';rawim=Image.open(rawfile).convert('RGBA');rgba=np.array(rawim);_,box=subject(rawim);_,nb=subject(new);_,ob=subject(old)
            row={'frame':frame,'direction':direction,'attempt':attempt,'raw_size':list(rawim.size),'raw_alpha_bbox':list(box),'transparent_pixels':int((rgba[:,:,3]==0).sum()),'raw_sha256':hashlib.sha256(rawfile.read_bytes()).hexdigest(),'actual_godot_bbox':list(nb),'current_godot_bbox':list(ob),'display_person_height_px':256,'current_commit':'769be38','current_actual_render':baseline,'guide_human_bbox':[x0,y0,x1,y1]};rows.append(row);print(json.dumps(row,ensure_ascii=False))
        boards.append(board)
    name='so_sanh' if not args.attempt else 'so_sanh_v'+str(args.attempt);boards[0].save(OUT/(name+'.png'));both=Image.new('RGB',(1200,1600),(24,28,36));both.paste(boards[0],(0,0));both.paste(boards[1],(0,800));both.save(OUT/(name+'_hai_huong.png'))
    (OUT/(name+'_measurements.json')).write_text(json.dumps({'order':'guide | new actual Godot preview | current actual Godot render','rows':rows,'note':'Concept-only normalization to equal human height; no part-fit or production-rig acceptance is inferred.'},ensure_ascii=False,indent=2)+'\n');print('Saved',OUT/(name+'.png'),'(1200x800), all persons height256px; source1x -> NEAREST2x. No labels/paint added.')
if __name__=='__main__':main()
