# Thiết kế bản đồ chơi được

Ảnh cảnh nền và tileset (khuôn P9, P10) chỉ cho biết bản đồ trông thế nào. Tài liệu này quy định bản đồ **chơi** ra sao: kích thước, nền đất, bục nhảy, chỗ sinh quái, NPC, lối ra, bẫy, đấu trường boss. Mỗi bản đồ có một file bố cục `design/maps/lay_<tên>_v<số>.md` viết theo mẫu ở mục 3, và một ảnh PNG dựng từ file đó bằng script:

```
python tools/render_layout.py design/maps/lay_dao_uc_v1.md design/maps/lay_dao_uc_v1.png
```

Bố cục vẽ bằng lưới chữ thay vì tạo ảnh AI, vì cần đúng từng ô. Sau khi duyệt, lưới này là bản vẽ để dựng bản đồ thật trong Godot (TileMapLayer) mà không phải đoán.

> **Sau A0 (28/10/2026):** dùng số đo đã chốt từ commit `7973729`, xem `13_thong_so.md`. Viewport logic rộng 960–1200 px; mọi bố cục mẫu cũ vẫn cần soát lại theo khả năng di chuyển, camera và vùng nút đã đổi, chưa được tự duyệt.

## 1. Số đo di chuyển (chuẩn A0)

Người dùng đã nghiệm thu Kiểu cổ điển trên Realme RMX3760 (Android, 1600×720),
Godot 4.7.2, commit `7973729`. Số đo di chuyển được chốt tại A0; giới hạn **bố cục
an toàn** vẫn phải thử theo từng bục/khe, không coi trần vật lý là mức bố trí mặc định.

- **Ô lưới:** hiện dùng 32×32 px (kích thước tile còn Tạm thời). Viewport 960–1200 px logic thấy 30–37,5 ô ngang; cao 540 px, khoảng 17 ô.
- **Nhân vật:** cao 96 px, khung 128×128, hộp va chạm 24×88 px.
- **Chạy:** 200 px/s, nhận ngay khi bấm. Hãm STOP_TIME=0,08 s; quay đầu đứng TURN_TIME=0,05 s, khung đầu đổi mặt. Trên không đổi hướng ngay; vùng chéo dùng 160 px/s (0,8 lần).
- **Một cú nhảy:** JUMP_HEIGHT=96 px, TIME_TO_APEX=0,38 s, g=2×96/0,38²≈1329,64 px/s², JUMP_SPEED≈−505,26 px/s. Lên/xuống cùng trọng lực, không treo ở đỉnh. Vận tốc rơi chặn tại 2×|JUMP_SPEED|≈1010,53 px/s.
- **Độ cao leo tối đa bằng một nhảy:** trần lý thuyết 96 px (3 ô nếu tile 32 px). Mức bậc an toàn 2 ô cũ chưa tự đổi thành 3 ô được duyệt: cần thử khoảng ngang, mép bục, hitbox và biên an toàn. Bục cao đúng 96 px ở sát trần nhảy không bảo đảm đáp được.
- **Khinh công:** khi còn đi lên và vận tốc lên còn ≤30% |JUMP_SPEED|, nhả rồi bấm mới để bật thêm 0,7×JUMP_SPEED; tối đa một lần/cú nhảy. Phần cao thêm là (0,7×505,263)²/(2×1329,640)=**47,04 px**. Bấm gần đỉnh cho trần tổng gần **96+47,04=143,04 px** (4,47 ô); bấm ở đầu cửa sổ, độ cao trước bật là 96×(1−0,3²)=87,36 px nên tổng **134,4 px**. Đây là tính liên tục; khung mô phỏng, thời điểm bấm và va chạm làm độ cao thực thấp hơn trần. Chưa duyệt bậc 4 ô làm đường bắt buộc.
- **Tầm ngang một nhảy cùng cao độ:** 200×(2×0,38)=**152 px** (4,75 ô); giữ vùng chéo: 160×0,76=**121,6 px** (3,8 ô), chưa tính khinh công. Khe 3 ô/96 px cũ chỉ còn đề xuất, không phải giới hạn đã duyệt. Với biên an toàn 1,5 lần bề rộng khe, nhảy chéo 121,6 px chưa đủ cho khe 96 px (cần 144 px); phải thử và giảm khe/thêm bục nếu dùng làm đường bắt buộc.
- **Đệm nhảy:** COYOTE_TIME=0,10 s; JUMP_BUFFER=0,12 s. Giữ để nhảy lại bật; giữ lâu nhảy cao tắt.
- **Camera:** DEAD_ZONE=(100,60) px là nửa rộng/nửa cao, LOOK_AHEAD=100 px, RESPONSE=5 /s; giới hạn theo viewport thật và biên bản đồ. Bản đồ nhiều tầng phải kiểm tra camera dọc riêng; A0 chỉ thử bản đồ cao một viewport.
- **Rơi và thú cưỡi:** quy tắc không mất máu khi rơi/nước sâu mất 10% HP, ngựa ×1,6, trâu ×1,2 nhảy 1,5 ô, voi không nhảy vẫn là thiết kế ngoài A0, cần kiểm tra và duyệt riêng.

### Vùng nhìn và vùng bị điều khiển che (từ A0)

- Thiết kế đồng thời cho viewport **960–1200 px logic**, không suy ra mọi điện thoại đều thấy đúng một số ô ngang.
- Chừa vùng đáy khoảng **140 px logic** dưới các cụm nút làm vùng bị che; không đặt hố hay bẫy ngay dưới cụm trái và cụm phải trong khung nhìn dự kiến. D-pad và vùng chéo phía trên còn cần kiểm tra vùng che thực tế, không coi 140 px là toàn bộ chiều cao cụm.
- Mặt đất chính nên cao hơn hàng nút, để thấy đường chân, mép vực và điểm đáp. Khi bố trí thế giới phải kiểm tra qua camera ở cả hai hướng chạy; không chỉ chừa vùng trên ảnh nền tĩnh.
- Rà quỹ đạo một nhảy và khinh công, cửa sổ thao tác, độ rộng bục và khả năng nhìn điểm đáp. Không tăng khe hoặc bậc hàng loạt chỉ từ công thức tối đa.

### Đường bắt buộc — bố cục Đào Úc 29/10/2026

Từ A0: nhảy chéo121,6 px, hướng riêng152 px, cao96 px. Với biên1,5 lần,
ngang an toàn ≤81,07 px (chéo) hoặc101,33 px (hướng riêng), bậc lên ≤64 px.
**Đường bắt buộc tới lối ra/đấu trường chỉ dùng khe ≤2 ô và bậc ≤2 ô (64 px)**,
qua bằng nhảy chéo, không cần khinh công. Vượt mức phải có bục phụ/dây leo L.
Không chỉ so hai trần riêng: phải kiểm quỹ đạo kết hợp ngang/cao, hitbox và điểm đáp.
Khinh công134,4–143,04 px chỉ cho lựa chọn/lối phụ/rương, không khóa tiến trình.

S/R lấy chân ở cạnh dưới ô, hitbox24×88. Tính vùng che theo A0 cho cả viewport960
và1200: cụm trái gồm hai vùng chéo vô hình, cụm phải và hàng5 kỹ năng. Chặn camera
ở cả biên trái/phải trước khi đổi ra tọa độ màn hình; không tái dùng spawn x100
cũ mà bỏ qua camera bị chặn. Mọi hố/chông/nước sâu phải kiểm mép khi đứng cách0–3
ô từ cả hai hướng. Mặt đất chính cao hơn hàng nút; chừa đáy140 px chỉ là mốc đầu,
không thay hộp che thật của d-pad cao hơn. Công cụ in nguồn số và miền camera,
không coi camera đã đứng yên là trường hợp duy nhất.

## 2. Kích thước và quy ước chung

- **Làng:** rộng 2 đến 3 màn (60 đến 90 ô), cao 12 ô, không có quái. NPC đứng cách nhau ít nhất 4 ô để chạm không nhầm.
- **Bản đồ đánh quái:** rộng 4 đến 6 màn (120 đến 180 ô), cao 12 đến 22 ô, có hai đến ba tầng bục. Mỗi màn hình (30 ô ngang) có ít nhất một vùng sinh quái, để người chơi không phải chạy xa mới thấy quái.
- **Đấu trường boss:** khu kín ở cuối bản đồ, rộng 1,5 đến 2 màn (45 đến 60 ô). Lối vào đóng lại khi trận bắt đầu.
- **Ải (giữ ải):** rộng 2 màn (60 ô), cờ lau ở giữa, 2 đến 3 cổng địch, 4 đến 6 ô dựng công trình.
- **Lối ra:** đặt ở mép trái hoặc phải, cao bằng mặt đất, có biển chỉ đường; đi vào là chuyển bản đồ, không cần bấm.
- **Điểm hồi sinh:** đầu mỗi bản đồ và trước mỗi đấu trường boss.
- **Không có lối cụt** không có lý do: lối cụt phải chứa rương hoặc vật phẩm nhiệm vụ.

Ký hiệu lưới:

| Ký tự | Nghĩa |
|---|---|
| `.` | Trống |
| `#` | Nền đất hoặc đá, đứng được, không đi xuyên |
| `=` | Bục, nhảy xuyên được từ dưới lên |
| `~` | Nước nông (đi được, chậm 30%) |
| `^` | Bẫy, chông, vùng gây sát thương |
| `L` | Dây leo hoặc thang |
| `S` | Điểm xuất hiện của người chơi |
| `R` | Điểm hồi sinh; chân ở giữa cạnh dưới ô, như S |
| `E` | Lối ra sang bản đồ khác |
| `N` | NPC |
| `m` / `M` | Vùng sinh quái thường / tinh anh hoặc thủ lĩnh |
| `B` | Boss |
| `F` | Cờ lau (giữ ải) |
| `T` | Ô dựng công trình (giữ ải) |
| `G` | Cổng địch xuất hiện (giữ ải) |
| `c` | Rương hoặc vật phẩm nhiệm vụ |
| `D` | Cổng gỗ, cửa lũy (phá được hoặc mở theo nhiệm vụ) |

## 3. Mẫu file bố cục

Mỗi file `lay_<tên>_v<số>.md` gồm:

1. **Thông tin chung:** tên bản đồ, cấp quái, nhiệm vụ diễn ra ở đây, kích thước (ô), cảnh nền dùng (mã `map_<tên>_bg`).
2. **Lưới bố cục** trong khối mã có nhãn `layout` (để script đọc được).
3. **Chú thích từng điểm:** mỗi `N`, `m`, `M`, `B`, `c`, `D`, `E` là gì, ví dụ "m tại cột 14: 3 thổ phỉ, hồi sinh sau 20 giây".
4. **Nhịp chơi:** người chơi đi từ đâu tới đâu, gặp gì trước, chỗ nào nghỉ, chỗ nào khó.
5. **Kiểm tra số đo:** hai bảng chép nguyên từ `tools/check_layout.py`: khe/bậc đường bắt buộc và vùng nút ở960/1200. Khe/bậc bắt buộc ≤64 px, có biên1,5× và quỹ đạo chéo kết hợp; không cần khinh công. Quỹ đạo thường/chéo/khinh công do công thức A0 tính, không vẽ tay; khinh công không là điều kiện tiến trình.
6. **Câu hỏi còn mở.**

## 4. Ví dụ: Đào Úc (giai đoạn 1, A1)

Bản cũ100 ô đã thay bằng hai file **đang làm, chưa duyệt**:

- [Đào Úc cấp10–15, 150×17 ô](../design/maps/lay_dao_uc_v1.md): NV9/CS04 tụ nghĩa,
  sân Đinh Điền/Nguyễn Bặc, bãi thổ phỉ, khe/chông64 px, nước nông, ba cổng D và ba
  điểm quân G cho NV14/CS05; E phải nối E trái đấu trường. NV13 chưa rõ địa điểm,
  ghi câu hỏi, không tự đặt ba hào trưởng ở đây.
- [Đấu trường Tướng tiên phong Hậu Ngô, 60×17 ô](../design/maps/lay_dao_uc_boss_v1.md):
  NV15, hai pha theo GDD, bốn vị trí lính cung trên lũy, đường bậc32 px tiếp cận,
  sân phẳng640 px, R trước cửa đóng khi vào trận, E sau thắng/CS06.

Mặt đất chính y288 px để không bị cụm nút che khi camera chạm biên. Hai file có
đủ lưới, chú thích, nhịp chơi, bảng kiểm bằng script và câu hỏi còn mở. Kích thước
map quái/boss ở mục2 khác bảng tạm `13_thong_so.md`: dùng mục2 theo yêu cầu,
không sửa13 và không coi kích thước mới đã được duyệt.

Chạy kiểm và dựng sơ đồ/lớp phủ, áp tương tự cho file boss:

```bash
python3 tools/check_layout.py design/maps/lay_dao_uc_v1.md --write-tables
python3 tools/check_layout.py design/maps/lay_dao_uc_v1.md
python3 tools/render_layout.py design/maps/lay_dao_uc_v1.md design/maps/lay_dao_uc_v1.png --trajectories
python3 tools/render_layout.py design/maps/lay_dao_uc_v1.md design/maps/lay_dao_uc_v1_overlay_960.png --overlay 960 --trajectories
python3 tools/render_layout.py design/maps/lay_dao_uc_v1.md design/maps/lay_dao_uc_v1_overlay_1200.png --overlay 1200 --trajectories
```

`--write-tables` chỉ thay hai vùng đánh dấu metrics/hud trong file được chỉ định;
không sửa nhật ký hay dữ liệu A0. Vạch màn đổi thành30 ô/960 và37,5 ô/1200.
Lớp phủ gồm snapshot viewport thật tại mỗi S/R, hitbox, vùng chết và hộp nút;
quỹ đạo mẫu màu tím không phải yêu cầu dùng khinh công. Test tĩnh không thay chơi thử.

## 5. Ví dụ: ải Tam Điệp (giai đoạn 3)

Cấp 30. Rộng 40 ô, cao 12 ô. Cờ lau (`F`) ở giữa, người chơi xuất hiện cạnh cờ. Địch vào từ ba cổng: mép trái, chân vách đá bên phải, và đỉnh vách đá. Năm ô dựng công trình (`T`): ba ở mặt đất, một trên bục trái để đặt chòi nỏ bắn xuống, một trên vách đá để chặn cổng trên cao.

```layout
........................................
........................................
........................................
........................................
........................................
..................................T...G.
..........T.............=====.##########
........======................##########
..............................##########
G.....T.....T.....SF....T....G##########
########################################
########################################
```

## 6. Danh sách bản đồ cần bố cục

Mỗi dòng: mã, kích thước đề xuất, điểm đặc biệt của bố cục. Điểm đặc biệt lấy từ cơ chế nhiệm vụ và boss trong GDD, nên bố cục phải phục vụ đúng cơ chế đó.

**Vùng Hoa Lư (giai đoạn 2):**

- `lay_lang_hoa_lu` — 50×12. Làng, không quái. NPC: thợ rèn, bà hàng cơm, ông lang, thợ may, sư trụ trì, mẹ Đàm thị; bãi bù nhìn rơm để tập (nhiệm vụ 1); chuồng trâu (nhiệm vụ 2).
- `lay_dong_chiem` — 80×12. Đồng phẳng, bờ ruộng thấp, ruộng nước nông. Cấp 1–5. Có bờ sông và cây cầu gãy cho cảnh chạy trốn người chú (nhiệm vụ 3).
- `lay_ben_do` — 80×14. Bến đò Hoàng Long, bãi sậy, cọc buộc thuyền. Cấp 4–8.
- `lay_trang_an` — 100×22. Núi đá vôi nhiều tầng, cửa hang, dây leo. Cấp 7–12. Bản đồ đầu tiên dạy leo nhiều tầng.
- `lay_dao_uc` — đã có ví dụ ở mục 4.

**Vùng ven biển (giai đoạn 3):**

- `lay_dam_dai_hoang` — 100×12. Đầm lầy, nhiều nước nông, khúc gỗ nổi làm bục. Hộ tống đoàn người (nhiệm vụ 16) nên đường phải liền, không có khe.
- `lay_bo_hai_khau` — 60×12. Làng, bến thuyền, nhà Trần Lãm.
- `lay_bai_boi` — 90×12. Bãi bồi, có 3 điểm dân chài bị lạc (nhiệm vụ 21).
- `lay_cua_bien` — 100×14. Bờ biển và boong thuyền. Có khu đánh trên thuyền (nhiệm vụ 23) và đấu trường boong thuyền cho thủ lĩnh hải tặc.

**Vùng sông nước Hồi 3 (giai đoạn 3):**

- `lay_duong_rung` — 100×16. Rừng, ba điểm phục kích (nhiệm vụ 27).
- `lay_song_dang_chau` — 100×14. Sông, cửa cống (nhiệm vụ 30), đấu trường thuyền cho Phạm Bạch Hổ có cọc nhọn trồi lên theo hàng.
- `lay_binh_kieu` — 90×14. Thành đất có ba hướng tấn công để giữ thành (nhiệm vụ 34).
- `lay_ai_tam_diep` — đã có ví dụ ở mục 5.

**Hồi 4 và Hồi 5 (giai đoạn 4):**

- `lay_do_dong` — 120×14. Ba lớp lũy nối tiếp, mỗi lớp là một pha boss; ba kho tên để đốt (nhiệm vụ 38).
- `lay_tay_phu_liet` — 110×14. Hai bờ sông nối bằng cầu hoặc thuyền; boss rút sang bờ kia ở 60% máu.
- `lay_te_giang` — 100×12. Bãi bồi rộng, phẳng, chỗ cho 10 lính vây boss (chiến thuật biển người).
- `lay_sieu_loai` — 90×12. Ngõ làng hẹp, nhiều tường; dân thường đứng rải rác (nhiệm vụ 44, 45).
- `lay_tien_du` — 120×12. Đồi thấp, rộng, ít bục, đủ chỗ cho kỵ binh phi ngang sân.
- `lay_duong_lam` — 60×12. Làng, ba điểm thử thách của Ngô Nhật Khánh.
- `lay_tam_dai` — 100×12. Đầm lún, năm lối tre ngầm an toàn (nhiệm vụ 49), đấu trường có sàn lún dần.
- `lay_phong_chau` — 110×18. Rừng đồi nhiều tầng, bốn ổ mai phục (nhiệm vụ 51), đấu trường đủ rộng cho voi chiến xông thẳng.
- `lay_hoi_ho` — 120×14. Ba bến thuyền nối nhau, mỗi bến một pha boss; mép bến có nước sâu (sóng đẩy người chơi xuống nước).
- `lay_kinh_thanh` — 60×12. Kinh thành Hoa Lư, thay làng Hoa Lư từ Hồi 5.
- `lay_duong_ve_kinh` — 100×14. Bản đồ đánh quái cuối cùng.
- `lay_ao_canh` — 5 đấu trường nhỏ 30×12 nối nhau, mỗi đấu trường một bóng boss.
- `lay_ai_than_phu`, `lay_ai_dang_chau`, `lay_ai_do_dong`, `lay_ai_bach_hac` — 40×12 mỗi ải, theo khuôn ải Tam Điệp nhưng đổi hướng cổng và địa hình theo vùng.

## 7. Tự soát bố cục

- Chạy `python3 tools/check_layout.py FILE`: tự tìm khe/bậc đường bắt buộc, kiểm ≤64 px và biên1,5×, quỹ đạo chéo có AABB24×88 ở cả hai hướng. Không dùng khinh công cứu đường chính; vượt mức phải thiết kế bục/L. Script thoát khác0 khi FAIL, nguyên nguồn ở `tools/check_layout.py`.
- Soát bảng vùng nút ở viewport960/1200: S/R không chạm hộp che, mép hố/bẫy thấy được khi tiến từ hai phía ở0–3 ô trước mép; xét dead-zone/look-ahead, miền làm mượt và chặn camera ở hai mép map. Đất chính trên hàng nút, không chỉ chừa140 px trên ảnh tĩnh.
- Mỗi màn hình có ít nhất một vùng sinh quái (trừ làng).
- Mọi vật phẩm nhiệm vụ và NPC trong nhiệm vụ của bản đồ đều có vị trí trên lưới.
- Đấu trường boss đủ chỗ cho mọi cơ chế của boss đó (Phần 4 GDD, mục 3).
- Lối ra khớp với bản đồ kế bên trong cùng vùng.
