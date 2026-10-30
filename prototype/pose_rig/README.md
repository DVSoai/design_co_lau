# Bộ tư thế vẽ trọn — pilot chưa duyệt

Godot **4.7.2 Standard/GDScript**, bản thử riêng; không thay nhân vật A0/Đào Úc.
Từ root repo:

```sh
godot --path prototype res://pose_rig/pose_rig.tscn
```

Hoặc mở dự án `prototype/`, chạy A0 rồi bấm **Nhân vật tư thế (thử)**.
Chọn idle/run/jump/fall/slash, đổi hướng, ẩn/hiện đao, hoặc Về A0.

4 lớp có tranh nguyên tư thế; PNG2×, Sprite2D scale0,5 cố định/filterlinear,
rotation0; actor root chỉ lật±1. `data/frames.json` chọn hình/thời lượng,
`data/anchors.json` lưu mốc cổ/hông/đế/chuôi theo pixel texture2×.
Đổi đồ cần bộ hình đầy đủ theo tư thế; chưa triển khai hệ thống đồ ở đây.

```sh
python3 tools/cut_pose_sheets.py
python3 tools/check_pose_sheets.py
godot --headless --path prototype --editor --import --quit
godot --headless --fixed-fps 60 --path prototype --script res://tests/pose_rig_checks.gd
```

Các lệnh trên chạy từ root. File sinh runtime nằm trong `pose_rig/art/`;
script kiểm chúng giống byte với PNG art nguồn. Nguồn AI đầu/vũ khí cần đăng ký
đồng dạng toàn tờ trước khi co chung; cả hai hệ số được ghi trong anchors.json,
không tuyên bố các sheet nguyên bản đã đồng tỉ lệ.

Chụp thật trên Linux có Xvfb (`xvfb-run` là tiện ích nếu máy đã cài):

```sh
xvfb-run -a -s '-screen 0 1600x720x24' godot --audio-driver Dummy --path prototype --windowed --resolution 1600x720 res://pose_rig/pose_rig.tscn -- --capture-poses
xvfb-run -a -s '-screen 0 1600x720x24' godot --audio-driver Dummy --path prototype --windowed --resolution 1600x720 res://pose_rig/pose_rig.tscn -- --capture-poses --left
python3 tools/compare_pose_captures.py
```

Lượt này dùng Xvfb21.1.16 giải nén trong `/tmp/pose-xvfb/`, Mesa llvmpipe,
Godot4.7.2; ảnh viewport thực1600×720 từng hướng lưu `reports/scene_*.png`.
Ảnh ghép chỉ nối hai ảnh viewport, không sửa hình trong ảnh.

Bàn dựng Blender2D (4 plane có texture đóng gói, chưa có mô hình3D):

```sh
blender --background --factory-startup --python tools/blender_pose_preview.py
```

[Báo cáo](../../docs/reports/g1_pose_sheets_report.md),
[nguyên đầu ra](../../docs/reports/g1_pose_sheets_checks.txt).
