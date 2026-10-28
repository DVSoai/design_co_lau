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
