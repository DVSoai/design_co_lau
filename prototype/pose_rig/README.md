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
