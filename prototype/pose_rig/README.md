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
xvfb-run -a -s '-screen 0 1600x720x24' godot --audio-driver Dummy --path prototype --windowed --resolution 1600x720 res://pose_rig/pose_rig.tscn -- --capture-weapons
xvfb-run -a -s '-screen 0 1600x720x24' godot --audio-driver Dummy --path prototype --windowed --resolution 1600x720 res://pose_rig/pose_rig.tscn -- --capture-weapons --left
python3 tools/compare_pose_captures.py
```

[Báo cáo](../../docs/reports/g1_kiem_cung_report.md),
[đầu ra thật](../../docs/reports/g1_kiem_cung_checks.txt).
Các báo cáo cũ giữ nguyên là lịch sử; hình hiện hành dùngkiem_*/cung_*.
