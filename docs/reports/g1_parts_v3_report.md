# G1 — Chỉnh dáng và thân v3 (29/10/2026)

**v3 chờ người dùng duyệt**. Main nguồn8bd5876, nhánhfix/g1-parts-v3.
Không dùng imagegen. Đầu giữ nguyên RGBA/pivot/attach; A0 và Đào Úc không sửa.

## Số đo và cơ sở

Đo ảnh nghiêng gốc tại ROI (610,20)–(780,570), tách nền xanh: cao520 px;
vai y198, giữa ngực y240, hông dưới đai y330. Bề ngang là trung vị ba hàng
liền nhau của đường bao nhìn thấy (có tay/áo che), không suy đoán cơ thể bị che.
Trên rig lấy đúng các mức tương ứng giữa cổ và gấu áo từ transform scene thật;
chia chiều cao alpha thực của PNG idle. Script: `prototype/rig/measure_reference.py --v3`.

| Vị trí | Ảnh nghiêng w/H | Idle trước w/H | Idle sau w/H | Sai lệch sau |
|---|---:|---:|---:|---:|
| shoulder | 76/520 = 0.146154 | 12/95 = 0.126316 | 14/96 = 0.145833 | -0.219% |
| chest | 93/520 = 0.178846 | 14/95 = 0.147368 | 17/96 = 0.177083 | -0.986% |
| hip | 99/520 = 0.190385 | 17/95 = 0.178947 | 19/96 = 0.197917 | +3.956% |

Body: size17×29 →23×29; pivot(7,3758865;26,0992908) →(11,3758865;26,0992908);
attach giữ (0;−46,9787234). Các size/pivot/attach khác giữ nguyên. Áo dùng nhóm
fabric/belt, gấu qua đai giữ chiều dài cũ; viền thân chỉ theo đường bao ngoài,
không tô viền mặt cắt cổ/khớp. Không đổi upper_arm.

Thêm Node2D phụ `hip` (không phải bộ phận thứ17). Parent của thigh_near/far:
body → hip, attach không đổi; `art_parent: body` giữ phép kiểm khe ảnh với thân.
Mặc định helper theo đúng transform body cũ, nên động tác khác không đổi tọa độ khớp.
Trong idle, hông y−47,0645254 cố định; chỉ thân/đầu/tay đi y0,−1,−2,−1 px.
Hai chân thẳng, thân0°, hai đế y0 (sai số float <0,00001 px). Giữ số khung/thời lượng.
Toàn bộ dữ liệu các clip khác giữ nguyên, chỉ thay khung cuối turn/land thành đứng thẳng.

| Trạng thái | Clip/khung | Gối gần/xa (°) | Thân (°) | Hông y (px) | Thân y (px) | Đế gần/xa y (px) |
|---|---|---:|---:|---:|---:|---:|
| before | idle/1 | 25.555/25.555 | 0.000 | -45.978722 | -45.978722 | 0.000002/-0.000000 |
| before | idle/2 | 36.991/36.991 | 0.000 | -44.978722 | -44.978722 | 0.000004/0.000002 |
| before | idle/3 | 45.718/45.718 | 0.000 | -43.978722 | -43.978722 | 0.000002/0.000002 |
| before | idle/4 | 36.991/36.991 | 0.000 | -44.978722 | -44.978722 | 0.000004/0.000002 |
| before | turn/1 | 0.051/0.051 | 0.000 | -46.978722 | -46.978722 | 0.085108/0.085108 |
| before | turn/2 | 0.051/0.051 | 0.000 | -46.978722 | -46.978722 | 0.085108/0.085108 |
| before | land/1 | 80.486/78.499 | 8.000 | -37.978722 | -37.978722 | 0.000003/0.000003 |
| before | land/2 | 36.991/36.991 | 0.000 | -44.978722 | -44.978722 | 0.000004/0.000002 |
| after | idle/1 | 0.000/0.000 | 0.000 | -47.064526 | -47.064526 | -0.000002/-0.000002 |
| after | idle/2 | 0.000/0.000 | 0.000 | -47.064526 | -48.064526 | -0.000002/-0.000002 |
| after | idle/3 | 0.000/0.000 | 0.000 | -47.064526 | -49.064526 | -0.000002/-0.000002 |
| after | idle/4 | 0.000/0.000 | 0.000 | -47.064526 | -48.064526 | -0.000002/-0.000002 |
| after | turn/1 | 0.051/0.051 | 0.000 | -46.978722 | -46.978722 | 0.085108/0.085108 |
| after | turn/2 | 0.000/0.000 | 0.000 | -47.064526 | -47.064526 | -0.000002/-0.000002 |
| after | land/1 | 80.486/78.499 | 8.000 | -37.978722 | -37.978722 | 0.000003/0.000003 |
| after | land/2 | 0.000/0.000 | 0.000 | -47.064526 | -47.064526 | -0.000002/-0.000002 |

Khung vẫn128×128, chân ở y120 (cách đáy8), idle đầu cao96 px. PNG idle cũ thực
cao95 px; không co giả bản trước. Khi thở nhấc thân lên1–2 px, alpha toàn dáng
cao97–98 px; đó là dịch thân theo yêu cầu, không đổi tỉ lệ/khung/hitbox A0.
Neutral measurement nay lấy đúng idle frame0, không đặt mọi góc0 như cách cũ.


## Ảnh thật và cách tái tạo

[So sánh](g1_parts_v3_compare.png): trên là ảnh tham chiếu nghiêng tách nền,
thu đồng dạng cao96 px; dưới trái là idle trước từ scene main, dưới phải idle sau.
Toàn bộ ghép128px được phóng4×NEAREST, không chèn chữ/hình vẽ.
Ảnh trước1× lưu tại [before](g1_parts_v3_before_idle_1x.png).
15 contact sheet (13 động tác và run/shoot trái) cùng idle1×/4× được xuất lại
trong [thư mục art](../../prototype/rig/contact_sheets/art/).

Các script đã chạy (mã nguồn thật trong repo):
- [Author v3](../../tools/polish_parts_v3.py): body resample theo hàng, trung vị + ép nhóm palette; tạo dữ liệu đứng thẳng; đọc fixture main, không ghi đầu.
- [Body outline](../../tools/outline_parts_v3.py): viền1 px chỉ theo silhouette xuất scene, bỏ mặt cắt cổ/khớp.
- [Godot exporter](../../prototype/rig/export_frames.gd): evaluate AnimationPlayer/Sprite2D scene thật.
- [Rasterizer](../../tools/render_parts_scene.py): đọc PNG thật và transform scene, nearest; không vẽ lại nhân vật.
- [Đo ảnh/pose](../../prototype/rig/measure_reference.py): `--v3`, tự in hai bảng trên từ PNG/scene.
- [Regression + ảnh ghép](../../tools/check_parts_v3.py): RGBA đầu so main, metadata, counts/timing, dữ liệu clip, tọa độ khớp động tác cũ, hông/chân/thở, khung/margin.
- [Khe khớp](../../tools/check_parts.py), [palette/viền](../../tools/check_parts_uniform.py), [nhóm màu](../../tools/check_parts_roles.py), [polish](../../tools/check_parts_polish.py), [trục vũ khí](../../tools/check_weapon_axes.py).

Fixture trước ở `prototype/rig/reports/v3_baseline/`: parts/animations từ main,
export scene main trước chỉnh. Dữ liệu đo sau: `parts_v3_measurements.json`.
Không đổi số A0, file config, các cảnh Đào Úc hay checklist. Bản này chưa được
người dùng duyệt trên Android; script chỉ kiểm48 khung tác giả hóa/13 động tác,
không khẳng định mọi thời điểm nội suy/GPU điện thoại.

## Nguyên đầu ra

Xem [đầu ra lệnh đầy đủ](g1_parts_v3_checks.txt); cũng chép nguyên vào commit message.
Hai FAIL tỷ lệ **before** là số đo lịch sử chứng minh lỗi cũ; toàn bộ tỷ lệ **after** phải PASS.
