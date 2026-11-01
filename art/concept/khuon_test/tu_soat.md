# Thử khuôn tư thế — hai khung, chưa duyệt

Nhánh `test/khuon-tu-the` tạo từ `origin/main` tại `a24ffca` (01/11/2026). Chỉ thêm concept và phần cuối nhật ký. Bộ Lv1 dùng làm mẫu là bản đã commit `769be38`, lấy từ ảnh ghép Godot thật; không dùng bản đổi tỉ lệ chưa commit. Không đổi prototype hoặc bộ Lv1.

Mỗi khung đã tạo **3 lần**, chọn **v3**. Không tạo thêm sau hạn mức. Ảnh PNG tạo ra giữ nguyên; prompt từng lần lưu nguyên văn cạnh ảnh. `selected.json` ghi lựa chọn, không phải phê duyệt.

Ảnh so: `so_sanh.png`, 1200×800. Hàng trên khung00, hàng dưới khung04; mỗi hàng từ trái sang phải: **khuôn | concept mới chụp trong Godot | Lv1 hiện tại chụp trong Godot**. `so_sanh_hai_huong.png` bổ sung hướng trái ở nửa dưới. Mọi ô chuẩn hóa cùng chiều cao người256px bằng bản1× rồi phóng NEAREST2×; không thêm chữ, vẽ bù hay sửa pose trong ảnh so.

## Sáu câu B5 — bản chọn v3

| Câu tự soát | Khung00 | Khung04 |
|---|---|---|
| 1. Dáng khớp khuôn: đầu/thân/chân/vũ khí đúng chỗ? | **Không.** Đầu lớn hơn bản cũ nhưng thân/tay còn hẹp hơn mảng xanh; bố cục các lớp chưa trùng khuôn. | **Không.** Đầu còn tiến ra trước; thân hẹp, chân co và vị trí kiếm chưa trùng các mảng của khuôn. |
| 2. Thấy đủ hai bàn chân? | **Có.** Hai giày tách nhau, cùng chạm đất. | **Có.** Một bàn chân co sau và một phía trước, đều đọc được. |
| 3. Đầu đúng trên cổ áo, không hở hoặc lòi cổ? | **Có** qua quan sát ảnh ghép. | **Có** qua quan sát ảnh ghép. |
| 4. Nắm tay bọc chuôi; vũ khí đúng hướng, trên thân, rõ? | **Có** ở v3: thấy nắm tay và cẳng tay gập; kiếm chéo xuống sau, phủ trên áo. | **Có** ở v3: đã vẽ rõ khuỷu/cẳng tay nối vai tới nắm tay. Bản v2 bị lỗi tay gần như mất, người dùng đã chỉ ra; v2 không được chọn. |
| 5. Kích thước kiếm/cung giống tham khảo, to bản/cong, không que/gậy? | **Có** về cách đọc thị giác: lưỡi to bản, sáng, viền rõ và chiều dài gần khuôn. Chưa phải nghiệm thu kích thước từng lớp. | **Không.** Lưỡi to bản và rõ, nhưng chiều dài/độ phủ của cả hình kiếm vẫn nhỏ hơn mảng vàng khi đặt cùng chiều cao người. |
| 6. Cùng mặt/tóc/áo/màu với Lv1? | **Có.** Giữ búi tóc đen, dải đỏ, mặt nghiêm, áo nâu viền kem, đai, quấn cổ tay, giày nâu. | **Có.** Cùng thiết kế và vật liệu; bỏ vệt đỏ/chi tiết nhọn thừa cạnh má của v2. |

Đây là đánh giá thị giác của **hai concept đủ người**, không phải test khớp cổ/grip1px hay nghiệm thu rig nhiều lớp.

## Nhận xét từng lượt

- Khung00 v1: giữ thiết kế, hai chân và tay cầm đọc được; đầu nhỏ và người dài, lệch khuôn. v2: đầu lớn hơn, thân/chân gọn hơn; thân còn hẹp. v3: tốt nhất về tổng thể, tay rõ hơn; vẫn chưa bám toàn bộ khuôn.
- Khung04 v1: sải rộng theo ảnh Lv1 cũ, không phải bước co chân của khuôn. v2: bước co và đầu lớn tốt hơn, nhưng chỉ thấy nắm tay sát má, cẳng tay bị mất/che; có chi tiết đỏ/nhọn thừa cạnh má. v3: tay nối rõ, bỏ chi tiết thừa và giữ bước co; vị trí các mảng và kích thước kiếm vẫn chưa khớp.

Khuôn giúp công cụ tiến gần tỉ lệ và bước chạy mong muốn qua từng lượt, nhưng **chưa kiểm chứng được khả năng giữ chính xác cả bốn lớp**. Không áp kết quả này cho toàn bộ Lv1 và không tự duyệt ảnh. Đã đủ hạn mức3lần/khung.

## Prompt nguyên văn và nguồn đính kèm

- `khung_00_v1.prompt.txt`, `khung_00_v2.prompt.txt`, `khung_00_v3.prompt.txt`.
- `khung_04_v1.prompt.txt`, `khung_04_v2.prompt.txt`, `khung_04_v3.prompt.txt`.
- Cả ba lượt đều đính kèm khuôn đúng khung, ảnh Lv1 hiện tại và bảng trang bị. V1 còn đính kèm bảng hoạt ảnh và ảnh nhân vật gốc; v2 chỉ ba ảnh chính để giảm ảnh hưởng của pose cũ; v3 thêm bản v2 tương ứng để sửa tay/chi tiết thừa.
- Khuôn/ảnh tham khảo gốc được đọc trong thư mục tạm, không chép ảnh gốc vào nhánh. Hai ô Lv1 hiện tại lấy từ render đầy đủ lớp ở commit `769be38`.

`compare.py`, `render_preview.gd` và các JSON phép đo ghi lại quy trình ghép từ file thật. Godot preview là dự án tạm ngoài repo; không sửa prototype. Các ảnh Godot ở cả hai hướng được giữ để kiểm lại.
