#!/usr/bin/env python3
"""Check PNGs and gaps on actual scene-evaluated Sprite2D transforms. No imagegen."""
from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageDraw
from snap_pixel import load_groups
from render_parts_scene import sprite_layer
ROOT=Path(__file__).resolve().parents[1]
def main():
    groups=load_groups(ROOT/'art/reference/palette.gpl');pal={c for g in ['outline','skin','fabric','belt','pants','limestone'] for c in groups[g]}
    definition=json.loads((ROOT/'prototype/rig/data/parts.json').read_text());parts={p['id']:p for p in definition['parts']};failed=0
    for id,p in parts.items():
        path=ROOT/f'art/sprites/characters/chr_dbl_parts/{id}.png';im=Image.open(path).convert('RGBA');a=np.asarray(im)
        colours={tuple(px) for px in a[:,:,:3][a[:,:,3]>0]};bad=sum(tuple(px) not in pal for px in a[:,:,:3][a[:,:,3]>0]);semi=int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum())
        same=path.read_bytes()==(ROOT/f'prototype/rig/art_parts/{id}.png').read_bytes();ok=im.size==tuple(p['size']) and bad==0 and semi==0 and same
        failed+=not ok;print(f'{"PASS" if ok else "FAIL"}: {id} size={im.size} expected={p["size"]} off_palette={bad} semi_alpha={semi} scene_copy_identical={same}')
    data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());details=[];checks=0
    # At 4x native sampling, count background *bounded by ink on both sides*
    # in all chords in eight directions through each joint disk. Exterior air is not a seam.
    scale=4;size=(640,640);origin=(320,504)
    for name,clip in data.items():
        if name not in json.loads((ROOT/'prototype/rig/data/animations.json').read_text())['clips']:continue
        for index,frame in enumerate(clip['frames']):
            sprites={p['id']:p for p in frame['geometry'] if p['kind']=='sprite'}
            masks={id:np.asarray(sprite_layer(p,size,origin,scale))[:,:,3]>0 for id,p in sprites.items()}
            for item in frame['geometry']:
                if item['kind']=='fill':
                    fill=Image.new('1',size);draw=ImageDraw.Draw(fill)
                    draw.polygon([(x*scale+origin[0],y*scale+origin[1]) for x,y in item['points']],fill=1)
                    masks[item['owner']] |= np.asarray(fill,dtype=bool)
            for id,p in parts.items():
                parent=p.get('art_parent',p['parent'])
                if not parent or id not in masks or parent not in masks:continue
                checks+=1;union=masks[id]|masks[parent];jx,jy=frame['joints'][id];cx=jx*scale+origin[0];cy=jy*scale+origin[1]
                radius=min(3,p['size'][0]/2)*scale;maxgap=0.0;holes=set()
                for angle in range(8):
                    theta=angle*math.pi/8
                    for offset in range(-math.floor(radius),math.floor(radius)+1):
                        chord=math.sqrt(max(0,radius*radius-offset*offset));coords=[]
                        for t in np.arange(-chord,chord+.25,.25):
                            xy=(round(cx+math.cos(theta)*t-math.sin(theta)*offset),round(cy+math.sin(theta)*t+math.cos(theta)*offset))
                            if not coords or xy!=coords[-1]:coords.append(xy)
                        occupied=[bool(union[y,x]) for x,y in coords];ink=[i for i,v in enumerate(occupied) if v]
                        if len(ink)<2:continue
                        run=[];before=None
                        for k in range(ink[0],ink[-1]+1):
                            x,y=coords[k]
                            if not occupied[k]:
                                run.append(coords[k])
                            else:
                                if run and before is not None:
                                    bx,by=before
                                    # A seam crosses from one part into the other, not a hole within one outline.
                                    crosses=(masks[id][by,bx] and masks[parent][y,x]) or (masks[parent][by,bx] and masks[id][y,x])
                                    if crosses:
                                        holes.update(run);maxgap=max(maxgap,(math.dist(run[0],run[-1])+1)/scale)
                                run=[];before=(x,y)
                # Joint must be within 1 native px of either part, even on silhouette boundary.
                near=[]
                for y in range(round(cy)-8,round(cy)+9):
                    for x in range(round(cx)-8,round(cx)+9):
                        if union[y,x]:near.append(math.hypot(x-cx,y-cy)/scale)
                distance=min(near,default=99)
                # Width of a crack is its thickness, not a grazing chord's length.
                # All bounded background samples are counted; use the union distance field.
                ink_points=np.argwhere(union[max(0,round(cy)-24):round(cy)+25,max(0,round(cx)-24):round(cx)+25])
                ink_points=ink_points+np.array([max(0,round(cy)-24),max(0,round(cx)-24)])
                gap=0.0
                for x,y in holes:
                    dist=float(np.sqrt(((ink_points-np.array([y,x]))**2).sum(axis=1).min()))
                    gap=max(gap,2*dist/scale)
                ok=gap<=1.0 and distance<=1.0
                failed+=not ok
                details.append({'clip':name,'frame':index+1,'joint':id,'background_samples':len(holes),'max_gap_px':round(gap,4),'longest_grazing_chord_px':round(maxgap,4),'joint_to_ink_px':round(distance,3),'ok':ok})
                if not ok:print(f'FAIL: {name} frame={index+1} joint={id} background_samples={len(holes)} max_gap={gap:.2f}px joint_to_ink={distance:.2f}px')
    report={'method':'Scene Sprite2D affine + actual PNG alpha; 4x nearest; all chords in eight directions across each joint disk; bounded background between different parts; width=2x maximum distance-to-union-ink at 4x; grazing chord length separately reported; <=1px thickness and <=1px joint-to-ink','checks':checks,'failures':failed,'details':details}
    target=ROOT/'prototype/rig/reports/art_checks.json';target.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'Joint checks: {checks}; max seam={max(d["max_gap_px"] for d in details):.2f}px; background samples={sum(d["background_samples"] for d in details)}; failures={failed}')
    print('Scope: all 48 authored frames / 13 actions, visible child-parent pairs; not a claim about every interpolated time or Android GPU output.')
    raise SystemExit(1 if failed else 0)
if __name__=='__main__':main()
