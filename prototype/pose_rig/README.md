## Bản sửa chạy / cầm / trên không / vệt —31/10/2026, chưa duyệt

Bảng hiện hành: đứng0–1, chạy2–7 (lên dùng7), cuộn tròn8–11 trong vòng gió
riêng, rơi12, đánh13–29;13là thủ kiếm. Không dùng12cho lên hoặc13/22cho rơi.
Nhịp A0vẫn0,38s lên đỉnh,0,20s/vòng. Sáu chân chạy được vẽ lại riêng, thân giữ
thẳng; grip kiếm nằm trong nắm tay và có lớp ngón tay phủ chuôi; cung40° cầm thấp
ra trước, trục dây không cắt phần thân giữa.

Vệt16sinh nhịp2 và tiếp tục qua nhịp3; vệt39sinh thêm ở nhịp3. Hình vệt tự vẽ,
neo tâm theo raw số nguồn, lớp vẽ trên người. Lõi vệt lia đủ đậm và đủ diện tích,
Trảm Kiếm xanh/dày hơn, nhịp giữ tan. Lưỡi dài cũ giữ nguyên PNG. Các khung tĩnh
cũng dựng đủ hiệu ứng từ nhịp trước. Ô chiêu84×84logic, tên hai dòng.

```sh
python3 tools/update_pose_playtest.py
godot --headless --path prototype --editor --import --quit
python3 tools/check_all_godot.py --out prototype/pose_rig/reports/motion_godot_checks.txt
python3 tools/check_motion_art.py
python3 tools/capture_motion_review.py
```

Lệnh chụp cần Xvfb/Mesa; tạo16ảnh Godot thật1600×720, đủ hai phái/hướng,
viewer và đòn thường/chiêu trong màn chơi thử. `frame_placement_proof.gd` in nguyên
số tham khảo và vị trí sprite đã đặt. Bằng chứng ls/dòng Java/renderer ở commit
message, không đưa mã hoặc ảnh tham khảo vào repo. Các phần dưới là lịch sử.

---

## Chạy thử nhân vật mới — 31/10/2026

Từ root repo: `godot --path prototype res://pose_rig/play_test.tscn`, hoặc bấm
**Thử nhân vật mới** trên màn A0. A/D/←/→ di chuyển; Space/W/↑ nhảy;
J/X đánh; Tab đổi Kiếm/Cung; 1 Trảm Kiếm, 2 Xạ Tiễn. Cảm ứng dùng d-pad A0,
ĐÁNH, PHÁI và hai ô chiêu. Chiêu của phái còn lại không kích hoạt. Có nền phẳng,
ba bục và hình nộm hiện số sát thương. Scene/controller/nhân vật A0 cũ giữ nguyên.

Bản hiện hành thay các mô tả lưỡi ngắn/5 nhịp bên dưới: lưỡi đánh thật
0,782H (không tính cán), vệt nối mũi. Kiếm6 nhịp theo bảng nguồn, Cung8 đất/7 không;
nhịp .05s, hit và controller lấy nguyên `prototype/config`. Đầu/cổ và hông ghép
bằng điểm đo trên tranh tự vẽ; mọi Sprite2D rotation0, chỉ gốc lật.

`tools/update_pose_playtest.py` đọc trực tiếp `docs/ref/so_lieu_tham_khao.json`:
30 dòng nguồn, lựa chọn hình qua bản đồ slot tranh tự vẽ, công thức vị trí, các độ lệch
hình/hiệu ứng, frame và sự kiện bắn của chiêu1/28. `registrations` ghi rõ hiệu chỉnh
crop/khớp cổ-hông theo từng phái/khung; không sửa số liệu nguồn. Đạn giữ tọa độ
nguồn và hiệu chỉnh về dây thật để không xuất hiện rời cung. Các khác biệt tỉ lệ,
neo và thời gian được ghi ở cuối `docs/05_log.md`, mục31/10/2026.

Kiểm tra từ root sau import:

```sh
godot --headless --path prototype --editor --import --quit
python3 tools/check_all_godot.py
python3 tools/check_lv1_sizes.py
python3 tools/check_lv1_30.py
python3 tools/check_arrow_alignment.py
python3 tools/capture_lv1_30.py --pages frames attacks
```

`playtest_godot_checks.txt` trong reports chứa nguyên output các suite độc lập;
classic_checks chạy qua wrapper hiện có. Chụp viewer bằng Xvfb1600×720, cả2phái/2hướng.
`reports/play_*` là ảnh scene chơi thử thật. Chưa thử đa chạm trên Android, chưa xuất APK.

---

## Bản hiện tại —30/10/2026, chưa duyệt mỹ thuật

Theo `docs/18_luong_tham_khao.md` mục 4: ngoại hình hàng Tổng thể Lv1, không nón,
áo giao lĩnh nâu dài, giày, dải tóc đỏ; đầu/tóc 0,40H ±0,03. Hiển thị 128 px trên
1600×720. Dữ liệu `parts.presentation` đo lại alpha người thật để tính hệ số xem.
Kiếm cầm đo cạnh dài nhất hộp alpha: 0,75–0,80H; cung 0,90–1,00H; tên 0,55–0,65H.
Tên được căn bằng pixel thân tên thật qua dây và điểm tựa cung; lúc thả sinh tại dây.
Kiếm đánh 5 nhịp thủ/kéo/lia/giữ/thu, 0,30 s; hit 0,10–0,20 s. Ẩn kiếm cầm,
thay bằng hình vung có lưỡi ngắn + vệt cong sát áo, toàn bộ vệt ≤1,3H.
Cung 8 nhịp, thả nhịp 5; tổng 0,40 s vẫn là đề xuất xem thử.
Chỉ có Lv1; hai phái không mang chung kiếm/cung. Các mục dưới là lịch sử, số cũ
không thay các quy định hiện tại ở đây.

```sh
python3 tools/check_lv1_30.py
python3 tools/check_lv1_sizes.py
python3 tools/check_arrow_alignment.py
python3 tools/audit_lv1_redraw.py --base 3371ab3
godot --headless --fixed-fps 60 --path prototype --script res://tests/compact_anatomy_checks.gd
godot --headless --fixed-fps 60 --path prototype --script res://tests/arrow_alignment_checks.gd
```

Dựng ảnh so bằng scene thật (cần display/Xvfb):

```sh
godot --path prototype res://pose_rig/review_capture.tscn -- --out /tmp/ref_render/own
python3 tools/compare_ref_lv1.py --out /tmp/ref_render/comparisons
```

Chạy trình dựng tham khảo theo docs/18 trước khi so. Ảnh so ba cột và tài nguyên
tham khảo chỉ lưu `/tmp`, tuyệt đối không commit. Ảnh viewer của dự án ở `reports/`; cột bảng mẫu và nhân vật mới đều cao 128 px.
Báo cáo kiểm tra hiện tại: `reports/lv1_compact40_checks.txt`.

## Sửa đúng dáng Kiếm và cách cầm —30/10/2026, chưa duyệt

Kiếm6nhịp lia ngang: thủ/kéo/lia/giữ/giữ/về thủ,0,30s, hit0,10–0,20s.
Vệt trắng ngang dài, mép tơi và đuôi giảm alpha; hai lớp lia ra/kéo dài nối tiếp.
Trảm Kiếm cùng dáng với vệt xanh dài/dày hơn. 4thân mới thay ô cũ; chân choãi bổ sung
riêng, không đổi bộ10chân di chuyển. Cung8nhịp, thả ởnhịp5/t=0,20s; tổng0,40s là
đề xuất cho preview, không lấy làm số game thật đã chốt.
Ngoài đánh: kiếm chúc xuống sau (chạy gần ngang hơn); cung chéo trước thân, đều tay
trước. Lộn/đánh ẩn hình cầm tay. Cỡ hiển thị vẫn128px, A0 không đổi.

Kiểm thêm:

```sh
python3 tools/check_lv1_sizes.py
godot --headless --fixed-fps 60 --path prototype --script res://tests/horizontal_weapon_checks.gd
```

Báo cáo lượt mới: `reports/lv1_horizontal_checks.txt`. Các mục pilot bên dưới là lịch sử.

## Sửa cỡ hiển thị và hình vung —30/10/2026, chưa duyệt

Nhân vật96px logic A0 hiển thị **128px** ở1600×720. Viewer minh họa hệ số720/540; đo RGBA idle96,204px nên
hiệu chỉnh128/96,204 để ảnh duyệt cao128px. Không đổi tuning A0 hay hình người.
Trang30khung dùng thumbnail tự co vừa ô (6cột×5hàng) để không chồng; xem cỡ thật128px
ở trang đòn/chiêu và so cạnh bảng. Thumbnail không phải thước đo cỡ trong game.

Kiếm cầm tay0,75–0,8H; cung0,35–0,4H; tên0,55–0,65H. H=96logic.
Mỗi nhịp một ảnh vung ghép **kiếm+vệt liền mũi**, neo tâm và hiệu chỉnh grip về tay;
nhịp giơ không vệt. Bốn mặt quét khác hình học, không dời một lưỡi liềm chung.
Trảm Kiếm dùng bản ghép xanh tương ứng. Mask/kiếm rời chỉ là đầu vào kiểm tra offline,
runtime mỗi nhịp chỉ nạp1PNG ghép. Kiểm bằng `python3 tools/check_lv1_sizes.py`.
Ảnh so nhân vật tham khảo cùng128px chỉ ở `/tmp/lv1-size-followup/`, không commit.

# Lv1 / 30 khung — bước 1/5, chưa duyệt (30/10/2026)

Mở `res://pose_rig/pose_rig.tscn` bằng **Godot 4.7.2 Standard**. Chọn Kiếm/Cung,
động tác/chiêu, Trên không, Chạy lại, Đổi hướng; các trang 30 khung, Các đòn/chiêu,
So cạnh bảng. Mỗi nhân vật chỉ mang vũ khí của phái đó. Chỉ Lv1 là bộ mới;
Lv10–60 chưa làm, các pilot cũ bên dưới không phải bộ đã hoàn thành.

Nguồn chuẩn mới: `data/frames30.json`, `parts.json`, `effects.json`, `skills.json`.
Đầu8/thân18/chân10 dùng chung; ảnh nguồn2×, lọc linear; dời/lật, mọi Sprite2Drotation0.
Lộn8–11 là các hình góc đã vẽ/bake trước; hoàn tất .20s rồi trở về hình rơi thẳng.
Đòn chém5nhịp .30s, hit .10–.20; nhịp đất và trên không tách riêng. Chiêu chỉ xem hình,
không triển khai luật chiến đấu, không thay số A0. Vệt trắng dùng chung, Trảm Kiếm dùng
hiệu ứng xanh theo bảng; Xạ Tiễn dùng đạn xanh. Vũ khí cầm tay ẩn trong nhịp đánh.

Nguồn imagegen và prompt nguyên văn: `art/sprites/characters/lv1_30/sources/`;
6 lần sinh (tờ thân đánh đầu tiên bị dính đầu, giữ `bodies_b_rejected.*`). Mỗi lần đều
đính kèm hai bảng + ref, lần sửa thân thêm tờ thân đúng. Không cắt ảnh mẫu vào sprite.
`reports/reference_lv1.png` là ô đối chiếu cắt từ bảng trang bị (100,348,151,421),
**chỉ viewer so sánh nạp**, không nằm trong dữ liệu nhân vật hay bộ hình game.

Sinh/kiểm tra từ root repo:

```sh
python3 tools/build_lv1_30.py
python3 tools/check_lv1_30.py
godot --headless --path prototype --editor --import --quit
godot --headless --fixed-fps 60 --path prototype --script res://tests/frames30_checks.gd
python3 tools/capture_lv1_30.py --godot godot --xvfb Xvfb
```

Lệnh chụp dùng Xvfb1600×720 và Godot thật, in từng lệnh con; tạo12ảnh trong
`reports/lv1_{kiem,cung}_{frames,attacks,compare}_{right,left}.png`. Không imagegen cho
ảnh báo cáo. `reports/lv1_checks.txt` lưu đầu ra thật; commit message lưu cả kiểm tên.
Giữ bộ thử cũ trong `legacy_pose_actor.gd` / `legacy_frames.tscn`; hai test hồi quy cũ
chỉ đổi đường dẫn scene sang fixture này, giữ mọi assert. `frames30_checks.gd` kiểm
hệ mới trực tiếp, không dùng fixture cũ để tuyên bố bộ mới đạt.

Không có tài nguyên bên thứ ba mới. Mã/hình tham khảo chỉ đọc cơ chế chọn lớp,
neo, hiệu ứng đặt theo tâm và đạn độc lập; dữ liệu và PNG ở đây được tự tạo.

---

# Kiếm/Cung — pilot tư thế vẽ trọn, chưa duyệt

Godot4.7.2, scene riêng; không thay A0 hoặc Đào Úc.
Từ repo root: `godot --path prototype res://pose_rig/pose_rig.tscn`.
Hoặc chạy A0, bấm **Nhân vật tư thế (thử)**. Chọn phái Kiếm/Cung, động tác,
đổi hướng, ẩn/hiện vũ khí, VềA0. Khung ảnh bên dưới là các pha để duyệt.

Kiếm idle/run/jump/fall đeo sau lưng; slash4hình vung/0,30s; thrust2hình/0,10s
(Đề xuất pilot). Cung dùng shoot3pha, run_shoot2pha; tên là hình riêng sinh ở
pha thả. Các pha giữ tổng thời gian/mốc spawn của09, xem báo cáo.

4 lớp Sprite2Dảnh2×, scale0,5/linear cố định, rotation0; gốc chỉ lật±1.
Chân y0, cổ/hông ghép theo mốc; kiếm theo tay gần, cung theo tay xa.
`data/frames.json` là hình/thời lượng; `data/anchors.json` là mốc2× sau cắt;
`data/source_regions.json` là vùng liền khối/mốc đã chọn bằng mắt ở ảnh nguồn.
Arrow_speed240logicpx/s là Đề xuất chỉ cho xem thử, không đổi tuningA0.

```sh
python3 tools/cut_pose_sheets.py
python3 tools/check_pose_sheets.py
godot --headless --path prototype --editor --import --quit
godot --headless --fixed-fps 60 --path prototype --script res://tests/pose_rig_checks.gd
godot --headless --fixed-fps 60 --path prototype --script res://tests/weapon_direction_checks.gd
```

Chụp Linux có Xvfb (từ root):

```sh
xvfb-run -a -s '-screen 0 1600x720x24' godot --audio-driver Dummy --path prototype --windowed --resolution 1600x720 res://pose_rig/pose_rig.tscn -- --capture-swing
xvfb-run -a -s '-screen 0 1600x720x24' godot --audio-driver Dummy --path prototype --windowed --resolution 1600x720 res://pose_rig/pose_rig.tscn -- --capture-swing --left
python3 tools/compare_pose_captures.py
```

[Báo cáo](../../docs/reports/g1_kiem_cung_report.md),
[đầu ra thật](../../docs/reports/g1_kiem_cung_checks.txt).
Các báo cáo cũ giữ nguyên là lịch sử; hình hiện hành dùngkiem_*/cung_*.

## Lưỡi theo cấp và vệt chung — chưa duyệt

Mỗi nhân vật chỉ Kiếm HOẶC Cung. Chọn Cung thì dropdowncấpKiếm bị khóa;
đổi phái xóa ngay hình/vệt/tên cũ. Các mẫu đứng cạnh nhau là mẫu so riêng.
Chọn cấp1/30/60, bấm **Chạy slash —0,30s thật**; dải tĩnh3hàng×5nhịp luôn
hiện để so. Viewer dùng canvasxem1600×720riêng, vềA0khôi phục kích thước trước.

Nguồn chuẩn `data/swing.json`:15lưỡi đã vẽ/5IDgóc,4vệt dùngchung, mốcgrip,
phasebody/thời lượng/tâmvệt.10/20/40/50làslotchưa vẽ, không cóspritegiả.
PNG2×canvas256×256, grip(96,144); trục≤3°/chiều lưỡi≤15%, chỉ xoayOFFLINEkhi
xuấtPNG. Runtime Sprite2Drotation0, chỉ rootlật±1; tấn công ẩn kiếm cầm, gắn
lưỡi vào tay và đặt vệt theo tâm. Nhịp5giữ followthrough; tổngslash0,30s.
Thrust giữ2khung/thời gian cũ. Tranh/mốc người không đổi khi thay cấp.

Cung có tên đặt trên dây ởshoot2/run_shoot1; pha thả ẩn tên này và sinh
Sprite2Dtên bay riêng. Chỉ kéo dài thân gỗOFFLINE, cùng ảnh cho tên sẵn/tên bay.
Không đổi speed/spawn của pilotcũ hoặc tuningA0.

```sh
python3 tools/build_weapon_template.py
python3 tools/check_weapon_template.py
godot --headless --path prototype --editor --import --quit
godot --headless --fixed-fps 60 --path prototype --script res://tests/weapon_direction_checks.gd
xvfb-run -a -s '-screen 0 1600x720x24' godot --audio-driver Dummy --path prototype --windowed --resolution 1600x720 res://pose_rig/pose_rig.tscn -- --capture-swing
xvfb-run -a -s '-screen 0 1600x720x24' godot --audio-driver Dummy --path prototype --windowed --resolution 1600x720 res://pose_rig/pose_rig.tscn -- --capture-swing --left
```

Các lệnh từ rootrepo, Godot4.7.2. Ảnh thật `reports/swing_right.png` và
`swing_left.png`; nguyên đầu ra kiểm `reports/swing_checks.txt` và commit message.
Lệnhgrepnguyênvăn còn khớp có sẵn trênmain/chuỗi con giấyphép/nhịphân; người
dùng chọn giữ nguyênđầura trongcommit và báo **chưa đạt0dòng**, không sửa giấyphép.

Tham khảo cơ chế thể loại chỉ đọc: frame chọn hình/độ lệch, vệt theo tâm ảnh,
lật bằnggốc và đảo trụcngang, ẩn hình cầm trong nhịp đánh; tên trên dây tách
với tên bay ở pha thả. Không đưa source, mã, hình, bảng số hoặc tên nguồn vào
thay đổi mới. Canvas/góc/offset/thời gian/ảnh là của CờLau.
Nguồn tự tạo `art/sprites/weapons/swing/sources/straight_tiers.png`, promptnguyên
văn cạnhảnh và log05; chuẩn hóa/xuất riêng bằng script. Không thêm tài nguyên
bên thứba nên không có mụcgiấyphéptài nguyên mới để ghi. Các ảnh vẫn chưa duyệt.
