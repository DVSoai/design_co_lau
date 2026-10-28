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
