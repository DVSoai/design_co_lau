# A0 — Bản thử cảm giác

Dự án độc lập, mã bỏ đi, **không chép sang game thật**. Mốc A0 chưa được nghiệm thu:
người dùng cần chơi thử trên Android và chốt thông số. Không thay đổi trạng thái
thiết kế trong docs. Không có giao diện game, lưu game, vật phẩm, nhiệm vụ hay âm thanh.
Các nút cảm ứng và chữ debug chỉ phục vụ kiểm thử kỹ thuật.

## Phiên bản và chạy PC

Dùng **Godot 4.7.2 stable**, bản Standard (GDScript), renderer Compatibility.
Đã kiểm tra bằng `4.7.2.stable.official.ed1daf0bf`.

1. Cài Godot 4.7.2 Standard từ nguồn chính thức.
2. Import **prototype/project.godot** trong Project Manager, không import thư mục gốc repo.
3. Mở dự án, chờ import PNG, bấm F6 với main.tscn hoặc F5.
   Từ thư mục gốc repo cũng có thể chạy `godot --path prototype`.
4. A/D hoặc ←/→ để đi; Space/W/↑ để nhảy; J/X để chém; F1 bật/tắt khung
   va chạm, cửa sổ chém đang hoạt động và các giá trị cấu hình.
5. Chạy qua bậc 32 px, nhảy qua hố 96 px, thử các bục nổi; rơi khỏi bản đồ sẽ về điểm đầu.
   Đứng cạnh hình nộm tại x=490 và chém: mỗi đòn chỉ hiện một số sát thương.
   Các khối nổi hiện dùng va chạm đặc, không phải bục một chiều.

Kích thước thiết kế 960×540, canvas_items, aspect **expand**, scale **fractional**
mặc định, texture nearest. Viewport logic mở rộng theo tỉ lệ màn hình thật;
không ép màn hình dài vào khung 16:9. Phóng lẻ có thể làm các pixel có bề rộng
hiển thị không đều, dù texture vẫn nearest. Bảng ⚙ có công tắc **Phóng nguyên/lẻ**
(bật = integer, tắt = fractional) để so sánh trực tiếp; integer có thể lại tạo viền.
Nút cảm ứng, ⚙, bảng và giới hạn camera cập nhật theo viewport mỗi lần resize.
PNG placeholder được chép nguyên từ
`art/sprites/characters/chr_dbl_idle_side_96.png` của commit
`3423fa9`; shader chỉ ẩn nền xanh #00FF00 lúc vẽ, không sửa ảnh nguồn.
Đây là ảnh chưa duyệt, không phải luồng chuyển art/approved sang game thật.

## Chỉnh cảm giác

Mở `config/tuning.gd`: tốc độ/gia tốc, chiều cao/thời gian lên đỉnh,
coyote time, jump buffer, hitbox, camera, nhịp chém, sát thương, hình học bản đồ.
Mỗi hằng số có chú thích đơn vị. Trọng lực và vận tốc nhảy suy ra từ
`g = 2h/t²`, `v = -2h/t`. Thời gian hồi chiêu tính **sau khi hết động tác**.
Chỉ gây sát thương trong [HIT_START, HIT_END), một lần mỗi mục tiêu mỗi đòn.
Camera có dead zone và look-ahead ngang; bản đồ chỉ cao một viewport nên camera
dọc bị khóa trong giới hạn bản đồ. Bản đồ rộng 2880 px (ba màn hình).
Các con số mới là giá trị thử A0, không tự chốt thông số chính thức.

## Xuất APK Android để thử

1. Cài Godot **4.7.2** Standard và **OpenJDK 17** trên PC.
2. Trong Godot: **Editor → Manage Export Templates**, cài template **4.7.2**
   khớp editor (tải từ nguồn chính thức hoặc dùng Download and Install).
3. Cài Android Studio và Android SDK Command-line Tools. Trong SDK Manager cài
   Android SDK Platform 35, Build-Tools 35.0.0 và Platform-Tools.
   Đây là quy trình xuất APK bằng template có sẵn; không bật Gradle/custom build.
   Nếu editor báo thiếu thành phần SDK, làm theo yêu cầu của exporter 4.7.2.
4. **Editor → Editor Settings → Export → Android**: đặt Java SDK Path tới JDK 17,
   Android SDK Path tới thư mục SDK; kiểm tra đường dẫn debug keystore.
   Nếu chưa có, tạo keystore thử bằng:

   ```sh
   keytool -genkeypair -keystore debug.keystore -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 -storepass android -keypass android -dname "CN=Android Debug,O=Android,C=US"
   ```

   Chọn file đó trong Android Debug Keystore của editor, user `androiddebugkey`,
   password `android`. Đây chỉ là khóa thử; không dùng phát hành, không commit keystore.
5. **Project → Export → Add → Android**. Đặt package duy nhất, ví dụ
   `org.colau.a0prototype`; orientation **Landscape**; bật arm64-v8a
   (thêm armeabi-v7a nếu thiết bị cần). Giữ Compatibility, tắt Gradle build.
   Trong preset Android bật **Screen → Immersive Mode** (`screen/immersive_mode=true`)
   để ẩn cả thanh trạng thái và thanh điều hướng. Dự án đặt
   `display/window/size/mode.mobile=3` (Fullscreen trên Android); PC vẫn chạy cửa sổ.
   Giữ **Landscape** và export template 4.7.2 khớp editor. Nếu dùng file
   export_presets.cfg đã có, kiểm tra lại mục sau trong phần [preset.N.options]:

   ```ini
   screen/immersive_mode=true
   ```

   Project Settings đã bật `rendering/textures/vram_compression/import_etc2_astc=true`;
   chờ import lại rồi xuất/cài lại APK để cấu hình mới có hiệu lực.
   Không cần quyền Internet hay Google Play.
6. Chọn **Export Project**, bật **Export With Debug**, lưu APK **ngoài checkout**,
   ví dụ thư mục Downloads. Đây là APK thử cài trực tiếp, không phải AAB phát hành.
7. Trên điện thoại bật Developer options → USB debugging; kết nối USB, chấp nhận
   máy tính. Chạy `adb devices`, rồi `adb install -r /đường/dẫn/a0.apk`;
   hoặc chép APK và cho phép cài từ nguồn tương ứng.
8. Mở app ở hướng ngang. D-pad bên trái có ←/→ ở dưới, ↑ ở trên giữa,
   hai vùng chạm vô hình ở hai bên ↑. Cụm chém/bình/đổi mục tiêu ở bên phải, năm ô kỹ năng
   ở giữa đáy; xem phần bố cục cảm ứng phía dưới. Thử nhiều ngón đồng thời.
   Các nút cũng được vẽ trên PC để xem bố cục và thử bằng chuột.
9. Kiểm tra chạy/nhảy, coyote/jump buffer, hitbox, camera, nhịp chém, mép màn hình
   và độ đọc của nhân vật 96 px. Dòng Screen / Window / Viewport / Scale xuất hiện
   trong bảng ⚙; F1 cũng hiện dòng này. Screen là độ phân giải màn hình vật lý,
   Window là diện tích cửa sổ app; Viewport là vùng logic sau stretch.
   Trên headless, Screen dùng kích thước cửa sổ mô phỏng.
   So sánh Phóng nguyên/lẻ ngay trên máy, kiểm tra immersive sau khi xuất APK.
   Có thể nối bàn phím gửi F1 để xem debug.
   Ghi nhận thiết bị và cảm giác để người dùng nghiệm thu A0; không coi headless là nghiệm thu Android.

Chưa xuất APK hoặc chạy trên thiết bị Android trong môi trường này.

## Kiểm tra headless

Từ thư mục gốc repo:

```sh
godot --headless --path prototype --editor --import --quit
godot --headless --path prototype --quit-after 120
godot --headless --path prototype --script res://tests/smoke.gd
```

Nếu thư mục người dùng chỉ đọc, đặt XDG_DATA_HOME, XDG_CONFIG_HOME,
XDG_CACHE_HOME tới các thư mục ghi được trước khi chạy. Smoke test thoát khác 0
khi lỗi: chạm đất, di chuyển, nhảy, rơi/chạm đất, chém đúng một lần,
hiện số sát thương, bật debug và hồi vị trí sau rơi. Kiểm tra này không thay thế
chơi thử đa chạm, đồ họa hoặc xuất APK.

Kết quả trong môi trường đám mây: import editor và chạy 120 frame thoát 0,
không có lỗi Godot; smoke test hiện tại 125 kiểm tra PASS, `A0 smoke failures: 0`.
Binary Linux 4.7.2 đã được đối chiếu SHA-512 với manifest chính thức.

## Bảng chỉnh khi chạy

Nút **⚙** ở góc trên phải luôn hiện trên PC và cảm ứng. Bấm để mở/đóng
bảng; cuộn để xem đủ 13 thanh trượt. Mỗi thanh hiện tên, số và đơn vị.
Các thay đổi tác dụng ngay cho chạy/gia tốc, nhảy, camera và nhịp chém;
trọng lực/vận tốc nhảy tự tính lại. Giữ ATTACK_DURATION tối thiểu 0,22 s
để cửa sổ trúng [0,10; 0,20) s vẫn nằm trong động tác.
Nút **Sao chép** đưa toàn bộ thông số hiện tại, kể cả trọng lực/vận tốc nhảy,
vào clipboard hệ điều hành (cần chạy có màn hình; headless chỉ kiểm tra nội dung).
Giá trị chỉ nằm trong bộ nhớ, khởi động lại sẽ lấy mặc định từ tuning.gd;
không lưu hoặc ghi đè file cấu hình.

Mặc định RUN_SPEED=200 px/s, TIME_TO_APEX=0,38 s: tầm nhảy ngang lý thuyết
200 × 2 × 0,38 = **152 px**, lớn hơn 1,5 × hố 96 px = **144 px**.
Đây là tầm lý thuyết với vận tốc ngang 200 px/s, cùng cao độ cất/hạ cánh.
Vùng chéo trong Kiểu cổ điển dùng 0,8 × tốc độ nên tầm tương ứng là 121,6 px
khi chưa khinh công. Ở kiểu cũ, cần chạy lấy đà để đạt tốc độ này. Smoke test assert điều kiện này từ hình học hố thật.

## Chuyển động giả (không thêm khung hình)

Bảng ⚙ có công tắc **Chuyển động giả**, mặc định bật. Tắt sẽ trả sprite về vị
trí, góc và scale gốc ngay ở tick vật lý kế tiếp; bật lại để so sánh cảm giác.
Chỉ Sprite2D đổi transform; CharacterBody2D, hitbox người chơi và Area2D chém
không đổi. Không sửa PNG hoặc thêm frame hoạt ảnh.

Mọi biên độ/thời gian nằm trong config/tuning.gd:
- Đứng yên nhún ±1 px, chu kỳ 1,2 s.
- Chạy nhấp nhô ±2 px, một chu kỳ mỗi 100 px di chuyển (0,5 s ở 200 px/s),
  nghiêng 4° theo hướng chạy; giữ mốc chân khi nghiêng/co giãn.
- Bật nhảy scale (0,9; 1,1), chạm đất (1,15; 0,85); hồi tuyến tính về (1; 1)
  trong 0,1 s. Không phát lại pulse nhảy khi chỉ đi ra khỏi mép.
- Chém dịch sprite 4 px theo hướng nhìn chỉ trong cửa sổ trúng.

Công tắc chỉ lưu trong bộ nhớ và có trong văn bản “Sao chép”. Chưa đánh giá
cảm giác hình ảnh trên điện thoại; headless kiểm tra transform và hitbox.

## Kết quả thử PC và bảo vệ thông số

Người dùng thử bằng Godot 4.7.2 trên PC ngày 28/10/2026, thấy ổn với bộ mặc
định, không chỉnh thông số. Kết quả này thuộc bộ trước khi thêm Kiểu cổ điển
(kiểu cũ nhảy 80 px); không xác nhận chế độ cổ điển mới nhảy 96 px.
Kết quả được ghi trong `docs/13_thong_so.md` và `docs/05_log.md`: vẫn Tạm thời,
chờ thử Android và xác nhận của người dùng.

Nút ⚙, thanh trượt, công tắc và nút Sao chép không nhận focus bàn phím.
Phím mũi tên tiếp tục dùng để chơi, không chuyển focus hoặc đổi số; con lăn
chỉ cuộn danh sách, không thay giá trị thanh trượt. Mỗi slider cao tối thiểu 44 px;
chỉ kéo ngang **bắt đầu trên núm** (vùng chạm rộng tối thiểu 32 px) mới đổi số.
Bấm hoặc vuốt từ rãnh không nhảy giá trị. Hướng kéo được khóa sau 8 px: vuốt dọc
cuộn bảng, kể cả bắt đầu trên núm; kéo ngang chỉnh giá trị. Chuột và cảm ứng cùng
áp dụng quy tắc này.

## Kiểm tra hiển thị Android trong headless

Smoke test resize Window thực của Godot và kiểm tra stretch transform phủ kín cửa sổ,
không có offset/viền letterbox, với ba trường hợp mặc định fractional + expand:

| Window mô phỏng | Viewport logic | Hệ số phóng |
|---|---|---|
| 1920×1080 | 960×540 | 2 |
| 2400×1080 | 1200×540 | 2 |
| 1600×720 | 1200×540 | 1,333333 |

Test xác nhận nút cảm ứng, ⚙ và bảng nằm trong viewport, camera dùng giới hạn mới,
công tắc phóng hoạt động. Sự kiện touch được đưa qua Input.parse_input_event để
kiểm tra cuộn dọc không đổi số và kéo ngang từ núm vẫn chỉnh được. Trong headless
bật mô phỏng touchscreen chỉ ở test để ScrollContainer nhận gesture như thiết bị touch.
Đây là kiểm tra bố cục/phép biến đổi và input, không phải ảnh chụp màn hình Android.
Chưa xuất lại APK hoặc xác minh thanh hệ thống immersive trên điện thoại trong môi trường này.

## Bố cục cảm ứng d-pad A0

Mọi nút/HUD được vẽ bằng mã (khối, đường tròn, chữ/mũi tên), không dùng ảnh,
biểu tượng hay mã của game khác. Nút di chuyển 84 px logic, cách mép ít nhất
24 px; nền alpha 0,45 và viền sáng. Khi chạm, viền sáng hơn và hình nút thu 0,95
nhưng vùng bắt chạm không co. Chữ/mũi tên tối thiểu 22 px logic.
Tất cả kích thước, tỉ lệ, khoảng cách và alpha nằm trong config/tuning.gd.

- Trái chỉ có **ba nút nhìn thấy: ←, →, ↑**. Với d = 84 px, ← ở x0,
  → ở x0 + 2,2d; ↑ căn giữa ở y = lower_y − 1,35d. Hai vùng chéo **vô hình**
  rộng 0,9d, cao d, sát hai mép bên của ↑, cùng hàng với ↑. Chạm vùng chéo
  giữ hướng tương ứng và nhảy, đồng thời làm sáng viền ↑ và nút ←/→ cùng phía.
  Chỉ F1 debug mới vẽ viền mảnh của vùng chéo, không có nền/chữ/mũi tên.
  Ưu tiên bắt chạm: ↑, sau đó vùng chéo, sau đó ←/→. Trượt ra khỏi vùng thì nhả action; nhả một
  ngón không hủy action mà ngón khác đang giữ. Bàn phím và touch dùng action
  riêng, không nhả nhầm phím PC đang giữ. Không còn nút nhảy ở bên phải.
- Phải: CHÉM tròn đường kính 1,4 lần nút di chuyển. Trên là ĐỔI (đổi mục tiêu,
  chỉ log); phía trên-trái là HP, phía trái là MP. HP/MP có số đếm thử, mỗi lần
  bấm giảm một và log, không hồi máu/nội lực, không có inventory.
- Giữa đáy: năm ô vuông 1–5, cạnh 0,7 lần nút di chuyển, cách nhau 6 px.
  Bấm chỉ log số ô; chưa có hệ thống kỹ năng.
- HUD giữ chỗ phía trên: vòng cấp độ, thanh đỏ/xanh ở trái; nút menu (≡, chỉ log)
  và khối bản đồ 120×80 ở phải. Không có giá trị gameplay hay chức năng bản đồ.
  Nút ⚙ tối thiểu 56×56; công tắc **Hiện HUD giữ chỗ** giúp so diện tích cảnh.

Các công tắc trong ⚙ chỉ đổi trong RAM và có trong văn bản Sao chép:

- **Giữ để nhảy lại**: mặc định bật. Giữ ↑, vùng chéo vô hình hoặc phím nhảy sẽ tự
  nhảy lần nữa khi chạm đất. Tắt để chỉ nhảy một lần mỗi lần bấm.
- **Giữ lâu nhảy cao**: mặc định tắt. Khi bật, nhả toàn bộ nút/phím nhảy sớm
  giảm vận tốc đi lên còn 50%; giữ đến đỉnh cho đủ độ cao.
- **Xoay khi nhảy chéo**: chỉ áp dụng khi **tắt Kiểu cổ điển**, mặc định bật.
  Nhảy bắt đầu từ vùng chéo trái/phải thì sprite xoay
  một vòng theo hướng nhảy; thời gian danh nghĩa bằng 2 × TIME_TO_APEX,
  phủ pha lên và rơi cùng cao độ. Khi chạm đất thì kết thúc, kể cả đáp lên bậc
  sớm; rơi lâu hơn thời gian danh nghĩa thì giữ góc đã đủ một vòng cho tới khi
  đáp đất. Không xoay body/hitbox. Công tắc Chuyển động giả vẫn là công tắc tổng.

Vệt chém và số sát thương nằm trên lớp z cao hơn hình nộm; hitbox không thay đổi.
Bảng ⚙ chặn các vùng cảm ứng phía dưới bảng khi đang mở. Đóng bảng để thử nút.
Khi xuất APK nhớ bật **Screen → Immersive Mode**, theo phần Android ở trên.
Headless kiểm tra vùng chéo, giữ nhảy, nhảy cao/thấp và bố cục ở 1600×720,
2400×1080, 1920×1080. Cần thử lại thao tác ngón cái và độ đọc trên điện thoại thật.

## Kiểu cổ điển (mặc định bật)

Công tắc **Kiểu cổ điển** và **Khinh công** trong ⚙ đều mặc định bật.
Đây là cơ chế tự triển khai trong prototype, không dùng mã hoặc tài nguyên game khác.

- Bấm hướng chạy đạt RUN_SPEED ngay. Buông hướng giảm vận tốc về 0 trong
  STOP_TIME (0,08 s). Bấm hướng ngược trên đất thì khung đầu đổi mặt, đứng
  TURN_TIME (0,05 s) rồi chạy; nhả trong nhịp đứng sẽ chỉ quay mặt.
- Trên không, hướng trái/phải nhận tốc độ ngay, không có nhịp quay đầu.
  Giữ vùng chéo dùng 0,8 × RUN_SPEED; nút hướng riêng dùng đủ RUN_SPEED.
- JUMP_HEIGHT mặc định 96 px, TIME_TO_APEX 0,38 s: g ≈ 1329,64 px/s²,
  JUMP_SPEED ≈ −505,26 px/s. Cùng một trọng lực khi lên và xuống, không chèn
  thời gian đứng ở đỉnh. Tích phân vị trí midpoint cho thời gian lên/xuống đối
  xứng; đầu ra kiểm tra trên mặt đất cùng cao độ là 23/23 khung ở 60 Hz.
  FALL_SPEED_MAX tự tính bằng 2 × |JUMP_SPEED|, mặc định ≈ 1010,53 px/s.
- **Khinh công**: chỉ khi đang đi lên và |vy| ≤ 30% |JUMP_SPEED|, nhả toàn bộ
  nút/phím nhảy rồi bấm mới được bật thêm một lần với 0,7 × JUMP_SPEED.
  Bấm sớm không xếp hàng để tự bật khinh công; giữ liên tục không phải lần bấm mới.
  Tối đa một lần cho mỗi cú nhảy, quyền bật thêm reset khi chạm đất.
- Mỗi pha nhảy bắt đầu lộn khi vận tốc lên vào ngưỡng 30%, theo hướng mặt lúc đó.
  Sprite xoay một vòng trong APEX_FLIP_TIME (0,2 s); khinh công có thêm một vòng.
  Nếu hai vòng đến sát nhau, vòng sau đợi vòng trước xong. Trên mặt đất cùng
  cao độ với mặc định, cả hai hoàn tất trước khi đáp đất. Va chạm đất/đầu hoặc
  đổi chế độ có thể kết thúc pha bay sớm. Hitbox không xoay.
  Kiểu cổ điển bỏ xoay chậm suốt nhảy chéo; Chuyển động giả vẫn là công tắc tổng.
- Có thanh trượt STOP_TIME, TURN_TIME và APEX_FLIP_TIME, đơn vị giây.
  ACCELERATION vẫn chỉnh được nhưng chỉ tác động khi dùng kiểu cũ.

Tắt Kiểu cổ điển để trở về tăng/giảm tốc bằng ACCELERATION, đổi mặt ngay khi
đổi hướng, tích phân và rơi như trước, không có khinh công/lộn đỉnh. Mặc định
chiều cao kiểu cũ là 80 px. Hai chế độ nhớ riêng giá trị chiều cao đã chỉnh trong
RAM; đổi công tắc cập nhật slider JUMP_HEIGHT, trọng lực và vận tốc nhảy theo
chế độ đó. Các thông số còn lại dùng chung; không ghi đè tuning.gd. Bộ kiểm tra
cũ chạy trong chế độ cũ, rồi kiểm tra riêng chế độ cổ điển và bật/tắt công tắc.
Chưa thử lại cảm giác điều khiển trên điện thoại Android thật trong môi trường này.

## Giai đoạn 1 — Rig greybox (chưa duyệt)

Giữ **Godot 4.7.2 Standard**. F5 chạy A0 gốc; bấm **Mở rig greybox** để sang cảnh mới
`rig/rig_greybox.tscn` (hoặc mở cảnh và F6). Mã player/world và thông số A0 giữ nguyên.
Mở ⚙: **Rig greybox** bật/tắt thay sprite, **Vũ khí cung** đổi đao/cung; bộ chọn
**Theo trạng thái thật A0** hoặc clip riêng để xem 3 nhát Đao, bắn, hurt/ngã.
**Về A0 gốc** nằm trong bảng ⚙. Cung chỉ đổi hoạt ảnh, không thêm đạn/hitbox mới.
F1 hiện điểm khớp. Cảnh mới dùng lại điều khiển PC/cảm ứng A0, không lưu tùy chọn.

Dữ liệu `rig/data/parts.json` và `animations.json` là nguồn bộ phận/pose/thời lượng,
không dùng ảnh game khác. Xem bảng khớp, trạng thái đề xuất và phép đo tại
`../docs/16_rig_nhan_vat.md`. Đây là ngoại lệ prototype, không phải mã game thật.

Sau ba lệnh headless ở trên, chạy thêm:

```sh
godot --headless --path prototype --script res://tests/rig_smoke.gd
godot --headless --path prototype --script res://rig/export_frames.gd
python prototype/rig/render_contact_sheets.py
```

Contact sheet tại `rig/contact_sheets/`, raster từ polygon đã được chính scene
Godot tính transform, không phải screenshot GPU toàn cảnh. Đo lại ảnh nguồn bằng
`python prototype/rig/measure_reference.py`; ngưỡng tách silhouette và mốc cổ/hông
chọn bằng mắt được ghi rõ trong script và tài liệu. Khối màu chưa duyệt mỹ thuật.


## Đào Úc greybox — bố cục Giai đoạn 1/A1 (29/10/2026)

Godot **4.7.2 Standard**. Từ A0 chính (F5), bấm **Đào Úc greybox** bên dưới nút
Mở rig greybox; hoặc mở `dao_uc/dao_uc.tscn` rồi F6. Nút **Về A0** ở trên.
Góc trên in map, tọa độ ô(c,r) ngay dưới chân và px để báo lỗi trên Realme.

Nguồn chuẩn là hai khối `layout` và `layout-meta` trong `design/maps/`. Runtime
đọc JSON sinh tự động, không nhập lại lưới và không đóng gói Markdown. Trước khi
chạy/build, sau **mọi thay đổi** hai file layout (kể cả ghi chú/bảng kiểm), hoặc
kích thước HUD boss trong `06_screens.md`, từ gốc repo chạy:

```sh
python3 tools/export_layout_json.py
python3 tools/export_layout_json.py --check
```

Hai JSON trong `prototype/dao_uc/layouts/` giữ nguyên ký tự từng hàng, meta và
SHA256 của toàn bộ Markdown nguồn. Phần HUD đi kèm lấy từ A0 và khối hud-metrics
của06; không phải bộ số A0 mới. `--check` so bản sinh trong bộ nhớ với file đang
có, không ghi file, thoát khác0 nếu lệch. Test PC so SHA và **từng ô** với nguồn
`../design/maps`; trên APK không có file nguồn nên việc đối chiếu phải chạy trước
export. Đã bỏ sync_layouts.py, bản sao Markdown và manifest cũ.

**Không cần include_filter** cho các JSON này khi xuất với Resources → Export
all resources; không thêm bộ lọc Markdown. Kiểm bằng export-pack với preset tạm
không có include_filter và đọc danh sách/JSON từ gói. Godot4.7.2 ghi chẩn đoán
thiếu khóa khi preset bỏ hẳn khóa này; export vẫn exit0 và được kiểm bằng dữ liệu
trong PCK. Với preset do editor tạo, để trường lọc rỗng, không cần thêm mẫu lọc. Android vẫn bật
**Screen → Immersive Mode**. Không export nhầm dự án gốc repo.

- `#` là đất va chạm; `=` là bục một chiều, nhảy từ dưới rồi đứng trên.
- Chông `^` hoặc rơi dưới map đưa về **R gần nhất bên trái điểm gặp nạn**
  (checkpoint phía trước chướng ngại theo tuyến trái→phải); trước R đầu thì về S.
  Không đưa về R chưa tới ở cuối map, không trừ HP, không có lưu game/checkpoint bền vững.
- `~` là nước nông: tốc độ ngang nhân0,7 khi chân ở trong nước; RUN_SPEED trong
  tuning vẫn200. Không đổi trọng lực/nhảy đã duyệt. Ra khỏi nước trở lại tốc độ A0.
- `L`: giữ ↑/W hoặc nút ↑ cảm ứng để leo, ↓/S để xuống. Khi gần/đang ở thang có
  nút ngữ cảnh **↓** và **Nhảy** bên trái phía trên d-pad. Trên thang có thể dừng
  giữ y, rời bằng ←/→ hoặc Space/nút Nhảy. Tốc độ leo chỉ cho greybox bằng
  RUN_SPEED/2=100 px/s; không phải số A0 được sửa hoặc nghiệm thu mới.
- N/m/M/B là `dummy.gd` A0, chém được, không đánh trả. c0…31 là trại an toàn,
  M Đinh Điền là hình nộm đấu tập; không sinh quái tự do. Không có AI/nhiệm vụ,
  boss2 pha thật hay mưa tên. Các marker còn lại là khối có nhãn. D mở sẵn.
- E phải Đào Úc ↔ E trái đấu trường chuyển hai chiều. Đi vào boss tại S; quay
  về Đào Úc tại R bên phải. Camera được reset/chặn tại điểm đến rồi mới bật
  lại xử lí player sau2 khung; giữ nguyên dead-zone/look-ahead/response A0.
- E trái Đào Úc ghi Tràng An; E phải boss ghi Đại Hoàng sau thắng/CS06: chỉ là
  nhãn đích vì hai map ngoài chưa được dựng, không tạo scene giả cho chúng.
- Bảng ⚙, F1, bàn phím và cụm cảm ứng dùng nguyên A0. Không sửa tuning.gd.
  Player/world có hook bounds/reset/speed với mặc định A0 cũ; lớp con greybox
  chỉ cung cấp kích thước lưới, hồi sinh R, nước và leo thang. Không sao chép
  controller thành một bộ thông số khác. Art hiện có giữ nguyên; terrain khối màu.

Kiểm tra (thay `godot` bằng đường dẫn executable4.7.2 nếu cần):

```sh
python3 tools/export_layout_json.py --check
godot --headless --path prototype --editor --import --quit
godot --headless --path prototype --script res://tests/smoke.gd
godot --headless --path prototype --script res://tests/classic_headless.gd
godot --headless --path prototype --script res://tests/rig_smoke.gd
godot --headless --path prototype --script res://tests/dao_uc_checks.gd
python3 tools/check_layout.py design/maps/lay_dao_uc_v1.md
python3 tools/check_layout.py design/maps/lay_dao_uc_boss_v1.md
```

`classic_checks.gd` hiện là RefCounted được gọi trong smoke; `classic_headless.gd`
chỉ bọc để chạy riêng nguyên bộ kiểm đó qua CLI. Có thể thêm `--fixed-fps 60`
để chạy headless nhanh với cùng bước mô phỏng60Hz; không dùng cho đo FPS thiết bị.
Test Đào Úc đi tuyến S→E→lũy bằng Input thật, lệnh nhảy tìm chướng ngại từ lưới;
chỉ đặt vị trí khi bắt đầu các fixture thử hố/chông/nước/thang/bục, không teleport
để vượt tuyến bắt buộc. Việc headless PASS không phải tôi đã thử Realme.

Sau chơi thử quyết thêm tầng bục2–3 và khe không đáy hay đáy nông. Lượt tileset
sau cần mặt cắt lũy/rễ/đá cho phần đất gần nửa dưới màn hình. Prototype này là mã
bỏ đi, không đưa sang `co_lau_game`, không duyệt Mốc A1 hoặc đánh dấu[x].


### Follow-up HUD trên sau chơi thử (29/10/2026)

Người dùng chấp nhận bản thử khối màu, **chưa duyệt chính thức**, UI thật làm sau.
SCR-05 giữ minimap120×80. SCR-06 chọn **A: ẩn minimap**, giữ neo menu/⚙ A0;
hiện khung thanh boss360×32 ởy24, căn giữa (gồm cả tên, Tạm thời, chưa có HP/AI).
HUD thật trong scene được so hình chữ nhật với checker ở960/1200.

Ẩn minimap riêng chưa đủ vì menu/⚙ còn che lính trên lũy; người dùng cho phép
hạ mặt lũy từ160→224 px. Còn hai bậc32 px, đúng4 lính và sân phẳng640 px.
Lính cung map thường c106 chuyển r4→r6, đứng trên bục dưới, các bục/thang còn lại
giữ nguyên. Checker xét hình96px (boss132), khác với hitbox88px, bỏ qua nhãn gỡ lỗi.
Ảnh phủ nút/HUD và JSON đều dựng lại từ cùng bố cục/cấu hình mới.
