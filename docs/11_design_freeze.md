# Danh sách chốt thiết kế

Mốc A chia thành A1–A5 theo hồi. Bản offline có A0 (thử cảm giác), A1–A5 (duyệt thiết kế theo hồi), B (trước khi phát hành); C dành cho bản có ngân phiếu nạp. Codex không tự đánh dấu mục nào; chỉ đánh dấu khi người dùng nói đã duyệt. Sau khi qua một mốc, mọi thay đổi thiết kế phải ghi vào `docs/05_log.md` kèm lý do.

- **A1:** mở đầu + Hồi 1 + toàn bộ hệ thống lõi: hai phái, tiềm năng, kỹ năng, trang bị, cường hóa/luyện đá/tách, túi đồ, cửa hàng NPC, lưu game ba ô, HUD, cửa hàng món vĩnh viễn bản đầu và kiến trúc `co_lau_game`. Qua A1 được bắt đầu code game thật.
- **A2:** Hồi 2; mở ngựa chiến và thuyền chiến.
- **A3:** Hồi 3; mở căn cứ Hoa Lư, giữ ải, dịch chuyển và tinh luyện.
- **A4:** Hồi 4; mở voi chiến.
- **A5:** Hồi 5 + epilogue.
- **Mốc B — Trước khi phát hành:** hồ sơ pháp lý, cách xác định tuổi, bảng giá thương mại, thanh toán thật, kiểm tra quyền sử dụng tài nguyên.

Thiết kế Hồi 2–5 làm song song với code sau A1; nội dung Hồi n chỉ đưa vào `co_lau_game` sau khi qua An. Trang bị t1/t2 chốt A1, t3 ở A2, t4 ở A3, t5/t6 ở A4, t7 ở A5. Hệ thống lõi chốt tại A1 phải tự đặt lại và duyệt **toàn bộ** bảng số, kể cả mức dùng ở hồi sau (như cường hóa +1…+16 và kinh nghiệm 1–60); hệ thống mở lần đầu ở hồi sau chốt toàn bộ số tại mốc hồi đó. Không thay số trong tác vụ chia mốc này.

Sau khi qua A1, thay đổi một hệ thống lõi đã chốt phải ghi `docs/05_log.md` kèm lý do, nêu phần code bị ảnh hưởng và được duyệt lại. Chuyển phần pháp lý sang B không có nghĩa bỏ qua: nếu yêu cầu pháp lý buộc đổi thiết kế đã chốt ở A1 hoặc An thì sửa thiết kế, ghi nhật ký và duyệt lại phần bị ảnh hưởng.

Mục A0 và phần quyết định lịch sử bên dưới giữ nguyên văn; các câu nói về mốc trước khi chia trong A0 không cấp quyền vượt quy tắc A1–A5 mới. Các mục **(Cần người dùng xác nhận)** được đưa tạm vào A1 khi tài liệu chưa xác định được lần dùng đầu; đây không phải tự chốt hồi hay tự duyệt. Bảng đối chiếu từng điều kiện: [milestone_a_by_act_mapping.md](reports/milestone_a_by_act_mapping.md).

## Quyết định đã chốt (28/10/2026)

Các quyết định dưới đây người dùng đã đồng ý; tài liệu đã cập nhật theo. Đây không phải mục chờ duyệt.

- Đã chọn **B — pixel bán hiện đại** (28/10/2026); P0 đã duyệt, xem `docs/05_log.md`.
- Không có hồi sinh tại chỗ. Thua thì về điểm hồi sinh; trong trận boss có nút "Đánh lại".
- Thêm SCR-14 Bản đồ vùng, cho đi nhanh miễn phí tới làng, căn cứ và điểm hồi sinh đã mở.
- SCR-22 Căn cứ Hoa Lư có 4 công trình, mỗi công trình 3 cấp, không có thời gian chờ xây. Lợi ích: trại lính (tướng đi cùng mạnh hơn), kho lương (tăng lương thảo tối đa), chuồng ngựa (tặng thức ăn thú), lò rèn (giảm phí rèn 5%, 10%, 15%). Chi phí vật liệu và các con số khác chưa chốt.
- Toàn bộ gameplay chơi offline. Đăng nhập Google luôn tùy chọn; chỉ hỏi khi người chơi chủ động nạp, dùng ngân phiếu nạp hoặc bật sao lưu, và luôn có nút "Để sau".
- Ngân phiếu có hai nguồn: ngân phiếu thưởng (nhận và tiêu offline), ngân phiếu nạp (máy chủ quản lý). Trừ thưởng trước, nạp sau. Giao dịch kết hợp do máy chủ xác nhận, có mã giao dịch chống trừ hai lần (`12_ngan_phieu.md`).
- Bản phát hành đầu tiên chỉ bán món vĩnh viễn qua Google Play (gói khởi đầu, đồ thời trang, thú cưỡi ngoại hình, túi da cấp 3), không có ngân phiếu nạp và không có máy chủ riêng. Món đã mua thuộc tài khoản Google Play và dùng được ở cả ba ô. Thiết kế ngân phiếu nạp giữ lại cho bản sau (`12_ngan_phieu.md`, mục 0 và 12).
- Engine Godot 4 với GDScript. Có kế hoạch chuẩn bị chuyển online nhưng chưa làm phần online (`14_online_migration.md`).
- Hoàn tiền: số dư nạp được âm, khóa giao dịch dùng ngân phiếu nạp cho tới khi bù xong; không thu hồi món đã mua, không khóa gameplay; sổ giao dịch chống áp dụng hoàn tiền hai lần.

## Mốc A0 — Bản thử cảm giác

**Trạng thái: Đã qua mốc A0 (28/10/2026).** Người dùng đã chơi thử và chấp nhận bộ mặc định Kiểu cổ điển tại commit `7973729`, trên Realme RMX3760 (Android, 1600×720), Godot 4.7.2. Số đo/thao tác được ghi Đã duyệt trong `13_thong_so.md`; sprite/HUD thành phẩm và toàn bộ Mốc A chưa được coi là duyệt. Quy tắc không code trước Mốc A vẫn giữ nguyên với **game thật**.

### Mục đích

Các thông số cảm giác dưới đây đã chốt tại A0; mục khác giữ trạng thái trong `13_thong_so.md`:
- Khung thiết kế **960×540**, stretch canvas_items/expand/fractional/nearest theo viewport thực; Android fullscreen + immersive; nhân vật chính **96 px**, khung 128×128.
- Tốc độ chạy; độ cao và thời gian nhảy.
- Va chạm và hitbox.
- Camera: vùng chết và tầm nhìn trước.
- Nhịp đòn chém cơ bản.

### Phạm vi

- Một dự án **Godot 4 riêng** trong thư mục `prototype/`.
- Hình tạm: sprite **PLACEHOLDER** và khối màu.
- Một bản đồ thử dài khoảng **ba màn hình ngang**, gồm đất bằng, bậc cao, hố và bục nổi.
- Đi, nhảy, rơi, chém thường và **một hình nộm nhận đòn**.
- Nút/HUD và bảng chỉnh trong prototype chỉ là giữ chỗ để thử. Không có giao diện game thành phẩm, lưu game, hệ thống vật phẩm, nhiệm vụ hoặc âm thanh.

### Quy tắc

- Mã trong `prototype/` là **mã bỏ đi**, không chép sang game thật.
- Mọi thông số của nguyên mẫu đặt trong **một file cấu hình**.
- Ngoại lệ prototype tiếp theo: lát cắt cuối Giai đoạn 1 gồm Đào Úc + nhân vật ghép bộ phận + một quái, được người dùng cho phép dựng trong `prototype/` để duyệt trước Giai đoạn 2; không phải mã game thật. Xem `02_asset_list.md`.
- Ngoại lệ A0 không mở khóa code game thật; quy tắc **không code trước Mốc A** giữ nguyên cho game thật.

### Điều kiện qua A0

- [x] Người dùng trực tiếp chơi thử nguyên mẫu trên **điện thoại Android**.
- [x] Người dùng chốt độ phân giải, nhân vật 96 px, tốc độ chạy, độ cao/thời gian nhảy, va chạm/hitbox, camera và nhịp chém.
- [x] Cập nhật kết quả trong `docs/13_thong_so.md` từ **Tạm thời → Đã duyệt**, ghi nhật ký `docs/05_log.md`.
- [x] Sau A0 tiếp tục **Mốc A** đầy đủ, không coi A0 thay thế A.

Ghi nhận trên theo xác nhận trực tiếp của người dùng, không suy ra chỉ từ kiểm tra headless. Tiếp tục Mốc A đầy đủ; bố cục bản đồ/HUD mỹ thuật còn phải soát và duyệt riêng.

## Mốc A1 — Mở đầu + Hồi 1 + toàn bộ hệ thống lõi; trước khi code game thật

### 1. Phong cách và nhân vật chính

<a id="a1-01"></a>

- [ ] Hệ thống ngoại hình (17_ngoai_hinh.md) đã duyệt.

<a id="a1-02"></a>

- [x] Xác nhận phong cách sau P0 và khối STYLE cuối cùng. *(Đã duyệt B ngày 28/10/2026; xem `docs/05_log.md`.)*

<a id="a1-03"></a>

- [x] Bảng màu 32 màu đã chốt và lưu thành file palette (`art/reference/palette.png` và `.gpl` hoặc `.ase`). *(Đã duyệt palette_v3; xem `docs/05_log.md`.)*

<a id="a1-04"></a>

- [ ] Ảnh gốc Đinh Bộ Lĩnh và bộ `chr_dbl_parts` (khớp, phần vẽ bù, lớp gần/xa) đã duyệt.

<a id="a1-05"></a>

- [ ] Bộ phận trang bị thay thế t1, t2 (áo/quần/vũ khí), cả Đao và Cung, dùng chung hệ khớp/dữ liệu động tác đã duyệt.

<a id="a1-06"></a>

- [ ] Dữ liệu ghép từng frame phái Đao và phái Cung ở bậc 1, đủ động tác trong `09_animation_spec.md`; khung đặc biệt bổ sung khi cần.

<a id="a1-07"></a>

- [ ] Bộ nhân vật chính ghép bộ phận đúng tỉ lệ 96 px, từng mảnh/khớp/frame được Claude/người dùng duyệt bằng script kiểm tra và bằng mắt; không yêu cầu thuê họa sĩ hoặc chỉnh tay.

### 2. Thế giới

<a id="a1-08"></a>

- [ ] Concept nhân vật đồng minh/NPC: Đinh Bộ Lĩnh lúc nhỏ và trưởng thành, Đàm thị, người chú, Đinh Điền, Nguyễn Bặc, Đinh Liễn, trẻ chăn trâu, thợ rèn Hoa Lư, thợ may, bà hàng cơm, ông lang, sư trụ trì, bô lão làng.

<a id="a1-09"></a>

- [ ] Concept quái: bù nhìn rơm, chuột đồng, rắn nước, cò đồng, chuột cống lớn, lợn rừng, nhím, cua đồng, lợn lòi nanh, khỉ đá, dơi hang, hổ con, hổ vằn, thổ phỉ, lính Hậu Ngô, lính cung Hậu Ngô, đội trưởng Hậu Ngô; hào trưởng quanh vùng (nhiệm vụ 13).

<a id="a1-10"></a>

- [ ] Concept boss: Tướng tiên phong Hậu Ngô, đúng màu cờ thế lực.

<a id="a1-11"></a>

- [ ] Cảnh nền và tileset: Làng Hoa Lư (`lang_hoa_lu`), Cánh đồng chiêm (`dong_chiem`), Bến đò Hoàng Long (`ben_do`), Núi đá Tràng An (`trang_an`), Đào Úc (`dao_uc`).

<a id="a1-12"></a>

- [ ] Concept Đinh Công Trứ (hồi tưởng/di vật), Trịnh Tú, lái buôn đường sông, quan thu lương và các NPC có tên trong bối cảnh nhưng chưa có nhiệm vụ xuất hiện đầu tiên — (Cần người dùng xác nhận).

<a id="a1-13"></a>

- [ ] Cảnh nền và tileset: ải Thần Phù (`ai_than_phu`), ải Đằng Châu (`ai_dang_chau`), ải Đỗ Động (`ai_do_dong`), ải Bạch Hạc (`ai_bach_hac`) — (Cần người dùng xác nhận); soát theo `08_map_layout.md` trước khi duyệt.

<a id="a1-14"></a>

- [ ] Concept quái giữ ải Thần Phù, Đằng Châu, Đỗ Động, Bạch Hạc: giặc núi, hải tặc, lính giáo, lính nỏ, kỵ binh, thủ lĩnh và tướng giặc của từng ải — (Cần người dùng xác nhận).

<a id="a1-15"></a>

- [ ] Chốt danh tính và concept năm bóng boss dùng lại ở Ảo cảnh Vạn Thắng — (Cần người dùng xác nhận); phần bố cục/tái sử dụng ở A5.

<a id="a1-16"></a>

- [ ] Xác định phạm vi cảnh Cổ Loa — (Cần người dùng xác nhận); chưa tự thêm vào danh sách bản đồ.

<a id="a1-17"></a>

- [ ] Trâu: concept và bản gắn trang bị phù hợp phạm vi hệ thống; thuyền chiến là hạng mục A2 theo quyết định, không tính thêm một thú cưỡi.

### 3. Bản đồ chơi được

<a id="a1-18"></a>

- [ ] File bố cục và ảnh dựng bằng script: Làng Hoa Lư (`lang_hoa_lu`), Cánh đồng chiêm (`dong_chiem`), Bến đò Hoàng Long (`ben_do`), Núi đá Tràng An (`trang_an`), Đào Úc (`dao_uc`); đã qua mục tự soát trong `08_map_layout.md`.

<a id="a1-19"></a>

- [ ] Đấu trường boss Tướng tiên phong Hậu Ngô có bố cục khớp cơ chế từng boss.

<a id="a1-20"></a>

- [ ] File bố cục và ảnh dựng bằng script: ải Thần Phù (`ai_than_phu`), ải Đằng Châu (`ai_dang_chau`), ải Đỗ Động (`ai_do_dong`), ải Bạch Hạc (`ai_bach_hac`) — (Cần người dùng xác nhận); soát theo `08_map_layout.md` trước khi duyệt.

<a id="a1-21"></a>

- [x] Số đo di chuyển đã chốt tại A0 (28/10/2026), xem `13_thong_so.md`. Việc soát mọi bố cục theo số mới còn thuộc các mục bố cục chưa duyệt bên trên; không tự đánh dấu 29 bản đồ đã hoàn tất.

<a id="a1-22"></a>

- [ ] Bản đồ vùng SCR-14: Hoa Lư, đánh dấu các điểm đi nhanh/điểm dịch chuyển đã mở trong phạm vi hồi.

### 4. Giao diện

<a id="a1-23"></a>

- [ ] Bố cục HUD đầy đủ (hiệu ứng, tên bản đồ, túi đồ, cửa hàng, Tự đánh, thú cưỡi) đã duyệt trên viewport 960 và 1200 px.

<a id="a1-24"></a>

- [ ] Bộ khung giao diện đã duyệt.

<a id="a1-25"></a>

- [ ] Mockup và đặc tả màn: SCR-01 Khởi động, SCR-02 Chọn ô (lưu game ba ô), SCR-03 Tải bản đồ, SCR-04 Chọn phái, SCR-05 HUD, SCR-06 Boss Hậu Ngô, SCR-08 Cài đặt, SCR-09a Hành trang/09b Trang bị/09c Kỹ năng/09d Tiềm năng/09e Thông tin/09f Trâu/09g Nhiệm vụ, SCR-10 Hội thoại, SCR-11 Cửa hàng NPC, SCR-12 Cường hóa/Luyện đá/Tách, SCR-13 thẻ ngân phiếu thưởng và Gói vĩnh viễn bản đầu, SCR-14 Hoa Lư, SCR-15 Thua trận, SCR-16 Phần thưởng, SCR-18 CS01–CS06, SCR-20 Xác nhận/thông báo.

<a id="a1-26"></a>

- [ ] SCR-21 Nhắc giờ chơi: thiết kế khung — (Cần người dùng xác nhận); cách xác định tuổi/giới hạn pháp lý vẫn chốt tại B. SCR-19 Đăng nhập Google chỉ thuộc C, không mockup ở bản đầu.

<a id="a1-27"></a>

- [ ] SCR-12 thẻ Chuyển hóa/Ấn truyền công — (Cần người dùng xác nhận); chưa có nhiệm vụ đầu tiên trong tài liệu.

<a id="a1-28"></a>

- [ ] Mockup trạng thái riêng bản đầu: SCR-13 thẻ Gói mất mạng/đang chờ Google Play/đã sở hữu; SCR-02 xóa ô; SCR-12 đang rèn/thành công/thất bại; trạng thái chung các màn A1.

<a id="a1-29"></a>

- [ ] Bộ biểu tượng đủ cho trang bị t1/t2, toàn bộ hai phái/kỹ năng, tiềm năng, vật liệu cường hóa/luyện đá/tách, thuốc/thức ăn, tiền tệ, túi đồ, món vĩnh viễn/thời trang bản đầu và trâu; dùng lại biểu tượng đã duyệt khi trùng hệ thống.

<a id="a1-30"></a>

- [ ] Font tiếng Việt đã chọn.

### 5. Luồng tương tác

<a id="a1-31"></a>

- [ ] Luồng F1 lần đầu mở game, F2 vòng chơi/lưu game, F3 cường hóa (nhánh bản đầu), F5 boss Hậu Ngô, F7 xóa ô chưa liên kết, F8 mất mạng (phần bản đầu), F9 nhánh ngân phiếu thưởng, F11 đi nhanh Hoa Lư, F13 mua/khôi phục món vĩnh viễn: đủ và qua tự soát.

<a id="a1-32"></a>

- [ ] Mỗi luồng của A1 có nhánh mất mạng đều giữ đúng nguyên tắc offline (không nhánh nào chặn gameplay); không đưa F4/F10/F12 hoặc nhánh ngân phiếu nạp vào bản đầu.

### 6. Hoạt ảnh và hiệu ứng

<a id="a1-33"></a>

- [ ] Đặc tả hoạt ảnh cho nhân vật/quái/boss đã nêu đích danh trong nhóm Thế giới của A1, gồm Trâu; dữ liệu nhân vật chính dùng chung theo hai phái, khớp `09_animation_spec.md`.

<a id="a1-34"></a>

- [ ] Concept hiệu ứng cơ bản và toàn bộ hai mươi chiêu hai phái: Trảm Đao, Đao Tâm, Song Trảm, Chấn Uy, Quét Ngang, Thiết Kỵ Xung Phong, Khai Sơn Trảm, Kiên Cường, Vạn Quân Trảm, Vạn Thắng; Xạ Tiễn, Tâm Nhãn, Phá Giáp Tiễn, Hộ Thân Khí, Song Tiễn, Liều Mạng Giương Cung, Thần Tiễn Xuyên Giáp, Ẩn Mình, Tam Tiễn Liên Châu, Vạn Tiễn; kể cả các chiêu chỉ dùng ở cấp/hồi sau.

<a id="a1-35"></a>

- [ ] Hoạt ảnh giao diện búa rèn, số sát thương, hồi chiêu, chuyển màn và tải đã duyệt.

### 7. Câu chuyện

<a id="a1-36"></a>

- [ ] Storyboard: CS01 Cờ lau tập trận, CS02 Mổ trâu khao quân, CS03 Cầu gãy/rồng vàng, CS04 Tụ nghĩa Đào Úc, CS05 Ngọn sào Đinh Liễn, CS06 Quân Ngô rút lui.

<a id="a1-37"></a>

- [ ] Bảng nhịp nhiệm vụ Hồi 1 và mở đầu đầy đủ, khớp nhiệm vụ trong GDD.

<a id="a1-38"></a>

- [ ] Tranh cutscene của Hồi 1 đã duyệt.

<a id="a1-39"></a>

- [ ] Lời thoại ít nhất cho mở đầu và Hồi 1.

### 8. Quy tắc nghiệp vụ

<a id="a1-40"></a>

- [ ] Chỉ số và giới hạn của thời trang đã chốt cùng cân bằng kinh tế.

<a id="a1-41"></a>

- [ ] Tự đặt lại và duyệt toàn bộ bảng số hệ thống lõi, không trùng nguồn tham khảo: hai phái và mọi chiêu, tiềm năng/công thức chiến đấu, đường kinh nghiệm cấp 1–60, trang bị, cường hóa +1…+16, luyện đá/tách, túi đồ, cửa hàng NPC, thời trang, ngân phiếu thưởng và cửa hàng món vĩnh viễn; kể cả mức dùng ở hồi sau.

<a id="a1-42"></a>

- [ ] Tự đặt lại và duyệt bảng số riêng nội dung Hồi 1 (quái/boss, nhiệm vụ/phần thưởng, rơi đồ và kinh tế vùng); khớp bảng hệ thống lõi đã chốt A1, không trùng nguồn tham khảo.

<a id="a1-43"></a>

- [ ] Quy tắc trong `12_ngan_phieu.md` cho bản đầu đã duyệt: mục 1 đến 4 (phần ngân phiếu thưởng), mục 10, mục 12.

### 9. Thông số và tài liệu nguồn

<a id="a1-44"></a>

- [ ] Kiến trúc co_lau_game (`15_kien_truc_game.md`) đã duyệt.

<a id="a1-45"></a>

- [ ] Quy ước id và phân loại logic trong `14_online_migration.md` đã duyệt; danh sách hạng mục và dữ liệu mẫu dùng đúng quy ước id.

<a id="a1-46"></a>

- [ ] Mọi thông số trong `13_thong_so.md` thuộc A1 ở trạng thái **Đã duyệt**, hoặc được người dùng chấp nhận giữ **Tạm thời** kèm điều kiện chốt; hệ thống lõi chốt đủ các mức ở A1.

<a id="a1-47"></a>

- [ ] `docs/GDD.md` khớp với `docs/06` đến `docs/14` cho mở đầu, Hồi 1 và toàn bộ hệ thống lõi; mọi chỗ mâu thuẫn đã sửa ở cả hai bên.

## Mốc A2 — Hồi 2

### 1. Phong cách và nhân vật chính

<a id="a2-01"></a>

- [ ] Bộ phận trang bị thay thế t3 (áo/quần/vũ khí), cả Đao và Cung, dùng chung hệ khớp/dữ liệu động tác đã duyệt.

### 2. Thế giới

<a id="a2-02"></a>

- [ ] Concept nhân vật đồng minh/NPC: Trần Lãm, thợ rèn Bố Hải, ông lang Bố Hải, lái buôn ngựa, ba tướng Trần Lãm và dân chài được hộ tống (chưa có tên riêng); Đinh Liễn dùng lại concept A1.

<a id="a2-03"></a>

- [ ] Concept quái: đỉa đầm, ếch cóc lớn, cá quả, cá sấu đầm, cua biển, rắn biển, hải tặc, hải tặc tinh anh, hải tặc cung thủ, cá mập con, thuyền trưởng hải tặc; thổ phỉ cung thủ, sói rừng, thủ lĩnh thổ phỉ trên đường rừng nhiệm vụ 27.

<a id="a2-04"></a>

- [ ] Concept boss: Thủ lĩnh hải tặc, đúng màu cờ thế lực.

<a id="a2-05"></a>

- [ ] Cảnh nền và tileset: Đầm lầy Đại Hoàng (`dam_dai_hoang`), Bố Hải Khẩu (`bo_hai_khau`), Bãi bồi cửa sông (`bai_boi`), Cửa biển (`cua_bien`), Đường rừng về Hoa Lư (`duong_rung`, dùng lần đầu ở nhiệm vụ 27).

<a id="a2-06"></a>

- [ ] Ngựa chiến; thuyền chiến theo nhiệm vụ 23: concept và bản gắn trang bị phù hợp phạm vi hệ thống; thuyền chiến là hạng mục A2 theo quyết định, không tính thêm một thú cưỡi.

### 3. Bản đồ chơi được

<a id="a2-07"></a>

- [ ] File bố cục và ảnh dựng bằng script: Đầm lầy Đại Hoàng (`dam_dai_hoang`), Bố Hải Khẩu (`bo_hai_khau`), Bãi bồi cửa sông (`bai_boi`), Cửa biển (`cua_bien`), Đường rừng về Hoa Lư (`duong_rung`, dùng lần đầu ở nhiệm vụ 27); đã qua mục tự soát trong `08_map_layout.md`.

<a id="a2-08"></a>

- [ ] Đấu trường boss Thủ lĩnh hải tặc có bố cục khớp cơ chế từng boss.

<a id="a2-09"></a>

- [ ] Bản đồ vùng SCR-14: ven biển và đường rừng nhiệm vụ 27, đánh dấu các điểm đi nhanh/điểm dịch chuyển đã mở trong phạm vi hồi.

### 4. Giao diện

<a id="a2-10"></a>

- [ ] Mockup và đặc tả màn: SCR-03/SCR-05/SCR-06/SCR-10/SCR-11/SCR-14/SCR-16/SCR-18 cho Hồi 2; SCR-09f ngựa/nuôi thú, HUD ngựa và thuyền chiến; SCR-12 Tách dùng lại thiết kế lõi A1.

<a id="a2-11"></a>

- [ ] Mockup riêng các trạng thái khác bố cục: ngựa/thuyền chiến và trạng thái màn Hồi 2.

<a id="a2-12"></a>

- [ ] Bộ biểu tượng đủ cho trang bị t3, vật phẩm nhiệm vụ Hồi 2, đồ nuôi/trang bị ngựa, thuyền chiến; dùng lại biểu tượng đã duyệt khi trùng hệ thống.

### 5. Luồng tương tác

<a id="a2-13"></a>

- [ ] Phần theo hồi của các luồng F2 hộ tống/giao thư, F5 hải tặc, F11 ven biển; F1/F2 phần mở ngựa/thuyền đã qua tự soát; dùng lại khung luồng đã duyệt.

<a id="a2-14"></a>

- [ ] Mỗi luồng của A2 có nhánh mất mạng đều giữ đúng nguyên tắc offline (không nhánh nào chặn gameplay); không đưa F4/F10/F12 hoặc nhánh ngân phiếu nạp vào bản đầu.

### 6. Hoạt ảnh và hiệu ứng

<a id="a2-15"></a>

- [ ] Đặc tả hoạt ảnh cho nhân vật/quái/boss đã nêu đích danh trong nhóm Thế giới của A2, gồm Ngựa chiến và thuyền chiến; dữ liệu nhân vật chính dùng chung theo hai phái, khớp `09_animation_spec.md`.

### 7. Câu chuyện

<a id="a2-16"></a>

- [ ] Storyboard: CS07 Ra mắt Trần Lãm, CS08 Nhận làm con nuôi, CS09 Thừa kế binh quyền (nhiệm vụ 27, kết Hồi 2).

<a id="a2-17"></a>

- [ ] Bảng nhịp nhiệm vụ Hồi 2 đầy đủ, khớp nhiệm vụ trong GDD.

### 8. Quy tắc nghiệp vụ

<a id="a2-18"></a>

- [ ] Tự đặt lại và duyệt toàn bộ bảng số của ngựa chiến/nuôi thú và thuyền chiến, kể cả mức dùng về sau; không trùng nguồn tham khảo.

<a id="a2-19"></a>

- [ ] Tự đặt lại và duyệt bảng số riêng nội dung Hồi 2 (quái/boss, nhiệm vụ/phần thưởng, rơi đồ và kinh tế vùng); khớp bảng hệ thống lõi đã chốt A1, không trùng nguồn tham khảo.

### 9. Thông số và tài liệu nguồn

<a id="a2-20"></a>

- [ ] Mọi thông số trong `13_thong_so.md` thuộc A2 ở trạng thái **Đã duyệt**, hoặc được người dùng chấp nhận giữ **Tạm thời** kèm điều kiện chốt; hệ thống lõi chốt đủ các mức ở A1.

<a id="a2-21"></a>

- [ ] GDD.md khớp với docs/06–docs/14 cho phần của hồi đó.

## Mốc A3 — Hồi 3

### 1. Phong cách và nhân vật chính

<a id="a3-01"></a>

- [ ] Bộ phận trang bị thay thế t4 (áo/quần/vũ khí), cả Đao và Cung, dùng chung hệ khớp/dữ liệu động tác đã duyệt.

### 2. Thế giới

<a id="a3-02"></a>

- [ ] Concept nhân vật đồng minh/NPC: Lưu Cơ, Lê Hoàn, Phạm Bạch Hổ, Ngô Xương Xí và thân nhân nhà Ngô; Nguyễn Bặc, Đinh Điền, sư trụ trì dùng lại concept A1.

<a id="a3-03"></a>

- [ ] Concept quái: thủy binh, rắn nước lớn, cá trê khổng lồ, thủy binh tinh anh; lính hào trưởng, lính nỏ, chó săn, hào trưởng Bình Kiều; giặc núi, hải tặc, lính giáo, lính nỏ, kỵ binh, thủ lĩnh đợt giữa và tướng giặc giữ ải Tam Điệp.

<a id="a3-04"></a>

- [ ] Concept boss: Phạm Bạch Hổ (đấu danh dự), đúng màu cờ thế lực.

<a id="a3-05"></a>

- [ ] Cảnh nền và tileset: Sông Đằng Châu (`song_dang_chau`), Đất Bình Kiều (`binh_kieu`), ải Tam Điệp (`ai_tam_diep`).

### 3. Bản đồ chơi được

<a id="a3-06"></a>

- [ ] File bố cục và ảnh dựng bằng script: Sông Đằng Châu (`song_dang_chau`), Đất Bình Kiều (`binh_kieu`), ải Tam Điệp (`ai_tam_diep`); đã qua mục tự soát trong `08_map_layout.md`.

<a id="a3-07"></a>

- [ ] Đấu trường boss Phạm Bạch Hổ (đấu danh dự) có bố cục khớp cơ chế từng boss.

<a id="a3-08"></a>

- [ ] Bản đồ vùng SCR-14: sông nước phía đông nam, đánh dấu các điểm đi nhanh/điểm dịch chuyển đã mở trong phạm vi hồi.

### 4. Giao diện

<a id="a3-09"></a>

- [ ] Mockup và đặc tả màn: SCR-07 Giữ ải, SCR-17 Kết quả Giữ ải, SCR-22 Căn cứ Hoa Lư; SCR-12 Dịch chuyển/Tinh luyện; phần Hồi 3 của SCR-03/SCR-05/SCR-06/SCR-09/SCR-10/SCR-11/SCR-14/SCR-16/SCR-18.

<a id="a3-10"></a>

- [ ] Mockup riêng các trạng thái khác bố cục: SCR-07 giữa đợt, SCR-17 chấm sao, SCR-22 chưa xây/thiếu vật liệu/tối đa; Dịch chuyển/Tinh luyện.

<a id="a3-11"></a>

- [ ] Bộ biểu tượng đủ cho trang bị t4, Hồn thạch, quặng tinh, gỗ lim/đá xanh/ngói và công trình căn cứ/giữ ải; dùng lại biểu tượng đã duyệt khi trùng hệ thống.

### 5. Luồng tương tác

<a id="a3-12"></a>

- [ ] Phần theo hồi của các luồng F6 Giữ ải, F2 căn cứ, F3 phần Dịch chuyển/Tinh luyện, F5 Phạm Bạch Hổ, F11 sông nước đã qua tự soát; dùng lại khung luồng đã duyệt.

<a id="a3-13"></a>

- [ ] Mỗi luồng của A3 có nhánh mất mạng đều giữ đúng nguyên tắc offline (không nhánh nào chặn gameplay); không đưa F4/F10/F12 hoặc nhánh ngân phiếu nạp vào bản đầu.

### 6. Hoạt ảnh và hiệu ứng

<a id="a3-14"></a>

- [ ] Đặc tả hoạt ảnh cho nhân vật/quái/boss đã nêu đích danh trong nhóm Thế giới của A3, gồm tướng đi cùng giữ ải; dữ liệu nhân vật chính dùng chung theo hai phái, khớp `09_animation_spec.md`.

<a id="a3-15"></a>

- [ ] Hoạt ảnh giao diện sao kết quả Giữ ải và dựng công trình căn cứ đã duyệt.

### 7. Câu chuyện

<a id="a3-16"></a>

- [ ] Storyboard: CS10 Gặp Lê Hoàn, CS11 Phạm Bạch Hổ quy phục, CS12 Ngô Xương Xí quy phục, CS13 Bản đồ tám sứ quân.

<a id="a3-17"></a>

- [ ] Bảng nhịp nhiệm vụ Hồi 3 đầy đủ, khớp nhiệm vụ trong GDD.

### 8. Quy tắc nghiệp vụ

<a id="a3-18"></a>

- [ ] Tự đặt lại và duyệt toàn bộ bảng số của căn cứ Hoa Lư, giữ ải, Dịch chuyển trang bị và Tinh luyện, kể cả mức dùng về sau; không trùng nguồn tham khảo.

<a id="a3-19"></a>

- [ ] Tự đặt lại và duyệt bảng số riêng nội dung Hồi 3 (quái/boss, nhiệm vụ/phần thưởng, rơi đồ và kinh tế vùng); khớp bảng hệ thống lõi đã chốt A1, không trùng nguồn tham khảo.

<a id="a3-20"></a>

- [ ] Các con số căn cứ Hoa Lư (vật liệu mỗi cấp, mức tăng tướng, lương thảo, thức ăn thú) đã chốt cùng bản cân bằng kinh tế.

### 9. Thông số và tài liệu nguồn

<a id="a3-21"></a>

- [ ] Mọi thông số trong `13_thong_so.md` thuộc A3 ở trạng thái **Đã duyệt**, hoặc được người dùng chấp nhận giữ **Tạm thời** kèm điều kiện chốt; hệ thống lõi chốt đủ các mức ở A1.

<a id="a3-22"></a>

- [ ] GDD.md khớp với docs/06–docs/14 cho phần của hồi đó.

## Mốc A4 — Hồi 4

### 1. Phong cách và nhân vật chính

<a id="a4-01"></a>

- [ ] Bộ phận trang bị thay thế t5, t6 (áo/quần/vũ khí), cả Đao và Cung, dùng chung hệ khớp/dữ liệu động tác đã duyệt.

### 2. Thế giới

<a id="a4-02"></a>

- [ ] Concept nhân vật đồng minh/NPC: Ngô Nhật Khánh, sư trụ trì Siêu Loại, dân Siêu Loại; các sứ quân Đỗ Cảnh Thạc, Nguyễn Siêu, Lã Đường, Lý Khuê, Nguyễn Thủ Tiệp, Nguyễn Khoan, Kiều Công Hãn, Kiều Thuận có concept ở mục boss.

<a id="a4-03"></a>

- [ ] Concept quái: lính giáo, lính khiên, lính nỏ Đỗ Động, tướng giữ lũy; lính cung và thủy binh Tây Phù Liệt; lính bộ Tế Giang, lính khiên mây, chó chiến, đội trưởng Tế Giang; lính Siêu Loại, lính nỏ, kẻ cướp làng, võ sư Siêu Loại; kỵ binh, lính giáo dài, ngựa hoang, kỵ binh tinh anh; lính Tam Đái, đỉa trâu, cá sấu, cá sấu chúa; lính mai phục, lính nỏ rừng, gấu ngựa, voi rừng; thủy binh Hồi Hồ, lính giáo, lính cung, thủy tướng Hồi Hồ.

<a id="a4-04"></a>

- [ ] Concept boss: Đỗ Cảnh Thạc, Nguyễn Siêu, Lã Đường, Lý Khuê, Nguyễn Thủ Tiệp, Nguyễn Khoan, Kiều Công Hãn, Kiều Thuận, đúng màu cờ thế lực.

<a id="a4-05"></a>

- [ ] Cảnh nền và tileset: Đỗ Động Giang (`do_dong`), Tây Phù Liệt (`tay_phu_liet`), Tế Giang (`te_giang`), Siêu Loại (`sieu_loai`), Đồi Tiên Du (`tien_du`), Đường Lâm (`duong_lam`), Đầm lầy Tam Đái (`tam_dai`), Rừng đồi Phong Châu (`phong_chau`), Ngã ba Hồi Hồ (`hoi_ho`).

<a id="a4-06"></a>

- [ ] Voi chiến: concept và bản gắn trang bị phù hợp phạm vi hệ thống; thuyền chiến là hạng mục A2 theo quyết định, không tính thêm một thú cưỡi.

### 3. Bản đồ chơi được

<a id="a4-07"></a>

- [ ] File bố cục và ảnh dựng bằng script: Đỗ Động Giang (`do_dong`), Tây Phù Liệt (`tay_phu_liet`), Tế Giang (`te_giang`), Siêu Loại (`sieu_loai`), Đồi Tiên Du (`tien_du`), Đường Lâm (`duong_lam`), Đầm lầy Tam Đái (`tam_dai`), Rừng đồi Phong Châu (`phong_chau`), Ngã ba Hồi Hồ (`hoi_ho`); đã qua mục tự soát trong `08_map_layout.md`.

<a id="a4-08"></a>

- [ ] Đấu trường boss Đỗ Cảnh Thạc, Nguyễn Siêu, Lã Đường, Lý Khuê, Nguyễn Thủ Tiệp, Nguyễn Khoan, Kiều Công Hãn, Kiều Thuận có bố cục khớp cơ chế từng boss.

<a id="a4-09"></a>

- [ ] Bản đồ vùng SCR-14: trung tâm/Kinh Bắc và trung du tây bắc, đánh dấu các điểm đi nhanh/điểm dịch chuyển đã mở trong phạm vi hồi.

### 4. Giao diện

<a id="a4-10"></a>

- [ ] Mockup và đặc tả màn: SCR-09f voi chiến và HUD voi; phần Hồi 4 của SCR-03/SCR-05/SCR-06/SCR-10/SCR-11/SCR-14/SCR-16/SCR-18, các màn dùng lại theo hồi.

<a id="a4-11"></a>

- [ ] Mockup riêng các trạng thái khác bố cục: voi chiến và các trận boss Hồi 4.

<a id="a4-12"></a>

- [ ] Bộ biểu tượng đủ cho trang bị t5/t6, voi chiến và vật phẩm nhiệm vụ Hồi 4; dùng lại biểu tượng đã duyệt khi trùng hệ thống.

### 5. Luồng tương tác

<a id="a4-13"></a>

- [ ] Phần theo hồi của các luồng F2 nhiệm vụ Hồi 4, F5 tám sứ quân, F11 trung tâm/Kinh Bắc/trung du, thao tác voi trong F2 đã qua tự soát; dùng lại khung luồng đã duyệt.

<a id="a4-14"></a>

- [ ] Mỗi luồng của A4 có nhánh mất mạng đều giữ đúng nguyên tắc offline (không nhánh nào chặn gameplay); không đưa F4/F10/F12 hoặc nhánh ngân phiếu nạp vào bản đầu.

### 6. Hoạt ảnh và hiệu ứng

<a id="a4-15"></a>

- [ ] Đặc tả hoạt ảnh cho nhân vật/quái/boss đã nêu đích danh trong nhóm Thế giới của A4, gồm Voi chiến; dữ liệu nhân vật chính dùng chung theo hai phái, khớp `09_animation_spec.md`.

### 7. Câu chuyện

<a id="a4-16"></a>

- [ ] Storyboard: CS14 Đỗ Cảnh Thạc, CS15 Nguyễn Siêu, CS16 Lã Đường, CS17 Lý Khuê, CS18 Nguyễn Thủ Tiệp, CS19 Nguyễn Khoan, CS20 Kiều Công Hãn, CS21 Kiều Thuận; CS22 Nghị hòa Đường Lâm; CS23 Vạn Thắng Vương.

<a id="a4-17"></a>

- [ ] Bảng nhịp nhiệm vụ Hồi 4 đầy đủ, khớp nhiệm vụ trong GDD.

### 8. Quy tắc nghiệp vụ

<a id="a4-18"></a>

- [ ] Tự đặt lại và duyệt toàn bộ bảng số của voi chiến, kể cả mức dùng về sau; không trùng nguồn tham khảo.

<a id="a4-19"></a>

- [ ] Tự đặt lại và duyệt bảng số riêng nội dung Hồi 4 (quái/boss, nhiệm vụ/phần thưởng, rơi đồ và kinh tế vùng); khớp bảng hệ thống lõi đã chốt A1, không trùng nguồn tham khảo.

### 9. Thông số và tài liệu nguồn

<a id="a4-20"></a>

- [ ] Mọi thông số trong `13_thong_so.md` thuộc A4 ở trạng thái **Đã duyệt**, hoặc được người dùng chấp nhận giữ **Tạm thời** kèm điều kiện chốt; hệ thống lõi chốt đủ các mức ở A1.

<a id="a4-21"></a>

- [ ] GDD.md khớp với docs/06–docs/14 cho phần của hồi đó.

## Mốc A5 — Hồi 5 + epilogue

### 1. Phong cách và nhân vật chính

<a id="a5-01"></a>

- [ ] Bộ phận trang bị thay thế t7 (áo/quần/vũ khí), cả Đao và Cung, dùng chung hệ khớp/dữ liệu động tác đã duyệt.

### 2. Thế giới

<a id="a5-02"></a>

- [ ] Concept nhân vật đồng minh/NPC: Ngô Chân Lưu (sư Khuông Việt); dùng lại Bộ Lĩnh, Đàm thị, Đinh Điền, Nguyễn Bặc, Đinh Liễn, Lê Hoàn, Lưu Cơ và nhân vật dự lễ/epilogue theo storyboard.

<a id="a5-03"></a>

- [ ] Concept quái: tàn quân giáo, tàn quân nỏ, tàn quân tinh anh; bóng của năm boss trong Ảo cảnh Vạn Thắng (danh tính chưa nêu rõ trong GDD, được đưa về A1 để xác nhận).

<a id="a5-04"></a>

- [ ] Cảnh nền và tileset: Kinh thành Hoa Lư (`kinh_thanh`), Đường về kinh thành (`duong_ve_kinh`), Ảo cảnh Vạn Thắng (`ao_canh`).

### 3. Bản đồ chơi được

<a id="a5-05"></a>

- [ ] File bố cục và ảnh dựng bằng script: Kinh thành Hoa Lư (`kinh_thanh`), Đường về kinh thành (`duong_ve_kinh`), Ảo cảnh Vạn Thắng (`ao_canh`); đã qua mục tự soát trong `08_map_layout.md`.

<a id="a5-06"></a>

- [ ] Bản đồ vùng SCR-14: kinh thành/Ảo cảnh và các điểm đã mở của Hồi 5, đánh dấu các điểm đi nhanh/điểm dịch chuyển đã mở trong phạm vi hồi.

### 4. Giao diện

<a id="a5-07"></a>

- [ ] Mockup và đặc tả màn: SCR-03/SCR-05/SCR-06 cho bóng boss/SCR-09g nhật ký/SCR-10/SCR-14/SCR-16/SCR-18 cho Hồi 5, lễ lên ngôi và epilogue.

<a id="a5-08"></a>

- [ ] Mockup riêng các trạng thái khác bố cục: bóng boss, lễ lên ngôi/epilogue.

<a id="a5-09"></a>

- [ ] Bộ biểu tượng đủ cho trang bị t7 và vật phẩm nhiệm vụ Hồi 5/epilogue; dùng lại biểu tượng đã duyệt khi trùng hệ thống.

### 5. Luồng tương tác

<a id="a5-10"></a>

- [ ] Phần theo hồi của các luồng F2 kết thúc game, F5 bóng boss, F11 kinh thành, xem cutscene/epilogue trong F2 đã qua tự soát; dùng lại khung luồng đã duyệt.

<a id="a5-11"></a>

- [ ] Mỗi luồng của A5 có nhánh mất mạng đều giữ đúng nguyên tắc offline (không nhánh nào chặn gameplay); không đưa F4/F10/F12 hoặc nhánh ngân phiếu nạp vào bản đầu.

### 6. Hoạt ảnh và hiệu ứng

<a id="a5-12"></a>

- [ ] Đặc tả hoạt ảnh cho nhân vật/quái/boss đã nêu đích danh trong nhóm Thế giới của A5, gồm nhân vật lễ lên ngôi và epilogue; dữ liệu nhân vật chính dùng chung theo hai phái, khớp `09_animation_spec.md`.

### 7. Câu chuyện

<a id="a5-13"></a>

- [ ] Storyboard: CS24 Lễ lên ngôi, CS25 Epilogue 968–979.

<a id="a5-14"></a>

- [ ] Bảng nhịp nhiệm vụ Hồi 5 và epilogue đầy đủ, khớp nhiệm vụ trong GDD.

### 8. Quy tắc nghiệp vụ

<a id="a5-15"></a>

- [ ] Tự đặt lại và duyệt bảng số riêng nội dung Hồi 5 (quái/boss, nhiệm vụ/phần thưởng, rơi đồ và kinh tế vùng); khớp bảng hệ thống lõi đã chốt A1, không trùng nguồn tham khảo.

### 9. Thông số và tài liệu nguồn

<a id="a5-16"></a>

- [ ] Mọi thông số trong `13_thong_so.md` thuộc A5 ở trạng thái **Đã duyệt**, hoặc được người dùng chấp nhận giữ **Tạm thời** kèm điều kiện chốt; hệ thống lõi chốt đủ các mức ở A1.

<a id="a5-17"></a>

- [ ] GDD.md khớp với docs/06–docs/14 cho phần của hồi đó.

## Mốc B — Trước khi phát hành

- [ ] Đã qua A1–A5.

- [ ] Chọn phương án phát hành tại Việt Nam (doanh nghiệp / nhà phát hành / chưa mở bán) và có xác nhận của luật sư.

- [ ] Hồ sơ cung cấp dịch vụ trò chơi điện tử theo quy định hiện hành, có ý kiến luật sư (xếp loại bản đầu: game tải về có thanh toán qua Google Play, không có máy chủ riêng).
- [ ] Cách xác định tuổi và giới hạn giờ chơi cho người dưới 18 tuổi (SCR-21); nếu luật sư yêu cầu khác thiết kế hiện tại thì quay lại sửa và duyệt lại.
- [ ] Giá các món vĩnh viễn bán bằng tiền thật.
- [ ] Thanh toán Google Play cho món vĩnh viễn chạy thật: mua, xác nhận đơn, khôi phục, thanh toán đang chờ, hoàn tiền.
- [ ] Nhân vật chính: bộ phận và dữ liệu ghép được kiểm, sửa pixel bằng script và Claude/người dùng duyệt từng phần bằng mắt; hồ sơ nguồn/sửa/duyệt đầy đủ. 11 boss và logo được vẽ lại hoặc chỉnh tay đáng kể theo quy trình thành phẩm riêng.
- [ ] `docs/05_log.md` đầy đủ, lưu cùng các file trung gian.
- [ ] Điều khoản dùng thương mại của công cụ tạo ảnh và giấy phép font đã kiểm tra.
- [ ] Bảng "Rà soát bản quyền" ở Phần 2 GDD, mục 9 đã rà hết.
- [ ] Nhãn hiệu tên game đã tra cứu và đăng ký.

## Mốc C — Trước khi bật ngân phiếu nạp (bản online hoặc bản cập nhật có nạp)

- [ ] Mockup các trạng thái ngân phiếu nạp: offline có ngân phiếu nạp, giao dịch đang chờ xác nhận, số dư nạp âm, thẻ Nạp, SCR-19.
- [ ] Quy tắc ngân phiếu nạp trong `12_ngan_phieu.md` (mục 5 đến 9) duyệt lại cho phù hợp kiến trúc máy chủ lúc đó.
- [ ] Máy chủ xác minh, sổ giao dịch, phục hồi, hoàn tiền chạy thật; luồng F4, F9, F10, F12 đã kiểm.
- [ ] Hồ sơ pháp lý cho việc có máy chủ và tiền tệ ảo, có ý kiến luật sư.

## Ký duyệt

Khi qua mỗi mốc, người dùng ghi ở cuối file: ngày, phiên bản tài liệu và câu "Đã qua mốc A0", "Đã qua mốc A1", "Đã qua mốc A2", "Đã qua mốc A3", "Đã qua mốc A4", "Đã qua mốc A5" hoặc "Đã qua mốc B". Việc cho phép thực hiện A0 không có nghĩa A0 đã nghiệm thu.

28/10/2026 — Đã qua mốc A0. Thử trên Realme RMX3760 (Android, 1600×720), Godot 4.7.2, commit 7973729.
