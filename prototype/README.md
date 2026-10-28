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
8. Mở app ở hướng ngang. Bốn nút tạm **trái, phải, nhảy, chém** chỉ hiện trên
   màn hình cảm ứng; thử giữ trái/phải đồng thời bấm nhảy/chém bằng ngón thứ hai.
   Nút dùng TouchScreenButton để giữ action theo từng ngón.
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
không có lỗi Godot; smoke test hiện tại 59 kiểm tra PASS, `A0 smoke failures: 0`.
Binary Linux 4.7.2 đã được đối chiếu SHA-512 với manifest chính thức.

## Bảng chỉnh khi chạy

Nút **⚙** ở góc trên phải luôn hiện trên PC và cảm ứng. Bấm để mở/đóng
bảng; cuộn để xem đủ 10 thanh trượt. Mỗi thanh hiện tên, số và đơn vị.
Các thay đổi tác dụng ngay cho chạy/gia tốc, nhảy, camera và nhịp chém;
trọng lực/vận tốc nhảy tự tính lại. Giữ ATTACK_DURATION tối thiểu 0,22 s
để cửa sổ trúng [0,10; 0,20) s vẫn nằm trong động tác.
Nút **Sao chép** đưa toàn bộ thông số hiện tại, kể cả trọng lực/vận tốc nhảy,
vào clipboard hệ điều hành (cần chạy có màn hình; headless chỉ kiểm tra nội dung).
Giá trị chỉ nằm trong bộ nhớ, khởi động lại sẽ lấy mặc định từ tuning.gd;
không lưu hoặc ghi đè file cấu hình.

Mặc định RUN_SPEED=200 px/s, TIME_TO_APEX=0,38 s: tầm nhảy ngang lý thuyết
200 × 2 × 0,38 = **152 px**, lớn hơn 1,5 × hố 96 px = **144 px**.
Đây là tầm lý thuyết khi đã đạt tốc độ chạy, cùng cao độ cất/hạ cánh;
không bảo đảm nhảy từ đứng yên. Smoke test assert điều kiện này từ hình học hố thật.

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
định, không chỉnh thông số. Kết quả được ghi trong `docs/13_thong_so.md` và
`docs/05_log.md`: vẫn Tạm thời, chờ thử Android và xác nhận của người dùng.

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
