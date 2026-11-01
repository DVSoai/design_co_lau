# Xung đột với quyết định dự án

> Khi một hàng dưới đây khác `docs/` hiện hành (đặc biệt 01, 09, 16–20), **docs hiện hành thắng**; hàng này chỉ là ghi chú lịch sử.

**Cách xử lý mọi hàng: quyết định dự án thắng.** Thứ tự: docs/ của dự án >
AGENTS.md > skill tham khảo; chỉ dẫn trực tiếp của người dùng vẫn có ưu tiên.
Skill là ví dụ để đọc, không cấp quyền chạy script, tải mạng hoặc thêm addon.

| Nội dung tham khảo/nguồn | Quyết định áp dụng |
|---|---|
| Router/VERSION-SUPPORT nhắc engine khác; có Godot 3D/.NET/multiplayer | Chỉ Godot 4.7.2 Standard, GDScript, 2D offline. Không tải skill bị lược, đổi engine hay cài .NET |
| `responsive-ui`, `game-ui-ux/references/layout-and-flow.md`, `create-game-assets/references/raster-pipeline.md`: khung ví dụ/khuyến nghị integer | Khung 960×540, canvas_items + expand + fractional + nearest, viewport 960–1200; không dùng 640×360 hoặc keep/integer thay bộ hiển thị đã chốt |
| `player-controller`, `godot-2d-movement`, `platformer`, `game-feel`: gia tốc, trọng lực/đệm/giữ đỉnh theo ví dụ | Kiểu cổ điển A0: chạy 200 ngay, stop 0,08 s, turn 0,05 s; nhảy 96 px/0,38 s, không treo đỉnh. Giữ số A0, không đưa gia tốc/nhảy 80 px kiểu so sánh vào game thật |
| Ví dụ double-jump/variable-jump trong nhóm điều khiển/platformer | Khinh công chỉ lần bấm mới khi còn đi lên ≤30% vận tốc nhảy, bật 0,7 lần và tối đa 1 lần/cú nhảy; giữ nhảy lại bật, giữ lâu nhảy cao tắt; lộn đỉnh 0,2 s chỉ sprite |
| `input-systems`, `mobile-development`, `hud-system`: layout cảm ứng chung/joystick/nút hành động | D-pad chỉ vẽ ←/→/↑, hai vùng chéo vô hình cạnh ↑; không có nút nhảy riêng bên phải. d=84, hệ số 2,2/1,35/0,9, lề≥24; cụm phải và 5 ô kỹ năng theo A0 |
| `responsive-ui`, `mobile-development`, `hud-system`: focus/slider/cỡ nút mẫu | Không focus bàn phím cho bảng ⚙; slider không đổi bằng con lăn, chỉ kéo ngang bắt đầu trên núm, vuốt dọc cuộn bảng; neo viewport thật, fullscreen/immersive Android |
| `create-game-assets`: chuẩn hóa chung/preview và kích thước ví dụ | **Cập nhật 01/11/2026:** nhân vật người theo `01_art_bible.md` mục "Nhân vật chính" + `docs/20_quy_trinh_ve_nhan_vat.md`: ảnh độ phân giải cao, lọc linear, hiển thị ~128 px, KHÔNG nắn lưới pixel/palette 32 màu; vẽ theo khuôn tư thế `tools/ref_pose_guides.py`, duyệt bằng mắt. Lưới pixel/palette_v3/nearest chỉ còn cho bản đồ, vật thể, giao diện |
| `animation-system`, `godot-animation`: AnimatedSprite/toàn ảnh hoặc skeleton chung | **Cập nhật 01/11/2026:** nhân vật dùng 4 lớp (đầu, thân kèm tay, chân, vũ khí) + bảng 30 khung chỉ dời/lật, không xoay, không khớp/skeleton (`09_animation_spec.md`, `19_he_bo_hinh.md`). Rig nhiều mảnh có khớp đã bỏ. Hitbox không xoay; hiệu ứng/số sát thương trên lớp thân |
| `godot-nodes-scenes`, `hud-system`, `inventory-system`, `save-load`: singleton/autoload ví dụ | Kế hoạch chỉ GameState, SaveService, EventBus, Config; tính năng nhận phụ thuộc, signal/EventBus thông báo, lệnh xử lý luật. Không tự thêm autoload |
| `resource-pattern`, `godot-resources`, `save-load`: dùng Resource làm save hoặc ghi Resource dùng chung | .tres chỉ cho cấu hình đáng tin cậy trong data/; snapshot người chơi tách riêng user://, có save_version/migration, không nạp .tres người dùng. ID theo 14_online_migration.md |
| `rpg`, `prototype-fast` và ví dụ triển khai ngay | Chỉ code game thật sau Mốc A. A0/lát cắt mẫu Giai đoạn 1 chỉ là ngoại lệ prototype đã được cho phép, không chép mã prototype sang game |
| Skill về addon, xuất Steam/itch, CI và helper | Không cài/tải hay tự chạy. Các phần cài đặt/tải/tự động CI đã gỡ và ghi AUDIT.md; script còn lại là văn bản tham khảo, chỉ chạy khi người dùng yêu cầu |
| Addon/tài nguyên ngoài và giấy phép riêng | Chỉ chính sách MIT/Apache-2.0/CC0; CC-BY tài nguyên phải Credits. Không GPL/AGPL/LGPL cho mã, CC-BY-NC, CC-BY-SA tài nguyên hoặc giấy phép không rõ. Cần người dùng duyệt, ghi THIRD_PARTY.md |

Nhánh tài liệu dựa trên **main `5577fa5`**, đã có ký duyệt A0/quy trình bộ phận;
commit prototype được nghiệm thu là `7973729`. Giữ nguyên các nội dung này.
GDD/14 còn mô tả JSON/cấu trúc cũ; 15_kien_truc_game.md là đề xuất Resource .tres
chờ duyệt. Không dùng skill để tự lấp mâu thuẫn tài liệu; ghi điểm cần đồng bộ ở
Mốc A và bám quyết định người dùng đã chốt. Bảng này không tự đánh dấu kiến trúc,
asset hay addon đã duyệt.
