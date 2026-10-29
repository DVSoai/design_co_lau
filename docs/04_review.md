# Soát ảnh và chuyển thành sprite

## Tự soát trước khi đưa người dùng duyệt

Codex soát từng ảnh theo năm điều. Ảnh trượt điều nào thì loại, ghi lý do vào `05_log.md`, và tạo lại.

1. **Lịch sử:** không có đồ võ sĩ Nhật Bản, chiến binh bí mật Nhật Bản, kiếm katana, long bào, áo dài, nón quai thao, mái cong cung đình. Trang phục đúng mục "Trang phục thế kỷ 10" của art bible.
2. **Đồng bộ:** đặt cạnh `art/reference/ref_dinh_bo_linh.png`, tỉ lệ đầu thân, độ dày nét viền, hướng sáng và cách tô bóng phải giống nhau.
3. **Dễ đọc:** thu ảnh về kích thước trong game (nhân vật người cao 96 điểm ảnh theo chuẩn A0) mà vẫn phân biệt được nhân vật, phái và loại quái.
4. **Màu cờ:** lính và boss đúng màu thế lực trong art bible.
5. **Sạch:** không có chữ, chữ ký, logo hay vật thể hiện đại; nền đúng màu để tách.

## Chuyển thành sprite

Ảnh duyệt rồi vẫn cần chuẩn hóa lưới. **Với nhân vật chính, dùng quy trình ghép bộ phận ở `01_art_bible.md`: imagegen + snap_pixel + sửa pixel bằng script; Claude/người dùng duyệt từng bộ phận bằng báo cáo và bằng mắt. Không bắt buộc chỉnh tay hoặc thuê họa sĩ.** Các bước chung bên dưới áp dụng cho asset còn lại; không dùng để ép mọi mảnh/pose động tác về silhouette 96 px.

1. Tách nền bằng script của skill `$imagegen`, ra PNG có kênh trong suốt.
2. Thu nhỏ về kích thước trong art bible bằng nearest neighbor.
3. Ép về bảng màu chung (palette quantize, không dither).
4. Sửa viền, điểm ảnh lạc và đường chân bằng script; Aseprite/LibreSprite là tùy chọn cho asset có quy trình chỉnh riêng, không phải yêu cầu nhân vật chính.
5. Với Đinh Bộ Lĩnh: kiểm bộ phận đầy đủ, khớp cha–con, phần vẽ bù khi xoay, vị trí/góc/thứ tự lớp từng frame và áo/quần/vũ khí thay thế; theo `chr_dbl_parts` và `chr_dbl_anim_*`, không chia ảnh thành bốn vùng chữ nhật để giả tách bộ phận.
6. Xuất sprite sheet theo lưới đều, lưu vào `art/sprites/`, `art/tiles/`, `art/ui/` hoặc `art/vfx/`.

## Bản quyền

Ảnh do AI tạo hoàn toàn có thể không được bảo hộ bản quyền (theo quan điểm hiện tại của Cục Bản quyền Mỹ). Nhân vật chính theo quy trình ghép bộ phận và sửa pixel bằng script đã chọn trong art bible; việc duyệt kỹ thuật/mỹ thuật không tự xác lập quyền bảo hộ. Các boss, ảnh chính quảng bá và logo vẫn phải được vẽ lại hoặc chỉnh tay đáng kể theo quy trình riêng trước phát hành. Giữ `05_log.md` và các file trung gian làm bằng chứng quá trình. Kiểm tra điều khoản sử dụng thương mại của OpenAI cho ảnh tạo ra trước khi phát hành.
