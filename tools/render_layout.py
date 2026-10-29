#!/usr/bin/env python3
"""Render real ASCII layouts, A0-derived arcs and optional camera/control overlays.

python3 tools/render_layout.py INPUT.md OUTPUT.png [--overlay 960|1200] [--trajectories]
All drawing is deterministic PIL; no imagegen or game code/assets are changed.
"""
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from check_layout import (TILE, HEIGHT, a0, load_layout, markers, challenges, controls,
                          camera_at, camera_envelope, trajectory, evaluate)

CELL = 12
SCALE = CELL/TILE
COLORS = {
    '.': (225,232,240), '#': (125,85,55), '=': (217,178,95),
    '~': (79,143,166), '^': (178,58,46), 'L': (94,148,65),
    'S': (46,79,163), 'R': (60,190,190), 'E': (107,74,140),
    'N': (217,165,32), 'm': (230,140,120), 'M': (200,80,60),
    'B': (120,20,20), 'F': (244,241,232), 'T': (150,150,150),
    'G': (60,60,70), 'c': (255,215,0), 'D': (90,60,40),
}
ARC_COLORS = {'normal': (20,90,190,255), 'diagonal': (200,50,50,255),
              'air_jump': (120,45,180,255)}


def font(size):
    path=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    return ImageFont.truetype(str(path),size) if path.exists() else ImageFont.load_default()


def sample_arcs(rows, m):
    _, obstacles = challenges(rows, m)
    result=[]
    for c in obstacles:
        # Draw the ascending step direction. Descending steps are walked/dropped.
        direction = -1 if c['kind']=='step' and c['target_row']>c['row'] else 1
        boundary = (c['left'] if direction==1 else c['right'])*TILE
        y = (c['row'] if direction==1 else c['target_row'])*TILE
        target = (c['target_row'] if direction==1 else c['row'])*TILE
        back = 64 if c['kind']=='step' else 32 if c['kind']=='trap' else 16
        for mode in ARC_COLORS:
            # Illustrative formula arcs. Only diagonal paths from the checker are
            # the verified required crossings; air jump is never required.
            result.append((mode,trajectory(m,(boundary-direction*back,y),direction,mode,target)))
    return result


def base_grid(rows, metrics, arcs):
    width=len(rows[0]);height=len(rows)
    image=Image.new('RGB',(width*CELL,height*CELL),(255,255,255));draw=ImageDraw.Draw(image)
    for y,row in enumerate(rows):
        for x,c in enumerate(row):
            draw.rectangle((x*CELL,y*CELL,(x+1)*CELL-1,(y+1)*CELL-1),fill=COLORS[c])
            if c not in '.#=~': draw.text((x*CELL+2,y*CELL-1),c,fill='black',font=font(10))
    # Two real viewport widths: 30 cells and 37.5 cells, including fractional ticks.
    for cells,color,dash in [(30,(255,255,255),False),(37.5,(30,90,130),True)]:
        for index in range(1,math.ceil(width/cells)):
            x=round(index*cells*CELL)
            if dash:
                for y in range(0,height*CELL,10): draw.line((x,y,x,min(y+5,height*CELL-1)),fill=color)
            else:draw.line((x,0,x,height*CELL-1),fill=color)
    for mode,points in arcs:
        if len(points)>1:draw.line([(x*SCALE,y*SCALE) for x,y in points],fill=ARC_COLORS[mode][:3],width=1)
    return image


def overlay_panel(rows, metrics, width, marker):
    col,row,symbol=marker;foot=((col+.5)*TILE,(row+1)*TILE)
    world=(len(rows[0])*TILE,len(rows)*TILE)
    camera=camera_at(foot,world,width,metrics)
    # Draw at native logical resolution first; downsample only for this diagram.
    panel=Image.new('RGBA',(width,HEIGHT),(225,232,240,255));draw=ImageDraw.Draw(panel)
    def screen(x,y):return (x-camera[0]+width/2,y-camera[1]+HEIGHT/2)
    for y,line in enumerate(rows):
        for x,c in enumerate(line):
            px,py=screen(x*TILE,y*TILE)
            if px+TILE<0 or px>width or py+TILE<0 or py>HEIGHT:continue
            draw.rectangle((px,py,px+TILE-1,py+TILE-1),fill=COLORS[c])
            if c not in '.#=~': draw.text((px+8,py+4),c,fill='black',font=font(16))
    for mode,points in sample_arcs(rows,metrics):
        if len(points)>1:draw.line([screen(x,y) for x,y in points],fill=ARC_COLORS[mode],width=2)
    overlay=Image.new('RGBA',panel.size);od=ImageDraw.Draw(overlay)
    for name,rect in controls(width,metrics).items():
        od.rectangle(rect,fill=(15,25,45,115),outline=(240,245,255,230),width=2)
        od.text((rect[0]+2,rect[1]+4),name,fill='white',font=font(12))
    panel.alpha_composite(overlay);draw=ImageDraw.Draw(panel)
    sx,sy=screen(*foot);half,high=metrics['PLAYER_BOX'][0]/2,metrics['PLAYER_BOX'][1]
    draw.rectangle((sx-half,sy-high,sx+half,sy),outline=(0,255,255,255),width=3)
    # Dead zone around current reset anchor, and look-ahead vector to camera.
    dx,dy=metrics['CAMERA_DEAD_ZONE'];draw.rectangle((sx-dx,sy-dy,sx+dx,sy+dy),outline=(20,120,30,255),width=2)
    draw.line((sx,sy,sx+metrics['CAMERA_LOOK_AHEAD'],sy),fill=(20,120,30,255),width=2)
    return panel.convert('RGB'), camera, camera_envelope(foot,world,width,metrics)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source');parser.add_argument('output')
    parser.add_argument('--overlay',type=int,choices=[960,1200])
    parser.add_argument('--trajectories',action='store_true')
    args=parser.parse_args();rows,config=load_layout(args.source);m=a0()
    arcs=sample_arcs(rows,m) if args.trajectories else []
    grid=base_grid(rows,m,arcs)
    header=64;gutter=20;panels=[]
    if args.overlay:
        # Refuse an unsafe overlay rather than producing a misleading green diagram.
        checked=evaluate(args.source)
        if checked['failures']:raise SystemExit('FAIL: '+str(checked['failures']))
        for marker in markers(rows,'SR'):
            panel,camera,envelope=overlay_panel(rows,m,args.overlay,marker)
            panels.append((panel,marker,camera,envelope))
    output_width=max(grid.width+gutter*2,(args.overlay or 0)+gutter*2)
    output_height=header+grid.height+gutter+len(panels)*(HEIGHT+50)
    image=Image.new('RGB',(output_width,output_height),(248,248,248));draw=ImageDraw.Draw(image)
    draw.text((gutter,5),Path(args.source).name+' — Tạm thời, chưa duyệt',fill='black',font=font(16))
    draw.text((gutter,28),'Vạch trắng: 30 ô / 960px; xanh đứt: 37,5 ô / 1200px. Ô=32px; sơ đồ=12px/ô.',fill='black',font=font(13))
    draw.text((gutter,45),'Quỹ đạo: xanh=thường; đỏ=chéo; tím=khinh công mẫu (không bắt buộc). Cyan=hitbox.',fill='black',font=font(12))
    image.paste(grid,(gutter,header));y=header+grid.height+gutter
    for panel,marker,camera,envelope in panels:
        col,row,sym=marker
        draw.text((gutter,y),f'{sym} c{col},r{row} — viewport {args.overlay}×540; cx/cy={camera}; miền kiểm={tuple(round(v,1) for v in envelope)}',fill='black',font=font(13))
        image.paste(panel,(gutter,y+28));y+=HEIGHT+50
    Path(args.output).parent.mkdir(parents=True,exist_ok=True);image.save(args.output)
    print(f'{args.output}: grid={len(rows[0])}x{len(rows)}, PNG={image.width}x{image.height}; ticks=30/37.5 cells; overlay={args.overlay or "none"}; snapshots={len(panels)}; formula_arcs={len(arcs)}')
    for _,marker,camera,envelope in panels:print(f'  {marker}: camera={camera}; checked envelope={envelope}; source=A0 + visible viewport; map-edge clamp enabled')


if __name__=='__main__':main()
