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

## 30/10/2026 — g1_pose_sheets_pilot — v1, bản thử chưa duyệt

- Theo quyết định người dùng29/10: dừng rig16 mảnh; thử4 lớp tư thế vẽ trọn,
  không xoay khớp/vũ khí; hình vung vẽ sẵn, ngoài đánh đeo đao sau lưng.
  Nhánhfeat/g1-pose-sheets-pilot từ main8bd5876; giữ nguyên các nhánh thử trước.
- Dùng imagegen với ảnh gốc Đinh Bộ Lĩnh, STYLE-B vẽ tay + AVOID, bốn tờ:
  12thân/10chân/3đầu/6đao. Mỗi tờ1lần, không sinh lại. Prompt nguyên văn cạnh
  ảnh và docs/03_prompts; không dùng imagegen cho bảng/ảnh so sánh/kết quả.
- Script cắt nền alpha mềm, khử xanh, cắt vùng liền khối và mốc ghi số.
  Tờ chân thừa dải áo được cắt tại mốc hông; đầu/vũ khí cần đăng ký đồng dạng
  toàn tờ trước hệ số xuất chung, có ghi hệ số thực. Không ép32 màu/pixel.
- Prototype riêng với4 Sprite2D linear scale0,5 và gốc lật±1; idle/run/jump/fall/
  slash0,30s, nút xem từng động tác/đổi hướng/đao/VềA0. Không đổi A0 hay Đào Úc.
- Theo yêu cầu bổ sung, đọc hai repo tham khảo người dùng cung cấp để đối chiếu
  nguyên tắc bộ hình theo tư thế/offset và thay bộ khi đổi trang bị; không chép
  tài nguyên, bảng dữ liệu hay mã vào Cờ Lau. Bản thử tự viết, hình tạo riêng.
- Blender4.3.2 đã có sẵn; dựng thử file4 mặt phẳng tranh2D, texture đóng gói,
  camera trực giao và render thật. Chưa có mô hình3D mới; không gọi render2D là3D.
- Xvfb/Godot4.7.2 chụp1600×720 cả hai hướng; báo cáo và nguyên đầu ra tại
  reports/g1_pose_sheets_report.md; nguyên đầu ra cũng trong commit message.
  Asset bản thử chưa duyệt; không tự đánh dấu[x]. Nhật ký cũ giữ nguyên từng byte.

## 30/10/2026 — g1_kiem_cung — v1, bản thử chưa duyệt

- Người dùng chốt đổi phái/vũ khí sang Kiếm; tên Trảm Kiếm, Kiếm Tâm. Đồng bộ
  tài liệu/ID ví dụ dự kiến, không đổi số liệu chiêu hoặc trạng thái checklist.
  Nhánhfeat/g1-kiem-cung từ main4c2e368 đã có PR23.
- Kiếm thẳng hai lưỡi, chắn nhỏ/cán quấn dây; vung vẽ sẵn, chuôi ở tay gần,
  mũi/vệt theo chiều chém. Cung lưng ở trước/dây sau; giương chữV về tay gần,
  thả dây thẳng; tên là hình riêng bay về trước. Ngoài đánh, vũ khí sau lưng.
- Tham khảo cơ chế thể loại theo yêu cầu: đối chiếu cách chọn hình/offset/lật
  theo khung, hình vung và lưng cung/dây; tự viết và tạo hình riêng, không chép
  mã/hình/số liệu/tên nguồn tham khảo vào repo.
- Imagegen với ảnh gốc, STYLE-B/AVOID:6kiếm,5cung,2tên,4thân bắn. Kiếm/tên/thân
  mỗi tờ1lần; cung2lần, loại lần1 do khoảng kéo dây quá ngắn. Lưu prompt nguyên
  văn cạnh ảnh và03_prompts; lưu nguồn bị loại để đối chiếu.
- Cut_pose_sheets cắt theo vùng liền khối, đăng ký đồng dạng toàn tờ, alpha mềm
  khử xanh; mốc chuôi/mũi/lưng/dây/tay ghi bằng số. Xóa6hình vũ khí cũ của pilot,
  thaykiếm; không chạm rig16mảnh lịch sử, configA0, Đào Úc hay art/reference.
- Scene đổi phái/động tác/hướng; slash4khung0,30s; thrust2khung0,10s Đề xuất;
  shoot3pha giữ5/15s và spawn3/15s; run_shoot2pha giữ6/12s và spawn2/12s.
  Tên240px/s chỉ là Đề xuất xem thử. Không thay số chiêu hoặc gameplayA0.
- Kiểm mốc/hướng cả2phía, mọi Sprite2Dkhông xoay, tên chỉ sinh ở pha thả và
  bay xa; chụp scene Godot1600×720 hai hướng. Báo cáo/scripts/nguyên đầu ra tại
  reports/g1_kiem_cung_report.md; đầu ra cũng trong commit message.
- Nhật ký cũ và mọi báo cáo cũ giữ nguyên; không tự duyệt mỹ thuật/đánh dấu[x].

## 30/10/2026 — g1_kiem_vet_chem — v1, bản thử chưa duyệt

- Nhánhfeat/g1-kiem-vet-chem từ main8f70b6f. Tách lưỡi kiếm theo cấp khỏi vệt
  dùng chung; chỉ3cấp1/30/60được vẽ,4cấp còn lại làslotchưa vẽ. Không đổi tranh
  thân slash/thrust, tuningA0, Đào Úc hoặc rigcũ.
- Tham khảo cơ chế thể loại chỉ đọc: khung chọn tranh/offset, vệt đặt theo tâm,
  lật gương theo gốc, ẩn vũ khí cầm khi đánh; đã đọc cả pha cung/tên. Không chép
  mã, ảnh, bảng số hay tên nguồn vào repo. Dữ liệu/góc/canvas/thời gian do dự án đặt.
- Nguồn kiếm/vệt tạo riêng bằngimagegen, đính kèmref_dinh_bo_linh.png; giữSTYLE-B/
  AVOID. Một lần sinh, chưa duyệt mỹ thuật. Offlinechuẩn hóa và xoay từng góc
  trước xuấtPNG4×supersamplingrồi downsample, runtimekhông xoay. Chuôi cùngpixel,
  trục≤3°/chiều lưỡi≤15%, checkerđo cả pixel ảnh. Không thêm tài nguyên bên thứ ba.
- Slash5nhịp từ4pha thân cũ, giữ nhịp kết thúc thêm1nhịp, tổng0,30s; thrustgiữ
  pilotcũ.4vệt riêng theo tâm/offsetlogic, đuôi nhạt, dùngchung mọicấp. Trởidle
  sau0,30s, không để vệt treo mãi. Viewerdropdowncấp và nút chạy thật/dải tĩnh.
- Cung có tên đặt sẵn ở pha kéo, ẩn khi nghỉ/buông; tên bay riêng chỉ sinh khi
  buông. Chỉ kéo dài thân gỗOFFLINE, giữ lông/mũi và dùng cùng ảnh cho hai trạng
  thái. Người dùng nhắc: một nhân vật chỉKiếm HOẶCCung; đổi phái xóa hình/vệt/tên
  còn lại ngay, viewerkhóa dropdowncấpKiếm khi chọnCung. Các mẫu tĩnh là mẫu riêng.
- Xóa bytecode đã lỡ theo dõi khỏigit, giữ__pycache__/trong.gitignore. Không đưa
  zip, presetxuất hoặcfiletạm vào repo. Nhật ký cũ nguyênbyte, không tự đánh dấu[x].
- KiểmGodot4.7.2, template và chụpXvfb1600×720phải/trái; nguyênđầura trongcommit
  vàprototype/pose_rig/reports/swing_checks.txt. Grepnguyênvăn chưa0dòng vì tên
  sẵn có/chuỗi conLicensorvànhịphân; người dùng chọn ghi nguyênđầura và báo chưađạt,
  không sửa giấyphép/file ngoài phạmvi để làm sạch giả.
- Prompt nguyên văn:

```text
Use the attached Vietnamese character only for costume-era/art rendering reference. Create an ORIGINAL weapon and physical slash-effect source sheet, not a result/comparison board. Flat pure green #00FF00 background, no text, no labels, no frames. TWO ROWS of large separated objects. Top row EXACTLY THREE HORIZONTAL straight double-edged swords, all handles on LEFT and tips pointing RIGHT, identical clean broad straight silhouette and size. Plain small crossguard, cord wrapped grip, no gemstones or fantasy shapes. First is a simple tier1 forged iron sword with rough brown wooden grip and small iron guard; second is a tier30 better steel sword, tidy brown cord grip, small bronze guard; third tier60 fine steel, dark-brown tightly wrapped handle, compact bronze fittings with a restrained reed-leaf engraved motif. Same small simple outline family, sharp pointed symmetrical blades; steel limestone-grey main #A5B8B0, shadow #718B87, highlight #D9DDD0. Large EMPTY GREEN GUTTERS. Bottom row EXACTLY FOUR separate VERTICAL WHITE CRESCENT physical slash swooshes, open side LEFT, convex advance side RIGHT. First small beginning sweep; second large broad SOLID WHITE CRESCENT with a tiny pale grey-blue inner edge, smooth pointed tips and strongest opaque bulb at RIGHT, thin tapering tails toward upper/lower LEFT; third angled-down followthrough crescent; fourth same followthrough fading tail, pale white (on green for chroma key). No sparkles, no particles, no glow. All4shapes isolated, do not overlap swords. Draw no hands, people, lettering, arrows, UI or background shadows. These source shapes will be registered to fixed template canvases offline; do not pre-rotate swords.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```
## 30/10/2026 — chốt nhân vật chính (tài liệu)

- Người dùng chốt: style nhân vật **v2_a** (khối STYLE-V2); dựng **4 lớp** đầu/thân/chân/vũ khí
  theo **bảng 30 khung** chỉ dời/lật; trang bị 10 ô theo GDD, chỉ nón/áo/quần/vũ khí hiện lên
  người; 7 cấp 1/10/20/30/40/50/60 theo thang màu bảng thiết kế người dùng gửi; vệt chém/bắn cung
  dùng chung mọi cấp, đổi màu theo cấp; **cho phép lửa/hào quang** ở vũ khí Lv50–60, vệt Lv40–60,
  hiệu ứng chiêu và hào quang cường hóa Full +8/+12/+14/+16.
- Định dạng chiêu: nhịp = khung thân + tối đa 3 hiệu ứng + 1 đạn, hiệu ứng vẽ theo tâm, lật khi
  quay trái. Tên/cấp mở/số liệu chiêu và thú cưỡi (Trâu, Ngựa chiến, Voi chiến) giữ theo GDD.
- Bỏ khỏi bộ hiện tại, để Mốc sau: trúng đòn, choáng, ngã, đứng dậy, nói chuyện, cưỡi thú,
  lên cấp, mừng.
- Thứ tự: vẽ trọn nhân vật chính (5 bước) rồi mới tới bản đồ.
- Sửa: 01_art_bible (mục mới + ghi chú ở Phong cách), AGENTS.md (STYLE-V2, ngoại lệ phát sáng),
  09_animation_spec (mục 30 khung/định dạng chiêu), 16_rig_nhan_vat (đánh dấu đã thay, tóm tắt
  cách mới), 17_ngoai_hinh (10 ô, khối lượng 36 hình/cấp, hào quang). Nhật ký cũ giữ nguyên.
- Bổ sung: nhân vật lấy từ 2 bảng thiết kế người dùng gửi, lưu ở art/reference/
  (chr_dbl_board_trang_bi.png, chr_dbl_board_animation.png; bảng B cắt bỏ dải tiêu đề).
  Giữ tên/cấp/số liệu chiêu, nội tại, thú cưỡi theo GDD (Hổ → Voi chiến); cải trang thần
  thoại để phạm vi sau; bỏ động tác "đi". Bảng gán hiệu ứng → chiêu ghi ở 01_art_bible mục 8.
- Người dùng chốt: hai bảng thiết kế là mẫu chính về hình nhân vật (thay v2_a làm mẫu); vẽ độ
  phân giải cao giống bảng, so cạnh bảng khi duyệt.


## 30/10/2026 — g1_nhan_vat_chot, bước 1/5 Lv1 — chưa duyệt

- Thực hiện quyết định bộ 4 lớp/30 khung đã có trên main `98e86dc`: đầu8/thân18/chân10
  mới dùng chung hai phái, nón lá/áo nâu/khăn đỏ theo cột Lv1 của hai bảng. Chỉ làm Lv1;
  Lv10/20/30/40/50/60 chưa có bộ mới, không tính các pilot cũ là hoàn thành.
- Nguồn mới imagegen: 6 lần sinh, mỗi lần đính kèm hai bảng mẫu + ref Đinh Bộ Lĩnh;
  lần sửa thân đánh thêm tờ thân đúng. Tờ `bodies_b_rejected` bị dính đầu, giữ cả nguồn
  và prompt, không dùng trong bộ hình. Không cắt hình bảng mẫu vào texture nhân vật.
- `tools/build_lv1_30.py`: tách xanh, chọn vùng/khối đã kiểm, nắn kích thước và điểm neo,
  xuất PNG trong suốt và bản sao runtime; 3 góc chân lộn và 5 góc kiếm bake offline.
  Vẽ lại dây chữ V theo hai điểm tay thực, tách tên khỏi cung; mọi sprite runtime rotation0.
  Nguồn/cách xử lý được ghi trong parts.json, manifest và prompt cạnh ảnh.
- JSON mới `frames30`, `parts`, `effects`, `skills`: mỗi khung 4 lớp chọn hình + dx/dy;
  chiêu có nhịp đất/trên không, tối đa3 hiệu ứng +1đạn. Đòn thường Kiếm5nhịp .30s,
  hit .10–.20s; Cung giương/giữ/thả, tên đặt trên dây, chỉ sinh tên bay lúc buông.
  Trảm Kiếm dùng vệt xanh theo gán Trảm Phong; Xạ Tiễn dùng tên xanh theo bảng.
  Hiệu ứng neo tâm trên người; hình vung gắn grip thông qua offset tâm.
- Mỗi người chỉ Kiếm HOẶC Cung. Chuyển phái xóa vệt, tên bay, tên trên dây; chỉ Cung có
  ống tên. Đầu/thân/chân chung. Chỉ kiểm hình/hoạt ảnh trong prototype, không thêm luật
  combat hay sửa số A0, không đụng config/dao_uc/rig cũ/art reference/GDD/art bible.
- Viewer chọn phái, động tác/chiêu, nhịp đất/trên không, Chạy lại, Đổi hướng; dải30khung,
  dải đòn/chiêu, so cạnh ô Lv1 cắt từ bảng **chỉ cho đối chiếu**. Ảnh báo cáo từ Godot thật
  qua Xvfb1600×720 hai hướng, không dùng imagegen làm ảnh kết quả. Mọi hình chưa duyệt;
  cần người dùng xem lại độ giống bảng, nét và chuyển động ở cỡ160px.
- Giữ bộ pilot trước thành `legacy_pose_actor.gd`/`legacy_frames.tscn`. Hai test cũ chỉ đổi
  scene fixture, không bỏ/sửa assert; thêm `frames30_checks.gd` kiểm trực tiếp bộ mới và
  `check_lv1_30.py` kiểm RGBA/dữ liệu thật. Không lấy PASS của pilot để duyệt bộ mới.
- Tài liệu: thêm asset đang chờ duyệt ở02; sửa đúng một ghi chú16 còn nói v2_a thành
  hai bảng mẫu (đã bị quyết định mới thay). Không cần sửa09/17. Không đánh dấu[x].
- Dọn: main đã không còn tools/__pycache__ được track và đã có __pycache__/ trong
  .gitignore; duy trì nguyên trạng. Không thêm tài nguyên bên thứ ba, sourcezip hay preset.
- Kiểm tra và lệnh chụp thật: `prototype/pose_rig/reports/lv1_checks.txt`, commit message.

### Prompt nguyên văn và ảnh tham chiếu

Mỗi prompt dưới đính kèm `chr_dbl_board_trang_bi.png`,
`chr_dbl_board_animation.png`, `ref_dinh_bo_linh.png`; riêng `bodies_b` đính kèm thêm
`bodies_a.png`. Trạng thái giữ/loại như manifest; chưa duyệt mỹ thuật.

#### heads

```text
Draw NEW production source sprite pieces, not a presentation board. The first two attached character design boards are the PRIMARY model. Match their Lv1 column character exactly in face, big chibi head (~1/3 total height), black spiky hair with small topknot, bright red headband tails, simple straw conical hat WITHOUT tassels, brown wrap short-sleeve tunic, brown belt, brown knee pants, sturdy bare feet. Reference3 is historical context only, do NOT copy its tall thin proportions or cream shirt. RIGHT-facing slightly three-quarter side view like boards. Clean high-resolution bold cel-shaded cartoon, NOT pixel art. Uniform key-green #00FF00 background. No text, grids, labels, props or scenery. Every piece isolated with generous gap. Same scale within sheet. No weapons attached to body pieces. Draw padded neck/waist seams without black dividing borders. EXACTLY EIGHT head-only pieces (head INCLUDING straw hat, black hair, red headband tails, neck), arranged strict 4 columns x 2 rows, one per equal cell, identical scale and dimensions: row1 neutral facing right, alert right, lowered chin looking right, looking up right; row2 sideways tucked head rotated 90 clockwise, upside-down head 180, tucked head rotated 270, determined attacking face right. This is offline pre-drawn rotation: each actual drawing oriented as requested, no arrows. Head+hat 1/3 human height. No torso.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### bodies_a

```text
Draw NEW production source sprite pieces, not a presentation board. The first two attached character design boards are the PRIMARY model. Match their Lv1 column character exactly in face, big chibi head (~1/3 total height), black spiky hair with small topknot, bright red headband tails, simple straw conical hat WITHOUT tassels, brown wrap short-sleeve tunic, brown belt, brown knee pants, sturdy bare feet. Reference3 is historical context only, do NOT copy its tall thin proportions or cream shirt. RIGHT-facing slightly three-quarter side view like boards. Clean high-resolution bold cel-shaded cartoon, NOT pixel art. Uniform key-green #00FF00 background. No text, grids, labels, props or scenery. Every piece isolated with generous gap. Same scale within sheet. No weapons attached to body pieces. Draw padded neck/waist seams without black dividing borders. EXACTLY NINE torso-with-BOTH-arms pieces, strict 3 columns x 3 rows. Crop from neck base through brown belt/hip; no head and no legs. Brown short-sleeve tunic loose over belt; tan hands. Row1 relaxed arms at sides; relaxed breathing arms; running right arm forward left back. Row2 running opposite arms; running forward lean; airborne knees-independent arms balance. Row3 tucked somersault body oriented 90 clockwise; torso upside down180; tucked270. No sword or bow, fists closed or cupped. Draw shoulder/neck stubs for seam.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### bodies_b_rejected

```text
Draw NEW production source sprite pieces, not a presentation board. The first two attached character design boards are the PRIMARY model. Match their Lv1 column character exactly in face, big chibi head (~1/3 total height), black spiky hair with small topknot, bright red headband tails, simple straw conical hat WITHOUT tassels, brown wrap short-sleeve tunic, brown belt, brown knee pants, sturdy bare feet. Reference3 is historical context only, do NOT copy its tall thin proportions or cream shirt. RIGHT-facing slightly three-quarter side view like boards. Clean high-resolution bold cel-shaded cartoon, NOT pixel art. Uniform key-green #00FF00 background. No text, grids, labels, props or scenery. Every piece isolated with generous gap. Same scale within sheet. No weapons attached to body pieces. Draw padded neck/waist seams without black dividing borders. EXACTLY NINE torso-with-BOTH-arms attack pieces, strict 3 columns x 3 rows, brown short sleeve tunic and belt. No head, legs, weapons, arrows or effects. Right-facing. Row1 right/near fist raised behind above shoulder for sword windup; near fist raised overhead moving forward; near arm extended horizontally RIGHT holding imaginary sword. Row2 near arm diagonally down-right follow-through; near arm thrust straight right; both hands low-right finishing attack. Row3 archer FAR arm straight horizontal RIGHT at shoulder height with open grip and NEAR hand drawing imaginary string toward cheek (cheek just above neck); same archer fully drawn near hand at cheek; archer release near hand pulling back past neck. Show FAR hand clearly, do not hide behind near arm. Match same torso scale as bodies_a.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### bodies_b

```text
Draw NEW production source sprite pieces, not a presentation board. The first two attached character design boards are the PRIMARY model. Match their Lv1 column character exactly in face, big chibi head (~1/3 total height), black spiky hair with small topknot, bright red headband tails, simple straw conical hat WITHOUT tassels, brown wrap short-sleeve tunic, brown belt, brown knee pants, sturdy bare feet. Reference3 is historical context only, do NOT copy its tall thin proportions or cream shirt. RIGHT-facing slightly three-quarter side view like boards. Clean high-resolution bold cel-shaded cartoon, NOT pixel art. Uniform key-green #00FF00 background. No text, grids, labels, props or scenery. Every piece isolated with generous gap. Same scale within sheet. No weapons attached to body pieces. Draw padded neck/waist seams without black dividing borders. CRITICAL: THE FOURTH REFERENCE SHOWS THE CORRECT HEADLESS TORSO FORMAT. Draw ONLY NECK STUMPS, SHIRT AND ARMS; absolutely NO face, eyes, hair, headband, hat or skull anywhere. Cut cleanly at the neck base. EXACTLY NINE torso-with-BOTH-arms attack pieces, strict 3 columns x 3 rows, brown short sleeve tunic and belt. No head, legs, weapons, arrows or effects. Right-facing. Row1 right/near fist raised behind above shoulder for sword windup; near fist raised overhead moving forward; near arm extended horizontally RIGHT holding imaginary sword. Row2 near arm diagonally down-right follow-through; near arm thrust straight right; both hands low-right finishing attack. Row3 archer FAR arm straight horizontal RIGHT at shoulder height with open grip and NEAR hand drawing imaginary string toward cheek (cheek just above neck); same archer fully drawn near hand at cheek; archer release near hand pulling back past neck. Show FAR hand clearly, do not hide behind near arm. Match same torso scale as bodies_a.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### legs

```text
Draw NEW production source sprite pieces, not a presentation board. The first two attached character design boards are the PRIMARY model. Match their Lv1 column character exactly in face, big chibi head (~1/3 total height), black spiky hair with small topknot, bright red headband tails, simple straw conical hat WITHOUT tassels, brown wrap short-sleeve tunic, brown belt, brown knee pants, sturdy bare feet. Reference3 is historical context only, do NOT copy its tall thin proportions or cream shirt. RIGHT-facing slightly three-quarter side view like boards. Clean high-resolution bold cel-shaded cartoon, NOT pixel art. Uniform key-green #00FF00 background. No text, grids, labels, props or scenery. Every piece isolated with generous gap. Same scale within sheet. No weapons attached to body pieces. Draw padded neck/waist seams without black dividing borders. EXACTLY TEN waist-to-feet pairs of legs, strict 5 columns x 2 rows. Brown knee-length pants, tan bare calves and big bare feet, brown belt seam pad at top; no torso or head. Row1 standing straight both feet on same baseline; run stride right leg forward; run compressed passing; run airborne wide; run left leg forward. Row2 run passing opposite; airborne knees bent jump; tightly tucked legs oriented90clockwise; tucked legs upside-down180; tucked270. Same hip-to-sole length across grounded cells. No footwear, no weapons.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### weapons

```text
Draw NEW production source sprite pieces, not a presentation board. The first two attached character design boards are the PRIMARY model. Match their Lv1 column character exactly in face, big chibi head (~1/3 total height), black spiky hair with small topknot, bright red headband tails, simple straw conical hat WITHOUT tassels, brown wrap short-sleeve tunic, brown belt, brown knee pants, sturdy bare feet. Reference3 is historical context only, do NOT copy its tall thin proportions or cream shirt. RIGHT-facing slightly three-quarter side view like boards. Clean high-resolution bold cel-shaded cartoon, NOT pixel art. Uniform key-green #00FF00 background. No text, grids, labels, props or scenery. Every piece isolated with generous gap. Same scale within sheet. No weapons attached to body pieces. Draw padded neck/waist seams without black dividing borders. EXACTLY TEN isolated weapon/effect objects strict 5columns x2rows, one per cell generous margin. row1: simple broad straight silver DOUBLE-EDGED sword pointing up-right with tiny crossguard wrapped brown grip and red cord; wooden bow standing vertical with belly bulging RIGHT and straight light string LEFT; same upright bow drawn, string V apex at LEFT; same upright bow released straight string LEFT; quiver brown with white feathered arrows no bow attached. row2: horizontal arrow pointing RIGHT; opaque WHITE crescent slash sweeping RIGHT; larger opaque WHITE crescent slash sweeping RIGHT; bright BLUE-white crescent slash sweeping RIGHT (skill); BLUE-white horizontal fast arrow pointing RIGHT (skill). No hands or people. Basic swords and white effects no glow. Blue skill effects may glow.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, modern objects, any text, letters, logos or watermarks.
```


## 30/10/2026 — g1_nhan_vat_chot_size_followup — chưa duyệt

- Sửa tiếp cùng nhánh theo người dùng: **số cũ khoảng160px là sai**. Người96px logic
  A0 hiển thị128px trên1600×720. Không thay ảnh người hay số A0; viewer dùng hệ số
  128/96,204 theo chiều cao RGBA đo thực. Hai tài liệu16/17 và README/viewer ghi chuẩn128.
  Art bible01 còn chuẩn cũ nhưng nằm ngoài phạm vi lượt này; quyết định trực tiếp mới
  của người dùng được ưu tiên, chưa tự sửa01.
- Đọc cơ chế/lấy số đo từ dữ liệu và ảnh tham khảo tại máy: người ghép33px ở bộ gốc,
  131px ở bộ4×; hiệu ứng được cấu thành bởi5hình riêng. Chỉ tự xây dữ liệu/hình của mình.
  Script, số đo chi tiết và ảnh so cùng128px nằm trong `/tmp/lv1-size-followup/`, không
  commit ảnh hoặc mã tham khảo. Không thêm tài nguyên bên thứ ba.
- Cỡ thực từ PNG: kiếm cầm tay0,780284H (tính cả chuôi theo trục), cung0,375H,
  tên thường0,578125H, tên chiêu0,593750H. Tất cả nằm trong khoảng người dùng yêu cầu.
- Thay vệt rời bằng5PNG vung riêng ghép lưỡi+vệt,4hình quét có hình học khác nhau theo
  góc. Nhịp giơ không vệt. Trảm Kiếm dùng5bản ghép xanh tương ứng. Runtime vẽ1PNG/nhịp
  theo tâm, bù offset để grip trùng tay; không xoay sprite, không dời lưỡi liềm dùng chung.
  Mask và lưỡi rời giữ để kiểm offline; bỏ5file trail cũ. Chỉ hình tự tạo bằng script từ
  kiếm nguồn của dự án, không dùng ảnh tham khảo làm đầu vào texture.
- Kiểm từ alpha thực: độ rộng/cao hình vung dưới1,6H/1,1H; khoảng mũi–mép vệt lớn
  nhất0,626719px logic, dưới2px. Kiểm texture ghép thật bằng so toàn bộ RGBA với lưỡi+
  mask, kiểm grip tại Sprite2D thật≤1px. Chuẩn96logic, hitbox và nhịp chém A0 giữ nguyên.
- Dải30khung đổi6cột×5hàng, co thumbnail vừa ô và đo bounds thật để tránh chồng.
  Thumbnail là ảnh xem tổng quan; cỡ128px xem ở trang chạy đòn/chiêu và so cạnh bảng.
  Test viewer kiểm mọi cặp ô hai hướng và chiều cao người chạy thật128px.
- Đầu ra test, lệnh chụp Godot/Xvfb1600×720 phải/trái và kiểm tên được giữ nguyên văn
  trong commit; `prototype/pose_rig/reports/lv1_size_checks.txt` lưu đầu ra không chứa
  nội dung tham khảo. Lv1 vẫn chờ người dùng duyệt; không làm Lv10–60.


## 30/10/2026 — g1_horizontal_and_held_weapons — chưa duyệt

- Mẫu đòn trước **sai lớp: Đao**, không phải Kiếm. Đối chiếu chỉ đọc dữ liệu tham khảo:
  lớp1/chiêu1 là Kiếm, lớp4/chiêu28 là Cung, lớp5/chiêu37 là Đao. Không chép code,
  ảnh, ID/offset vào bộ hình game. Các file soi tham khảo chỉ ở `/tmp/horizontal-reference/`.
- Kiếm sửa thành6nhịp **thủ → kéo → lia ngang → giữ/kéo dài → giữ → về thủ**.
  Mỗi nhịp0,05s, tổng0,30s, hit0,10–0,20s giữ A0. Mũi nằm ngang hông/ngực,
  không giơ cao bổ xuống. Vệt lia ra ở nhịp2, kéo dài ở nhịp3, tàn ở nhịp4;
  nhịp thủ/về thủ chỉ kiếm. Trảm Kiếm cùng dáng với lớp sáng xanh dài/dày hơn.
- Vệt riêng dài1,2–1,6H, cao≤0,35H; mép tơi liên tục, alpha đuôi giảm dần,
  nối mũi≤2px. Lõi trắng Lv1, lưu sẵn slot màu cam/đỏ cho bước sau (chưa vẽ cấp sau).
  H=96logic. Giới hạn toàn ảnh1,6H của bản cũ không còn phù hợp vì vệt mới bắt đầu
  ở mũi, ngoài phần kiếm0,78H; sửa test theo đúng giới hạn vệt mới, không che FAIL.
  Kiểm PNG thực: RGBA ghép lưỡi+mask, kích thước vệt,1khối liền, alpha đầu/đuôi,
  khoảng hở mũi–mép vệt nhìn thấy. Runtime mỗi nhịp1texture neo tâm, rotation0.
- Vẽ mới4thân thay `body_9..12` bằng imagegen, cùng mẫu Lv1 và điểm neo hip/neck/hand.
  Thêm1hình `legs_guard` phụ trợ để choãi chân/hạ trọng tâm ở các nhịp trên đất;
  bộ10hình chân di chuyển vẫn nguyên vẹn,18ô thân vẫn18 (thay4ô). Chân phụ trợ chỉ là
  thử nghiệm chưa duyệt, không tự chốt lại khối lượng art/trang bị. Nhịp trên không dùng
  chân bay cũ. Nguồn và prompt: `art/sprites/characters/lv1_30/sources/horizontal_attack.*`.
- Cung đối chiếu đúng8nhịp: giương2, giữ2, thả1, hồi3; chỉ sinh tên ởnhịp5, tại0,20s.
  Tên đặt trên dây4nhịp đầu. Mỗi nhịp0,05s/tổng0,40s là **Đề xuất thời gian xem prototype**,
  không tuyên bố đó là thời gian tuyệt đối đo từ nguồn hay số game thật đã duyệt.
  Hình cung/tên giữ bộ hiện có, hướng bụng trước/dây sau giữ nguyên.
- Bổ sung cách cầm theo người dùng: đứng/nhảy kiếm ở tay trước ngang hông, mũi chéo
  xuống sau; chạy gần ngang về sau. Cung ở tay trước, chéo trước thân, đầu trên ra trước/
  đầu dưới về sau. Vẽ góc sẵn offline, runtime không xoay. Chỉ hiện ở tư thế đứng/chạy/
  nhảy/rơi, ẩn cả lộn và đánh. Không bê số khung21 tham khảo sang khung21 bảng dự án:
  khung này ở dự án đang giương cung nên phải ẩn hình cầm tay, hiện hình cung của nhịp đánh.
- Giữ người96logic/hiển thị128px, số chạy/nhảy/hitbox A0 không đổi. Viewer giữ dải30khung
  không chồng, dải đòn đổi lưới để hiển thị đủ6nhịp Kiếm/8nhịp Cung. Ảnh chụp thật
  Xvfb/Godot1600×720 cả hai hướng, không imagegen cho kết quả/so sánh.
- Tài liệu:09 sửa mục Đòn chém cơ bản và nhịp Cung,16 ghi tư thế/kiểm tra;01 chỉ sửa
  mục Kiếm/Cung — quy tắc hình vũ khí theo phạm vi bổ sung. README ghi cách xem mới.
  Không sửa17, GDD,02 hay prototype/config/dao_uc/rig cũ/art reference. Không đánh dấu[x].
- Test cũ vẫn chạy (pilot cũ giữ riêng làm hồi quy); test30khung kiểm bộ hiện hành,
  thêm `horizontal_weapon_checks.gd` đo vị trí sprite thật hai hướng, kiểm8nhịp Cung.
  Đầu ra nguyên văn trong commit và `prototype/pose_rig/reports/lv1_horizontal_checks.txt`.
  Không thêm tài nguyên bên thứ ba. Lv1 vẫn chờ người dùng duyệt; chưa làm Lv10–60.

### Prompt nguyên văn — horizontal_attack

Đính kèm hai bảng `chr_dbl_board_trang_bi.png`, `chr_dbl_board_animation.png`,
`ref_dinh_bo_linh.png`, và tờ thân `sources/bodies_a.png`. 1lần sinh, giữ nguồn mới,
chưa duyệt mỹ thuật. Chỉ dùng imagegen vẽ nguồn, script tách/ghép/kiểm hình thật.

```text
Production source of FIVE isolated Lv1 character pieces, equal 3 columns x2 rows, last bottom-right cell EMPTY. Bright pure green #00FF00 background, generous gaps, no text. First two references are primary design: brown wrap short-sleeve shirt, belt, knee pants, chunky bare limbs, red headband character but NO HEAD on these pieces. Fourth reference gives exactly the headless-torso separation and shirt colors. NO face, hair, head, hat, weapons, slash effects. All looking RIGHT in three-quarter side view. Same torso scale in all four cells. ROW1: (1) headless torso with both arms, low sword guard: near fist close to RIGHT waist at belly-button height, far fist before abdomen, shoulders relaxed; (2) headless torso coiling hips and shoulders to pull a sword BACK HORIZONTALLY: near fist to LEFT hip at waist level, elbow bent, far arm balancing forward; (3) headless torso uncoiling hips and shoulders in a HORIZONTAL WAIST-HIGH sweep to RIGHT: near fist extended to RIGHT at belly-button height, elbow slightly bent, far arm counterbalancing. ROW2: (4) headless torso follow-through from horizontal waist-level sweep: near fist low-forward RIGHT at hip level, shoulders twisted, no arm above chest; (5) ONLY a pair of legs from waist through soles, brown knee pants, bare feet widely planted on SAME horizontal baseline, knees bent in a stable low martial stance, weight centered, no torso/head, feet pointing slightly right; (6) empty green. Neck stumps and waist pads for overlap. Do NOT depict an overhead swing. No axe-chopping motion. Strong thick clean contours, few big folds. Match the brown Lv1 clothing and chunky chibi silhouette on the attached boards.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```


## 30/10/2026 — lv1_compact40 — vẽ lại Lv1 và sửa kiếm/cung (chưa duyệt)

- **Lý do:** quyết định và phản hồi người dùng; bản trước sai ngoại hình, đầu nhỏ,
  vệt chém lơ lửng, kiếm cầm nhỏ và tên không đi qua điểm tựa cung.
- **Thứ tự quyết định:** đã thử brief đầu 0,50H/áo cộc/chân đất, rồi bỏ theo chỉ đạo
  cuối: hàng Tổng thể Lv1, đầu/tóc 0,40H ±0,03, không nón lá, áo giao lĩnh nâu dài,
  giày, dải tóc đỏ; người hiển thị 128 px trên 1600×720. Nguồn đầu của lượt 0,50H
  vẫn dùng được sau khi xuất lại cỡ 0,40H; nguồn áo/quần và nón cũ chỉ lưu lịch sử.
- **Nguồn chuẩn làm việc:** fetch main trả `98e86dc`, chưa có docs/18; đã nhập nguyên
  hai file luồng tham khảo từ nhánh tài liệu `85d3ad8` bằng merge `9402f50` trên nhánh
  tính năng, không merge vào main. Đọc mục 4, chạy công cụ dựng tham khảo rồi mở
  cả bốn bảng cầm kiếm/cung và đòn kiếm/cung. Chỉ đọc cơ chế; không chép mã/ảnh.
- **Bộ hình:** xuất lại đủ 8 đầu, 18 thân, 10 chân cùng hai chân thủ/lunge bổ sung;
  36 ảnh chung khác RGBA so với `3371ab3`. Không có hình nón đang hoạt động.
  Đầu đo 0,401671H, người alpha 95,8495 px logic; hệ số preview tính từ alpha,
  scene Godot xuất cả hai phái cao đúng 128 px. Sprite không xoay; chỉ lật node gốc.
- **Kiếm:** bốn thân thủ/kéo/lia/thu khác nhau, năm nhịp 0,05/0,05/0,10/0,05/0,05 s,
  tổng 0,30 s; cửa sổ trúng 0,10–0,20 s giữ A0. Ẩn kiếm cầm khi đánh, dùng lưỡi ngắn
  vẽ sẵn cùng đường vung cong sát thân, thêm vệt lao ra và quét ngược; tổng vệt ≤1,3H.
  Trảm Kiếm thêm lớp xanh, chưa vẽ bộ cấp cao. Kiếm ngoài đánh chúc xuống sau.
  Lỗi kiếm nhỏ do kiểm chiều dọc trục thay cho cạnh dài nhất hộp alpha: đã đổi phép
  đo và cỡ ảnh, đứng khoảng 0,772H, chạy 0,793H; không kéo dài lưỡi ngắn trong hình vung.
- **Cung/tên:** thay số cung 0,35–0,40H sai bằng 0,90–1,00H, cầm trước thân; đầu tên
  dài 0,55–0,65H. Căn đường pixel thân tên thật qua tay kéo dây và điểm tựa trên gỗ;
  nướng góc vào ảnh, không xoay runtime. Khi thả, đuôi tên sinh tại dây đã thả thay
  vì nhảy sang tay cầm gỗ. Kiểm tra ảnh thật: lệch điểm tựa tối đa khoảng 0,112 px
  logic trong bốn ảnh tên, không nới ngưỡng 1 px. Bắn 8 nhịp, sinh tên nhịp 5;
  tổng 0,40 s chỉ là đề xuất xem prototype. Hai phái không hiện lẫn vũ khí.
- **So bằng ảnh thật:** scene xuất 88 ảnh tạm; ghép 86 ảnh ba cột (mình | bảng Lv1 |
  dựng tham khảo), chuẩn đứng cùng 128 px. Đã xem đứng/cầm, giương và nhịp lia.
  Bản mình đọc rõ mặt, áo dài nâu/giày và dải đỏ; cung lớn trước người, tên qua tay
  và điểm tựa, vệt cong bắt đầu sát áo thay cho vệt xám lơ lửng. Khác biệt còn rõ:
  đầu mình theo quyết định 0,40H, không theo tỉ lệ 0,58H của nguồn; Lv1 mình trắng,
  không lấy màu cam của nguồn; dáng và nét vẽ vẫn chờ người dùng duyệt. Ảnh có hình
  tham khảo và dữ liệu dựng đều chỉ ở `/tmp/ref_render`, không commit.
- **Viewer:** dời vùng phát đòn sang phải để vệt quay trái không bị cắt mép màn;
  thêm kiểm tra mọi nhịp xem tĩnh và phát trực tiếp đều nằm trong viewport, cả hai phái/hướng.
  Cột mẫu Lv1 của viewer cũng thu về 128 px thay cho phóng ×4 khác cỡ.
- **Kiểm tra:** Godot 4.7.2 import và 13 bài kiểm cũ/mới; Python kiểm alpha, tỉ lệ,
  đường tên, hash bộ hình; chụp viewer 1600×720 phải/trái từ scene thật. Đầu ra nguyên
  văn trong commit và `prototype/pose_rig/reports/lv1_compact40_checks.txt`; đầu ra
  dựng tham khảo chỉ trong commit, không chép vào báo cáo theo dõi. Có fixture cũ
  để giữ hồi quy; kiểm ảnh mới nằm riêng, PASS kỹ thuật không phải duyệt mỹ thuật.
- **Phạm vi:** không đổi số A0, dao_uc, rig cũ, ảnh mẫu, GDD hay nội dung nhật ký cũ;
  không đánh dấu [x], không tự duyệt. Nhân vật này vẫn là bản thử Lv1.

### Nhật ký nguồn ảnh và prompt nguyên văn

Ảnh do imagegen tạo; ảnh so và chụp scene không dùng imagegen. Mọi lượt đính kèm
hai bảng `chr_dbl_board_trang_bi.png`, `chr_dbl_board_animation.png` và
`ref_dinh_bo_linh.png` của dự án. Hai lượt thân ban đầu thêm `sources/bodies_a.png`;
hai lượt thân board40 thêm cùng ảnh thân và crop hàng Tổng thể Lv1 phóng lớn;
chân board40 thêm crop này. Crop chỉ từ bảng riêng của dự án, không từ tài nguyên
tham khảo bên ngoài. Hash, trạng thái và prompt cạnh nguồn có trong `sources/manifest.json`.

#### heads_50 — Giữ để xuất bản thử, chưa duyệt

Nguồn: `art/sprites/characters/lv1_30/sources/heads_50.png`.

```text
NEW complete Lv1 family, bold clean chibi cel-shaded cartoon, 2D RIGHT-facing side/three-quarter view. PRIMARY model is the attached equipment/animation boards: same black hair/topknot, red headband tails, tan face, BROWN wrap short-sleeve tunic, brown belt and knee pants, bare feet, plain rural straw hat. This NEW proportion overrides the old reference anatomy: head+hair WITHOUT hat = EXACTLY HALF of standing person height. Very LARGE rounded expressive head, BIG readable eyes and face; SHORT WIDE STOCKY torso and SHORT STRONG legs, broad hands/feet. Leave a strong broad chest/shoulder silhouette suitable for future armor. Not tall/thin; no long neck, long abdomen or long calves. Smooth dark thick contours, large flat clean earth-color shapes. Pure green #00FF00 background, separated pieces with generous empty margins, strict equal cell grid, no labels, grid lines or text. No weapons or effects on human pieces. Same scale in each sheet. EXACTLY8 isolated HEADS ONLY, WITHOUT any hat, no torso: 4columns x2rows. All upright facing RIGHT (rotation baked later): neutral; alert; lowered chin; looking up; determined closed mouth; tightly focused; surprised; attacking face. Full black hair including SMALL topknot, red headband/ribbon tails, HUGE clearly defined eyes, round cheek and short chin matching board face. Finish at chin with at most a tiny attachment stump, NO long neck. No straw hat anywhere. Draw high resolution clean original face, not pixel art. These heads will be half the complete person height.

The new HALF-height head ratio takes priority over older proportion text in the style block below.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### bodies_a_50 — Không dùng ở bản hiện tại: brief bị thay; giữ lịch sử

Nguồn: `art/sprites/characters/lv1_30/sources/bodies_a_50.png`.

```text
NEW complete Lv1 family, bold clean chibi cel-shaded cartoon, 2D RIGHT-facing side/three-quarter view. PRIMARY model is the attached equipment/animation boards: same black hair/topknot, red headband tails, tan face, BROWN wrap short-sleeve tunic, brown belt and knee pants, bare feet, plain rural straw hat. This NEW proportion overrides the old reference anatomy: head+hair WITHOUT hat = EXACTLY HALF of standing person height. Very LARGE rounded expressive head, BIG readable eyes and face; SHORT WIDE STOCKY torso and SHORT STRONG legs, broad hands/feet. Leave a strong broad chest/shoulder silhouette suitable for future armor. Not tall/thin; no long neck, long abdomen or long calves. Smooth dark thick contours, large flat clean earth-color shapes. Pure green #00FF00 background, separated pieces with generous empty margins, strict equal cell grid, no labels, grid lines or text. No weapons or effects on human pieces. Same scale in each sheet. EXACTLY9 HEADLESS torso+TWOarms pieces, 3columns x3rows. Neck-base through belt/hip including shirt hem; NO head/face/hair/hat/legs. Very SHORT BROAD chest, width about1.3times neck-to-belt distance, chunky shoulders/forearms/fists, shirt over belt, few big folds, not an elongated adult torso. Row1 relaxed arms to sides; breathing arms; running right arm forward/left back. Row2 running opposite arms; forward-lean running; airborne balancing arms. Row3 three distinct compact curled somersault torsos, still upright source: arms tucked across belly; fists beside shoulders; one forearm across chest. All same short sturdy build.

The new HALF-height head ratio takes priority over older proportion text in the style block below.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### bodies_b_50 — Không dùng ở bản hiện tại: brief bị thay; giữ lịch sử

Nguồn: `art/sprites/characters/lv1_30/sources/bodies_b_50.png`.

```text
NEW complete Lv1 family, bold clean chibi cel-shaded cartoon, 2D RIGHT-facing side/three-quarter view. PRIMARY model is the attached equipment/animation boards: same black hair/topknot, red headband tails, tan face, BROWN wrap short-sleeve tunic, brown belt and knee pants, bare feet, plain rural straw hat. This NEW proportion overrides the old reference anatomy: head+hair WITHOUT hat = EXACTLY HALF of standing person height. Very LARGE rounded expressive head, BIG readable eyes and face; SHORT WIDE STOCKY torso and SHORT STRONG legs, broad hands/feet. Leave a strong broad chest/shoulder silhouette suitable for future armor. Not tall/thin; no long neck, long abdomen or long calves. Smooth dark thick contours, large flat clean earth-color shapes. Pure green #00FF00 background, separated pieces with generous empty margins, strict equal cell grid, no labels, grid lines or text. No weapons or effects on human pieces. Same scale in each sheet. EXACTLY9 HEADLESS short broad torso+TWOarms pieces,3columns x3rows. NO head/face/hair/hat/legs/weapons. Same VERY SHORT WIDE chunky brown shirt body: neck-to-belt about3/4 chest width, strong shoulders, short arms and big fists. First FOUR poses must have VERY DIFFERENT silhouettes and hip/shoulder twist: row1col1 LOW GUARD torso lowered forward, near fist beside RIGHT hip, far arm tucked. row1col2 DRAW BACK: near fist far LEFT behind hip with elbow pulled back, shoulders twist away, far arm balancing. row1col3 SWEEP: near arm fully extended RIGHT at WAIST level, torso leans FORWARD and hips twist, far arm far LEFT as counterweight. row2col1 RECOVER: near fist returns in FRONT OF CHEST, elbow bent, shoulders unwind, far hand low. row2col2 horizontal forward thrust; row2col3 both fists low forward. Row3: archer FAR arm fully extended right, NEAR hand pulling imaginary string at cheek position slightly ABOVE neck stump; fully drawn archer hold; release near hand behind cheek/neck. Far hand must be clearly visible. No overhead sword attack. No actual sword, bow, arrows or effects.

The new HALF-height head ratio takes priority over older proportion text in the style block below.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### legs_50 — Không dùng ở bản hiện tại: brief bị thay; giữ lịch sử

Nguồn: `art/sprites/characters/lv1_30/sources/legs_50.png`.

```text
NEW complete Lv1 family, bold clean chibi cel-shaded cartoon, 2D RIGHT-facing side/three-quarter view. PRIMARY model is the attached equipment/animation boards: same black hair/topknot, red headband tails, tan face, BROWN wrap short-sleeve tunic, brown belt and knee pants, bare feet, plain rural straw hat. This NEW proportion overrides the old reference anatomy: head+hair WITHOUT hat = EXACTLY HALF of standing person height. Very LARGE rounded expressive head, BIG readable eyes and face; SHORT WIDE STOCKY torso and SHORT STRONG legs, broad hands/feet. Leave a strong broad chest/shoulder silhouette suitable for future armor. Not tall/thin; no long neck, long abdomen or long calves. Smooth dark thick contours, large flat clean earth-color shapes. Pure green #00FF00 background, separated pieces with generous empty margins, strict equal cell grid, no labels, grid lines or text. No weapons or effects on human pieces. Same scale in each sheet. EXACTLY10 isolated waist-to-sole PAIRS of legs,5columns x2rows, no torso/head/weapons. NEW VERY SHORT STOCKY chibi legs: brown pants to knees take60percent hip-to-sole, short thick bare calves, BIG wide bare feet; do not draw long human shins. Hip-to-sole length about HALF of head height. Row1 standing straight both feet SAME baseline; run stride right-forward; compressed running passing; airborne run wide; run opposite stride. Row2 running passing opposite; jump tightly tucked; LOW GUARD knees deeply bent feet WIDE firmly on SAME baseline; forward LUNGE right foot stepped far right, both soles SAME baseline; compact airborne tucked variant. Uniform short strong anatomy across all10, broad hips for future armor.

The new HALF-height head ratio takes priority over older proportion text in the style block below.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### hat_50 — Không dùng ở bản hiện tại: brief bị thay; giữ lịch sử; công cụ còn sinh cả người ngoài yêu cầu nón, đã loại hoàn toàn

Nguồn: `art/sprites/characters/lv1_30/sources/hat_50.png`.

```text
NEW complete Lv1 family, bold clean chibi cel-shaded cartoon, 2D RIGHT-facing side/three-quarter view. PRIMARY model is the attached equipment/animation boards: same black hair/topknot, red headband tails, tan face, BROWN wrap short-sleeve tunic, brown belt and knee pants, bare feet, plain rural straw hat. This NEW proportion overrides the old reference anatomy: head+hair WITHOUT hat = EXACTLY HALF of standing person height. Very LARGE rounded expressive head, BIG readable eyes and face; SHORT WIDE STOCKY torso and SHORT STRONG legs, broad hands/feet. Leave a strong broad chest/shoulder silhouette suitable for future armor. Not tall/thin; no long neck, long abdomen or long calves. Smooth dark thick contours, large flat clean earth-color shapes. Pure green #00FF00 background, separated pieces with generous empty margins, strict equal cell grid, no labels, grid lines or text. No weapons or effects on human pieces. Same scale in each sheet. ONE isolated plain Vietnamese conical straw HAT only, no head or character. Very LOW flat cone with broad curved brim in three-quarter right-facing side view, earth/straw yellow, dark clean border, simple3tone cel shading. Small opening for hair topknot at apex, no tassels, no cords. Width about4times the height. Keep entire hat visible with generous margin. Its shape and colors match Lv1 hat item on the primary board. No other objects.

The new HALF-height head ratio takes priority over older proportion text in the style block below.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### compact_swings_50 — Giữ để xuất bản thử, chưa duyệt

Nguồn: `art/sprites/characters/lv1_30/sources/compact_swings_50.png`.

```text
FIVE isolated pre-drawn SWORD-SWING VFX sprites in one horizontal row of5 equal cells, on pure #00FF00 green. NO character, NO hands, NO text. These belong to the brown Lv1 chibi hero in attached boards. Each cell has one tiny brown wrapped hilt with a SHORT silver blade fragment (ONLY about1/5 human height, not a full long sword) plus its own WHITE/very pale grey painted swing. Handle is at the same relative left-centre position in each cell. Whole effect must fit within1.3times human height width, NOT a long detached projectile. Cell1 low GUARD: tiny hilt and short blade only. Cell2 PULL: thin curved white swish tight around and partly BEHIND the hilt/hip position, no overhead swing. Cell3 MAIN SWEEP: bold WHITE CURVED HOOK/CURL embracing the FRONT OF THE TORSO/HIP, starting slightly LEFT/BEHIND the hilt, curling BELOW and around to the RIGHT, thick body with CONCAVE interior, torn pointed brush tails, plus a SHORT small forward spur; not an ellipse, cigar, pill, detached cloud, flat horizontal lance or huge overhead axe crescent. Cell4 HOLD/FADE: a different looser pale-white curl breaking into connected feathered pointed tails and a small BACKWARD grey sweep near hilt; still compact and curved. Cell5 RECOVER: tiny hilt and short silver blade fragment only. Thin clean dark brown outline around all swishes so they read on pale background. NO glow for Lv1. Keep shapes smooth but tapered, curved and visibly different between cells2/3/4. Paint whole effects as original art, do not reuse any reference image pixels. Main curve occupies the space around the grip, not starting AFTER a long sword tip. Leave ample margins between five sprites. High resolution clean bold cartoon art, no pixel grid.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### bodies_a_board40 — Giữ để xuất bản thử, chưa duyệt

Nguồn: `art/sprites/characters/lv1_30/sources/bodies_a_board40.png`.

```text
NEW Lv1 CLOTHING from the first column TOTAL-APPEARANCE row of the primary equipment board, shown enlarged in last attached image. This model OVERRIDES the old cream short shirt/bare feet: DARK EARTH-BROWN SLEEVELESS LONG CROSS-COLLAR ROBE/TUNIC, pale cream narrow piping on the diagonal collar and split skirt hems, brown belt at waist, robe split front panels hanging to MID-THIGH / near knee, brown wrist-wraps on bare sturdy forearms. Brown pants and BROWN CLOSED SHOES/ANKLE WRAPS (legs sheet only). Black hair and red ribbon belong to head, do NOT draw them here. NO straw hat. The total-character head+hair is0.40H, torso/limbs short broad sturdy to allow armor later. Style face/color identity stays that of the board. High resolution clean bold cartoon with thick dark brown contours, flat earth colors2–3sharp cel-shade tones. NO fabric grain. Pure #00FF00 green background, ample gaps, strict grid, no text or grid lines. EXACTLY NINE HEADLESS upper-body+both-arms+LONG ROBE-SKIRT pieces,3columns x3rows. Absolutely NO head, face, neck length, hair, hat, legs, feet, weapons or effects. Show neck stump at collar and full hanging split skirt; common hip/belt attachment stays under robe. Broad short chest, no long adult torso. Row1: relaxed arms beside robe; breathing arms; running right fist forward left back. Row2: opposite running arms; forward-lean running; jump balancing arms. Row3: curled somersault torso rotated90clockwise, curled torso upside down180, curled torso270. All retain sleeveless dark brown cross-collar long skirt, pale thin hem piping and wrist wraps. Follow fourth reference HEADLESS LAYER format, but replace its cream short shirt with the BROWN LONG outfit in fifth reference.

The sleeveless BROWN LONG ROBE / CLOSED SHOES of the primary board take priority over obsolete cream cloth/bare-foot text in the style block.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### bodies_b_board40 — Giữ để xuất bản thử, chưa duyệt

Nguồn: `art/sprites/characters/lv1_30/sources/bodies_b_board40.png`.

```text
NEW Lv1 CLOTHING from the first column TOTAL-APPEARANCE row of the primary equipment board, shown enlarged in last attached image. This model OVERRIDES the old cream short shirt/bare feet: DARK EARTH-BROWN SLEEVELESS LONG CROSS-COLLAR ROBE/TUNIC, pale cream narrow piping on the diagonal collar and split skirt hems, brown belt at waist, robe split front panels hanging to MID-THIGH / near knee, brown wrist-wraps on bare sturdy forearms. Brown pants and BROWN CLOSED SHOES/ANKLE WRAPS (legs sheet only). Black hair and red ribbon belong to head, do NOT draw them here. NO straw hat. The total-character head+hair is0.40H, torso/limbs short broad sturdy to allow armor later. Style face/color identity stays that of the board. High resolution clean bold cartoon with thick dark brown contours, flat earth colors2–3sharp cel-shade tones. NO fabric grain. Pure #00FF00 green background, ample gaps, strict grid, no text or grid lines. EXACTLY NINE HEADLESS upper-body+both-arms+LONG ROBE-SKIRT attack pieces,3columns x3rows. Absolutely NO head, face, hair, hat, legs, feet, weapon, arrow or VFX. Neck stump, waist belt and full split skirt to mid-thigh; same short broad chest and outfit all9. First4MUST be sharply DIFFERENT silhouettes: row1col1 LOW GUARD leaning/crouching forward, near fist at right hip, opposite fist tucked; row1col2 DRAW: near fist sweeps LEFT BEHIND hip, elbow drawn far backward, shoulders twisted away, far arm balances; row1col3 SWEEP: near arm fully extended RIGHT at waist, torso leans forward and hip strongly rotates, far arm pulled back left. Row2col1 RECOVER: near fist in FRONT OF CHEST, bent elbow, shoulders unwind. Row2col2 horizontal thrust; row2col3 both fists low-front. Row3: archer far arm extended straight right at shoulder height, near hand draws beside cheek position just above collar; archer fully drawn holding; release near hand behind cheek. Far hand clearly visible. No overhead chops. Brown LONG SLEEVELESS cross-collar robe, cream narrow piping, bare upper arms, brown wrist wraps. Fourth image only shows headless formatting; fifth is required outfit.

The sleeveless BROWN LONG ROBE / CLOSED SHOES of the primary board take priority over obsolete cream cloth/bare-foot text in the style block.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### legs_board40 — Giữ để xuất bản thử, chưa duyệt

Nguồn: `art/sprites/characters/lv1_30/sources/legs_board40.png`.

```text
NEW Lv1 CLOTHING from the first column TOTAL-APPEARANCE row of the primary equipment board, shown enlarged in last attached image. This model OVERRIDES the old cream short shirt/bare feet: DARK EARTH-BROWN SLEEVELESS LONG CROSS-COLLAR ROBE/TUNIC, pale cream narrow piping on the diagonal collar and split skirt hems, brown belt at waist, robe split front panels hanging to MID-THIGH / near knee, brown wrist-wraps on bare sturdy forearms. Brown pants and BROWN CLOSED SHOES/ANKLE WRAPS (legs sheet only). Black hair and red ribbon belong to head, do NOT draw them here. NO straw hat. The total-character head+hair is0.40H, torso/limbs short broad sturdy to allow armor later. Style face/color identity stays that of the board. High resolution clean bold cartoon with thick dark brown contours, flat earth colors2–3sharp cel-shade tones. NO fabric grain. Pure #00FF00 green background, ample gaps, strict grid, no text or grid lines. EXACTLY TEN waist-to-sole PAIRS of legs,5columns x2rows. NO head, torso, arms, weapons, bare feet or sandals. Dark brown loose TROUSERS tucked into BROWN CLOSED SHOES/SHORT BOOTS and pale-brown calf wraps as Lv1 TOTAL row. No cream shirt/flap on waist: robe is separate upper-body layer. Broad short strong thighs and short calves, sturdy large rounded shoe soles. These legs form roughly1/3 of total chibi person height. Row1 standing straight feet SAME baseline; run stride right-forward; run compressed passing; wide airborne run; run opposite stride. Row2 passing opposite; jump tightly tucked; LOW GUARD deep bent knees feet widely planted SAME baseline; forward LUNGE right foot far forward both soles SAME baseline; compact tuck. Generous gap between pairs, same shoe/trouser design and short anatomy all10.

The sleeveless BROWN LONG ROBE / CLOSED SHOES of the primary board take priority over obsolete cream cloth/bare-foot text in the style block.

STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```


## 31/10/2026 — Sửa cổ, lưỡi đầy đủ và scene thử nhân vật mới (chưa duyệt)

- Nhánh `feat/g1-nhan-vat-chot` merge main mới nhất, giữ bản18có mục dùng trực tiếp bảng số.
- Nguồn đọc trực tiếp: `docs/ref/so_lieu_tham_khao.json`; đối chiếu bảng30khung trong
  Char.java và công thức vẽ. Không đưa mã/ảnh tham khảo mới vào repo.
- Mốc cổ thân đo lại trên pixel da ở cổ áo. Sửa các thân đứng/đánh/cung,
  đặc biệt15/16/17; head.dx/dy=0, tất cả cổ và hông ghép≤1px cả120trường hợp.
- Lưỡi dùng chính tranh kiếm tự vẽ đã có, bake trục ngang và kéo riêng phần lưỡi.
  Phần thép đo alpha0,782477H, không tính cán; Trảm Kiếm và Kiếm dùng lưỡi đầy đủ,
  vệt tự dựng bằng ImageDraw nối tại mũi. Không imagegen, không ảnh/mã bên ngoài mới.
  Script đã chạy: `python3 tools/update_pose_playtest.py`; phép đo/test ở
  `tools/check_lv1_sizes.py` và `prototype/tests/neck_blade_checks.gd`.
- Dữ liệu nguồn giữ nguyên30dòng, độ lệch hình, danh sách khung cầm vũ khí,
 6nhịp chiêuKiếm1 và8đất/7không chiêuCung28; hiệu ứng vẽ riêng chạy đúng chuỗi
 độ lệch và tâmảnh nguồn. Chỉ ánh xạ số hình sang tranh riêng đã có.
- Khác biệt có chủ đích:1pxnguồn32H→3logic để giữ cỡA0≈96H. Tranh người có
 đầu≈.402H thay vì.58H nguồn, cung≈.965H thay vì1.01H, giữ bộ hìnhLv1 và tỉ lệ
 đã yêu cầu trước; kiếm thép≈.782H theo.78Hnguồn. Không vẽ lại tỉ lệ người trong lượt sửa cổ.
- Khác biệt neo: ảnh riêng khác hình/crop nên nguyên dx/dy nguồn không tự khớp cổ/hông/tay.
 `registrations` lưu hiệu chỉnh từng lớp/khung/phái; công thức và raworigin nguồn giữ nguyên,
 kết quả phải khớp khớp thật≤1px. Vũ khí cầm/vung giữ grip ở tay; tên dùngdx/dynguồn
 quy đổi rồi hiệu chỉnh về dây thật. Không dịch tên rời dây chỉ để khớp origin nguồn.
- Khác biệt thời gian: JSONnguồn không ghi số giây; dùng.05s mỗi nhịp để giữ Kiếm.30s,
 thảCung.20s. Controller, hitbox, hitwindow, sát thương, cooldown lấy nguyênA0.
 Tên240logicpx/s giữ từ pilot, chưa có số tốc độ trong bảng nguồn; không coi đây là số game thật.
- Scene riêng `play_test.tscn` kế thừa A0, nền phẳng+3bục, pose_actor4lớp,
 phím/cảm ứng, đổi phái,2ôchiêu, hình nộm/số sát thương. main.tscn chỉ thêm nút điều hướng;
 không sửa config/controller/nhân vậtA0 cũ. Ảnh scene và viewer chụp bằng Godot/Xvfb thật.
- Chưa nghiệm thu mỹ thuật, cảm giác hay đa chạm Android; không tự duyệt tài nguyên.


## 31/10/2026 — Chạy / cầm / vệt / nhảy-lộn-rơi, lượt sửa theo đối chiếu nguồn

**Chưa duyệt mỹ thuật hoặc cảm giác chơi.** Chỉ prototype Lv1 trên nhánh feature,
không mở PR hay merge vào main. Không sửa config, controller và nhân vật A0 cũ.

- Đã dùng thư mục nguồn thật ngoài checkout đích; ls, các dòng Java kèm số dòng,
  output đầy đủ `ref_render.py --out /tmp/ref_render` và bảng raw số nguồn ↔ vị trí
  sprite thật được dán nguyên văn trong commit message. Ảnh tham khảo và ảnh so
  ba cột giữ riêng dưới `/tmp/ref_render`, không commit mã/ảnh tham khảo.
- Đã mở riêng đủ45ảnh gốc được chỉ định: đứng, chạy, cuộn trong gió, rơi, đánh,
  cầm hai vũ khí, hiệu ứng16/39và10/50. Dựng ảnh so từ Godot thật ở cùng H128px.
- **Khung2–7:** lấy nguyên từng dòng bảng30khung (đầu/chân/thân/vũ khí +dx,dy),
  số độ lệch hình của từng phần. Sáu chân mới tự vẽ riêng có6hash khác nhau,
  ít nhất4khung sải chân≥0,25H. Dùng thân thẳng, không dùng thân gập cũ.
  Khoảng đỉnh đầu–hông khi chạy lệch≤0,05H so với đứng. Raw và phần hiệu chỉnh
  crop/khớp được giữ riêng trong `registrations`, in đầy đủ bằng test placement.
- **Khung cầm0–7,12,21:** dùng raw vũ khí của từng khung và phần12/14, rồi đăng ký
  crop của tranh riêng về tâm nắm tay. Kiếm chéo xuống sau, có mask ngón tay từ
  chính pixel thân phủ lên chuôi. Cung nghiêng40°; vẽ thêm thân tay thấp đưa ra
  trước để dây không cắt phần thân giữa. Không dịch cung rời bàn tay để vượt test.
- **Lên7 / lộn8–11 / rơi12:** đối chiếu các dòng chọn khung khi vận tốc lên và
  rơi trong Java. Vẽ dáng cuộn tròn ôm gối, đầu cúi, bake4góc90°; vòng gió riêng
  neo tâm. Vẽ dáng rơi12một gối co cao, một tay giơ nắm. Khung13là thủ kiếm,
  không dùng cho rơi. Giữ nguyên A0lên đỉnh0,38s, một vòng lộn0,20s.
- **Kiếm, Trảm Kiếm:** giữ nguyên byte PNG lưỡi dài từ commit a528fc7; phần thép
  không cán đo≈0,782477H. Đọc trực tiếp nhịp chiêu1: hiệu ứng16ở nhịp2,39ở nhịp3.
  Vệt16bắt đầu cong ôm hông, qua lia to/dày;39thêm vệt ngắn lao trước, đuôi xé tơi;
  giữ thì tan. Texture vệt tự vẽ, neo tâm, baseoffset+frameoffset theo nguồn,
  vẽ trên người. Review tĩnh dựng lại cả hiệu ứng từ nhịp trước, không mất16khi39sinh.
  Test đo diện tích pixel alpha≥0,8 của vệt16lia≥0,25H²; Trảm Kiếm cùng dáng, xanh
  rõ và dày hơn. Viền tối mảnh; không dùng một pixel đậm để đại diện cả lõi.
- **Ô chiêu:** tăng riêng hai ô lên84×84logic, chữ hai dòng; kiểm font thật tại
  viewport960×540và1200×540. Không đổi layout điều khiển A0 gốc.
- **Khác số nguồn và lý do:** vẫn quy đổi3logic/px gốc cho bộ người≈96logic.
  Tỉ lệ đầu/trang phục riêng của bộ Lv1 giữ nguyên thay vì chép ngoại hình nguồn;
  số thứ tự hình được ánh xạ sang tranh mới. Crop khác nên đăng ký khớp được
  hiệu chỉnh riêng; raw dx/dy không sửa. Thời gian mỗi nhịp0,05s giữ hit/cooldownA0;
  bảng nguồn không ghi giây. Vệt mới to/đậm theo yêu cầu đọc rõ ở128px, không sao
  chép hình gốc. Các số và vị trí đã đặt có trong output placement, không giấu
  hiệu chỉnh trong sprite transform hoặc xoay node runtime.
- Kiểm số liệu bằng script PIL/NumPy trên PNG thật: `tools/check_motion_art.py`
  (nguyên script và output lưu trong report Python và commit message), cùng các
  test Godot chạy scene thật. Không coi headless là nghiệm thu Android.

### Ảnh tự vẽ / lời nhắc nguyên văn


#### slash_crescent_surge_v1 — v1, chưa duyệt

Tệp: `art/sprites/characters/lv1_30/sources/slash_crescent_surge_v1.png`.
Ảnh đã đính kèm: `art/sprites/characters/lv1_30/sources/compact_swings_50.png`.
Vệt cong và vệt lao ra trước, nền xanh rồi tách; không dùng ảnh tham khảo làm đầu vào.

Prompt nguyên văn:

```text
Edit only the attached independently authored effects sheet into a CLEAN TWO-CELL source sheet for a mobile game, landscape 1536x768 or similar. Pure solid #00FF00 background everywhere outside the two shapes. NO TEXT, NO weapons, NO swords, NO people. Remove all swords completely. LEFT CELL: one large, very thick horizontal sweeping white wind crescent shaped like a broad hooked C wrapping around an empty center where a fighter's hips would be, opening to the RIGHT. Its lower belly sweeps powerfully forward right and finishes in three large torn pointed tongues, NOT tiny particles. The upper hook curls back over the empty hip area. Broad opaque white core, pale cool-gray hard cel shading and thin dark brown-black contour. The crescent should have substantial filled area at least 40 percent of its bounding box. RIGHT CELL: one separate short thick white horizontal surge moving right like a ragged flame of displaced air, broad at its left rear, 3 big trailing torn tongues on the left, a crisp pointed broad spearhead on the right. Compact, not a thin line. White wind, no literal orange fire, no sparks. Both cells separated with a large green gutter, both have generous green padding, their bounding boxes must not touch. Preserve the clean strong contour and bold solid white of the attached original shapes, make the left crescent markedly thicker and more horizontal. This is source artwork for independent animation sprites, not a diagram or comparison board. Only these two shapes.
Style: 2D pixel art for a side-scrolling mobile action RPG, semi-realistic proportions about 4 heads tall, clean dark outline, 32-color palette, 3-tone shading with soft highlights, readable silhouettes, light source from top-left. Setting: northern Vietnam in the 10th century: limestone karst, rice fields, earthen ramparts, thatched or simple clay-tiled roofs, white reed-plume banners.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### run_strides_v1 — v1, chưa duyệt

Tệp: `art/sprites/characters/lv1_30/sources/run_strides_v1.png`.
Ảnh đã đính kèm: `art/sprites/characters/lv1_30/sources/legs_board40.png`.
Sáu dáng chạy mới, không cắt lại sáu dáng cũ.

Prompt nguyên văn:

```text
Redraw ONLY six running lower-body poses for the same original brown-clothed character as in the attached source sheet. Make a NEW 3-column by 2-row sprite source sheet, with six equally sized square cells, plenty of pure #00FF00 green gutters and margins. No labels, no lines, no text, no torsos, no heads, no arms. Each cell contains the waist belt, short two-flap brown tunic skirt, brown knee-length pants, cream calf wraps and BROWN SHOES matching the attached original (boots override the barefoot generic style below). All six face RIGHT. These must be visibly DIFFERENT frames of ONE RUN cycle: top-left right foot fully stretched forward and left leg pushing far backward; top-middle left foot leaving ground with right foot landing in front; top-right right leg supporting straight down and left knee lifting forward; bottom-left left foot reaching forward while right leg stretches far behind; bottom-middle right foot leaving ground and left foot contacting in front; bottom-right left leg supporting straight down and right knee passing forward. No squat, no deep crouch, no folded-in ball of legs. Tall extended knees and readable large stride gaps: in four of the six poses, shoe centers separated horizontally by at least the width of the waistband; do not overlap both shoes. The top waist location and total waist-to-ground height must be consistent in all six cells so the torso will remain upright. Show the entire waistband and both entire shoes in every pose. The skirt flaps are SHORT enough to show thighs and extended knees, not long enough to cover the strides. Chunky strong simple cartoon linework, broad coherent flat color shapes, clean readable at tiny mobile scale. Entire silhouettes isolated on flat #00FF00, no shadows on background. Follow attached ORIGINAL character's costume and style, but the locomotion must now have six distinct clear running strides. Boots and short tunic from the reference sheet take priority over generic costume below.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### air_poses_wind_v1 — v1, chưa duyệt

Tệp: `art/sprites/characters/lv1_30/sources/air_poses_wind_v1.png`.
Ảnh đã đính kèm: `prototype/pose_rig/art/lv1_30/head_7.png; prototype/pose_rig/art/lv1_30/body_0.png; art/sprites/characters/lv1_30/sources/run_strides_v1.png`.
Dáng cuộn, dáng rơi và vòng gió; chia lớp/bake góc offline.

Prompt nguyên văn:

```text
Create ONE original sprite source sheet on pure flat #00FF00 with THREE isolated items in a 2x2 grid (bottom-right cell empty). Match the same brown tunic, brown knee pants, tan calf wraps, brown shoes, thick dark outlines, large head, red hair ribbon and black topknot as these independently drawn character pieces. No text, no weapons, no arrows, no background shadows. TOP LEFT: complete right-facing chibi fighter tucked into a very compact somersault ball: both knees drawn tightly against the chest, hands hugging shins, back curled, chin lowered, head bowed to knees. Entire figure fits a near-circular silhouette, NOT an upright or stretched jumping person. Keep brown shoes and red hair ribbon readable. We will rotate this single compact pose offline 90 degrees per frame. TOP RIGHT: complete fighter in an upright falling pose facing RIGHT, one knee raised high in front and the other leg stretched downward, torso only slightly leaned forward, back fist raised above his head and forward hand clenched low outside the body at hip height, ready to hold a weapon. Arms must be visibly separate from face, knee and chest; no weapons. Keep the same large-head proportions as our existing sprites. BOTTOM LEFT: separate circular white swirling WIND RING, empty transparent-to-green center (no character inside), near-opaque solid white thick curved segments with small hard gray cel-shading and a thin dark brown-black outline. 3 connected bold sweeping hooked arcs forming one round rotating wind ring, a few large sharp torn ends, no particles/no blur/no glow. Enough empty center for the tucked fighter to sit within. All three objects comfortably inside their own cells with generous green space and gutters, completely separate; never overlap. The body costume stays brown (not the cream generic description), shoes not bare feet; prioritize attached independently drawn pieces. Only these three original items.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

#### bow_low_torso_v1 — v1, chưa duyệt

Tệp: `art/sprites/characters/lv1_30/sources/bow_low_torso_v1.png`.
Ảnh đã đính kèm: `prototype/pose_rig/art/lv1_30/body_0.png`.
Thân cung mới có tay thấp đưa xa ra trước; không đổi hình đầu/trang phục.

Prompt nguyên văn:

```text
Edit this original headless brown-tunic body into a headless upper-body sprite for holding a bow LOW and well AHEAD to the RIGHT. Preserve the same sleeveless brown crossover tunic, belt and cream edging, tan skin, wrist wraps, thick dark outline, scale and upright chest. No head, hair, legs, weapons, bow or text. Pure #00FF00 background. The chest/neck stays vertical, not crouched or hunched. Near/right arm must reach LOW and FORWARD: upper arm slopes down alongside ribs, elbow low near waist, forearm extends almost horizontally to the RIGHT at belt height, hand clenched into a solid holding fist. Put this fist far beyond the right edge of the torso, at least one entire torso-width from the chest center. This creates enough clearance for a diagonal bow/string entirely in front of the torso. Back/left arm remains lowered near the body. Keep the whole tunic skirt and both entire hands, with generous green margins. This is one connected torso with both arms, not a full character and not a sheet. Do not add any other objects. Brown outfit and wrist wraps of the attached sprite take priority over generic costume text below.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

Đối chiếu nhấp nhô chạy cuối lượt: tâm hông lấy đúng chênh dx/dy của dòng thân2–7 so với dòng thân0, nhân3logic; các crop chân mới đăng ký vào hông đó. Test in và so trực tiếp từng delta, tránh để chiều cao crop chân cũ làm thân gập hoặc làm sai nhấp nhô.


### 2026-11-01 — v3: chỉ dáng chạy2–7, hai phái (chưa duyệt hình)

Vẽ mới6 thân Kiếm,6 thân Cung và6 chân chạy. Trục cổ–hông đổ trước12°, tay tự do vung theo bước; tay cầm có nhịp nhẹ. Vạt áo giữa hông được rút ngắn còn0,4 chiều dài dưới hông để lộ chân; phần tay không bị rút. Hai thân Kiếm ở bước5/6 ghép cánh tay cầm thấp từ thân mới bước2, giữ nguyên tay tự do đang vung ra sau. Kiếm nằm sau lớp chân (z=-1); cung có bản đăng ký riêng cho chạy, nắm vào cành gỗ phía thấp, trục40°, ở phía trước. Không thay ảnh vũ khí cũ hay tư thế ngoài chạy.

Đã mở từng ảnh tham khảo chân24–29, thân6–11, vũ khí262/283 trước khi vẽ; đọc bảng30 khung và công thức neo/lật hướng. Chỉ dùng số liệu, không đưa ảnh hay mã tham khảo vào tệp theo dõi. Bằng chứng đường dẫn thật, ls, dòng mã có số dòng và output renderer nguyên văn nằm trong commit message.

Số liệu đặt khung: giữ nguyên bộ [hình,dx,dy] bên dưới từ bảng tham khảo. Nhấp nhô tâm hông bằng chênh tọa độ thân so với khung0 nhân3logic; mỗi crop mới có registration riêng để khớp cổ/hông/tay. Registration là đổi gốc crop tự vẽ, không thay số liệu nguồn; output PLACEMENT ghi đủ số nguồn, registration và vị trí thực của từng lớp, từng phái. Lệch có chủ đích về hình: thân nghiêng12°, tay vung mạnh, vạt áo ngắn hơn để đáp ứng yêu cầu chạy; kiếm vẽ sau đùi và cung chuyển điểm nắm trên gỗ để không che chân.

|Khung|Đầu [hình,dx,dy]|Chân|Thân|Vũ khí|
|---|---|---|---|---|
|2|[1, -10, 33]|[2, -10, 11]|[2, -9, 16]|[1, -12, 49]|
|3|[1, -10, 32]|[3, -11, 9]|[3, -11, 16]|[1, -13, 47]|
|4|[1, -10, 34]|[4, -9, 9]|[4, -8, 16]|[1, -12, 47]|
|5|[1, -10, 34]|[5, -11, 11]|[5, -10, 17]|[1, -13, 49]|
|6|[1, -10, 33]|[6, -9, 9]|[6, -8, 16]|[1, -12, 47]|
|7|[0, -9, 36]|[7, -5, 15]|[7, -10, 21]|[1, -8, 49]|

Kiểm tra thực:5/6 bước mỗi phái có khoảng cách bàn chân≥0,30H; tay tự do so với hông di chuyển xa nhất0,728H (Kiếm),0,584H (Cung), cả hai hướng. Diện tích chân bị vũ khí phủ thực tế tối đa5,947% (Cung); Kiếm0% vì vẽ sau chân, giao hình học vẫn được in riêng (tối đa0,787%). Sáu hash chân và sáu hash thân từng phái đều khác nhau; điểm tay được kiểm trên pixel da thật. Giữ nguyên24 dòng khung khác, tất cả ảnh cũ, chiêu, hiệu ứng, config và thông số chuyển động. Khung7 dùng chung khi đang lên nên thừa hưởng hình chạy mới; không đổi ánh xạ hay nhịp nhảy.

17/17 bộ Godot và5/5 trình kiểm Python qua.24 ảnh Godot thật qua Xvfb1600×720:8 bảng khung/đòn,8 màn chơi thử thường/chiêu,4 bảng chạy128px và4 màn điều khiển chạy; đủ hai phái/hai hướng. Report đầy đủ trong prototype/pose_rig/reports/run_v3_*checks.txt. Cảnh run_cycle_v3_review chỉ để chụp kiểm, không thêm vào luồng chơi. Không có kiểm thử thiết bị Android và chưa tự duyệt mỹ thuật.

#### Prompt sinh hình nguyên văn, bản v3 chưa duyệt

run_v3_torsos — ảnh riêng đã đính kèm: prototype/pose_rig/art/lv1_30/body_0.png; art/sprites/characters/lv1_30/sources/bow_low_torso_v1.png

```text
Redraw the attached independently authored brown torso into TWELVE DISTINCT FAST RUNNING upper-body sprites. Portrait sheet, EXACTLY 3 columns and 4 rows, generous pure #00FF00 green gutters and margins. Each cell ONE headless torso with both complete arms, brown sleeveless crossover tunic, cream edge, brown belt and SHORT skirt flaps. No head, hair, legs, weapons, lettering, labels or shadows. All face RIGHT, lean FORWARD 12 degrees from hip to neck (not a folded squat), with flaps flying BACK to the left. Cut skirt flaps very SHORT, so running thighs/knees will remain exposed. Keep the same clothing colors and chunky outlined hands as the attached original.
TOP TWO ROWS (six consecutive sword-running torso phases): the NEAR arm's CLOSED WEAPON-HOLDING FIST remains LOW BEHIND the hip (to LEFT), moving gently with the rhythm; the OTHER FREE ARM has a huge obvious shoulder/elbow swing opposite the running legs. These six free-fist positions in reading order: high forward near chest far RIGHT; forward at sternum level; down-forward at belt level; far BACK LEFT at waist level; up-back behind lower ribs; coming forward low. A complete free-arm pendulum from far forward to far back, with at least a torso-width change in free-fist position. Show the free arm clearly separate from the short tunic, not pasted onto the belt. The two fists must never touch or fuse.
BOTTOM TWO ROWS (six bow-running torso phases): weapon-holding NEAR fist is extended LOW FORWARD well to the RIGHT at belt level, at least one torso-width in front of chest center, moving gently; OTHER FREE arm swings through the same six opposing phase positions as above. Again six unmistakably different elbow and free-fist silhouettes, not a repeated stationary pose. Keep every torso upright but leaning 12 degrees forward, neck positions and belt size consistent. Keep all complete fists safely inside their cell. Brown sleeveless outfit and covered wrists from the source override the generic cream clothing below. Only twelve upper bodies, NO feet, NO lower legs.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

run_v3_legs — ảnh riêng đã đính kèm: art/sprites/characters/lv1_30/sources/run_strides_v1.png

```text
Redraw ONLY SIX dramatically different FAST RUNNING lower-body sprites matching the attached original brown pants, cream calf wraps and brown shoes. Landscape sheet,3 columns by2 rows, one isolated lower body per equally sized cell, pure solid #00FF00 green background, wide green gutters and margins. NO text, NO labels, NO torso, NO arms, NO head, NO weapons, NO ground or shadow. Keep a thin waistband at top; SHORT brown tunic skirt flaps flying behind to LEFT, only cover top quarter of thighs, never knees or calves. All six face RIGHT, all shoes point right. Knee-height pants, calf wraps and brown shoes are mandatory. Maximum readable limb separation at small mobile scale.
Six CLEARLY DIFFERENT fast stride phases in reading order: 1) right foot stretched far FORWARD heel contact, left leg stretched far BACK toe push, a huge split stride; 2) right leg bends under body bearing weight and left foot lifted far BEHIND at knee height; 3) explosive airborne extension, left leg stretched forward and right leg stretched back with BOTH entire shoes far apart horizontally; 4) left foot stretched far FORWARD heel contact and right leg stretched far BACK toe push (OPPOSITE LEAD LEG to first pose); 5) left leg bears weight as right knee swings high FORWARD with the two shoes still separated; 6) both feet in flight, right knee bent HIGH FORWARD and left foot kicked far BEHIND. At least FOUR of the six have shoe centers horizontally separated by MORE than 1.2 times the waistband width. Do not make two rows of the same three drawings: opposite leading legs, heel/toe contacts and raised-knee silhouettes must differ, not just tiny folds. Keep waist-to-lowest-foot height consistent, and make leg length/stride tall and athletic rather than coiled in a squat. Every complete shoe must be clearly visible outside the SHORT flying skirt flaps. Reference outfit, pants, wraps and shoes take priority over generic costume/bare-feet below.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

run_v3_sword_torsos — ảnh riêng đã đính kèm: /workspace/generated_images/exec-42340803-710c-42b9-93f8-459974f3f89c.png (bản lưu art/sprites/characters/lv1_30/sources/run_v3_torsos.png)

```text
Redraw ONLY SIX sword-running upper bodies based on this original torso source. Landscape sheet3columns2rows, exactly6isolated headless torsos, pure flat #00FF00 background, generous gutters and margins. No words, weapons, legs or heads. Brown sleeveless crossover tunic, cream edge, belt, VERY SHORT flared-back skirt tips, tan skin and wrapped wrists. Every chest leans12degrees to the RIGHT, not crouched. EVERY torso MUST have TWO COMPLETE VISIBLE ARMS AND TWO CLOSED FISTS. Do not hide, omit or merge either fist, including the back-swing frames. One NEAR arm is the WEAPON ARM: keep its fist LOW BEHIND the hip to the LEFT in ALL six pictures, near the lower left of the waistband, with only small rhythmic motion. This fist never jumps to the right of the body. Keep the near upper arm sloping down/back, elbow low, fist below the hip. The OTHER FREE ARM swings broadly through six DIFFERENT phases, in reading order:1 high far-forward RIGHT at chest level,2 forward at middle ribs,3 lowered forward RIGHT at belt level,4 far-BACK LEFT at shoulder/rib level with fist visibly ABOVE and LEFT of the low weapon fist,5 high BACK LEFT bent elbow (fist still visibly ABOVE the weapon fist),6 coming forward low but clearly separate from low rear weapon fist. The leftward free-arm swing of4/5 is HIGH; the stationary rear weapon fist is LOW, so both entire fists remain separate and unmistakably visible. Neither hand intersects the tunic or another hand. Make the six free-arm silhouettes strongly different, not repeated standing arms. Keep torso and neck height/size consistent. Short flaps blow LEFT, leave almost all thighs for a separate leg layer. Preserve the same simple original outfit and dark chunky contour; no fantasy armor or ornate details. Brown outfit overrides the generic cream clothes below.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```


### 2026-11-01 — Lv1 v4: chân chạy khung3 và nắm chuôi giữa cung (chưa duyệt hình)

Phạm vi: thay riêng hình chân khung3 bằng bản vẽ mới, chân sau hạ xuống và đưa xa sau để thấy cả cẳng chân quấn vải và giày. Năm hình chân chạy còn lại, toàn bộ thân/tay/đầu và mọi ảnh vũ khí cũ giữ nguyên. Dùng bản cung cầm tay mới, điểm nắm nằm trên phần quấn giữa; áp đúng0–7,12,21. Các ảnh giương/bắn, nhịp chiêu, ánh xạ hoạt ảnh và thông số A0 không đổi. Tất cả ảnh cũ và metadata asset cũ được kiểm nguyên vẹn.

Đã mở riêng chân24–29 (đặc biệt25), thân6–11 và cung283; đọc bảng khung tại dòng345 và giải mã trực tiếp phần chân mặc định/phần cung14. Phần cung14 có hình283, lệch[-10,9]. Giữ nguyên bộ[hình,dx,dy] nguồn của mọi lớp. Registration chỉ đổi gốc crop của chân mới/cung mới, giữ nguyên hông và nắm tay thực; report PLACEMENT in số nguồn, độ lệch hình, số registration và tọa độ đặt thật. Bốn mục bằng chứng đầy đủ, gồm ls nguồn thật, dòng mã có số dòng và renderer, được lưu nguyên văn trong commit message.

Lệch hình có chủ đích: chọn phương án chân đầu tiên (chân sau thấp) thay phương án co cao; bản sinh đầu tiên dùng chân trần nên sửa riêng thành giày nâu khớp bộ cũ. Cung tự vẽ được chuẩn hóa chiều dài150pixel nguồn, nén phương vuông góc trục0,4 để chuôi giữa gần trung điểm hai đầu theo giới hạn0,05H; trục khoảng41,18°. Không dời grip xuống cành dưới. Khung6 Cung: đầu dưới đi ngang bàn chân đang nhấc, nên vẽ cung sau chân gần (z=-1), giữ nguyên vị trí tay và cung; các khung cung khác vẫn lớp3. Không xoay sprite lúc chạy.

Bảng số dùng để đối chiếu (đơn vị nguồn):

|Khung|Chân [hình,dx,dy]|Thân|Vũ khí|
|---|---|---|---|
|0|[1, -7, 7]|[1, -11, 15]|[1, -9, 45]|
|1|[1, -7, 7]|[1, -11, 16]|[1, -9, 46]|
|2|[2, -10, 11]|[2, -9, 16]|[1, -12, 49]|
|3|[3, -11, 9]|[3, -11, 16]|[1, -13, 47]|
|4|[4, -9, 9]|[4, -8, 16]|[1, -12, 47]|
|5|[5, -11, 11]|[5, -10, 17]|[1, -13, 49]|
|6|[6, -9, 9]|[6, -8, 16]|[1, -12, 47]|
|7|[7, -5, 15]|[7, -10, 21]|[1, -8, 49]|
|12|[8, -4, 13]|[8, -14, 27]|[1, -9, 49]|
|21|[8, -4, 13]|[8, -15, 25]|[1, -10, 46]|

Kết quả:18/18 bộ Godot headless và6/6 trình kiểm Python qua. 24 trường hợp chạy (6khung×2phái×2hướng),48 bàn chân: hai vùng giày nhìn thấy tách biệt ở mọi khung; từng bàn chân bị thân/tay/đầu/vũ khí che nhiều nhất24,733% (PIL), dưới30%. Hai bàn chân khung3 mới lộ riêng, chân sau không bị che; cả6/6 khung mỗi phái đạt sải≥0,3H. Test dùng polygon toàn giày giao alpha thật, tính che theo thứ tự lớp và thành phần liên thông; không lấy một pixel đế chân làm bằng chứng cả bàn chân. Phát hiện dữ liệu cũ khung3 đặt cả hai landmark đế lên cùng giày trước; kiểm mới chọn riêng đúng giày sau. Không kết luận sai rằng riêng diện tích giày cũ đã vượt30%: vấn đề đọc dáng còn gồm cẳng chân bị che.

Cung cả20 trường hợp khung/hướng: tay–trung điểm/H=0,044744705, hai đầu cách tay36,377379 và39,063707logic, độ chênh7,384610% với mẫu số là khoảng ngắn hơn. Grip khớp tâm tay≤1pixel, trên vùng quấn giữa có alpha thật. Test đối chứng bác cả điểm nắm cũ của cung đứng và cung chạy.

Đã chụp24 ảnh Godot thật bằng Xvfb1600×720: dải30khung, các đòn, dải chạy128px và màn chơi thử, đủ hai phái/hai hướng. Chỉ vị trí bắt đầu của chế độ chụp --run hướng phải được dời khỏi hình nộm để nhìn rõ; không đổi luồng chơi. Report tại prototype/pose_rig/reports/carry_v4_*checks.txt. Chưa duyệt mỹ thuật, chưa kiểm thiết bị Android.

#### Prompt nguyên văn — v4

carry_v4_leg_candidates — ảnh riêng đã đính kèm: prototype/pose_rig/art/lv1_30/run_v3_legs_1.png

```text
Edit the attached original leg sprite into TWO candidate running leg poses side by side, generous empty space between. Headless, armless, torso-free legs ONLY, brown knee-length trousers, tan ankle wraps and bare chunky feet, bold same dark outlines and same colors as original. Preserve the belt and pelvis position, scale of limbs, the forward planted right foot and right bent leg. Fix the rear LEFT leg: rear thigh extends BACK to LEFT, knee bends, but rear calf and entire rear foot are LOWER and FARTHER LEFT than the attached sprite, not tucked against the hip. Rear knee below pelvis by 20% of leg height; rear heel below pelvis by 55% of leg height. Both feet completely exposed, separated widely horizontally; left rear foot about half-way between hip and lowest front sole in height. Dynamic running recovery with knee folded, absolutely TWO complete legs, no arm or sword. Candidate1: rear calf slopes down-left and bare rear toes point down-left; candidate2: rear calf near horizontal, rear foot points down. Two original concepts, not a presentation/comparison, no text, no labels or dividers. Solid pure #00FF00 background. Preserve costume and outline from the attached original over generic style text. No added effects.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

carry_v4_leg_shoes — ảnh riêng đã đính kèm: /workspace/generated_images/exec-6d7af01f-26e7-4e2e-94a7-05385fe6b29f.png (bản lưu sources/carry_v4_leg_candidates.png); prototype/pose_rig/art/lv1_30/run_v3_legs_1.png

```text
Edit the FIRST attached two-candidate leg artwork. Keep BOTH running silhouettes, waist, pants, calf wraps, outlines, colors and exact foot positions. Change ONLY the four bare feet into chunky CLOSED BROWN SHOES matching the second attached original sprite. Rounded slightly pointed brown shoes with warm beige sole edging and dark outlines, NO toes visible. Do not alter any leg pose. Left candidate remains long low rear calf and low-left rear shoe, right candidate has folded raised rear calf. Preserve generous spacing, pure flat #00FF00 background and no labels. Costume consistency with the original second image overrides generic bare-feet wording below.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

carry_v4_bow — ảnh riêng đã đính kèm: prototype/pose_rig/art/lv1_30/bow_hold.png

```text
Edit this isolated wooden sports bow for a cartoon character. Create two original variants on flat #00FF00 green, side by side with empty space between; no text or people. Same simple brown wood, pale cream string and beige wrapped handle as reference. Each bow diagonal from LOWER LEFT to UPPER RIGHT, about50 degrees from vertical. Upper and lower limbs are equal length and mirror-symmetric about the middle wrapped handle. The wrapped handle must be at the center, equally far from both ends. Make wood curvature VERY SHALLOW, almost straight with small recurve ends: middle wooden handle just4 percent of total length to the RIGHT of the straight string. String connects both ends at LEFT behind the wood. First variant shallow symmetric curve; second even shallower. Clear dark contour, flat warm brown shading, simple uncluttered outline. No arrows or hands. Only these two simple isolated objects. Preserve the sporting object's simplicity over other generic style details.
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```
