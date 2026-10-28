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
| Độ phân giải gốc | 960×540; viewport rộng 960–1200 px logic theo tỉ lệ máy | Đã duyệt (A0, 28/10/2026) | — | Mọi mockup, sprite, bố cục màn hình | A0 Android, Realme RMX3760, Godot 4.7.2; commit `7973729` |
| Bảng màu | palette_v3, 32 màu; `art/reference/palette.gpl` và `.png` | Đã duyệt (A0, 28/10/2026) | — | Mọi sprite và giao diện | A0 Android, Realme RMX3760, Godot 4.7.2; commit `7973729` |
| Chiều cao nhân vật người | 96 px, khung 128×128, chân cách đáy 8 px | Đã duyệt (A0, 28/10/2026) | — | Sprite người, hộp va chạm | A0 Android, Realme RMX3760, Godot 4.7.2; commit `7973729` |
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
- **Tài liệu/đặc tả liên quan:** `01_art_bible.md`, `02_asset_list.md`, `03_prompts.md`, `05_log.md`, `09_animation_spec.md`, P1–P17 và các bản mockup về sau. Thông số hiển thị, nhân vật người và di chuyển được chốt riêng tại A0 bên dưới; kích thước boss, thú, tile và số khung hoạt ảnh chưa được duyệt theo A0. Mọi bố cục/hoạt ảnh phải soát lại theo thông số đã chốt.

## Giao diện

| Thông số | Giá trị | Trạng thái | Chốt khi | Ảnh hưởng tới | Nguồn |
|---|---|---|---|---|---|
| Lề cụm điều khiển trong trận | Ít nhất 24 px logic tới mép viewport | Đã duyệt (A0, 28/10/2026) | — | HUD trong trận; safe area tai thỏ vẫn phải soát khi dựng mockup | A0 Android, Realme RMX3760, Godot 4.7.2; commit `7973729` |
| Cỡ chạm nhỏ nhất | 20×20 | Tạm thời | Thử trên máy thật | Mọi nút | `06_screens.md` |
| Nút trong trận | Di chuyển d=84; CHÉM 1,4d=117,6; kỹ năng 0,7d=58,8; bình/đổi mục tiêu 0,65d=54,6 px logic | Đã duyệt (A0, 28/10/2026) | — | SCR-05, SCR-06, SCR-07 | A0 Android, Realme RMX3760, Godot 4.7.2; commit `7973729` |
| Cỡ chữ tối thiểu | 8 (phụ), 10 (chính) | Tạm thời | Khi chọn font | Mọi màn | `06_screens.md` |

## Di chuyển và bản đồ

| Thông số | Giá trị | Trạng thái | Chốt khi | Ảnh hưởng tới | Nguồn |
|---|---|---|---|---|---|
| Hộp va chạm nhân vật (`PLAYER_BOX`) | 24×88 px | Đã duyệt (A0, 28/10/2026) | — | Bố cục bản đồ, va chạm | A0 Android, Realme RMX3760, Godot 4.7.2; commit `7973729` |
| Tốc độ chạy (`RUN_SPEED`) | 200 px/s, đạt ngay khi bấm hướng trong Kiểu cổ điển | Đã duyệt (A0, 28/10/2026) | — | Bố cục, nhịp chơi | A0 Android, Realme RMX3760, Godot 4.7.2; commit `7973729` |
| Độ cao nhảy (`JUMP_HEIGHT`) | 96 px (= chiều cao nhân vật); 3 ô theo tile 32 px tạm thời | Đã duyệt (A0, 28/10/2026) | — | Mọi bố cục bản đồ | A0 Android, Realme RMX3760, Godot 4.7.2; commit `7973729` |
| Khe rộng nhất | Chưa chốt; mốc 3 ô (96 px) cũ chỉ là đề xuất. Tầm ngang một nhảy: 152 px khi đi hướng riêng, 121,6 px khi giữ vùng chéo | Tạm thời | Thử khe/bục với biên an toàn, cả nhảy chéo và khinh công; tầm lý thuyết không phải bề rộng khe an toàn | Mọi bố cục bản đồ | `08_map_layout.md`, mục 1 |
| Tốc độ thú cưỡi | Ngựa ×1,6; trâu ×1,2, nhảy 1,5 ô; voi không nhảy | Tạm thời | Chơi thử | Bản đồ có thú cưỡi, boss Tiên Du | `08_map_layout.md` |
| Kích thước bản đồ | Làng 40–60 ô, đánh quái 80–120 ô, đấu trường 30–40 ô, ải 40 ô | Tạm thời | Khi duyệt từng bố cục | Bố cục | `08_map_layout.md` |

## Bộ thông số đã duyệt tại A0 trên Android

Người dùng đã chơi và chấp nhận bộ mặc định tại **commit main `7973729`** trên
**Realme RMX3760 (Android, màn hình 1600×720), Godot 4.7.2**, ngày 28/10/2026.
**Kiểu cổ điển bật** là chuẩn cho game thật. Kết quả này thay trạng thái chờ Android
của bộ thử PC trước đây; các mục ngoài phạm vi A0 giữ trạng thái riêng.

| Thông số/quy tắc | Giá trị đã chốt | Trạng thái |
|---|---|---|
| `Stretch và lọc ảnh` | canvas_items; aspect expand; scale fractional; nearest. 1600×720 ứng với viewport 1200×540 và phóng 4/3 | Đã duyệt (A0, 28/10/2026) |
| `Hiển thị Android` | Fullscreen + immersive, ẩn thanh trạng thái và thanh điều hướng | Đã duyệt (A0, 28/10/2026) |
| `CLASSIC_CONTROLS` | Bật; chuẩn di chuyển cho game thật | Đã duyệt (A0, 28/10/2026) |
| `STOP_TIME` | 0,08 s, buông hướng thì hãm về 0 | Đã duyệt (A0, 28/10/2026) |
| `TURN_TIME` | 0,05 s; khung đầu chỉ đổi mặt, đứng trong nhịp quay rồi chạy; chạm nhẹ chỉ quay mặt | Đã duyệt (A0, 28/10/2026) |
| `Điều khiển trên không` | Đổi hướng ngay; hướng riêng = RUN_SPEED = 200 px/s; vùng chéo = 0,8 × RUN_SPEED = 160 px/s | Đã duyệt (A0, 28/10/2026) |
| `TIME_TO_APEX` | 0,38 s; nhảy 96 px. Lên/xuống dùng cùng trọng lực, không treo đỉnh; cùng cao độ có thời gian bằng nhau (sai số một khung mô phỏng) | Đã duyệt (A0, 28/10/2026) |
| `GRAVITY` | 2 × 96 / 0,38² ≈ 1329,64 px/s² | Đã duyệt (A0, 28/10/2026) |
| `JUMP_SPEED` | −2 × 96 / 0,38 ≈ −505,26 px/s (trục y dương xuống) | Đã duyệt (A0, 28/10/2026) |
| `FALL_SPEED_MAX` | 2 × \|JUMP_SPEED\| ≈ 1010,53 px/s | Đã duyệt (A0, 28/10/2026) |
| `COYOTE_TIME; JUMP_BUFFER` | 0,10 s; 0,12 s | Đã duyệt (A0, 28/10/2026) |
| `HOLD_AUTO_JUMP; VARIABLE_JUMP` | Giữ để nhảy lại: bật. Giữ lâu nhảy cao: tắt | Đã duyệt (A0, 28/10/2026) |
| `AIR_JUMP_ENABLED; cửa sổ khinh công` | Bật. Khi còn đi lên: 0 < \|vy\| ≤ 0,3 × \|JUMP_SPEED\|; phải nhả rồi bấm mới, giữ liên tục không tính | Đã duyệt (A0, 28/10/2026) |
| `Cú bật khinh công` | Vận tốc = 0,7 × JUMP_SPEED ≈ −353,68 px/s; tối đa 1 lần/cú nhảy, reset khi chạm đất | Đã duyệt (A0, 28/10/2026) |
| `APEX_FLIP_TIME` | Mỗi cú nhảy và cú khinh công lộn 360° theo hướng mặt, trong 0,2 s tại vùng đỉnh; chỉ sprite, không xoay hitbox | Đã duyệt (A0, 28/10/2026) |
| `ATTACK_DURATION; HIT_START–HIT_END` | 0,30 s; cửa sổ trúng 0,10–0,20 s | Đã duyệt (A0, 28/10/2026) |
| `ATTACK_COOLDOWN` | 0,15 s sau khi hết động tác | Đã duyệt (A0, 28/10/2026) |
| `SLASH_BOX; SLASH_OFFSET` | 56×56 px; (34, −52) px từ chân, x theo hướng nhìn | Đã duyệt (A0, 28/10/2026) |
| `CAMERA_DEAD_ZONE` | (100, 60) px: nửa rộng × nửa cao; toàn vùng chết 200×120 px | Đã duyệt (A0, 28/10/2026) |
| `CAMERA_LOOK_AHEAD; CAMERA_RESPONSE` | 100 px; 5 /s | Đã duyệt (A0, 28/10/2026) |
| `FAKE_MOTION_ENABLED` | Bật trong A0; game thật dùng dữ liệu ghép từng frame, thêm khung riêng khi cần, thay xoay nguyên sprite tạm | Đã duyệt (A0, 28/10/2026) |
| `D-pad` | 3 nút nhìn thấy ←, →, ↑ nhảy; 2 vùng chéo vô hình sát hai bên ↑. Ưu tiên ↑ > chéo > hướng; chạm chéo làm sáng ↑ và nút cùng phía | Đã duyệt (A0, 28/10/2026) |
| `Kích thước d-pad` | d=84 px logic; lệch hai nút dưới 2,2d; ↑ cao hơn 1,35d và căn giữa; vùng chéo rộng 0,9d, cao d | Đã duyệt (A0, 28/10/2026) |
| `Lề và chữ nút` | Cách mép ít nhất 24 px logic; chữ/mũi tên ≥22 px logic, neo viewport thật khi resize | Đã duyệt (A0, 28/10/2026) |
| `Cụm phải` | CHÉM tròn 1,4d ở góc dưới phải; đổi mục tiêu phía trên; bình máu trên-trái và bình nội lực bên trái CHÉM | Đã duyệt (A0, 28/10/2026) |
| `Hàng kỹ năng` | 5 ô vuông giữa đáy, cạnh 0,7d, cách nhau 6 px; 5 ô chiêu; người chơi chọn 5 trong 8 chiêu chủ động/hỗ trợ của phái (kể cả tuyệt kỹ) để xếp vào ô; chiêu nội tại tự có hiệu lực, không cần ô | Đã duyệt (A0, 28/10/2026) |
| `HUD trên` | Vòng cấp, máu đỏ/nội lực xanh ở trái; menu và bản đồ nhỏ 120×80 ở phải | Đã duyệt (A0, 28/10/2026) |

Nguồn: `prototype/config/tuning.gd`, `prototype/project.godot` và README xuất Android
ở commit `7973729`, cùng xác nhận nghiệm thu của người dùng. Bảng hiển thị và di
chuyển phía trên ghi riêng độ phân giải, nhân vật, RUN_SPEED, JUMP_HEIGHT và PLAYER_BOX.

**Giới hạn bố cục chưa chốt:**

| Hạng mục | Căn cứ sau A0 | Trạng thái / việc còn lại |
|---|---|---|
| Bậc cao nhất dùng an toàn | Trần vật lý một nhảy 96 px; theo tile 32 px tạm thời là 3 ô. Bậc 2 ô cũ là mức chừa dư, không phải trần nhảy | Tạm thời — cần thử độ rộng bục, khoảng chạy ngang, mép va chạm và độ dễ thao tác; chưa duyệt mọi bậc 3 ô |
| Độ cao có khinh công | Bật thêm 47,04 px; tổng lý thuyết 134,4 đến gần 143,04 px tùy thời điểm bấm, khoảng 4,2–4,47 ô | Giá trị suy ra từ cơ chế đã duyệt; độ cao bục an toàn cần thử từng bố cục |
| Khe rộng nhất | Tầm ngang cùng cao độ một nhảy 200 × 2 × 0,38 = 152 px; vùng chéo 160 × 2 × 0,38 = 121,6 px | Tạm thời — chưa suy ra khe an toàn từ tầm tối đa; cần biên an toàn, kiểm tra khinh công và điều khiển thực tế |

**Kiểu cũ:** có ACCELERATION=900 px/s², nhảy 80 px và xoay chậm khi nhảy chéo,
chỉ giữ trong `prototype/` để so sánh, **không dùng cho game thật**. Đây không phải
bộ thông số A0 đã duyệt cho sản phẩm. `prototype/` giữ làm tham khảo, không chép mã
sang `co_lau_game`; việc qua A0 chưa mở khóa code game thật trước Mốc A.

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
