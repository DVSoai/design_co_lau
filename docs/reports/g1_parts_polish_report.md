# G1 — Chỉnh vật liệu và tư thế bộ phận (29/10/2026)

**Đang làm, chưa duyệt mỹ thuật.** Nhánh `fix/g1-parts-polish`, nền main `8997b8c`.
Không sinh concept mới. Sửa pixel bằng script từ concept hiện có; đầu do Claude
vẽ tay từng pixel giữ nguyên tuyệt đối. Không đổi kích thước, pivot hay attach.

## Thay đổi

- Cho phép nhóm limestone của palette_v3 ở `dao`/`bow`; không mở nhóm này cho da,
  áo hay quần. Lưỡi đao: #A5B8B0 chủ đạo (85 pixel), #718B87 bóng (29),
  #D9DDD0 sáng (12), nét #17151A theo đường bao đứng đã có. Cán/phần vỏ giữ belt.
  Mốc phân vật liệu lưỡi/cán chọn ở y=264 của crop nguồn, quy về y=30 px.
- Cung dùng gỗ belt (115 pixel); dây Line2D sáng #D9DDD0 (limestone), rộng 1 px.
- `thigh_near`/`thigh_far` chỉ pants và nét outline: 268/263 pixel quần,
  10/16 pixel nét; không còn pixel skin trên đùi. Cẳng chân/bàn chân giữ skin.
- Giảm **35% góc gập giải phẫu ở cả hai gối** trong toàn bộ 19 pose của
  run/slash_1–3. Giải hai đoạn chân từ độ dài attach, không co mảnh.
  Hông nâng 1,216–4,073 px khi chạy và 2,109–2,160 px khi chém.
  Chạy: giữ x/y chân trụ, chân vung điều chỉnh theo độ duỗi, vẫn ở trên đất.
  Chém: giữ x/y cả hai bàn chân, giao hai đường tròn xác định hông mới.
  Số frame, tổng thời lượng, event và các động tác khác giữ nguyên.

## Kết quả kiểm trên file thật

Godot **4.7.2 Standard**. Ba lệnh headless trong README đều exit 0;
A0 smoke, rig smoke, art checks và visual checks đều đạt. XDG_DATA_HOME,
XDG_CONFIG_HOME, XDG_CACHE_HOME trỏ vào `/tmp/polish-xdg/` để editor ghi cache.

- 16 PNG: đúng kích thước; 0 pixel ngoài palette; 0 pixel bán trong suốt;
  0 pixel sai nhóm; bản trong rig giống byte với bản art.
- 672 cặp khớp nhìn thấy, 48 pose / 13 động tác: khe lớn nhất **0,50 px**,
  không vượt 1 px; riêng cổ **0,00 px**.
- Viền trong dáng đứng: chỉ 17 pixel O của đầu Claude đã có; ngoài đầu 0.
  Các màu H tô tóc được báo riêng. Đứng duỗi cao 96 px; idle co gối cao 95 px.
- Kiểm trực tiếp khớp scene: cả hai gối giảm 35%, hông nâng, chân trụ/chân chém
  y≈0 (sai số float <0,001 px), chân vung không xuyên đất.
- 15 contact sheet art (13 động tác và run/shoot nhìn trái) đủ kích thước;
  idle ×4 khớp đúng ảnh 1× được resize NEAREST. Run/shoot trái có transform
  phản chiếu và thứ tự lớp gần/xa đúng. Kiểm contact sheet greybox cũ cũng đạt;
  không ghi đè dữ liệu hoặc ảnh greybox.

Phạm vi kiểm khe là các pose đã tác giả hóa, không khẳng định mọi thời điểm
nội suy hay kết quả GPU Android. Kỹ thuật đạt không thay cho duyệt mỹ thuật.

## Ảnh để duyệt

- [Idle ×4](../../prototype/rig/contact_sheets/art/chr_dbl_idle_art_4x.png)
- [Run](../../prototype/rig/contact_sheets/art/chr_dbl_anim_run_art.png)
- [Slash 1](../../prototype/rig/contact_sheets/art/chr_dbl_anim_slash_1_art.png),
  [Slash 2](../../prototype/rig/contact_sheets/art/chr_dbl_anim_slash_2_art.png),
  [Slash 3](../../prototype/rig/contact_sheets/art/chr_dbl_anim_slash_3_art.png)
- [Shoot](../../prototype/rig/contact_sheets/art/chr_dbl_anim_shoot_art.png)

Toàn bộ ảnh được raster từ transform Sprite2D của scene thật bằng PIL, không
imagegen. Ảnh ×4 dùng Image.resize(..., Image.Resampling.NEAREST) từ PNG 1× đã lưu.

## Lệnh và nguyên đầu ra

[Nguyên đầu ra mọi script/headless](g1_parts_polish_output.txt), cũng chép nguyên
vào commit message. Đọc báo cáo lượt trước ở [g1_parts_art_report.md](g1_parts_art_report.md)
như lịch sử; màu vũ khí, đùi và góc gối hiện tại lấy theo báo cáo này.

## Script đã chạy

Các nguồn dưới đây là nguyên văn script kiểm số liệu trên PNG/scene thực.
Script dựng ảnh: [render_parts_scene.py](../../tools/render_parts_scene.py);
script tạo/cập nhật: [cut_parts.py](../../tools/cut_parts.py),
[outline_parts.py](../../tools/outline_parts.py), [retarget_parts.py](../../tools/retarget_parts.py).

### tools/check_parts_roles.py

```python
"""Check immutable Claude head, material groups, shirt budget and evaluated fingertip height."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from cut_parts import claude_head
from snap_pixel import load_groups
from render_parts_scene import sprite_layer
ROOT=Path(__file__).resolve().parents[1]
def main():
 g=load_groups(ROOT/'art/reference/palette.gpl');outline=g['outline'];errors=[];report={}
 for p in json.loads((ROOT/'prototype/rig/data/parts.json').read_text())['parts']:
  id=p['id'];a=np.array(Image.open(ROOT/f'art/sprites/characters/chr_dbl_parts/{id}.png').convert('RGBA'))
  allowed=outline+(g['pants'] if id.startswith('thigh_') else g['skin'] if id.startswith(('forearm_','hand_','shin_','foot_')) else g['fabric']+g['skin'] if id.startswith('upper_arm_') else g['belt']+g['limestone'] if id in ['dao','bow'] else g['fabric']+g['belt'])
  if id=='head':allowed=outline+[g['pants'][1]]+g['skin'];same=np.array_equal(a,claude_head());print('Head exact Claude matrix:',same);errors+=[] if same else ['head changed']
  bad=[(int(x),int(y)) for y,x in zip(*np.where(a[:,:,3]>0)) if tuple(a[y,x,:3]) not in allowed]
  report[id]={'forbidden_group_pixels':len(bad)};print(f'{id}: forbidden group pixels={len(bad)}');errors+=bad
  if id=='dao':
   blade=a[:round(264*96/846)];counts={('#'+''.join(f'{v:02X}' for v in c)):int((np.all(blade[:,:,:3]==c,axis=2)&(blade[:,:,3]>0)).sum()) for c in g['limestone']}
   print('dao blade limestone counts:',counts);report[id]['blade_counts']=counts
   if max(counts,key=counts.get)!='#A5B8B0' or not counts['#718B87'] or not counts['#D9DDD0']:errors.append('blade material balance')
  if id=='body' or id.startswith('upper_arm_'):
   counts={('#'+''.join(f'{v:02X}' for v in c)):int((np.all(a[:,:,:3]==c,axis=2)&(a[:,:,3]>0)).sum()) for c in g['fabric']};total=sum(counts.values());ratio=counts['#EAD8B8']/max(1,total);dominant=max(counts,key=counts.get)
   report[id]['shirt_counts']=counts;report[id]['shirt_percent']={k:round(100*v/max(1,total),3) for k,v in counts.items()};print(id,'shirt counts/percent:',counts,report[id]['shirt_percent'])
   if ratio>.15 or dominant!='#C3A98A':errors.append(f'{id} shirt budget')
 data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());tips={}
 for name in ['idle','standing_neutral']:
  for item in data[name]['frames'][0]['geometry']:
   if item['id'] not in ['hand_near','hand_far']:continue
   mask=np.array(sprite_layer(item,(160,160),(80,126)))[:,:,3]>0;ys,xs=np.where(mask);tip=int(ys.max())+1-126;tips[name+'_'+item['id']]=tip
   print(f'{name} {item["id"]}: fingertip bottom y={tip} px from feet')
   if not -34<=tip<=-30:errors.append(f'{name} fingertip {tip}')
 report['fingertips']=tips;report['failures']=len(errors);(ROOT/'prototype/rig/reports/material_checks.json').write_text(json.dumps(report,indent=2)+'\n');print('Material/Claude/arm failures:',len(errors));raise SystemExit(1 if errors else 0)
if __name__=='__main__':main()
```

### tools/check_parts_uniform.py

```python
"""Measure actual PNG palette/face colours and outline inside evaluated standing silhouette."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from render_parts_scene import layers
from snap_pixel import load_groups
ROOT=Path(__file__).resolve().parents[1]
def main():
    groups=load_groups(ROOT/'art/reference/palette.gpl');data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());results={};failure=0
    for name in ['idle','standing_neutral']:
        im=Image.new('RGBA',(128,128));owners=np.full((128,128),'',object)
        for id,layer in layers(data[name]['frames'][0],(128,128),(64,120)):
            owners[np.array(layer)[:,:,3]>0]=id;im.alpha_composite(layer)
        a=np.array(im);mask=a[:,:,3]>0;p=np.pad(mask,1);inner=mask&p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]
        dark=np.zeros(mask.shape,bool)
        # O is stroke; Claude explicitly uses H as hair fill, report it separately.
        dark=np.all(a[:,:,:3]==groups['outline'][0],axis=2)
        hair_fill=int((inner&np.all(a[:,:,:3]==groups['outline'][1],axis=2)).sum())
        print(name,'H hair-fill pixels inside silhouette:',hair_fill)
        coords=[]
        items={i['id']:i for i in data[name]['frames'][0]['geometry'] if i['kind']=='sprite'}
        for y,x in zip(*np.where(inner&dark)):
            id=str(owners[y,x]);point={'x':int(x),'y':int(y),'part':id}
            if id in items:
                aa,b,c,d,tx,ty=items[id]['transform'];det=aa*d-b*c;wx=x+.5-64-tx;wy=y+.5-120-ty
                point['texture_x']=int(np.floor((d*wx-c*wy)/det));point['texture_y']=int(np.floor((-b*wx+aa*wy)/det))
            coords.append(point)
        ys,xs=np.where(mask);h=int(ys.max()-ys.min()+1);results[name]={'height_px':h,'interior_outline_count':len(coords),'positions':coords,'opaque_pixels':int(mask.sum()),'interior_outline_percent':round(100*len(coords)/int(mask.sum()),4)}
        print(f'{name}: height={h}px; internal outline pixels={len(coords)}; positions={coords}')
        # Claude's supplied head intentionally uses outline colours as hair fill.
        # Report them, but only reject unintended interior ink outside immutable head.
        failure+=any(c['part']!='head' for c in coords)
        if name=='standing_neutral':failure+=h!=96
    head=np.array(Image.open(ROOT/'art/sprites/characters/chr_dbl_parts/head.png').convert('RGBA'));skin=np.zeros(head.shape[:2],bool)
    for colour in groups['skin']:skin|=np.all(head[:,:,:3]==colour,axis=2)&(head[:,:,3]>0)
    measured=json.loads((ROOT/'art/concept/characters/chr_dbl_parts_work/uniform_measurements.json').read_text());skin[int(measured['landmarks_manual']['head']['chin_y']*measured['scale'])+1:]=False
    ys,xs=np.where(skin);span=int(xs.max()-xs.min()+1);ratio=span/head.shape[1]
    print(f'Head face skin span={span}/{head.shape[1]}={ratio:.4f}; neck below chin={measured["neck_below_chin_px"]:.4f}px; Claude pixel matrix applied unchanged')
    results['face']={'width':span,'frame_width':head.shape[1],'ratio':ratio,'neck_below_chin':measured['neck_below_chin_px']};failure+=ratio<.4 or not 2<=measured['neck_below_chin_px']<=3
    for id in ['hand_near','hand_far','foot_near','foot_far']:
        a=np.array(Image.open(ROOT/f'art/sprites/characters/chr_dbl_parts/{id}.png').convert('RGBA'));counts={label:int(np.all(a[:,:,:3]==colour,axis=2).sum()) for label,colour in [('dark',groups['skin'][0]),('mid',groups['skin'][2]),('light',groups['skin'][3])]}
        print(f'{id}: skin counts {counts}');failure+=not all(counts.values());results[id]=counts
    results['failures']=int(failure);(ROOT/'prototype/rig/reports/uniform_art_checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print('Uniform-art checks failures:',failure);raise SystemExit(1 if failure else 0)
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

### tools/check_parts_polish.py

```python
"""Check polished materials and actual Godot-evaluated knee/sole geometry."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
from snap_pixel import load_groups
ROOT=Path(__file__).resolve().parents[1]
def main():
 data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text())
 poses=json.loads((ROOT/'prototype/rig/data/animations.json').read_text())
 source=json.loads((ROOT/'prototype/rig/data/animations_greybox.json').read_text())
 checks=json.loads((ROOT/'prototype/rig/reports/leg_polish.json').read_text());failures=0;errors=[]
 for row in checks:
  name=row['clip'];i=row['frame']-1;frame=data[name]['frames'][i];j=frame['joints'];angles=[];feet=[]
  for side in ['near','far']:
   hip=np.array(j['thigh_'+side]);knee=np.array(j['shin_'+side]);ankle=np.array(j['foot_'+side]);v=knee-hip;w=ankle-knee
   bend=math.degrees(math.acos(np.clip(v@w/(np.linalg.norm(v)*np.linalg.norm(w)),-1,1)))
   reduction=1-bend/abs(row['old_knee_degrees'][side]);angles.append(round(100*reduction,3))
   if not .30<=reduction<=.40:errors.append(f'{name}/{i}/{side} knee reduction')
   foot=next(p for p in frame['geometry'] if p['id']=='foot_'+side and p['kind']=='sprite');a,b,c,d,tx,ty=foot['transform'];size=Image.open(ROOT/'prototype'/foot['source'].removeprefix('res://')).size
   bottom=max(b*x+d*y+ty for x,y in [(0,0),(size[0],0),size,(0,size[1])]);feet.append(round(bottom,5))
   if abs(bottom-row['foot_targets'][side][1])>.001:errors.append(f'{name}/{i}/{side} sole target')
   if bottom>.001:errors.append(f'{name}/{i}/{side} underground')
  rise=row['old_hip'][1]-j['body'][1]
  if rise<=0:errors.append(f'{name}/{i} hip not raised')
  print(f'{name} frame={i+1}: knee reduction near/far={angles}%; hip rise={rise:.3f}px; sole y near/far={feet}')
 for name,clip in poses['clips'].items():
  old=source['clips'][name]
  if len(clip['frames'])!=len(old['frames']):errors.append(name+' count')
  for f,g in zip(clip['frames'],old['frames']):
   if f['duration']!=g['duration']:errors.append(name+' timing')
  if clip.get('events')!=old.get('events'):errors.append(name+' events')
 print('13 clip frame counts, durations and events retained')
 g=load_groups(ROOT/'art/reference/palette.gpl')
 for id in ['dao','bow','thigh_near','thigh_far']:
  a=np.array(Image.open(ROOT/f'art/sprites/characters/chr_dbl_parts/{id}.png').convert('RGBA'));opaque=a[:,:,3]>0
  counts={name:int(sum(tuple(px) in colours for px in a[:,:,:3][opaque])) for name,colours in g.items()};counts={k:v for k,v in counts.items() if v}
  if id.startswith('thigh') and any(k not in ['outline','pants'] for k in counts):errors.append(id+' exposed skin')
  if id=='bow' and any(k not in ['outline','belt','limestone'] for k in counts):errors.append('bow material')
  print(id,'material pixel counts:',counts)
 if poses['clips']['shoot']['frames'][0]['angles']['bow']!=90:errors.append('bow orientation')
 definition=json.loads((ROOT/'prototype/rig/data/parts.json').read_text())
 if definition['bow_string']['color']!='#D9DDD0':errors.append('string colour')
 sheets=ROOT/'prototype/rig/contact_sheets/art'
 for name,clip in data.items():
  if name=='standing_neutral':continue
  size=Image.open(sheets/f'chr_dbl_anim_{name}_art.png').size
  if size!=(160*len(clip['frames']),160):errors.append(name+' sheet size')
 idle=Image.open(sheets/'chr_dbl_idle_art_1x.png').convert('RGBA');x4=Image.open(sheets/'chr_dbl_idle_art_4x.png').convert('RGBA')
 if not np.array_equal(np.array(idle.resize((512,512),Image.Resampling.NEAREST)),np.array(x4)):errors.append('idle x4')
 print('15 art contact sheets: frame dimensions correct; idle x4 equals saved 1x resized NEAREST')
 for name in ['run','shoot']:
  for right,left in zip(data[name]['frames'],data[name+'_left']['frames']):
   by_id={p['id']:p for p in left['geometry'] if p['kind']=='sprite'}
   for part in right['geometry']:
    if part['kind']!='sprite':continue
    other=by_id[part['id']];a=np.array(part['transform']);b=np.array(other['transform']);a[[0,2,4]]*=-1
    if not np.allclose(a,b,atol=.001) or part['z']!=other['z']:errors.append(name+' art mirror/layers')
 print('Art run/shoot: both directions reflect actual sprite transforms, near/far layers unchanged')
 failures=len(errors);print('Polish failures:',failures,errors);raise SystemExit(bool(failures))
if __name__=='__main__':main()
```
