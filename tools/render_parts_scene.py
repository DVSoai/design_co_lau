#!/usr/bin/env python3
"""Rasterize actual Sprite2D transforms exported by Godot; alpha is read from real PNGs."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]

def sprite_layer(part,size,origin,scale=1):
    src=Image.open(ROOT/'prototype'/part['source'].removeprefix('res://')).convert('RGBA')
    a,b,c,d,tx,ty=part['transform'];det=a*d-b*c
    # output -> input affine, matching nearest-filtered Sprite2D at pixel centres.
    ox,oy=origin
    coeff=(d/(det*scale),-c/(det*scale),(-d*(ox+tx*scale)+c*(oy+ty*scale))/(det*scale),
           -b/(det*scale),a/(det*scale),(b*(ox+tx*scale)-a*(oy+ty*scale))/(det*scale))
    return src.transform(size,Image.Transform.AFFINE,coeff,resample=Image.Resampling.NEAREST)

def layers(frame,size=(160,160),origin=(80,126),scale=1):
    result=[]
    for part in sorted(frame['geometry'],key=lambda p:p['z']):
        if part['kind']=='sprite':layer=sprite_layer(part,size,origin,scale)
        else:
            layer=Image.new('RGBA',size);draw=ImageDraw.Draw(layer)
            points=[(x*scale+origin[0],y*scale+origin[1]) for x,y in part['points']]
            if part['kind']=='fill':draw.polygon(points,fill='#'+part['color'][:6])
            else:draw.line(points,fill='#'+part['color'][:6],width=max(1,round(part['width']*scale)))
        result.append((part['id'],layer))
    return result

def main():
    data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text())
    out=ROOT/'prototype/rig/contact_sheets/art';out.mkdir(parents=True,exist_ok=True)
    names=[name for name in data if name!='standing_neutral']
    for name in names:
        sheet=Image.new('RGBA',(160*len(data[name]['frames']),160),(32,40,50,255))
        for i,frame in enumerate(data[name]['frames']):
            cell=Image.new('RGBA',(160,160),(32,40,50,255));ImageDraw.Draw(cell).line((0,126,159,126),fill='#62707D')
            for _,layer in layers(frame):cell.alpha_composite(layer)
            sheet.alpha_composite(cell,(160*i,0))
        target=out/f'chr_dbl_anim_{name}_art.png';sheet.convert('RGB').save(target)
        print(f'{target.relative_to(ROOT)} {sheet.width}x{sheet.height} frames={len(data[name]["frames"])}')
    idle=Image.new('RGBA',(128,128))
    for _,layer in layers(data['idle']['frames'][0],(128,128),(64,120)):idle.alpha_composite(layer)
    idle.save(out/'chr_dbl_idle_art_1x.png')
    Image.open(out/'chr_dbl_idle_art_1x.png').resize((512,512),Image.Resampling.NEAREST).save(out/'chr_dbl_idle_art_4x.png')
    print('idle: 128x128 -> 512x512 using Image.resize(..., Image.Resampling.NEAREST) from saved 1x')
if __name__=='__main__':main()
