# Danh sách hạng mục thiết kế

Mỗi dòng là một hạng mục: mã (dùng làm tên file), mô tả ngắn, và khuôn prompt (P..) hoặc tài liệu đặc tả cần theo. Đánh dấu `[x]` khi người dùng đã duyệt. Giai đoạn sau chỉ mở khi giai đoạn trước đã duyệt đủ.

**Các giai đoạn là thứ tự sản xuất thiết kế, không phải thứ tự lập trình.** Giai đoạn 1 dựng một bộ mẫu chuẩn gồm nhân vật chính, một vùng và màn chơi, để mọi thứ làm sau so theo đó cho đồng bộ. Code game thật chỉ bắt đầu khi qua Mốc A của `11_design_freeze.md`. A0 và lát cắt mẫu cuối Giai đoạn 1 là ngoại lệ prototype riêng, không mở khóa code game thật.

Có bốn loại hạng mục:

- **Ảnh** (mã `chr_` trừ `chr_dbl_anim_*`, `npc_`, `enm_`, `bos_`, `map_..._bg`, `map_..._tiles`, `mnt_`, `ui_`, `ico_`, `por_`, `vfx_`, `prp_`, `cs`): tạo bằng `$imagegen`, lưu ở `art/concept/`.
- **Đặc tả** (mã `scr_`, `flw_`, `lay_`, `beats_`, `cs.._sb`): viết Markdown theo tài liệu đặc tả, lưu ở `design/`.
- **Dữ liệu ghép hoạt ảnh** (`chr_dbl_anim_*`): vị trí, góc, thứ tự lớp từng bộ phận theo từng khung, cùng thời lượng/sự kiện trong `09_animation_spec.md`; không phải ảnh vẽ lại trọn bộ động tác cho mỗi trang bị.
- **Sơ đồ dựng bằng script** (`lay_` và `flw_` có ảnh PNG đi kèm): dựng từ file đặc tả, không tạo bằng AI.

## Giai đoạn 0 — Chốt phong cách và ảnh gốc

- [x] `sty_explore_a` — mẫu A pixel chibi trong bảng P0 điều chỉnh; đã so sánh và không chọn (ảnh cắt lưu `art/concept/style/sty_explore_a_v2.png`)
- [x] `sty_explore_b` — mẫu B pixel bán hiện đại trong bảng P0 điều chỉnh; **đã chọn** (ảnh cắt lưu `art/concept/style/sty_explore_b_v2.png`)
- [x] `sty_explore_free` — **bỏ qua có phê duyệt**, không tạo ảnh không STYLE vì đã xác định hướng pixel; thay bằng mẫu C vẽ tay để đối chiếu (`art/concept/style/sty_explore_c_v2.png`); xem `05_log.md`
- [x] Người dùng chọn **B — pixel bán hiện đại** ngày 28/10/2026; đã cập nhật Art Bible, thông số và nhật ký
- [x] `chr_dbl_base` — ảnh gốc Đinh Bộ Lĩnh xoay bốn hướng (P1). **Đã duyệt v9**, lưu `art/reference/ref_dinh_bo_linh.png` (dựng lại từ ảnh chụp màn hình; thay bằng file gốc nếu tìm được)
- [ ] `chr_dbl_parts` — **đang làm, chưa duyệt:** đã có concept một tờ/16 mảnh, PNG co theo một s chung và khớp đo lại, đầu do Claude vẽ tay từng pixel, tay đã rút ngắn, rig Sprite2D và báo cáo kiểm (`reports/g1_parts_art_report.md`); chờ Claude/người dùng soát mỹ thuật. Bộ bộ phận theo tỉ lệ nhân vật **96 px** (P2): đầu kèm tóc, thân, cánh tay trên/dưới gần và xa, đùi/cẳng chân gần và xa, bàn tay, vũ khí. Từng mảnh có điểm khớp, phần vẽ bù bị che, hệ tọa độ và lớp gần/xa. Tạo bằng imagegen + snap_pixel + sửa pixel bằng script, kiểm bằng check_sprite và kiểm khớp phù hợp; Claude/người dùng duyệt từng mảnh bằng script và bằng mắt. Xem giới hạn công cụ hiện tại trong art bible
- [x] `palette` — bảng 32 màu rút từ các ảnh đã duyệt, dựa trên 16 màu khung xương trong art bible; lưu `art/reference/palette.png`. **Đã duyệt palette_v3** (kèm `palette.gpl`)
- [ ] `chr_dbl_idle_side_96` — **PLACEHOLDER**, `art/sprites/characters/chr_dbl_idle_side_96.png`: báo cáo kỹ thuật cũ ghi kích thước/chiều cao/palette/nền/NEAREST; **chưa đạt mỹ thuật và chưa được người dùng duyệt**, không coi báo cáo cũ là kiểm đạt theo quy trình bộ phận mới. Giữ làm mẫu tạm để kiểm thử nguyên mẫu Godot; thay bằng pose ghép từ bộ phận mới theo art bible sau khi qua kiểm tra và duyệt; không yêu cầu thuê họa sĩ hay chỉnh tay. Không đánh dấu `[x]` trước khi duyệt bản thay thế.

## Giai đoạn 1 — Bộ mẫu chuẩn

- [ ] `chr_dbl_rig_greybox` — **bước 1: đã dựng bản thử, chưa duyệt**. Khối màu 96 px, 16 mảnh có khớp, 13 clip/48 khung trong `prototype/rig/`; bảng bộ phận, đo ảnh nghiêng và thời lượng tại `16_rig_nhan_vat.md`. Có công tắc rig/cung, xem pose và contact sheet. Chờ người dùng duyệt tỉ lệ/khớp/pose trước khi vẽ; không đóng `chr_dbl_parts`, trang bị hay động tác thành phẩm.

- [ ] `chr_dbl_t1` — bộ phận thay thế trang bị bậc 1 (áo, quần, vũ khí Đao/Cung), chung điểm khớp và dữ liệu hoạt ảnh; không vẽ lại cả động tác (P3)
- [ ] `chr_dbl_anim_dao_t1`, `chr_dbl_anim_cung_t1` — dữ liệu ghép bộ phận theo từng frame (vị trí, góc, thứ tự lớp, thời lượng, hit/spawn), đủ số khung trong `09_animation_spec.md`; số khung đang chưa chốt phải dựng/duyệt trước khi đóng hạng mục. Lộn đỉnh/chiêu lớn có thể thêm khung vẽ riêng khi cần (P4)
- [ ] `map_dao_uc_bg`, `map_dao_uc_tiles` — cảnh nền và tileset Đào Úc (P9, P10). Khi duyệt cảnh nền, sao chép thành `art/reference/ref_map_hoa_lu.png` cho tới khi có cảnh làng Hoa Lư
- [ ] `lay_dao_uc` — bố cục Đào Úc kèm đấu trường boss (`08_map_layout.md`, đã có bản ví dụ)
- [ ] `enm_tho_phi`, `enm_hau_ngo_giao`, `enm_hau_ngo_cung`, `enm_doi_truong_hau_ngo` — quái Đào Úc (P6)
- [ ] `bos_hau_ngo_tien_phong` — tướng tiên phong Hậu Ngô (P7)
- [ ] `ui_kit` — bộ khung giao diện (P12). Khi duyệt, sao chép thành `art/reference/ref_ui_kit.png`
- [ ] `ui_hud`, `scr_05_hud` — mockup và đặc tả màn chơi SCR-05 (P13, `06_screens.md`)
- [ ] `ui_hud_boss`, `scr_06_boss` — màn chơi khi đánh boss SCR-06
- [ ] `vfx_basic` — hiệu ứng cơ bản (P15)

- [ ] `slice_dao_uc_parts` — **lát cắt mẫu cuối Giai đoạn 1**: ghép bản đồ Đào Úc + nhân vật ghép bộ phận + **1 quái** trong `prototype/` để Claude/người dùng duyệt trước khi sang Giai đoạn 2. Đây là ngoại lệ prototype giống A0, chỉ thử cảm giác/độ đọc/khớp/hoạt ảnh; mã bỏ đi, không phải mã game thật và không chép sang `co_lau_game`. Chưa thực hiện hoặc duyệt lát cắt trong lần cập nhật tài liệu này.

## Giai đoạn 2 — Mở đầu và Hồi 1 đầy đủ

- [ ] Bản đồ (mỗi bản đồ một `_bg`, một `_tiles`, một `lay_`): `lang_hoa_lu` (khi duyệt cảnh nền, thay `ref_map_hoa_lu.png`), `dong_chiem`, `ben_do`, `trang_an`
- [ ] Quái: `enm_bu_nhin`, `enm_chuot_dong`, `enm_ran_nuoc`, `enm_co_dong`, `enm_chuot_cong_lon`, `enm_lon_rung`, `enm_nhim`, `enm_cua_dong`, `enm_lon_loi_nanh`, `enm_khi_da`, `enm_doi_hang`, `enm_ho_con`, `enm_ho_van`, `enm_hao_truong` (P6)
- [ ] NPC: `npc_dam_thi`, `npc_chu`, `npc_dinh_dien`, `npc_nguyen_bac`, `npc_dinh_lien`, `npc_tho_ren`, `npc_tho_may`, `npc_ba_hang_com`, `npc_ong_lang`, `npc_su_tru_tri`, `npc_tre_chan_trau` (P5)
- [ ] `chr_dbl_child` — Bộ Lĩnh lúc nhỏ cho CS01 đến CS03 (P5, cùng gương mặt ảnh gốc nhưng 10 tuổi)
- [ ] `chr_dbl_t2` — bộ phận thay thế áo, quần, vũ khí bậc 2; dùng lại dữ liệu động tác và khớp (P3)
- [ ] `mnt_trau` — trâu (P11)
- [ ] `por_set_01` — chân dung: Bộ Lĩnh, Đàm thị, người chú, Đinh Điền, Nguyễn Bặc, Đinh Liễn (P8)
- [ ] `ico_set_01` — 16 biểu tượng vật phẩm đầu game (P14)
- [ ] Storyboard: `cs01_sb` đến `cs06_sb` (đã có bản nháp trong `10_storyboard.md`), `beats_hoi1`
- [ ] Tranh cutscene: `cs01_1` đến `cs06_3`, đúng số tranh trong storyboard (P17)

## Giai đoạn 3 — Toàn bộ màn hình và luồng

- [ ] Đặc tả `scr_01` đến `scr_22` theo `06_screens.md`
- [ ] Mockup cho mọi màn (P13, mã `ui_<tên>`), gồm cả `ui_world_map` (SCR-14) và `ui_base` (SCR-22)
- [ ] Mockup riêng cho trạng thái khác bố cục (P13b): thợ rèn đang rèn, thành công, thất bại; SCR-13 thẻ Gói khi mất mạng, đang chờ Google Play, đã sở hữu; chọn ô khi xóa; giữ ải giữa hai đợt
- Mockup các trạng thái ngân phiếu nạp (thẻ Nạp, offline có ngân phiếu nạp, giao dịch đang chờ, số dư âm, SCR-19) **không làm ở bản đầu**; để tới mốc C
- [ ] Sơ đồ luồng `flw_f1` đến `flw_f8` dựng thành PNG từ `07_ui_flow.md`
- [ ] Hoạt ảnh giao diện theo `09_animation_spec.md` (búa rèn, số sát thương, sao giữ ải): concept dạng bảng khung
- [ ] `ico_set_02` trở đi cho đủ vật phẩm, tiền tệ và biểu tượng hệ thống

## Giai đoạn 4 — Hồi 2 và Hồi 3

- [ ] Bản đồ (`_bg`, `_tiles`, `lay_`): `dam_dai_hoang`, `bo_hai_khau`, `bai_boi`, `cua_bien`, `duong_rung`, `song_dang_chau`, `binh_kieu`
- [ ] Giữ ải: `prp_giu_ai` (P16), `map_ai_tam_diep_bg`, `lay_ai_tam_diep` (đã có bản ví dụ), mockup `ui_giu_ai` và đặc tả `scr_07`
- [ ] Quái vùng ven biển và sông nước theo `08_map_layout.md` mục 6 (P6)
- [ ] Boss: `bos_hai_tac`, `bos_pham_bach_ho` (P7)
- [ ] NPC: `npc_tran_lam`, `npc_le_hoan`, `npc_luu_co`, `npc_trinh_tu`, `npc_ngo_xuong_xi`, `npc_lai_buon`, `npc_buon_ngua` (P5)
- [ ] Bộ phận thay thế áo/quần/vũ khí `chr_dbl_t3`, `chr_dbl_t4`, dùng lại dữ liệu động tác; thú cưỡi `mnt_ngua`
- [ ] `por_set_02`; storyboard `cs07_sb` đến `cs13_sb`, `beats_hoi2`, `beats_hoi3`

## Giai đoạn 5 — Hồi 4 và Hồi 5

- [ ] Bản đồ (`_bg`, `_tiles`, `lay_`): `do_dong`, `tay_phu_liet`, `te_giang`, `sieu_loai`, `tien_du`, `duong_lam`, `tam_dai`, `phong_chau`, `hoi_ho`, `kinh_thanh`, `duong_ve_kinh`, `ao_canh`, bốn ải còn lại
- [ ] Quái: lính 8 sứ quân theo màu cờ, kỵ binh, chó chiến, ngựa hoang, lính mai phục, gấu ngựa, voi rừng, đỉa trâu, cá sấu chúa, tàn quân (P6)
- [ ] Boss: `bos_do_canh_thac`, `bos_nguyen_sieu`, `bos_la_duong`, `bos_ly_khue`, `bos_nguyen_thu_tiep`, `bos_nguyen_khoan`, `bos_kieu_cong_han`, `bos_kieu_thuan` (P7)
- [ ] NPC: `npc_ngo_nhat_khanh`, `npc_ngo_chan_luu` (P5)
- [ ] Bộ phận thay thế áo/quần/vũ khí `chr_dbl_t5`, `chr_dbl_t6`, `chr_dbl_t7`, dùng lại dữ liệu động tác; thú cưỡi `mnt_voi` và thú cưỡi ngoại hình
- [ ] Hiệu ứng `vfx_skills_dao`, `vfx_skills_cung`, hiệu ứng đòn đặc biệt của boss (P15)
- [ ] Storyboard `cs14_sb` đến `cs25_sb`, `beats_hoi4`, `beats_hoi5`; mockup `ui_coronation`

## Giai đoạn 6 — Chuẩn hóa và chốt

- [ ] Bộ mẫu chuẩn đúng kích thước: Đinh Bộ Lĩnh ghép bộ phận bậc 1 đủ dữ liệu động tác, từng mảnh được Claude/người dùng duyệt bằng script và bằng mắt; một quái, một boss, một tileset theo `04_review.md`
- [ ] File palette cuối cùng
- [ ] Rà mốc A của `11_design_freeze.md` cùng người dùng

## Giai đoạn 7 — Quảng bá

- [ ] `art_key_visual` — ảnh chính cho trang Cửa hàng Play
- [ ] `art_logo_ideas` — phác ý logo, không chữ. Logo thật do người thiết kế.
