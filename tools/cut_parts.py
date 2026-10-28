#!/usr/bin/env python3
"""Split the actual generated sheet; median-cell snapping, 17-colour palette, joint overdraw.
No imagegen here. Does not change approved files. Head corrections are explicit data.
"""
import argparse,json,math,hashlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image
from snap_pixel import green_mask,detect_period,nearest,load_groups
ROOT=Path(__file__).resolve().parents[1]
ORDER=['head','body','upper_arm_near','upper_arm_far','forearm_near','forearm_far','hand_near','hand_far','thigh_near','thigh_far','shin_near','shin_far','foot_near','foot_far','dao','bow']
GROUPS=['outline','skin','fabric','belt','pants']

def components(mask):
    seen=np.zeros(mask.shape,bool); result=[]; h,w=mask.shape
    for y,x in zip(*np.where(mask)):
        if seen[y,x]:continue
        todo=[(int(x),int(y))];seen[y,x]=True;points=[]
        while todo:
            xx,yy=todo.pop();points.append((xx,yy))
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx,ny=xx+dx,yy+dy
                if 0<=nx<w and 0<=ny<h and mask[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx]=True;todo.append((nx,ny))
        result.append(points)
    return result

def median_cells(rgb,mask,width,height):
    """Every output cell uses the median of its source rectangle, never NEAREST decimation."""
    h,w=mask.shape;out=np.zeros((height,width,4),np.uint8)
    for y in range(height):
        for x in range(width):
            x0=int(x*w/width);x1=max(x0+1,math.ceil((x+1)*w/width))
            y0=int(y*h/height);y1=max(y0+1,math.ceil((y+1)*h/height))
            region=mask[y0:y1,x0:x1]
            if region.mean()>=.35:
                out[y,x,:3]=np.median(rgb[y0:y1,x0:x1][region],axis=0)
                out[y,x,3]=255
    return out

def fill_cap(a,point,diameter,down=True):
    """Automatic occluded fill: sample the median adjacent material, extend a semicircle."""
    px,py=point;h,w=a.shape[:2];r=diameter/2
    neighbourhood=a[max(0,int(py-r)):min(h,math.ceil(py+r+1)),max(0,int(px-r)):min(w,math.ceil(px+r+1))]
    pixels=neighbourhood[neighbourhood[:,:,3]>0,:3]
    if not len(pixels):pixels=a[a[:,:,3]>0,:3]
    colour=np.median(pixels,axis=0).astype(np.uint8)
    for y in range(h):
        for x in range(w):
            dx=max(x-px,px-(x+1),0);dy=max(y-py,py-(y+1),0)
            if dx*dx+dy*dy <= r*r and (y<=py if down else y+1>=py):
                a[y,x]=[*colour,255]

def clean_outline(a,outline):
    mask=a[:,:,3]>0
    for cluster in components(mask):
        if len(cluster)<2:
            for x,y in cluster:a[y,x]=0
    mask=a[:,:,3]>0; padded=np.pad(mask,1)
    interior=padded[1:-1,1:-1]&padded[:-2,1:-1]&padded[2:,1:-1]&padded[1:-1,:-2]&padded[1:-1,2:]
    a[mask&~interior,:3]=outline
    a[~mask]=0
    return a

def matrix(a,pal):
    chars='0123456789ABCDEFG';lookup={tuple(c):chars[i] for i,c in enumerate(pal)}
    return '\n'.join(''.join(lookup[tuple(px[:3])] if px[3] else '.' for px in row) for row in a)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',default='art/concept/characters/chr_dbl_parts_concept.png');args=ap.parse_args()
    groups=load_groups(ROOT/'art/reference/palette.gpl');pal=[c for name in GROUPS for c in groups[name]];assert len(pal)==17
    definition=json.loads((ROOT/'prototype/rig/data/parts.json').read_text());parts={p['id']:p for p in definition['parts']}
    source=ROOT/args.source;rgb=np.array(Image.open(source).convert('RGB'));mask=~green_mask(rgb)
    clusters=[c for c in components(mask) if len(c)>100]
    assert len(clusters)==16,f'Expected exactly 16 isolated foreground regions, found {len(clusters)}; inspect source, no guessed crops'
    clusters.sort(key=lambda c:sum(y for x,y in c)/len(c));ordered=[]
    for row in range(4):ordered+=sorted(clusters[row*4:row*4+4],key=lambda c:sum(x for x,y in c)/len(c))
    out=ROOT/'art/sprites/characters/chr_dbl_parts';out.mkdir(parents=True,exist_ok=True)
    report=ROOT/'art/concept/characters/chr_dbl_parts_work';report.mkdir(parents=True,exist_ok=True)
    patch_path=ROOT/'tools/chr_dbl_head_edits.json';patches=json.loads(patch_path.read_text()) if patch_path.exists() else []
    manifest={'status':'Đang làm — chưa duyệt','source':args.source,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'palette':[list(c) for c in pal],'parts':[],'automatic_fill':'median-material semicircles at joint ends, within prescribed canvas; not artist-painted hidden anatomy'}
    for id,cluster in zip(ORDER,ordered):
        part=parts[id];xs,ys=zip(*cluster);x0,x1=min(xs),max(xs)+1;y0,y1=min(ys),max(ys)+1
        crop=rgb[y0:y1,x0:x1];cmask=np.zeros(crop.shape[:2],bool)
        for x,y in cluster:cmask[y-y0,x-x0]=True
        px,_=detect_period(crop,1);py,_=detect_period(crop,0)
        grid=median_cells(crop,cmask,math.ceil(crop.shape[1]/px),math.ceil(crop.shape[0]/py))
        a=median_cells(grid[:,:,:3],grid[:,:,3]>0,*part['size'])
        Image.fromarray(a).save(report/f'{id}_scaled.png')
        # Joint cap: expand back towards the hidden proximal end, within the same target canvas.
        fill_cap(a,part['pivot'],8 if id=='head' else part['size'][0],True)
        fill_cap(a,part['pivot'],8 if id=='head' else part['size'][0],False)
        # Extend parent-side material round the attachment points hidden by children.
        for child in definition['parts']:
            if child['parent']==id:
                anchor=[part['pivot'][i]+child['attach'][i] for i in range(2)]
                fill_cap(a,anchor,min(part['size'][0],child['size'][0]),False)
                fill_cap(a,anchor,min(part['size'][0],child['size'][0]),True)
        for y,x in zip(*np.where(a[:,:,3]>0)):a[y,x,:3]=nearest(a[y,x,:3],pal)
        a=clean_outline(a,pal[0])
        if id=='head':
            Image.fromarray(a).save(report/'head_before.png')
            before=matrix(a,pal);(report/'head_before.txt').write_text(before+'\n')
            print('HEAD BEFORE (24 rows x 18 chars; . transparent, 0..G palette):\n'+before)
            for patch in patches:
                x,y,c=patch['x'],patch['y'],patch['index'];assert 0<=x<18 and 0<=y<24 and 0<=c<17
                a[y,x]=[*pal[c],255]
            a=clean_outline(a,pal[0])
            Image.fromarray(a).save(report/'head_after.png');after=matrix(a,pal)
            (report/'head_after.txt').write_text(after+'\n');print('HEAD AFTER:\n'+after)
        Image.fromarray(a).save(out/f'{id}.png')
        manifest['parts'].append({'id':id,'source_box':[x0,y0,x1,y1],'source_area':len(cluster),'detected_grid':[px,py],'snapped_grid':[grid.shape[1],grid.shape[0]],'size':part['size'],'pivot':part['pivot'],'file':str((out/f'{id}.png').relative_to(ROOT))})
        print(f'{id}: source={x1-x0}x{y1-y0}; grid={px}x{py}; median -> {part["size"]}; automatic joint cap')
    (report/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    dest=ROOT/'prototype/rig/art_parts';dest.mkdir(exist_ok=True)
    caps={}
    for part in definition['parts']:
        id=part['id'];shutil.copyfile(out/f'{id}.png',dest/f'{id}.png')
        if not part['parent'] or id.startswith(('foot_','hand_')) or id in ('dao','bow'):continue
        a=np.array(Image.open(out/f'{id}.png').convert('RGBA'));px,py=part['pivot'];r=(8 if id=='head' else part['size'][0])/2
        pixels=a[max(0,int(py-r)):min(a.shape[0],math.ceil(py+r+1)),max(0,int(px-r)):min(a.shape[1],math.ceil(px+r+1))]
        good=pixels[:,:,3]>0
        for outline in pal[:2]:good &= np.any(pixels[:,:,:3]!=outline,axis=2)
        colour=nearest(np.median(pixels[good,:3],axis=0),pal) if good.any() else pal[2]
        caps[id]={'radius':r,'color':'#'+''.join(f'{c:02X}' for c in colour),'method':'automatic proximal joint underpaint: two semicircles, no new bone/PNG; supports cap clipped by fixed frame'}
    (dest/'joint_fill.json').write_text(json.dumps(caps,indent=2)+'\n')
    print('Copied 16 identical PNGs into prototype/rig/art_parts (not approved assets)')
if __name__=='__main__':main()
