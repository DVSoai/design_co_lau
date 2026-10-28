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

Viewport 960×540, canvas_items, scale số nguyên, texture nearest.
Đổi kích thước cửa sổ để thử viền trống tại kích thước không chia hết;
màn hình nhỏ hơn viewport vẫn cần kiểm tra độ đọc trên thiết bị.
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
   keytool -keygenpair -keystore debug.keystore -alias androiddebugkey -keyalg RSA -keysize 2048 -validity 10000 -storepass android -keypass android -dname "CN=Android Debug,O=Android,C=US"
   ```

   Chọn file đó trong Android Debug Keystore của editor, user `androiddebugkey`,
   password `android`. Đây chỉ là khóa thử; không dùng phát hành, không commit keystore.
5. **Project → Export → Add → Android**. Đặt package duy nhất, ví dụ
   `org.colau.a0prototype`; orientation **Landscape**; bật arm64-v8a
   (thêm armeabi-v7a nếu thiết bị cần). Giữ Compatibility, tắt Gradle build.
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
   và độ đọc của nhân vật 96 px. Có thể nối bàn phím gửi F1 để xem debug.
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
không có lỗi Godot; smoke test 11 kiểm tra PASS, `A0 smoke failures: 0`.
Binary Linux 4.7.2 đã được đối chiếu SHA-512 với manifest chính thức.
