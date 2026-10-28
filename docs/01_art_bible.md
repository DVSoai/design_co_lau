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
Avoid: Japanese ninja or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

**Quyết định P0:** phương án B trong bảng so sánh là *pixel bán hiện đại*, không phải STYLE-B vẽ tay trong khuôn P0 lịch sử của `03_prompts.md`. Xem ngoại lệ và prompt đã dùng trong `05_log.md`. Không tự thay STYLE đã duyệt bằng STYLE-B vẽ tay.

## Bảng màu chính

Bảng màu cuối cùng có 32 màu; 16 màu dưới đây là khung xương. Khi chỉnh tay sprite, mọi màu phải quy về bảng này hoặc các sắc độ đã thêm vào bảng.

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


## Quy định nguồn tạo sprite theo loại asset (28/10/2026)

- Quy trình **$imagegen + `tools/snap_pixel.py` chỉ áp dụng cho quái, NPC, tile và vật phẩm**. Các ảnh này vẫn phải qua kiểm tra kỹ thuật, tự soát mỹ thuật và người dùng duyệt.
- **Sprite nhân vật chính Đinh Bộ Lĩnh không được coi là thành phẩm từ $imagegen + snap_pixel**. Sprite nhân vật chính cần được **sửa tay bằng công cụ pixel art (ví dụ Aseprite) hoặc thuê họa sĩ vẽ**, rồi kiểm tra palette, kích thước, đường chân và hoạt ảnh trước khi duyệt.
- `art/sprites/characters/chr_dbl_idle_side_96.png` hiện là **PLACEHOLDER đạt kỹ thuật nhưng chưa đạt mỹ thuật**, chỉ dùng tạm khi kiểm thử nguyên mẫu; không thay ảnh tham chiếu `art/reference/ref_dinh_bo_linh.png`, không đưa vào `art/approved/`.
- Quy định này thay thế hướng dẫn pipeline tự động trước đây **đối với nhân vật chính**; các quy định chung về kiểm tra file thật và báo cáo script vẫn giữ nguyên.

## Kích thước

Game dựng ở độ phân giải gốc **960×540** (16:9), phóng **×2** lên **1920×1080** bằng lọc nearest. Các thông số dưới đây **Tạm thời**, chờ kiểm tra mẫu chuẩn trên thiết bị thật.

- **Nhân vật người:** cao khoảng 96 điểm ảnh, đặt trong khung 128×128, chân cách đáy khung 8 điểm ảnh. Mọi khung động tác dùng chung một đường chân.
- **Boss người:** cao khoảng 132 điểm ảnh, khung 192×192. Boss cưỡi ngựa hay voi dùng khung 192×160.
- **Quái thú nhỏ** (chuột, rắn, cò): khung 64×64. **Quái thú lớn** (hổ, cá sấu, gấu, voi): khung 128×96.
- **Thú cưỡi:** khung 128×96, có điểm neo cho nhân vật ngồi.
- **Tile:** 32×32. **Biểu tượng vật phẩm:** 32×32 trong game, vẽ bản gốc 64×64.
- **Chân dung hội thoại:** 128×128, chỉ đầu và vai.
- **Cảnh nền:** mỗi lớp rộng 1920, cao 540 để lặp lại khi cuộn.

### Quy trình sprite (tạm thời, áp dụng cho `chr_dbl_idle_side_96`)

1. Dùng `$imagegen` **chỉ để vẽ ảnh concept** nhân vật pixel art cỡ lớn, nền xanh `#00FF00`, khối pixel rõ; concept không phải sprite được duyệt.
2. Chạy `tools/snap_pixel.py`: ước lượng chu kỳ ô pixel theo hai trục bằng tự tương quan/tần số của chênh lệch pixel kề nhau; lấy trung vị màu mỗi ô (bỏ ô có trên 50% nền xanh); ép màu về `art/reference/palette.gpl` theo khoảng cách có trọng số độ sáng; co giãn nearest đến chiều cao **96 px**; căn giữa trên canvas **128×128**, chân cách đáy **8 px**.
3. Sửa tay trong Aseprite: viền, mắt, tay, các pixel lẻ. **Chưa thực hiện bước này trong bản thử tự động.**
4. Chạy `tools/check_sprite.py` trên PNG thật: kích thước, bbox, chiều cao, khoảng cách đáy, đếm pixel từng màu, 0 pixel ngoài palette (trừ nền), nền đúng `#00FF00`; xác nhận ảnh ×4 được tạo bằng `Image.resize(..., Image.Resampling.NEAREST)` từ bản 1×.

Không dùng imagegen để dựng báo cáo, bảng số liệu, ảnh so sánh hoặc bản ×4. Chỉ kiểm tra bằng script trên file thật.

## Nhân vật vẽ theo bộ phận

Đinh Bộ Lĩnh vẽ thành bốn lớp chồng lên nhau: đầu (mặt và tóc), thân (áo và tay), chân (quần và giày), vũ khí. Mỗi bộ trang bị chỉ thay lớp tương ứng. Vì vậy mọi bậc trang bị phải giữ đúng dáng người, độ dài tay chân và vị trí khớp của ảnh gốc.

## Trang phục thế kỷ 10

- **Dân thường và lính:** áo cánh ngắn tay hoặc dài tay, khố hoặc quần vải ngắn, chân đất hoặc dép cỏ, xà cạp quấn chân. **Nón lá chỉ dành cho dân làng và một số thổ phỉ; lính các sứ quân dùng khăn chít đầu hoặc mũ trụ đơn giản và mang màu cờ của sứ quân để phân biệt phe.**
- **Tướng:** giáp da, giáp vảy sắt hoặc đồng, mũ trụ đơn giản tròn, áo choàng ngắn.
- **Tóc:** **Đinh Bộ Lĩnh búi tóc nhỏ trên đỉnh đầu**, không dùng tóc dài buộc đuôi bay. Nhân vật khác có thể búi tóc hoặc dùng khăn chít đầu che tóc.
- **Vũ khí:** đao lưỡi rộng một cạnh, giáo, nỏ, cung tre hoặc cung sừng, khiên mây tròn.
- **Kiến trúc:** nhà gỗ sàn mái tranh, mái ngói đất nung đơn giản, thành đất đắp lũy, cổng gỗ, chòi canh, chùa gỗ nhỏ. Kinh đô Hoa Lư là thành đất nối các dãy núi đá vôi.
- **Cấm:** áo dài, nón quai thao, long bào, đồ samurai và ninja, kiếm katana, kiến trúc mái cong kiểu cung đình Trung Hoa.

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

Chất liệu khung giao diện là gỗ sơn mài tối màu, đan tre và viền đồng, có họa tiết bông lau kín đáo. Không có chữ trong ảnh. Bố cục các màn đã chốt ở Phần 5 của `GDD.md`: màn chơi (máu, khí ở góc trên trái; bản đồ nhỏ và nút menu, túi đồ, Nạp ở góc trên phải; cần điều khiển góc dưới trái; nút đánh và 6 ô chiêu góc dưới phải), menu nhân vật 7 thẻ, màn hội thoại, cửa hàng, thợ rèn, nạp và cửa hàng ngân phiếu, chọn ô nhân vật.

Ba loại tiền có biểu tượng riêng: tiền đồng (đồng xu đồng có lỗ vuông), ngân lượng (thỏi bạc), ngân phiếu (tờ giấy đổi bạc có dấu son).
