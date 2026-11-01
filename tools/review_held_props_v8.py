#!/usr/bin/env python3
"""Assemble real render reviews; original reference pixels stay outside the repository."""
from pathlib import Path
import argparse,json,math
from PIL import Image,ImageDraw,ImageFont
from ref_render import load_parts,load_frames
R=Path(__file__).resolve().parents[1];REPORT=R/'prototype/pose_rig/reports';OUT=R/'art/sprites/weapons/lv1'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';BG=(32,40,51,255)
def caption(im,xy,text,size=22):ImageDraw.Draw(im).text(xy,text,font=ImageFont.truetype(FONT,size),fill='white')
def full(school,frame,renders):
    im=Image.open(R/renders/f'{school}_right_{frame:02d}.png').convert('RGBA');return im.crop((0,0,256,256))
def put_actor(im,actor,cx,baseline,scale=2):
    actor=actor.resize((round(actor.width*scale),round(actor.height*scale)),Image.Resampling.NEAREST)
    im.alpha_composite(actor,(round(cx-128*scale),round(baseline-210*scale)))
def masters(im):
    caption(im,(30,15),'Lv1 • H128 • ảnh Godot thật ×2 • CHƯA DUYỆT',28)
    for school,x in [('kiem',90),('cung',1000)]:
        master=Image.open(OUT/(school+'_lv1_master.png')).convert('RGBA');master.thumbnail((550,390),Image.Resampling.LANCZOS);im.alpha_composite(master,(x,65));caption(im,(x,470),school+' • nguồn SVG chỉnh màu được')
def original(source,client,school,frame):
    parts=load_parts(source/'res/cache/data/nj_part');rows=load_frames(client/'src/Char.java');icon=source/'res/icon/4';cv=Image.new('RGBA',(256,256))
    # Formula and numbers only; references are composed only for the external board.
    for layer,part in [(1,parts[0][1]),(2,parts[1][1]),(0,parts[2][1]),(3,parts[12 if school=='kiem' else 14][1])]:
        idx,dx,dy=rows[frame][layer];iid,px,py=part[idx]
        if iid<=0:continue
        tile=Image.open(icon/f'{iid}.png').convert('RGBA');s=128/131;tile=tile.resize((round(tile.width*s),round(tile.height*s)),Image.Resampling.LANCZOS)
        cv.alpha_composite(tile,(round(128+(dx+px)*4*s),round(210+(-dy+py)*4*s)))
    return cv

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--renders',default='prototype/pose_rig/reports/ablation_v10');ap.add_argument('--server',type=Path,required=True);ap.add_argument('--client',type=Path,required=True);ap.add_argument('--comparison-out',type=Path,default=Path('/tmp/ref_render/review_lv1.png'));args=ap.parse_args()
    resolved=args.comparison_out.resolve();assert not resolved.is_relative_to(R),'Do not write original reference pixels inside repo'
    own=Image.new('RGBA',(1600,980),BG);masters(own)
    for i,(school,frame) in enumerate([('kiem',0),('kiem',4),('cung',0),('cung',4)]):
        caption(own,(i*400+35,535),f'{school} • khung {frame} • H128 ×2');put_actor(own,full(school,frame,args.renders),i*400+230,940)
    temporary=OUT/'review_lv1.new.png';own.convert('RGB').save(temporary);temporary.replace(OUT/'review_lv1.png')
    comparison=Image.new('RGBA',(1600,1500),BG);masters(comparison)
    for i,(school,frame) in enumerate([('kiem',0),('kiem',4),('cung',0),('cung',4)]):
        col=i%2;row=i//2;left=col*800;baseline=960+row*450
        caption(comparison,(left+30,550+row*450),f'{school} • khung {frame} • cùng H128 ×2')
        caption(comparison,(left+65,590+row*450),'Tự vẽ / Godot');caption(comparison,(left+465,590+row*450),'Tham khảo / 128÷131')
        put_actor(comparison,full(school,frame,args.renders),left+230,baseline);put_actor(comparison,original(args.server,args.client,school,frame),left+610,baseline)
    resolved.parent.mkdir(parents=True,exist_ok=True);comparison.convert('RGB').save(resolved)
    print('Own art only:',OUT/'review_lv1.png','1600x980; actual GPU poses0/4, both schools, exact2x nearest zoom')
    print('Original references ONLY OUTSIDE repository:',resolved,'1600x1500; equal neutral H128, exact2x nearest zoom')
if __name__=='__main__':main()
