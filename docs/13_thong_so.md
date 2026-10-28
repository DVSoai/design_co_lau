# Danh sách thông số và trạng thái

Mỗi con số quan trọng trong bộ thiết kế được ghi ở đây cùng một trong ba trạng thái:

- **Đã duyệt:** người dùng đã chốt. Muốn đổi phải ghi nhật ký và duyệt lại những gì bị ảnh hưởng.
- **Tạm thời:** dùng ngay để vẽ và dựng, nhưng có thể đổi sau khi chơi thử hoặc sau một mốc cụ thể. Cột "Chốt khi" ghi mốc đó.
- **Đề xuất:** mới chỉ là ý, chưa dùng để sản xuất.
- **Chưa có:** chưa đặt con số; mockup dùng ô số giữ chỗ.

Khi đổi một thông số, cập nhật dòng tương ứng, ghi vào `05_log.md`, và liệt kê các hạng mục đã duyệt bị ảnh hưởng (cột "Ảnh hưởng tới"). Qua mốc A, mọi dòng phải là Đã duyệt, hoặc người dùng đồng ý giữ Tạm thời kèm điều kiện chốt.

## Hiển thị và hình ảnh

| Thông số | Giá trị | Trạng thái | Chốt khi | Ảnh hưởng tới | Nguồn |
|---|---|---|---|---|---|
| Phong cách | Pixel bán hiện đại khoảng 4 đầu, 32 màu | Đã duyệt (28/10/2026) | — | Mọi ảnh, P1–P17, nhân vật, quái, boss, bối cảnh, UI, VFX, trang bị | `01_art_bible.md` |
| Độ phân giải gốc | 960×540, phóng ×2 lên 1920×1080, lọc nearest | Tạm thời | Sau P0 | Mọi mockup, sprite, bố cục màn hình | `01_art_bible.md`, GDD Phần 6 |
| Bảng màu | 16 màu khung xương, mở rộng thành 32 | Tạm thời | Giai đoạn 0, khi có ảnh gốc | Mọi sprite | `01_art_bible.md` |
| Chiều cao nhân vật người | Khoảng 96 điểm ảnh, khung 128×128, chân cách đáy 8 px | Tạm thời | Bộ mẫu chuẩn giai đoạn 1 | Sprite người, hộp va chạm | `01_art_bible.md` |
| Chiều cao boss người | Khoảng 132 điểm ảnh, khung 192×192 (cưỡi thú 192×160) | Tạm thời | Giai đoạn 1 | Sprite boss, đấu trường | `01_art_bible.md` |
| Khung quái thú | Nhỏ 64×64, lớn 128×96 | Tạm thời | Giai đoạn 1 | Sprite quái | `01_art_bible.md` |
| Ô tile | 32×32 | Tạm thời | Giai đoạn 1, khi duyệt tileset Đào Úc | Mọi tileset và bố cục bản đồ | `01_art_bible.md`, `08_map_layout.md` |
| Biểu tượng vật phẩm | 32×32 trong game, bản gốc 64×64 | Tạm thời | Giai đoạn 2 | Biểu tượng | `01_art_bible.md` |
| Chân dung hội thoại | 128×128 | Tạm thời | Giai đoạn 2 | Chân dung, SCR-10 | `01_art_bible.md` |
| Cảnh nền | Mỗi lớp 1920×540, lặp khi cuộn | Tạm thời | Giai đoạn 1 | Cảnh nền | `01_art_bible.md` |

### Hạng mục chịu ảnh hưởng bởi quyết định kích thước 28/10/2026

- Sprite người 96 px / canvas 128×128, boss người 132 px / canvas 192×192, các bộ phận, sprite sheet, baseline và điểm neo.
- Hitbox, tốc độ di chuyển, tầm đánh, vị trí va chạm, vị trí NPC và quái (đều phải kiểm tra lại, không tự tăng tỷ lệ).
- Camera 960×540, giới hạn camera, số ô tile thấy trên màn, bố cục làng/ải/boss, kích thước nền parallax.
- HUD, nút điều khiển, safe area, vị trí màn hình, chân dung, bố cục và vùng chạm; cần dựng lại mockup trên 960×540.
- Bảng hoạt ảnh, vị trí hiệu ứng, hit/spawn frame và khoảng trống quanh nhân vật.

### Hạng mục chịu ảnh hưởng bởi quyết định P0

- **Nhân vật:** `chr_dbl_base`, `chr_dbl_parts`, `chr_dbl_t1` và các bậc trang bị, chân dung; cần kiểm tra lại khớp ghép và baseline ở chiều cao ~96 px.
- **Kẻ địch và boss:** sprite lính các sứ quân, NPC, boss người (~132 px), các sheet animation, hitbox và tỷ lệ so với nhân vật.
- **Bản đồ và công trình:** Hoa Lư, Đào Úc, nền parallax, tileset, thành đất, chòi canh, mái tranh/ngói đơn giản, cờ lau trắng.
- **Hiệu ứng:** P15 chỉ bụi, tia lửa, vệt gió; loại bỏ energy glow.
- **Giao diện và màu:** icon, portrait, UI kit, palette 32 màu, khả năng đọc ở 960×540.
- **Tài liệu/đặc tả liên quan:** `01_art_bible.md`, `02_asset_list.md`, `03_prompts.md`, `05_log.md`, `09_animation_spec.md`, P1–P17 và các bản mockup về sau. Thông số kích thước vẫn **Tạm thời**, chưa tự động thay đổi hitbox/animation khi chưa duyệt mẫu chuẩn.

## Giao diện

| Thông số | Giá trị | Trạng thái | Chốt khi | Ảnh hưởng tới | Nguồn |
|---|---|---|---|---|---|
| Vùng an toàn hai cạnh | 16 điểm ảnh | Tạm thời | Thử trên máy thật | Mọi màn | `06_screens.md` |
| Cỡ chạm nhỏ nhất | 20×20 | Tạm thời | Thử trên máy thật | Mọi nút | `06_screens.md` |
| Nút đánh, ô chiêu, ô vật phẩm | 56×56, 32×32, 28×28 | Tạm thời | Mockup SCR-05 được duyệt | SCR-05, SCR-09 | `06_screens.md` |
| Cỡ chữ tối thiểu | 8 (phụ), 10 (chính) | Tạm thời | Khi chọn font | Mọi màn | `06_screens.md` |

## Di chuyển và bản đồ

| Thông số | Giá trị | Trạng thái | Chốt khi | Ảnh hưởng tới | Nguồn |
|---|---|---|---|---|---|
| Hộp va chạm nhân vật | 16×44 | Tạm thời | Chơi thử bản mẫu | Bố cục bản đồ | `08_map_layout.md` |
| Tốc độ chạy | 112 điểm ảnh/giây (3,5 ô) | Tạm thời | Chơi thử | Bố cục, nhịp chơi | `08_map_layout.md` |
| Độ cao nhảy | 80 điểm ảnh (2,5 ô); bậc tối đa 2 ô | Tạm thời | Chơi thử | Mọi bố cục bản đồ | `08_map_layout.md` |
| Khe rộng nhất | 3 ô | Tạm thời | Chơi thử | Mọi bố cục bản đồ | `08_map_layout.md` |
| Tốc độ thú cưỡi | Ngựa ×1,6; trâu ×1,2, nhảy 1,5 ô; voi không nhảy | Tạm thời | Chơi thử | Bản đồ có thú cưỡi, boss Tiên Du | `08_map_layout.md` |
| Kích thước bản đồ | Làng 40–60 ô, đánh quái 80–120 ô, đấu trường 30–40 ô, ải 40 ô | Tạm thời | Khi duyệt từng bố cục | Bố cục | `08_map_layout.md` |

## Hoạt ảnh

| Thông số | Giá trị | Trạng thái | Chốt khi | Ảnh hưởng tới | Nguồn |
|---|---|---|---|---|---|
| Tốc độ chuẩn | 12 khung/giây; đòn thường và chiêu hồi dài 15 | Tạm thời | Bảng động tác bậc 1 được duyệt | Mọi sprite động | `09_animation_spec.md` |
| Chiêu bấm liên tục | 18 khung/giây, tối đa hồi chiêu × 18 khung | Tạm thời | Chơi thử | 10 chiêu bấm liên tục | `09_animation_spec.md` |
| Số khung từng động tác | Theo bảng trong `09_animation_spec.md` | Tạm thời | Từng bảng động tác được duyệt | Sprite | `09_animation_spec.md` |
| Thời gian báo đòn boss | 0,8–1,2 giây | Tạm thời | Chơi thử từng boss | Sprite boss, hiệu ứng | `09_animation_spec.md` |

## Chiến đấu và tiến trình

| Thông số | Giá trị | Trạng thái | Chốt khi | Ảnh hưởng tới | Nguồn |
|---|---|---|---|---|---|
| Chỉ số và công thức | Theo GDD Phần 2 | Tạm thời | Cân bằng sau bản mẫu | Dữ liệu | GDD Phần 2 |
| Đường cấp | Cấp tối đa 60, công thức kinh nghiệm GDD Phần 2 | Tạm thời | Đo thời gian chơi lát cắt dọc | Nhiệm vụ, quái | GDD Phần 2 |
| Kỹ năng | 20 chiêu, số liệu GDD Phần 2 | Tạm thời | Cân bằng sau bản mẫu | Hoạt ảnh, dữ liệu | GDD Phần 2 |
| Máu và sát thương quái, boss | Theo GDD Phần 4 | Tạm thời | Cân bằng | Dữ liệu | GDD Phần 4 |
| Bảng cường hóa | Theo GDD Phần 2 | Tạm thời | Cân bằng | Dữ liệu, SCR-12 | GDD Phần 2 |
| Giữ ải | 8 đợt, đợt 4 thủ lĩnh, đợt 8 boss; 20 giây chuẩn bị; tối đa 4 công trình; sao 1, 2, 3 ở cờ còn đứng, 50%, 80% | Tạm thời | Chơi thử ải Tam Điệp | Bố cục ải, SCR-07, SCR-17 | GDD Phần 3 |

## Kinh tế và nạp tiền

| Thông số | Giá trị | Trạng thái | Chốt khi | Ảnh hưởng tới | Nguồn |
|---|---|---|---|---|---|
| Giá NPC bằng tiền đồng | Quy đổi từ giá yên Ninja School | Chưa có | Sau lát cắt dọc | Dữ liệu cửa hàng | GDD Phần 6 |
| Tỉ giá | 1 ngân phiếu = 1.000 ngân lượng, một chiều | Đề xuất | Cân bằng kinh tế | Cửa hàng ngân phiếu | GDD Phần 2 |
| Ngân phiếu thưởng | 50 mỗi hồi, 20 lần đầu hạ mỗi boss | Đề xuất | Cân bằng kinh tế | Nhiệm vụ | GDD Phần 3 |
| Giá cửa hàng ngân phiếu | Theo bảng GDD Phần 2 mục 10 | Đề xuất | Cân bằng kinh tế | SCR-13 | GDD Phần 2 |
| Phạm vi bán ở bản đầu | Chỉ món vĩnh viễn qua Google Play, không ngân phiếu nạp, không máy chủ | Đã duyệt (28/10) | — | SCR-13, F13 | `12_ngan_phieu.md` mục 12 |
| Ngân phiếu thưởng trong gói khởi đầu | 300, mỗi ô nhận một lần | Đề xuất | Cân bằng kinh tế | Gói khởi đầu | `12_ngan_phieu.md` mục 12 |
| Giá món vĩnh viễn | Đề xuất: gói khởi đầu 22.000đ; đồ thời trang 22.000–49.000đ; thú cưỡi ngoại hình 49.000–99.000đ; túi da cấp 3 22.000đ | Đề xuất | Mốc B | SCR-13 | `12_ngan_phieu.md` mục 12 |
| Gói nạp ngân phiếu | 5 gói từ 20.000đ đến 500.000đ | Đề xuất cho bản có nạp | Mốc C | SCR-13 bản có nạp | GDD Phần 2 |
| Căn cứ Hoa Lư | 4 công trình, 3 cấp, không chờ xây; lò rèn giảm 5%, 10%, 15% | Đã duyệt (28/10) | — | SCR-22 | `11_design_freeze.md` |
| Vật liệu mỗi cấp căn cứ, mức tăng tướng, lương thảo, thức ăn thú | Chưa đặt | Chưa có | Cân bằng kinh tế | SCR-22 | `06_screens.md` |
| Thời hạn giao dịch đang chờ | 7 ngày | Đề xuất cho bản có nạp | Mốc C | `12_ngan_phieu.md` | `12_ngan_phieu.md` |

## Quyết định đã duyệt

Các quyết định ngày 28/10/2026 ghi ở đầu `11_design_freeze.md` là Đã duyệt: phong cách mặc định, bỏ hồi sinh tại chỗ, bản đồ vùng có đi nhanh, căn cứ 4 công trình 3 cấp không chờ xây, offline toàn bộ, đăng nhập tùy chọn, hai nguồn ngân phiếu, cách xử lý hoàn tiền, và chuyển xác định tuổi cùng giá gói nạp sang mốc B. Engine Godot 4 với GDScript cũng là Đã duyệt.
