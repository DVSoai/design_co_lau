# Hiệu ứng chiêu phái Kiếm v1

**09/11/2026 · Đề xuất để duyệt.** Tám chiêu theo bảng GDD đã chốt ngày 09/11 trên nhánh tham chiếu `art/dbl-bo-tu-the-gon` tại `9456f69`. Cấp mở, mục tiêu và tác dụng theo GDD. Thời lượng dưới đây là nhịp hình đề xuất, độc lập với hồi chiêu và thời lượng trạng thái. Kiếm Tâm 15 và Kiên Cường 45 thuộc phạm vi icon nội tại.

## Quy ước ghép và nhịp

- Lấy H là chiều cao đứng của Đinh Bộ Lĩnh v2 (~1340 px ở ảnh nguồn, ~130 px khi chơi), lấy chân làm gốc. Hướng chuẩn sang phải. Tên pose PNG dưới đây thuộc `art/concept/characters/chr_dbl_v2/kiem/` tại nhánh tham chiếu. Hình gốc `art/approved/characters/chr_dbl_v2_goc_kiem.png` cũng lấy từ nhánh đó. Các ảnh này chưa nằm trên main `5226eeb`; tên pose mới chỉ là chỉ dẫn cho đợt vẽ sau.
- Mỗi pose là một hình toàn thân cầm sẵn kiếm theo quyết định 09/11. Khi ghép khung nền #00FF00, đặt vệt sau mặt và thân, đầu vệt tới đúng mũi kiếm ở khung vung; vệt đi theo đường mũi kiếm giữa các pose. Giữ kiếm và vệt cách mép 40 px nếu dựng khung 1600×1600; giữ tỉ lệ H, mở rộng khung nếu cần. Điểm trúng bám mục tiêu, bụi bám mặt đất tại điểm va chạm. Lật gương cả chuỗi và các neo khi quay trái.
- Vẽ khối đặc, viền rõ, 2–3 mảng màu, tan bằng cách giảm diện tích, tách mảng và đổi sang sắc tối. Tránh quầng sáng mờ, hạt vụn, rồng, biểu tượng ngoại lai. Mẫu duyệt riêng trên đen #000000. Khi dựng game dùng lớp alpha thường cho bụi, đá, lau và lõi màu đặc; bản nền đen chỉ để duyệt.
- Ba thời lượng ngăn bằng dấu / lần lượt là xuất hiện / mạnh nhất / tan. Pose lấy đà tính riêng khi ghi rõ. Mốc trúng hình ảnh bắt đầu ở nhịp mạnh nhất tương ứng; chỉ phát hiệu ứng trúng đích khi game xác nhận. Tia trúng chuẩn dùng chung 2 khung 35/45 ms, rộng 0,16H, hai mảng sắc nhọn tại điểm va chạm. Số khung trong bảng gồm dải hiệu ứng riêng của chiêu; tia dùng chung ghi riêng.

## Đặc tả tám chiêu

### 10 · Trảm Kiếm
- Pose `chem_1.png` lấy đà 55 ms, `chem_2.png` vung, `chem_3.png` kết thúc. Dùng `fx_tram_kiem_a.png`, `fx_tram_kiem.png`, `fx_tram_kiem_c.png` để định hình.
- Lưỡi liềm đứng trắng #F7FBFF viền xanh #A6E2FF, rộng 0,45H × cao 0,53H. Từ mũi kiếm phía sau vai vòng lên rồi xuống tới mũi kiếm trước thân. Khung 1 nét mảnh nửa trên, khung 2 lõi trắng dày ở đầu, khung 3 tách hai đoạn.
- 3 khung 40/55/65 ms. Trúng một mục tiêu phát tia trắng xanh. Không có hiệu ứng đất.

### 20 · Song Trảm
- Dùng `chem_1.png` lấy đà 45 ms rồi `chem_2.png` cho nhát xuống. Hai pose mới `song_tram_hoi_kiem.png` thu kiếm thấp sát hông và `song_tram_vung_nguoc.png` vung ngược lên qua sườn. Giữ tư thế thứ hai qua nhịp tan.
- Hai cung chéo cắt nhau ở phía trước ngực, không hợp thành biểu tượng X cố định. Nhát 1 trắng xanh bạc, nhát 2 thêm cạnh vàng rơm nhạt; rộng 0,45H và 0,58H, cao khoảng 0,50H. Dấu nhát đầu thu nhỏ trước khi nhát sau lên rõ.
- 6 khung, nhát đầu 30/40/35 ms, nhát sau 30/45/55 ms. Mỗi nhát có tia trúng riêng khi được xác nhận. Không có hiệu ứng đất.

### 25 · Chấn Uy
- Pose mới `chan_uy_ha_tan.png`, hạ trọng tâm, khuỷu gần ép sát, hạ mũi kiếm trước chân nhưng không chạm đất. Giữ pose qua nhịp phát sóng.
- Sóng ép thấp như hai đường đồng tâm trên mặt trống đồng Việt, góc nhìn bầu dục dẹt. Màu đồng nhạt #D9B25F và kem #F4F1E8, mỗi vành chỉ có vài răng tam giác lớn. Tâm ở chân, mặt và thân vẫn rõ. Mở rộng 0,60H → 1,55H → 1,70H, cao tối đa 0,24H; cuối nhịp còn vài cung rời. Đây là cách điệu cho game.
- 3 khung 55/75/95 ms. Mục tiêu bị khóa tấn công có hai cung đồng ngắn tại chân, 2 khung 50/70 ms. Không bụi hay đá, vòng đất chính là sóng khống chế. Dấu ngắn chỉ báo lúc áp trạng thái.

### 30 · Quét Ngang
- `quet_1.png` lấy đà 55 ms, `quet_2.png` giữ nhịp vung và hồi. Tham khảo `fx_quet_ngang_a.png`, `fx_quet_ngang.png`, `fx_quet_ngang_c.png`.
- Vòng vàng nhạt #FFE39A, lõi kem. Bầu dục rộng 0,82H × cao 0,22H ở ngang hông. Cung sau nằm sau thân; cung trước chạy qua phía dưới tay và gặp mũi kiếm lúc vung. Vành trước hiện trước, vòng đủ tại đỉnh, tan bằng 3 cung rời. Cung sau dùng vàng tối phẳng.
- 3 khung 40/55/60 ms. Tia vàng ở từng mục tiêu được xác nhận, tối đa ba theo GDD. Không bụi đất.

### 35 · Thiết Kỵ Xung Phong
- Dùng `chay_1.png` nén bước 45 ms và `chay_3.png` cho đoạn lao. Pose mới `xung_phong_ham_kiem.png` hãm chân trước, đưa mũi kiếm thấp ra trước ở điểm đến. Chiêu minh họa động tác lao bộ; không yêu cầu thú cưỡi.
- Hai dải gió sắc trắng ngà và vàng rơm, neo sau hông và gót, rộng 0,35H → 1,20H → 0,55H, cao tối đa 0,20H. Mũi kiếm dẫn hướng, dải thu về điểm hãm. Hình theo khoảng lướt đã đi, không báo tầm xa hơn logic.
- 3 khung 35/70/55 ms. Tia trúng trắng vàng ở điểm đến khi kiếm gặp mục tiêu. Bụi hãm ochre rộng 0,32H, neo gót ở mặt đất, 2 khung 35/60 ms.

### 40 · Khai Sơn Trảm
- Dùng `van_quan_1.png` nâng kiếm 100 ms, rồi pose mới `khai_son_ghim_dat.png`: bổ một nhát nặng, hạ gối trước, mũi kiếm dừng sát chân mục tiêu. Giữ pose qua nhịp hồi.
- Nêm chém trắng ngà #FFF4D6 viền đồng #DBA94A, góc dốc khoảng 60°, dài 0,85H. Vệt bám lưỡi từ trên vai xuống; đỉnh dồn mảng sáng quanh đầu nêm rồi co thành một mảnh chéo. Phân biệt với Vạn Quân bằng chấn điểm hẹp và nét đá góc cạnh.
- 3 khung 45/60/75 ms. Tia trúng chung; nếu có choáng, thêm hai nét đá/vàng lệch trên mục tiêu 2 khung 45/70 ms. Khi chạm đất, khe đá vôi ngắn và hai mảng đá lớn sát điểm chạm rộng 0,42H, 3 khung 30/50/80 ms. Trên không bỏ lớp khe đá.

### 50 · Vạn Quân Trảm
- `van_quan_1.png` lấy đà 85 ms, `van_quan_2.png` bổ xuống chéo phải và hồi. Dùng `fx_van_quan_chem.png` và `fx_van_quan_bui.png` để đối chiếu hình khối.
- Vệt bổ cam vàng #F59729, lõi trắng #FFF5DA, dài 0,75H–1,05H theo đường mũi kiếm. Mảng lõi mở rộng khi hạ, rồi ngắn lại thành hai mảng sắc. Bụi nâu vàng và vài mảnh đá văng hai bên ở đáy, rộng ~0,90H tại đỉnh, thấp dưới gối.
- Vệt 3 khung 40/60/65 ms; bụi 3 khung 35/65/90 ms bắt đầu ở nhịp mạnh của vệt nếu chạm đất. Tia cam nhạt ở từng mục tiêu trúng (tối đa bốn), dấu choáng dùng chung Khai Sơn nếu trạng thái được áp.

### 60 · Vạn Thắng
- Hai pose mới `van_thang_lay_da.png` ép gối và thu kiếm hai tay ngang vai 95 ms; `van_thang_mo_kiem.png` bước mở tấn và đưa kiếm chéo ngang ra trước. Dùng `chem_3.png` làm dáng hồi khi vệt đã qua.
- Mũi quét rộng đỏ son #B23A2E, lõi vàng #FFD16C với một cạnh kem, rộng tối đa 1,45H × cao 0,45H. Đỉnh gắn mũi kiếm và dẫn từ trái sang phải. Ba bông lau trắng #F4F1E8 có cuống lớn đi theo đuôi như cờ lau tập trận, lớp sau nhân vật, thấp hơn mắt. Không dùng cờ vải đỏ; màu đỏ chỉ thuộc vệt chém. Cờ lau xuất hiện khi mở kiếm, nghiêng theo đà rồi thu thành hai bông.
- Vệt 3 khung 45/70/80 ms; lau 3 khung 45/70/80 ms đồng bộ vệt. Tia đỏ vàng ở mục tiêu xác nhận (tối đa bốn), dấu choáng dùng chung nếu được áp. Không có bụi đất cho đòn quét tầm hông.

## Tóm tắt khung riêng cần sản xuất

| Cấp và chiêu | Pose mới | Khung hiệu ứng riêng |
|---|---:|---:|
| 10 Trảm Kiếm | 0 | 3 |
| 20 Song Trảm | 2 | 6 |
| 25 Chấn Uy | 1 | 5 (3 sóng + 2 dấu trúng) |
| 30 Quét Ngang | 0 | 3 |
| 35 Thiết Kỵ Xung Phong | 1 | 5 (3 gió + 2 bụi) |
| 40 Khai Sơn Trảm | 1 | 8 (3 vệt + 3 đất + 2 dấu choáng dùng chung) |
| 50 Vạn Quân Trảm | 0 | 6 (3 vệt + 3 bụi) |
| 60 Vạn Thắng | 2 | 6 (3 vệt + 3 lau) |
| **Tổng** | **7** | **42**, cộng **2** khung tia trúng dùng chung |

Bốn PNG `fx_*_v1.png` trong thư mục concept là mẫu nhịp mạnh để duyệt hình, chưa phải bộ 42 khung. Khi duyệt ở cỡ chơi, kiểm tra đường kiếm, vùng che mặt, tương phản với giáp đỏ và độ phân biệt giữa chấn đất hẹp của Khai Sơn, bụi ngang của Vạn Quân và đuôi lau của Vạn Thắng.

## Đối chiếu nhịp tham khảo

Đọc class từ bảng `skill` trong `nja.sql`, số nhịp mặt đất/trên không từ `nj_skill`, các ID hiệu ứng được gọi ở từng nhịp và số khung con từ `nj_effect` qua bộ đọc `tools/ref_render.py`. Các nhịp có thể nối đuôi hiệu ứng sau lúc gọi. Đòn ngắn như ID 1 gọi hiệu ứng ở nhịp 2–3, ID 5 gọi gần đầu trên đất và muộn hơn trên không, ID 9 chia hai đợt ở nhịp 3 và 7. Điều này gợi cách tách lấy đà, điểm vung và phần tan, và cho hai nhát Song Trảm có khoảng ngắt. Không quy đổi số nhịp nguồn thành mili giây của game này.

Bản đọc class 1 bên dưới. Số trong ngoặc là số khung con của hiệu ứng; dấu gạch là nhịp không gọi hiệu ứng trong ba ô được đọc.

```text
1 Chiêu Hiyoko
  ground=6 1:- 2:16(5) 3:39(2) 4:- 5:- 6:-
  air=6 1:- 2:16(5) 3:39(2) 4:- 5:- 6:-
2 Chiêu Amagedon
  ground=0
  air=0
3 Chiêu Jizokuzan
  ground=15 1:- 2:6(15) 3:39(2) 4:- 5:- 6:- 7:- 8:- 9:40(2),40(2) 10:- 11:- 12:- 13:- 14:40(2),40(2) 15:-
  air=11 1:- 2:6(15) 3:39(2) 4:- 5:- 6:- 7:- 8:- 9:40(2),40(2) 10:- 11:-
4 Chiêu Kakyuu
  ground=12 1:64(7) 2:- 3:- 4:- 5:- 6:- 7:- 8:- 9:- 10:- 11:- 12:-
  air=10 1:64(7) 2:- 3:- 4:- 5:- 6:- 7:- 8:- 9:- 10:-
5 Chiêu X Zangeki
  ground=8 1:- 2:53(3) 3:11(4),46(4) 4:- 5:- 6:- 7:- 8:-
  air=10 1:- 2:17(4) 3:- 4:- 5:- 6:- 7:11(4),46(4) 8:- 9:- 10:-
6 Chiêu Raikou
  ground=9 1:57(7) 2:- 3:- 4:- 5:- 6:- 7:- 8:- 9:-
  air=9 1:57(7) 2:- 3:- 4:- 5:- 6:- 7:- 8:- 9:-
7 Chiêu Hihebun
  ground=23 1:3(4) 2:- 3:- 4:- 5:18(2) 6:- 7:- 8:9(1) 9:9(1) 10:12(5) 11:- 12:20(2) 13:- 14:20(2),33(4) 15:- 16:12(5) 17:- 18:20(2) 19:- 20:20(2),33(4) 21:- 22:- 23:-
  air=14 1:33(4) 2:- 3:- 4:- 5:18(2) 6:- 7:20(2) 8:32(4),18(2) 9:- 10:20(2) 11:33(4) 12:20(2) 13:- 14:-
8 Chiêu Shuurai
  ground=0
  air=0
9 Chiêu Choukouhirenzo
  ground=10 1:- 2:17(4) 3:45(4),45(4) 4:- 5:- 6:- 7:45(4),45(4) 8:- 9:- 10:-
  air=10 1:- 2:17(4) 3:45(4),45(4) 4:- 5:- 6:- 7:45(4),45(4) 8:- 9:- 10:-
55 Chiêu Pawaraikou
  ground=0
  air=0
61 Chiêu Maajizangeki
  ground=10 1:- 2:12(5) 3:- 4:94(5) 5:35(2) 6:- 7:35(2),35(2) 8:- 9:96(2),35(2),35(2) 10:-
  air=11 1:94(5) 2:- 3:- 4:- 5:- 6:- 7:- 8:35(2),35(2),35(2) 9:- 10:96(2) 11:-
67 Nhẫn thuật Kage Bunshin
  ground=9 1:- 2:- 3:- 4:- 5:142(6) 6:- 7:- 8:- 9:-
  air=0
73 Chiêu Ikkakujuu
  ground=14 1:- 2:16(5) 3:108(7),123(12) 4:- 5:- 6:- 7:32(4) 8:- 9:- 10:- 11:- 12:- 13:- 14:-
  air=0
79 Chiêu Enko Bakusatsu
  ground=14 1:154(4) 2:- 3:- 4:- 5:16(5) 6:159(4) 7:160(8) 8:- 9:- 10:16(5),155(4) 11:- 12:- 13:- 14:-
  air=0

```
