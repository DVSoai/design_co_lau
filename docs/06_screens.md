# Thiết kế màn hình và trạng thái giao diện

Tài liệu này liệt kê mọi màn hình của game, mỗi màn hình có mục đích, đường vào ra, bố cục, thành phần, các trạng thái và chữ hiển thị. Bố cục gốc lấy từ Phần 5 của `GDD.md`; tài liệu này chi tiết hóa và thắng GDD khi có khác biệt.

Mỗi màn hình cần hai sản phẩm thiết kế: **mockup hình ảnh** tạo bằng khuôn P13 (mã `ui_<tên>`), và **đặc tả** lưu ở `design/screens/scr_<số>_<tên>.md` theo mẫu ở cuối tài liệu. Mockup cho thấy trông như thế nào; đặc tả cho thấy hoạt động ra sao. Cả hai phải khớp nhau.

## Quy ước chung

**Khung tọa độ.** Mọi số đo tính trên độ phân giải gốc 960×540 (điện thoại nằm ngang), gốc tọa độ ở góc trên bên trái. Quy ước chung ngoài HUD chừa vùng an toàn 16 điểm ảnh ở hai cạnh; riêng HUD trong trận theo chuẩn A0 bên dưới, lề nút ít nhất 24 px logic và neo theo viewport thực. Khi dựng mockup phải soát tai thỏ và bo góc màn hình.

**Cỡ chạm.** Ngoài HUD, cỡ chạm nhỏ nhất 20×20 còn là đề xuất. Riêng nút đánh, di chuyển, kỹ năng và bình trong trận dùng kích thước đã chốt ở mục HUD chuẩn từ A0, thay cho bộ 56/32/28 px cũ.

**Chữ.** Dùng một font có đủ dấu tiếng Việt, cỡ tối thiểu 8 điểm ảnh gốc cho chữ phụ và 10 cho chữ chính. Không đặt chữ trong ảnh; mockup dùng thanh giữ chỗ.

**Trạng thái dùng chung cho mọi nút và ô:** bình thường, đang chạm (sáng lên, lún 1 điểm ảnh), vô hiệu (xám, chạm vào hiện lý do), được chọn (viền vàng), có thông báo (chấm đỏ góc trên phải).

**Trạng thái dùng chung cho mọi màn có dữ liệu:** đang tải (biểu tượng bông lau xoay), trống (hình minh họa nhỏ và một dòng hướng dẫn), lỗi (thông báo và nút thử lại), mất mạng (chỉ ở những phần cần mạng: nạp, giao dịch dùng ngân phiếu nạp, sao lưu; phần còn lại của màn vẫn dùng được).

**Nguyên tắc offline:** không màn nào được chặn người chơi vì mất mạng, trừ đúng các nút nạp, dùng ngân phiếu nạp và sao lưu (`12_ngan_phieu.md`, mục 1).

**Màu hiếm của vật phẩm** (viền ô): thường xám #8A8F98, tốt xanh #5E9441, hiếm lam #2E4FA3, quý tím #6B4A8C, dấu ấn sứ quân vàng #D9A520.

## HUD trong trận (chuẩn từ A0)

**Đã duyệt (A0, 28/10/2026)** về bố cục và thao tác, theo thử Android trên
Realme RMX3760 (1600×720), Godot 4.7.2, commit `7973729`.
Áp dụng cho SCR-05 và nền bố cục của SCR-06/SCR-07. Khung thiết kế 960×540,
`canvas_items`, `expand`, `fractional`, nearest; viewport thực rộng 960–1200 px
logic. Android dùng fullscreen + immersive. Không đặt vị trí dựa vào độ rộng 960
cố định; cập nhật neo góc theo viewport khi đổi kích thước.

| Cụm | Bố cục và thao tác đã chốt |
|---|---|
| Trái | Chỉ 3 nút nhìn thấy ←, → và ↑ nhảy. Với d=84 px: ← ở (x0, lower_y), → ở (x0+2,2d, lower_y), ↑ ở (x0+1,1d, lower_y−1,35d). Hai vùng chéo vô hình, rộng 0,9d, cao d, cùng hàng ↑ và sát hai mép bên ↑ |
| Bắt chạm cụm trái | Ưu tiên ↑ > vùng chéo > ←/→. Vùng chéo giữ hướng và nhảy, cùng sáng ↑ và nút hướng; vuốt giữa vùng và đa chạm không làm nhả action của ngón khác. Chỉ bản debug mới hiện viền vùng chéo |
| Phải | CHÉM tròn đường kính 1,4d=117,6 px ở góc dưới phải; đổi mục tiêu tròn ở trên; bình máu ở trên-trái, bình nội lực bên trái CHÉM. Nút nhỏ 0,65d=54,6 px, có số đếm bình |
| Giữa đáy | 5 ô kỹ năng vuông cạnh 0,7d=58,8 px, cách nhau 6 px, căn giữa theo viewport |
| Trên trái | Vòng cấp độ, thanh máu đỏ và thanh nội lực xanh; trong A0 là các khối giữ chỗ |
| Trên phải | Menu và bản đồ nhỏ 120×80 px logic. Nút chỉnh ⚙ của prototype tối thiểu 56×56; là công cụ thử, không mặc định trở thành nút của HUD sản phẩm |
| Lề và chữ | Cách mép viewport ít nhất 24 px logic; chữ/mũi tên nút ít nhất 22 px logic. Khi chạm: viền sáng hơn, hình nút scale 0,95; vùng bắt chạm không co |

Kiểu cổ điển và khinh công là chuẩn di chuyển, xem `13_thong_so.md`.
Giữ để nhảy lại bật, giữ lâu nhảy cao tắt. HUD ẩn/hiện trong A0 chỉ để so diện tích
cảnh; chức năng game của menu, bình, kỹ năng, bản đồ nhỏ còn phải đặc tả/duyệt ở
Mốc A. Không coi việc chấp nhận các khối placeholder là duyệt hình nút thành phẩm.

**Hình nút sẽ vẽ riêng theo phong cách Việt**, phù hợp art bible: chất liệu gỗ,
tre, viền đồng; có thể dùng hoa văn trống đồng làm ví dụ hướng trang trí.
Không dùng ảnh, biểu tượng hay mã của game khác. Chữ giao diện do game vẽ bằng
font, không chèn chữ vào ảnh asset. Mockup thành phẩm vẫn phải duyệt riêng.

## Danh sách màn hình

### SCR-01 Màn khởi động

- **Mục đích:** hiện logo, nạp dữ liệu lần đầu, kiểm tra giao dịch nạp còn treo.
- **Bố cục:** nền tối, logo giữa màn, thanh tải mảnh dưới logo, dòng cảnh báo sức khỏe nhỏ sát đáy (theo yêu cầu pháp lý ở Phần 6 GDD).
- **Trạng thái:** đang tải; lỗi dữ liệu (nút "Thử lại"); có giao dịch treo đã cộng (thông báo nhỏ khi vào màn sau).
- **Ra tới:** SCR-02.

### SCR-02 Chọn ô nhân vật

- **Mục đích:** chọn một trong ba ô để chơi tiếp, chơi mới hoặc xóa.
- **Bố cục:** ba thẻ dọc xếp ngang giữa màn (mỗi thẻ 160×240). Góc trên phải: nút Cài đặt. Góc trên trái: nút tài khoản Google (chỉ hiện khi đã đăng nhập).
- **Thẻ có dữ liệu:** hình Đinh Bộ Lĩnh mặc đồ hiện tại, phái (hoặc "Chưa chọn phái"), cấp, hồi đang chơi, tổng giờ chơi, lần chơi cuối, nút "Chơi tiếp", nút xóa nhỏ góc thẻ.
- **Thẻ trống:** khung mờ, nút "Chơi mới" lớn.
- **Trạng thái:** thẻ đang chọn (sáng, nhân vật thở); xác nhận xóa lần 1 ("Xóa ô này? Không khôi phục được"); xác nhận xóa lần 2 (gõ chữ XOA hoặc giữ nút 2 giây), có dòng đỏ ghi số ngân phiếu và ngân lượng sẽ mất; file lưu hỏng (thông báo đã khôi phục bản sao lần lưu trước); đã cấp lại món đã mua sau khi đồng bộ (thông báo nổi, xem F12).
- **Xóa ô có liên kết máy chủ** (bản có ngân phiếu nạp; bản đầu mọi ô đều chưa liên kết nên xóa luôn được; quy tắc ở `12_ngan_phieu.md`, mục 9):
  - Ô có ngân phiếu nạp hoặc giao dịch đang chờ, khi offline: nút xóa vô hiệu, dòng "Cần kết nối để xóa ô có ngân phiếu nạp".
  - Ô có ngân phiếu nạp, khi có mạng: hộp xác nhận lần 2 hiện số dư thật từ máy chủ.
  - Ô đã liên kết, số dư nạp bằng 0, khi offline: xóa được; sau khi xóa, vị trí trống hiện nút "Chơi mới" và một nhãn nhỏ "Đang chờ đồng bộ xóa ô cũ".
  - Máy chủ từ chối xóa vì ô còn ngân phiếu nạp: hộp thông báo với hai nút "Khôi phục ô" và "Xóa hẳn" (ghi số dư thật).
- **Ra tới:** cutscene CS01 (chơi mới) hoặc vị trí cuối của ô (chơi tiếp).

### SCR-03 Màn tải giữa bản đồ

- **Bố cục:** tranh nền của vùng sắp vào, tên vùng, một câu mẹo hoặc một dòng sử ngắn, thanh tải.
- **Trạng thái:** đang tải; xong (chạm để tiếp, hoặc tự vào sau 0,5 giây).

### SCR-04 Chọn phái

- **Mục đích:** chọn Đao hoặc Cung ở nhiệm vụ 10. Lựa chọn cố định cho ô nhân vật này.
- **Bố cục:** hai nửa màn. Mỗi nửa: Đinh Bộ Lĩnh cầm vũ khí phái đó đang làm động tác mẫu, tên phái, ba dòng đặc điểm (tầm đánh, hiệu ứng phụ, cách chơi), hai chiêu tiêu biểu có biểu tượng. Dưới cùng: nút "Chọn phái này" cho mỗi bên.
- **Trạng thái:** đang xem một bên (bên kia tối đi); xác nhận ("Phái không đổi được trong ô nhân vật này. Chọn phái Đao?").
- **Chữ:** "Phái Đao — cận chiến, gây choáng", "Phái Cung — tầm xa, ghim chân".

### SCR-05 Màn chơi (HUD)

- **Bố cục:** theo mục **HUD trong trận (chuẩn từ A0)**: d-pad 3 nút và 2 vùng chéo vô hình bên trái; CHÉM/đổi mục tiêu/bình bên phải; 5 ô kỹ năng giữa đáy; cấp/HP/MP trên trái, menu/bản đồ nhỏ trên phải.
- **Thành phần ngoài A0:** biểu tượng hiệu ứng, theo dõi nhiệm vụ, lên/xuống thú cưỡi, Túi đồ/Nạp, Tự đánh, kinh nghiệm và máu mục tiêu còn cần đặc tả vị trí ở Mốc A; không chen lấn các vùng điều khiển đã chốt. Bộ tọa độ cũ theo khung 640 px, cần điều khiển ảo và 6 ô chiêu vòng cung được thay bằng bố cục A0.
- **Trạng thái ô chiêu:** sẵn sàng; đang hồi (vòng quét tối và số giây); không đủ MP (xám, viền lam); chưa học (ổ khóa); bị khóa khi cưỡi trâu hoặc voi (gạch chéo).
- **Trạng thái khác:** Tự đánh bật (nút sáng, biểu tượng xoay chậm); Tự đánh bị tắt trong trận boss (nút xám); HP dưới 25% (viền màn đỏ nhịp chậm); đang cưỡi thú (đổi bộ nút); nhiệm vụ hoàn thành (dấu chấm than vàng trên ô theo dõi).
- **Thông báo nổi:** nhặt đồ (trượt từ trái, tối đa 3 dòng); lên cấp (giữa màn, hiệu ứng cột sáng); mở hệ thống mới (thẻ lớn giữa màn, chạm để đóng).

### SCR-06 Màn chơi khi đánh boss

- **Khác SCR-05:** thanh máu boss rộng ở giữa cạnh trên (tên, 2 hoặc 3 vạch chia pha); ẩn theo dõi nhiệm vụ; Tự đánh vô hiệu.
- **Trạng thái:** boss báo đòn đặc biệt (vòng đỏ trên mặt đất, biểu tượng chấm than trên đầu boss, 0,8 đến 1,2 giây); chuyển pha (màn khựng 0,3 giây, tên pha hiện ngắn); đấu danh dự (thanh máu boss có vạch 30% đánh dấu điểm kết thúc, áp dụng cho Phạm Bạch Hổ).
- **Ra tới:** SCR-15 (thua) hoặc SCR-16 (thắng).

### SCR-07 Màn chơi chế độ Giữ ải

- **Trước trận:** bảng chọn tướng đi cùng (4 thẻ: Đinh Điền, Nguyễn Bặc, Lê Hoàn, Lưu Cơ; tướng chưa theo về bị khóa), số lương thảo mang theo, số sao cao nhất đã đạt, nút "Vào trận".
- **Trong trận, khác SCR-05:** giữa cạnh trên là thanh máu cờ lau và bộ đếm đợt ("Đợt 3/8"); mũi tên đỏ ở mép màn chỉ hướng địch đang tới.
- **Giữa hai đợt (20 giây):** đồng hồ đếm ngược lớn; các ô dựng công trình phát sáng trên bản đồ; chạm ô mở bảng 4 công trình (chông tre, rào tre, chòi nỏ, trống trận) kèm giá lương thảo; nút "Bắt đầu đợt sớm".
- **Trạng thái:** cờ dưới 30% (cờ rung, viền màn đỏ); hết lương thảo (công trình xám, ghi lý do); đã đủ 4 công trình (ô dựng ẩn đi).
- **Ra tới:** SCR-17.

### SCR-08 Tạm dừng và cài đặt

- **Thành phần:** Tiếp tục; Cài đặt (âm lượng nhạc, âm lượng tiếng, rung, mức HP tự uống thuốc khi Tự đánh, chất lượng đồ họa, ngôn ngữ để sau); nút "Khôi phục món đã mua" (bản đầu); Tài khoản (đăng nhập Google, sao lưu ngay, lần sao lưu cuối; chỉ có ở bản có ngân phiếu nạp); Về màn chọn ô.
- **Trạng thái:** sao lưu đang chạy; sao lưu xong; sao lưu lỗi hoặc mất mạng.

### SCR-09 Menu nhân vật

Một khung chung, cột thẻ dọc bên trái, nội dung bên phải. Bảy thẻ theo GDD:

- **09a Hành trang:** lưới ô (30 ô, mở rộng thêm 6, 6, 12), ba loại tiền ở đầu khung (ngân phiếu hiện số tổng, chạm xem chi tiết thưởng và nạp, có biểu tượng mất kết nối khi offline), nút sắp xếp. Chạm một món mở bảng chi tiết: chỉ số, cấp yêu cầu, nút Dùng, Mặc, Bán, Bỏ, Khóa. Trạng thái: ô trống; ô khóa chống bán nhầm (biểu tượng ổ khóa nhỏ); ô chưa mở (xám, ghi cách mở); hành trang đầy (thông báo khi nhặt đồ).
- **09b Trang bị:** nhân vật đứng giữa, 10 ô quanh người (vũ khí, đầu, thân, tay, chân, bàn chân, cổ, ngón, hông, bùa). Chạm ô xem chỉ số, nút Tháo, nút So sánh với món trong túi (mũi tên xanh tăng, đỏ giảm).
- **09c Kỹ năng:** cây chiêu của phái, điểm còn lại; chạm chiêu xem mô tả theo cấp; kéo chiêu vào 6 ô. Trạng thái chiêu: chưa đủ cấp, đã học, đã tối đa.
- **09d Tiềm năng:** bốn chỉ số Sức mạnh, Thân pháp, Thể lực, Khí lực; nút +1 và ô nhập số; dòng xem trước HP, MP, tấn công thay đổi ra sao trước khi xác nhận.
- **09e Thông tin:** bảng chỉ số đầy đủ, danh hiệu, danh vọng từng vùng.
- **09f Thú cưỡi:** thú đang dùng, cấp, sao, thanh kinh nghiệm x/1.000, 4 ô trang bị thú, nút Cho ăn, Nâng sao, Đổi thú. Trạng thái: chưa có thú; thú đã tối đa cấp (nút Nâng sao sáng).
- **09g Nhiệm vụ:** nhiệm vụ chính đang làm (bước và số đếm), việc làng đang nhận, nhật ký cốt truyện đã qua (xem lại cutscene), nút "Tìm đường".

### SCR-10 Hội thoại

- **Bố cục:** chân dung NPC bên trái (128×128), khung lời thoại nửa dưới màn, cột lựa chọn bên phải (tối đa 4).
- **Trạng thái:** chữ đang chạy (chạm để hiện hết); chờ chạm tiếp (mũi tên nhấp nháy); có lựa chọn; người nói là Đinh Bộ Lĩnh (chân dung chuyển sang bên phải).
- **Dấu trên đầu NPC ngoài bản đồ:** chấm than vàng (có nhiệm vụ mới), dấu hỏi vàng (chờ trả nhiệm vụ), dấu hỏi xám (nhiệm vụ đang làm, chưa xong).

### SCR-11 Cửa hàng NPC

- **Bố cục:** nửa trái là hàng theo thẻ; nửa phải là hành trang; dải tiền ở trên cùng.
- **Thành phần:** chạm món hiện chỉ số, giá, cấp yêu cầu; nút Mua, Mua nhiều (thanh trượt số lượng); kéo món từ hành trang sang để bán, nút Bán nhiều.
- **Trạng thái:** chưa đủ cấp (mờ, "Yêu cầu cấp n"); thiếu tiền đồng nhưng đủ khi trừ ngân lượng (nút đổi thành "Mua (trừ n ngân lượng)"); thiếu cả hai (nút xám); hàng chưa mở bán theo hồi (ổ khóa, "Mở sau Hồi n"); hành trang đầy.

### SCR-12 Thợ rèn

Một màn sáu thẻ: Cường hóa, Luyện đá, Tách, Chuyển hóa, Dịch chuyển, Tinh luyện. Bố cục chung ba cột như GDD Phần 5, mục 3.

- **Cột trái:** ô món đồ chính, các ô nguyên liệu (đá, bùa bảo hộ, quặng tinh).
- **Cột giữa:** cấp hiện tại → cấp kế, chỉ số trước và sau, tỉ lệ thành công lớn, phí tiền đồng; ở thẻ Cường hóa có công tắc **Thường / Rèn kỹ**, khi chọn Rèn kỹ hiện phí ngân phiếu (ghi rõ phần trừ từ thưởng và từ nạp) hoặc ô đặt Lệnh bài rèn kỹ.
- **Cột phải:** hành trang chỉ hiện món dùng được cho thẻ đang mở.
- **Dưới cùng:** nút thực hiện (búa), nút "Tự chọn đá", dòng cảnh báo rớt cấp ("Thất bại sẽ về +8") khi chưa có bùa bảo hộ.
- **Trạng thái:** chưa đặt món; thiếu đá (tỉ lệ đỏ); đã đạt tỉ lệ tối đa (tỉ lệ vàng, ghi "Tối đa"); món đã đạt giới hạn cấp; Rèn kỹ khi phí vượt ngân phiếu thưởng mà mất mạng (vô hiệu, gợi ý dùng Lệnh bài hoặc ngân phiếu thưởng; quy tắc ở `12_ngan_phieu.md`); đang rèn (búa gõ 3 nhịp, khóa mọi nút); thành công; thất bại có rớt cấp; thất bại không rớt cấp.

### SCR-13 Cửa hàng ngân phiếu và Gói

Quy tắc ở `12_ngan_phieu.md`. Màn này có hai bản; **mockup cho bản đầu là bắt buộc ở mốc A**, bản có ngân phiếu nạp làm sau.

**Bản đầu (mục 12 của `12_ngan_phieu.md`):**

- **Đầu màn:** số ngân phiếu thưởng. Không có biểu tượng mất kết nối vì không có ngân phiếu nạp.
- **Thẻ Cửa hàng ngân phiếu:** bố cục như SCR-11, nhóm Bảo hộ, Tiện ích, Thời trang, Thú cưỡi; mua bằng ngân phiếu thưởng, offline được; nút đổi ngân phiếu thưởng ra ngân lượng.
- **Thẻ Gói:** các món vĩnh viễn bán bằng tiền thật (gói khởi đầu, đồ thời trang, thú cưỡi ngoại hình, túi da cấp 3). Mỗi món có giá do Google Play trả về, nút xem thử trên nhân vật, nút Mua. Dòng nhỏ ghi "Món đã mua dùng được ở cả ba ô".
- **Trạng thái thẻ Gói:** mất mạng ("Cần kết nối để mua", món đã sở hữu vẫn hiện); đang chờ Google Play; mua thành công (món vào ô đang chơi, hiệu ứng mở hộp); hủy hoặc lỗi; đã sở hữu (nút đổi thành "Đã có"); đã có quyền lợi qua sản phẩm khác (nút "Đã có qua Gói khởi đầu", không cho mua); gói khởi đầu đã mua (ẩn khỏi danh sách); vừa cấp khoản ngân phiếu thưởng của gói cho ô này lần đầu (thông báo nổi); thanh toán đang chờ ("Sẽ nhận khi Google Play xác nhận").

**Bản có ngân phiếu nạp (để sau):**

- **Đầu màn:** số tổng ngân phiếu, chạm mở bảng chi tiết thưởng và nạp (mục 3 của `12_ngan_phieu.md`); biểu tượng mất kết nối khi offline.
- **Thêm thẻ Nạp:** 5 gói (giá, số ngân phiếu hoặc ngân lượng, phần thưởng thêm), mỗi gói hai nút "Nhận ngân phiếu", "Nhận ngân lượng"; dòng ghi rõ ô nhân vật nhận tiền; dấu "Gấp đôi lần đầu" nếu ô chưa nạp.
- **Trạng thái thẻ Nạp:** mất mạng; chưa đăng nhập (SCR-19); đang chờ Google Play; đang xác minh với máy chủ; thành công; thất bại hoặc bị hủy; thanh toán đang chờ; giới hạn giờ chơi (SCR-21).
- **Trạng thái thẻ Cửa hàng:** món mua được bằng ngân phiếu thưởng; món cần ngân phiếu nạp khi offline (nút vô hiệu, "Cần kết nối để dùng ngân phiếu nạp. Bạn có thể dùng ngay T ngân phiếu thưởng"); giao dịch đang chờ xác nhận; số dư nạp âm do hoàn tiền; không đủ cả hai nguồn.
### SCR-14 Bản đồ vùng

- **Mục đích:** chạm bản đồ nhỏ ở SCR-05 mở bản đồ cả vùng, và đi nhanh tới các điểm đã mở. Chạy offline hoàn toàn.
- **Bố cục:** bản đồ vẽ tay của vùng đang đứng ở giữa; các bản đồ con là ô có tên; thẻ chọn vùng ở cạnh trên (chỉ hiện vùng đã tới); chú thích ở góc dưới phải.
- **Thành phần:** vị trí người chơi (cờ lau nhỏ); NPC có nhiệm vụ (chấm than, dấu hỏi); lối nối giữa các bản đồ; **điểm dịch chuyển** là các làng, căn cứ và điểm hồi sinh đã tới.
- **Dịch chuyển:** chạm một điểm dịch chuyển đã mở hiện hộp xác nhận "Đi tới …?", rồi chuyển qua SCR-03. Không tốn tiền.
- **Trạng thái:** bản đồ chưa tới (mờ, không có tên); bản đồ khóa theo cốt truyện (ổ khóa, ghi nhiệm vụ mở); điểm dịch chuyển chưa mở (xám); không dịch chuyển được khi đang trong trận boss, giữ ải, hộ tống hoặc màn đuổi bắt (nút xám, ghi lý do).

### SCR-15 Thua trận

- **Thành phần:** màn tối dần, dòng "Bộ Lĩnh ngã xuống", nút "Về điểm hồi sinh". Không có hồi sinh tại chỗ.
- **Trong trận boss:** thêm nút "Đánh lại", đưa người chơi về điểm hồi sinh trước đấu trường và vào lại trận ngay, boss đầy máu.
- **Trong giữ ải:** chuyển sang SCR-17 trạng thái thua.

### SCR-16 Phần thưởng

- **Dùng cho:** xong nhiệm vụ, thắng boss.
- **Thành phần:** tiêu đề, danh sách phần thưởng dạng ô (kinh nghiệm, tiền, đá, vật phẩm), nút Nhận. Thắng boss thêm tranh tĩnh nhỏ của boss và dòng kết cục (quy phục hay bị đánh dẹp).

### SCR-17 Kết quả Giữ ải

- **Thành phần:** 1 đến 3 sao (hiện lần lượt), máu cờ còn lại, số đợt đã giữ, rương mở theo số sao, phần thưởng lần đầu đạt 3 sao, nút "Giữ lại" và "Rời ải".
- **Trạng thái:** thua (cờ đổ, không có sao, vẫn nhận phần nhỏ theo số đợt đã qua); cao hơn cấp ải quá 10 cấp (dòng ghi chỉ nhận rương 1 sao).

### SCR-18 Trình chiếu cutscene

- **Bố cục:** tranh tĩnh toàn màn, hai dải đen trên dưới, khung lời thoại dưới; góc trên phải nút "Bỏ qua" (giữ 1 giây) và nút tự chạy.
- **Trạng thái:** đang chạy; tạm dừng; xem lại từ nhật ký (không có nút bỏ qua vì đã xem).
- Nội dung từng cutscene ở `10_storyboard.md`.

### SCR-19 Đăng nhập Google (bản có ngân phiếu nạp)

Bản đầu không có màn này: mua và khôi phục món vĩnh viễn dùng tài khoản Google Play có sẵn trên máy.


- **Khi nào:** chỉ khi người chơi chủ động: bấm nạp lần đầu; dùng ngân phiếu nạp trên máy chưa đăng nhập; bật sao lưu đám mây ở Cài đặt (mục 8 của `12_ngan_phieu.md`). Không bao giờ hiện khi vào game hay khi chơi.
- **Thành phần:** giải thích ngắn vì sao cần (giữ tiền nạp và sao lưu ba ô khi đổi máy), nút "Đăng nhập bằng Google", nút "Để sau".
- **Trạng thái:** đang đăng nhập; lỗi; mất mạng; đã đăng nhập (hiện tên tài khoản). "Để sau" luôn đưa về đúng chỗ đang chơi, offline.

### SCR-20 Hộp xác nhận và thông báo nổi

- **Hộp xác nhận chuẩn:** tiêu đề, một đến hai dòng nội dung, nút chính bên phải, nút hủy bên trái. Hộp nguy hiểm (xóa ô, bán món quý, đổi ngân phiếu) dùng nút chính màu đỏ chiến.
- **Thông báo nổi:** một dòng ở giữa cạnh trên, tự ẩn sau 2 giây; loại thường, thành công (viền xanh), lỗi (viền đỏ).

### SCR-21 Nhắc giờ chơi

- **Mục đích:** đáp ứng yêu cầu pháp lý về giờ chơi của người dưới 18 tuổi và cảnh báo sức khỏe định kỳ (Phần 6 GDD). Cách xác định tuổi cần luật sư chốt.
- **Thành phần:** thông báo nổi mỗi 30 phút; hộp chặn khi hết giờ cho phép, có nút lưu và thoát.

### SCR-22 Căn cứ Hoa Lư

- **Mục đích:** xây và nâng cấp bốn công trình với Lưu Cơ. Chạy offline. Không có thời gian chờ xây: bấm Xây là xong ngay, kèm hoạt ảnh dựng công trình ngắn.
- **Bố cục:** cảnh căn cứ nhìn ngang với bốn khu đất cố định; chạm khu đất mở bảng công trình: tên, cấp hiện tại trên 3, lợi ích cấp hiện tại và cấp kế, vật liệu cần (gỗ lim, đá xanh, ngói), nút Xây hoặc Nâng cấp.
- **Bốn công trình**, mỗi công trình 3 cấp:
  - **Trại lính:** tướng đi cùng trong giữ ải mạnh hơn.
  - **Kho lương:** tăng lương thảo tối đa.
  - **Chuồng ngựa:** tặng thức ăn thú cưỡi.
  - **Lò rèn:** giảm phí rèn 5%, 10%, 15%.
- **Chưa chốt (làm khi cân bằng, không chặn mockup):** số vật liệu mỗi cấp, mức tăng sức mạnh tướng, lương thảo tối đa và lượng thức ăn thú mỗi cấp. Mockup dùng ô số giữ chỗ.
- **Trạng thái:** chưa xây (khu đất trống, biểu tượng búa); thiếu vật liệu (vật liệu thiếu hiện đỏ, nút xám); đủ vật liệu (nút sáng); đã cấp 3 (ghi "Tối đa"); chưa mở theo cốt truyện (căn cứ mở ở nhiệm vụ 28).

## Mẫu đặc tả một màn hình

Mỗi file `design/screens/scr_<số>_<tên>.md` gồm các phần:

1. **Mục đích** — một hai câu.
2. **Vào từ / ra tới** — các màn và hành động dẫn tới, khớp với `07_ui_flow.md`.
3. **Bố cục** — danh sách vùng, mỗi vùng có tọa độ (x, y, rộng, cao) trên khung 960×540.
4. **Thành phần** — mỗi thành phần: loại (nút, ô, thanh, danh sách), kích thước, hành động khi chạm.
5. **Trạng thái** — mỗi trạng thái: điều kiện xảy ra, cái gì thay đổi trên màn, mã mockup tương ứng nếu có hình riêng.
6. **Chữ hiển thị** — mọi chuỗi chữ tiếng Việt, kể cả thông báo lỗi.
7. **Âm thanh và hoạt ảnh** — tham chiếu mã trong `09_animation_spec.md`.
8. **Câu hỏi còn mở** — chỗ cần người dùng quyết định.

## Tự soát một màn hình

- Mọi nút đều có hành động và trạng thái vô hiệu nếu có lúc không dùng được.
- Mọi màn có dữ liệu đều có trạng thái trống và lỗi; màn cần mạng có trạng thái mất mạng.
- Không có nút nào trong vùng an toàn 16 điểm ảnh ở hai cạnh.
- Mockup và đặc tả khớp nhau về vị trí và số lượng thành phần.
- Chữ dài nhất vẫn vừa khung (thử với chuỗi dài nhất có thể, ví dụ tên vật phẩm dài nhất).
