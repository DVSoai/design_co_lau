# Rig nhân vật Đinh Bộ Lĩnh — greybox Giai đoạn 1, bước 1

**Đề xuất — chưa duyệt bộ phận, khớp, pose hay mỹ thuật.** Chỉ là thử nghiệm trong
`prototype/`, không phải mã game thật, không chép sang `co_lau_game`. Không mở Mốc A
hay Giai đoạn 2. Nguồn: `01_art_bible.md`, `09_animation_spec.md`, `13_thong_so.md`.
Giữ chuẩn A0: người 96 px, khung 128×128, chân tại (64,120), hitbox 24×88;
Godot **4.7.2 Standard/GDScript**. Khối màu phân biệt mảnh, không phải art/palette mới.

## 1. Đo ảnh tham chiếu

Ảnh thật: `art/reference/ref_dinh_bo_linh.png`, 1735×576, góc nghiêng nhìn phải ở
ROI [610,20,780,570) (tọa độ ảnh gốc, phải/dưới loại trừ). Bỏ nền xanh bằng ngưỡng
G>240, R<20, B<20 để lấy silhouette. Cổ y=174 và hông y=299 là mốc giải phẫu chọn
bằng mắt; áo che hông nên số đo chỉ là đối chiếu, không phải tự động nhận dạng cơ thể.
Silhouette từ y=40 đến trước y=560: **520 px**. Chuẩn hóa bằng 96/520:

| Vùng | Khoảng y nguồn | Cao nguồn | Quy về 96 px | Greybox đề xuất |
|---|---|---|---|---|
| Đầu kèm tóc | [40,174) | 134 px | 24,738 px | 24 px |
| Thân (cổ đến hông) | [174,299) | 125 px | 23,077 px | 24 px |
| Chân kèm bàn chân | [299,560) | 261 px | 48,185 px | 48 px |

Tổng greybox 24+24+48=96 px, khoảng bốn đầu. Làm tròn có chủ ý để thử rig;
không tự thay tỉ lệ ảnh/art đã duyệt. Chân khung nghỉ ở y=0 trong hệ rig, đỉnh y=−96.
Báo cáo đo có SHA-256 ảnh nguồn: `prototype/rig/reports/reference_measurements.json`.

Script đã chạy (`python prototype/rig/measure_reference.py`), nguyên văn:

```python
"""Measure manually identified anatomical landmarks on the actual side-view reference.
Segmentation detects the silhouette; neck and hip landmarks are explicitly manual,
not claimed to be inferred automatically from clothing pixels.
"""
from pathlib import Path
import hashlib, json
from PIL import Image
root = Path(__file__).resolve().parents[2]
p = root / 'art/reference/ref_dinh_bo_linh.png'
im = Image.open(p).convert('RGB')
box = (610, 20, 780, 570)
points = [(x,y) for y in range(box[1],box[3]) for x in range(box[0],box[2])
          if not (lambda c: c[1] > 240 and c[0] < 20 and c[2] < 20)(im.getpixel((x,y)))]
top, bottom = min(y for x,y in points), max(y for x,y in points)+1
# Half-open ranges; chosen visually at neck and waist/hip of the side view.
neck, hip = 174, 299
height = bottom-top
result = {'image':str(p.relative_to(root)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
          'image_size':list(im.size), 'side_roi':list(box), 'silhouette_y':[top,bottom],
          'manual_neck_y':neck, 'manual_hip_y':hip, 'height_source_px':height,
          'segments':{name:{'source_px':b-a, 'at_96_px':round((b-a)*96/height,3)}
                      for name,a,b in [('head_hair',top,neck),('torso',neck,hip),('legs_feet',hip,bottom)]}}
text=json.dumps(result,ensure_ascii=False,indent=2)
(root/'prototype/rig/reports/reference_measurements.json').write_text(text+'\n')
print(text)
```

## 2. Hệ khớp và bộ phận

Chọn **cây Node2D + AnimationPlayer**. Mỗi mảnh cứng là một Polygon2D con của
Node2D tại khớp; không skin/biến dạng lưới nên không cần Skeleton2D/IK. Cấu trúc này
cho kiểm tra khớp cha–con trực tiếp, thay mảnh trang bị mà không đổi clip. AnimationPlayer
nạp track từ JSON, không viết pose trong mã. AnimationTree chưa cần cho thử nghiệm này.

Tọa độ px logic: x phải, y xuống. Pivot tính từ góc trên-trái khung mảnh. `attach`
là vị trí pivot trong hệ khớp cha; root nằm ở chân, tâm xoay hình tại (0,−48).
Mảnh body nghỉ tại (0,−48). Bảng là dữ liệu đề xuất, cùng nguồn với
`prototype/rig/data/parts.json`; góc độ tính tương đối khớp cha, dương theo chiều kim
đồng hồ. Xoay toàn vòng chỉ ở PoseRoot, không áp giới hạn cục bộ cho vòng lộn.
Thứ tự z tuyệt đối: số nhỏ ở xa, số lớn ở gần; polygon không cộng z cha.

| Mảnh | Khung W×H px | Pivot px | Cha | Attach px | z | Góc cho phép (độ) | Vẽ bù bị che |
|---|---|---|---|---|---|---|---|
| `body` | 20×26 | (10, 24) | `root` | (0, -48) | 0 | -30…30 | Cổ/vai/hông kín thêm 2 px |
| `head` | 18×24 | (9, 24) | `body` | (0, -24) | 1 | -30…30 | Chân cổ 2 px; tóc sau đầu kín |
| `upper_arm_far` | 8×19 | (4, 2) | `body` | (0, -21) | -6 | -160…160 | Vai và khuỷu: chồng kín 2 px |
| `forearm_far` | 7×17 | (3, 2) | `upper_arm_far` | (0, 15) | -5 | -150…150 | Khuỷu/cổ tay: chồng kín 2 px |
| `hand_far` | 7×8 | (3, 2) | `forearm_far` | (0, 13) | -4 | -90…90 | Cổ tay 2 px và lòng bàn tay sau cán |
| `thigh_far` | 10×24 | (5, 2) | `body` | (-2, 0) | -6 | -100…100 | Hông/gối: chồng kín 2 px |
| `shin_far` | 8×24 | (4, 2) | `thigh_far` | (0, 22) | -5 | -140…140 | Gối/cổ chân: chồng kín 2 px |
| `foot_far` | 14×6 | (4, 2) | `shin_far` | (0, 22) | -4 | -60…60 | Cổ chân 2 px, vẽ đầy gót/bàn chân |
| `upper_arm_near` | 8×19 | (4, 2) | `body` | (0, -21) | 3 | -160…160 | Vai và khuỷu: chồng kín 2 px |
| `forearm_near` | 7×17 | (3, 2) | `upper_arm_near` | (0, 15) | 4 | -150…150 | Khuỷu/cổ tay: chồng kín 2 px |
| `hand_near` | 7×8 | (3, 2) | `forearm_near` | (0, 13) | 5 | -90…90 | Cổ tay 2 px và lòng bàn tay sau cán |
| `thigh_near` | 10×24 | (5, 2) | `body` | (2, 0) | 3 | -100…100 | Hông/gối: chồng kín 2 px |
| `shin_near` | 8×24 | (4, 2) | `thigh_near` | (0, 22) | 4 | -140…140 | Gối/cổ chân: chồng kín 2 px |
| `foot_near` | 14×6 | (4, 2) | `shin_near` | (0, 22) | 5 | -60…60 | Cổ chân 2 px, vẽ đầy gót/bàn chân |
| `dao` | 5×34 | (2, 28) | `hand_near` | (0, 4) | 7 | -180…180 | Cán kín dưới bàn tay 4 px |
| `bow` | 10×38 | (5, 19) | `hand_far` | (0, 4) | -2 | -180…180 | Tay cầm giữa cung kín 4 px |

`head` gồm tóc; `upper_arm/forearm/hand` là tay trên/tay dưới/bàn tay;
`thigh/shin/foot` là đùi/cẳng/bàn chân, mỗi loại có near (gần) và far (xa).
`dao` gắn bàn tay gần, `bow` gắn bàn tay xa; chỉ hiện một vũ khí. Khối cung là hình
chữ nhật màu riêng để kiểm tay cầm, chưa vẽ dây/cánh cung hay tạo đạn thật.
Mọi mảnh hiện là chữ nhật, phần chồng khớp nằm trong khung, không cộng thêm vào chiều cao 96.

## 3. Tên file và thay trang bị

- Bộ gốc: `chr_dbl_parts_<part>_vN.png`, ví dụ `chr_dbl_parts_forearm_near_v1.png`.
- Metadata khớp tương ứng: `chr_dbl_parts_vN.json`, ghi size/pivot/attach/parent/z/giới hạn.
- Trang bị: `chr_dbl_t1_<part>_vN.png` … `chr_dbl_t7_<part>_vN.png`; ví dụ
  `chr_dbl_t3_body_v1.png`, `chr_dbl_t3_thigh_near_v1.png`,
  `chr_dbl_t3_dao_v1.png` hoặc `chr_dbl_t3_bow_v1.png`. Mảnh đầu/tay/chân dùng chung
  nếu không đổi; áo thay body và mảnh tay áo, quần thay thigh/shin. Giữ nguyên khớp.
- Dữ liệu động tác: `chr_dbl_anim_<clip>_vN.json`; prototype hiện gom các clip vào
  `rig/data/animations.json`. Trang bị chỉ thay mảnh, không nhân bản pose từng bậc.
- Chưa tạo PNG bộ phận, chưa imagegen hay đưa khối màu vào art/approved.

## 4. Dữ liệu động tác

Schema v1 trong `prototype/rig/data/animations.json`: mỗi clip có `frames[]`,
mỗi frame có duration (s), góc từng mảnh (độ), body_position (px), root_position (px), root_angle (độ).
Clip có loop, weapon, events[] (frame đếm từ 1), end_root_angle và trạng thái.
AnimationPlayer dùng pose rời cho các mảnh; góc PoseRoot nội suy không quấn ngược
để vòng lộn đủ 360°. Khóa cuối 360° không tính là khung nghệ thuật thứ bảy.
Events là marker kiểm tra/xem, **không** điều khiển hitbox, gây sát thương, âm thanh hay
spawn đạn. Nhịp chiến đấu thật vẫn do A0 quyết định.

| Clip | Khung | Tổng thời lượng | Lặp | Trạng thái/căn cứ |
|---|---|---|---|---|
| `idle` | 4 | 0.666667 s | Có | Tạm thời — số khung theo 09_animation_spec.md |
| `run` | 6 | 0.500000 s | Có | Tạm thời — số khung theo 09_animation_spec.md |
| `jump_up` | 2 | 0.380000 s | Không | Đề xuất — 2 khung; tổng 0,38 s theo A0 |
| `apex_flip` | 6 | 0.200000 s | Không | Đề xuất — 6 khung + khóa kết thúc 360°; tổng 0,20 s đã duyệt A0 |
| `fall` | 2 | 0.166667 s | Có | Tạm thời — số khung theo 09_animation_spec.md |
| `land` | 2 | 0.166667 s | Không | Tạm thời — số khung theo 09_animation_spec.md |
| `turn` | 2 | 0.050000 s | Không | Đề xuất — 2 khung; tổng 0,05 s theo A0, hướng mặt do A0 quyết định |
| `slash_1` | 4 | 0.300000 s | Không | Đề xuất — combo; nhát 1 tổng 0,30 s, hit 0,10–0,20 theo A0 |
| `slash_2` | 4 | 0.266667 s | Không | Đề xuất — combo chỉ xem, không đổi chiến đấu A0 |
| `slash_3` | 5 | 0.333333 s | Không | Đề xuất — combo chỉ xem, không đổi chiến đấu A0 |
| `shoot` | 5 | 0.333333 s | Không | Tạm thời — số khung theo 09_animation_spec.md |
| `hurt` | 2 | 0.166667 s | Không | Tạm thời — số khung theo 09_animation_spec.md |
| `knockdown` | 4 | 0.400000 s | Không | Tạm thời — số khung theo 09_animation_spec.md |

- Nhảy lên: hai pose trong 0,38 s; trạng thái thật chuyển sang lộn khi A0 vào cửa sổ đỉnh,
  không chờ phát hết clip và không kéo dài quỹ đạo.
- Lộn: đề xuất sáu pose trong đúng 0,20 s. Mỗi pha nhảy/khinh công lấy thời gian,
  chiều vòng và hàng đợi từ player A0. Không cộng thêm xoay sprite tạm lên rig.
- Quay đầu: đề xuất hai pose 0,025 s; không dùng 12 fps để kéo dài TURN_TIME.
- Chém 1: bốn pose thời lượng 0,10/0,10/0,05/0,05 s, hit khung 2,
  khớp cửa sổ A0 [0,10;0,20). Combo 2 (4/15 s), combo 3 (5/15 s) chỉ xem trong bộ
  chọn pose, chưa thêm combo vào A0. Spec có hit/cancel 2/3 cho nhát 2, 3/5 cho nhát 3.
- Bắn: 5 khung/15 fps, spawn khung 4, cancel 5 theo spec; khi dùng trên A0, clip được
  đồng bộ theo ATTACK_DURATION hiện tại, chỉ thay hình, không thêm cơ chế bắn hay đổi hitbox.
- Chạm đất: pose gập gối có bù cao độ hông trong dữ liệu để hai bàn chân tiếp đất.
- Ngã: root_position trong dữ liệu bù đường đất theo từng pose, không áp vào body A0.
- Trúng đòn/ngã: xem bằng bộ chọn clip, vì A0 không có trạng thái bị đánh/chết.
- Các khung theo bảng 09 vẫn Tạm thời/Đề xuất, không được coi là đã duyệt vì qua test.

## 5. Chạy và kiểm tra

F5 mở A0 gốc. Bấm **Mở rig greybox** để sang `rig/rig_greybox.tscn` (hoặc mở scene
đó và F6). Đây là bản kế thừa A0, giữ nguyên player/world/hitbox và điều khiển.
Trong ⚙: **Rig greybox** thay sprite tạm, tắt để so sánh; **Vũ khí cung** đổi hình
đao/cung; bộ chọn clip mặc định **Theo trạng thái thật A0**, chọn clip khác để xem
đủ combo/hurt/ngã; **Về A0 gốc** trở lại. Công tắc chỉ ở cảnh mới, không sửa bảng ⚙
hay mã player của A0 gốc. F1 hiện khớp; thao tác preview không áp root motion lên body.

Chạy ba lệnh README bằng Godot 4.7.2, rồi test rig:

```sh
godot --headless --path prototype --editor --import --quit
godot --headless --path prototype --quit-after 120
godot --headless --path prototype --script res://tests/smoke.gd
godot --headless --path prototype --script res://tests/rig_smoke.gd
```

Tạo lại tờ khung từ **chính scene đã được AnimationPlayer tính pose**:

```sh
python prototype/rig/measure_reference.py
godot --headless --path prototype --script res://rig/export_frames.gd
python prototype/rig/render_contact_sheets.py
```

`export_frames.gd` instantiate `rig.tscn`, seek từng thời điểm frame và lấy polygon
sau transform thật của scene vào `rig/reports/evaluated_frames.json`. Python/PIL chỉ
tô các polygon đó theo z, không tính lại pose hay dùng imagegen. Đường ngang là y=0,
mỗi ô 160×160, đặt gốc chân (80,126). PNG tại `prototype/rig/contact_sheets/`, mỗi clip
một tờ, đúng số khung dữ liệu. Đây là raster phần rig từ scene, không phải screenshot
GPU của toàn cảnh gameplay. Cần người dùng xem trực tiếp trong Godot 4.7.2/Android.

Điều kiện tự kiểm: đủ số khung; mọi pivot con trùng attach của cha ở từng pose;
góc trong giới hạn đề xuất; chân đứng/chạm đất ở y=0; vòng lộn đúng 360°/0,20 s và
hoàn tất trước khi đáp cùng cao độ, kể cả khinh công; tắt rig khôi phục sprite;
nhịp/transform body, slash và các thông số A0 không đổi. Đáp bậc/va trần vẫn theo
va chạm A0; không trì hoãn đáp đất để hoàn tất vòng lộn. Chưa duyệt rig/mỹ thuật.
