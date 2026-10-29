# G1 — Đầu Claude, sửa chất liệu và chiều dài tay

> Cập nhật tiếp: [polish vật liệu và tư thế 29/10/2026](g1_parts_polish_report.md). Các số liệu dưới đây là báo cáo của lượt trước.

**Đang làm — chưa duyệt toàn bộ art.** Theo ma trận người dùng gửi:
**đầu do Claude vẽ tay từng pixel**. Không imagegen trong lượt này.

## Đầu nguyên pixel

23×25, giữ pivot (9,418;24,738) và attach (0;−24,284). Pipeline không cleanup
hay bôi viền trên đầu. So RGBA trùng ma trận bên dưới, cả PNG nguồn và bản rig.
Cổ khớp thân: khe lớn nhất 0,00 px trong 48 frame.

| Ký tự | Hex | Vai trò |
|---|---|---|
| O | #17151A | Nét |
| H | #342923 | Tóc |
| L | #59443E | Ánh tóc (ngoại lệ màu pants) |
| D | #78432E | Da tối |
| s | #B66C49 | Da bóng |
| k | #E99A69 | Da trung |
| W | #FFD0A0 | Da sáng |

`.` trong suốt. Ma trận đúng nguyên văn người dùng cung cấp:

```text
........OOO............
.......OHLHO...........
.......OHHHO...........
........OHO............
....O.OOHHOOO.O........
...OHOHHHHHHHOHO.......
..OHHHHHLHHHHHHHO.O....
.OHHHHHHHHHHLHHHHOHO...
.OHHHLHHHHHHHHHHHHHHO..
OHHHHHHHHHHHHHHHHHHHO..
.OHHHHHHHHHHHHHHHHHHHO.
OHHHHHHHHHHHHHHHOkHHO..
.OHHHHHHHHHHHHHOkkWkO..
OHHHHHHHHHHHHHskOOOkkO.
.OHHHHHHHHHHHsksOWkkkO.
.OHHHHHHHHHHDssksskkkkO
..OHHHHHHHHHDkskkkkkkkO
..OHHHHHHHHHsDkkkkkkksO
...OHHHHHHHOsskkkkkDDO.
....OHHHHHHOskkkkkkkkO.
.....OHHHOOOsskkkkkkO..
......OOOssssskkkkOO...
........OsskkOOOOO.....
........OsskkO.........
........OsskkO.........
```

## Tay: cũ → mới

Chỉ tay trên/cẳng tay có ngoại lệ co riêng trục dài 0,60; giữ nguyên chiều ngang.
Đầu ngón y=−33 ở đứng duỗi, −32 ở idle, cả gần/xa; gốc chân y=0.
Khung/mốc ghép cập nhật như sau, x/y theo px, bảng làm tròn 3 số:

| Mảnh | Khung cũ → mới | Pivot cũ → mới | Attach cũ → mới |
|---|---|---|---|
| `upper_arm_near` | (10, 26) → (10, 16) | (4.766, 1.362) → (4.766, 0.817) | (0.34, -20.993) → (0.34, -20.993) |
| `forearm_near` | (8, 19) → (8, 12) | (3.404, 1.135) → (3.404, 0.681) | (0.34, 22.922) → (0.34, 13.753) |
| `hand_near` | (10, 13) → (10, 13) | (2.95, 1.021) → (2.95, 1.021) | (0.113, 16.227) → (0.113, 9.736) |
| `upper_arm_far` | (10, 26) → (10, 16) | (4.652, 1.362) → (4.652, 0.817) | (0.34, -20.993) → (0.34, -20.993) |
| `forearm_far` | (7, 19) → (7, 12) | (3.291, 1.135) → (3.291, 0.681) | (0.227, 22.922) → (0.227, 13.753) |
| `hand_far` | (10, 14) → (10, 14) | (2.837, 1.021) → (2.837, 1.021) | (0.113, 15.887) → (0.113, 9.532) |

Các bộ phận khác vẫn dùng s=96/846, greybox gốc giữ riêng. Frame counts, duration,
events 13 động tác giữ nguyên; không sửa A0 player/hitbox/physics.

## Nhóm màu và tỉ lệ áo

- Đầu: đúng ma trận O/H/L/skin; L chỉ là ánh tóc.
- Body: fabric/belt + viền ngoài, không pants.
- Upper_arm: fabric trên ống tay, skin dưới; forearm/hand/shin/foot: skin + viền ngoài.
- Thigh là quần: pants và da lộ ở gối; vũ khí dùng fabric/belt + viền ngoài.
- Phần bù khớp dùng chất liệu đúng nhóm, không có viền.

Tỉ lệ dưới đây lấy mẫu số là **pixel vải** (bốn màu fabric), loại viền/belt/da.
Đây là mẫu số chặt hơn lấy toàn PNG tay có cả da.

| Mảnh | #554638 bóng | #89745E bóng | #C3A98A chủ đạo | #EAD8B8 sáng |
|---|---|---|---|---|
| body | 33 px / 12.132% | 45 px / 16.544% | 164 px / 60.294% | 30 px / 11.029% |
| upper_arm_near | 11 px / 15.068% | 15 px / 20.548% | 40 px / 54.795% | 7 px / 9.589% |
| upper_arm_far | 11 px / 15.714% | 14 px / 20.000% | 38 px / 54.286% | 7 px / 10.000% |

## Kiểm palette, khớp và nét trong dáng

PNG: 0 pixel ngoài palette, 0 bán trong suốt, 0 sai nhóm; đầu trùng tuyệt đối
ma trận Claude. Khe khớp ≤1 px: 672 cặp/48 frame/13 động tác, lớn nhất 0,50 px.
Đo từ affine scene và PNG alpha thật + lớp bù khớp; raster 4×, kiểm khoảng nền
giữa hai mảnh theo tám hướng và distance field. Không phải kiểm GPU Android.

O nội bộ trong idle/đứng duỗi: **17**, đều ở đầu Claude. H là màu tô tóc theo
ma trận, báo riêng (197 pixel nội bộ trong idle), không coi toàn màu H là nét lỗi.
**Ngoài đầu: 0 nét nội bộ.** Đầu được giữ nguyên, không sửa nét người dùng gửi.
Tọa độ (0-based) trong texture đầu:

- (10,4), canvas đứng (65,28).
- (16,11), canvas đứng (71,35).
- (15,12), canvas đứng (70,36).
- (16,13), canvas đứng (71,37).
- (17,13), canvas đứng (72,37).
- (18,13), canvas đứng (73,37).
- (16,14), canvas đứng (71,38).
- (11,18), canvas đứng (66,42).
- (11,19), canvas đứng (66,43).
- (9,20), canvas đứng (64,44).
- (10,20), canvas đứng (65,44).
- (11,20), canvas đứng (66,44).
- (7,21), canvas đứng (62,45).
- (8,21), canvas đứng (63,45).
- (8,22), canvas đứng (63,46).
- (13,22), canvas đứng (68,46).
- (8,23), canvas đứng (63,47).

## Đầu ra script nguyên văn

```text
SOURCE neutral assembly: head=218, torso=214, legs=414; H=846px; guide=24/24/48; s=96/846=0.113475177305 on BOTH axes
Scaled anatomical spans: [24.7376, 24.2837, 46.9787] ; no independent per-part scale
head: source=200x219 -> [23, 25]; pivot=[9.418, 24.738]; attach=[0.0, -24.284]; shared s, arm-longitudinal=0.60 if applicable
body: source=144x255 -> [17, 29]; pivot=[7.376, 26.099]; attach=[0.0, -46.979]; shared s, arm-longitudinal=0.60 if applicable
upper_arm_near: source=84x227 -> [10, 16]; pivot=[4.766, 0.817]; attach=[0.34, -20.993]; shared s, arm-longitudinal=0.60 if applicable
upper_arm_far: source=83x228 -> [10, 16]; pivot=[4.652, 0.817]; attach=[0.34, -20.993]; shared s, arm-longitudinal=0.60 if applicable
forearm_near: source=62x166 -> [8, 12]; pivot=[3.404, 0.681]; attach=[0.34, 13.753]; shared s, arm-longitudinal=0.60 if applicable
forearm_far: source=60x162 -> [7, 12]; pivot=[3.291, 0.681]; attach=[0.227, 13.753]; shared s, arm-longitudinal=0.60 if applicable
hand_near: source=84x114 -> [10, 13]; pivot=[2.95, 1.021]; attach=[0.113, 9.736]; shared s, arm-longitudinal=0.60 if applicable
hand_far: source=83x115 -> [10, 14]; pivot=[2.837, 1.021]; attach=[0.113, 9.532]; shared s, arm-longitudinal=0.60 if applicable
thigh_near: source=132x204 -> [15, 24]; pivot=[7.376, 1.362]; attach=[1.5, 0.0]; shared s, arm-longitudinal=0.60 if applicable
thigh_far: source=130x204 -> [15, 24]; pivot=[7.262, 1.362]; attach=[-1.5, 0.0]; shared s, arm-longitudinal=0.60 if applicable
shin_near: source=72x186 -> [9, 22]; pivot=[4.085, 1.362]; attach=[-0.113, 19.972]; shared s, arm-longitudinal=0.60 if applicable
shin_far: source=72x183 -> [9, 21]; pivot=[3.972, 1.362]; attach=[-0.113, 19.972]; shared s, arm-longitudinal=0.60 if applicable
foot_near: source=161x105 -> [19, 12]; pivot=[4.993, 2.156]; attach=[-0.113, 17.248]; shared s, arm-longitudinal=0.60 if applicable
foot_far: source=156x105 -> [18, 12]; pivot=[4.879, 2.156]; attach=[-0.113, 17.248]; shared s, arm-longitudinal=0.60 if applicable
dao: source=64x353 -> [8, 41]; pivot=[3.518, 32.908]; attach=[1.816, 6.355]; shared s, arm-longitudinal=0.60 if applicable
bow: source=85x356 -> [10, 41]; pivot=[1.589, 20.879]; attach=[1.816, 6.355]; shared s, arm-longitudinal=0.60 if applicable
HEAD: đầu do Claude vẽ tay từng pixel; exact supplied matrix, no cleanup or feature edits:
........000............
.......01E10...........
.......01110...........
........010............
....0.0011000.0........
...0101111111010.......
..011111E11111110.0....
.01111111111E1111010...
.0111E111111111111110..
011111111111111111110..
.011111111111111111110.
011111111111111104110..
.01111111111111044540..
0111111111111134000440.
.011111111111343054440.
.0111111111123343344440
..011111111124344444440
..011111111132444444430
...0111111103344444220.
....011111103444444440.
.....0111000334444440..
......00033333444400...
........0334400000.....
........033440.........
........033440.........
Palette: {'0': '#17151A', '1': '#342923', '2': '#78432E', '3': '#B66C49', '4': '#E99A69', '5': '#FFD0A0', '6': '#554638', '7': '#89745E', '8': '#C3A98A', '9': '#EAD8B8', 'A': '#3D2D24', 'B': '#6B4A35', 'C': '#98765A', 'D': '#322B2B', 'E': '#59443E', 'F': '#80614D', 'G': '#A38269'}
Head neck below chin: 3.000px; source face span / frame width=0.592
Retargeted art poses: 13 clips/48 frames; unchanged duration/events; foot targets retained; geometry from common-scale parts
Removed generated internal-outline samples: 30
Standing silhouette outline pixels painted per source piece: {'body': 41, 'upper_arm_far': 0, 'forearm_far': 0, 'hand_far': 0, 'thigh_far': 19, 'shin_far': 21, 'foot_far': 24, 'upper_arm_near': 0, 'forearm_near': 0, 'hand_near': 5, 'thigh_near': 10, 'shin_near': 23, 'foot_near': 34, 'dao': 7}
Cut planes and joint overdraw remain unoutlined; facial feature edit lists not read.
body: forbidden group pixels=0
body shirt counts/percent: {'#554638': 33, '#89745E': 45, '#C3A98A': 164, '#EAD8B8': 30} {'#554638': 12.132, '#89745E': 16.544, '#C3A98A': 60.294, '#EAD8B8': 11.029}
Head exact Claude matrix: True
head: forbidden group pixels=0
upper_arm_far: forbidden group pixels=0
upper_arm_far shirt counts/percent: {'#554638': 11, '#89745E': 14, '#C3A98A': 38, '#EAD8B8': 7} {'#554638': 15.714, '#89745E': 20.0, '#C3A98A': 54.286, '#EAD8B8': 10.0}
forearm_far: forbidden group pixels=0
hand_far: forbidden group pixels=0
thigh_far: forbidden group pixels=0
shin_far: forbidden group pixels=0
foot_far: forbidden group pixels=0
upper_arm_near: forbidden group pixels=0
upper_arm_near shirt counts/percent: {'#554638': 11, '#89745E': 15, '#C3A98A': 40, '#EAD8B8': 7} {'#554638': 15.068, '#89745E': 20.548, '#C3A98A': 54.795, '#EAD8B8': 9.589}
forearm_near: forbidden group pixels=0
hand_near: forbidden group pixels=0
thigh_near: forbidden group pixels=0
shin_near: forbidden group pixels=0
foot_near: forbidden group pixels=0
dao: forbidden group pixels=0
bow: forbidden group pixels=0
idle hand_far: fingertip bottom y=-32 px from feet
idle hand_near: fingertip bottom y=-32 px from feet
standing_neutral hand_far: fingertip bottom y=-33 px from feet
standing_neutral hand_near: fingertip bottom y=-33 px from feet
Material/Claude/arm failures: 0
idle H hair-fill pixels inside silhouette: 197
idle: height=95px; internal outline pixels=17; positions=[{'x': 65, 'y': 29, 'part': 'head', 'texture_x': 10, 'texture_y': 4}, {'x': 71, 'y': 36, 'part': 'head', 'texture_x': 16, 'texture_y': 11}, {'x': 70, 'y': 37, 'part': 'head', 'texture_x': 15, 'texture_y': 12}, {'x': 71, 'y': 38, 'part': 'head', 'texture_x': 16, 'texture_y': 13}, {'x': 72, 'y': 38, 'part': 'head', 'texture_x': 17, 'texture_y': 13}, {'x': 73, 'y': 38, 'part': 'head', 'texture_x': 18, 'texture_y': 13}, {'x': 71, 'y': 39, 'part': 'head', 'texture_x': 16, 'texture_y': 14}, {'x': 66, 'y': 43, 'part': 'head', 'texture_x': 11, 'texture_y': 18}, {'x': 66, 'y': 44, 'part': 'head', 'texture_x': 11, 'texture_y': 19}, {'x': 64, 'y': 45, 'part': 'head', 'texture_x': 9, 'texture_y': 20}, {'x': 65, 'y': 45, 'part': 'head', 'texture_x': 10, 'texture_y': 20}, {'x': 66, 'y': 45, 'part': 'head', 'texture_x': 11, 'texture_y': 20}, {'x': 62, 'y': 46, 'part': 'head', 'texture_x': 7, 'texture_y': 21}, {'x': 63, 'y': 46, 'part': 'head', 'texture_x': 8, 'texture_y': 21}, {'x': 63, 'y': 47, 'part': 'head', 'texture_x': 8, 'texture_y': 22}, {'x': 68, 'y': 47, 'part': 'head', 'texture_x': 13, 'texture_y': 22}, {'x': 63, 'y': 48, 'part': 'head', 'texture_x': 8, 'texture_y': 23}]
standing_neutral H hair-fill pixels inside silhouette: 197
standing_neutral: height=96px; internal outline pixels=17; positions=[{'x': 65, 'y': 28, 'part': 'head', 'texture_x': 10, 'texture_y': 4}, {'x': 71, 'y': 35, 'part': 'head', 'texture_x': 16, 'texture_y': 11}, {'x': 70, 'y': 36, 'part': 'head', 'texture_x': 15, 'texture_y': 12}, {'x': 71, 'y': 37, 'part': 'head', 'texture_x': 16, 'texture_y': 13}, {'x': 72, 'y': 37, 'part': 'head', 'texture_x': 17, 'texture_y': 13}, {'x': 73, 'y': 37, 'part': 'head', 'texture_x': 18, 'texture_y': 13}, {'x': 71, 'y': 38, 'part': 'head', 'texture_x': 16, 'texture_y': 14}, {'x': 66, 'y': 42, 'part': 'head', 'texture_x': 11, 'texture_y': 18}, {'x': 66, 'y': 43, 'part': 'head', 'texture_x': 11, 'texture_y': 19}, {'x': 64, 'y': 44, 'part': 'head', 'texture_x': 9, 'texture_y': 20}, {'x': 65, 'y': 44, 'part': 'head', 'texture_x': 10, 'texture_y': 20}, {'x': 66, 'y': 44, 'part': 'head', 'texture_x': 11, 'texture_y': 20}, {'x': 62, 'y': 45, 'part': 'head', 'texture_x': 7, 'texture_y': 21}, {'x': 63, 'y': 45, 'part': 'head', 'texture_x': 8, 'texture_y': 21}, {'x': 63, 'y': 46, 'part': 'head', 'texture_x': 8, 'texture_y': 22}, {'x': 68, 'y': 46, 'part': 'head', 'texture_x': 13, 'texture_y': 22}, {'x': 63, 'y': 47, 'part': 'head', 'texture_x': 8, 'texture_y': 23}]
Head face skin span=13/23=0.5652; neck below chin=3.0000px; Claude pixel matrix applied unchanged
hand_near: skin counts {'dark': 28, 'mid': 29, 'light': 29}
hand_far: skin counts {'dark': 29, 'mid': 29, 'light': 28}
foot_near: skin counts {'dark': 22, 'mid': 37, 'light': 43}
foot_far: skin counts {'dark': 22, 'mid': 38, 'light': 41}
Uniform-art checks failures: 0
PASS: body size=(17, 29) expected=[17, 29] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: head size=(23, 25) expected=[23, 25] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: upper_arm_far size=(10, 16) expected=[10, 16] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: forearm_far size=(7, 12) expected=[7, 12] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: hand_far size=(10, 14) expected=[10, 14] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: thigh_far size=(15, 24) expected=[15, 24] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: shin_far size=(9, 21) expected=[9, 21] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: foot_far size=(18, 12) expected=[18, 12] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: upper_arm_near size=(10, 16) expected=[10, 16] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: forearm_near size=(8, 12) expected=[8, 12] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: hand_near size=(10, 13) expected=[10, 13] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: thigh_near size=(15, 24) expected=[15, 24] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: shin_near size=(9, 22) expected=[9, 22] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: foot_near size=(19, 12) expected=[19, 12] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: dao size=(8, 41) expected=[8, 41] off_palette=0 semi_alpha=0 scene_copy_identical=True
PASS: bow size=(10, 41) expected=[10, 41] off_palette=0 semi_alpha=0 scene_copy_identical=True
Joint checks: 672; max seam=0.50px; background samples=52; failures=0
Scope: all 48 authored frames / 13 actions, visible child-parent pairs; not a claim about every interpolated time or Android GPU output.
prototype/rig/contact_sheets/art/chr_dbl_anim_apex_flip_art.png 960x160 frames=6
prototype/rig/contact_sheets/art/chr_dbl_anim_fall_art.png 320x160 frames=2
prototype/rig/contact_sheets/art/chr_dbl_anim_hurt_art.png 320x160 frames=2
prototype/rig/contact_sheets/art/chr_dbl_anim_idle_art.png 640x160 frames=4
prototype/rig/contact_sheets/art/chr_dbl_anim_jump_up_art.png 320x160 frames=2
prototype/rig/contact_sheets/art/chr_dbl_anim_knockdown_art.png 640x160 frames=4
prototype/rig/contact_sheets/art/chr_dbl_anim_land_art.png 320x160 frames=2
prototype/rig/contact_sheets/art/chr_dbl_anim_run_art.png 960x160 frames=6
prototype/rig/contact_sheets/art/chr_dbl_anim_run_left_art.png 960x160 frames=6
prototype/rig/contact_sheets/art/chr_dbl_anim_shoot_art.png 800x160 frames=5
prototype/rig/contact_sheets/art/chr_dbl_anim_shoot_left_art.png 800x160 frames=5
prototype/rig/contact_sheets/art/chr_dbl_anim_slash_1_art.png 640x160 frames=4
prototype/rig/contact_sheets/art/chr_dbl_anim_slash_2_art.png 640x160 frames=4
prototype/rig/contact_sheets/art/chr_dbl_anim_slash_3_art.png 800x160 frames=5
prototype/rig/contact_sheets/art/chr_dbl_anim_turn_art.png 320x160 frames=2
idle: 128x128 -> 512x512 using Image.resize(..., Image.Resampling.NEAREST) from saved 1x
```

## Tái tạo

```sh
python tools/cut_parts.py
python tools/retarget_parts.py
godot --headless --path prototype --editor --import --quit
godot --headless --path prototype --script res://rig/export_frames.gd -- --art
python tools/outline_parts.py
godot --headless --path prototype --editor --import --quit
godot --headless --path prototype --script res://rig/export_frames.gd -- --art
python tools/render_parts_scene.py
python tools/check_parts_roles.py
python tools/check_parts_uniform.py
python tools/check_parts.py
```

Dùng Godot 4.7.2 Standard. Ba lệnh headless README và rig tests có nguyên đầu ra
trong commit message. Contact sheet từ scene, idle ×4 đọc PNG 1× rồi phóng NEAREST.
Chưa thử Android mới; không coi kiểm kỹ thuật là duyệt mỹ thuật toàn bộ.

## Script đã chạy nguyên văn

### tools/cut_parts.py

```python
#!/usr/bin/env python3
"""Shared body scale; authorized 0.60 arm-length exception; immutable Claude head."""
import json,math,hashlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image
from snap_pixel import green_mask,nearest,load_groups
ROOT=Path(__file__).resolve().parents[1]
GROUPS=['outline','skin','fabric','belt','pants']
# Anatomical/overlap landmarks in each source crop, selected visually, never inferred as ground truth.
LANDMARKS={
 'head':{'pivot':[83,218],'crop_bottom':219,'chin_y':197,'face_box':[80,105,200,198]},
 'body':{'pivot':[65,230],'neck':[65,16],'shoulder':[68,45]},
 'upper_arm_near':{'pivot':[42,12],'end':[45,214]},'upper_arm_far':{'pivot':[41,12],'end':[43,214]},
 'forearm_near':{'pivot':[30,10],'end':[31,153]},'forearm_far':{'pivot':[29,10],'end':[30,150]},
 'hand_near':{'pivot':[26,9],'grip':[42,65]},'hand_far':{'pivot':[25,9],'grip':[41,65]},
 'thigh_near':{'pivot':[65,12],'end':[64,188]},'thigh_far':{'pivot':[64,12],'end':[63,188]},
 'shin_near':{'pivot':[36,12],'end':[35,164]},'shin_far':{'pivot':[35,12],'end':[34,164]},
 'foot_near':{'pivot':[44,19],'ground':105},'foot_far':{'pivot':[43,19],'ground':105},
 'dao':{'pivot':[31,290]},'bow':{'pivot':[14,184],'top':[75,3],'bottom':[78,354]}}

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

def matrix(a,pal):
    chars='0123456789ABCDEFG';lookup={tuple(c):chars[i] for i,c in enumerate(pal)}
    return '\n'.join(''.join(lookup[tuple(px[:3])] if px[3] else '.' for px in row) for row in a)

def sample_uniform(rgb,mask,s):
    h,w=mask.shape;out=np.zeros((math.ceil(h*s),math.ceil(w*s),4),np.uint8)
    for y in range(out.shape[0]):
        for x in range(out.shape[1]):
            x0=int(x/s);x1=min(w,math.ceil((x+1)/s));y0=int(y/s);y1=min(h,math.ceil((y+1)/s));tile=mask[y0:y1,x0:x1]
            if tile.size and tile.mean()>=.35:
                out[y,x,:3]=np.median(rgb[y0:y1,x0:x1][tile],axis=0);out[y,x,3]=255
    return out

def claude_head():
    colours={'O':'17151A','H':'342923','L':'59443E','D':'78432E','s':'B66C49','k':'E99A69','W':'FFD0A0'}
    rows=(ROOT/'art/concept/characters/chr_dbl_parts_work/claude_head/matrix.txt').read_text().splitlines()
    assert len(rows)==25 and all(len(row)==23 for row in rows)
    a=np.zeros((25,23,4),np.uint8)
    for y,row in enumerate(rows):
        for x,c in enumerate(row):
            if c!='.':a[y,x]=[*bytes.fromhex(colours[c]),255]
    return a

def colour_part(id,a,groups):
    mask=a[:,:,3]>0
    if id=='head':return claude_head()
    garment=mask.copy() if id=='body' else mask&(np.indices(mask.shape)[0]<a.shape[0]*.48) if id.startswith('upper_arm_') else np.zeros(mask.shape,bool)
    belt=mask&(np.indices(mask.shape)[0]>=a.shape[0]*.56)&(np.indices(mask.shape)[0]<=a.shape[0]*.68) if id=='body' else np.zeros(mask.shape,bool)
    garment &= ~belt
    for y,x in zip(*np.where(mask&~garment)):
        palette=groups['belt'] if belt[y,x] else groups['pants']+groups['skin'] if id.startswith('thigh_') else groups['skin'] if id.startswith(('upper_arm_','forearm_','hand_','shin_','foot_')) else groups['fabric']+groups['belt']
        a[y,x,:3]=nearest(a[y,x,:3],palette)
    ys,xs=np.where(garment)
    if len(xs):
        lum=a[ys,xs,:3].astype(float)@np.array([.2126,.7152,.0722]);order=np.argsort(lum,kind='stable')
        for rank,k in enumerate(order):
            q=rank/len(order);a[ys[k],xs[k],:3]=groups['fabric'][0 if q<.15 else 1 if q<.35 else 2 if q<.90 else 3]
    return a

def main():
    work=ROOT/'art/concept/characters/chr_dbl_parts_work';manifest=json.loads((work/'manifest.json').read_text());source=ROOT/manifest['source']
    rgb=np.array(Image.open(source).convert('RGB'));groups=load_groups(ROOT/'art/reference/palette.gpl');pal=[c for name in GROUPS for c in groups[name]]
    definition=json.loads((ROOT/'prototype/rig/data/parts_greybox.json').read_text());parts={p['id']:p for p in definition['parts']}
    # Neutral assembly along its actual source pivots: head->neck->hip->knee->ankle->sole.
    measures=[218,230-16,188-12,164-12,105-19];height=sum(measures);s=96/height
    print(f'SOURCE neutral assembly: head={measures[0]}, torso={measures[1]}, legs={sum(measures[2:])}; H={height}px; guide=24/24/48; s=96/{height}={s:.12f} on BOTH axes')
    print('Scaled anatomical spans:',[round(v*s,4) for v in [measures[0],measures[1],sum(measures[2:])]],'; no independent per-part scale')
    out=ROOT/'art/sprites/characters/chr_dbl_parts';dest=ROOT/'prototype/rig/art_parts';raw=work/'uniform_raw';raw.mkdir(exist_ok=True)
    rows=[];fills={};pivot={id:np.array(l['pivot'],float)*s for id,l in LANDMARKS.items()}
    for item in manifest['parts']:
        id=item['id'];box=item['source_box'];x0,y0,x1,y1=box;crop=rgb[y0:y1,x0:x1];mask=~green_mask(crop)
        if id=='head':crop=crop[:LANDMARKS[id]['crop_bottom']];mask=mask[:len(crop)]
        a=sample_uniform(crop,mask,s)
        if id.startswith(('upper_arm_','forearm_')):
            # User-authorized exception: shorten only the longitudinal arm axis.
            old_h=len(a);new_h=math.ceil(old_h*.60);short=np.zeros((new_h,a.shape[1],4),np.uint8)
            for yy in range(new_h):
                region=a[int(yy/.60):min(old_h,math.ceil((yy+1)/.60))]
                for xx in range(a.shape[1]):
                    cells=region[:,xx];fg=cells[:,3]>0
                    if fg.mean()>=.35:short[yy,xx]=[*np.median(cells[fg,:3],axis=0).astype(np.uint8),255]
            a=short;pivot[id][1]*=.60
        a=colour_part(id,a,groups)
        # Hands/feet retain dark/mid/light skin by a luminance quantile mapping, not aspect changes.
        if id.startswith(('hand_','foot_')):
            ys,xs=np.where(a[:,:,3]>0);lum=a[ys,xs,:3].astype(float)@np.array([.2126,.7152,.0722]);order=np.argsort(lum,kind='stable')
            for rank,k in enumerate(order):a[ys[k],xs[k],:3]=pal[[2,4,5][min(2,rank*3//len(order))]]
        for cluster in ([] if id=='head' else components(a[:,:,3]>0)):
            if len(cluster)<2:
                for x,y in cluster:a[y,x]=0
        Image.fromarray(a).save(raw/f'{id}.png');Image.fromarray(a).save(out/f'{id}.png');shutil.copyfile(out/f'{id}.png',dest/f'{id}.png')
        p=parts[id];old={k:p[k] for k in ['size','pivot','attach']};p['size']=[a.shape[1],a.shape[0]];p['pivot']=pivot[id].tolist()
        if id=='body':attach=np.array([0,-sum(measures[2:])*s])
        elif id=='head':attach=(np.array(LANDMARKS['body']['neck'])-LANDMARKS['body']['pivot'])*s
        elif id.startswith('upper_arm_'):attach=(np.array(LANDMARKS['body']['shoulder'])-LANDMARKS['body']['pivot'])*s
        elif id.startswith('thigh_'):attach=np.array([-1.5 if id.endswith('far') else 1.5,0])
        elif id in ['dao','bow']:
            parent=p['parent'];attach=(np.array(LANDMARKS[parent]['grip'])-LANDMARKS[parent]['pivot'])*s
        else:
            parent=p['parent'];attach=(np.array(LANDMARKS[parent]['end'])-LANDMARKS[parent]['pivot'])*s
        if p['parent'].startswith(('upper_arm_','forearm_')):attach[1]*=.60
        p['attach']=attach.tolist()
        if id.startswith('foot_'):p['angle_limit']=[-75,75]
        p['occluded_fill']='Unoutlined automatic material at true joint; no greybox frame fitting'
        rows.append({'id':id,'source_crop':box,'common_scale':s,'old':old,'new':{k:p[k] for k in ['size','pivot','attach']}})
        if p['parent'] and not id.startswith('foot_') and id not in ['dao','bow']:
            # Small hidden material disk under the joint, with NO outline.
            radius=min(3.0 if id.startswith('hand_') else 4.0,p['size'][0]/2)
            px,py=p['pivot'];patch=a[max(0,int(py-radius-1)):min(len(a),math.ceil(py+radius+2)),max(0,int(px-radius-1)):min(a.shape[1],math.ceil(px+radius+2))]
            inside=patch[patch[:,:,3]>0,:3]
            if not len(inside):inside=a[a[:,:,3]>0,:3]
            colour=nearest(np.median(inside,axis=0),groups['skin'] if id.startswith(('head','forearm_','hand_','shin_')) else groups['fabric'] if id.startswith('upper_arm_') else groups['pants'])
            fills[id]={'radius':radius,'color':'#'+''.join(f'{v:02X}' for v in colour),'method':'automatic unoutlined joint material, not a drawn body outline'}
        print(f'{id}: source={crop.shape[1]}x{crop.shape[0]} -> {p["size"]}; pivot={np.round(p["pivot"],3).tolist()}; attach={np.round(p["attach"],3).tolist()}; shared s, arm-longitudinal=0.60 if applicable')
    definition['status']='Đề xuất — common-scale art measurements, chưa duyệt';definition['common_scale']=s;definition['source_height']=height;definition['source_spans']=measures;definition['parts']=list(parts.values());definition['rotation_center']=[0,-sum(measures[2:])*s]
    bow=LANDMARKS['bow'];definition['bow_string']['top']=((np.array(bow['top'])-bow['pivot'])*s).tolist();definition['bow_string']['bottom']=((np.array(bow['bottom'])-bow['pivot'])*s).tolist();definition['bow_string']['hand_anchor']=((np.array(LANDMARKS['hand_near']['grip'])-LANDMARKS['hand_near']['pivot'])*s).tolist()
    (ROOT/'prototype/rig/data/parts.json').write_text(json.dumps(definition,ensure_ascii=False,indent=2)+'\n');(dest/'joint_fill.json').write_text(json.dumps(fills,indent=2)+'\n')
    measurements={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':s,'height_source':height,'source_spans':measures,'guide':[24,24,48],'scaled_spans':[measures[0]*s,measures[1]*s,sum(measures[2:])*s],'landmarks_manual':LANDMARKS,'parts':rows,'arm_length_scale':.60,'head_source':'đầu do Claude vẽ tay từng pixel','neck_below_chin_px':3,'face_width_px':(200-80)*s,'head_width_px':parts['head']['size'][0]}
    (work/'uniform_measurements.json').write_text(json.dumps(measurements,ensure_ascii=False,indent=2)+'\n')
    head=np.array(Image.open(raw/'head.png'));text=matrix(head,pal);(work/'head_claude.txt').write_text(text+'\n');Image.fromarray(head).save(work/'head_claude.png')
    print('HEAD: đầu do Claude vẽ tay từng pixel; exact supplied matrix, no cleanup or feature edits:');print(text)
    print('Palette:',{c:'#'+''.join(f'{v:02X}' for v in col) for c,col in zip('0123456789ABCDEFG',pal)})
    print(f'Head neck below chin: {measurements["neck_below_chin_px"]:.3f}px; source face span / frame width={measurements["face_width_px"]/parts["head"]["size"][0]:.3f}')
if __name__=='__main__':main()
```

### tools/retarget_parts.py

```python
"""Author new art pose data from old timing/poses and newly measured bones; no A0 physics edits."""
from pathlib import Path
import json,math,copy
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def rotate(v,a):
 t=math.radians(a);return np.array([v[0]*math.cos(t)-v[1]*math.sin(t),v[0]*math.sin(t)+v[1]*math.cos(t)])
def leg_solve(frame,p,side,target):
 b=frame['angles']['body'];hip=np.array(frame['body_position'])+rotate(p['thigh_'+side]['attach'],b)
 v1=np.array(p['shin_'+side]['attach']);v2=np.array(p['foot_'+side]['attach']);l1=np.linalg.norm(v1);l2=np.linalg.norm(v2)
 foot=p['foot_'+side];ankle=np.array([target[0],target[1]-(foot['size'][1]-foot['pivot'][1])]);dx,dy=ankle-hip;dist=math.hypot(dx,dy)
 if dist>l1+l2+.001:raise ValueError(('unreachable',side,dist,l1+l2))
 k=-math.acos(max(-1,min(1,(dist*dist-l1*l1-l2*l2)/(2*l1*l2))));q=math.atan2(-dx,dy)-math.atan2(l2*math.sin(k),l1+l2*math.cos(k));a1=math.atan2(-v1[0],v1[1]);a2=math.atan2(-v2[0],v2[1])
 frame['angles']['thigh_'+side]=math.degrees(q-a1)-b;frame['angles']['shin_'+side]=math.degrees(k+a1-a2);frame['angles']['foot_'+side]=-math.degrees(q+k-a2)
def old_foot(f,side):
 a=f['angles'];b=a['body'];hip=np.array(f['body_position'])+rotate([-2 if side=='far' else 2,0],b);t=b+a['thigh_'+side];s=t+a['shin_'+side];v=hip+rotate([0,22],t)+rotate([0,22],s);return [float(v[0]),float(v[1]+4)]
def main():
 data=json.loads((ROOT/'prototype/rig/data/animations_greybox.json').read_text());d=json.loads((ROOT/'prototype/rig/data/parts.json').read_text());p={x['id']:x for x in d['parts']};base=-p['body']['attach'][1]
 for name,c in data['clips'].items():
  for f in c['frames']:
   old=copy.deepcopy(f);f['body_position'][1]+=48-base;f['root_position'][1]+=48-base
   if name in ['idle','land','run','slash_1','slash_2','slash_3'] or (name=='jump_up' and f is c['frames'][0]):
    for side in ['near','far']:leg_solve(f,p,side,old_foot(old,side))
  if name=='shoot':
   arm=np.array(p['forearm_far']['attach']);fore=np.array(p['hand_far']['attach']);a1=math.atan2(-arm[0],arm[1]);a2=math.atan2(-fore[0],fore[1])
   near1=np.array(p['forearm_near']['attach']);near2=np.array(p['hand_near']['attach']);l1=np.linalg.norm(near1);l2=np.linalg.norm(near2);n1=math.atan2(-near1[0],near1[1]);n2=math.atan2(-near2[0],near2[1])
   for i,f in enumerate(c['frames']):
    f['angles'].update(upper_arm_far=-90-math.degrees(a1),forearm_far=math.degrees(a1-a2),hand_far=math.degrees(a2),bow=90)
    dx=[.94,.65,.23,.94,.8][i]*(l1+l2);dy=[0,-5,-10,0,1][i];k=-math.acos(max(-1,min(1,(dx*dx+dy*dy-l1*l1-l2*l2)/(2*l1*l2))));q=math.atan2(-dx,dy)-math.atan2(l2*math.sin(k),l1+l2*math.cos(k))
    f['angles'].update(upper_arm_near=math.degrees(q-n1),forearm_near=math.degrees(k+n1-n2),hand_near=max(-90,min(90,-90-math.degrees(q+k-n2))))
 data['status']='Đề xuất — retarget geometry only; original frame counts/timings retained'
 (ROOT/'prototype/rig/data/animations.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Retargeted art poses: 13 clips/48 frames; unchanged duration/events; foot targets retained; geometry from common-scale parts')
if __name__=='__main__':main()
```

### tools/outline_parts.py

```python
"""Bake outlines ONLY on the evaluated standing silhouette; no joint-cut borders.
No eye/nose/mouth patches. Source-derived dark facial pixels are preserved and reported.
"""
from pathlib import Path
import json,math,shutil
import numpy as np
from PIL import Image
from render_parts_scene import layers
from snap_pixel import load_groups
ROOT=Path(__file__).resolve().parents[1]
def main():
    data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());frame=data['idle']['frames'][0]
    size=(128,128);origin=(64,120);owner=np.full((128,128),'',object);union=np.zeros((128,128),bool)
    for id,layer in layers(frame,size,origin):
        a=np.asarray(layer)[:,:,3]>0;owner[a]=id;union|=a
    padded=np.pad(union,1);inside=padded[:-2,1:-1]&padded[2:,1:-1]&padded[1:-1,:-2]&padded[1:-1,2:];edge=union&~inside
    definition=json.loads((ROOT/'prototype/rig/data/parts.json').read_text());parts={p['id']:p for p in definition['parts']}
    raw=ROOT/'art/concept/characters/chr_dbl_parts_work/uniform_raw';out=ROOT/'art/sprites/characters/chr_dbl_parts';dest=ROOT/'prototype/rig/art_parts';groups=load_groups(ROOT/'art/reference/palette.gpl');outline=groups['outline'][0]
    counts={}
    for item in frame['geometry']:
        if item['kind']!='sprite':continue
        id=item['id'];p=parts[id];a=np.array(Image.open(raw/f'{id}.png').convert('RGBA'));m=item['transform'];count=0
        if id=='head':
            Image.fromarray(a).save(out/f'{id}.png');shutil.copyfile(out/f'{id}.png',dest/f'{id}.png');continue
        # Exclude the cut planes around proximal and distal joints from border painting.
        joints=[p['pivot']]+[[p['pivot'][i]+c['attach'][i] for i in range(2)] for c in parts.values() if c['parent']==id]
        for y,x in zip(*np.where(a[:,:,3]>0)):
            wx=m[0]*(x+.5)+m[2]*(y+.5)+m[4]+origin[0];wy=m[1]*(x+.5)+m[3]*(y+.5)+m[5]+origin[1];gx=int(math.floor(wx));gy=int(math.floor(wy))
            near_cut=any(abs(y-j[1])<=1 and abs(x-j[0])<=max(2,p['size'][0]/3) for j in joints)
            if 0<=gx<128 and 0<=gy<128 and owner[gy,gx]==id and edge[gy,gx] and not near_cut:
                a[y,x,:3]=outline;count+=1
        # Only source pieces visible in the standing frame get outlines; hidden bow remains material.
        Image.fromarray(a).save(out/f'{id}.png');shutil.copyfile(out/f'{id}.png',dest/f'{id}.png');counts[id]=count
    # Remove ONLY newly painted outline if it becomes internal in either standing pose.
    # Source-derived dark eye/nose/mouth pixels are never changed by this pass.
    protected=groups['outline']
    cleared=0
    for iteration in range(4):
        edits={}
        for name in ['idle','standing_neutral']:
            f=data[name]['frames'][0];composite=Image.new('RGBA',size);owners=np.full((128,128),'',object)
            items={i['id']:i for i in f['geometry'] if i['kind']=='sprite'}
            for id,layer in layers(f,size,origin):
                owners[np.array(layer)[:,:,3]>0]=id;composite.alpha_composite(layer)
            image=np.array(composite);mask=image[:,:,3]>0;pad=np.pad(mask,1);interior=mask&pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:]
            ink=np.zeros(mask.shape,bool)
            for colour in protected:ink|=np.all(image[:,:,:3]==colour,axis=2)
            for y,x in zip(*np.where(interior&ink)):
                id=owners[y,x]
                if id not in items or id=='head':continue
                m=items[id]['transform'];a,b,c,d,tx,ty=m;det=a*d-b*c;wx=x+.5-origin[0]-tx;wy=y+.5-origin[1]-ty
                sx=int(math.floor((d*wx-c*wy)/det));sy=int(math.floor((-b*wx+a*wy)/det))
                original=np.array(Image.open(raw/f'{id}.png').convert('RGBA'));current=np.array(Image.open(out/f'{id}.png').convert('RGBA'))
                for yy in range(max(0,sy-1),min(len(original),sy+2)):
                    for xx in range(max(0,sx-1),min(original.shape[1],sx+2)):
                        if tuple(current[yy,xx,:3]) in protected and tuple(original[yy,xx,:3]) not in protected:
                            edits.setdefault(id,[]).append((xx,yy))
        if not edits:break
        for id,coords in edits.items():
            current=np.array(Image.open(out/f'{id}.png').convert('RGBA'));original=np.array(Image.open(raw/f'{id}.png').convert('RGBA'))
            for x,y in set(coords):current[y,x]=original[y,x];cleared+=1
            Image.fromarray(current).save(out/f'{id}.png');shutil.copyfile(out/f'{id}.png',dest/f'{id}.png')
    print('Removed generated internal-outline samples:',cleared)
    print('Standing silhouette outline pixels painted per source piece:',counts)
    print('Cut planes and joint overdraw remain unoutlined; facial feature edit lists not read.')
if __name__=='__main__':main()
```

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
  allowed=outline+(g['pants']+g['skin'] if id.startswith('thigh_') else g['skin'] if id.startswith(('forearm_','hand_','shin_','foot_')) else g['fabric']+g['skin'] if id.startswith('upper_arm_') else g['fabric']+g['belt'])
  if id=='head':allowed=outline+[g['pants'][1]]+g['skin'];same=np.array_equal(a,claude_head());print('Head exact Claude matrix:',same);errors+=[] if same else ['head changed']
  bad=[(int(x),int(y)) for y,x in zip(*np.where(a[:,:,3]>0)) if tuple(a[y,x,:3]) not in allowed]
  report[id]={'forbidden_group_pixels':len(bad)};print(f'{id}: forbidden group pixels={len(bad)}');errors+=bad
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
```
