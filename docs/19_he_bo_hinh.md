# Hệ bộ hình nhân vật theo cách game tham khảo (chốt 01/11/2026)

Người dùng chốt: tổ chức hình nhân vật **đúng như game tham khảo** (số liệu ở
`docs/ref/so_lieu_tham_khao.json`, mục `quy_mo_tham_khao`). Hình là của mình; cách chia,
dùng chung và đặt khung theo tham khảo.

## 1. Bộ hình (part set)

- Mỗi **bộ** là một danh sách hình của một lớp: **đầu 8**, **thân 18**, **chân 10**,
  **vũ khí cầm tay 1** (+ hình vung/hiệu ứng riêng).
- Mỗi hình trong bộ có `{ảnh, dx, dy}` (độ lệch so với điểm neo của khung). Bảng 30 khung
  chọn hình nào trong bộ cho từng khung — **bảng khung dùng chung cho mọi bộ**.
- Món trang bị chỉ trỏ tới id bộ: nón → bộ đầu, áo → bộ thân, quần → bộ chân, vũ khí → 1 hình.

## 2. Dùng chung để giảm khối lượng (như tham khảo)

- **Đầu dùng chung nhiều cấp**: Lv1–30 chung một bộ đầu (tóc búi, dải đỏ); Lv40, 50, 60 mỗi
  cấp một bộ đầu có mũ. Các ô thời trang đầu là bộ riêng.
- **Chân đánh dùng chung**: nhóm khung 13–20, 21–25, 26–29 mỗi nhóm một hình chân đứng tấn
  (mục `chan_dung_chung_khi_danh`).
- **Vũ khí cầm tay**: 1 hình cho mỗi cấp, đặt bằng grip + dx, dy ở khung 0–7, 12, 21;
  vẽ trên thân. Ẩn khi lộn và khi đánh.
- **Vệt chém, mũi tên, vòng gió lộn**: dùng chung mọi cấp, chỉ đổi màu theo cấp.

## 3. Khối lượng nhân vật chính

| Phần | Số hình |
|---|---|
| Bộ thân × 7 cấp | 18 × 7 = 126 |
| Bộ chân × 7 cấp | 10 × 7 = 70 |
| Bộ đầu (Lv1–30 chung + Lv40/50/60) | 8 × 4 = 32 |
| Vũ khí cầm tay (kiếm, cung × 7) | 14 |
| Hiệu ứng (đòn thường + 16 chiêu, dùng chung cấp) | ~50–80 |
| **Tổng** | **~290–320** |

## 4. Quy trình mỗi cấp

1. Lấy **bộ Lv1 đã duyệt** làm khuôn: giữ nguyên dáng, điểm neo, bảng khung.
2. Chỉ "thay áo" theo cột cấp đó trên bảng mẫu (`art/reference/chr_dbl_board_*.png`).
3. Ảnh duyệt: từng khung đặt dưới khung Lv1 và khung tham khảo tương ứng; duyệt bằng mắt.
4. Test chỉ kiểm hồi quy (thời lượng, tỉ lệ, số khung, lật hướng) và đo trên ảnh đã ghép thật.
