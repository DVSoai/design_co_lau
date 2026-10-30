# Art bible — Cờ Lau Khởi Nghĩa

Tài liệu này quy định mọi hình ảnh trong game trông như thế nào. Khi có mâu thuẫn giữa tài liệu này và một prompt, tài liệu này thắng.

## Game là gì

Cờ Lau Khởi Nghĩa là game nhập vai hành động 2D cuộn ngang trên điện thoại Android, kể chuyện Đinh Bộ Lĩnh dẹp loạn 12 sứ quân ở Bắc Bộ thế kỷ 10 (khoảng năm 944 đến 968). Người chơi chỉ điều khiển Đinh Bộ Lĩnh, chọn một trong hai phái: Kiếm (cận chiến, gây choáng) hoặc Cung (tầm xa, ghim chân). Ngoại hình nhân vật chính chỉ đổi theo vũ khí và quần áo đang mặc. Giọng game là dã sử hiện thực: không có quái vật thần thoại, không có phép thuật lấp lánh; quái là thú vật có thật ở Bắc Bộ hoặc con người cùng thời.

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

**Cập nhật 30/10/2026:** nhân vật người (Đinh Bộ Lĩnh, NPC, quái người, boss người) chuyển sang **STYLE-V2** — xem mục "Nhân vật chính — chốt 30/10/2026" cuối file. Bản đồ, vật thể, giao diện vẫn theo STYLE pixel ở trên.

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

Riêng vũ khí `dao`/`bow` được dùng thêm limestone của palette_v3. Lưỡi kiếm lấy
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
- **Vũ khí:** kiếm thẳng hai lưỡi cho phái Kiếm; đao lưỡi rộng một cạnh chỉ là vũ khí lính địch/đạo cụ, cùng giáo, nỏ, cung tre hoặc cung sừng, khiên mây tròn.
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

Chất liệu khung giao diện là gỗ sơn mài tối màu, đan tre và viền đồng, có họa tiết bông lau kín đáo. Không có chữ trong ảnh. Bố cục HUD trong trận theo chuẩn A0 ở `06_screens.md`: vòng cấp, máu/nội lực trên trái; menu và bản đồ nhỏ trên phải; d-pad 3 nút với hai vùng chéo vô hình dưới trái; cụm CHÉM/đổi mục tiêu/bình dưới phải; 5 ô kỹ năng giữa đáy. Hình nút thành phẩm sẽ vẽ riêng theo phong cách Việt (có thể tham khảo hoa văn trống đồng), không dùng ảnh hay biểu tượng game khác. Các màn còn lại tra Phần 5 `GDD.md` và đặc tả `06_screens.md`, tiếp tục duyệt ở A1 hoặc An theo lần đầu dùng màn, như `11_design_freeze.md`.

Ba loại tiền có biểu tượng riêng: tiền đồng (đồng xu đồng có lỗ vuông), ngân lượng (thỏi bạc), ngân phiếu (tờ giấy đổi bạc có dấu son).

## Thứ tự lớp trong trận (chốt từ A0)

Hiệu ứng đòn đánh (vệt chém, tia lửa trúng đòn) và số sát thương **luôn vẽ đè
lên nhân vật, hình nộm và quái**. Khi dựng scene hoặc sprite sheet phải giữ lớp
hiệu ứng/số cao hơn lớp thân, không để thứ tự node khiến quái che mất phản hồi
trúng đòn. Lộn người chỉ đổi hình hoạt ảnh, không xoay hitbox hoặc đổi lớp vẽ.

## Nhân vật: bộ tư thế vẽ trọn theo lớp, hiển thị mượt (người dùng chốt 29/10/2026)

Quyết định mới thay quy trình rig16 mảnh cho nhân vật/NPC/quái người: đầu,
thân kèm hai tay, chân (quần/cẳng/bàn chân), vũ khí. Mỗi lớp có trọn bộ hình
tư thế; runtime chỉ dời/lật, không xoay khớp hoặc xoay vũ khí theo tay.
Đòn đánh dùng hình vung vũ khí vẽ sẵn kèm vệt vật lý, lưỡi sắc theo chiều chém;
ngoài đòn đánh dùng hình kiếm sau lưng, đi theo thân. Thay áo/quần phải có đủ
bộ tư thế tương ứng; chỉ làm bậc0 trong bản thử này.

Nhân vật người giữ ảnh độ phân giải2× và hiển thị linear, không ép palette32 màu.
Đây là ngoại lệ mới cho người, không đổi phong cách/palette/lọcnearest của bản đồ,
vật thể hoặc thông số A0: người96px logic, khung128×128, chân cách đáy8px.
Dùng STYLE-B vẽ tay từ03_prompts, AVOID nguyên văn, luôn đính kèm ảnh gốc
`art/reference/ref_dinh_bo_linh.png`. Prompt nguyên văn và nguồn được giữ cạnh
bốn tờ ở `art/concept/characters/chr_dbl_poses/`; mọi hình còn chưa duyệt.

Cắt nền xanh alpha mềm, khử màu xanh ở viền; cắt theo thành phần liền khối,
chọn mốc cổ/hông/nắm tay/đế/chuôi bằng mắt và ghi số vào anchors.json.
Các tờ AI nguồn không đồng tỉ lệ: đăng ký đồng dạng TOÀN TỜ đầu/vũ khí trước,
sau đó xuất cùng hệ số; không co x/y khác nhau hoặc sửa tư thế lẻ. Báo cáo ghi
cả hệ số đăng ký và hệ số thực từ từng nguồn, không gọi tờ gốc đồng tỉ lệ.
Bản thử chỉ idle/run/jump/fall/slash; chưa thay nhân vật A0/Đào Úc.
Rig16 mảnh đã dừng, giữ nguyên để đối chiếu; xem16_rig và báo cáo pilot.

## Kiếm/Cung — quy tắc hình vũ khí (người dùng chốt30/10/2026)

Phái Kiếm dùng kiếm **thẳng hai lưỡi**, mũi nhọn, chắn tay nhỏ, cán quấn dây.
Không dùng katana hoặc kiếm Trung Hoa cầu kỳ; khối AVOID giữ nguyên. Bảy bậc
đều giữ cấu trúc này, khác vật liệu/hoàn thiện: t1sắt thô; t2sắt rèn; t3thép;
t4thép/chắn đồng nhỏ; t5thép tôi; t6thép sẫm; t7thép tốt/hoa văn lau tiết chế.
Không đổi chỉ số, cơ chế hoặc số liệu chiêu; Trảm Kiếm và Kiếm Tâm là tên hiện tại.

- Đứng/chạy/nhảy: kiếm cầm ở **tay trước ngang hông**, mũi **chéo xuống phía sau**,
  vắt trước thân; chạy thì lưỡi gần ngang hơn về sau, nhảy như đứng. Không chĩa lên/ra
  trước khi không đánh. Hình theo thân bằng điểm neo, không xoay sprite runtime.
- Đánh: **lia ngang hông** theo chuỗi thủ → kéo → lia → giữ → về thủ, hạ trọng tâm,
  chân choãi và vặn hông. Ẩn kiếm cầm tay, mỗi nhịp có hình kiếm+vệt riêng neo theo tâm;
  grip trùng nắm tay≤1px, vệt nối mũi≤2px. Không giơ cao bổ xuống hay dùng vệt trăng khuyết.
  Vệt thường trắng ngang dẹt, mép tơi/đuôi mờ; Trảm Kiếm thêm lớp sáng xanh theo bảng mục5.
- Cung đứng/chạy/nhảy cầm **tay trước, chéo trước thân**: đầu trên chếch lên trước,
  đầu dưới xuống sau, bụng hướng ra trước; không dựng sau lưng. Khi bắn, tay xa duỗi ra
  trước cầm cung; **lưng cong phồng ra trước, dây ở sau về phía người bắn**.
  Giương: dây chữV tới tay gần cạnh má; thả: dây thẳng. Tên là hình riêng,
  mũi ở đầu phía trước và bay ra trước sau khung thả.
- Vũ khí cầm tay chỉ hiện ở tư thế đứng/chạy/nhảy/rơi (khung0–7,12–13 của bảng dự án);
  ẩn cả4khung lộn và mọi khung đánh. Không nhầm chỉ số khung trên không của nguồn
  tham khảo với khung21giương cung của bảng dự án.

Bản thử dùng tranh2×, Sprite2Dlinear scale0,5 cố định, rotation0; chỉ lật gốc.
Mốc và hình thật được kiểm trong `weapon_direction_checks.gd`; tài nguyên cũ
của rig16mảnh đã dừng không bị đổi ID hay nội dung. Các đoạn rig lịch sử phía
trước chỉ là lưu đối chiếu, không quy định hình vũ khí hiện hành.

## Nhân vật chính — chốt 30/10/2026 (người dùng duyệt)

Mục này thay mọi quy định nhân vật trước đó (rig 16 mảnh, bộ tư thế STYLE-B vẽ tay,
pixel 96 px). Các mục cũ giữ lại để đối chiếu, không còn hiệu lực cho nhân vật người.

**1. Style.** Mẫu chính: hai bảng ở mục 8. Bản **v2_a** trong `art/concept/style_v2/` chỉ còn là chuẩn viền/màu. Viền đậm đều (2–3% chiều cao
người), màu phẳng, đổ bóng 2–3 tông sắc nét, khối to rõ, đầu to (~1/3 chiều cao).
Hiển thị ~160 px trên màn 1600×720, ảnh nguồn độ phân giải cao, lọc linear, không ép
palette 32 màu. Khối STYLE cho mọi prompt nhân vật người (dán nguyên văn), sau đó là
khối AVOID nguyên văn:

```
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
```

**2. Dựng nhân vật: 4 lớp** — đầu, thân (kèm hai tay), chân, vũ khí. Mỗi khung chọn một
hình vẽ sẵn của từng lớp rồi dời (dx, dy); quay trái chỉ lật gương ở node gốc. Không xoay
sprite, không xoay khớp. Bảng 30 khung và định dạng chiêu: `09_animation_spec.md`.
Số hình mỗi bộ: đầu 8, thân 18, chân 10, vũ khí cầm tay 1–2.

**3. Mỗi nhân vật một phái.** Phái Kiếm: không có cung/ống tên. Phái Cung: không có
kiếm/bao kiếm, ống tên đeo sau lưng. Đầu/thân/chân dùng chung hai phái.

**4. Bảy cấp trang bị 1/10/20/30/40/50/60.** Thang màu: Lv1 vải mộc nâu xám, nón lá →
Lv10 bạc/thép → Lv20 xanh lam → Lv30 tím → Lv40 vàng đồng → Lv50 đỏ vàng → Lv60 đỏ
vàng rực, giáp tướng. Dáng kiếm (thẳng hai lưỡi) và dáng cung giữ nguyên qua mọi cấp;
cấp cao thêm chi tiết, hoa văn, vật liệu. Mỗi cấp vẽ lại đủ bộ nón/áo/quần đúng số khung
và điểm neo của Lv1. Ảnh bảng thiết kế người dùng gửi 30/10 là tham khảo thang màu và
mức chi tiết, không vẽ lại y nguyên.

**5. Vũ khí và hiệu ứng.** Ngoài đòn đánh vẽ vũ khí cầm tay/đeo lưng theo cấp. Trong nhịp
đánh ẩn vũ khí cầm tay, thay bằng **hình vung + vệt chém dùng chung cho mọi cấp của phái**,
chỉ đổi màu vệt theo cấp (trắng → xanh → vàng → đỏ); mũi tên đổi màu tương tự.
**Ngoại lệ phát sáng:** vũ khí Lv50–60, vệt chém/mũi tên Lv40–60, hiệu ứng chiêu và
hào quang cường hóa Full +8/+12/+14/+16 **được** có lửa/ánh sáng/hào quang. Prompt cho các
hình này bỏ cụm `magic glow or glowing energy slashes` khỏi khối AVOID; mọi cụm khác giữ.

**6. Trang bị 10 ô theo GDD.** Chỉ nón/áo/quần/vũ khí hiện lên người (găng nằm trong hình
áo, giày trong hình quần). Dây chuyền, nhẫn, ngọc bội, bùa chỉ có icon. Phi phong là ô
thời trang. Mỗi ô × mỗi cấp có 1 icon.

**7. Thứ tự vẽ nhân vật chính** (mỗi bước một nhánh, review xong mới sang bước sau):
(1) hệ thống 30 khung + Lv1 hai phái; (2) Lv10/20/30; (3) Lv40/50/60; (4) hiệu ứng đủ
8 chiêu mỗi phái; (5) hào quang cường hóa, cưỡi Trâu/Ngựa chiến/Voi chiến, icon 10 ô × 7 cấp.
Bản đồ làm sau khi nhân vật chính xong.

**8. Bảng thiết kế tham khảo (người dùng gửi 30/10/2026)** — nhân vật lấy từ hai bảng:
`art/reference/chr_dbl_board_trang_bi.png` (bảng A: trang bị, vũ khí, chiêu, hào quang) và
`art/reference/chr_dbl_board_animation.png` (bảng B: động tác, cải trang, thú cưỡi). Chỉ học
thiết kế, không cắt ghép ảnh vào game.

**Hai bảng này là MẪU CHÍNH về hình nhân vật** (người dùng chốt 30/10/2026, thay v2_a làm mẫu): dáng chibi đầu to, mặt, tóc, khăn đỏ, màu bão hòa đỏ/vàng/xanh, viền tối rõ, đổ bóng tương phản như bảng. Mọi prompt nhân vật đính kèm hai bảng + ảnh `ref_dinh_bo_linh.png` và yêu cầu "giống nhân vật trên bảng". Chỉ khác bảng ở độ phân giải: vẽ to, nét sạch để hiển thị 128 px trên màn 1600×720 mà không vỡ (không thu nhỏ thành pixel 30–40 px như ô trên bảng). Khối STYLE-V2 vẫn dùng cho phần viền đậm/màu phẳng; chỗ nào STYLE-V2 khác bảng thì theo bảng. Mọi bản vẽ phải đặt cạnh bảng để so; không giống bảng là không đạt.

*Lấy theo bảng:*
- Ngoại hình Đinh Bộ Lĩnh: tóc đen búi, khăn/dải đỏ, mặt và dáng chibi đầu to (đầu kèm tóc, không tính nón/chóp nón = 0,40H ± 0,03 ở khung 00) như hàng "Tổng thể" bảng A.
- Trang phục 7 cấp theo hàng nón/áo/quần/găng/giày bảng A: Lv1 không nón lá, áo giao lĩnh nâu dài, giày, dải tóc đỏ; Lv10–30 vải
  xanh/tím; Lv40–60 giáp đỏ vàng, mũ tướng.
- Kiếm và cung 7 cấp, vệt chém và mũi tên đổi màu theo cấp (bảng A mục 2–3).
- Hào quang Full +8/+12/+14/+16 (bảng A mục 8, bảng B mục 10).
- Hiệu ứng chiêu (bảng A mục 5–6, bảng B mục 6–7) gán cho chiêu GDD như dưới.
- Icon 10 ô × 7 cấp, icon sách chiêu (bảng B mục 11).

*Đổi lại cho khớp tài liệu:*
- **Tên, cấp mở, số liệu chiêu giữ theo GDD**; chỉ lấy hình hiệu ứng. Gán:
  Kiếm — Trảm Kiếm ← Trảm Phong; Song Trảm ← Liên Trảm; Quét Ngang ← Hồi Phong Trảm;
  Thiết Kỵ Xung Phong ← Xung Phong; Khai Sơn Trảm ← Thiên Quân Trảm; Vạn Quân Trảm ← Long Trảm;
  Vạn Thắng ← Càn Khôn Trảm; Chấn Uy vẽ mới.
  Cung — Xạ Tiễn ← Xạ Tiễn; Phá Giáp Tiễn ← Xuyên Giáp Tiễn; Song Tiễn ← Liên Tiễn;
  Thần Tiễn Xuyên Giáp ← Phong Tỏa Tiễn; Tam Tiễn Liên Châu ← Tán Hoa Tiễn; Vạn Tiễn ← Thiên Vũ
  Tiễn; Hộ Thân Khí, Liều Mạng Giương Cung vẽ mới; Hỏa Vũ Tiễn để dự phòng.
- **Nội tại theo GDD** (Kiếm Tâm, Kiên Cường, Tâm Nhãn, Ẩn Mình). Các icon bị động trên bảng
  chỉ dùng làm icon chỉ số/tiềm năng.
- **Thú cưỡi theo GDD: Trâu, Ngựa chiến, Voi chiến.** Hổ trên bảng thay bằng Voi chiến. Thú
  cấp 0–99, mốc ngoại hình 1/20/40/60/99 (không có Lv100). Cưỡi thú để Mốc sau.
- **Cải trang Sơn Tinh / Thủy Tinh / Thánh Gióng** = biến hình thay cả người, [Phạm vi sau]
  theo 17_ngoai_hinh; chưa làm.
- **Bỏ hàng "Đi"**: chỉ có chạy (bảng 30 khung).
- Nhân vật áo đỏ, áo choàng đỏ ở bảng B là dáng đồ cấp cao; **Lv1 theo bảng A** (không nón lá, áo giao lĩnh nâu dài, giày, dải tóc đỏ).
  Áo choàng là ô thời trang.
- Đòn thường "Tấn công 1/2/3" trên bảng B dựng bằng 16 tư thế đánh trong bảng 30 khung.

**Cập nhật ưu tiên theo quyết định cuối 30/10/2026 — bộ hình thử chưa duyệt:**
Mẫu ngoại hình là hàng “Tổng thể” Lv1, không lấy nón lá ở hàng trang bị. Đầu kèm tóc
bằng 0,40H ± 0,03, thay các tỉ lệ cũ và đề nghị 0,50H trước đó. Người cao 128 px
khi hiển thị trên 1600×720, tương ứng khoảng 96 px logic A0; thân/chân ngắn, chắc.
Áo giao lĩnh nâu dài, giày và dải tóc đỏ; không đổi trang phục theo các đoạn STYLE cũ
khi chúng trái quyết định này. Các mô tả cũ ở mục 1/4 giữ để tra lịch sử.
Kiếm cầm tay: cạnh dài nhất của hộp pixel không trong suốt = 0,75–0,80H;
không thay bằng phép đo dọc trục lưỡi. Cung cầm/giương cao 0,90–1,00H (thay số cũ
0,35–0,40H); tên dài 0,55–0,65H. Kiếm chúc xuống sau ngoài đánh; cung ở trước thân.
Trong nhịp đánh ẩn kiếm cầm, hình vung có đoạn lưỡi ngắn cùng vệt cong sát thân;
không tăng đoạn lưỡi này thành cây kiếm cầm tay nguyên chiều dài.
Tên đặt sẵn: đuôi ở tay kéo dây, thân tên qua điểm tựa trên cung; khi thả, đuôi tên bay
bắt đầu tại dây đã thả, không nhảy sang bàn tay cầm thân cung. Góc được vẽ sẵn vào ảnh;
mọi Sprite2D vẫn rotation = 0. Kiếm và cung thuộc hai phái riêng, không hiện cùng người.
