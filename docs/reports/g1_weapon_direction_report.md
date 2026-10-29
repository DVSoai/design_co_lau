# G1 — Sửa hướng đao quanh điểm cầm (29/10/2026)

**Đang làm, chưa duyệt mỹ thuật.** Tiếp trên `fix/g1-parts-polish`, sau `c0d6c58`.

## Lỗi và cách sửa

Ở dữ liệu trước, trục lưỡi trong PNG trỏ −Y nhưng frame để góc đao bằng 0,
vì vậy lưỡi vươn về khuỷu/ngực. `tools/retarget_parts.py` xoay đao 180° quanh
pivot cầm hiện có; bù góc bàn tay để không đưa lưỡi ngược về khuỷu khi cổ tay
xoay. Không đổi pivot, attach, kích thước hay hình học khớp.

Riêng idle/turn, đặt trục chuôi→mũi ở 60° trong hệ rig nhìn phải: mũi hướng xuống
và ra trước chân. Lật nhân vật thì hướng trước lật theo. Những frame còn lại
cho lưỡi theo cẳng tay ra khỏi nắm tay. Mọi góc lưu trong dữ liệu JSON,
không sửa điều khiển/hitbox A0. Góc chân đã giảm 35% ở lượt trước giữ nguyên.

Cung: tâm vẫn ở điểm cầm của bàn tay xa, trục cung gần vuông góc với cẳng tay
xa lúc bắn. Không đổi pose cung. Đường nối hai đầu cánh cung không thẳng tuyệt
đối do hình cong lệch 3 px nguồn; góc đo thật 89,510°, lệch 0,490° so với 90°.

## Phép kiểm trên scene thật

Exporter thêm `weapon_axes` từ global transform của Node2D/Sprite2D, kể cả đao
đang ẩn khi preview shoot. Mũi lấy tâm hai pixel thật trên cùng của PNG: (7;0,5),
kiểm lại landmark bằng PIL. Điểm chuôi là pivot hiện có, nằm trên pixel cán đặc.

- **59 frame:** 48 frame / 13 động tác, thêm 6 run trái và 5 shoot trái.
- Ngoài idle/turn: góc giữa chuôi→mũi và khuỷu→cổ tay khoảng **6,801°**, dưới 30°.
- Idle/turn: mũi có thành phần hướng xuống và ra trước; góc cẳng tay khoảng 29,332°.
- Mọi frame: chiếu mũi lên trục khuỷu→cổ tay có t≥4,5028 (khuỷu t=0, cổ tay t=1).
  Không mũi nào nằm trong đoạn khuỷu–cổ tay. In góc và t riêng từng frame.
- Shoot cả hai hướng: trục cung/cẳng tay **89,510°** (dung sai vuông góc 1°),
  tâm cung lệch điểm cầm bàn tay xa **0,000000 px**.

Godot **4.7.2 Standard**: ba lệnh headless README, rig smoke, art/visual tests,
kiểm palette/nhóm màu/alpha, viền trong dáng và khớp đều đạt. 16 PNG đúng size,
0 pixel sai palette/nhóm/bán trong suốt; 672 cặp khớp, khe lớn nhất **0,50 px**.
Các phần cần bôi viền theo dáng đứng được dựng lại sau khi đao đổi hướng;
17 pixel nét nội bộ ở đầu Claude giữ nguyên, ngoài đầu 0. Không dùng imagegen.

Kiểm này bao phủ pose đã tác giả hóa, không thay duyệt mỹ thuật hoặc thử Android.
XDG_DATA_HOME/CONFIG_HOME/CACHE_HOME dùng thư mục tạm `/tmp/polish-xdg/`.

## Ảnh xuất lại

Tất cả 15 contact sheet art được xuất lại từ scene, gồm các ảnh được yêu cầu:

- [Idle](../../prototype/rig/contact_sheets/art/chr_dbl_anim_idle_art.png)
- [Run](../../prototype/rig/contact_sheets/art/chr_dbl_anim_run_art.png)
- [Slash 1](../../prototype/rig/contact_sheets/art/chr_dbl_anim_slash_1_art.png)
- [Slash 2](../../prototype/rig/contact_sheets/art/chr_dbl_anim_slash_2_art.png)
- [Slash 3](../../prototype/rig/contact_sheets/art/chr_dbl_anim_slash_3_art.png)
- [Shoot](../../prototype/rig/contact_sheets/art/chr_dbl_anim_shoot_art.png)
- [Idle ×4](../../prototype/rig/contact_sheets/art/chr_dbl_idle_art_4x.png), tạo
  bằng Image.resize(..., Image.Resampling.NEAREST) từ PNG 1× đã lưu.

## Nguyên đầu ra và script

[Toàn bộ đầu ra](g1_weapon_direction_output.txt), cũng chép nguyên vào commit
message. [Các script kiểm palette/khớp/viền](g1_parts_polish_report.md#script-đã-chạy)
giữ nguyên; [script retarget](../../tools/retarget_parts.py) và
[export scene](../../prototype/rig/export_frames.gd) đã bổ sung hướng vũ khí.
Script đo mới đã chạy trên file thật, nguyên văn:

```python
"""Measure actual Godot scene weapon axes, including hidden dao in shoot frames."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def angle(a,b):
 return math.degrees(math.acos(float(np.clip(a@b/(np.linalg.norm(a)*np.linalg.norm(b)),-1,1))))
def main():
 data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());definition=json.loads((ROOT/'prototype/rig/data/parts.json').read_text());parts={p['id']:p for p in definition['parts']};errors=[];rows=[]
 tex=np.array(Image.open(ROOT/'prototype/rig/art_parts/dao.png').convert('RGBA'));ys,xs=np.where(tex[:,:,3]>0)
 # Actual topmost blade pixels x=6,7 at y=0; their centre is (7,.5).
 if ys.min()!=0 or set(xs[ys==0])!={6,7}:errors.append('tip landmark no longer matches actual PNG')
 pivot=parts['dao']['pivot'];grip=tex[round(pivot[1]),round(pivot[0])]
 if grip[3]!=255:errors.append('grip outside solid hilt')
 for name,clip in data.items():
  if name=='standing_neutral':continue
  for index,frame in enumerate(clip['frames']):
   p={k:np.array(v,float) for k,v in frame['weapon_axes'].items()};fore=p['near_wrist']-p['near_elbow'];blade=p['dao_tip']-p['dao_grip'];deg=angle(blade,fore)
   t=float((p['dao_tip']-p['near_elbow'])@fore/(fore@fore));between=0<=t<=1
   rest=name in ['idle','turn'];forward=blade[0]*(-1 if name.endswith('_left') else 1)
   ok=(not between) and (deg<=30.001 if not rest else blade[1]>0 and forward>0)
   if not ok:errors.append(f'{name}/{index+1} dao axis')
   row={'clip':name,'frame':index+1,'dao_angle_deg':round(deg,4),'tip_projection_elbow_to_wrist':round(t,4),'tip_between_elbow_wrist':between,'rest_down_forward':bool(rest and blade[1]>0 and forward>0),'ok':bool(ok)};rows.append(row)
   print(f'{"PASS" if ok else "FAIL"}: {name} frame={index+1}: dao vs forearm={deg:.3f}deg; tip projection={t:.3f}; between={between}; rest={rest}')
   if name in ['shoot','shoot_left']:
    bow=p['bow_bottom']-p['bow_top'];far=p['far_wrist']-p['far_elbow'];bow_angle=angle(bow,far);distance=float(np.linalg.norm(p['bow_grip']-p['far_grip']))
    good=abs(bow_angle-90)<=1.0 and distance<.001
    row.update(bow_angle_deg=round(bow_angle,4),bow_grip_error_px=round(distance,6))
    print(f'{"PASS" if good else "FAIL"}: {name} frame={index+1}: bow vs forearm={bow_angle:.3f}deg; grip error={distance:.6f}px')
    if not good:errors.append(f'{name}/{index+1} bow axis')
 (ROOT/'prototype/rig/reports/weapon_axes_checks.json').write_text(json.dumps({'method':'Godot evaluated node/Sprite2D transforms; actual PNG tip centre (7,.5), existing hilt pivot; projection t in [0,1] is between elbow/wrist','frames':len(rows),'failures':len(errors),'details':rows},indent=2)+'\n')
 print('Weapon axis failures:',len(errors),errors);raise SystemExit(bool(errors))
if __name__=='__main__':main()
```
