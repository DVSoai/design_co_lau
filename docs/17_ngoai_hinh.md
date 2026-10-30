# Hệ thống ngoại hình

Ô thời trang, một dạng cố định, gồm vũ khí và có chỉ số: người dùng chốt **28/10/2026**. Giới hạn số, hiệu ứng và thiết kế chi tiết còn đề xuất Mốc A1. Theo 01_art_bible và rig 16; không sửa prototype ở lượt này.

## Trang bị thường và part_set

Mỗi item có part_set. Áo thay thân/tay trên gần xa; quần thay đùi/cẳng chân gần xa; vũ khí thay kiem/cung; nón/khăn nếu có ô thay phần trên đầu. Các ô đổi độc lập; mảnh còn lại dùng bộ gốc. Cùng bậc dùng chung hình, màu/hoa văn riêng theo món là tùy chọn sau.

| Bậc | Hướng thiết kế riêng thế kỷ 10 (chưa duyệt art) |
|---|---|
| chr_dbl_t1 | Vải mộc bền, quần nâu, kiếm/cung tre giản dị |
| chr_dbl_t2 | Vải dày nhuộm đất, đai chắc, vũ khí hoàn thiện hơn |
| chr_dbl_t3 | Giáp da nhẹ, quần gia cố, cung gỗ/tre ghép |
| chr_dbl_t4 | Giáp da đóng lá sắt nhỏ, trang phục quân sĩ |
| chr_dbl_t5 | Giáp lá sắt, vải chàm tiết chế, kiếm chắc/cung sừng |
| chr_dbl_t6 | Giáp tướng bằng lá sắt, đai đồng giản dị, vũ khí tinh luyện |
| chr_dbl_t7 | Bộ nghi lễ chiến trận của quân Đinh, dấu bông lau chỉ ở bậc này |

Mọi bậc có áo/quần/kiếm/cung riêng; bám STYLE/AVOID, không áo dài/giáp samurai/long bào hay năng lượng phép thuật.

## Hiệu ứng cường hóa — đề xuất, chưa chốt số

+8 ánh kim nhẹ trên áo/vũ khí; +12 vệt phản sáng theo đường vung; +16 hạt bụi/tia lửa quanh vũ khí khi chuyển động/va chạm. Chỉ phản xạ kim loại, bụi và tia lửa vật lý; không hào quang năng lượng, không hạt phép tự phát. Cần thử độ dễ đọc và chốt mốc ở Mốc A1.

## Các ô thời trang bản đầu

- `head`: khăn/búi tóc: head.
- `shirt`: áo: body + upper_arm_near/far.
- `pants`: quần: thigh_near/far + shin_near/far.
- `weapon`: vũ khí: kiem hoặc cung theo phái.
- `cape`: áo choàng: cape sau lưng, khớp vai.
- `face`: khăn che mặt/mặt nạ tuồng/chèo: face_overlay trên mặt.
- `mount`: thú cưỡi ngoại hình.
- `title`: danh hiệu: hình trên đầu.

Thời trang theo ô độc lập, mỗi món một dạng hình cố định, không đổi theo cấp. Ô trống hiện trang bị thật; mặc lẻ từng ô. Thời trang **có chỉ số**, cộng vào trang bị thật, không thay thế; ẩn hình vẫn giữ chỉ số. Không cường hóa thời trang. Tổng chỉ số một bộ đề xuất ≤10–15% bộ trang bị cùng bậc, từng loại chỉ số đối chiếu tương ứng; không thêm loại chỉ số trang bị thường không có. Cách cộng/chuẩn hóa và trần chính xác chốt Mốc A1, không cộng thô các đại lượng khác đơn vị. Toàn bộ số chỉ số là thiết kế riêng. Hai nguồn: mua vĩnh viễn Google Play dùng chung cả 3 ô nhân vật; boss/nhiệm vụ/giữ ải cho món có chỉ số tương đương nhưng hình khác, không để người không nạp kém hẳn. Vũ khí thời trang thay hình theo phái, vẫn hiện hiệu ứng mức cường hóa vũ khí thật. [Phạm vi sau]: biến hình thay cả người.

## Dữ liệu và khối lượng

Item thường: id ổn định itm_, part_set. Thời trang: id itm_fsh_, part_set, stats, source=iap/ingame, slot; dùng sku_/ent_ cho sản phẩm/quyền lợi mua, theo 14_online_migration. Quyền sở hữu IAP dùng chung 3 ô, lựa chọn mặc và món kiếm trong game thuộc từng ô; cấp quyền lợi idempotent, không cộng chỉ số 3 lần. part_set là map part_id→asset_id, không cho món kiếm hiển thị thành cung sai phái.

7 bậc × (áo 3 mảnh + quần 4 mảnh + kiếm 1 + cung 1) = **63 mảnh thay thế**, 28 part_set danh mục. Không vẽ lại toàn bộ clip cho từng bậc. Đầu gốc/tay/bàn chân dùng lại. Nếu vẽ nón trang bị riêng, cộng tối thiểu 1 lớp/món; chưa tính vào 63.

| Ô thời trang | Khối lượng mỗi mẫu |
|---|---|
| head | 1 mảnh đầu/tóc |
| shirt | 3 mảnh |
| pants | 4 mảnh |
| weapon | 1 mảnh/phái; 2 nếu phát hành cả Kiếm/Cung |
| cape | 1 lớp, vòng 6–10 frame đề xuất |
| face | 1 lớp |
| mount | 1 bộ thú, số frame theo 09; không phải 1 PNG |
| title | 1 hình trên đầu |

Số mẫu IAP/ingame mỗi ô chưa chốt, nên chưa thể tính tổng art thời trang. Áo choàng/ánh kim có vòng 6–10 frame đề xuất chạy song song rig, không kéo dài attack/hit window. Chỉ sản xuất/duyệt sau thiết kế mẫu.

## Khung mẫu vũ khí theo cấp — bản thử chưa duyệt

Mỗi nhân vật chỉ trang bị **Kiếm HOẶC Cung** theo phái, không cầm/đeo đồng thời
hai loại. Các mẫu đứng cạnh nhau trong viewer là nhân vật so sánh riêng.

Bảy cấp vũ khí1/10/20/30/40/50/60 dùng chung5IDgóc: gio_sau, vung_len, ngang,
bo_xuong, dam. Mỗi bộ thay bằng5PNGvẽ sẵn, runtime không xoay. Bản thử hiện có
cấp1/30/60 (15PNG);10/20/40/50 là slotchưa vẽ, không coi là asset đã hoàn thành.
Cùng góc: canvas256×256ở2×, grip(96,144) cùng pixel; trục mũi lệch≤3° và chiều
lưỡi khác≤15%. Góc ngang và đâm có thể dùng cùng hướng nhưng IDriêng.
Vệt4khung dùng chung mọi cấp, đặt theo **tâm ảnh +offsetlogic** trong swing.json;
không vẽ lại vệt theo từng bộ kiếm. Khi tấn công ẩn hình kiếm cầm/đeo và hiện
lưỡi đã đăng ký vào tay; không chồng hai kiếm.

`tools/build_weapon_template.py` chỉ đăng ký/co đồng dạng và xoayOFFLINEtừ
nguồn tạo riêng, xuấtPNGgóc cố định bằng supersampling/BICUBIC→LANCZOS.
`tools/check_weapon_template.py` kiểm cả metadata lẫn trục pixel/chiều lưỡi thực.
Runtime mỗi Sprite2Drotation0, scale0,5cố định, chỉ lật nodegốc.
Cung có tên trên dây ở pha kéo; tên bay là Sprite2Driêng chỉ sinh khi buông.
Khung mẫu/phép kiểm chưa thay duyệt mỹ thuật hay bộ đồ/các cấp còn thiếu.
