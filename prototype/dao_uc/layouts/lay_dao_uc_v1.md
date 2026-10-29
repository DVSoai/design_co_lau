# lay_dao_uc_v1 — Trại Đào Úc, bản đồ đánh quái

**Tạm thời — đang làm, chưa duyệt (A1).** Ô 32 px; tọa độ cột/hàng bắt đầu từ 0.
Ký hiệu S/R/E/N/m/M/B/D/G/c đặt ở ô chứa chân: chân tại ((c+0,5)×32;(r+1)×32).
Không phải ảnh cảnh nền, không phải bản đồ đã chơi thử; không sửa prototype hay số A0.

## 1. Thông tin chung

- Vùng cấp10–15; **150×17 ô = 4800×544 px** (5 viewport960, 4 viewport1200).
- Nền `map_dao_uc_bg`, tile `map_dao_uc_tiles`: trại tre, lũy đất, chòi canh;
  chưa vẽ art mới. Đây là phân tách bản mẫu cũ thành bản đồ đánh quái và boss.
- NV9/CS04 tụ nghĩa và đấu Đinh Điền: địa điểm trại Đào Úc được xác nhận tại
  `10_storyboard.md` CS04. NV10 chọn phái và hỏi Nguyễn Bặc dùng lại vị trí NPC.
- NV14/CS05 giữ **3 cổng** trước **3 đợt quân Hậu Ngô**. NV15 chuyển qua đấu trường
  riêng. Nguồn: GDD Phần3 mục2, Phần4 mục2–3. NV11–13 xem câu hỏi mục6;
  không tự gán các mục tiêu chưa rõ địa điểm vào Đào Úc.
- E(c149,r8) nối **E(c0,r8) của `lay_dao_uc_boss_v1.md`** hai chiều trước trận.
  E(c0,r8) trở về tuyến Hoa Lư; bản đồ nối cụ thể chưa chốt.

## 2. Lưới bố cục

```layout-meta
{
  "kind": "field",
  "tile_px": 32,
  "mandatory_route": "lowest exposed support, c0..149; all gates traversable after quest conditions"
}
```

```layout
......................................................................................................................................................
......................................................................................................................................................
......................................................................................................................................................
......................................................................................................................................................
........................................................................................................c.m..L........................................
.......................................................................................................======L........................................
....................................c........................................................................L........................................
..................................======.................m....########..............................=========L........................................
E...........SR...N......N..M....m.....................########################m.~~~...^^..G...D.....m.......GL..D.....m.......G...D.....M....m....R..E
############################################..########################################################################################################
############################################..########################################################################################################
############################################..########################################################################################################
############################################..########################################################################################################
############################################..########################################################################################################
############################################..########################################################################################################
############################################..########################################################################################################
############################################..########################################################################################################
```

## 3. Chú thích từng điểm

- S(c12,r8), R(c13,r8): xuất hiện (400;288), hồi sinh đầu trại (432;288).
  R(c146,r8): hồi sinh trước lối sang boss (4688;288); boss còn có R riêng trước cửa khóa.
- N(c17,r8): Nguyễn Bặc, giao/trả các NV9–11/13–15; ba câu hỏi NV9, chọn phái NV10.
  N(c24,r8): Đinh Điền; M(c27,r8) là điểm đấu tay đôi NV9, chỉ kích hoạt khi nhận nhiệm vụ,
  không phải quái thường, không tự đặt máu/số lần sinh. Sân tập c20…31.
- m(c32,r8), m(c57,r7), m(c78,r8): thổ phỉ, các bãi tập chiến đấu theo bảng quái Đào Úc.
- m(c100,r8), m(c118,r8), m(c141,r8): lính giáo Hậu Ngô theo tiến độ NV14–15.
  m(c106,r4): lính cung Hậu Ngô trên bục trại. M(c136,r8): đội trưởng Hậu Ngô.
  Số lượng/hồi sinh chưa được GDD chốt; không tự thêm số cân bằng.
- D(c94,r8), D(c112,r8), D(c130,r8): Cổng1/2/3 NV14, không phải giữ ải A3.
  G(c90,r8), G(c108,r8), G(c126,r8): điểm vào của quân Hậu Ngô cho ba mặt trận;
  nơi phát sinh từng đợt phải được duyệt trong kịch bản NV14, không tự đặt quân số.
  D(c112,r8) cũng là mốc kích hoạt/dàn cảnh CS05 (ngọn sào Đinh Liễn);
  vị trí sào và nhân vật trong shot theo `10_storyboard.md`, không thêm NPC chiến đấu.
- Khe c44–45: rộng64 px, không có sàn dưới, rơi thì dùng quy tắc hồi sinh đã thiết kế.
  Chông ^(c86–87,r8): 64×32 px, phải nhảy. Nước ~(c80–82,r8) có đáy ngay hàng9,
  chỉ **nông**, đi chậm30%, không phải nước sâu/mất máu. Không có nước sâu ở bản này.
- c(c36,r6): rương nghỉ sau sân tập, bục y224. c(c104,r4): rương lối phụ y160,
  lên bục y224 rồi y160 hoặc leo L(c109,r4…8). Không bắt khinh công để lấy rương;
  nếu thử khinh công chỉ ở nhánh phụ này, không bỏ biên an toàn đường chính.
- Các bục =(c34…39,r7), =(c100…108,r7), =(c103…108,r5) là lớp phụ;
  mặt đất chính lên dần32 px tại c54/c62, xuống32 px tại c70/c78.
- E(c0,r8) và E(c149,r8): như kết nối mục1, đặt cùng cao độ mặt đất.

## 4. Nhịp chơi

1. c0…31: vào trại, thấy Nguyễn Bặc, sân đấu Đinh Điền; có chỗ nghỉ/đọc hội thoại
   trước khi tăng áp lực. Không sinh lính địch giữa sân NPC ở pha tụ nghĩa.
2. c32…79: bãi thổ phỉ → nhánh rương → khe64 px trên nền bằng → gò đất bậc32 px.
   Giới thiệu khe không kèm địch ở mép ngay lần đầu; bãi kế tiếp có chỗ hạ xuống an toàn.
3. c80…89: nước nông cho nhịp chậm, rồi chông64 px; chưa ghép chông với bậc/khe cao.
4. c90…135: ba cổng liên tiếp, điểm gọi quân rõ trên lưới; NV14 tăng áp lực qua ba đợt,
   giữa các đợt có hội thoại/cutscene theo kịch bản, không tự đặt thời gian nghỉ.
5. c136…149: đội trưởng rồi bãi lính cuối; hồi sinh an toàn và E sang boss.
   Mỗi đoạn30 cột có điểm m/M; con số quân thật vẫn chờ cân bằng.

## 5. Kiểm tra số đo

Sơ đồ từ lưới thật: [lay_dao_uc_v1.png](lay_dao_uc_v1.png),
[lớp phủ960](lay_dao_uc_v1_overlay_960.png),
[lớp phủ1200](lay_dao_uc_v1_overlay_1200.png).
Ảnh là sơ đồ PIL, không imagegen; không thay bản chơi thử.

### Nguồn số và mô hình camera/nút

- `prototype/config/tuning.gd`: RUN_SPEED=200; JUMP_HEIGHT=96; TIME_TO_APEX=0,38;
  PLAYER_BOX=24×88; CAMERA_DEAD_ZONE=(100,60) là **nửa** rộng/cao;
  CAMERA_LOOK_AHEAD=100; CAMERA_RESPONSE=5 /s. g=2H/t²; JUMP_SPEED=−2H/t.
  Nguồn thiết kế: `docs/13_thong_so.md`, `docs/08_map_layout.md` mục 1.
- `prototype/scripts/touch_controls.gd::layout` + tuning.gd: d=84, lề=24,
  gap=12, right=2,2d, up=1,35d, vùng chéo=0,9d; CHÉM=1,4d;
  bình/đổi mục tiêu=0,65d; 5 kỹ năng=0,7d, cách6. Nguồn HUD:
  `docs/06_screens.md`, mục HUD trong trận. Dưới đây là hộp bao cả cụm,
  gồm vùng chéo vô hình và khoảng trống giữa nút, kiểm bảo thủ hơn hình tròn.
- Tính lại từ nguồn bằng `tools/check_layout.py`, không nhập tay bảng kết quả.
  Camera bắt đầu ở điểm S/R, nhìn phải; kiểm cả nhìn trái và biên dead-zone;
  miền ngang tính thêm lag v/response=40 px rồi chặn [W/2;world_width−W/2].
  Miền dọc dùng **mọi vị trí camera hợp lệ**, kể cả đang làm mượt/reset:
  map cao544 → cy∈[270;274]. Vì vậy mặt đất y288 hiện ở y284…288,
  trên vùng chéo cao nhất y318,6 và trên hàng nút đáy khoảng140 px.
- Kiểm hitbox S/R, mép hố/bẫy từ cả hai hướng ở cách0/1/2/3 ô tính từ mép
  hitbox; không chỉ kiểm camera đã ổn định. Hai mép bản đồ được kiểm riêng.
  Không giả định spawn x100 của A0 cũ là an toàn: S mới ở x400.
  Khi chuyển map/hồi sinh, thiết kế yêu cầu reset camera về điểm S/R đã chặn
  trước khi nhận điều khiển; không khẳng định một camera còn ở map cũ sẽ thấy điểm mới.
- Đường bắt buộc là mặt đứng thấp nhất có đủ khoảng trống đầu mỗi cột,
  không chọn bục một chiều phía trên thay đất. Cửa nhiệm vụ được kiểm khi mở;
  script không xác nhận logic khóa/mở hoặc địch. Khe/bậc tự tìm từ lưới,
  không nhập danh sách vượt chướng ngại thủ công. Quỹ đạo 240 mẫu/s kiểm
  AABB24×88, đất/chông và bục một chiều khi rơi; chưa là mô phỏng Godot.
- Khe/bậc bắt buộc ≤64 px; soát 1,5× ngang/cao và quỹ đạo kết hợp cả hai chiều.
  Không tính coyote/khinh công để cứu đường bắt buộc. Hướng riêng152 px,
  chéo121,6 px; biên ngang chính xác121,6/1,5=81,07 px, nhưng lưới chỉ dùng64.
  Bậc96/1,5=64 px. Khinh công cho trần134,4–143,04 px; chỉ là lựa chọn/lối phụ,
  không làm điều kiện tiến trình. Các nét quỹ đạo là mẫu tính liên tục, không là
  bằng chứng người dùng đã chơi được.

<!-- BEGIN metrics -->
| Loại | Vị trí (c/r từ 0) | ngang/cao px | Cách qua bắt buộc | tầm/1,5; cao/1,5 px | Kết quả |
|---|---|---|---|---|---|
| gap | c44..46, r9→r9 | 64/0 | nhảy chéo, không khinh công | 81.07/64.00 | PASS (quỹ đạo +24×88 hai hướng) |
| step | c54..54, r9→r8 | 0/32 | nhảy chéo, không khinh công | 81.07/64.00 | PASS (quỹ đạo +24×88 hai hướng) |
| step | c62..62, r8→r7 | 0/32 | nhảy chéo, không khinh công | 81.07/64.00 | PASS (quỹ đạo +24×88 hai hướng) |
| step | c70..70, r7→r8 | 0/32 | nhảy chéo, không khinh công | 81.07/64.00 | PASS (quỹ đạo +24×88 hai hướng) |
| step | c78..78, r8→r9 | 0/32 | nhảy chéo, không khinh công | 81.07/64.00 | PASS (quỹ đạo +24×88 hai hướng) |
| trap | c86..88, r9→r9 | 64/32 | nhảy chéo, không khinh công | 81.07/64.00 | PASS (quỹ đạo +24×88 hai hướng) |
<!-- END metrics -->

<!-- BEGIN hud -->
| Điểm/hố/bẫy | Viewport | Hướng/khoảng cách | Hộp màn hình quét [x1,y1,x2,y2] | Camera đã chặn | Kết quả |
|---|---|---|---|---|---|
| S c12,r8 hitbox24×88 | 960 | hai hướng + mép chặn | [228.0, 196.0, 412.0, 288.0] | cx=480.0..640.0, cy=270.0..274.0 | PASS |
| S c12,r8 hitbox24×88 | 1200 | hai hướng + mép chặn | [348.0, 196.0, 412.0, 288.0] | cx=600.0..640.0, cy=270.0..274.0 | PASS |
| R c13,r8 hitbox24×88 | 960 | hai hướng + mép chặn | [228.0, 196.0, 444.0, 288.0] | cx=480.0..672.0, cy=270.0..274.0 | PASS |
| R c13,r8 hitbox24×88 | 1200 | hai hướng + mép chặn | [348.0, 196.0, 444.0, 288.0] | cx=600.0..672.0, cy=270.0..274.0 | PASS |
| R c146,r8 hitbox24×88 | 960 | hai hướng + mép chặn | [836.0, 196.0, 860.0, 288.0] | cx=4320.0..4320.0, cy=270.0..274.0 | PASS |
| R c146,r8 hitbox24×88 | 1200 | hai hướng + mép chặn | [1076.0, 196.0, 1100.0, 288.0] | cx=4200.0..4200.0, cy=270.0..274.0 | PASS |
| gap mép c44,r9 | 960 | →, trước 0 ô | [251.0, 283.0, 533.0, 289.0] | cx=1356.0..1636.0, cy=270.0..274.0 | PASS |
| gap mép c44,r9 | 1200 | →, trước 0 ô | [371.0, 283.0, 653.0, 289.0] | cx=1356.0..1636.0, cy=270.0..274.0 | PASS |
| gap mép c44,r9 | 960 | →, trước 1 ô | [283.0, 283.0, 565.0, 289.0] | cx=1324.0..1604.0, cy=270.0..274.0 | PASS |
| gap mép c44,r9 | 1200 | →, trước 1 ô | [403.0, 283.0, 685.0, 289.0] | cx=1324.0..1604.0, cy=270.0..274.0 | PASS |
| gap mép c44,r9 | 960 | →, trước 2 ô | [315.0, 283.0, 597.0, 289.0] | cx=1292.0..1572.0, cy=270.0..274.0 | PASS |
| gap mép c44,r9 | 1200 | →, trước 2 ô | [435.0, 283.0, 717.0, 289.0] | cx=1292.0..1572.0, cy=270.0..274.0 | PASS |
| gap mép c44,r9 | 960 | →, trước 3 ô | [347.0, 283.0, 629.0, 289.0] | cx=1260.0..1540.0, cy=270.0..274.0 | PASS |
| gap mép c44,r9 | 1200 | →, trước 3 ô | [467.0, 283.0, 749.0, 289.0] | cx=1260.0..1540.0, cy=270.0..274.0 | PASS |
| gap mép c46,r9 | 960 | ←, trước 0 ô | [427.0, 283.0, 709.0, 289.0] | cx=1244.0..1524.0, cy=270.0..274.0 | PASS |
| gap mép c46,r9 | 1200 | ←, trước 0 ô | [547.0, 283.0, 829.0, 289.0] | cx=1244.0..1524.0, cy=270.0..274.0 | PASS |
| gap mép c46,r9 | 960 | ←, trước 1 ô | [395.0, 283.0, 677.0, 289.0] | cx=1276.0..1556.0, cy=270.0..274.0 | PASS |
| gap mép c46,r9 | 1200 | ←, trước 1 ô | [515.0, 283.0, 797.0, 289.0] | cx=1276.0..1556.0, cy=270.0..274.0 | PASS |
| gap mép c46,r9 | 960 | ←, trước 2 ô | [363.0, 283.0, 645.0, 289.0] | cx=1308.0..1588.0, cy=270.0..274.0 | PASS |
| gap mép c46,r9 | 1200 | ←, trước 2 ô | [483.0, 283.0, 765.0, 289.0] | cx=1308.0..1588.0, cy=270.0..274.0 | PASS |
| gap mép c46,r9 | 960 | ←, trước 3 ô | [331.0, 283.0, 613.0, 289.0] | cx=1340.0..1620.0, cy=270.0..274.0 | PASS |
| gap mép c46,r9 | 1200 | ←, trước 3 ô | [451.0, 283.0, 733.0, 289.0] | cx=1340.0..1620.0, cy=270.0..274.0 | PASS |
| trap mép c86,r8 | 960 | →, trước 0 ô | [251.0, 251.0, 533.0, 257.0] | cx=2700.0..2980.0, cy=270.0..274.0 | PASS |
| trap mép c86,r8 | 1200 | →, trước 0 ô | [371.0, 251.0, 653.0, 257.0] | cx=2700.0..2980.0, cy=270.0..274.0 | PASS |
| trap mép c86,r8 | 960 | →, trước 1 ô | [283.0, 251.0, 565.0, 257.0] | cx=2668.0..2948.0, cy=270.0..274.0 | PASS |
| trap mép c86,r8 | 1200 | →, trước 1 ô | [403.0, 251.0, 685.0, 257.0] | cx=2668.0..2948.0, cy=270.0..274.0 | PASS |
| trap mép c86,r8 | 960 | →, trước 2 ô | [315.0, 251.0, 597.0, 257.0] | cx=2636.0..2916.0, cy=270.0..274.0 | PASS |
| trap mép c86,r8 | 1200 | →, trước 2 ô | [435.0, 251.0, 717.0, 257.0] | cx=2636.0..2916.0, cy=270.0..274.0 | PASS |
| trap mép c86,r8 | 960 | →, trước 3 ô | [347.0, 251.0, 629.0, 257.0] | cx=2604.0..2884.0, cy=270.0..274.0 | PASS |
| trap mép c86,r8 | 1200 | →, trước 3 ô | [467.0, 251.0, 749.0, 257.0] | cx=2604.0..2884.0, cy=270.0..274.0 | PASS |
| trap mép c88,r8 | 960 | ←, trước 0 ô | [427.0, 251.0, 709.0, 257.0] | cx=2588.0..2868.0, cy=270.0..274.0 | PASS |
| trap mép c88,r8 | 1200 | ←, trước 0 ô | [547.0, 251.0, 829.0, 257.0] | cx=2588.0..2868.0, cy=270.0..274.0 | PASS |
| trap mép c88,r8 | 960 | ←, trước 1 ô | [395.0, 251.0, 677.0, 257.0] | cx=2620.0..2900.0, cy=270.0..274.0 | PASS |
| trap mép c88,r8 | 1200 | ←, trước 1 ô | [515.0, 251.0, 797.0, 257.0] | cx=2620.0..2900.0, cy=270.0..274.0 | PASS |
| trap mép c88,r8 | 960 | ←, trước 2 ô | [363.0, 251.0, 645.0, 257.0] | cx=2652.0..2932.0, cy=270.0..274.0 | PASS |
| trap mép c88,r8 | 1200 | ←, trước 2 ô | [483.0, 251.0, 765.0, 257.0] | cx=2652.0..2932.0, cy=270.0..274.0 | PASS |
| trap mép c88,r8 | 960 | ←, trước 3 ô | [331.0, 251.0, 613.0, 257.0] | cx=2684.0..2964.0, cy=270.0..274.0 | PASS |
| trap mép c88,r8 | 1200 | ←, trước 3 ô | [451.0, 251.0, 733.0, 257.0] | cx=2684.0..2964.0, cy=270.0..274.0 | PASS |
| biên 0px | 960 | chặn camera | [0.0, 283.0, 0.0, 289.0] | cx=480.0..480.0, cy=270.0..274.0 | PASS |
| biên 0px | 1200 | chặn camera | [0.0, 283.0, 0.0, 289.0] | cx=600.0..600.0, cy=270.0..274.0 | PASS |
| biên 4800px | 960 | chặn camera | [960.0, 283.0, 960.0, 289.0] | cx=4320.0..4320.0, cy=270.0..274.0 | PASS |
| biên 4800px | 1200 | chặn camera | [1200.0, 283.0, 1200.0, 289.0] | cx=4200.0..4200.0, cy=270.0..274.0 | PASS |
<!-- END hud -->

Chạy để tái tạo hai bảng (nguyên script ở `tools/check_layout.py`):

```bash
python3 tools/check_layout.py design/maps/lay_dao_uc_v1.md --write-tables
python3 tools/check_layout.py design/maps/lay_dao_uc_v1.md
```

## 6. Câu hỏi còn mở và quyết định 29/10/2026

### Đã quyết định cho lượt chơi thử

- Giữ Đào Úc150 ô, khoảng chung map quái120–180 ô theo08; đã đồng bộ13.
  Trạng thái vẫn **Tạm thời — chốt sau chơi thử**, không phải duyệt bố cục.
- NV11 không ở Đào Úc: chuột đồng lớn tại Cánh đồng chiêm; lợn rừng tại Bến đò
  Hoàng Long; hổ con tại Núi đá Tràng An, theo bảng quái GDD. Không sửa GDD.
- NV13: mỗi hào trưởng ở một trong ba bản đồ trên; chốt tọa độ khi dựng các
  bố cục đó. Không thêm ba hào trưởng vào lưới Đào Úc.
- E trái ↔ Núi đá Tràng An. E phải ↔ E trái của đấu trường boss như mục1.
- c0…31 là **vùng an toàn**, ngoại lệ quy tắc mỗi màn có quái của08. M(c27,r8)
  là Đinh Điền đấu tập theo NV9, không sinh quái tự do; bản greybox cho chém hình nộm,
  không triển khai nhiệm vụ/AI. Không sửa lưới hiện có.
- Giữ nguyên tầng bục và khe c44–45 cho chơi thử. Trong greybox, D mở sẵn;
  chông/rơi hồi sinh ở R gần nhất đã ở phía trước trên đường đi (checkpoint đã qua),
  không trừ HP; đây không phải quyết định thay luật mất máu của sản phẩm.
- Ghi cho lệnh tileset sau: đất chiếm gần nửa dưới màn hình; cần chi tiết mặt cắt
  lũy, rễ và đá, không để toàn bộ đất là một mảng phẳng.

### Còn chờ chơi thử/quyết định

- Sau chơi thử quyết (a) thêm tầng bục thứ2–3 theo khuyến nghị08 hay không;
  (b) khe c44–45 giữ không đáy hay làm đáy nông. Hiện giữ nguyên lưới.
- Phân bổ ba đợt NV14 cho ba G, luật bảo vệ/khóa D, số quân, hồi sinh quái,
  phần thưởng rương và thời lượng từng đoạn vẫn chờ duyệt; greybox không làm nhiệm vụ.
- Cao độ y288, camera, HUD đầy đủ và điểm đáp phải được tôi thử trên Realme;
  không suy từ test headless thành duyệt bố cục hay mỹ thuật.
