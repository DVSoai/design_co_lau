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

## 2. Hệ khớp và bộ phận greybox cũ

Chọn **cây Node2D + AnimationPlayer**. Mỗi mảnh cứng là một Polygon2D con của
Node2D tại khớp; không skin/biến dạng lưới nên không cần Skeleton2D/IK. Cấu trúc này
cho kiểm tra khớp cha–con trực tiếp, thay mảnh trang bị mà không đổi clip. AnimationPlayer
nạp track từ JSON, không viết pose trong mã. AnimationTree chưa cần cho thử nghiệm này.

Tọa độ px logic: x phải, y xuống. Pivot tính từ góc trên-trái khung mảnh. `attach`
là vị trí pivot trong hệ khớp cha; root nằm ở chân, tâm xoay hình tại (0,−48).
Mảnh body nghỉ tại (0,−48). Bảng là dữ liệu đề xuất, cùng nguồn với
`prototype/rig/data/parts_greybox.json`; góc độ tính tương đối khớp cha, dương theo chiều kim
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
| `bow` | 6×38 | (3, 19) | `hand_far` | (0, 0) | -2 | -180…180 | Tay cầm giữa cung kín 4 px |

`head` gồm tóc; `upper_arm/forearm/hand` là tay trên/tay dưới/bàn tay;
`thigh/shin/foot` là đùi/cẳng/bàn chân, mỗi loại có near (gần) và far (xa).
`dao` gắn bàn tay gần, `bow` gắn bàn tay xa; chỉ hiện một vũ khí. Khối cung là hình
chữ nhật màu riêng để kiểm tay cầm, có dây mảnh Line2D nối hai đầu cung qua tay kéo; chưa vẽ cánh cung hay tạo đạn thật.
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
Clip có layer_overrides (z cục bộ theo động tác), loop, weapon, events[] (frame đếm từ 1), end_root_angle và trạng thái.
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
một tờ, đúng số khung dữ liệu; thêm hai tờ `run_left` và `shoot_left` từ scale.x=−1 của scene (15 tờ cho 13 clip). Đây là raster phần rig từ scene, không phải screenshot
GPU của toàn cảnh gameplay. Cần người dùng xem trực tiếp trong Godot 4.7.2/Android.

Điều kiện tự kiểm: đủ số khung; mọi pivot con trùng attach của cha ở từng pose;
góc trong giới hạn đề xuất; chân đứng/chạm đất ở y=0; vòng lộn đúng 360°/0,20 s và
hoàn tất trước khi đáp cùng cao độ, kể cả khinh công; tắt rig khôi phục sprite;
nhịp/transform body, slash và các thông số A0 không đổi. Đáp bậc/va trần vẫn theo
va chạm A0; không trì hoãn đáp đất để hoàn tất vòng lộn. Chưa duyệt rig/mỹ thuật.

## 6. Sửa pose thân và cung sau xem contact sheet (chưa duyệt)

- **Shoot:** cung 6×38 px, pivot (3,19), attach (0,0) tại bàn tay xa. Tay xa duỗi ngang vai về trước, góc tay trên −90°, khuỷu 0°. Cung bù +90° để trục dài luôn dọc. Tay gần kéo từ phía tâm cung về vai/má ở khung 1–3, thả khung 4 (marker spawn giữ nguyên), thu tay khung 5. Dây 1 px nối đỉnh/đáy cung tới điểm tay gần; màu/đầu dây/điểm tay lấy từ `parts.json`. Line2D chạy trong scene và được xuất cùng polygon, không chỉ vẽ thêm lên contact sheet.
- **Tay xa khi bắn:** layer_overrides nâng tay trên/tay dưới xa lên z=1, bàn tay xa z=2 để không chìm trong thân/vũ khí; tay gần vẫn z=3/4/5. Khi sang clip khác trả về z mặc định. Không đổi nhãn gần/xa khi lật hướng: mảnh gần luôn phía người xem, thứ tự lớp không phụ thuộc dấu scale.x.
- **Run:** thân nghiêng 6–8° về hướng chạy, đầu bù −1/2 góc thân; hông nhún −2/0/+2 px quanh y=−42 theo bước. Góc chân được ghi trong từng frame để chân trụ ở y=0, chân vung nhấc khỏi đất. Không dùng việc dời toàn rig để giả nhún làm chân xuyên đất.
- **Slash 1/2/3:** thân đánh qua hai phía 8–12°, hông dịch 2–3 px theo nhịp; góc chân bù giữ hai điểm đặt chân trên đường đất. Nhịp/frame/hit/cancel không đổi.
- **Jump_up:** khung đầu gập cả hai gối, thân chúi 8°, đầu bù −4°; không đổi quỹ đạo A0. **Land:** một khung gập gối, thân chúi, rồi đứng lên; hai bàn chân tiếp đất ở cả hai khung.
- **Idle:** hông thở ±1 px quanh y=−46, chân gập/duỗi bù để điểm đặt chân cố định. Chiều cao mảnh/khớp không đổi; 96 px là chiều cao duỗi, không ép mọi pose gập gối cao đủ 96 px.
- Tất cả góc, dịch hông và vị trí bù ở JSON; không thêm chuyển động vật lý hay thay mã A0. Các góc chân được giải khi tác giả pose theo hai đoạn dài 22 px, lưu kết quả vào dữ liệu; runtime không chạy IK. Khớp cha vẫn nối đúng attach.

### Kiểm tra bổ sung hai hướng

```sh
godot --headless --path prototype --script res://rig/tests/visual_checks.gd
python prototype/rig/tests/check_contact_sheets.py
```

`visual_checks.gd` kiểm mọi pose ở scale.x=±1: lớp gần luôn trên xa, khớp không tách,
chân idle/land/slash tiếp đất, chân chạy trụ/vung không xuyên đất; mọi khung bắn có
cung dọc tại tay xa, tay xa ngang vai, dây nối tới tay kéo. Script PIL raster scene
geometry theo z để đếm pixel tay xa còn lộ ở cả năm khung/cả hai hướng (mỗi mảnh
tay trên/tay dưới/bàn tay ít nhất 5 pixel); so tọa độ tờ trái với scene lật thật và
kiểm kích thước PNG. Không chỉ đổi dấu tọa độ trong Python để tạo bản trái.

Đã xuất lại shoot/run/slash_1–3/jump_up/land/idle và thêm run_left/shoot_left;
các tờ còn lại cũng được tạo lại từ cùng scene. Chạy lại ba lệnh headless README,
rig smoke và các kiểm tra bổ sung bằng **Godot 4.7.2.stable.official.ed1daf0bf**;
đầu ra nguyên văn nằm trong commit sửa này. Chỉ sửa `prototype/rig/` và tài liệu
này; nhật ký lần chỉnh được ghi tại đây theo phạm vi người dùng, không sửa 05_log.
Rig/pose vẫn **Đề xuất — chưa duyệt**, chưa thử Android mới.

## 7. Bộ phận vẽ bậc 0 — bản ép ô cũ đã bị thay

Mục này lưu cách làm lượt đầu đã bị loại về tỉ lệ; dùng **mục 8** và báo cáo mới cho hiện trạng.

Trong cảnh rig, ⚙ có **Bộ phận vẽ / Khối màu (bật = vẽ)**, mặc định bật.
Mỗi mảnh dùng Sprite2D nearest, texture bản sao đúng byte từ
`art/sprites/characters/chr_dbl_parts/`, giữ size/pivot/attach/layer đã có.
Không đổi pose JSON, hitbox hay điều khiển. Tắt để trở lại các khối màu.

Các khung cố định/pivot sát mép không chứa trọn đầu tròn ở một số góc gập.
Ngoài phần vẽ bù bán nguyệt trong PNG, script sinh metadata màu/vùng đầu tròn
`prototype/rig/art_parts/joint_fill.json`; scene vẽ lớp bù tự động dưới ảnh tại
cổ, vai, khuỷu, hông và gối (hai nửa bán nguyệt, cùng màu vùng gần khớp).
Lớp bù có thể vượt mép khung ảnh một ít để không hở khi xoay, không thêm bone hay
thay kích thước PNG/collision. Không thêm lớp bù tròn ở bàn chân/tay/vũ khí để
tránh biến chân đất/tay cầm thành khối tròn lớn. Phần này là vẽ bù bằng script,
chưa duyệt thẩm mỹ; không giả là họa sĩ đã vẽ phần giải phẫu bị che.

Ảnh concept, bước xử lý, hai ma trận đầu 24×18, kiểm PNG/khớp và script nguyên
văn tại `reports/g1_parts_art_report.md`. Contact sheet texture ở
`prototype/rig/contact_sheets/art/`; idle ×4 chỉ phóng NEAREST từ file 1× thật.
Claude/người dùng còn phải soát khuôn mặt và mọi bộ phận, chưa thử Android mới.

## 8. Co art theo một hệ số chung (thay cách ép ô ở mục 7)

Bản art trước bị méo vì mỗi mảnh co độc lập vào ô greybox. Lượt này dùng lại tờ
concept, không sinh ảnh mới. Giữ nguyên cấu hình gốc thành `parts_greybox.json`
và pose tương ứng `animations_greybox.json`. Công tắc art/khối màu dựng lại
đúng bộ khớp/pose riêng cho từng chế độ, không chỉ nhét ảnh art vào khung cũ.

Các mốc nguồn được chọn bằng mắt trên crop thật và ghi trong
`tools/cut_parts.py`/`uniform_measurements.json`, không giả là nhận dạng tự động.
Đường ghép thử theo hướng dẫn đầu/thân/chân 24/24/48: đầu tới cổ 218 px, cổ tới
điểm ghép quần dưới vạt áo 214 px, hông→gối 176 px, gối→cổ chân 152 px,
cổ chân→gót/đế 86 px. Tổng **846 px**, nên **s=96/846=0,113475177305** cho cả
x/y của mọi mảnh. Sau co các đoạn là **24,738 / 24,284 / 46,979 px**, không ép
từng đoạn đúng 24/24/48. Mốc ghép quần dưới vạt áo là điểm rig tạm, cần duyệt
chứ không khẳng định là mốc giải phẫu chính xác. Lấy trung vị theo ô có bước
1/s ở cả hai trục; ceil chỉ thêm ô cuối, không đổi tỉ lệ theo kích thước ảnh đích.

### Bảng greybox cũ → art đo lại

Mọi tọa độ px, attach trong hệ khớp cha; số bảng làm tròn 3 chữ số, JSON giữ
độ chính xác. Nhịp 13 động tác/48 frame và marker không đổi; pose art retarget
theo chiều dài mảnh mới để giữ chân tiếp đất, không đổi physics A0.

| Mảnh | Khung cũ → mới | Pivot cũ → mới | Attach cũ → mới |
|---|---|---|---|
| `head` | 18×24 → 23×25 | (9, 24) → (9.418, 24.738) | (0, -24) → (0, -24.284) |
| `body` | 20×26 → 17×29 | (10, 24) → (7.376, 26.099) | (0, -48) → (0, -46.979) |
| `upper_arm_near` | 8×19 → 10×26 | (4, 2) → (4.766, 1.362) | (0, -21) → (0.34, -20.993) |
| `upper_arm_far` | 8×19 → 10×26 | (4, 2) → (4.652, 1.362) | (0, -21) → (0.34, -20.993) |
| `forearm_near` | 7×17 → 8×19 | (3, 2) → (3.404, 1.135) | (0, 15) → (0.34, 22.922) |
| `forearm_far` | 7×17 → 7×19 | (3, 2) → (3.291, 1.135) | (0, 15) → (0.227, 22.922) |
| `hand_near` | 7×8 → 10×13 | (3, 2) → (2.95, 1.021) | (0, 13) → (0.113, 16.227) |
| `hand_far` | 7×8 → 10×14 | (3, 2) → (2.837, 1.021) | (0, 13) → (0.113, 15.887) |
| `thigh_near` | 10×24 → 15×24 | (5, 2) → (7.376, 1.362) | (2, 0) → (1.5, 0) |
| `thigh_far` | 10×24 → 15×24 | (5, 2) → (7.262, 1.362) | (-2, 0) → (-1.5, 0) |
| `shin_near` | 8×24 → 9×22 | (4, 2) → (4.085, 1.362) | (0, 22) → (-0.113, 19.972) |
| `shin_far` | 8×24 → 9×21 | (4, 2) → (3.972, 1.362) | (0, 22) → (-0.113, 19.972) |
| `foot_near` | 14×6 → 19×12 | (4, 2) → (4.993, 2.156) | (0, 22) → (-0.113, 17.248) |
| `foot_far` | 14×6 → 18×12 | (4, 2) → (4.879, 2.156) | (0, 22) → (-0.113, 17.248) |
| `dao` | 5×34 → 8×41 | (2, 28) → (3.518, 32.908) | (0, 4) → (1.816, 6.355) |
| `bow` | 6×38 → 10×41 | (3, 19) → (1.589, 20.879) | (0, 0) → (1.816, 6.355) |

Giới hạn cổ chân art đề xuất ±75° để giữ đế chân ngang với đoạn chân đã đo
(lớn nhất đang dùng khoảng 71,54°); greybox vẫn ±60°. Cổ tay giữ giới hạn cũ.
Góc pose/IK được tác giả script tính trước và ghi JSON; không sửa player A0.

- Viền chỉ được bôi ở đường bao dáng đứng xuất từ scene. Mặt cắt cổ/vai/khuỷu/
  cổ tay/hông/gối/cổ chân và phần bù tự động không có viền. Script xóa nét viền
  do chính nó bôi nếu nét đó lọt vào trong ở cả dáng idle lẫn đứng duỗi.
- Nét tối tóc được phân loại vào màu vật liệu; vùng mắt/mũi/miệng giữ màu lấy
  mẫu từ concept. **Không đọc/áp dụng tools/chr_dbl_head_edits.json, không sửa
  feature pixel**. Ma trận mới là **23 cột × 25 dòng** sau co, kèm bảng màu ở
  `reports/g1_parts_art_report.md`; chờ Claude gửi ma trận đã sửa.
- Cắt cổ dưới cằm còn khoảng 2,50 px; da mặt chiếm 13/23≈56,52% bề rộng ô đầu.
- Tay/chân giữ 3 sắc da sáng/trung/tối. Chân giữ tỉ lệ nguồn để thấy gót/mũi chân,
  không thêm đĩa bù ở bàn chân. Lớp bù khớp vẫn chỉ là màu vật liệu, không có viền.
- Dáng đứng duỗi từ scene cao đúng 96 px. Idle thở/gập gối thấp hơn một pixel,
  không kéo giãn mảnh cho mọi pose đều cao 96.
- Báo cáo hiện liệt kê 8 pixel màu outline nội bộ, tất cả ở đầu/mặt lấy từ nguồn;
  không còn pixel viền nội bộ ở các mối nối. Giữ chúng để Claude soát, không
  tự sửa mắt/mũi/miệng chỉ để ép số đo thành 0.

Pipeline/lệnh tái tạo, ma trận và đầu ra tại
`reports/g1_parts_art_report.md`; số 17 dành cho `17_ngoai_hinh.md`. Mọi art/khớp
mới vẫn Đề xuất/đang làm, chưa duyệt.

## 9. Đầu Claude và tay rút ngắn theo duyệt mới

Theo ma trận người dùng gửi: **đầu do Claude vẽ tay từng pixel**. PNG đầu giữ
23×25, pivot/attach không đổi; so RGBA từng pixel với ma trận đầu vào. Không
thực hiện làm sạch/bôi viền hoặc sửa feature trên đầu. Cổ được kiểm không hở
ở cả 48 frame. H là màu tóc, O là nét; L=#59443E là ngoại lệ ánh tóc, không phải
cho phép dùng nhóm pants trên da hay áo.

Ngoại lệ do người dùng cho phép: upper_arm/forearm rút trục dài còn 60%, giữ
chiều ngang; các phần khác vẫn giữ s chung. Đầu ngón đo từ scene ở y=−33 khi
đứng duỗi, y=−32 ở idle, cả hai tay, trong khoảng −30…−34.

| Mảnh | Khung cũ → mới | Pivot cũ → mới | Attach cũ → mới |
|---|---|---|---|
| `upper_arm_near` | (10, 26) → (10, 16) | (4.766, 1.362) → (4.766, 0.817) | (0.34, -20.993) → (0.34, -20.993) |
| `forearm_near` | (8, 19) → (8, 12) | (3.404, 1.135) → (3.404, 0.681) | (0.34, 22.922) → (0.34, 13.753) |
| `hand_near` | (10, 13) → (10, 13) | (2.95, 1.021) → (2.95, 1.021) | (0.113, 16.227) → (0.113, 9.736) |
| `upper_arm_far` | (10, 26) → (10, 16) | (4.652, 1.362) → (4.652, 0.817) | (0.34, -20.993) → (0.34, -20.993) |
| `forearm_far` | (7, 19) → (7, 12) | (3.291, 1.135) → (3.291, 0.681) | (0.227, 22.922) → (0.227, 13.753) |
| `hand_far` | (10, 14) → (10, 14) | (2.837, 1.021) → (2.837, 1.021) | (0.113, 15.887) → (0.113, 9.532) |

Màu áo: #C3A98A chủ đạo, bóng #89745E/#554638, #EAD8B8 ≤15% số pixel vải.
Các nhóm chất liệu kiểm riêng cho từng PNG, ngoài quần không dùng pants trừ L
trên tóc Claude. Tỉ lệ từng màu và ma trận nguyên văn ở
`reports/g1_parts_art_report.md`. Các mục 7–8 là lịch sử trước lần chỉnh này.

## Lớp ngoại hình bổ sung — đề xuất, chưa sửa prototype

| Mảnh | Khung đề xuất | Pivot | Cha/attach | Lớp |
|---|---|---|---|---|
| cape | 32×56 px | (16,4) | body, khớp vai đo theo part_set | Sau thân, trên nền; tránh che tay xa |
| face_overlay | 18×18 px | (7,8) | head, neo tâm mặt theo mẫu đầu | Trên đầu/tóc, dưới số sát thương |

Kích thước và điểm gắn cuối phải thử với đầu/tay mới, chưa duyệt. Không thay parts.json trong lượt docs. Theo 17_ngoai_hinh.md.


## Chỉnh bộ phận 29/10/2026 — chưa duyệt

Vũ khí art cho phép limestone: lưỡi đao #A5B8B0, bóng #718B87, sáng #D9DDD0,
viền #17151A; cán/vỏ belt. Cung gỗ belt, dây sáng #D9DDD0. Hai đùi chỉ pants
và nét outline; da bắt đầu từ gối/cẳng chân. Kích thước/pivot/attach giữ nguyên.

Run/slash_1–3 giảm 35% góc gập gối ở cả hai chân. Giải lại hông và góc chân từ
độ dài xương: hông nâng tương ứng, chân trụ khi chạy và cả hai chân khi chém
không đổi điểm đặt. Chân vung chỉnh theo độ duỗi mới, không xuyên đất.
Giữ dữ liệu greybox để so sánh; chỉ thay `animations.json` của bản art.
Kết quả scene thật và nguyên văn script ở [báo cáo polish](reports/g1_parts_polish_report.md).


### Sửa hướng đao 29/10/2026 — chưa duyệt

Trục lưỡi PNG hướng −Y, nên phải xoay 180° quanh pivot cầm, có bù góc bàn tay.
Ở mọi pose thường, chuôi→mũi cùng hướng khuỷu→cổ tay, góc đo khoảng 6,801°.
Idle/turn chúc mũi xuống và ra trước (trục 60° ở hệ rig nhìn phải). Giữ pivot,
attach và hitbox; không dùng góc 0 cũ khiến lưỡi nằm dọc cẳng tay về phía khuỷu.
Cung gắn nắm tay xa; trục hai đầu cánh cung lúc bắn lệch vuông góc 0,490°.
59 pose đã kiểm (13 động tác và run/shoot trái), không mũi đao nào nằm giữa khuỷu
và cổ tay. [Báo cáo, ảnh và script](reports/g1_weapon_direction_report.md).
