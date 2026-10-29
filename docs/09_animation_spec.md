# Đặc tả hoạt ảnh

Tài liệu này quy định mỗi nhân vật, quái, boss, hiệu ứng và giao diện cần những động tác nào, bao nhiêu khung, chạy nhanh bao nhiêu, có lặp không, và khung nào gây sát thương. Bảng động tác tạo bằng khuôn P4 phải đủ các động tác ở đây. Số khung là đề xuất; khi dựng dữ liệu ghép và sửa pixel bằng script có thể thêm hoặc bớt một hai khung, miễn giữ đúng **khung gây sát thương** và **tổng thời gian**, vì hai thứ đó gắn với hồi chiêu và cảm giác đánh.

## Quy ước

- **Tốc độ chuẩn:** 12 khung mỗi giây (mỗi khung khoảng 83 mili giây). Đòn thường và chiêu có hồi chiêu từ 1 giây trở lên dùng 15 khung mỗi giây.
- **Chiêu bấm liên tục** (hồi chiêu dưới 1 giây, như Trảm Đao 0,4 giây hay Song Tiễn 0,55 giây) chạy 18 khung mỗi giây, và số khung tối đa bằng hồi chiêu nhân 18 (0,4 giây → 7 khung; 0,45 → 8; 0,5 và 0,55 → 9). Như vậy động tác luôn xong trước khi chiêu hồi xong, người chơi bấm liên tục không bị khựng. Phần hoành tráng của chiêu (cờ lau, mưa tên) làm bằng hiệu ứng chạy song song, không kéo dài động tác.
- **Khung sprite:** theo kích thước trong art bible (nhân vật cao 96 px trong khung 128×128, chân cách đáy khung 8 điểm ảnh; boss người cao ~132 px trong khung 192×192 (tạm thời)).
- **Sự kiện trong động tác** ghi bằng số khung, đếm từ 1:
  - `hit` — khung bắt đầu gây sát thương (hộp đánh bật lên).
  - `spawn` — khung bắn ra mũi tên hay hiệu ứng.
  - `cancel` — từ khung này có thể bấm động tác khác để ngắt.
  - `sfx` — khung phát âm thanh.
- **Hướng:** chỉ vẽ hướng phải; hướng trái lật ngang trong game. Vì vậy vũ khí không được có chi tiết chỉ đúng một phía (ví dụ chữ khắc).
- **Bộ phận và frame:** `chr_dbl_parts` gồm đầu kèm tóc, thân, cánh tay trên/dưới gần/xa, đùi/cẳng chân gần/xa, bàn tay và vũ khí; từng mảnh có khớp và phần vẽ bù. `chr_dbl_anim_*` ghi vị trí/góc/thứ tự lớp, thời lượng và sự kiện theo từng frame. Trang bị `chr_dbl_t1`…`t7` chỉ thay áo/quần/vũ khí cùng khớp, không vẽ lại chuỗi động tác.

## Đinh Bộ Lĩnh — động tác chung

| Động tác | Khung | Tốc độ | Lặp | Sự kiện |
|---|---|---|---|---|
| Đứng thở | 4 | 6 | Có | — |
| Chạy | 6 | 12 | Có | sfx bước chân khung 2, 5 |
| Nhảy lên | 2 (đề xuất) | theo quỹ đạo A0, lên đỉnh 0,38 s | Không | chuyển vào lộn tại cửa sổ vận tốc 30% |
| Lộn người ở đỉnh / khinh công | Chưa chốt số khung | tổng 0,20 s/vòng | Không | một vòng 360° theo hướng mặt; không xoay hitbox |
| Quay đầu | Chưa chốt số khung | tổng 0,05 s | Không | khung đầu đổi mặt; đứng trong TURN_TIME rồi chạy |
| Rơi | 2 | 12 | Có | — |
| Chạm đất | 2 | 12 | Không | sfx khung 1, bụi đất |
| Trúng đòn | 2 | 12 | Không | — |
| Bị choáng | 4 | 8 | Có | sao choáng trên đầu |
| Ngã xuống | 4 | 10 | Không | — |
| Đứng dậy | 3 | 10 | Không | — |
| Nói chuyện (trong hội thoại) | 2 | 4 | Có | — |
| Cưỡi thú, ngồi yên | 2 | 4 | Có | — |
| Cưỡi thú, đánh thường | 4 | 12 | Không | hit 3 |
| Lên cấp | 6 | 12 | Không | cột sáng |
| Mừng (nhận thưởng, thắng boss) | 4 | 8 | Không | — |

### Nhịp di chuyển và lộn người đã chốt từ A0

**Đã duyệt (A0, 28/10/2026)** về nhịp/thao tác tại commit `7973729`,
Godot 4.7.2, Realme RMX3760. Nhảy cao 96 px, lên đỉnh 0,38 s, cùng trọng lực
khi lên/xuống và không chèn khung treo đỉnh. Khinh công cần lần bấm mới khi còn
đi lên trong cửa sổ ≤30% |JUMP_SPEED|, bật thêm 0,7 lần, tối đa một lần/cú nhảy.

- Mọi cú nhảy và cú khinh công cần **khung lộn người ở đỉnh**, một vòng 360° theo hướng mặt trong APEX_FLIP_TIME=0,20 s. Dựng pose ghép bộ phận theo từng khung, thay xoay nguyên sprite tạm của A0; lộn đỉnh/chiêu lớn được vẽ thêm khung riêng nếu cần để đọc rõ. Giữ đúng tỉ lệ và điểm khớp của mọi mảnh. Không xoay body hoặc hitbox theo hình.
- Bắt đầu lộn khi vận tốc lên vào cửa sổ 30%; vòng của khinh công vẫn phải đủ một vòng. Nếu hai vòng tới sát nhau, xếp vòng sau sau vòng trước như mẫu A0. Kiểm tra kết thúc trước khi đáp đất trên quỹ đạo cùng cao độ; kiểm tra đáp lên bậc/va trần riêng, không chèn thời gian giữ nhân vật trên không để đủ khung.
- Quay đầu bám TURN_TIME=0,05 s: khung logic đầu chỉ đổi hướng mặt, giữ vị trí rồi mới chạy; chạm nhẹ chỉ quay mặt. Không kéo dài nhịp quay theo số khung ở tốc độ 12 fps. Chạy đạt 200 px/s ngay khi bấm, buông hãm trong STOP_TIME=0,08 s.
- Số khung nghệ thuật, chia thời lượng từng khung và bộ sprite thành phẩm còn phải dựng/duyệt ở Mốc A1. Tổng thời gian A0 đã chốt thắng tốc độ 12/15 fps đề xuất nếu hai thứ không khớp.
- Chém cơ bản: 0,30 s, cửa sổ trúng 0,10–0,20 s, hồi thêm 0,15 s sau động tác. Bảng combo bên dưới là đề xuất ngoài phạm vi nghiệm thu A0; khi dựng nhát cơ bản phải chia timeline để khớp nhịp này, không dùng số khung cũ để đổi thời điểm hit.
- Vệt chém/hiệu ứng trúng đòn và số sát thương luôn ở lớp vẽ trên nhân vật, hình nộm và quái; lộn người không thay đổi thứ tự lớp hoặc hộp đánh.

### Bản thử rig greybox Giai đoạn 1 (chưa duyệt)

`16_rig_nhan_vat.md` và `prototype/rig/data/animations.json` dựng thử các động tác
chung/Đao/Cung bằng khối màu. Đề xuất **6 pose lộn trong 0,20 s**, khóa kết thúc 360°,
và **2 pose quay đầu trong 0,05 s**; hai tổng thời gian giữ A0, số pose chưa được duyệt.
Chém cơ bản 4 pose chia 0,10/0,10/0,05/0,05 s để giữ cửa sổ trúng A0; combo 2–3
và bắn thường theo bảng bên dưới chỉ xem, chưa thêm cơ chế mới vào A0.
Không thay bảng số khung thành phẩm hay đánh dấu các mục này Đã duyệt vì có greybox.

## Phái Đao

Đòn thường là chuỗi ba nhát; bấm tiếp trong khung `cancel` thì sang nhát sau.

| Động tác | Khung | Tốc độ | Sự kiện |
|---|---|---|---|
| Đánh thường nhát 1 | 4 | 15 | hit 2, cancel 3 |
| Đánh thường nhát 2 | 4 | 15 | hit 2, cancel 3 |
| Đánh thường nhát 3 (mạnh, đẩy lùi) | 5 | 15 | hit 3, cancel 5 |

Mười chiêu (tên và số liệu ở Phần 2 GDD, mục 3). Chiêu nội tại không có động tác riêng, chỉ có hiệu ứng khi kích hoạt.

| Chiêu | Kiểu động tác | Khung | Sự kiện |
|---|---|---|---|
| Trảm Đao | Chém ngang một nhát | 5 | hit 3 |
| Đao Tâm (nội tại) | Không có động tác | — | Hiệu ứng ánh đao lướt quanh người khi vào trận |
| Song Trảm | Hai nhát chéo liên tiếp | 7 | hit 3, hit 5 |
| Chấn Uy | Dậm đất, sóng chấn quanh người | 6 | hit 4 |
| Quét Ngang | Xoay người quét vòng | 7 | hit 3 đến 5 |
| Thiết Kỵ Xung Phong | Lướt tới 220 điểm ảnh, đâm | 6 | hit 2 đến 5 (trong lúc lướt) |
| Khai Sơn Trảm | Nhảy lên, bổ dọc xuống | 9 | hit 7, rung màn |
| Kiên Cường (nội tại) | Không có động tác | — | Viền sáng quanh người khi thoát khống chế |
| Vạn Quân Trảm | Ba nhát quét liên hoàn | 7 | hit 2, 4, 6 |
| Vạn Thắng (tuyệt kỹ) | Chém một nhát dài; hiệu ứng cờ lau hiện sau lưng chạy song song | 7 | hit 5, rung màn nhẹ |

## Phái Cung

| Động tác | Khung | Tốc độ | Sự kiện |
|---|---|---|---|
| Bắn thường | 5 | 15 | spawn 4, cancel 5 |
| Bắn khi chạy | 6 | 12 | spawn 3, lặp cùng nhịp chân |

| Chiêu | Kiểu động tác | Khung | Sự kiện |
|---|---|---|---|
| Xạ Tiễn | Bắn một mũi nhanh | 5 | spawn 4 |
| Tâm Nhãn (nội tại) | Không có động tác | — | Mắt lóe sáng khi chí mạng |
| Phá Giáp Tiễn | Kéo căng, bắn mũi nặng | 7 | spawn 6 |
| Hộ Thân Khí (hỗ trợ) | Hít sâu, khí bao quanh người | 5 | Vòng khí kéo dài 90 giây |
| Song Tiễn | Bắn hai mũi tỏa | 6 | spawn 5 (hai mũi) |
| Liều Mạng Giương Cung (hỗ trợ) | Gồng người, viền đỏ | 5 | Viền đỏ kéo dài 5 giây |
| Thần Tiễn Xuyên Giáp | Quỳ một gối, bắn mũi xuyên | 9 | spawn 8, vệt sáng thẳng |
| Ẩn Mình (nội tại) | Không có động tác | — | Người mờ đi một nhịp khi thoát khống chế |
| Tam Tiễn Liên Châu | Bắn ba mũi liền | 7 | spawn 3, 5, 7 |
| Vạn Tiễn (tuyệt kỹ) | Bắn lên trời; mưa tên rơi xuống vùng trước mặt là hiệu ứng riêng | 8 | spawn 5, mưa tên rơi sau 0,2 giây |

## Quái

Mỗi quái thường có năm động tác. Quái được chia theo kiểu để dùng chung nhịp.

| Động tác | Khung | Tốc độ | Lặp |
|---|---|---|---|
| Đứng | 4 | 6 | Có |
| Đi | 6 | 10 | Có |
| Tấn công | 4 đến 6 | 12 | Không |
| Trúng đòn | 2 | 12 | Không |
| Chết | 4 | 10 | Không |

- **Cận chiến người** (thổ phỉ, lính giáo, lính khiên): tấn công 5 khung, hit khung 4; khung 1 đến 3 là động tác báo trước để người chơi kịp né.
- **Tầm xa người** (lính cung, lính nỏ): tấn công 6 khung, spawn khung 5.
- **Thú nhỏ** (chuột, rắn, cò): tấn công 4 khung, hit khung 3.
- **Thú lớn** (hổ, cá sấu, gấu, voi): thêm động tác vồ hoặc húc 7 khung, hit khung 6, có 2 khung báo trước rõ rệt.
- **Kỵ binh:** đi và tấn công trên ngựa; thêm động tác ngã ngựa 5 khung khi chết.
- **Tinh anh và thủ lĩnh:** dùng chung bảng động tác với quái cùng loại nhưng sprite lớn hơn 25% và có thêm một đòn riêng 6 khung.

## Boss

Mỗi boss có các động tác của quái người, cộng:

| Động tác | Khung | Ghi chú |
|---|---|---|
| Ra mắt | 6 đến 8 | Chạy khi trận bắt đầu, có thể kèm cutscene ngắn |
| Báo đòn đặc biệt | 4 | Lặp trong 0,8 đến 1,2 giây, đồng bộ với vòng đỏ trên mặt đất |
| Đòn đặc biệt | 8 đến 10 | Theo cơ chế từng boss (Phần 4 GDD, mục 3) |
| Chuyển pha | 6 | Gầm, rút lui hoặc đổi vị trí; boss không nhận sát thương |
| Quy phục (Phạm Bạch Hổ) | 6 | Hạ vũ khí, chắp tay; thay cho động tác chết |
| Thua (các boss bị đánh dẹp) | 6 | Quỳ xuống, không có máu me |

Boss cưỡi thú (Nguyễn Thủ Tiệp cưỡi ngựa, Kiều Công Hãn cưỡi voi ở pha 3) có bộ động tác riêng trên lưng thú.

## NPC

Đứng thở 4 khung, nói chuyện 2 khung. NPC giao nhiệm vụ có thêm động tác vẫy gọi 4 khung, chạy khi người chơi tới gần mà NPC có nhiệm vụ mới.

## Thú cưỡi

Đứng, đi, chạy, nhảy (ngựa, trâu), húc (trâu, voi). Mỗi động tác 4 đến 6 khung, chạy cùng nhịp với nhân vật ngồi trên lưng. Điểm neo chỗ ngồi phải ghi cho từng khung.

## Hiệu ứng

| Hiệu ứng | Khung | Tốc độ |
|---|---|---|
| Vệt chém | 5 | 15 |
| Tia lửa trúng đòn | 4 | 15 |
| Mũi tên bay | 1 | — |
| Mũi tên cắm | 3 | 12 |
| Sao choáng | 4 | 8, lặp |
| Dây ghim chân | 4 | 8, lặp |
| Bụi đất | 4 | 12 |
| Cột sáng lên cấp | 6 | 12 |
| Vòng đỏ báo đòn boss | 1 | Phóng to dần bằng code |
| Mưa tên (Vạn Tiễn, Đỗ Cảnh Thạc) | 6 | 12, lặp |
| Cọc nhọn trồi lên (Phạm Bạch Hổ) | 5 | 12 |
| Sóng nước (Kiều Thuận) | 8 | 12 |

## Giao diện

- **Búa rèn:** 3 nhịp gõ, mỗi nhịp 0,3 giây; thành công lóe vàng 6 khung và tiếng ngân dài; thất bại tóe lửa đỏ 5 khung và tiếng gãy cụt.
- **Số sát thương:** bay lên 24 điểm ảnh trong 0,6 giây rồi mờ dần; chí mạng to gấp 1,5 lần, màu vàng.
- **Hồi chiêu:** vòng quét tối theo chiều kim đồng hồ.
- **Sao kết quả giữ ải:** từng sao rơi xuống và nảy, cách nhau 0,3 giây.
- **Chuyển màn:** mờ đen 0,25 giây.
- **Dựng công trình căn cứ:** giàn tre dựng lên rồi công trình hiện ra, 8 khung, khoảng 1 giây; không có thời gian chờ xây.
- **Giao dịch ngân phiếu đang chờ:** biểu tượng bông lau xoay nhỏ cạnh món hàng, cùng biểu tượng tải chung.
- **Biểu tượng tải:** bông lau xoay, 8 khung, lặp.

## Tự soát

- Mỗi chiêu có đúng một khung `hit` hoặc `spawn` cho mỗi lần gây sát thương ghi trong số liệu chiêu.
- Mọi đòn của quái và boss có ít nhất 2 khung báo trước trước khung `hit`.
- Chiêu bấm liên tục không vượt số khung tối đa theo hồi chiêu (mục Quy ước); chiêu hồi dài không kéo quá 0,8 giây.
- Các bộ trang bị khớp khung với bảng động tác bậc 1.

## Hoạt ảnh thời trang

Vòng riêng 6–10 khung (Đề xuất) chạy song song rig: cape bay theo đứng/chạy/nhảy, vũ khí phản sáng kim loại. Không đổi hit/spawn/cancel hoặc kéo dài động tác. Mỗi món một dạng cố định; không biến thành bộ nhiều cấp. Khung, tốc độ và giao lớp cần duyệt Mốc A1; không dùng năng lượng phép thuật.
