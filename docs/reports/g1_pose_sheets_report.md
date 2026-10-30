# G1 — Pilot bộ tư thế vẽ trọn (30/10/2026)

**Bản thử, chưa duyệt.** Quyết định29/10, nhánhfeat/g1-pose-sheets-pilot từ
main8bd5876. Không lấy v3 hoặc các nhánh thử khác. Chỉ xem riêng trong prototype.

## Nguồn và giới hạn

4 tờ imagegen đính kèm ảnh gốc, STYLE-B vẽ tay + AVOID; mỗi tờ1lần, không có
lần sinh bị loại. 12thân/10chân/3đầu/6đao; prompt nguyên văn cạnh PNG và03_prompts.
Không dùng imagegen cho ảnh kết quả. Các tư thế đang chờ người dùng soát bằng mắt.

Tờ chân có thừa dải áo phía trên: cắt theo hàng hông đã ghi. Đầu/vũ khí nguồn
AI lớn hơn tờ thân/chân, không thể tuyên bố cùng scale trực tiếp từ PNG gốc.
Đăng ký ĐỒNG DẠNG TOÀN TỜ đầu/vũ khí trước, rồi xuất một hệ số chung;
không co x/y khác nhau, không nắn từng pose. Nếu yêu cầu tuyệt đối một hệ số
trực tiếp từ mọi PNG nguyên bản, nguồn hiện tại **chưa đáp ứng điều đó**.

Hệ số xuất sau đăng ký: `0.343470483005`; hệ số đăng ký toàn tờ: `{'body': 1.0, 'legs': 1.0, 'head': 0.30952380952380953, 'dao': 0.43}`. Hệ số thực/kích thước/mốc từng hình ở anchors.json và đầu ra script.

Các mốc nguồn được chọn bằng mắt, số lưu có thể phân số sau co; sai số cổ/hông
đo trên scene, không tự suy đoán khớp từ artwork. Ảnh giữ màu mượt và alpha mềm.
Idle2× đóng khung256×256, alpha cao192px, mép dưới16px (logic128/96/8).
Mốc vector hình đứng cao96,0125px do raster hóa/subpixel, dung sai0,1logic;
ảnh đóng khung có silhouette192px đúng. Không sửa thông số A0 để ép test.

## Dựng và xem

Mở `prototype/` bằng Godot4.7.2, trên A0 bấm **Nhân vật tư thế (thử)**;
hoặc chạy `godot --path prototype res://pose_rig/pose_rig.tscn` từ repo root.
Nút idle/run/jump/fall/slash, đổi hướng, bật/tắt đao và VềA0.
4 Sprite2D linear scale0,5 cố định; chỉ actor root lật±1, mọi góc0.
Mốc đế/hông/cổ/chuôi giải từ anchors.json; dữ liệu frames.json.
Jump/fall có2frame dữ liệu nhưng hiện lặp một pose lớp; slash4khung0,30s là
pilot theo lệnh, chưa thay combo thành phẩm; chưa làm hurt/khinh công.

[Ảnh ghép từ hai viewport thật](g1_pose_sheets_compare.png)1600×1440:
trên quay phải, dưới quay trái. Mỗi viewport1600×720 có ảnh gốc nghiêng,
idle,6run,jump,4slash. Không vẽ thêm nhân vật hoặc sửa ảnh viewport.
Nguồn chụp riêng trong prototype/pose_rig/reports/scene_right.png và scene_left.png.

## Tham khảo và Blender

Đã đối chiếu project người dùng chỉ định ở ngoài repo: bộ hình theo tư thế,
offset từng phần, trạng thái chọn frame, thay bộ khi đổi trang bị. Không có cơ sở
để kết luận quy trình họ vẽ bằng Blender. Không chép hình/mã/dữ liệu của nguồn khác.
Áp dụng nguyên tắc chung bằng GDScript và JSON mới của Cờ Lau.

Blender4.3.2 đã cài sẵn. [File nguồn bàn dựng2D](../../art/concept/characters/chr_dbl_poses/pose_authoring_2d.blend)
chứa4 mặt phẳng và texture đóng gói; [render thật](g1_pose_blender_idle.png).
Đây là công cụ xem/chỉnh tranh2D, **không phải mô hình3D/điêu khắc nhân vật mới**.
Chưa chuyển hướng sản xuất sang3D; cần người dùng chọn sau khi xem pilot.

## Script và kiểm tra

Chạy từ repo root; các lệnh Godot dưới đây dùng đường dẫn tương đương chạy trong prototype/.

```sh
python3 tools/cut_pose_sheets.py
python3 tools/check_pose_sheets.py
blender --background --factory-startup --python tools/blender_pose_preview.py
godot --headless --path prototype --editor --import --quit
godot --headless --fixed-fps 60 --path prototype --script res://tests/pose_rig_checks.gd
```

Script đã chạy: [cắt](../../tools/cut_pose_sheets.py), [kiểmPNG](../../tools/check_pose_sheets.py),
[Godot actor](../../prototype/pose_rig/pose_actor.gd), [test](../../prototype/tests/pose_rig_checks.gd),
[chụp scene](../../prototype/pose_rig/viewer.gd), [ghép viewport](../../tools/compare_pose_captures.py),
[Blender](../../tools/blender_pose_preview.py). Mốc đầy đủ: art/sprites/characters/chr_dbl_poses/anchors.json.
Nguyên đầu ra tại [checks.txt](g1_pose_sheets_checks.txt) và commit message.
Kiểm cũ vẫn chạy; test mới mọi khung/cả2hướng: không xoay, scale/linear,
chân y0, cổ/hông≤1px, đủ khung, mũi chém/kết thúc ở trước mặt và đối xứng gốc.
Không thay việc duyệt mỹ thuật hoặc thử lại Android.
