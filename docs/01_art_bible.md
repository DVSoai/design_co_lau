# Art bible — Cờ Lau Khởi Nghĩa

Tài liệu này quy định mọi hình ảnh trong game trông như thế nào. Khi có mâu thuẫn giữa tài liệu này và một prompt, tài liệu này thắng.

## Game là gì

Cờ Lau Khởi Nghĩa là game nhập vai hành động 2D cuộn ngang trên điện thoại Android, kể chuyện Đinh Bộ Lĩnh dẹp loạn 12 sứ quân ở Bắc Bộ thế kỷ 10 (khoảng năm 944 đến 968). Người chơi chỉ điều khiển Đinh Bộ Lĩnh, chọn một trong hai phái: Đao (cận chiến, gây choáng) hoặc Cung (tầm xa, ghim chân). Ngoại hình nhân vật chính chỉ đổi theo vũ khí và quần áo đang mặc. Giọng game là dã sử hiện thực: không có quái vật thần thoại, không có phép thuật lấp lánh; quái là thú vật có thật ở Bắc Bộ hoặc con người cùng thời.

## Phong cách

**Đã duyệt P0 (28/10/2026): Pixel bán hiện đại.** Pixel art 2D cuộn ngang, dáng người bán hiện thực khoảng **4 đầu**, viền tối rõ, **32 màu**, tô bóng **3 tông** với điểm sáng mềm, ánh sáng từ góc trên bên trái. Ưu tiên hình khối dễ đọc trên điện thoại; bối cảnh Bắc Bộ thế kỷ 10, núi đá vôi, ruộng lúa, thành đất, nhà tranh/ngói đất nung đơn giản, cờ lau trắng. Không dùng hiệu ứng năng lượng phát sáng; hiệu ứng chiến đấu dùng bụi, tia lửa và vệt gió vật lý.

Khối STYLE dùng cho mọi prompt (dán nguyên văn):

```
Style: 2D pixel art for a side-scrolling mobile action RPG, semi-realistic proportions about 4 heads tall, clean dark outline, 32-color palette, 3-tone shading with soft highlights, readable silhouettes, light source from top-left. Setting: northern Vietnam in the 10th century: limestone karst, rice fields, earthen ramparts, thatched or simple clay-tiled roofs, white reed-plume banners.
```

Khối AVOID dùng cho mọi prompt (dán nguyên văn):

```
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

**Quyết định P0:** phương án B trong bảng so sánh là *pixel bán hiện đại*, không phải STYLE-B vẽ tay trong khuôn P0 lịch sử của `03_prompts.md`. Xem ngoại lệ và prompt đã dùng trong `05_log.md`. Không tự thay STYLE đã duyệt bằng STYLE-B vẽ tay.

## Bảng màu chính

**Đã duyệt palette_v3**, xác nhận tại A0 ngày 28/10/2026: bảng 32 màu trong `art/reference/palette.gpl` và `palette.png`. 16 màu dưới đây là khung xương tham khảo. Khi chỉnh tay sprite, mọi màu phải quy về bảng này hoặc các sắc độ đã thêm vào bảng.

| Tên | Mã | Dùng cho |
|---|---|---|
| Đen viền | #1B1A1F | Nét viền, bóng sâu nhất |
| Xám đá vôi tối | #4A4E57 | Núi đá vôi phần bóng |
| Xám đá vôi | #8A8F98 | Núi đá vôi, đá |
| Xám sáng | #C9CCD1 | Sương, mây, đá phần sáng |
| Nâu đất tối | #4B3221 | Đất, gỗ phần bóng |
| Nâu đất | #7D5537 | Đất, gỗ, da |
| Vàng rơm | #D9B25F | Rơm, tre khô, mái tranh |
| Kem vải | #EFE2C2 | Vải mộc, áo cánh |
| Xanh lúa tối | #2F5A2E | Cây, lá phần bóng |
| Xanh lúa | #5E9441 | Lúa, cỏ, lá |
| Xanh mạ | #A8C96A | Lúa non, phần sáng của lá |
| Chàm | #2D3E6B | Vải nhuộm chàm, áo lính |
| Xanh nước | #4F8FA6 | Sông, đầm |
| Da người | #D99A6C | Da (thêm một sắc tối #A86A45) |
| Đỏ chiến | #B23A2E | Máu, lửa, cờ chiến, chỉ dùng trong chiến trận |
| Trắng bông lau | #F4F1E8 | Bông lau, cờ lau |


## Quy trình nhân vật chính: ghép bộ phận (28/10/2026)

Người dùng **không thuê họa sĩ**. Nhân vật chính dùng quy trình
**imagegen → snap_pixel → sửa pixel bằng script → kiểm tra bằng check_sprite**,
rồi **Claude/người dùng duyệt từng bộ phận dựa trên script kiểm tra và bằng mắt**.
Quy trình này thay quy định cũ loại nhân vật chính khỏi pipeline và yêu cầu chỉnh
tay bằng công cụ pixel art/thuê họa sĩ. Quái, NPC, tile và vật phẩm tiếp tục qua
pipeline tạo ảnh/chuẩn hóa, báo cáo file thật và duyệt mỹ thuật tương ứng.

- **`chr_dbl_parts`:** bộ bộ phận theo tỉ lệ nhân vật cao 96 px, không phải mỗi mảnh đều cao 96 px. Gồm đầu kèm tóc, thân; cánh tay trên/dưới gần và xa; đùi/cẳng chân gần và xa; bàn tay gần/xa và vũ khí. Mỗi mảnh có điểm khớp trong tọa độ pixel cục bộ, điểm gắn với mảnh cha và vùng vẽ bù phía bị che để khi xoay không thủng vai, khuỷu, hông, gối hoặc cổ tay.
- **`chr_dbl_anim_*`:** dữ liệu ghép theo từng khung: id bộ phận, vị trí, góc, thứ tự lớp; kèm thời lượng và sự kiện hit/spawn theo `09_animation_spec.md`. Dữ liệu chuyển pose từng khung, không phải chỉ xoay toàn bộ ảnh đứng. Lộn ở đỉnh/chiêu lớn được bổ sung khung vẽ riêng nếu ghép bộ phận chưa đủ rõ.
- **`chr_dbl_t1`…`chr_dbl_t7`:** bộ phận thay thế áo, quần, vũ khí; giữ chung id khớp, tỉ lệ và dữ liệu động tác. Không vẽ lại toàn bộ chuỗi hoạt ảnh cho từng bậc trang bị.
- **Duyệt:** so script (palette_v3, kích thước/tỉ lệ, khớp, đường chân, độ kín khi ghép) và xem từng bộ phận cùng các pose ghép thật ở 1×/phóng NEAREST. Chạy kiểm tra kỹ thuật không thay duyệt mỹ thuật; không ghi đè ảnh đã duyệt. Lưu prompt, ảnh nguồn, script sửa, dữ liệu khớp/khung và báo cáo trong nhật ký.
- **Ảnh cũ:** `art/sprites/characters/chr_dbl_idle_side_96.png` tiếp tục là PLACEHOLDER, không tự được duyệt lại; ảnh gốc `art/reference/ref_dinh_bo_linh.png` vẫn là tham chiếu. Lát cắt mẫu Giai đoạn 1 dùng bộ phận mới đã duyệt để thay placeholder, xem `02_asset_list.md`.

**Phạm vi công cụ hiện có:** `snap_pixel.py` và `check_sprite.py` hiện kiểm một
nhân vật nguyên khung 128×128, silhouette 96 px, chân cách đáy 8 px, nền xanh và
bản ×4. Chúng **chưa có chế độ kiểm mảnh/khớp/dữ liệu hoạt ảnh**. Khi sản xuất bộ
phận cần bổ sung chế độ phù hợp hoặc báo cáo kiểm riêng cho từng mảnh, giữ kiểm
sprite ghép chuẩn bằng check_sprite; không đổi kích thước từng mảnh thành 96 px
chỉ để ép qua kiểm tra. Việc cập nhật tài liệu lần này không sửa công cụ hay tạo
asset, không tuyên bố bộ phận đã qua kiểm tra.

### Pipeline bộ phận bậc 0 đang làm

`tools/cut_parts.py` co mọi mảnh theo **một s=96/846** cho x/y, dùng trung vị
ô nguồn, giữ aspect và đo lại khớp theo hình. Không ép vào ô greybox: cấu hình
art ở parts.json, greybox ở parts_greybox.json. Viền chỉ ở đường bao dáng đứng,
không bôi vào mặt cắt/vùng bù khớp. Đầu hiện áp nguyên ma trận người dùng gửi: **đầu do Claude vẽ tay từng pixel**.
Tay trên/cẳng tay có ngoại lệ rút trục dài còn 60%; da dùng skin, áo dùng fabric,
ngoài quần không dùng pants trừ ánh tóc #59443E của ma trận đầu. Báo cáo và script nguyên văn tại
`reports/g1_parts_art_report.md`; vẫn đang làm, chưa duyệt.

### Bổ sung vật liệu bộ phận 29/10/2026 (chưa duyệt mỹ thuật)

Riêng vũ khí `dao`/`bow` được dùng thêm limestone của palette_v3. Lưỡi đao lấy
#A5B8B0 làm chính, #718B87 bóng, #D9DDD0 sáng, viền #17151A; cán/vỏ vẫn belt.
Cung gỗ belt và dây sáng #D9DDD0. Đùi của quần ngang gối chỉ pants (và nét
outline); skin từ gối xuống. Kiểm nhóm màu theo từng mảnh, không mở limestone
cho da/áo/quần. Xem [báo cáo](reports/g1_parts_polish_report.md).

## Kích thước

**Đã duyệt (A0, 28/10/2026):** khung thiết kế **960×540**, nhân vật người **96 px trong khung 128×128**. Dùng `canvas_items`, aspect `expand`, scale `fractional`, lọc nearest; viewport thực rộng 960–1200 px logic theo tỉ lệ màn hình (1600×720 → 1200×540, hệ số 4/3). Android fullscreen + immersive. Kết quả trên Realme RMX3760, Godot 4.7.2, commit `7973729`; không ép mọi thiết bị phóng nguyên ×2. Các kích thước boss, thú, tile, icon và nền bên dưới vẫn **Tạm thời**; A0 không duyệt sprite mỹ thuật thành phẩm.

- **Nhân vật người:** cao khoảng 96 điểm ảnh, đặt trong khung 128×128, chân cách đáy khung 8 điểm ảnh. Mọi khung động tác dùng chung một đường chân.
- **Boss người:** cao khoảng 132 điểm ảnh, khung 192×192. Boss cưỡi ngựa hay voi dùng khung 192×160.
- **Quái thú nhỏ** (chuột, rắn, cò): khung 64×64. **Quái thú lớn** (hổ, cá sấu, gấu, voi): khung 128×96.
- **Thú cưỡi:** khung 128×96, có điểm neo cho nhân vật ngồi.
- **Tile:** 32×32. **Biểu tượng vật phẩm:** 32×32 trong game, vẽ bản gốc 64×64.
- **Chân dung hội thoại:** 128×128, chỉ đầu và vai.
- **Cảnh nền:** mỗi lớp rộng 1920, cao 540 để lặp lại khi cuộn.

### Sản xuất và kiểm bộ phận nhân vật chính

1. Dùng imagegen theo ảnh tham chiếu và STYLE/AVOID đã duyệt để tạo bộ phận, bao gồm phần vẽ bù bị che; giữ nhất quán lưới pixel và tỉ lệ nhân vật ghép cao 96 px.
2. Chuẩn hóa lưới/màu bằng snap_pixel theo quy cách phù hợp bộ phận; script sửa viền, pixel lạc, phần che, nền và vùng nối. Giữ dữ liệu ảnh nguồn; không co một lưới nghệ thuật sai thành đúng 96 px để giả đạt chuẩn.
3. Ghi id mảnh, khớp, mảnh cha, vị trí gốc và lớp gần/xa. Dựng ảnh ghép kiểm đứng chuẩn trong khung 128×128, mốc chân cách đáy 8 px; so tỉ lệ với ảnh tham chiếu.
4. Kiểm file thật bằng check_sprite và báo cáo bổ sung cho mảnh/khớp: palette, kích thước, điểm nối, độ kín ở nhiều góc, thứ tự lớp và dữ liệu từng frame. Công cụ nguyên khung hiện có chỉ kiểm pose chuẩn đáp ứng hợp đồng của nó; các pose co chân/lộn phải có phép kiểm phù hợp, không được ép silhouette mọi frame cao đúng 96 px.
5. Claude/người dùng duyệt từng bộ phận bằng báo cáo script và bằng mắt, rồi duyệt các chuỗi ghép. Thêm khung riêng cho lộn/chiêu lớn khi cần; không bắt buộc Aseprite, sửa tay hoặc thuê họa sĩ.
6. Dựng lát cắt Đào Úc + nhân vật ghép bộ phận + một quái trong prototype để duyệt cuối Giai đoạn 1. Chỉ mở Giai đoạn 2 sau khi duyệt đủ giai đoạn trước, bao gồm lát cắt này.

Ảnh ×4 chỉ tạo từ ảnh 1× thật bằng `Image.resize(..., Image.Resampling.NEAREST)`;
bảng so sánh phải ghép bằng script từ file thật, không tạo báo cáo bằng imagegen.

## Nhân vật vẽ theo bộ phận

Bộ phận có điểm khớp cho đầu/cổ, thân/vai/hông, cánh tay trên–dưới gần/xa,
đùi–cẳng chân gần/xa, bàn tay và tay cầm vũ khí. Ghi rõ hệ tọa độ cục bộ,
khớp cha–con và lớp vẽ ở mỗi frame; phần bị che vẫn phải vẽ đủ để ghép khi đổi góc.
Các bậc trang bị chỉ thay áo, quần, vũ khí tương ứng, cùng hệ khớp và cùng dữ liệu
động tác. Chiều dài cụ thể từng mảnh và bộ pose phải được duyệt khi dựng
`chr_dbl_parts`, không tự coi ảnh chia ô/chia vùng chữ nhật cũ là bộ phần đã duyệt.

## Trang phục thế kỷ 10

- **Dân thường và lính:** áo cánh ngắn tay hoặc dài tay, khố hoặc quần vải ngắn, chân đất hoặc dép cỏ, xà cạp quấn chân. **Nón lá chỉ dành cho dân làng và một số thổ phỉ; lính các sứ quân dùng khăn chít đầu hoặc mũ trụ đơn giản và mang màu cờ của sứ quân để phân biệt phe.**
- **Tướng:** giáp da, giáp vảy sắt hoặc đồng, mũ trụ đơn giản tròn, áo choàng ngắn.
- **Tóc:** **Đinh Bộ Lĩnh búi tóc nhỏ trên đỉnh đầu**, không dùng tóc dài buộc đuôi bay. Nhân vật khác có thể búi tóc hoặc dùng khăn chít đầu che tóc.
- **Vũ khí:** đao lưỡi rộng một cạnh, giáo, nỏ, cung tre hoặc cung sừng, khiên mây tròn.
- **Kiến trúc:** nhà gỗ sàn mái tranh, mái ngói đất nung đơn giản, thành đất đắp lũy, cổng gỗ, chòi canh, chùa gỗ nhỏ. Kinh đô Hoa Lư là thành đất nối các dãy núi đá vôi.
- **Cấm:** áo dài, nón quai thao, long bào, trang phục võ sĩ và chiến binh bí mật Nhật Bản, kiếm katana, kiến trúc mái cong kiểu cung đình Trung Hoa.

Chi tiết ngoại hình cụ thể của từng nhân vật là mở rộng cho game, vì sử không ghi.

## Biểu tượng bông lau

Cờ lau trắng là biểu tượng thị giác của cả game: Đinh Bộ Lĩnh thuở nhỏ lấy bông lau làm cờ tập trận. Về sau cờ thành nền vàng có hình bông lau. Bông lau chỉ xuất hiện trên trang bị của nhân vật chính ở bậc 7, trên cờ của quân Đinh và trong khung giao diện, để giữ giá trị của biểu tượng.

## Màu cờ các thế lực

Màu cờ là mở rộng cho game, đặt sao cho hai sứ quân đánh liền nhau không trùng màu. Lính và boss mỗi thế lực mặc giáp vải hoặc mang cờ đúng màu này.

| Thế lực | Màu | Mã |
|---|---|---|
| Quân Đinh Bộ Lĩnh | Trắng bông lau, sau là vàng | #F4F1E8, #D9A520 |
| Hậu Ngô | Đỏ nâu | #8C3B2A |
| Hải tặc | Đen | #2A2A2E |
| Phạm Bạch Hổ | Trắng và xanh biển | #E8EEF2, #2F6B8F |
| Đỗ Cảnh Thạc | Nâu đất | #6E4B2A |
| Nguyễn Siêu | Xanh nước | #3E9AB0 |
| Lã Đường | Cam | #D9782B |
| Lý Khuê | Tím | #6B4A8C |
| Nguyễn Thủ Tiệp | Đỏ tươi | #D33B3B |
| Nguyễn Khoan | Xanh rêu | #5C6B35 |
| Kiều Công Hãn | Xanh lá đậm | #2E6B3F |
| Kiều Thuận | Xanh lam | #2E4FA3 |

## Giao diện

Chất liệu khung giao diện là gỗ sơn mài tối màu, đan tre và viền đồng, có họa tiết bông lau kín đáo. Không có chữ trong ảnh. Bố cục HUD trong trận theo chuẩn A0 ở `06_screens.md`: vòng cấp, máu/nội lực trên trái; menu và bản đồ nhỏ trên phải; d-pad 3 nút với hai vùng chéo vô hình dưới trái; cụm CHÉM/đổi mục tiêu/bình dưới phải; 5 ô kỹ năng giữa đáy. Hình nút thành phẩm sẽ vẽ riêng theo phong cách Việt (có thể tham khảo hoa văn trống đồng), không dùng ảnh hay biểu tượng game khác. Các màn còn lại tra Phần 5 `GDD.md` và đặc tả `06_screens.md`, tiếp tục duyệt ở Mốc A.

Ba loại tiền có biểu tượng riêng: tiền đồng (đồng xu đồng có lỗ vuông), ngân lượng (thỏi bạc), ngân phiếu (tờ giấy đổi bạc có dấu son).

## Thứ tự lớp trong trận (chốt từ A0)

Hiệu ứng đòn đánh (vệt chém, tia lửa trúng đòn) và số sát thương **luôn vẽ đè
lên nhân vật, hình nộm và quái**. Khi dựng scene hoặc sprite sheet phải giữ lớp
hiệu ứng/số cao hơn lớp thân, không để thứ tự node khiến quái che mất phản hồi
trúng đòn. Lộn người chỉ đổi hình hoạt ảnh, không xoay hitbox hoặc đổi lớp vẽ.
