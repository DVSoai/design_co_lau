# Luồng tham khảo nhân vật — bắt buộc trước khi vẽ/dựng nhân vật chính

Người dùng chốt 30/10/2026: mọi bước vẽ/dựng nhân vật chính (trang phục, vũ khí, đòn đánh,
chiêu, thú cưỡi) phải **dựng lại hình của game tham khảo bằng `tools/ref_render.py` và đặt
cạnh bản của mình** trước khi báo xong. Zip nguồn game tham khảo nằm NGOÀI repo; ảnh xuất ra
thư mục tạm, **không commit** ảnh/dữ liệu/tên của game tham khảo.

## 1. Chạy công cụ

```
python3 tools/ref_render.py --server <thư mục giải nén zip server> --client <thư mục giải nén zip client> --out /tmp/ref_render
```

Xuất: `ref_30_khung.png` (30 khung thân), `ref_cam_kiem.png`, `ref_cam_cung.png` (tư thế cầm
lúc đứng/chạy/nhảy), `ref_don_kiem.png`, `ref_don_cung.png` (đòn cơ bản đúng lớp), và in số đo.

## 2. Cơ chế (đọc từ nguồn)

- **4 lớp**: đầu, chân, thân kèm tay, vũ khí. Bảng 30 khung trong `Char.java`
  (`Class127`): mỗi khung [đầu, chân, thân, vũ khí] = {chỉ số hình trong bộ, dx, dy}.
  Vẽ: x = gốc + (dx khung + dx hình) × hướng; y = gốc − dy khung + dy hình.
  Quay phải neo góc trên-trái; quay trái lật gương. Không xoay.
- **Bộ hình** (`nj_part`): loại 0 đầu 8 hình, 1 thân 18, 2 chân 10, 3 vũ khí 2.
  Phần vũ khí 12 = kiếm, 14 = cung.
- **Vũ khí cầm tay chỉ hiện** ở khung 0–7 (đứng, chạy), 12 (nhảy), 21. Lộn người và mọi
  khung đánh: không vẽ vũ khí cầm tay; hình hiệu ứng thay cho vũ khí.
- **Lớp** (bảng `skill` trong `nja.sql`, cột `class`): 1 = Kiếm, 4 = Cung, 5 = Đao.
  **Chỉ so Kiếm với lớp 1, Cung với lớp 4.** Không dùng chiêu lớp 5 (Đao) làm mẫu Kiếm.
- **Chiêu** (`nj_skill`): danh sách nhịp mặt đất và trên không; mỗi nhịp = khung thân +
  3 hiệu ứng {id, dx, dy} + đạn {id, dx, dy}. **Hiệu ứng** (`nj_effect`): chuỗi {hình, dx, dy},
  vẽ theo TÂM ảnh, quay trái lật và đảo dấu dx.
- Đòn cơ bản Kiếm (chiêu 1): khung thân 13 → 14 → 15 → 16 → 16 → 13; hiệu ứng 16 ở nhịp 2,
  39 ở nhịp 3 — vệt lia ngang ôm trước thân. Đòn cơ bản Cung (chiêu 28): khung 14, 14, 18, 18,
  18, 17, 17, 17; hiệu ứng 10 ở nhịp 1, 50 ở nhịp 5.

## 3. Số đo (zoom 4 ≈ màn cao 720)

| Mục | Game tham khảo | Cờ Lau |
|---|---|---|
| Nhân vật khung 00 | 131 px (32 px gốc) | 128 px hiển thị (A0) |
| Đầu kèm tóc | 0,58 H (tóc dựng cao) | theo 01_art_bible mục 8 |
| Kiếm cầm tay | dài 0,78 H | 0,75–0,8 H |
| Cung cầm tay | cao ≈ 1,0 H | 0,9–1,0 H |
| Hình vung lớn nhất | rộng ≤ 1,6 H, cao ≤ 1,1 H | như vậy |

## 4. Quy trình mỗi lần vẽ

1. Chạy công cụ, mở ảnh tham khảo tương ứng.
2. Vẽ theo **bảng mẫu của mình** (`art/reference/chr_dbl_board_*.png`) về ngoại hình,
   và theo **ảnh tham khảo** về tư thế, nhịp, cách cầm, dáng hiệu ứng, tỉ lệ.
3. Xuất ảnh so tạm: bản mình | bảng mẫu | game tham khảo, cùng chiều cao 128 px.
   Khác kiểu (tư thế, cách cầm, hướng/dáng vệt, tỉ lệ) là chưa đạt.
4. Ghi kết quả so (bằng lời) vào log; không commit ảnh so có hình game tham khảo.

## 5. Số liệu đã trích sẵn trong repo (người dùng chốt 31/10/2026)

`docs/ref/so_lieu_tham_khao.json` chứa **số liệu cơ chế** đã đọc từ game tham khảo — không có
ảnh, không có mã: công thức đặt lớp, bảng 30 khung (đầu/chân/thân/vũ khí + dx, dy), độ lệch
hình mặc định, khung có vũ khí cầm tay, toàn bộ chiêu lớp Kiếm (1) và Cung (4) theo nhịp
(khung thân, hiệu ứng, đạn, dx, dy), độ lệch từng hình của các hiệu ứng đó, và số đo tỉ lệ.
**Được dùng thẳng các số này** (khung, nhịp, độ lệch, tỉ lệ) để dựng nhân vật Cờ Lau; hình vẽ
vẫn là của mình. Không cần zip vẫn làm được; có zip thì chạy thêm `ref_render.py` để xem hình.
