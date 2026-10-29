# Nhật ký thiết kế

Mỗi lần tạo ảnh hoặc sửa đặc tả thêm một mục theo mẫu dưới. Không xóa mục cũ. Sau khi chốt thiết kế, mọi thay đổi vẫn ghi ở đây kèm lý do.

## Mẫu cho ảnh

- **Ngày:** 2026-10-28
- **Mã:** chr_dbl_base_v1
- **Prompt:** (nguyên văn)
- **Ảnh tham chiếu:** (đường dẫn, hoặc "không")
- **Kết quả:** giữ / loại — lý do

## Mẫu cho đặc tả

- **Ngày:** 2026-10-28
- **Mã:** lay_dao_uc_v2
- **Thay đổi:** (ví dụ: thêm bậc thang lên lũy, dời vùng sinh quái ở cột 46)
- **Lý do:** (ví dụ: theo góp ý của người dùng, hoặc soát số đo nhảy)

---

## Quyết định P0 — 28/10/2026 (đã duyệt hướng mỹ thuật)

- **Mã:** `p0_style_decision_v2`
- **Quyết định:** chọn B — pixel bán hiện đại, dáng khoảng 4 đầu, bảng 32 màu, bóng 3 tông. Tóc Đinh Bộ Lĩnh búi nhỏ trên đỉnh đầu. Kích thước sprite người ~64 px/khung 96×96, boss người ~88 px/khung 160×160 **vẫn Tạm thời**.
- **Ngoại lệ quy trình:** P0 thực tế so sánh A pixel chibi, B pixel bán hiện đại, C vẽ tay; không chạy bản không có STYLE theo khuôn gốc vì người dùng đã chắc đi theo pixel và muốn so sánh các mức chi tiết/chi phí. Tên `sty_explore_free` được đánh dấu bỏ qua có lý do, **không** giả vờ đã sinh bản free.
- **Vòng P0 đầu:** bảng ghép có lỗi vệt năng lượng phát sáng, mái cong nhiều tầng, thành đá kiểu lâu đài, cờ đỏ, mũ cánh chuồn và nhắc tên game khác. **Vòng P0 thứ hai** đã sửa các lỗi đó bằng vệt gió/bụi, thành đất, nhà tranh, cờ lau trắng, NPC không mũ cánh chuồn và bỏ tên game khác.
- **Tồn đọng cho P1/giai đoạn 1:** chỉnh lính các sứ quân sang khăn chít đầu/mũ trụ và màu cờ phe; tránh nón lá hàng loạt; nhân vật chính búi tóc nhỏ; kiểm tra tỷ lệ trên màn hình 640×360.
- **Ảnh nguồn:** `wide_poster_like_concept_art_board_with_a_clean_l.png` (bảng ghép vòng hai, ngoài kit); các ảnh `art/concept/style/sty_explore_{a,b,c}_v2.png` **là ảnh cắt từ cùng một bảng ghép, không phải ba lần sinh độc lập**. Chúng là concept tham khảo, chưa phải sprite hay asset production.
- **Prompt nguyên văn của vòng P0 thứ hai:**

```text
Wide, poster-style concept board comparing three visual directions for a realistic 2D side-scrolling game set in 10th-century Vietnam, arranged as a clean infographic with Vietnamese labels, a dark title header, three bordered columns (A, B, C), gameplay scenes, character sprites, NPCs, environment thumbnails, palettes, and a bottom evaluation table recommending Style B. Column A presents compact chibi pixel art, Column B offers more detailed semi-modern pixel art as the preferred balance, and Column C shows richly painted non-pixel artwork, all featuring Vietnamese rural architecture, reeds, earthen fortifications, rice fields, karst mountains, straw-hatted fighters, sword-and-dust effects, and no heavy magical glow.
```

- **Prompt vòng P0 đầu:** prompt nguyên văn không được lưu trong dữ liệu tạo ảnh hiện có; **không thể xác nhận hoặc tái tạo nguyên văn**. Bảng đầu có chữ “Ninja School” ở tiêu đề, nhưng không có bằng chứng chữ đó nằm trong prompt đã dùng. Không tái sử dụng prompt hoặc bảng đầu cho các asset sau.
- **Ảnh tham chiếu:** không có ảnh tham chiếu đính kèm cho vòng hai.
- **Kết quả:** giữ hướng B; P0 duyệt phong cách, các file concept tách cột chỉ phục vụ tham khảo.

## 28/10/2026 — chr_dbl_base, palette, kích thước sprite

- **chr_dbl_base:** duyệt v9 làm ảnh mẫu. Không ép màu, không tách lớp trên ảnh mẫu khổ lớn: đã thử (v9_pal, v9_pal_v3, parts khổ 280×724) và loại vì chia vùng bằng khung chữ nhật, lấp lỗ bằng khối màu phẳng, màu ngoài bảng.
- **palette:** duyệt palette_v3, 32 màu, gpl khớp png.
- **Báo cáo giả:** nhiều bảng trình bày trước đó do $imagegen vẽ, số liệu không khớp file thật; file chr_dbl_idle_side_96.png chưa từng tồn tại. Đã thêm QUY TẮC BÁO CÁO KIỂM TRA vào AGENTS.md.
- **Kích thước sprite:** ở 64 px phong cách B mất gương mặt. Đề xuất đổi sang màn hình gốc 960×540, nhân vật người cao 96 px, canvas 128×128 (Tạm thời), chờ người dùng xác nhận rồi cập nhật 13_thong_so và 01_art_bible.

## 28/10/2026 — Bản dự án chuẩn v2 → v3: kích thước và thử sprite

- Nguồn duy nhất: `CoLauKhoiNghia_project_v2.zip` do người dùng đính kèm; không trộn kit cũ.
- Đổi **Tạm thời** sang 960×540 (xuất ×2 lên 1920×1080), nhân vật 96 px trong 128×128, chân cách đáy 8 px, boss người ~132 px trong 192×192. Đã đồng bộ `01_art_bible.md`, `13_thong_so.md`, `06_screens.md`, `08_map_layout.md`, `09_animation_spec.md`.
- Hạng mục ảnh hưởng: mọi sprite/animation, hitbox, baseline, camera, HUD, map layout, tileset, parallax, VFX, vùng chạm. Bố cục cũ phải được soát lại; chưa tự duyệt.
- `chr_dbl_concept_side_big.png`: cắt vùng nhân vật từ **một ảnh concept do imagegen tạo**, vì kết quả imagegen là bảng ghép không đúng yêu cầu ảnh đơn. Chỉ giữ vùng nhân vật, không dùng phần bảng làm kết quả. Nền concept chưa bảo đảm thuần `#00FF00`; script xử lý nền.
- `chr_dbl_idle_side_96`: bản thử tự động qua `snap_pixel.py`; chưa sửa tay Aseprite; **Chưa duyệt**. Kiểm tra bằng `check_sprite.py` và lưu stdout trong `tools/chr_dbl_idle_side_96_check.txt`.

### 2026-10-28 — chr_dbl_idle_side_96_v2 — vòng thử chưa đạt, không duyệt
- Nguồn duy nhất: CoLauKhoiNghia_project_v3.zip.
- Yêu cầu: 17 màu nhân vật (`outline,skin,fabric,belt,pants`), cấm 6 nhóm môi trường; không được thu nhỏ lưới nghệ thuật 141→96; chiều cao lưới phải 96±2.
- Ảnh concept mới được sinh bằng công cụ hình ảnh nhưng công cụ vẫn xuất bảng ghép. Đã cắt riêng nhân vật để lưu `art/concept/characters/chr_dbl_concept_side_big_v2.png`; đây không phải concept đơn độc nguyên bản, và phần cắt có kích thước 365×830, chưa đạt yêu cầu ảnh concept >=1024 px chiều cao.
- Script `tools/snap_pixel.py` đã thêm `--groups`, lấy trung vị mỗi ô, dò chu kỳ hai trục, và từ chối ảnh nếu số ô không trong 94..98. Không thực hiện resize sau nắn lưới.
- Chạy thực tế: crop 259×815, chu kỳ x=5 y=6, 52×136 ô. **REJECT**, không tạo sprite `_v2.png` hay `_v2_x4.png`, giữ nguyên sprite v3 cũ. Log lỗi: `tools/chr_dbl_idle_side_96_v2_snap.log`.
- `tools/check_sprite.py` bổ sung thống kê theo nhóm và số pixel thuộc nhóm cấm; chưa chạy được trên v2 vì v2 chưa tồn tại.
- `docs/10_storyboard.md`: đổi cutscene 640×360 sang 960×540.
- Trạng thái: CHƯA DUYỆT; cần concept đúng một nhân vật, đúng native grid 96±2 rồi chạy lại.

## 28/10/2026 — Phân loại sprite chính là PLACEHOLDER, chuẩn bị nguyên mẫu

- **Nguồn chuẩn:** `CoLauKhoiNghia_project_v4.zip`, chỉnh sửa trong dự án và đóng gói thành v5.
- **Mã:** `chr_dbl_idle_side_96` — `art/sprites/characters/chr_dbl_idle_side_96.png`.
- **Trạng thái:** **PLACEHOLDER**. Đã đạt kiểm tra kỹ thuật trong báo cáo v3 (128×128, nhân vật 96 px, cách đáy 8 px, palette hợp lệ và x4 NEAREST); **chưa đạt mỹ thuật, chưa được duyệt**. Kết quả tạo v2 bằng snap_pixel chưa đạt nên không thay thế file này.
- **Quyết định:** giữ placeholder để kiểm thử nguyên mẫu Godot; sau nguyên mẫu phải thay bằng sprite nhân vật chính được chỉnh tay hoặc thuê họa sĩ vẽ. Không sao chép placeholder sang `art/approved/`.
- **Quy trình art:** $imagegen + snap_pixel chỉ dành cho quái, NPC, tile và vật phẩm; không dùng làm pipeline chốt sprite nhân vật chính. Đã sửa `01_art_bible.md`.
- **Mốc A:** đã rà lại `11_design_freeze.md`. Danh sách còn thiếu xem báo cáo gửi kèm; **chưa ký duyệt Mốc A**, không tự đánh dấu bất kỳ checkbox nào. Nếu muốn dựng nguyên mẫu trước khi qua Mốc A thì cần người dùng quyết định ngoại lệ và cập nhật quy định mốc trước khi code.

## 28/10/2026 — Duyệt phạm vi A0 và đánh dấu các quyết định P0 đã chốt

- **Nguồn chuẩn:** `main` của `DVSoai/design_co_lau`; đề xuất thay đổi trên nhánh `a0-freeze`.
- **Quyết định:** người dùng cho phép dựng nguyên mẫu **Mốc A0 — Bản thử cảm giác** bằng Godot 4, tách riêng trong `prototype/`. Mục tiêu: kiểm tra 960×540, nhân vật 96 px, chạy/nhảy, va chạm/hitbox, camera dead zone/look-ahead, nhịp chém trên thiết bị Android.
- **Phạm vi khóa:** một bản đồ thử dài khoảng ba màn hình, đất bằng/bậc/hố/bục nổi, sprite PLACEHOLDER hoặc khối màu, đi/nhảy/rơi/chém và một hình nộm; không giao diện, save, vật phẩm, nhiệm vụ, âm thanh.
- **Quy tắc:** mã trong `prototype/` chỉ để thử rồi bỏ, không chép sang game thật; thông số tập trung trong một file. Game thật vẫn không code trước Mốc A.
- **Trạng thái:** **đã duyệt cho phép làm A0, chưa nghiệm thu A0**. Chỉ khi người dùng chơi thử Android và chốt thông số mới cập nhật trạng thái Tạm thời → Đã duyệt ở `docs/13_thong_so.md` và ghi nhật ký.
- **Mốc A nhóm 1:** đánh dấu hai mục đã duyệt: phong cách B — pixel bán hiện đại (P0) và bảng palette_v3 32 màu, dựa theo quyết định đã ghi trong nhật ký.
- **PR lần này chỉ sửa tài liệu, không viết mã Godot.**

## 28/10/2026 — Tổ chức repo thiết kế và game thật

- **Mã:** `repo_split`.
- **Thay đổi:** thêm mục “Tổ chức repo” vào `README.md` và `AGENTS.md`: `design_co_lau` giữ tài liệu thiết kế, art nguồn, script và `prototype/` cho A0; mã A0 là mã bỏ đi, chỉ kiểm chứng thiết kế.
- **Mốc A:** repo game thật `co_lau_game` đã được người dùng tạo và thêm; chỉ bắt đầu triển khai game thật sau khi Mốc A được duyệt; nguyên mẫu A0 là ngoại lệ giới hạn trong repo thiết kế, không thay thế việc duyệt mốc.
- **Nguồn art:** chép ảnh đã duyệt từ `art/approved/` sang `co_lau_game/assets/` bằng script và ghi commit nguồn của `design_co_lau` mỗi lần chép.
- **Phiên bản thiết kế:** khi qua Mốc A, gắn tag `design-vX.Y`; repo game ghi tag đang theo và giữ bản sao `docs/GDD.md` từ đúng tag đó.
- **Phạm vi:** chỉ cập nhật tài liệu theo yêu cầu người dùng; không tạo thêm repo game, tag, prototype hay script chuyển art, không viết mã và không đánh dấu Mốc A đã duyệt.

## 28/10/2026 — Kết quả A0 trên PC và sửa điều khiển bảng ⚙

- **Mã:** `a0_pc_result`.
- **Kết quả người dùng:** đã chơi thử A0 trên PC bằng Godot 4.7.2, thấy ổn với bộ mặc định trong `prototype/config/tuning.gd`, không chỉnh thông số. Độ phân giải 960×540 và nhân vật 96 px hiển thị ổn trên PC; chuyển động giả bật.
- **Thông số:** ghi bộ đã thử vào `docs/13_thong_so.md`, gồm chạy/gia tốc, nhảy và giá trị suy ra, coyote/jump buffer, hitbox, camera, nhịp chém và công tắc chuyển động giả. Trạng thái: **Tạm thời — đạt thử PC (Godot 4.7.2, 28/10/2026), chờ thử Android**; không đổi sang Đã duyệt.
- **Sửa bảng ⚙:** nút ⚙, mọi HSlider, CheckButton và nút Sao chép dùng `FOCUS_NONE`; HSlider tắt `scrollable`. Phím mũi tên và con lăn không đổi thông số; thao tác kéo trực tiếp vẫn được giữ. Thêm kiểm tra sự kiện bàn phím/con lăn và thao tác kéo.
- **Ảnh hưởng:** kết quả là cơ sở tạm cho bố cục bản đồ, va chạm, camera, hoạt ảnh và nhịp chơi; không tự đổi asset đã duyệt. Các tài liệu ngoài phạm vi lần này giữ nguyên.
- **Bước tiếp theo:** người dùng thử trên điện thoại Android và xác nhận; chỉ sau đó mới chuyển thông số sang Đã duyệt và nghiệm thu A0 theo điều kiện mốc. A0 không thay Mốc A.

## 28/10/2026 — Ký duyệt A0 trên Android

- **Mã:** `a0_signoff`; nguồn bộ mặc định: **main `7973729`**, `prototype/config/tuning.gd`.
- **Nghiệm thu của người dùng:** đã chơi trên **Realme RMX3760 (Android, màn hình 1600×720), Godot 4.7.2**, bật **Kiểu cổ điển**, và chấp nhận. Đã qua **Mốc A0**; đây là xác nhận thử thiết bị thật của người dùng, không phải kết luận từ headless.
- **Hiển thị:** 960×540, nhân vật 96 px/khung 128×128; canvas_items/expand/fractional/nearest; Android fullscreen + immersive; bảng màu palette_v3 đã duyệt. HUD và cụm nút neo theo viewport thực 960–1200 px logic.
- **Di chuyển/nhảy:** RUN_SPEED=200 px/s tức thì; STOP_TIME=0,08 s; TURN_TIME=0,05 s, khung đầu chỉ đổi mặt. Nhảy 96 px, lên đỉnh 0,38 s, g≈1329,64 px/s², JUMP_SPEED≈−505,26 px/s; lên/xuống cùng trọng lực, không treo đỉnh; rơi tối đa≈1010,53 px/s. Coyote 0,10 s, buffer 0,12 s; giữ nhảy lại bật, giữ lâu nhảy cao tắt. Hướng trên không nhận ngay, vùng chéo dùng 0,8 RUN_SPEED.
- **Khinh công/lộn đỉnh:** lần bấm mới khi còn đi lên trong cửa sổ ≤30% vận tốc nhảy; bật 0,7 JUMP_SPEED, tối đa một lần/cú nhảy, reset khi chạm đất. Mỗi pha nhảy/khinh công lộn 360° trong 0,2 s, chỉ sprite. Game thật cần khung hoạt ảnh riêng thay xoay ảnh tạm.
- **Hitbox/chém/camera:** người 24×88; đòn 0,30 s, trúng 0,10–0,20 s, hồi thêm 0,15 s; vùng chém 56×56 tại (34,−52). Camera nửa vùng chết (100,60), nhìn trước 100 px, đáp ứng 5 /s. Hiệu ứng đòn đánh và số sát thương luôn trên lớp thân nhân vật/quái.
- **Điều khiển:** chỉ ba nút thấy được ←/→/↑, hai vùng chéo vô hình sát ↑, ưu tiên ↑ > chéo > hướng; chạm chéo làm sáng cả ↑ và hướng. d=84 px, hệ số 2,2/1,35/0,9; lề≥24, chữ≥22. Cụm CHÉM 1,4d/đổi mục tiêu/HP/MP ở phải; năm ô kỹ năng giữa đáy; HUD trên gồm vòng cấp, máu/nội lực, menu và bản đồ nhỏ. Hình nút thành phẩm vẽ riêng theo phong cách Việt, chưa duyệt mỹ thuật từ các khối A0.
- **Lỗi trôi slider khi cuộn cảm ứng:** slider chỉ bắt kéo ngang nếu bắt đầu trên núm; khóa hướng vuốt, chuyển vuốt dọc cho ScrollContainer; vùng slider cao 44 px. Con lăn không chỉnh số.
- **Lỗi focus bàn phím:** dùng FOCUS_NONE cho nút/bảng chỉnh liên quan để mũi tên điều khiển nhân vật, không chuyển focus hoặc đổi giá trị.
- **Lỗi viền đen trên màn 720p:** thay keep + integer bằng expand + fractional, giữ nearest; fullscreen + Immersive Mode khi xuất APK. Cập nhật neo nút, camera và thông tin màn hình theo viewport thật.
- **Lỗi xuất nhầm dự án:** thống nhất mở/import và xuất đúng `prototype/project.godot`, kiểm tra tên dự án và Godot/export template 4.7.2; không xuất thư mục kit thiết kế hay dự án khác.
- **Lỗi vùng chéo bị vẽ thành nút:** tách vùng nhận chạm vô hình khỏi hình nút, chỉ hiện viền mảnh khi F1; feedback chuyển sang ↑ và nút hướng tương ứng.
- **Tài liệu:** cập nhật `13_thong_so.md`, `06_screens.md`, `08_map_layout.md`, `09_animation_spec.md`, `01_art_bible.md`, `11_design_freeze.md`. Chỉ các thông số/cơ chế đã nêu chuyển sang Đã duyệt (A0, 28/10/2026); bậc/khe an toàn và mọi bố cục còn cần thử, không coi 143,04 px lý thuyết là bậc bắt buộc đã duyệt.
- **Ảnh hưởng cần soát:** 29 bố cục bản đồ, vùng che HUD/điểm đáp, camera nhiều tầng, hitbox, hoạt ảnh nhảy/khinh công/quay đầu và nhịp chém. Không tự duyệt lại asset hay các hạng mục còn thiếu ở Mốc A.
- **Sau A0:** `prototype/` giữ làm tham khảo; không chép mã sang `co_lau_game`. Kiểu cũ có gia tốc/nhảy 80 px chỉ để so sánh, không dùng cho game thật. Tiếp tục Mốc A đầy đủ; chưa qua Mốc A, chưa mở code game thật.

## 28/10/2026 — Quy trình nhân vật chính ghép bộ phận và lát cắt Giai đoạn 1

- **Mã:** `chr_dbl_parts_workflow`. Người dùng xác nhận **không thuê họa sĩ**; thay yêu cầu trước đây về chỉnh tay/thuê họa sĩ bằng imagegen + snap_pixel + sửa pixel bằng script, kiểm check_sprite và duyệt từng bộ phận bằng script/bằng mắt bởi Claude/người dùng.
- **Bộ phận:** tỉ lệ nhân vật 96 px, gồm đầu kèm tóc, thân, cánh tay trên/dưới gần/xa, đùi/cẳng chân gần/xa, bàn tay, vũ khí; mỗi mảnh có điểm khớp và phần vẽ bù bị che. Dữ liệu `chr_dbl_anim_*` ghép vị trí, góc và thứ tự lớp theo từng frame ở `09_animation_spec.md`; lộn/chiêu lớn được bổ sung khung riêng nếu cần.
- **Trang bị:** `chr_dbl_t1`…`t7` là áo/quần/vũ khí thay thế, giữ khớp/dữ liệu hoạt ảnh, không vẽ lại cả động tác mỗi bậc.
- **Cửa duyệt cuối Giai đoạn 1:** lát cắt Đào Úc + nhân vật ghép bộ phận + một quái trong `prototype/`, phải duyệt trước khi mở Giai đoạn 2. Ngoại lệ kỹ thuật giống A0, mã bỏ đi, không mở code game thật trước Mốc A và không chép sang `co_lau_game`.
- **Phạm vi hiện tại:** chỉ đổi tài liệu. Công cụ snap_pixel/check_sprite đang kiểm nhân vật nguyên khung, chưa kiểm mảnh/khớp/dữ liệu frame; cần bổ sung kiểm phù hợp khi sản xuất. Không sửa công cụ, không tạo bộ phận/lát cắt, không tự đánh dấu asset đã duyệt. Các thử nghiệm tách ảnh bị loại và placeholder cũ vẫn giữ trạng thái cũ; quyết định quy trình mới thay quy định trước nhưng không biến ảnh cũ thành asset đã duyệt.

## 28/10/2026 — Kế hoạch kiến trúc và skill tham khảo

- **Mã:** `architecture_and_skills`; nhánh dựa trên **main `5577fa5`**, đã merge PR A0. Giữ nguyên các mục A0/quy trình ghép bộ phận, ghi nối tiếp mục này; commit prototype nghiệm thu vẫn là `7973729`.
- **Kiến trúc:** thêm `15_kien_truc_game.md`, đề xuất Godot 4.7.2/GDScript, src theo tính năng, Resource .tres trong data/, snapshot lưu riêng, ID theo `14_online_migration.md`, signal/EventBus và bốn autoload tối thiểu. Mỗi SCR-xx có thư mục UI riêng; rig ghép bộ phận/trang bị thay mảnh. Thêm checkbox kiến trúc ở Mốc A, vẫn để chưa duyệt. Chưa tạo mã game hay thêm addon.
- **Nguồn 1:** `gamedev-skills/awesome-gamedev-agent-skills`, commit `19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9`, **Apache-2.0**; giữ LICENSE/NOTICE. Chép router, 16 Godot, 15 discipline, RPG/platformer, prototype-fast, tài liệu format/version; bỏ mọi engine/genre/workflow ngoài yêu cầu.
- **Nguồn 2:** `jame581/godotprompter`, commit `d7b26cdb5fae14d4ef7b713c5bf259395e75c3c6`, **MIT**; giữ LICENSE. Chỉ chép 16 skill được yêu cầu và references/assets/scripts đi kèm.
- **Rà B3:** quét toàn văn 153 file nguồn, đọc đối chiếu các vùng khớp lệnh/tự động hóa; 84 file có điều chỉnh (bao gồm banner/link/định dạng), phần nội dung cần gỡ/đổi nằm ở 21 file. Gỡ hướng dẫn cài addon/SDK/template/phụ thuộc, tải Butler/SDK/artwork, mẫu CI tự chạy và chỉ dẫn gọi helper tự động. Không phát hiện yêu cầu bỏ qua quy tắc cấp cao. Lưu vùng dòng gốc, hash trước/sau và kết quả từng file trong `tools/agent-skills/AUDIT.md` và `AUDIT.json`.
- **Giới hạn nhập:** không chép hooks/, commands/, agents/, plugin.json hoặc cấu hình tự chạy. Ba helper Python giữ dạng văn bản 0644; chỉ rà AST, không thực thi; không cài phụ thuộc hoặc đăng ký plugin. Các CLI còn lại là ví dụ thụ động, không cấp quyền chạy. Link tới file ngoài tập con trỏ về nguồn đúng commit, không tự tải thêm.
- **Xung đột:** `tools/agent-skills/CONFLICTS.md` ghi rõ quyết định dự án thắng: hiển thị A0/di chuyển cổ điển/d-pad vô hình, palette/kiểm sprite/ghép bộ phận, giới hạn autoload, save tách Resource, offline và cửa Mốc A. GDD/14 còn nhắc JSON; phải đồng bộ khi duyệt kiến trúc, không âm thầm đổi dữ liệu.
- **Bên thứ ba:** ghi nguồn/commit/giấy phép skill trong mục bên thứ ba của kế hoạch; addon chỉ là đề xuất, cần kiểm Godot 4.7 và giấy phép rồi người dùng duyệt. Khi sang co_lau_game, chép skill đã rà và giữ nguyên mục Skill tham khảo trong AGENTS.md; cập nhật THIRD_PARTY.md.
- **Phạm vi:** chỉ docs/, tools/agent-skills/ và AGENTS.md; không sửa prototype/, không thay nội dung đã ký duyệt A0, không mở code game thật.

## 28/10/2026 — Đồng bộ GDD với A0 và chốt 5 ô kỹ năng

- **Mã:** `gdd_sync_a0`; nguồn: thông số A0 tại `7973729`, tài liệu đã ký duyệt trên main `5577fa5`. Chỉ sửa GDD, màn hình, thông số và nhật ký; không sửa `prototype/` (SKILL_COUNT đã là 5).
- **Quyết định:** 5 ô chiêu; người chơi chọn 5 trong 8 chiêu chủ động/hỗ trợ của phái (kể cả tuyệt kỹ) để xếp vào ô; chiêu nội tại tự có hiệu lực, không cần ô. Đồng bộ HUD, menu nhân vật, thẻ kỹ năng và dữ liệu lưu nhân vật. Không đổi số liệu/cách học chiêu hoặc duyệt lại các giá trị cân bằng còn tạm thời.
- **Lý do:** viewport rộng 960 px, cạnh ô 58,8 px, khe 6 px: 6 ô rộng 6×58,8 + 5×6 = 382,8 ≈ 383 px, chồng nút → khoảng 4,2 ≈ 4 px; 5 ô rộng 5×58,8 + 4×6 = 318 px, cách d-pad khoảng 28,2 ≈ 28 px. Năm ô là mức đã được kiểm chứng ở thể loại này theo quyết định người dùng; mỗi phái có 8 chiêu cần ô nên người chơi phải chọn. Đây là tính toán bố cục từ kích thước đã chốt, không phải lần thử thiết bị mới.
- **Đồng bộ A0:** hiển thị, phong cách B/palette_v3, cụm nút/HUD, chạy cổ điển, nhảy/khinh công/lộn đỉnh; giữ số đo chi tiết tại `13_thong_so.md`. Không thay nội dung A0 hay quy trình ghép bộ phận đã ký duyệt trong tài liệu nguồn.

### Từng chỗ sửa trong GDD

Số dòng dưới đây tính trên main `5577fa5` trước khi sửa; nội dung cũ → mới:

- **Dòng 1212:** Giao diện tham khảo client Ninja School bản 2.0.1 bạn gửi, nhưng chuyển từ bàn phím điện thoại cũ sang màn hình cảm ứng nằm ngang. Client Ninja School gán 6 kỹ năng vào các phím Q, W, E, 7, 8, 9 và có nút Tự đánh; game mình giữ đúng 6 ô kỹ năng và chế độ tự đánh. → Giao diện cảm ứng nằm ngang theo kết quả A0 đã chốt. Hàng kỹ năng có 5 ô chiêu; người chơi chọn 5 trong 8 chiêu chủ động/hỗ trợ của phái (kể cả tuyệt kỹ) để xếp vào ô; chiêu nội tại tự có hiệu lực, không cần ô. Chế độ Tự đánh giữ theo mô tả bên dưới.
- **Dòng 1216:** | Góc trên trái | Chân dung Đinh Bộ Lĩnh, cấp, thanh HP và MP, biểu tượng hiệu ứng đang có (thức ăn, chiêu hỗ trợ, choáng) | → | Góc trên trái | Vòng cấp độ, thanh máu và thanh nội lực |
- **Dòng 1217:** | Góc trên phải | Bản đồ nhỏ, tên bản đồ, nút menu, nút túi đồ, nút Nạp | → | Góc trên phải | Nút menu, bản đồ nhỏ |
- **Dòng 1219:** | Góc dưới trái | Cần điều khiển ảo, nút nhảy | → | Góc dưới trái | D-pad 3 nút nhìn thấy (←, →, ↑ nhảy), hai vùng chéo vô hình sát hai bên ↑ để nhảy chéo; không dùng cần analog ảo hay phím nhảy tách riêng |
- **Dòng 1220:** | Góc dưới phải | Nút tấn công lớn, 6 ô kỹ năng xếp vòng cung quanh nó, nút lên xuống thú cưỡi | → | Góc dưới phải | Nút CHÉM lớn ở góc; đổi mục tiêu phía trên; bình máu phía trên bên trái và bình nội lực bên trái CHÉM |
- **Dòng 1221:** | Giữa cạnh dưới | 2 ô dùng nhanh cho thuốc HP và MP, nút Tự đánh | → | Giữa đáy | Hàng 5 ô kỹ năng vuông |
- **Dòng 1224:** Mỗi ô kỹ năng hiện vòng hồi chiêu → Kích thước và neo cụm nút xem [HUD trong trận](06_screens.md#hud-trong-trận-chuẩn-từ-a0) và [bảng thông số](13_thong_so.md). Nút Tự đánh và thao tác lên/xuống thú cưỡi chưa có vị trí chốt trong HUD A0; cần duyệt bố cục ở Mốc A. /  / **Di chuyển và nhảy:** kiểu cổ điển đạt tốc độ chạy ngay khi bấm, buông thì hãm ngắn; quay đầu có nhịp dừng và khung đầu chỉ đổi mặt. Trên không đổi hướng tức thì. Nhảy dùng cùng trọng lực khi lên và xuống, không treo ở đỉnh; giữ ↑ hoặc vùng chéo thì nhảy lại khi chạm đất. Nhảy chéo bằng vùng chạm vô hình, đồng thời giữ hướng tương ứng. Khinh công cần nhả rồi bấm lại gần đỉnh khi còn đi lên để bật thêm, tối đa một lần mỗi cú nhảy; giữ liên tục không tính là bấm mới. Mỗi cú nhảy và cú khinh công đều có lộn người ở đỉnh, chỉ xoay hình nhân vật, không xoay hitbox. Các tốc độ, thời gian và cửa sổ kích hoạt lấy từ [13_thong_so.md](13_thong_so.md); kiểu cũ chỉ giữ trong prototype để so sánh. /  / Mỗi ô kỹ năng hiện vòng hồi chiêu
- **Dòng 1238:** Cộng điểm, kéo chiêu vào 6 ô trên màn hình chơi → Cộng điểm; 5 ô chiêu; người chơi chọn 5 trong 8 chiêu chủ động/hỗ trợ của phái (kể cả tuyệt kỹ) để xếp vào ô; chiêu nội tại tự có hiệu lực, không cần ô
- **Dòng 1321:** - **Độ phân giải gốc 640×360**, phóng to theo số nguyên, lọc ảnh kiểu nearest cho pixel art (cài trong Project Settings: kích thước cửa sổ, chế độ stretch và scale mode integer). Đây là thông số tạm thời, chốt sau khi xác nhận phong cách ở P0. → - **Hiển thị đã duyệt A0:** độ phân giải gốc **960×540**; stretch **canvas_items**, aspect **expand**, scale **fractional**, lọc texture **nearest**. Viewport logic rộng **960–1200 px** theo tỉ lệ máy. Nhân vật người cao **96 px**, khung **128×128**. Android chạy **fullscreen + immersive**, ẩn thanh trạng thái và thanh điều hướng. Chi tiết và trạng thái duyệt xem `13_thong_so.md`.
- **Dòng 1355:** điểm kỹ năng từng chiêu, 6 ô chiêu, HP và MP hiện tại, danh hiệu. → điểm kỹ năng từng chiêu, HP và MP hiện tại, danh hiệu; lưu lựa chọn và thứ tự 5 ô chiêu; người chơi chọn 5 trong 8 chiêu chủ động/hỗ trợ của phái (kể cả tuyệt kỹ) để xếp vào ô; chiêu nội tại tự có hiệu lực, không cần ô.
- **Dòng 1480:** - **Phong cách mỹ thuật cuối cùng:** mặc định pixel art chibi ở độ phân giải gốc 640×360, xác nhận sau khi xem ba ảnh P0 trong Design Kit. → - **Phong cách đã chốt (không còn là quyết định mở):** phương án B, pixel bán hiện đại, dáng khoảng 4 đầu, **palette_v3 32 màu**. Theo `01_art_bible.md`; không dùng khối STYLE-B vẽ tay lịch sử.
- **Dòng 1507:** **Bước 1 — Chốt phong cách.** Chạy prompt ở mục 3 để ra ba phương án phong cách cho cùng một cảnh. Chọn một, rồi chỉ dùng đúng một khối phong cách ở mục 2 cho mọi prompt về sau. Đề xuất phương án A (pixel art chibi), vì nhân vật nhỏ, đọc rõ trên điện thoại, chạy nhẹ trên máy yếu và hợp với cách vẽ nhân vật theo bộ phận đã chốt ở Phần 6. → **Bước 1 — Theo phong cách đã duyệt.** Phương án B là pixel bán hiện đại, khoảng 4 đầu, palette_v3 32 màu. Không mở lại lựa chọn P0; dùng nguyên văn STYLE và AVOID hiện hành trong `01_art_bible.md`.
- **Dòng 1523:** **STYLE-A — pixel art chibi (đề xuất):** /  / ``` / Style: 2D pixel art for a side-scrolling mobile action RPG, chibi proportions about 3 heads tall, clean 1-pixel dark outline, limited palette of 32 colors, soft 2-tone cel shading, bright readable colors, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire. / ``` /  / **STYLE-B — vẽ tay 2D (phương án dự phòng):** /  / ``` / Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire. / ``` /  /  → **STYLE — pixel bán hiện đại (phương án B đã duyệt):** /  / Dùng nguyên văn khối STYLE trong `01_art_bible.md`, mục Phong cách. Phương án B đã duyệt không phải khối STYLE-B vẽ tay của khuôn P0 lịch sử trong `03_prompts.md`. Bảng màu áp dụng là palette_v3 32 màu. /  /
- **Dòng 1545:** Chạy prompt này một lần với từng phương án (thay `[STYLE]` bằng STYLE-A, rồi STYLE-B), và một lần không có khối phong cách để xem AI tự đề xuất gì. → P0 đã hoàn tất. Prompt dưới đây chỉ để tra cứu bố cục; nếu dùng cho ảnh mới, `[STYLE]` và `[AVOID]` phải lấy nguyên văn từ `01_art_bible.md`, không chạy lại các phương án lịch sử.
- **Dòng 1548:** a simple health bar and six round skill buttons as placeholder UI at the bottom right → a level ring and health and energy bars at the top left, a menu and minimap at the top right, three visible directional buttons and invisible diagonal touch zones at the bottom left, an attack cluster at the bottom right, and five square skill slots centered along the bottom
- **Dòng 1729:** nhân vật cao khoảng 64 điểm ảnh → nhân vật người cao 96 điểm ảnh trong khung 128×128
- **Dòng 651:** Phí luyện theo cấp viên đích (yên): → Phí luyện tham khảo từ Ninja School theo cấp viên đích (yên của nguồn; chưa quy đổi sang tiền đồng):
- **Dòng 667:** | Tiền (yên) | → | Tiền tham khảo (yên Ninja School; chưa quy đổi) |

### Chỗ giữ lại để người dùng quyết

- **Giá tiền nguồn chưa quy đổi (Phần 2, mục 4–5):** giữ bảng cường hóa ghi yên Ninja School, phí luyện đá và bảng tinh luyện; hai chỗ thiếu nhãn đã bổ sung rõ nguồn và “chưa quy đổi”. Cần người dùng chốt giá tiền đồng sau cân bằng; không tự đổi tên đơn vị mà giữ nguyên số để tránh coi giá nguồn là giá đã chốt.
- **Đối chiếu nguồn:** giữ yên/xu/lượng khi đang mô tả Ninja School hoặc cột “Gốc Ninja School”, gồm Phần 1 mục hệ thống, Phần 2 mục 4 và 10, bảng đổi tên và việc còn phải chốt. Đây không phải tên tiền của Cờ Lau; mọi chỗ mô tả tiền game hiện tại dùng tiền đồng/ngân lượng/ngân phiếu. Giữ “yên” trong yên ngựa/đất nước đã yên, cùng các từ số lượng, lực lượng… theo nghĩa thường.
- **HUD ngoài A0 (Phần 5, mục 1):** vị trí nút Tự đánh và thao tác lên/xuống thú cưỡi chưa được chốt; giữ chức năng, chưa gán vị trí mới hay coi là đã duyệt A0. Người dùng quyết khi duyệt HUD Mốc A.
- **Prompt lịch sử (Phần 7):** khối AVOID và quy trình chuyển sprite cũ vẫn là nội dung tham khảo; dùng `01_art_bible.md`/`04_review.md` khi sản xuất, không mở lại quy trình ghép bộ phận đã chốt.

## 28/10/2026 — Bổ sung HUD đầy đủ sau đồng bộ GDD

- **Mã:** `gdd_full_hud_restore`. Sửa trên nhánh `docs/gdd-sync-a0`; HUD A0 chỉ là khối giữ chỗ để kiểm chứng cụm điều khiển, không thay cho HUD đầy đủ.
- **GDD Phần 5 mục 1 và 06_screens — HUD trong trận:** thêm lại dải hiệu ứng thức ăn/chiêu hỗ trợ/choáng dưới thanh máu và nội lực; tên bản đồ dưới bản đồ nhỏ, nút túi đồ và nút cửa hàng ở cụm trên phải. Bản đầu chỉ có cửa hàng món vĩnh viễn, không có ngân phiếu nạp; sửa tên Túi đồ/Nạp trong SCR-05 cho khớp.
- **Cụm phải:** bổ sung nút Tự đánh và lên/xuống thú cưỡi; chức năng giữ nguyên. Các thành phần bổ sung đều ghi “vị trí chốt ở Mốc A”; không che cụm CHÉM hoặc hàng 5 ô kỹ năng ở viewport 960 px.
- **Giữ nguyên:** d-pad và vùng chéo, CHÉM, đổi mục tiêu, hai bình, hàng 5 ô kỹ năng cùng các kích thước/thao tác A0 đã duyệt. Không sửa prototype hay bảng thông số.
- **Cửa duyệt:** thêm checklist chưa đánh dấu tại Mốc A nhóm 4 trong `11_design_freeze.md`, yêu cầu duyệt HUD đầy đủ trên viewport 960 và 1200 px. File này được sửa theo yêu cầu bổ sung cụ thể trong cùng lượt; ngoài ba file nêu đầu yêu cầu chỉ thêm đúng checklist này.
- **Kiểm tra:** soát khác biệt tài liệu và lỗi khoảng trắng; đây là cập nhật đặc tả, chưa dựng hay thử bố cục HUD đầy đủ trên thiết bị.

## 28/10/2026 — Giai đoạn 1 bước 1: rig greybox Đinh Bộ Lĩnh

- **Mã:** `chr_dbl_rig_greybox`; nhánh `feat/g1-rig-greybox`, từ main `e14aefc`. Ngoại lệ prototype theo yêu cầu người dùng, mã bỏ đi; chưa qua Mốc A, không chép sang game thật.
- **Nguồn đọc:** AGENTS, CONFLICTS/router, godot-animation/animation-system; art bible, danh sách asset, review, đặc tả hoạt ảnh và thông số A0. Không chạy helper của skill, không cài addon hay dùng ảnh/mã game khác.
- **Đo ảnh:** `art/reference/ref_dinh_bo_linh.png` 1735×576, ROI nghiêng [610,20,780,570). Silhouette y=[40,560), cao 520 px; mốc cổ 174/hông 299 chọn bằng mắt. Script đo đầu kèm tóc 134 px → 24,738 px, thân 125 → 23,077 px, chân/bàn chân 261 → 48,185 px khi chuẩn hóa cao 96. Greybox đề xuất 24/24/48; ảnh, script nguyên văn, phương pháp và báo cáo có hash tại `16_rig_nhan_vat.md`/`prototype/rig/reports/`. Không tạo art mới hay sửa ảnh nguồn.
- **Rig:** 16 mảnh màu riêng: đầu/tóc, thân, tay trên/dưới/bàn tay gần/xa, đùi/cẳng/bàn chân gần/xa, đao/cung. Bảng khung, pivot, khớp cha/attach, lớp, phần vẽ bù, giới hạn góc và quy ước chr_dbl_t1…t7 tại `16_rig_nhan_vat.md`. Chọn cây Node2D + AnimationPlayer vì mảnh cứng, dễ kiểm khớp và thay trang bị, chưa cần skin/IK.
- **Dữ liệu:** JSON bộ phận và 13 clip/48 frame: đứng, chạy, nhảy lên, lộn, rơi, chạm đất, quay đầu, ba nhát Đao, bắn Cung, trúng đòn, ngã. Đề xuất sáu pose lộn/0,20 s và hai pose quay đầu/0,05 s; giữ nhịp A0. Nhát cơ bản 0,30 s, trúng 0,10–0,20; combo 2–3 chỉ preview. Marker hit/cancel/spawn không thêm logic chiến đấu, đạn hay âm thanh.
- **Cảnh mới:** `rig/rig_greybox.tscn` kế thừa A0; adapter đọc trạng thái thật và thay sprite qua công tắc **Rig greybox** trong ⚙. Công tắc cung chỉ đổi hình/bắn xem thử; bộ chọn clip để xem hurt/ngã/combo chưa có trong A0. Nút về A0 trong ⚙, nút mở cảnh ở A0 gốc. Không sửa scripts A0, tuning, hitbox, điều khiển, bản đồ hay nhịp vật lý; `main.tscn` chỉ thêm node nút chuyển cảnh.
- **Contact sheet:** instantiate/seek chính `rig.tscn` bằng Godot, xuất polygon sau transform vào `evaluated_frames.json`; Python/PIL tô polygon theo z thành 13 PNG tại `prototype/rig/contact_sheets/`. Không imagegen, không dựng pose thứ hai trong Python. Đây là raster của rig đã tính pose, không phải screenshot GPU của toàn cảnh. Khi soát đã sửa pose ngã bằng dữ liệu bù cao độ để tiếp đất.
- **Kiểm tra:** Godot **4.7.2.stable.official.ed1daf0bf**, dùng binary 4.7.2 riêng vì lệnh godot mặc định của môi trường là 4.6.3. Chạy ba lệnh README, test rig và mở cảnh rig headless; đầu ra nguyên văn ghi trong commit message. Test đủ số frame, điểm nối mọi pose, giới hạn góc, chân đứng/chạm đất đúng y=0, lộn đủ 360°/0,20 s và cả hai vòng khinh công hoàn tất trước đáp cùng cao độ; trạng thái A0 chọn clip đúng, tắt rig khôi phục sprite, body/slash không xoay theo hình. Chưa thử Android hoặc nghiệm thu cảm giác/mỹ thuật mới.
- **Tiến độ:** asset list vẫn `[ ]`, ghi “đã dựng bản thử, chưa duyệt”; bổ sung đề xuất số pose vào 09, không chuyển số nghệ thuật thành Đã duyệt. Chờ người dùng duyệt tỉ lệ/khớp/pose và xem trực tiếp bằng Godot 4.7.2 trước bước vẽ bộ phận.

## 28/10/2026 — Giai đoạn 1: bộ phận vẽ bậc 0 (đang làm, chưa duyệt)

- **Mã:** `chr_dbl_parts`; nhánh `feat/g1-parts-art`, từ main `77acc3d`. Chỉ art/, tools/, prototype/rig/, docs/. Không sửa physics/hitbox/điều khiển A0, không đánh dấu asset hay Mốc A đã duyệt.
- **Concept:** 1 lần imagegen (giới hạn 4), một tờ 16 mảnh tách rời nghiêng phải, nền xanh. Ảnh tham chiếu đính kèm nguyên `art/reference/ref_dinh_bo_linh.png`. Nguồn giữ nguyên tại `art/concept/characters/chr_dbl_parts_concept.png`; prompt nguyên văn bên dưới và trong `.prompt.txt`. Không dùng imagegen cho báo cáo/contact sheet/ảnh ×4.
- **Chuẩn hóa:** `tools/cut_parts.py` tìm 16 vùng foreground liên thông; dùng lại green_mask/detect_period/nearest/load_groups của snap_pixel. Nắn lưới, lấy trung vị từng ô để co đúng parts.json, giới hạn 17 màu, viền ngoài 1 px, bỏ cụm alpha rời <2 px. PNG trong `art/sprites/characters/chr_dbl_parts/`; bản sao đúng byte trong `prototype/rig/art_parts/`, chưa phải luồng chuyển art đã duyệt.
- **Vẽ bù tự động:** kéo màu trung vị vùng gần khớp thành nửa hình tròn theo bề rộng mảnh ở đầu vai/khuỷu/hông/gối và phần cha bị che. Không coi đây là giải phẫu do họa sĩ vẽ; không nới canvas/pivot. Cổ dùng đường kính 8 px để không biến đầu 18×24 thành khối cổ rộng.
- **Khắc phục khe khi gập:** phép kiểm rộng phát hiện PNG trong khung cố định không chứa đủ đầu tròn ở cổ/khuỷu/gối. Script vẽ hai nửa bán nguyệt vào PNG và sinh lớp màu bù dưới texture tại cổ/vai/khuỷu/hông/gối, có thể vượt mép khung ảnh một ít; giữ nguyên 16 PNG, pivot/bone/hitbox. Không thêm lớp tròn ở bàn chân/tay/vũ khí. Vùng bù là tự động, còn cần duyệt thẩm mỹ.
- **Đầu:** lưu PNG/ma trận trước và sau; `tools/chr_dbl_head_edits.json` ghi tọa độ/chỉ số màu sửa mắt, mũi, miệng bằng script, sau đó giữ lại viền ngoài. Đây là bản Codex sửa đề xuất; **Claude chưa soát**, không giả nhận đã được Claude/người dùng duyệt. Bảng màu và hai ma trận 24×18 tại `reports/g1_parts_art_report.md`.
- **Rig:** Sprite2D nearest đúng pivot, công tắc “Bộ phận vẽ / Khối màu” trong ⚙ của cảnh rig; vũ khí/lớp/khớp và timeline giữ nguyên. Exporter lấy affine Sprite2D + khớp thật từ scene; script PIL đọc alpha PNG để đo khe và dựng tờ khung.
- **Kiểm tra file thật:** 16 mảnh đúng kích thước, 0 pixel ngoài palette, 0 pixel bán trong suốt; 672 cặp khớp hiện trong 48 khung/13 động tác, độ dày khe lớn nhất 0,50 px, 45 mẫu nền thuộc vùng nối, không có ca vượt 1 px. Phương pháp: raster nearest 4× từ transform scene, quét toàn bộ dây cung theo tám hướng trong đĩa khớp; chỉ đếm nền nằm giữa mực của hai mảnh khác nhau. Độ dày khe đo bằng hai lần khoảng cách tới mực gần nhất; chiều dài đường cắt lướt ghi riêng, không nhầm với độ dày. Đồng thời yêu cầu tâm khớp cách mực không quá 1 px. Không khẳng định đã kiểm mọi thời điểm nội suy/GPU Android.
- **Sản phẩm xem:** contact sheet texture idle/run/jump_up/apex_flip/slash_1/shoot/hurt; ảnh idle 1× và ×4 tạo bằng Image.resize(NEAREST) từ file thật. Đường đi tại `prototype/rig/contact_sheets/art/`. Số liệu, script nguyên văn và đầu ra tại báo cáo; đầu ra các lệnh headless ghi nguyên văn trong commit message.
- **Còn chờ:** Claude/người dùng soát từng mảnh, khuôn mặt, cảm giác trang phục, các đường nối và chuyển động trong Godot 4.7.2/Android. Kiểm kỹ thuật đạt không tự duyệt mỹ thuật. Không sao chép sang co_lau_game.

### Prompt imagegen nguyên văn (lần 1/4)

```text
Create ONE concept sheet of EXACTLY SIXTEEN fully detached character rig pieces on a perfectly flat pure green #00FF00 background, using the attached Vietnamese young man's RIGHT-FACING SIDE VIEW as the appearance reference. Tier zero costume: undyed short-sleeved rustic linen tunic, dark brown knee-length pants, bare feet, small topknot, black hair; no armor. This is a parts concept, NOT an animation sheet or assembled character, NOT a results table. No writing, labels, numbers, letters, grid lines, joints drawn, watermarks or shadow cast on the green background.

Arrange sixteen pieces in a spacious regular FOUR BY FOUR layout, ONE detached piece centered per invisible cell, large green gaps between all pieces. Draw near and far pieces separately, similarly scaled; far pieces slightly darker. Keep the specified order exactly:
Row 1: head including hair/topknot in right-facing profile; torso/tunic alone with waist belt, no arms; near upper arm with short sleeve and bare upper arm; far upper arm with short sleeve and bare upper arm.
Row 2: near forearm bare; far forearm bare; near hand in holding pose; far hand in holding pose.
Row 3: near thigh with dark knee-length pants; far thigh with dark knee-length pants; near bare shin; far bare shin.
Row 4: near bare foot pointing right; far bare foot pointing right; a simple broad single-edged DAO held vertically point-up, grip at lower end; a simple vertical bamboo BOW, grip at centre, without a drawn bowstring (the rig draws the string).
All arm and leg pieces in straight neutral downward orientation, with rounded fully painted joint ends and generous occluded overlap at shoulder/elbow/hip/knee. Torso is side view. Head must have a readable single eye, nose profile and mouth. Feet are strict right-facing side view. Weapons same rustic tenth-century visual vocabulary, no decorative script. Do not add any additional objects or intact person. Suggested final part sizes for proportions only: head18x24, torso20x26, upper arms8x19, forearms7x17, hands7x8, thighs10x24, shins8x24, feet14x6, dao5x34, bow6x38. The source sheet should be drawn generously large and will be reduced by median-cell sampling; do not print dimensions.
Style: 2D pixel art for a side-scrolling mobile action RPG, semi-realistic proportions about 4 heads tall, clean dark outline, 32-color palette, 3-tone shading with soft highlights, readable silhouettes, light source from top-left. Setting: northern Vietnam in the 10th century: limestone karst, rice fields, earthen ramparts, thatched or simple clay-tiled roofs, white reed-plume banners.
Avoid: Japanese ninja or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

## 28/10/2026 — Sửa tỉ lệ chung và viền bộ phận bậc 0

- **Mã:** `chr_dbl_parts_common_scale`. Người dùng chỉ ra bản kỹ thuật đạt nhưng mỹ thuật hỏng do co từng mảnh vào ô. Lượt này không sinh lại concept, không áp dụng sửa mắt/mũi/miệng cũ.
- **Tỉ lệ:** ghép thử nguồn theo mốc 24/24/48: đường đầu→cổ 218, cổ→ghép quần dưới vạt 214, chân 414, tổng 846 px. Một hệ số s=96/846≈0,113475177305 cho cả x/y của mọi mảnh; trung vị ô nguồn, không đổi aspect để vừa khung. Các đoạn mới 24,738/24,284/46,979 px. Mốc chọn bằng mắt, ghi nguồn/crop/landmark; cần duyệt rig, không giả nhận dạng giải phẫu tự động.
- **Cấu hình:** giữ parts_greybox.json và animations_greybox.json; parts.json đo khung/pivot/attach mới. Công tắc dựng đúng cấu hình của từng chế độ. Bảng cũ→mới trong 16_rig_nhan_vat.md, retarget pose art giữ timing/event và chân trụ; không sửa physics/hitbox/điều khiển A0.
- **Viền:** bỏ nét cắt quanh mảnh, chỉ bôi nét 1 px trên bao dáng đứng từ scene; đầu nối và lớp bù tự động không viền. Tóc dùng màu vật liệu tối, giữ feature màu nguồn trong vùng mắt/mũi/miệng; không dùng danh sách sửa pixel khuôn mặt.
- **Tay/chân:** giữ đủ sáng/trung/tối; bàn chân giữ tỉ lệ nguồn, gót và mũi. Đầu mới 23×25, cổ dưới cằm≈2,50 px, da mặt ngang 13/23≈56,52%; ma trận không chỉnh feature chờ Claude trả.
- **Báo cáo:** chuyển docs/17_parts_art_report.md → docs/reports/g1_parts_art_report.md, sửa mọi liên kết, dành số 17 cho 17_ngoai_hinh.md. Lưu raw uniform PNG, mốc đo và bản cấu hình greybox để đối chiếu.
- **Kiểm:** PNG đúng khung mới, 0 ngoài palette/0 alpha bán trong; 672 cặp khớp/48 khung/13 động tác, khe lớn nhất 0,50 px, 0 ca vượt 1 px. Dáng đứng duỗi từ scene cao 96 px; idle thấp hơn 1 px do pose. Đếm được 8 pixel màu outline trong đầu/mặt, liệt kê tất cả tọa độ ở báo cáo, không có nét viền nội bộ ở mối nối; giữ pixel nguồn này cho Claude soát theo yêu cầu không sửa mặt.
- **Sản phẩm:** tạo lại các contact sheet art và idle ×4 bằng script/NEAREST từ file thật, không imagegen. Headless và script output nguyên văn trong commit message. Chưa duyệt art, chưa thử lại Android.

## 28/10/2026 — Đầu Claude, sửa nhóm màu và chiều dài tay

- **Mã:** `chr_dbl_parts_claude_head_arm`. Theo ma trận người dùng gửi: **đầu do Claude vẽ tay từng pixel**. Giữ nguyên 23×25/pivot/attach; không cleanup, không sửa mặt hoặc bôi viền lại đầu. Lưu ma trận nguyên văn cạnh art work; kiểm RGBA trùng tuyệt đối hai bản head.png. Cổ: khe 0,00 px qua 48 frame.
- **Màu:** tóc chỉ O/H và ánh L=#59443E; da dùng skin; ngoài quần không dùng pants trừ L tóc. Body/upper_arm dùng #C3A98A chủ đạo, #89745E/#554638 bóng, #EAD8B8 là sáng. Script kiểm nhóm riêng; tỉ lệ sáng đo trên pixel vải lần lượt body 11,029%, tay gần 9,589%, tay xa 10,000%, đều ≤15%. Đếm đủ từng màu tại báo cáo.
- **Tay:** chỉ rút trục dài upper_arm/forearm còn 60%; giữ ngang, cập nhật pivot và attach ở cả khớp khuỷu/cổ tay. Bảng cũ→mới ở 16; retarget pose theo xương mới, giữ nhịp/event và A0 physics. Scene đo đầu ngón y=−33 ở đứng duỗi, −32 ở idle cho cả gần/xa.
- **Kiểm:** 16 PNG đúng khung hiện tại, 0 ngoài palette, 0 alpha bán trong, 0 pixel sai nhóm; 672 cặp khớp qua 48 frame/13 động tác, khe tối đa 0,50 px. Viền O nội bộ: 17 pixel, đều thuộc đầu Claude nguyên mẫu, liệt kê tọa độ; H là màu tô tóc được báo riêng, không coi là lỗi viền. Ngoài đầu không có viền nội bộ. Không tự xóa nét đầu được người dùng cung cấp để ép số thành 0.
- **Kết quả:** xuất lại 15 tờ art và idle ×4 từ file 1× bằng NEAREST. Godot 4.7.2, ba lệnh README và rig tests đạt; nguyên đầu ra trong commit message. Báo cáo tại reports/g1_parts_art_report.md; các bộ phận còn cần duyệt mỹ thuật, chưa thử Android mới.

## 28/10/2026 — Ngoại hình và rà nguồn/pháp lý

- Chốt: thời trang theo ô, một dạng cố định, gồm cả vũ khí, có chỉ số; hai nguồn IAP/ingame. Giới hạn 10–15%, hiệu ứng cường hóa và frame vẫn đề xuất.
- Thêm 17/18, đồng bộ part_set, asset list, giao dịch, thông số, animation và checklist. Không sửa art/tools/prototype.
- Pháp lý: cần luật sư xác nhận trước Mốc B; chưa kiểm văn bản online, không trình bày giả định G4/thủ tục/giờ chơi là kết luận pháp lý áp dụng.
- C6: 433 tracked paths; Java/JAR/CLASS: []; image names matching conservative reference-resource patterns: []. Filename scan only, no reference asset corpus/hash comparison available; cannot establish provenance from names alone.

### Từng thay đổi GDD (cũ → mới)

- chuyển thể từ source server Ninja School Online → tham khảo thể loại.
- dựa trên source server bạn gửi (Java, bộ `nso-core` và database `nja.sql`) → dựa trên tham khảo thể loại.
- con số lấy thẳng từ code → con số tham khảo cần tự thiết kế lại.
- Số liệu lấy từ `GameScr.java`. → Số liệu tham khảo thể loại — Phải tự đặt lại số trước Mốc A..
- Chỉ đổi ngoại hình, không cộng chỉ số → Có chỉ số cộng thêm, theo ô và giới hạn tại 17_ngoai_hinh.md.
- Game mình giữ y nguyên → Game mình tham khảo thể loại.
- Bảng tại dòng gốc 549: cột Gốc Ninja School → Bỏ cột đối chiếu, giữ nguyên số.
- Bảng tại dòng gốc 566: cột Gốc Ninja School → Bỏ cột đối chiếu, giữ nguyên số.
- Bảng tại dòng gốc 628: cột Gốc Ninja School → Bỏ cột đối chiếu, giữ nguyên số.
- Bảng tại dòng gốc 790: cột Gốc Ninja School → Bỏ cột đối chiếu, giữ nguyên số.
- Bảng tại dòng gốc 804: cột Gốc Ninja School → Bỏ cột đối chiếu, giữ nguyên số.
- Bảng tại dòng gốc 845: cột Gốc Ninja School → Bỏ cột đối chiếu, giữ nguyên số.
- Bảng tại dòng gốc 1019: cột Gốc Ninja School → Bỏ cột đối chiếu, giữ nguyên số.
- Bảng số tham khảo Phần 2 (chiêu/cường hóa/giá/tỉ lệ/kinh nghiệm/phí luyện) → Đánh dấu Phải tự đặt lại số trước Mốc A, chưa thay số.
- Thiếu part_set/thời trang theo ô, có chỗ ghi chỉ đổi hình → Thêm mục Hệ thống ngoại hình và quy tắc 17, có chỉ số/hai nguồn/trần đề xuất.

### Chờ người dùng quyết

- Trần chính xác 10 hay 15%, cách chuẩn hóa từng chỉ số, mẫu IAP/ingame từng ô, biến thể nón và mặt nạ lịch sử (tuồng/chèo cần duyệt cách điệu, không khẳng định tồn tại nguyên dạng thế kỷ 10).
- Số liệu riêng thay bảng tham khảo, thiết kế HUD cuối, mốc hiệu ứng/frame.
- Phương án phát hành Việt Nam và kết luận luật sư; tác quyền cần rà nội dung/hash khi có bộ nguồn đối chiếu.

## 29/10/2026 — Trung tính hóa tài liệu repo công khai

- **Mã:** `neutral_references`; từ main `87ade17`, nhánh `docs/neutral-references`. Chỉ sửa docs/ và AGENTS.md.
- Repo công khai: bỏ tên thương mại/đối chiếu vật phẩm và các phát biểu về tiếp cận mã hoặc dữ liệu sản phẩm khác; bỏ danh sách liên kết tham khảo riêng, cột đối chiếu, giữ cột Cờ Lau. Viết mô tả cơ chế bằng ngôn ngữ của dự án.
- Giữ quyết định, cơ chế, bảng số Cờ Lau và dấu “Phải tự đặt lại số trước Mốc A”. Đơn vị giá tham khảo chưa quy đổi được ghi rõ, không coi là giá tiền đồng đã chốt.
- Thay từ mô tả trang phục bị cấm trong prompt bằng cách diễn đạt tương đương; không bỏ ràng buộc lịch sử. Nhật ký các lượt cũ giữ nguyên byte, kể cả prompt lịch sử.
- Chạy phép rà theo yêu cầu; toàn bộ kết quả còn lại chỉ thuộc các mục nhật ký cũ, không có dòng ngoài nhật ký. Nguyên đầu ra trong commit message và báo cáo trả người dùng.


## 29/10/2026 — g1_parts_polish — v1, đang làm/chưa duyệt

- Nhánh `fix/g1-parts-polish` từ main `8997b8c`. Không sinh ảnh mới; concept và ảnh
  tham chiếu `art/reference/ref_dinh_bo_linh.png` giữ nguyên. Không có prompt mới.
- Cho phép limestone riêng vũ khí: đao #A5B8B0 chủ đạo, bóng #718B87, sáng
  #D9DDD0, nét #17151A; cán/vỏ belt. Cung gỗ belt, dây sáng #D9DDD0.
- Hai đùi bỏ skin, chỉ pants và outline. Giữ nguyên đầu do Claude vẽ tay từng pixel,
  kích thước, pivot, attach và số đo/điều khiển A0.
- Run/slash_1–3 giảm 35% góc gập hai gối; giải lại hông nâng, giữ chân trụ/chân
  chém trên đất; chân vung vẫn trên đất. Không đổi số khung/thời lượng/event.
- Godot 4.7.2: ba lệnh headless README, rig/art/visual tests và các kiểm PIL đều
  đạt. 16 PNG không sai palette/nhóm màu/bán trong suốt; 672 kiểm khớp trên
  48 pose/13 động tác, khe lớn nhất 0,50 px; cổ 0,00 px.
- Xuất lại 15 contact sheet art và idle 1×/×4 từ scene, ×4 NEAREST; không imagegen
  cho ảnh kết quả. [Báo cáo, script và ảnh](reports/g1_parts_polish_report.md),
  [nguyên đầu ra](reports/g1_parts_polish_output.txt); nguyên đầu ra cũng trong
  commit message. Bộ phận vẫn đang làm, chưa được duyệt mỹ thuật.


## 29/10/2026 — g1_weapon_direction — v1, đang làm/chưa duyệt

- Tiếp trên `fix/g1-parts-polish`: sửa lỗi đao chĩa từ nắm tay về khuỷu/ngực.
  Xoay 180° quanh điểm cầm, bù góc bàn tay; idle/turn chúc xuống, chếch ra trước.
  Giữ pivot/attach, hình dáng bộ phận, màu, góc chân và điều khiển/hitbox A0.
- Test scene thật in góc từng frame: 48 pose/13 động tác và 11 pose run/shoot
  trái, tổng 59. Góc đao thường ≈6,801° (≤30°); không mũi nào nằm giữa khuỷu
  và cổ tay. Cung ở nắm tay xa, góc với cẳng tay 89,510°, sai lệch điểm cầm 0 px.
- Godot 4.7.2: ba lệnh headless README và toàn bộ rig/art/visual/PIL checks đạt;
  672 kiểm khớp, khe tối đa 0,50 px. Xuất lại contact sheet và idle ×4 NEAREST
  từ scene; không imagegen, không có prompt mới. Nguồn art/ảnh tham chiếu cũ giữ nguyên.
- [Báo cáo và script](reports/g1_weapon_direction_report.md), [nguyên đầu ra](reports/g1_weapon_direction_output.txt);
  đầu ra cũng trong commit message. Chờ người dùng duyệt mỹ thuật.


## 29/10/2026 — milestone_a_by_act — v1, đặc tả chia mốc

- Ngày: 29/10/2026.
- Mã: milestone_a_by_act.
- Thay đổi: chia checklist trước khi code thành A1–A5 theo hồi; A1 gồm mở đầu/Hồi 1 và toàn bộ hệ thống lõi, sau A1 được bắt đầu code game thật. Nội dung Hồi n chỉ đưa vào game sau An; thiết kế Hồi 2–5 làm song song với code. Hệ thống mới và bậc trang bị phân theo quyết định, mọi bảng số hệ thống lõi duyệt đủ ở A1.
- Đồng bộ tên mốc trong README, AGENTS và tài liệu; giữ thứ tự giai đoạn sản xuất. Thêm bảng đối chiếu từng checkbox, căn cứ nhiệm vụ và các điểm (Cần người dùng xác nhận). Mỗi mốc có tag thiết kế riêng khi được duyệt, repo game cập nhật GDD/DESIGN_VERSION theo tag mới nhất.
- Lý do: quyết định người dùng ngày 29/10/2026.
- Giữ nguyên mục A0, Mốc C, toàn bộ quyết định lịch sử, dòng ký A0 và trạng thái các điều kiện đã có. Không đổi số liệu, không tạo ảnh, không sửa prototype/art/tools/co_lau_game. Không có prompt hoặc ảnh tham chiếu mới.
- Tác vụ này chỉ sửa cách chốt thiết kế, không có nghĩa A1–A5 đã được duyệt; không gắn tag nghiệm thu. Báo cáo: `docs/reports/milestone_a_by_act_mapping.md`.


## 29/10/2026 — a_confirmations — v1, xác nhận phân mốc

- Mã: a_confirmations.
- Lý do: quyết định người dùng ngày 29/10/2026 về các điểm phân mốc sau khi chia A1–A5.
- Thay đổi: chuyển ải Thần Phù sang A3; Đằng Châu/Đỗ Động/Bạch Hạc sang A4; năm bóng boss Ảo cảnh Vạn Thắng sang A5 để chọn từ concept A1–A4; Cổ Loa thuộc [Phạm vi sau], chưa vào A nào và không nằm trong 29 bản đồ. Gộp SCR-21 vào B, giữ SCR-19 chỉ thuộc C; Chuyển hóa/Ấn truyền công ở A1 vì chung màn/bảng cấp với cường hóa.
- NPC: gộp Đinh Công Trứ, lái buôn đường sông và quan thu lương vào A1 theo phạm vi mở đầu/kinh tế lõi; Trịnh Tú vào A3 cùng căn cứ. Không tự phân NPC có tên chưa có nhiệm vụ; thêm vào mốc của hồi khi có nhiệm vụ dùng tới.
- Hiệu ứng: số liệu/đặc tả đủ 20 chiêu vẫn A1; concept hiệu ứng chủ động/hỗ trợ chia theo cấp mở 10 → A1, 20/25 → A2, 30/35 → A3, 40/50 → A4, 60 → A5; bốn nội tại không cần concept hiệu ứng. Cập nhật bảng đối chiếu và phục hồi ba dòng lịch sử README nguyên văn từ 7cc3b1e.
- Giữ nguyên trạng thái duyệt, A0, C, các quyết định lịch sử, chữ ký A0 và anchor còn lại; không đổi số liệu game, không tạo ảnh, không sửa prototype/art/tools/co_lau_game. Chốt phân mốc không có nghĩa nghiệm thu A1–A5.
- Báo cáo: `docs/reports/milestone_a_by_act_mapping.md`, mục “Xác nhận 29/10/2026”. Không có prompt hoặc ảnh tham chiếu mới.


## 29/10/2026 — lay_dao_uc_v1 — v1, đang làm/chưa duyệt (A1)

- Theo yêu cầu người dùng: dựng `design/maps/lay_dao_uc_v1.md` (150×17 ô) và
  `lay_dao_uc_boss_v1.md` (60×17 ô), ô32 px Tạm thời. Map quái E phải nối E trái
  đấu trường; chưa làm mã game/lát cắt hay art. Main nền `ca1c6d7`.
- NV9/CS04 đặt Nguyễn Bặc, Đinh Điền và sân đấu tại trại; NV14/CS05 có3 D/cổng
  và3 G/điểm gọi quân. NV15 có boss hai pha,4 lính cung pha2 trên lũy, bậc32 px
  lên được, sân phẳng640 px, R trước cổng khóa; Đánh lại trở về R, không revive tại chỗ.
- Đường bắt buộc: khe64 px, chông64×32, các bậc32 px; nhảy chéo có biên1,5×,
  không cần khinh công. Mặt đất chính y288 và map cao544 chừa vùng nút bên dưới.
- `tools/check_layout.py` tự đọc lưới và số A0 (chỉ đọc prototype), tìm khe/bậc,
  kiểm quỹ đạo/AABB24×88 hai hướng, hộp nút960/1200 tại S/R và trước hố/bẫy0–3 ô,
  gồm dead-zone/look-ahead, miền theo camera và chặn hai mép. Hai bảng ở mỗi file
  chép từ script, không viết tay. Test tĩnh chưa thay chơi thử Godot/Android.
- `render_layout.py` dùng vạch30/37,5 ô, quỹ đạo thường/chéo/khinh công từ công thức,
  PNG và lớp phủ960/1200 tại từng S/R. Sơ đồ dựng bằng PIL, không imagegen;
  không có prompt mới, không tạo/sửa ảnh tham chiếu hay art.
- `08_map_layout.md` thay ví dụ cũ bằng liên kết hai bố cục, bổ sung R và quy tắc
  đường bắt buộc/cách kiểm. `02_asset_list.md` giữ chưa duyệt; Thần Phù A3,
  Đằng Châu/Đỗ Động/Bạch Hạc A4. Không đổi `13_thong_so.md` hoặc checklist nghiệm thu.
- Câu hỏi: địa điểm NV11/NV13 chưa rõ, không tự thêm quái/hào trưởng vào Đào Úc;
  phân bổ3 đợt quân và luật cổng NV14; liên kết map ngoài hai file; bán kính vòng đỏ;
  ngưỡng60% của boss2 pha và báo đòn1,5s theo GDD; kích thước map/báo đòn khác
  bảng tạm ở13. Ghi rõ tại mục6 của từng bố cục, chờ người dùng duyệt.
- Nguyên đầu ra hai check, sáu lệnh render, test phản chứng và kiểm phạm vi/nhật ký
  được chép vào commit message. Chỉ sửa đúng phạm vi, chưa duyệt mục nào.


## 29/10/2026 — dao_uc_greybox — v1, đang chơi thử khối màu/chưa duyệt (A1)

- Quyết định người dùng: giữ Đào Úc150 ô (map quái chung120–180), đấu trường60 ô
  (chung45–60); đồng bộ13, vẫn Tạm thời — chốt sau chơi thử. Boss đầu báo1,5s,
  boss sau rút dần về1,2–0,8s, không dưới0,8; đồng bộ09/13, không sửa GDD.
- NV11: chuột lớn ở Cánh đồng chiêm, lợn rừng ở Bến đò Hoàng Long, hổ con ở Núi đá
  Tràng An. NV13: mỗi hào trưởng ở một trong ba map đó, vị trí chốt khi dựng bố cục.
  E trái Đào Úc ↔ Tràng An; E phải boss sau thắng/CS06 → Đầm lầy Đại Hoàng(NV16).
- c0…31 là vùng an toàn, ngoại lệ quy tắc sinh quái08; M Đinh Điền chỉ đấu tập.
  Tướng tiên phong Hậu Ngô đúng2 pha, chỉ chuyển60%, không ngưỡng30%.
  Giữ nguyên lưới; sau thử quyết thêm tầng bục2–3 và khe c44–45 không đáy/đáy nông.
  Lượt tileset sau cần mặt cắt lũy/rễ/đá vì đất chiếm gần nửa dưới màn hình.
- Nhánh `feat/g1-dao-uc-greybox` từ main `5a2d60b`. Dựng `prototype/dao_uc/`:
  nạp nguyên khối layout trong hai Markdown sao chép giống byte, có manifestSHA256,
  script `sync_layouts.py` và kiểm đối chiếu bản gốc. Không gõ lại lưới; chỉ sửa mục6
  của hai file layout gốc, ảnh/lưới/phần1–5 giữ nguyên.
- Đất va chạm, bục một chiều, chông/rơi → R gần nhất bên trái (trước R đầu dùng S),
  chưa trừ HP; nước nông chậm30%; thang giữ↑/↓, rời bằng←/→ hoặc Space/nút Nhảy.
  Tốc độ leo mới chỉ cho greybox làRUN_SPEED/2, không thay số A0. D mở sẵn;
  N/m/M/B dùng dummy.gd đứng yên, chém được, không đánh trả; không có nhiệm vụ/AI boss.
- Thêm nút Đào Úc greybox từ A0 và Về A0, tọa độ ô dưới chân. Hai E nội bộ chuyển
  hai chiều, camera reset/chặn trước khi mở điều khiển; Tràng An/Đại Hoàng chỉ nhãn đích.
  Tái dùng player/camera/touch/tuning A0 qua hook có mặc định cũ; không đổi tuning.gd.
- Test Godot4.7.2: smoke, classic gốc qua wrapper, rig smoke, art/visual và Đào Úc;
  đường bắt buộc dùng Input thật từ S đến E rồi lên lũy, không teleport qua chướng ngại,
  không dùng khinh công; fixture riêng kiểm hố/chông, nước, bục một chiều và leo thang.
  Hai check_layout.py, kiểm byte bản sao, nhật ký append-only, không đổi A0/checklist
  và nguyên đầu ra lệnh được ghi trong commit message. Chưa chơi thử Realme trong cloud.
- Không tạo/sửa art, không chạm co_lau_game, không đánh dấu[x] hay nghiệm thu mốc.
  Không có prompt/imagegen mới; prototype vẫn là mã bỏ đi để tôi chơi thử bố cục.


## 29/10/2026 — dao_uc_greybox_followup — v1, chưa duyệt chính thức

- Người dùng đã xem/chấp nhận bản thử khối màu29/10/2026, UI thật làm sau.
  Nhánh `fix/g1-dao-uc-greybox-followup` từ main `501b621` (đã có PR21).
- Đồng bộ đúng câu báo đòn trong GDD và SCR-06: Tướng tiên phong Hậu Ngô1,5s,
  boss sau rút dần, không dưới0,8s; Tạm thời — chốt sau chơi thử. Không đổi số khác.
- Thay pipeline sao Markdown bằng `tools/export_layout_json.py`: lấy nguyên từng
  hàng layout, layout-meta và SHA256 toàn bộ nguồn; --check chỉ so trong bộ nhớ,
  báo lệch/mã khác0. Runtime đọc hai JSON; xóa sync_layouts.py, hai bản sao Markdown
  và manifest cũ. PC đối chiếu SHA/từng ô với nguồn, không nhập tay lưới.
- Checker bổ sung HUD trên SCR-05/SCR-06 ở960/1200 từ A0 +06: cấp, HP/MP,
  menu, ⚙, minimap120×80; riêng SCR-06 có thanh boss360×32 căn giữa,y24,
  gồm tên/vạch pha (Tạm thời ghi13). Không tính nhãn tọa độ/Về A0 là HUD.
  Hình người/quái cao96,boss132, dùng rộng khung128/192; không dùng collider88 thay ảnh.
- Người dùng chọn A: ẩn minimap SCR-06. Kiểm cho thấy menu/⚙ vẫn che lính khi
  camera bị chặn; sau khi được báo, người dùng cho phép hạ lũy. Hạ đỉnh từy160→224,
  giữ bậc32 px, đúng4 lính c54/55/57/58 (r4→r6), E phải r4→r6, sân phẳng640 px.
  Map thường m(c106,r4) bị che, chuyển riêng xuốngr6 trên bục dưới; không đổi địa hình.
- Kiểm mọi cột/mặt đứng được của sân/lũy và mỗi m/B trong khung hình, cả hai hướng;
  map thường từng m/M/N/B trong0–6 ô hai phía; hình96px S/R không chạm HUD trên/nút dưới.
  Bản thử áp đúng HUD đã chọn; test đối chiếu Rect thật của các Control với mô hình Python.
- Dựng lại ảnh/lớp phủ từ script và sinh JSON. Nguyên đầu ra Godot4.7.2 (import,
  smoke/classic/rig/Đào Úc), check_layout hai map, export JSON --check, phản chứng
  JSON sai/pose cũ bị che, export-pack preset tạm không include_filter và đọc nội dung
  PCK được chép vào commit message. Không commit preset tạm/gói xuất thử.
- Giữ nguyên prototype/config, art, tools/agent-skills, co_lau_game và checklist11;
  nhật ký cũ không đổi. Đây chưa phải duyệt chính thức/UI thành phẩm hoặc thử lại Realme.
- Ghi nhận export: Godot4.7.2 báo thiếu khóa include_filter khi preset cố ý bỏ hẳn
  khóa theo lệnh; export exit0 và script đọc PCK xác minh JSON/loader đúng nguồn cuối.
  Giữ nguyên chẩn đoán trong đầu ra commit, không che bằng bộ lọc hay đổi preset yêu cầu.

## 29/10/2026 — g1_parts_v3 — v3, chưa duyệt

- Theo người dùng: sửa thân gầy và đứng khom; không sửa tóc/đầu do Claude vẽ tay.
  Từ main8bd5876, nhánhfix/g1-parts-v3. Không tạo concept mới, không dùng imagegen.
- Idle và khung đứng cuối turn/land: gối0°, thân0°, hai đế y0. Thêm helper hông
  cố định, thở chỉ thân/đầu/tay dịch0,−1,−2,−1 px; giữ khung/thời lượng và dữ liệu
  mọi động tác khác. Hitbox, số A0, prototype/config và Đào Úc giữ nguyên.
- Đo lại ảnh nghiêng và scene: vai/ngực/hông trước12/14/17 px (cao95), sau14/17/19 px
  (cao96); sai lệch so ảnh gốc −0,219%/−0,986%/+3,956%, trong±10%.
  Body17×29→23×29, pivotx+4, attach và mọi metadata đầu giữ nguyên; gấu áo qua đai,
  palette theo vùng, viền chỉ ngoài đường bao; không sửa upper_arm.
- Xuất lại15 contact sheet art, idle×4 và ảnh so sánh từ file thật; báo cáo số đo
  trước/sau và script tại reports/g1_parts_v3_report.md. chr_dbl_parts: v3 chờ người dùng duyệt.
- Kiểm Godot4.7.2, palette/alpha/nhóm màu/viền/khớp và trục vũ khí; nguyên đầu ra
  trong commit message và reports/g1_parts_v3_checks.txt. Đầu so main giống từng
  pixel RGBA, pivot/attach; không tự đánh dấu[x], không sửa byte nhật ký cũ.
