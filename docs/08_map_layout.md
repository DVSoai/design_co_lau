# Thiết kế bản đồ chơi được

Ảnh cảnh nền và tileset (khuôn P9, P10) chỉ cho biết bản đồ trông thế nào. Tài liệu này quy định bản đồ **chơi** ra sao: kích thước, nền đất, bục nhảy, chỗ sinh quái, NPC, lối ra, bẫy, đấu trường boss. Mỗi bản đồ có một file bố cục `design/maps/lay_<tên>_v<số>.md` viết theo mẫu ở mục 3, và một ảnh PNG dựng từ file đó bằng script:

```
python tools/render_layout.py design/maps/lay_dao_uc_v1.md design/maps/lay_dao_uc_v1.png
```

Bố cục vẽ bằng lưới chữ thay vì tạo ảnh AI, vì cần đúng từng ô. Sau khi duyệt, lưới này là bản vẽ để dựng bản đồ thật trong Godot (TileMapLayer) mà không phải đoán.

> **Lưu ý đổi độ phân giải:** các số ô/màn được cập nhật theo viewport 960×540; bố cục map cũ, camera, hitbox và khoảng nhảy cần kiểm thử lại trước khi duyệt.

## 1. Số đo di chuyển (đề xuất, chỉnh khi chơi thử)

Bố cục phải khớp với khả năng di chuyển của nhân vật, nếu không sẽ có bục không nhảy tới được. Các con số dưới đây là đề xuất ban đầu; khi chơi thử bản mẫu mà đổi số thì phải soát lại mọi bố cục.

- **Ô lưới:** 32×32 điểm ảnh. Màn hình gốc 960×540 thấy được 30 ô ngang, khoảng 17 ô dọc.
- **Nhân vật:** hộp va chạm rộng 16, cao 44 điểm ảnh (**thông số cũ, phải thử lại khi nhân vật cao 96 px**) (khoảng nửa ô ngang, gần 1,5 ô dọc).
- **Chạy:** 112 điểm ảnh mỗi giây, tức 3,5 ô mỗi giây.
- **Nhảy:** cao tối đa 80 điểm ảnh (2,5 ô). Vì vậy **bậc cao nhất leo được là 2 ô**, chừa nửa ô cho dễ.
- **Nhảy xa khi chạy:** tối đa khoảng 4 ô. **Khe rộng nhất nên đặt là 3 ô.**
- **Rơi:** không mất máu khi rơi. Rơi xuống nước sâu thì về điểm đứng gần nhất và mất 10% HP.
- **Thú cưỡi:** ngựa chạy nhanh gấp 1,6 lần và nhảy như người; trâu nhanh gấp 1,2 lần, nhảy thấp 1,5 ô; voi chỉ ở trận Kiều Công Hãn, không nhảy.
- **Camera:** theo người chơi theo chiều ngang, vùng chết rộng 4 ô ở giữa màn; theo chiều dọc chỉ dịch khi người chơi đứng trên bục cao hơn 3 ô.

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
5. **Kiểm tra số đo:** liệt kê mọi bậc cao hơn 2 ô và mọi khe rộng hơn 3 ô (phải bằng 0, hoặc có dây leo hay bục phụ).
6. **Câu hỏi còn mở.**

## 4. Ví dụ: Đào Úc (giai đoạn 1)

Cấp 10 đến 15. Nơi diễn ra nhiệm vụ 9 (tụ nghĩa, đấu với Đinh Điền), 14 (giữ ba cổng trước ba đợt quân Hậu Ngô) và 15 (đánh tướng tiên phong Hậu Ngô). Rộng 100 ô (5 màn), cao 14 ô.

```layout
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
....................................................................................................
.................................................................c..................................
................................................................====................................
....................====............=====..................................................m..B..m..
.............c............................................................................==========
............=====.....................m.................======..........................############
.................................#########..................D.........D.........D...===.############
ES.N..........m...m.....m...m.###############.m.........m.m.D.....m...D...m..M..D.......############
##############################################^^##~~~###############################################
####################################################################################################
```

Nhịp chơi: người chơi vào từ trái (`E`, `S`), gặp Nguyễn Bặc (`N`) ngay đầu bản đồ. Màn 1 và 2 là đất trống với thổ phỉ, có bục cao giữ rương. Màn 3 có gò đất và một hố chông nhỏ (`^`) dạy người chơi nhảy qua chướng ngại, rồi bãi nước nông. Màn 4 là trại có ba cổng gỗ (`D`), nơi diễn ra trận giữ ba cổng ở nhiệm vụ 14; đội trưởng Hậu Ngô (`M`) đứng trước cổng thứ ba. Màn 5 là lũy đất cao của tướng tiên phong (`B`) với lính cung đứng trên lũy, đúng cơ chế mưa tên ở pha 2 (Phần 4 GDD). Bậc thang `===` ở cột 84 giúp leo lên lũy cao 3 ô, vì nhảy chỉ được 2 ô.

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

- Chạy script, xem ảnh: không có bậc nào cao hơn 2 ô và khe nào rộng hơn 3 ô mà không có bục phụ hay dây leo.
- Mỗi màn hình có ít nhất một vùng sinh quái (trừ làng).
- Mọi vật phẩm nhiệm vụ và NPC trong nhiệm vụ của bản đồ đều có vị trí trên lưới.
- Đấu trường boss đủ chỗ cho mọi cơ chế của boss đó (Phần 4 GDD, mục 3).
- Lối ra khớp với bản đồ kế bên trong cùng vùng.
