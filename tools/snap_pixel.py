#!/usr/bin/env python3
"""Snap a concept's native pixel grid; NEVER rescale a non-96px character."""
import argparse
from pathlib import Path
import numpy as np
from PIL import Image

BG=np.array((0,255,0),dtype=np.uint8)
ALLOWED={'outline','skin','fabric','belt','pants'}
FORBIDDEN={'limestone','young_rice','ripe_rice','water','reed_red','highlight'}

def load_groups(path):
    groups={}
    for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
        bits=line.split()
        if len(bits)>=4 and all(v.isdigit() for v in bits[:3]):
            rgb=tuple(map(int,bits[:3]));groups.setdefault(bits[3],[]).append(rgb)
    if sum(map(len,groups.values()))!=32: raise ValueError('Expected 32 GPL entries')
    return groups

def green_mask(a):
    b=a.astype(np.int32)
    return (b[...,1]>105)&(b[...,1]>b[...,0]*1.45)&(b[...,1]>b[...,2]*1.4)

def detect_period(a,axis,max_period=16):
    """Normalized autocorrelation of adjacent-pixel RGB edge energy."""
    d=np.abs(np.diff(a.astype(np.float32),axis=axis)).mean(axis=2)
    edge=d.mean(axis=0 if axis==1 else 1)
    edge-=edge.mean();denom=float(edge@edge)
    if denom<1e-8: return 1,[]
    scores=[]
    for p in range(2,min(max_period+1,len(edge)//3)):
        score=float(edge[:-p]@edge[p:]/denom)
        scores.append((p,round(score,5)))
    candidates=[(p,s) for p,s in scores if s>=.30]
    return (max(candidates,key=lambda v:v[1]-.012*v[0])[0] if candidates else 1),scores

def nearest(c,pal):
    p=np.asarray(pal,dtype=float);delta=p-np.asarray(c,dtype=float)
    lum=delta@np.array([.2126,.7152,.0722]);distance=np.sum(delta**2*np.array([.30,.59,.11]),axis=1)+1.3*lum**2
    return tuple(map(int,p[int(np.argmin(distance))]))

def run(args):
    groups=load_groups(args.palette)
    names=[s.strip() for s in args.groups.split(',') if s.strip()]
    if not names or set(names)-ALLOWED:raise ValueError('Only character groups allowed: '+','.join(sorted(ALLOWED)))
    pal=[rgb for name in names for rgb in groups.get(name,[])]
    if len(pal)!=17 and set(names)==ALLOWED:raise ValueError(f'Expected 17 character colors, got {len(pal)}')
    src=np.asarray(Image.open(args.input).convert('RGB'))
    fg=~green_mask(src);ys,xs=np.where(fg)
    if not len(xs):raise ValueError('No character pixels')
    crop=src[ys.min():ys.max()+1,xs.min():xs.max()+1]
    px,sx=detect_period(crop,1);py,sy=detect_period(crop,0)
    h,w=crop.shape[:2];oh=(h+py-1)//py;ow=(w+px-1)//px
    print(f'input={args.input}')
    print(f'crop_size={w}x{h}')
    print(f'grid_period_x={px} grid_period_y={py}')
    print(f'grid_cells={ow}x{oh}')
    print(f'groups={",".join(names)} palette_colors={len(pal)}')
    print(f'grid_x_scores={sx}')
    print(f'grid_y_scores={sy}')
    # HARD STOP: must not create output if native grid is not close to 96.
    if not 94<=oh<=98:
        raise ValueError(f'REJECT: native character grid height={oh}, expected 96±2; no resizing or output')
    sample=np.empty((oh,ow,3),dtype=np.uint8);sample[:]=BG
    for y in range(oh):
        for x in range(ow):
            tile=crop[y*py:min((y+1)*py,h),x*px:min((x+1)*px,w)]
            mask=green_mask(tile)
            if mask.mean()>.5:continue
            sample[y,x]=nearest(np.median(tile[~mask],axis=0),pal)
    ys,xs=np.where(np.any(sample!=BG,axis=2))
    if not len(xs):raise ValueError('No foreground after snapping')
    tight=sample[ys.min():ys.max()+1,xs.min():xs.max()+1]
    th,tw=tight.shape[:2]
    if th!=96:raise ValueError(f'REJECT: snapped silhouette height={th}; must be exactly 96 without resizing')
    if tw>128:raise ValueError(f'REJECT: width {tw}>128')
    canvas=Image.new('RGB',(128,128),(0,255,0))
    canvas.paste(Image.fromarray(tight),((128-tw)//2,128-8-th))
    Path(args.output).parent.mkdir(parents=True,exist_ok=True)
    canvas.save(args.output)
    canvas.resize((512,512),Image.Resampling.NEAREST).save(args.x4)
    print(f'output={args.output}')
    print(f'output_x4={args.x4}')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('input','palette','output','x4'):ap.add_argument('--'+k,required=True)
    ap.add_argument('--groups',default='outline,skin,fabric,belt,pants')
    run(ap.parse_args())
