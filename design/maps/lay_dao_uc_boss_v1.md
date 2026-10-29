# lay_dao_uc_boss_v1 — Lũy Tướng tiên phong Hậu Ngô

**Tạm thời — đang làm, chưa duyệt (A1).** Ô 32 px; tọa độ cột/hàng bắt đầu từ 0.
Ký hiệu S/R/E/N/m/M/B/D/G/c đặt ở ô chứa chân: chân tại ((c+0,5)×32;(r+1)×32).
Không phải ảnh cảnh nền, không phải bản đồ đã chơi thử; không sửa prototype hay số A0.

## 1. Thông tin chung

- Boss cấp15, NV15; **60×17 ô = 1920×544 px** (2 viewport960; 1,6 viewport1200),
  theo giới hạn45–60 ô của mục08. Dùng nền/tile Đào Úc, chưa vẽ art mới.
- E(c0,r8) nối **E(c149,r8) của `lay_dao_uc_v1.md`**. Trước trận đi hai chiều;
  D đóng khi bắt đầu, không đưa người chơi vào lại qua một cổng đã khóa.
- E(c59,r6) mở sau thắng/CS06 sang tuyến Hồi2; bản đồ đích cụ thể chờ xác nhận.
- GDD Phần4 mục3: boss **2 pha**, ngưỡng chuyển pha đầu **60% HP** theo quy tắc
  chung (30% dành bước chuyển tiếp của boss3 pha). Pha2 gọi **4 lính cung trên lũy**;
  đòn đặc biệt báo **1,5 giây**, vòng đỏ, ưu tiên xử lí lính phụ.

## 2. Lưới bố cục

```layout-meta
{
  "kind": "boss",
  "tile_px": 32,
  "mandatory_route": "lowest exposed support c0..59; open entrance after prerequisite, rampart included"
}
```

```layout
............................................................
............................................................
............................................................
............................................................
............................................................
............................................................
......................................................mm.mmE
............................................################
E...........S...R..D.........B..........####################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
############################################################
```

## 3. Chú thích từng điểm

- E(c0,r8): lối vào từ map đánh quái. S(c12,r8)=(400;288): điểm xuất hiện,
  không dùng x100 cũ. R(c16,r8)=(528;288): hồi sinh **ngay trước** D(c19,r8).
  "Đánh lại" SCR-06 đưa về R này rồi mới tái khởi động trận, không hồi sinh tại boss.
- D(c19,r8): cổng vào lũy; collider đóng cao đủ chắn nhảy khi trận bắt đầu
  (marker một ô chỉ là vị trí, không quy định cửa thật chỉ cao32 px).
- B(c29,r8): Tướng tiên phong Hậu Ngô. Sân c20…39, x640…1280: **640 px đất bằng**,
  không hố/chông/nước. Boss đứng x944, có304/336 px trống hai phía tới biên sân;
  sprite người~132 px, khung192×192 đặt chân y288, đầu khung y96, không bị trần che.
- Lũy đất sau kiểm HUD: c40…43 cao32 px; c44…59 cao64 px so với sân.
  **Mỗi lần lên32 px**; bậc đầu rộng128 px, mặt lũy trên rộng512 px;
  không bắt nhảy thẳng64 px, không cần khinh công. Người chơi lên được đánh lính.
- m(c54,r6), m(c55,r6), m(c57,r6), m(c58,r6): đúng4 vị trí lính cung pha2 trên mặt
  lũy y224, vùng dành cho lính c52…59 rộng256 px. Chưa sinh pha1; không thêm địch thứ5.
- E(c59,r6): ra sau trận; khóa trong trận, mở sau chiến thắng và CS06.

## 4. Nhịp chơi

1. Từ E, đi đến S rồi R trước cổng: nghỉ, thấy sân và lũy, chuẩn bị trước khi khóa.
2. Pha1 trên sân bằng640 px: học dấu vòng đỏ1,5 giây, không né kèm hố.
   Chạy200 px/s trong1,5 giây cho300 px di chuyển lý thuyết. Kích thước vòng đỏ
   chưa có nên đây là khoảng trống đề xuất, **chưa chứng minh né được mọi bán kính**.
3. Tới60% HP gọi4 lính cung trên lũy. Dãy bậc32 px nối sân lên tầng cao;
   người chơi có đường tiếp cận lính phụ, quay lại sân không bị khóa bởi cửa trong.
4. Thắng boss → CS06, cổng mở; E phải sang tuyến Hồi2. Thua → R trước cửa,
   thao tác Đánh lại giữ theo SCR-06, không tự thêm revive tại chỗ.

## 5. Kiểm tra số đo

Sơ đồ từ lưới thật: [lay_dao_uc_boss_v1.png](lay_dao_uc_boss_v1.png),
[lớp phủ960](lay_dao_uc_boss_v1_overlay_960.png),
[lớp phủ1200](lay_dao_uc_boss_v1_overlay_1200.png).
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
| step | c40..40, r9→r8 | 0/32 | nhảy chéo, không khinh công | 81.07/64.00 | PASS (quỹ đạo +24×88 hai hướng) |
| step | c44..44, r8→r7 | 0/32 | nhảy chéo, không khinh công | 81.07/64.00 | PASS (quỹ đạo +24×88 hai hướng) |
<!-- END metrics -->

<!-- BEGIN hud -->
| Điểm/hố/bẫy | Viewport | Hướng/khoảng cách | Hộp màn hình quét [x1,y1,x2,y2] | Camera đã chặn | Kết quả |
|---|---|---|---|---|---|
| S c12,r8 hitbox24×88 | 960 | hai hướng + mép chặn | [228.0, 196.0, 412.0, 288.0] | cx=480.0..640.0, cy=270.0..274.0 | PASS |
| S c12,r8 hitbox24×88 | 1200 | hai hướng + mép chặn | [348.0, 196.0, 412.0, 288.0] | cx=600.0..640.0, cy=270.0..274.0 | PASS |
| R c16,r8 hitbox24×88 | 960 | hai hướng + mép chặn | [228.0, 196.0, 540.0, 288.0] | cx=480.0..768.0, cy=270.0..274.0 | PASS |
| R c16,r8 hitbox24×88 | 1200 | hai hướng + mép chặn | [348.0, 196.0, 540.0, 288.0] | cx=600.0..768.0, cy=270.0..274.0 | PASS |
| biên 0px | 960 | chặn camera | [0.0, 283.0, 0.0, 289.0] | cx=480.0..480.0, cy=270.0..274.0 | PASS |
| biên 0px | 1200 | chặn camera | [0.0, 283.0, 0.0, 289.0] | cx=600.0..600.0, cy=270.0..274.0 | PASS |
| biên 1920px | 960 | chặn camera | [960.0, 219.0, 960.0, 225.0] | cx=1440.0..1440.0, cy=270.0..274.0 | PASS |
| biên 1920px | 1200 | chặn camera | [1200.0, 219.0, 1200.0, 225.0] | cx=1320.0..1320.0, cy=270.0..274.0 | PASS |
<!-- END hud -->

Chạy để tái tạo hai bảng (nguyên script ở `tools/check_layout.py`):

```bash
python3 tools/check_layout.py design/maps/lay_dao_uc_boss_v1.md --write-tables
python3 tools/check_layout.py design/maps/lay_dao_uc_boss_v1.md
```

<!-- BEGIN top-hud -->
| HUD / actor / player column | Viewport | Standing-camera cases (clamped) | Result |
|---|---|---|---|
| SCR-06 c0, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c0, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c0, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c0, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c1, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c1, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c1, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c1, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c2, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c2, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c2, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c2, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c3, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c3, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c3, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c3, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c4, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c4, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c4, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c4, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c5, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c5, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c5, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c5, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c6, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c6, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c6, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c6, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c7, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c7, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c7, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c7, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c8, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c8, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c8, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c8, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c9, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c9, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c9, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c9, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c10, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c10, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c10, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c10, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c11, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c11, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c11, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c11, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c12, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c12, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c12, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c12, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c13, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c13, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c13, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c13, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c14, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c14, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c14, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c14, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c15, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c15, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c15, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c15, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c16, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c16, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c16, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c16, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c17, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c17, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c17, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c17, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c18, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c18, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c18, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c18, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c19, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c19, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c19, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c19, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c20, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c20, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c20, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c20, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c21, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c21, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c21, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c21, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c22, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c22, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c22, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c22, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c23, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c23, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c23, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c23, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c24, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c24, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c24, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c24, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c25, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c25, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c25, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c25, chân r9 | 1200 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c26, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c26, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c26, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c26, chân r9 | 1200 | face +1; visible=mc54,Bc29; player96 | PASS |
| SCR-06 c27, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c27, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c27, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c27, chân r9 | 1200 | face +1; visible=mc54,mc55,Bc29; player96 | PASS |
| SCR-06 c28, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c28, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c28, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c28, chân r9 | 1200 | face +1; visible=mc54,mc55,Bc29; player96 | PASS |
| SCR-06 c29, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c29, chân r9 | 960 | face +1; visible=Bc29; player96 | PASS |
| SCR-06 c29, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c29, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,Bc29; player96 | PASS |
| SCR-06 c30, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c30, chân r9 | 960 | face +1; visible=mc54,Bc29; player96 | PASS |
| SCR-06 c30, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c30, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c31, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c31, chân r9 | 960 | face +1; visible=mc54,mc55,Bc29; player96 | PASS |
| SCR-06 c31, chân r9 | 1200 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c31, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c32, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c32, chân r9 | 960 | face +1; visible=mc54,mc55,Bc29; player96 | PASS |
| SCR-06 c32, chân r9 | 1200 | face -1; visible=mc54,Bc29; player96 | PASS |
| SCR-06 c32, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c33, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c33, chân r9 | 960 | face +1; visible=mc54,mc55,mc57,Bc29; player96 | PASS |
| SCR-06 c33, chân r9 | 1200 | face -1; visible=mc54,mc55,Bc29; player96 | PASS |
| SCR-06 c33, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c34, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c34, chân r9 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c34, chân r9 | 1200 | face -1; visible=mc54,mc55,Bc29; player96 | PASS |
| SCR-06 c34, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c35, chân r9 | 960 | face -1; visible=Bc29; player96 | PASS |
| SCR-06 c35, chân r9 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c35, chân r9 | 1200 | face -1; visible=mc54,mc55,mc57,Bc29; player96 | PASS |
| SCR-06 c35, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c36, chân r9 | 960 | face -1; visible=mc54,Bc29; player96 | PASS |
| SCR-06 c36, chân r9 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c36, chân r9 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c36, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c37, chân r9 | 960 | face -1; visible=mc54,mc55,Bc29; player96 | PASS |
| SCR-06 c37, chân r9 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c37, chân r9 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c37, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c38, chân r9 | 960 | face -1; visible=mc54,mc55,Bc29; player96 | PASS |
| SCR-06 c38, chân r9 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c38, chân r9 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c38, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c39, chân r9 | 960 | face -1; visible=mc54,mc55,mc57,Bc29; player96 | PASS |
| SCR-06 c39, chân r9 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c39, chân r9 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c39, chân r9 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c40, chân r8 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c40, chân r8 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c40, chân r8 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c40, chân r8 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c41, chân r8 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c41, chân r8 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c41, chân r8 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c41, chân r8 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c42, chân r8 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c42, chân r8 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c42, chân r8 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c42, chân r8 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c43, chân r8 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c43, chân r8 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c43, chân r8 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c43, chân r8 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c44, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c44, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c44, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c44, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c45, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c45, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c45, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c45, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c46, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c46, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c46, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c46, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c47, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c47, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c47, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c47, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c48, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c48, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c48, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c48, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c49, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c49, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c49, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c49, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c50, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c50, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c50, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c50, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c51, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c51, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c51, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c51, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c52, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c52, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c52, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c52, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c53, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c53, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c53, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c53, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c54, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c54, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c54, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c54, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c55, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c55, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c55, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c55, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c56, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c56, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c56, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c56, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c57, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c57, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c57, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c57, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c58, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c58, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c58, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c58, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c59, chân r7 | 960 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c59, chân r7 | 960 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c59, chân r7 | 1200 | face -1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| SCR-06 c59, chân r7 | 1200 | face +1; visible=mc54,mc55,mc57,mc58,Bc29; player96 | PASS |
| S c12,r8, image128×96 | 960 | top+bottom; [176.0, 188.0, 464.0, 288.0] | PASS |
| S c12,r8, image128×96 | 1200 | top+bottom; [296.0, 188.0, 464.0, 288.0] | PASS |
| R c16,r8, image128×96 | 960 | top+bottom; [176.0, 188.0, 592.0, 288.0] | PASS |
| R c16,r8, image128×96 | 1200 | top+bottom; [296.0, 188.0, 592.0, 288.0] | PASS |
<!-- END top-hud -->

## 6. Câu hỏi còn mở và quyết định 29/10/2026

### Đã quyết định cho lượt chơi thử

- Giữ đấu trường60 ô; khoảng chung45–60 ô theo08 đã đồng bộ13;
  **Tạm thời — chốt sau chơi thử**.
- Tướng tiên phong Hậu Ngô có **đúng2 pha, chỉ chuyển ở60% HP**.
  Không dùng ngưỡng30%, không thêm pha3. Không đổi HP/sát thương trong GDD.
- Boss đầu báo đòn đặc biệt1,5 giây; boss sau rút dần về1,2–0,8 giây,
  không dưới0,8 giây. Đã ghi13 và09, vẫn Tạm thời. Greybox chỉ hình nộm,
  chưa có đòn, vòng đỏ hoặc AI boss.
- E phải sau thắng/CS06 → Đầm lầy Đại Hoàng (NV16). E trái ↔ Đào Úc.
  Hai bản đồ ngoài phạm vi (Tràng An/Đại Hoàng) chỉ có nhãn đích trong bản thử,
  không tạo map giả thay cho thiết kế của chúng. Hai E nội bộ chuyển được hai chiều.
- Người dùng chấp nhận bản thử29/10/2026; lượt sửa HUD này chọn ẩn minimap
  và cho phép hạ lũy y160→224, giữ từng bậc32 px,4 lính và sân640 px. D mở sẵn; nút hồi sinh/quay lại không làm
  cơ chế revive tại chỗ. R trước cửa vẫn dùng như lưới.
- Lệnh tileset sau cần mặt cắt lũy/đất có rễ và đá vì đất chiếm gần nửa dưới màn.

### Còn chờ chơi thử/quyết định

- Cùng bản đồ quái: sau chơi thử quyết thêm tầng bục thứ2–3 theo08 hay không,
  và khe c44–45 ở map quái giữ không đáy hay đáy nông. Lưới chỉ hạ lũy để tránh HUD theo xác nhận bổ sung; chưa duyệt chính thức.
- Bán kính vòng đỏ, hitbox boss, tầm cung và va chạm khi áp sát chưa chốt;
  sân640 px vẫn cần chơi thử trước khi duyệt khả năng né.
- Cửa thật phải đủ cao để không nhảy qua; quy tắc khóa/mở và reset trận chờ
  lượt triển khai riêng. Greybox không giả làm trận boss hoàn chỉnh.
- Bốn lính cung là hình nộm đứng yên, không bắn; kiểm camera/HUD trên Realme còn chờ.

- Follow-up29/10/2026: SCR-06 ẩn minimap, thêm thanh boss360×32 ởy24 (Tạm thời).
  Ẩn minimap riêng chưa đủ do menu/⚙; người dùng đã cho phép hạ lũy thêm64 px.
  Bốn m giữ c54/55/57/58, chuyển r4→r6; E phải r4→r6. Sân c20…39 vẫn640 px.
  Hộp hình người96px và boss132px kiểm ở mọi cột đứng được, cả hai viewport/hướng;
  các hình vẽ/JSON/bản thử phải theo cấu hình này. Không phải UI thành phẩm.
