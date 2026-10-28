# Báo cáo bộ phận Đinh Bộ Lĩnh bậc 0

**Đang làm — chưa duyệt.** Concept 1 lần imagegen, nguồn
`art/concept/characters/chr_dbl_parts_concept.png`, tham chiếu
`art/reference/ref_dinh_bo_linh.png`; prompt nguyên văn ở 05_log và file cạnh concept.
Không sửa ảnh đã duyệt. 16 PNG từ concept mới, chưa chuyển sang co_lau_game.

## Pipeline và giới hạn

- 16 component foreground tách theo nền xanh, thứ tự 4×4 kiểm trên tờ nguồn;
  manifest ghi bounding box/diện tích và SHA-256. Không giả chia một ảnh đứng thành mảnh.
- Dùng lại green_mask/detect_period/load_groups/nearest của snap_pixel; CLI cũ vẫn
  giữ chặn sprite nguyên người sai 96 px. Pipeline bộ phận này được người dùng yêu
  cầu co chính xác theo parts.json: trung vị từng ô, không lấy mẫu NEAREST để co ảnh.
- Màu/alpha: đúng 17 màu nhân vật, alpha chỉ 0 hoặc 255, viền ngoài một pixel;
  bỏ đảo alpha <2 px, không xóa mọi điểm màu đơn vì mắt cần điểm nhấn.
- Vẽ bù tự động: lấy màu trung vị gần khớp, bán nguyệt theo bề rộng mảnh, raster
  các ô pixel giao đĩa. Ghép hai nửa ở vùng khớp để kín khi xoay. Cổ dùng đường kính 8 px.
- Khung/pivot sát mép có thể cắt vòng tròn: joint_fill.json sinh màu/vùng bù cho
  cổ/vai/khuỷu/hông/gối; scene thêm lớp màu dưới ảnh, không thêm bone/PNG hay đổi
  collision. Có thể vượt mép canvas một ít; chưa duyệt mỹ thuật của vùng nối.
- Sprite2D nearest, centered=false, offset=−pivot. Bản sao trong prototype đúng
  byte PNG nguồn. Công tắc “Bộ phận vẽ / Khối màu” chỉ đổi lớp hiển thị.
- Contact sheet lấy affine và khớp thật từ scene, đọc PNG alpha và tô lớp bù thật;
  không tính pose thứ hai trong Python. Đây là raster từ scene data, không phải
  screenshot GPU toàn cảnh. Chưa thử lại Android.

## Ma trận đầu trước/sau

18×24, `.` = trong suốt. Hai bản PNG tại
`art/concept/characters/chr_dbl_parts_work/head_before.png` và `head_after.png`.
Bản sau là **sửa pixel đề xuất bởi Codex bằng script**, chưa được Claude/người dùng
soát/duyệt. Danh sách tọa độ trong `tools/chr_dbl_head_edits.json`; sau sửa vẫn ép
viền ngoài nên điểm sửa ở biên có thể được trả về outline. Không gọi đây là Claude review.

| Chỉ số | RGB | Nhóm |
|---|---|---|
| 0 | #17151A | outline |
| 1 | #342923 | outline |
| 2 | #78432E | skin |
| 3 | #B66C49 | skin |
| 4 | #E99A69 | skin |
| 5 | #FFD0A0 | skin |
| 6 | #554638 | fabric |
| 7 | #89745E | fabric |
| 8 | #C3A98A | fabric |
| 9 | #EAD8B8 | fabric |
| A | #3D2D24 | belt |
| B | #6B4A35 | belt |
| C | #98765A | belt |
| D | #322B2B | pants |
| E | #59443E | pants |
| F | #80614D | pants |
| G | #A38269 | pants |

### Trước sửa

```text
......0000........
.....000100.......
....0000000.......
....000010........
....000000000.....
....000001100000..
...0000000000000..
..000001100011000.
.00000100011110010
..0000000000000000
.0000000000000A000
.00000000000004000
.0000000000000400.
0000000300A4F0A00.
.000000300448E30..
.0000003F044440...
..00000044444440..
...0000A3445540...
...000043455540...
....0344444540....
....0444444440....
....044444440.....
.....04444440.....
....0000000000....
```

### Sau sửa đề xuất

```text
......0000........
.....000100.......
....0000000.......
....000010........
....000000000.....
....000001100000..
...0000000000000..
..000001100011000.
.00000100011110010
..0000000000000000
.0000000000000A000
.00000000000004000
.0000000000002440.
0000000300A4F5040.
.000000300448E350.
.0000003F0444400..
..00000044444440..
...0000A3445520...
...000043455540...
....0344444540....
....0444444440....
....044444440.....
.....04444440.....
....0000000000....
```

## Kết quả kiểm file thật (nguyên đầu ra)

```text
PASS: body size=(20, 26) expected=[20, 26] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: head size=(18, 24) expected=[18, 24] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: upper_arm_far size=(8, 19) expected=[8, 19] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: forearm_far size=(7, 17) expected=[7, 17] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: hand_far size=(7, 8) expected=[7, 8] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: thigh_far size=(10, 24) expected=[10, 24] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: shin_far size=(8, 24) expected=[8, 24] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: foot_far size=(14, 6) expected=[14, 6] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: upper_arm_near size=(8, 19) expected=[8, 19] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: forearm_near size=(7, 17) expected=[7, 17] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: hand_near size=(7, 8) expected=[7, 8] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: thigh_near size=(10, 24) expected=[10, 24] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: shin_near size=(8, 24) expected=[8, 24] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: foot_near size=(14, 6) expected=[14, 6] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: dao size=(5, 34) expected=[5, 34] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: bow size=(6, 38) expected=[6, 38] off_palette=0 semi_alpha=0 scene_copy_identical=True
Joint checks: 672; max seam=0.50px; background samples=45; failures=0
Scope: all 48 authored frames / 13 actions, visible child-parent pairs; not a claim about every interpolated time or Android GPU output.
```

Phương pháp đo: quét mọi dây cung theo tám hướng trong đĩa bán kính tối đa 3 px quanh khớp, raster 4×. Chỉ nền được kẹp giữa mực của hai mảnh khác nhau mới tính là vùng nối. Độ dày = 2× khoảng cách lớn nhất từ các mẫu nền tới union alpha; chiều dài đường lướt được ghi riêng. Tâm khớp phải cách mực ≤1 px. Chi tiết mỗi cặp/khung trong `prototype/rig/reports/art_checks.json`. Bao gồm lớp màu bù tự động trong scene; không giả rằng PNG độc lập đã kín nếu thiếu lớp này.

## Tờ khung và ảnh phóng

```text
prototype/rig/contact_sheets/art/chr_dbl_anim_idle_art.png 640x160 frames=4
prototype/rig/contact_sheets/art/chr_dbl_anim_run_art.png 960x160 frames=6
prototype/rig/contact_sheets/art/chr_dbl_anim_jump_up_art.png 320x160 frames=2
prototype/rig/contact_sheets/art/chr_dbl_anim_apex_flip_art.png 960x160 frames=6
prototype/rig/contact_sheets/art/chr_dbl_anim_slash_1_art.png 640x160 frames=4
prototype/rig/contact_sheets/art/chr_dbl_anim_shoot_art.png 800x160 frames=5
prototype/rig/contact_sheets/art/chr_dbl_anim_hurt_art.png 320x160 frames=2
idle: 128x128 -> 512x512 using Image.resize(..., Image.Resampling.NEAREST) from saved 1x
```

Tờ khung tại `prototype/rig/contact_sheets/art/`. Ảnh idle 1× lưu trước, ×4 phóng bằng Image.resize(NEAREST) từ đúng pixel 1×; không dùng imagegen.

## Lệnh tái tạo

```sh
python tools/cut_parts.py
godot --headless --path prototype --editor --import --quit
godot --headless --path prototype --script res://rig/export_frames.gd -- --art
python tools/render_parts_scene.py
python tools/check_parts.py
godot --headless --path prototype --script res://rig/tests/art_checks.gd
```

Godot 4.7.2 Standard; chạy thêm ba lệnh README, rig smoke và visual_checks. Đầu ra headless nguyên văn trong commit message.

## Script đã chạy (nguyên văn)

### tools/cut_parts.py

```python
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
```

### tools/check_parts.py

```python
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
    groups=load_groups(ROOT/'art/reference/palette.gpl');pal={c for g in ['outline','skin','fabric','belt','pants'] for c in groups[g]}
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
        if name.endswith('_left'):continue
        for index,frame in enumerate(clip['frames']):
            sprites={p['id']:p for p in frame['geometry'] if p['kind']=='sprite'}
            masks={id:np.asarray(sprite_layer(p,size,origin,scale))[:,:,3]>0 for id,p in sprites.items()}
            for item in frame['geometry']:
                if item['kind']=='fill':
                    fill=Image.new('1',size);draw=ImageDraw.Draw(fill)
                    draw.polygon([(x*scale+origin[0],y*scale+origin[1]) for x,y in item['points']],fill=1)
                    masks[item['owner']] |= np.asarray(fill,dtype=bool)
            for id,p in parts.items():
                parent=p['parent']
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
```

### tools/render_parts_scene.py

```python
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
    names=['idle','run','jump_up','apex_flip','slash_1','shoot','hurt']
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
    idle.resize((512,512),Image.Resampling.NEAREST).save(out/'chr_dbl_idle_art_4x.png')
    print('idle: 128x128 -> 512x512 using Image.resize(..., Image.Resampling.NEAREST) from saved 1x')
if __name__=='__main__':main()
```

### tools/chr_dbl_head_edits.json

```json
[
  {"x":13,"y":12,"index":2,"note":"eyebrow shadow"},
  {"x":14,"y":12,"index":4,"note":"upper eyelid skin"},
  {"x":15,"y":12,"index":4,"note":"brow/nose bridge"},
  {"x":13,"y":13,"index":5,"note":"eye light"},
  {"x":14,"y":13,"index":0,"note":"single eye pupil"},
  {"x":15,"y":13,"index":4,"note":"nose bridge"},
  {"x":16,"y":13,"index":4,"note":"nose silhouette"},
  {"x":15,"y":14,"index":5,"note":"nose highlight"},
  {"x":16,"y":14,"index":4,"note":"nose tip"},
  {"x":15,"y":15,"index":2,"note":"nostril shadow"},
  {"x":14,"y":16,"index":4,"note":"cheek"},
  {"x":14,"y":17,"index":2,"note":"mouth"},
  {"x":13,"y":17,"index":2,"note":"mouth continuation"},
  {"x":14,"y":18,"index":4,"note":"chin"}
]
```
