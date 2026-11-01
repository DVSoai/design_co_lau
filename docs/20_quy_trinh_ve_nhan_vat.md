# Quy trình vẽ nhân vật — bắt buộc cho mọi lượt vẽ đầu/thân/chân/vũ khí/hiệu ứng

Viết 01/11/2026 sau nhiều lượt Lv1 phải sửa đi sửa lại. Mỗi lỗi đã gặp đều có một bước
chặn tương ứng ở dưới. Thứ tự ưu tiên khi mâu thuẫn: người dùng > `01_art_bible.md` mục 8 >
file này > số liệu tham khảo.

## Lỗi đã gặp → nguyên nhân → bước chặn

| Lỗi | Nguyên nhân | Bước chặn |
|---|---|---|
| Kiếm cầm ngược, kiếm như que, cung như gậy | Vẽ theo mô tả chữ, không có khuôn | B2 khuôn tư thế + B3 khung kích thước |
| Mất một chân, cổ lệch, chuôi ngoài nắm tay | Mỗi khung sinh ảnh riêng, không so | B5 tự soát bằng mắt |
| Người gầy "é", lệch tỉ lệ tham khảo | Tự chọn tỉ lệ | Khung kích thước tham khảo (B3) |
| Lấy nhầm đòn Đao làm mẫu Kiếm | Không kiểm lớp | Kiếm = lớp 1, Cung = lớp 4 (`nja.sql`) |
| Test xanh mà hình sai | Test so với số tự khai | Test đo trên ảnh ghép thật; duyệt bằng mắt |
| Ảnh AI bị từ chối "violence" | Prompt có từ chiến đấu | Mẫu prompt B4 (vật phẩm/tư thế trung tính) |

## B1. Chuẩn bị (mỗi lượt)

```
python3 tools/ref_render.py      --server <zip server> --client <zip client> --out /tmp/ref_render
python3 tools/ref_pose_guides.py --server <zip server> --client <zip client> --out /tmp/ref_pose --scale 2
```
- `/tmp/ref_render`: hình tham khảo (30 khung, cầm kiếm/cung, đòn kiếm/cung) — CHỈ để so.
- `/tmp/ref_pose`: **khuôn tư thế** từng khung = bóng phẳng theo màu lớp (đầu đỏ, thân xanh lá,
  chân xanh dương, vũ khí vàng) + khung bao + gốc chân, đã đổi về cỡ Cờ Lau (scale 2 = người ~256 px).
  `khuon.json`: khung bao từng lớp mỗi khung (tọa độ so với gốc chân).
- Không commit hai thư mục này.

## B2. Mỗi hình vẽ phải theo khuôn tư thế của đúng khung đó

- Đính kèm khi tạo ảnh: (1) `khung_XX.png` (hoặc `_kiem`/`_cung`) của khung đang vẽ; (2) hình Lv1
  đã duyệt cùng lớp (nếu có) làm mẫu thiết kế; (3) bảng mẫu `art/reference/chr_dbl_board_*.png`.
- Yêu cầu: **giữ đúng dáng và vị trí các mảng màu của khuôn**; chỉ thay bằng nhân vật của mình.
- Không sinh tư thế mới ngoài khuôn. Cấp Lv10–60: dùng hình Lv1 đã duyệt làm ảnh gốc, chỉ "thay áo".

## B3. Khung kích thước

- Khung bao từng hình = khung bao lớp tương ứng trong `khuon.json` (±8%), trừ đầu nếu người dùng chốt
  tỉ lệ khác (xem `01_art_bible.md` mục 8).
- Vũ khí cầm tay: 1 hình/cấp; điểm cầm (grip) đặt cùng vị trí tỉ lệ như hình tham khảo; vẽ TRÊN thân.

## B4. Mẫu prompt tạo ảnh

```
Character sprite part for a 2D side-view mobile game, facing right, transparent/flat #00FF00 background.
Redraw the attached COLOR-BLOCK POSE GUIDE as the attached character design:
- keep exactly the same silhouette, pose and position of each color block
  (red = head+hair, green = torso with arms, blue = legs, yellow = held prop);
- [lớp đang vẽ: chỉ vẽ phần ... / vẽ đủ cả người để cắt]
- same face, hair, red hair ribbon, outfit and colors as the attached design sheet;
- bold even dark outline, flat colors with 2–3 tone shading, no text.
<khối STYLE-V2 nguyên văn> <khối AVOID nguyên văn>
```
- Vũ khí/hiệu ứng: mô tả như **vật phẩm** ("game inventory item icon, ... prop, isolated object, no person");
  tránh các từ attack, kill, fight, blood, weapon. Bị từ chối 1 lần → vẽ SVG theo khung kích thước,
  giữ file .svg nguồn.

## B5. Tự soát bằng mắt TRƯỚC khi push (bắt buộc, ghi kết quả vào commit message)

Xuất một tờ: mỗi khung 3 ô cạnh nhau — **khuôn** | **hình mình (ảnh chụp Godot thật)** | **tham khảo** —
cùng chiều cao, phóng 2×, cả hai hướng. Trả lời từng khung (Có/Không):
1. Dáng khớp khuôn (các mảng đầu/thân/chân/vũ khí đúng chỗ)?
2. Thấy đủ 2 bàn chân (khung chạy/đánh)?
3. Đầu nằm đúng trên cổ áo, không hở/không lòi cổ?
4. Nắm tay bọc chuôi; vũ khí đúng hướng, nằm trên thân, thấy rõ?
5. Kích thước kiếm/cung giống tham khảo (to bản / cong, không que/gậy)?
6. Cùng mặt, tóc, áo, màu với Lv1 đã duyệt?
Khung nào "Không" → sửa xong mới push. Không tự hạ ngưỡng test.

## B6. Mỗi lượt chỉ làm một việc

Lượt vẽ chỉ vẽ (và gắn hình); lượt hệ thống chỉ sửa code/dữ liệu. Không gộp vẽ lại + đổi cơ chế + viết
test lớn trong một lượt.
