# Danh sách chốt thiết kế

Có hai mốc, mỗi mốc một danh sách. Codex không tự đánh dấu mục nào; chỉ đánh dấu khi người dùng nói đã duyệt. Sau khi qua một mốc, mọi thay đổi thiết kế phải ghi vào `docs/05_log.md` kèm lý do.

- **Mốc A — Trước khi code:** duyệt toàn bộ thiết kế gameplay, giao diện, bản đồ, nhân vật, hoạt ảnh và mọi quy tắc ảnh hưởng tới trải nghiệm. Qua mốc A mới mở thư mục code.
- **Mốc B — Trước khi phát hành:** hồ sơ pháp lý, cách xác định tuổi, bảng giá thương mại, thanh toán thật, kiểm tra quyền sử dụng tài nguyên.

Chuyển phần pháp lý sang mốc B không có nghĩa là bỏ qua. Nếu yêu cầu pháp lý buộc thay đổi một quy tắc đã chốt ở mốc A (ví dụ cách giới hạn giờ chơi, hay luồng nạp), thì sửa thiết kế, ghi nhật ký, và duyệt lại phần bị ảnh hưởng.

## Quyết định đã chốt (28/10/2026)

Các quyết định dưới đây người dùng đã đồng ý; tài liệu đã cập nhật theo. Đây không phải mục chờ duyệt.

- Phong cách mặc định là pixel art chibi; xác nhận lần cuối sau khi xem ba ảnh P0.
- Không có hồi sinh tại chỗ. Thua thì về điểm hồi sinh; trong trận boss có nút "Đánh lại".
- Thêm SCR-14 Bản đồ vùng, cho đi nhanh miễn phí tới làng, căn cứ và điểm hồi sinh đã mở.
- SCR-22 Căn cứ Hoa Lư có 4 công trình, mỗi công trình 3 cấp, không có thời gian chờ xây. Lợi ích: trại lính (tướng đi cùng mạnh hơn), kho lương (tăng lương thảo tối đa), chuồng ngựa (tặng thức ăn thú), lò rèn (giảm phí rèn 5%, 10%, 15%). Chi phí vật liệu và các con số khác chưa chốt.
- Toàn bộ gameplay chơi offline. Đăng nhập Google luôn tùy chọn; chỉ hỏi khi người chơi chủ động nạp, dùng ngân phiếu nạp hoặc bật sao lưu, và luôn có nút "Để sau".
- Ngân phiếu có hai nguồn: ngân phiếu thưởng (nhận và tiêu offline), ngân phiếu nạp (máy chủ quản lý). Trừ thưởng trước, nạp sau. Giao dịch kết hợp do máy chủ xác nhận, có mã giao dịch chống trừ hai lần (`12_ngan_phieu.md`).
- Bản phát hành đầu tiên chỉ bán món vĩnh viễn qua Google Play (gói khởi đầu, đồ thời trang, thú cưỡi ngoại hình, túi da cấp 3), không có ngân phiếu nạp và không có máy chủ riêng. Món đã mua thuộc tài khoản Google Play và dùng được ở cả ba ô. Thiết kế ngân phiếu nạp giữ lại cho bản sau (`12_ngan_phieu.md`, mục 0 và 12).
- Engine Godot 4 với GDScript. Có kế hoạch chuẩn bị chuyển online nhưng chưa làm phần online (`14_online_migration.md`).
- Hoàn tiền: số dư nạp được âm, khóa giao dịch dùng ngân phiếu nạp cho tới khi bù xong; không thu hồi món đã mua, không khóa gameplay; sổ giao dịch chống áp dụng hoàn tiền hai lần.

## Mốc A — Trước khi code

### 1. Phong cách và nhân vật chính

- [ ] Xác nhận phong cách sau P0 và khối STYLE cuối cùng.
- [ ] Bảng màu 32 màu đã chốt và lưu thành file palette (`art/reference/palette.png` và `.gpl` hoặc `.ase`).
- [ ] Ảnh gốc Đinh Bộ Lĩnh và bảng tách lớp đã duyệt.
- [ ] Đủ 7 bậc trang bị, cả bản cầm đao và cầm cung.
- [ ] Bảng động tác phái Đao và phái Cung ở bậc 1, đủ động tác trong `09_animation_spec.md`.
- [ ] Một bộ sprite chuẩn đã chỉnh tay đúng kích thước làm mẫu cho mọi sprite sau.

### 2. Thế giới

- [ ] Concept đủ nhân vật đồng minh và NPC có tên trong GDD.
- [ ] Concept đủ quái của 5 vùng và quái giữ ải.
- [ ] Concept đủ 11 boss, đúng màu cờ thế lực.
- [ ] Ba thú cưỡi có cả bản gắn trang bị.
- [ ] Cảnh nền và tileset đủ 29 bản đồ.

### 3. Bản đồ chơi được

- [ ] File bố cục và ảnh dựng bằng script cho đủ 29 bản đồ, đã qua mục tự soát trong `08_map_layout.md`.
- [ ] Đấu trường của 11 boss có bố cục khớp cơ chế từng boss.
- [ ] Số đo di chuyển đã chốt; nếu đổi, mọi bố cục đã soát lại.
- [ ] Bản đồ vùng (SCR-14) của 5 vùng, có đánh dấu các điểm dịch chuyển.

### 4. Giao diện

- [ ] Bộ khung giao diện đã duyệt.
- [ ] Mockup và đặc tả đủ 22 màn trong `06_screens.md`.
- [ ] Mockup riêng cho các trạng thái khác bố cục của bản đầu, gồm SCR-13 thẻ Gói (mất mạng, đang chờ Google Play, đã sở hữu).
- [ ] Bộ biểu tượng vật phẩm đủ cho mọi vật phẩm trong GDD.
- [ ] Font tiếng Việt đã chọn.

### 5. Luồng tương tác

- [ ] Đủ các luồng của bản đầu trong `07_ui_flow.md` (F1 đến F3, F5 đến F8, nhánh ngân phiếu thưởng của F9, F11, F13), đã qua mục tự soát.
- [ ] Mỗi luồng có nhánh mất mạng đều giữ đúng nguyên tắc offline (không nhánh nào chặn gameplay).

### 6. Hoạt ảnh và hiệu ứng

- [ ] Đặc tả hoạt ảnh cho mọi nhân vật, quái, boss, thú cưỡi đã duyệt.
- [ ] Hiệu ứng cơ bản và hiệu ứng 20 chiêu đã có concept.
- [ ] Hoạt ảnh giao diện (búa rèn, số sát thương, sao giữ ải, dựng công trình căn cứ) đã duyệt.

### 7. Câu chuyện

- [ ] Storyboard đủ 25 cutscene trong `10_storyboard.md`.
- [ ] Tranh cutscene của Hồi 1 đã duyệt.
- [ ] Bảng nhịp nhiệm vụ đủ 5 hồi.
- [ ] Lời thoại ít nhất cho mở đầu và Hồi 1.

### 8. Quy tắc nghiệp vụ

- [ ] Quy tắc trong `12_ngan_phieu.md` cho bản đầu đã duyệt: mục 1 đến 4 (phần ngân phiếu thưởng), mục 10, mục 12.
- [ ] Các con số căn cứ Hoa Lư (vật liệu mỗi cấp, mức tăng tướng, lương thảo, thức ăn thú) đã chốt cùng bản cân bằng kinh tế.

### 9. Thông số và tài liệu nguồn

- [ ] Mọi thông số trong `13_thong_so.md` ở trạng thái **Đã duyệt**, hoặc được người dùng chấp nhận giữ **Tạm thời** kèm điều kiện chốt.
- [ ] `docs/GDD.md` của bản kit đang dùng khớp với các tài liệu `docs/06` đến `docs/14`; mọi chỗ mâu thuẫn đã sửa ở cả hai bên.
- [ ] Quy ước id và phân loại logic trong `14_online_migration.md` đã duyệt; danh sách hạng mục và dữ liệu mẫu dùng đúng quy ước id.

## Mốc B — Trước khi phát hành

- [ ] Hồ sơ cung cấp dịch vụ trò chơi điện tử theo quy định hiện hành, có ý kiến luật sư (xếp loại bản đầu: game tải về có thanh toán qua Google Play, không có máy chủ riêng).
- [ ] Cách xác định tuổi và giới hạn giờ chơi cho người dưới 18 tuổi (SCR-21); nếu luật sư yêu cầu khác thiết kế hiện tại thì quay lại sửa và duyệt lại.
- [ ] Giá các món vĩnh viễn bán bằng tiền thật.
- [ ] Thanh toán Google Play cho món vĩnh viễn chạy thật: mua, xác nhận đơn, khôi phục, thanh toán đang chờ, hoàn tiền.
- [ ] Nhân vật chính, 11 boss và logo đã được vẽ lại hoặc chỉnh tay đáng kể.
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

Khi qua mỗi mốc, người dùng ghi vào cuối file này: ngày, phiên bản các tài liệu, và một câu "Đã qua mốc A" hoặc "Đã qua mốc B".
