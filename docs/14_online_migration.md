# Kế hoạch chuẩn bị chuyển sang online

Cờ Lau Khởi Nghĩa phát hành trước dưới dạng game offline. Định hướng lâu dài là có thể chuyển thành game online thuộc thể loại nhập vai mobile khi có nguồn lực. Tài liệu này **không** yêu cầu làm phần online bây giờ: không viết máy chủ game, không chọn ngôn ngữ hay dịch vụ máy chủ (Golang, Supabase hay thứ khác). Nó chỉ quy định những gì bản offline phải làm ngay từ đầu để sau này chuyển được mà không phải viết lại game.

Thiết kế hình ảnh, màn hình và bản đồ trong Design Kit không cần đổi vì tài liệu này. Phần ảnh hưởng chủ yếu nằm ở dữ liệu và code, nên các quy tắc dưới đây được kiểm ở mốc A (cho dữ liệu và kiến trúc) và áp dụng khi code.

## 1. ID ổn định

Mọi thứ có trong dữ liệu game mang một **id dạng chữ, không bao giờ đổi**, kể cả khi đổi tên hiển thị, đổi hình hay đổi chỉ số. Không dùng số thứ tự trong mảng làm id.

| Loại | Mẫu id | Ví dụ |
|---|---|---|
| Vật phẩm mẫu | `itm_<nhóm>_<tên>` | `itm_dao_t1`, `itm_da_mai_05`, `itm_bua_bao_ho_so` |
| Kỹ năng | `skl_<phái>_<tên>` | `skl_dao_tram_dao`, `skl_cung_xa_tien` |
| Nhiệm vụ | `qst_<số ba chữ số>` | `qst_014` |
| Bản đồ | `map_<tên>` | `map_dao_uc`, `map_ai_tam_diep` |
| Quái và boss | `mob_<tên>`, `bos_<tên>` | `mob_tho_phi`, `bos_hau_ngo_tien_phong` |
| NPC | `npc_<tên>` | `npc_nguyen_bac` |
| Cửa hàng, công trình | `shp_<tên>`, `bld_<tên>` | `shp_tho_ren_hoa_lu`, `bld_lo_ren` |
| Sản phẩm Google Play | `sku_<tên>` | `sku_goi_khoi_dau`, `sku_ngua_o` |
| Quyền lợi trong game | `ent_<tên>` | `ent_tui_da_3`, `ent_np_thuong_khoi_dau` |

Id sản phẩm Google Play đặc biệt quan trọng: Google không cho dùng lại id của một sản phẩm đã tạo, nên đặt sai thì phải tạo sản phẩm mới. Cách sản phẩm ánh xạ sang quyền lợi ở `12_ngan_phieu.md`, mục 12.

Mã tài nguyên trong `02_asset_list.md` (ví dụ `enm_tho_phi`, `bos_hau_ngo_tien_phong`) dùng cùng phần tên, để từ id dữ liệu tìm ra hình dễ dàng.

Ngoài id mẫu, cần thêm hai loại id cho từng bản thể:

- **Định danh ô nhân vật:** đã có từ v2.2, tạo lúc bấm Chơi mới, không bao giờ dùng lại. Sau này đây là gốc để sinh id nhân vật online.
- **Id từng món trang bị:** mỗi món trang bị (vũ khí, giáp, trang sức) khi sinh ra có một id riêng, lưu cùng cấp cường hóa và dòng chỉ số. Đồ xếp chồng như đá, thuốc thì không cần. Id này cho phép sau này truy vết một món đồ, cần cho giao dịch và chống gian lận khi online.

## 2. Luật chơi tách khỏi cảnh và giao diện

Kiến trúc ba lớp ở GDD Phần 6 đã tách lớp hệ thống khỏi cảnh Godot. Để chuyển online được, lớp hệ thống còn phải theo thêm ba quy tắc:

- **Mọi thay đổi trạng thái đi qua lệnh.** Giao diện và cảnh không sửa thẳng dữ liệu nhân vật; chúng gửi một lệnh (ví dụ "cường hóa món X với các đá Y ở chế độ Z", "mua món A ở cửa hàng B", "trả nhiệm vụ C") cho lớp hệ thống, rồi nhận về kết quả và sự kiện để vẽ. Khi online, chính các lệnh này được gửi lên máy chủ.
- **Luật là hàm của dữ liệu đầu vào.** Hàm tính sát thương, tỉ lệ cường hóa, rơi đồ chỉ đọc dữ liệu được truyền vào và bộ sinh số ngẫu nhiên được truyền vào, không đọc trạng thái toàn cục hay node. Như vậy cùng một luật có thể chạy ở máy để dự đoán và ở máy chủ để quyết định.
- **Không dựa vào thời gian máy.** Đồng hồ điện thoại có thể bị chỉnh. Những gì phụ thuộc thời gian (ví dụ thẻ tháng nếu sau này có) phải tính được theo thời gian máy chủ.

## 3. Phiên bản dữ liệu và chuyển đổi

- File lưu có `save_version`; dữ liệu game (12 nhóm JSON) có `data_version`.
- Mỗi lần đổi cấu trúc file lưu, viết một hàm chuyển đổi từ phiên bản trước sang phiên bản sau. Game chạy lần lượt các hàm cho tới phiên bản mới nhất khi mở một file cũ.
- Giữ một bộ file lưu mẫu của từng phiên bản trong `res://tests/`, và test tự động mở được tất cả.
- Không xóa id khỏi dữ liệu. Món hay nhiệm vụ không dùng nữa thì đánh dấu ngừng dùng, để file lưu cũ vẫn đọc được.

## 4. Logic nào sau này phải lên máy chủ

Phân loại này giúp viết code bây giờ sao cho phần cần lên máy chủ nằm gọn trong lớp hệ thống.

| Nhóm | Bản offline | Khi online |
|---|---|---|
| Hiển thị, âm thanh, hoạt ảnh, điều khiển, camera | Máy | Máy |
| Di chuyển nhân vật | Máy | Máy dự đoán, máy chủ kiểm tra |
| Va chạm và sát thương PvE | Máy | Máy chủ quyết định hoặc kiểm tra; máy dự đoán để mượt |
| Rơi đồ, kinh nghiệm, lên cấp | Máy | Máy chủ |
| Cường hóa, luyện đá, tách, tinh luyện và số ngẫu nhiên của chúng | Máy | Máy chủ |
| Tiền đồng, ngân lượng, ngân phiếu thưởng | Máy | Máy chủ |
| Quyền sở hữu món đã mua | Google Play quản lý; máy lưu món nào đã được cấp cho ô nào | Máy chủ xác minh với Google Play và quản lý |
| Ngân phiếu nạp, giao dịch nạp | Không có ở bản đầu | Máy chủ |
| Mua bán ở NPC, cửa hàng ngân phiếu | Máy (ngân phiếu thưởng) | Máy chủ |
| Tiến độ nhiệm vụ, cờ cốt truyện, căn cứ, giữ ải | Máy | Máy chủ |
| Lưu game | File trên máy, sao lưu tùy chọn | Máy chủ |

## 5. Chuyển nhân vật offline sang online

**Nguyên tắc: không mặc định tin dữ liệu file lưu**, vì file lưu do người chơi giữ và sửa được (GDD Phần 6, mục 3). Khi có bản online, những gì được chuyển sang chia làm hai nhóm:

- **Chuyển sau khi xác minh lại:** quyền sở hữu món vĩnh viễn đã mua qua Google Play (thời trang, thú cưỡi ngoại hình, túi da, gói khởi đầu). Máy chủ online kiểm tra lại từng đơn hàng với Google Play; đơn còn hiệu lực thì cấp quyền lợi cho tài khoản online. Không dùng danh sách món trong file lưu làm căn cứ.
- **Không chuyển nguyên vẹn:** cấp, đồ, tiền trong game, tiến độ cốt truyện. Cách xử lý cụ thể chốt khi làm bản online. Đề xuất hiện tại là nhân vật online bắt đầu mới, nhận một phần thưởng ghi nhận (danh hiệu, đồ thời trang riêng) theo các mốc cốt truyện đã đạt, có giới hạn hợp lý.

Bản đầu không có máy chủ riêng, nên không có gì để chuyển từ máy chủ cũ. Google Play là nơi giữ quyền sở hữu; bản offline chỉ cần dùng đúng id sản phẩm và id quyền lợi theo mục 1 để bản online xác minh lại được. Nếu trước bản online có một bản cập nhật bật ngân phiếu nạp (mốc C), máy chủ của bản đó trở thành nguồn cho số dư ngân phiếu nạp khi chuyển.

## 6. Pháp lý khi chuyển online

Chuyển sang online nhiều người chơi thường đổi cách xếp loại dịch vụ trò chơi điện tử và đổi yêu cầu giấy phép, nên phải hỏi lại luật sư trước khi làm. Nếu bản online có giao dịch vật phẩm giữa người chơi, cần kiểm tra quy định hiện hành về mua bán vật phẩm ảo giữa người chơi (Nghị định 147/2024 có điều khoản về việc này). Đây là việc của giai đoạn online, không ảnh hưởng thiết kế bản offline.

## 7. Kiểm ở mốc A

- Mọi file dữ liệu và mọi hạng mục trong `02_asset_list.md` có id theo mục 1.
- Đặc tả lớp hệ thống (khi viết ở đầu giai đoạn code) liệt kê đủ các lệnh theo mục 2.
- File lưu có `save_version`, dữ liệu có `data_version`.
