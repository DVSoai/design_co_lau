# Soát ảnh và chuyển thành sprite

## Tự soát trước khi đưa người dùng duyệt

Codex soát từng ảnh theo năm điều. Ảnh trượt điều nào thì loại, ghi lý do vào `05_log.md`, và tạo lại.

1. **Lịch sử:** không có đồ samurai, ninja, kiếm katana, long bào, áo dài, nón quai thao, mái cong cung đình. Trang phục đúng mục "Trang phục thế kỷ 10" của art bible.
2. **Đồng bộ:** đặt cạnh `art/reference/ref_dinh_bo_linh.png`, tỉ lệ đầu thân, độ dày nét viền, hướng sáng và cách tô bóng phải giống nhau.
3. **Dễ đọc:** thu ảnh về kích thước trong game (nhân vật cao khoảng 48 điểm ảnh) mà vẫn phân biệt được nhân vật, phái và loại quái.
4. **Màu cờ:** lính và boss đúng màu thế lực trong art bible.
5. **Sạch:** không có chữ, chữ ký, logo hay vật thể hiện đại; nền đúng màu để tách.

## Chuyển thành sprite

Ảnh duyệt rồi vẫn chưa dùng thẳng được, vì công cụ tạo ảnh không vẽ đúng lưới điểm ảnh. Người chỉnh tay (hoặc Codex khi được yêu cầu, bằng script Python với Pillow) làm các bước:

1. Tách nền bằng script của skill `$imagegen`, ra PNG có kênh trong suốt.
2. Thu nhỏ về kích thước trong art bible bằng nearest neighbor.
3. Ép về bảng màu chung (palette quantize, không dither).
4. Mở trong Aseprite hoặc LibreSprite: sửa viền, sửa điểm ảnh lạc màu, căn đường chân cho mọi khung.
5. Với Đinh Bộ Lĩnh: tách thành bốn lớp đầu, thân, chân, vũ khí, cùng điểm neo ở từng khung.
6. Xuất sprite sheet theo lưới đều, lưu vào `art/sprites/`, `art/tiles/`, `art/ui/` hoặc `art/vfx/`.

## Bản quyền

Ảnh do AI tạo hoàn toàn có thể không được bảo hộ bản quyền (theo quan điểm hiện tại của Cục Bản quyền Mỹ). Vì vậy nhân vật chính, các boss, ảnh chính quảng bá và logo phải được vẽ lại hoặc chỉnh tay đáng kể trước khi phát hành. Giữ `05_log.md` và các file trung gian làm bằng chứng quá trình. Kiểm tra điều khoản sử dụng thương mại của OpenAI cho ảnh tạo ra trước khi phát hành.
