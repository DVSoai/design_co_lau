# Quy tắc ngân phiếu và giao dịch

Tài liệu này quy định cách hai nguồn ngân phiếu được giữ, hiển thị và tiêu, cả khi có mạng lẫn khi mất mạng. Nó thắng mọi mô tả ngắn hơn về ngân phiếu trong các tài liệu khác. Đây là quy tắc thiết kế, ảnh hưởng tới mockup SCR-09a, SCR-12, SCR-13 và các luồng F3, F4, F9, F10; chi tiết hiện thực (giao thức, cấu trúc dữ liệu máy chủ) làm ở giai đoạn code nhưng không được trái với tài liệu này.

## 0. Phạm vi theo phiên bản

Đã chốt ngày 28/10/2026: **bản phát hành đầu tiên chỉ bán món vĩnh viễn qua Google Play** (mục 12), không có ngân phiếu nạp và không có máy chủ riêng. Vì vậy tài liệu này chia hai phần:

- **Áp dụng ngay cho bản đầu:** mục 1 (nguyên tắc offline), ngân phiếu thưởng trong mục 2 đến 4, mục 10 (kiểm tra toàn vẹn), mục 12 (bán món vĩnh viễn).
- **Thiết kế cho bản có ngân phiếu nạp** (dự kiến ra cùng bản online, `14_online_migration.md`): mọi phần về ngân phiếu nạp, giao dịch kết hợp (mục 5), phục hồi giao dịch (mục 6), hoàn tiền ngân phiếu nạp (mục 7), tài khoản (mục 8), xóa ô có ngân phiếu nạp (mục 9). Các phần này giữ nguyên để không phải thiết kế lại, nhưng không làm mockup hay code cho bản đầu.

Ở bản đầu, mọi ô nhân vật đều ở trạng thái "chưa liên kết máy chủ", giao diện chỉ hiện ngân phiếu thưởng, và không có màn đăng nhập.

## 1. Nguyên tắc offline

Không tính năng chơi nào cần mạng. Ở bản đầu, mạng chỉ dùng để mua và khôi phục món vĩnh viễn qua Google Play (mục 12). Ở bản có ngân phiếu nạp, mạng dùng thêm cho nạp tiền, tiêu ngân phiếu nạp và sao lưu đám mây. Mất mạng không bao giờ chặn việc vào game, chơi cốt truyện, đánh quái, giữ ải, mua bán ở NPC, cường hóa thường, Rèn kỹ bằng Lệnh bài, hay tiêu ngân phiếu thưởng. Đăng nhập Google không bao giờ bắt buộc để chơi.

## 2. Hai nguồn ngân phiếu

- **Ngân phiếu thưởng:** nhận từ nhiệm vụ cuối mỗi hồi và lần đầu hạ mỗi boss sứ quân. Lưu trong file lưu của ô nhân vật (có chữ ký HMAC như mọi dữ liệu lưu). Tiêu được offline.
- **Ngân phiếu nạp:** nhận khi nạp tiền. Số dư thật do máy chủ giữ, theo từng ô nhân vật của tài khoản Google. Máy chỉ giữ một **bản sao số dư lần đồng bộ cuối**, dùng để hiển thị tham khảo, không bao giờ dùng để quyết định một giao dịch.

Hai nguồn có cùng giá trị khi mua hàng. Ngân phiếu nạp không đổi thành ngân phiếu thưởng và ngược lại.

## 3. Hiển thị

Giao diện hiện **một số tổng** ở dải tiền (SCR-09a, SCR-11, SCR-13). Chạm vào số tổng mở bảng chi tiết.

**Khi có mạng và đã đồng bộ:**

```
Ngân phiếu 420
  Thưởng 120 · Nạp 300
```

**Khi mất mạng, hoặc chưa đồng bộ được:** số tổng có biểu tượng mất kết nối nhỏ bên cạnh, và bảng chi tiết ghi rõ phần nào dùng được:

```
Ngân phiếu 420 (ngoại tuyến)
  Dùng được ngay: 120 ngân phiếu thưởng
  Ngân phiếu nạp: 300 — số dư lần đồng bộ lúc 09:15 ngày 28/10, chỉ để tham khảo.
  Cần kết nối để dùng ngân phiếu nạp.
```

**Khi chưa từng nạp:** chỉ hiện số ngân phiếu thưởng, không có dòng ngân phiếu nạp và không có biểu tượng mất kết nối.

**Khi số dư nạp âm do hoàn tiền:** dòng nạp ghi số âm màu đỏ và một dòng giải thích (mục 7).

## 4. Giá phải trả và nút mua

Mọi giá ghi bằng ngân phiếu. Khi người chơi chọn một món giá G, với T là ngân phiếu thưởng và N là ngân phiếu nạp đã xác thực:

- **G ≤ T:** trừ toàn bộ bằng ngân phiếu thưởng, ngay trên máy, không cần mạng. Nút ghi "Mua".
- **G > T và có mạng:** cần ngân phiếu nạp cho phần G − T. Nút ghi "Mua (T thưởng + (G − T) nạp)". Giao dịch đi qua máy chủ theo mục 5.
- **G > T và mất mạng:** nút vô hiệu, dòng dưới ghi "Cần kết nối để dùng ngân phiếu nạp. Bạn có thể dùng ngay T ngân phiếu thưởng."
- **G > T + N:** nút vô hiệu, gợi ý nạp thêm.

Thứ tự trừ luôn là ngân phiếu thưởng trước, nạp sau. Người chơi không chọn thứ tự, để màn hình đơn giản.

Áp dụng giống hệt cho phí Rèn kỹ ở thợ rèn (SCR-12) và nút đổi ngân phiếu ra ngân lượng.

## 5. Giao dịch kết hợp hai nguồn

Một món mua bằng cả hai nguồn là **một giao dịch duy nhất**, hoặc thành công trọn vẹn, hoặc không có gì thay đổi. Máy **không trừ ngân phiếu thưởng trước** rồi mới thử trừ phần nạp qua mạng.

1. Máy tạo một **mã giao dịch** duy nhất, ghi vào file lưu một mục "đang chờ" gồm: mã, món hàng, giá, phần thưởng T dùng, phần nạp cần trừ. Phần T này bị **giữ chỗ**: chưa trừ, nhưng không tiêu vào việc khác được cho tới khi giao dịch xong.
2. Máy gửi yêu cầu kèm mã giao dịch lên máy chủ.
3. Máy chủ kiểm tra số dư nạp, trừ phần nạp, ghi vào sổ giao dịch theo mã. Nếu mã này đã được xử lý trước đó, máy chủ trả lại đúng kết quả cũ, **không trừ lần nữa**.
4. Máy chủ trả về biên nhận (thành công) hoặc lý do từ chối.
5. Có biên nhận: máy trừ phần thưởng T, giao món, xóa mục "đang chờ", ghi mã vào danh sách đã áp dụng, rồi lưu ngay. Bị từ chối: máy bỏ giữ chỗ, không trừ gì.
6. Mất mạng hoặc tắt game giữa bước 2 và bước 5: mục "đang chờ" vẫn nằm trong file lưu. Lần mở game kế tiếp có mạng, máy hỏi máy chủ kết quả của mã đó và làm tiếp bước 5. Danh sách mã đã áp dụng bảo đảm một biên nhận chỉ được áp dụng một lần.

Mục "đang chờ" hiện trong SCR-13 với dòng "Đang xác nhận giao dịch, sẽ hoàn tất khi có kết nối". Mục chờ quá 7 ngày mà máy chủ không có ghi nhận thì tự hủy và bỏ giữ chỗ.

Mọi yêu cầu gửi máy chủ đều kèm **định danh ô** (tạo lúc bấm Chơi mới, không bao giờ dùng lại) để máy chủ ghi đúng ô. Sau bước 5, máy gửi thêm một xác nhận "đã áp dụng" để máy chủ biết giao dịch đã xong; xác nhận này chỉ để theo dõi, không quyết định việc cấp lại (mục 6).

Giao dịch chỉ dùng ngân phiếu nạp (T = 0) đi cùng đường này.

## 6. Phục hồi khi file lưu mất, hỏng hoặc quay về bản cũ

Máy chủ là nguồn sự thật cho mọi thứ đã trả bằng ngân phiếu nạp. Sổ giao dịch của máy chủ ghi mỗi giao dịch theo mã và định danh ô, kèm loại hàng và phần ngân phiếu thưởng đã dùng. File lưu giữ danh sách mã đã áp dụng.

Mỗi lần đồng bộ (mở game có mạng và đã đăng nhập), máy so danh sách mã trong file lưu với sổ của máy chủ. Mã nào máy chủ có mà file lưu chưa có thì xử lý theo loại hàng:

- **Món vĩnh viễn** (đồ thời trang, thú cưỡi ngoại hình, túi da mở rộng hành trang): máy chủ giữ danh sách quyền sở hữu của ô. Món có trên máy chủ mà thiếu trong file lưu thì cấp lại. Việc so theo món chứ không theo lần mua, nên không bao giờ có hai bản.
- **Món tiêu hao và tiền đổi** (bùa bảo hộ, giấy tẩy điểm, thức ăn, ngân lượng đổi từ ngân phiếu): áp dụng lại đúng một lần rồi ghi mã vào danh sách. Phần ngân phiếu thưởng của giao dịch đó được trừ lại trong file lưu hiện tại; không đủ thì trừ về 0.
- **Dịch vụ không dựng lại được** (phí Rèn kỹ): kết quả lần rèn không dựng lại được, nên máy chủ hoàn phần ngân phiếu nạp của giao dịch đó vào số dư và đánh dấu giao dịch là đã hoàn.

Ba trường hợp phải xử lý đúng:

- **File lưu mất hoặc hỏng, mở bản sao lần lưu trước:** các giao dịch sau bản sao được áp dụng lại theo quy tắc trên. Người chơi không mất món đã trả tiền.
- **Cài lại game, khôi phục từ sao lưu đám mây:** như trên, so với bản được khôi phục.
- **File lưu còn nguyên, giao dịch đã áp dụng:** mã đã có trong danh sách nên không làm gì. Không bao giờ nhận hai lần.

### Những gì được bảo đảm và những gì không

Ba loại hàng được xử lý khác nhau vì máy chủ biết về chúng ở mức khác nhau:

- **Quyền sở hữu vĩnh viễn:** máy chủ biết chính xác món nào thuộc ô nào. Bảo đảm không mất và không nhân đôi.
- **Vật phẩm tiêu hao:** máy chủ chỉ biết món đã được **giao**, không biết món đã được **dùng** hay chưa, vì việc dùng diễn ra offline. Bảo đảm: không mất món đã trả tiền khi file lưu mất hoặc hỏng; một file lưu không nhận cùng một giao dịch hai lần. **Không bảo đảm:** chặn người chơi dùng lại món tiêu hao bằng cách tự khôi phục một bản lưu cũ có món đó còn chưa dùng (ví dụ mua thức ăn thú, cho thú ăn hết, rồi chép đè bản lưu trước lúc cho ăn).
- **Dịch vụ đã thực hiện** (Rèn kỹ): máy chủ chỉ biết phí đã trả. Nếu file lưu mất trước khi kết quả được lưu, phí được hoàn; nếu kết quả đã lưu, không làm gì thêm.

Giới hạn thứ hai là giới hạn chung của mọi game offline, không sửa được bằng thiết kế giao dịch. Bản offline chấp nhận nó vì người chơi chỉ ảnh hưởng game của chính mình, và vì thao tác này buộc họ bỏ hết tiến độ sau bản lưu cũ. Để thu hẹp nó, game chỉ giữ một bản sao lưu cục bộ (lần lưu ngay trước), sao lưu đám mây chỉ khôi phục bản mới nhất, và file lưu nằm trong thư mục riêng của ứng dụng. Chỉ bản online, khi máy chủ giữ cả việc dùng vật phẩm, mới chặn được hoàn toàn (`14_online_migration.md`).

## 7. Hoàn tiền

- Máy chủ nhận thông báo hoàn tiền từ Google Play và trừ lại số ngân phiếu nạp tương ứng khỏi ô đã nhận. Mỗi đơn hàng Google chỉ được áp dụng hoàn tiền một lần, theo mã đơn hàng ghi trong sổ giao dịch.
- Số dư nạp được phép âm. Khi âm, mọi giao dịch cần ngân phiếu nạp bị khóa; lần nạp sau bù vào phần âm trước.
- **Không thu hồi** món đã mua, **không khóa** gameplay, không khóa ngân phiếu thưởng.
- SCR-13 hiện dòng: "Ngân phiếu nạp −150 do một giao dịch đã được hoàn tiền. Bạn vẫn chơi và dùng ngân phiếu thưởng bình thường."

## 8. Tài khoản

Gameplay không bao giờ cần đăng nhập. Đăng nhập Google chỉ được hỏi (SCR-19) khi người chơi **chủ động**:

- bấm nạp tiền lần đầu;
- dùng ngân phiếu nạp trên một máy chưa đăng nhập (ví dụ đã cài lại game);
- bật sao lưu đám mây.

Nút "Để sau" luôn có, và luôn đưa người chơi về game offline đúng chỗ đang chơi.

## 9. Xóa ô nhân vật

Xóa ô không phải là gameplay, nên được phép đòi mạng khi trong ô có tiền thật.

- **Ô chưa từng liên kết máy chủ:** xóa ngay, kể cả khi offline. Xóa cả ngân phiếu thưởng trong ô.
- **Ô có ngân phiếu nạp (theo lần đồng bộ cuối) hoặc có giao dịch đang chờ:** không xóa được khi offline. Nút xóa ghi "Cần kết nối để xóa ô có ngân phiếu nạp". Khi có mạng, hộp xác nhận lần hai hiện số dư thật lấy từ máy chủ.
- **Ô đã liên kết nhưng số dư nạp bằng 0 và không có giao dịch chờ:** xóa được khi offline. Ô biến mất khỏi màn chọn ô ngay, vị trí đó chơi mới được (ô mới có định danh mới). Lệnh xóa nằm trong `user://saves/index.json` ở trạng thái **chờ đồng bộ xóa**. Máy chủ giữ nguyên dữ liệu và định danh của ô cho tới khi nhận được lệnh; định danh ô trên máy chủ không bị xóa trước thời điểm đó.
- **Khi lệnh xóa tới máy chủ:** nếu máy chủ thấy ô vẫn còn ngân phiếu nạp hoặc giao dịch (ví dụ một lần nạp được ghi nhận sau lần đồng bộ cuối), máy chủ không xóa. Game báo cho người chơi và cho hai lựa chọn: khôi phục ô từ sao lưu đám mây, hoặc xác nhận xóa hẳn với số dư thật được ghi rõ.
- **Cài lại game trước khi lệnh xóa kịp gửi:** lệnh xóa mất theo máy cũ, nên ô vẫn còn trên máy chủ và có thể xuất hiện lại khi khôi phục từ đám mây. Người chơi xóa lại nếu muốn. Trường hợp này được chấp nhận vì không làm mất tiền của ai.

## 10. Kiểm tra toàn vẹn và chỉnh sửa file lưu

File lưu có mã kiểm tra để phát hiện file hỏng, và chữ ký HMAC để chặn kiểu sửa tay đơn giản. Đây là **kiểm tra toàn vẹn, không phải chống chỉnh sửa**: khóa ký nằm trong ứng dụng nên có thể bị trích xuất, và game không cam kết người chơi không sửa được file lưu.

Với game một người chơi không có giao dịch giữa người chơi, rủi ro này được chấp nhận: ai sửa file chỉ ảnh hưởng game của chính họ, kể cả ngân phiếu thưởng. Mọi thứ có giá trị tiền thật (ngân phiếu nạp, giao dịch nạp, quyền sở hữu món đã mua) do máy chủ xác thực, và máy chủ không bao giờ tin số liệu tiền nạp trong file lưu.

## 11. Câu hỏi còn mở (trước khi phát hành)

- Giá các gói nạp và tỉ lệ thưởng thêm.
- Thời hạn 7 ngày cho mục "đang chờ" có hợp với quy định lưu giữ giao dịch hay không.

## 12. Bán món vĩnh viễn ở bản đầu

### Bán gì

Chỉ bán **món vĩnh viễn**, mua thẳng bằng tiền thật qua Google Play (loại sản phẩm không tiêu hao). Không bán tiền tệ, không bán vật phẩm tiêu hao, không bán thứ gì tăng sức mạnh chiến đấu ngoài túi da mở rộng hành trang.

- **Gói khởi đầu:** mua được một lần; gồm một bộ đồ thời trang riêng, túi da cấp 3 và một khoản ngân phiếu thưởng.
- **Đồ thời trang:** khăn, mũ, áo choàng, thời trang theo ô, có chỉ số theo 17_ngoai_hinh.md.
- **Thú cưỡi ngoại hình:** ngựa ô, ngựa bạch, voi trắng; chỉ số bằng thú cùng loại.
- **Túi da cấp 3:** mở sớm 12 ô hành trang (túi da cấp 1 và 2 chỉ nhận từ nhiệm vụ hoặc mua bằng ngân phiếu thưởng).

Giá bằng tiền thật là đề xuất, chốt ở mốc B (`13_thong_so.md`). Đồ thời trang và thú cưỡi ngoại hình bán qua Google Play là các bộ riêng, khác với món bán trong cửa hàng ngân phiếu, để không có hai cách mua cùng một món.

### Sản phẩm và quyền lợi

Mỗi sản phẩm Google Play (id `sku_…`) ánh xạ sang một danh sách **quyền lợi** trong game (id `ent_…`). Bảng ánh xạ nằm trong dữ liệu game, không viết cứng trong code. Có hai loại quyền lợi, xử lý khác nhau:

- **Quyền lợi sở hữu:** đồ thời trang, thú cưỡi ngoại hình, túi da cấp 3. Một ô hoặc có, hoặc không. Ô nào chưa có thì cấp; đã có thì thôi. Không bao giờ thành hai bản.
- **Quyền lợi cấp một lần mỗi ô:** khoản ngân phiếu thưởng trong gói khởi đầu. Mỗi ô nhận đúng một lần. File lưu của ô ghi cờ "đã nhận" theo id quyền lợi; ô chưa có cờ thì cấp và ghi cờ, ô đã có cờ thì không cấp nữa.

Ví dụ `sku_goi_khoi_dau` ánh xạ sang `ent_thoi_trang_khoi_dau` (sở hữu), `ent_tui_da_3` (sở hữu) và `ent_np_thuong_khoi_dau` (cấp một lần mỗi ô).

Hệ quả, đều đã xét và chấp nhận:

- **Mỗi ô trong ba ô** nhận khoản ngân phiếu thưởng của gói một lần, vì quyền mua thuộc tài khoản và ba ô tách biệt; ngân phiếu thưởng không chuyển được giữa các ô.
- **Xóa ô rồi chơi mới:** ô mới có định danh mới nên nhận lại khoản ngân phiếu thưởng. Việc này không tạo lợi thế gì đáng kể, vì người chơi phải bắt đầu lại từ đầu và khoản đó không chuyển sang ô khác.
- **Khôi phục bản lưu cũ trước lúc nhận:** bản cũ chưa có cờ nên được cấp, đúng với thời điểm của bản đó. Bản lưu có cờ rồi thì không cấp nữa, nên một file lưu không bao giờ nhận hai lần.
- **Sản phẩm trùng quyền lợi:** nếu tài khoản đã có `ent_tui_da_3` qua gói khởi đầu, sản phẩm túi da cấp 3 bán riêng hiện "Đã có qua Gói khởi đầu" và không cho mua.

### Món đã mua thuộc tài khoản Google Play, dùng ở cả ba ô

Google Play ghi món không tiêu hao theo tài khoản Google trên máy, không theo ô nhân vật. Vì bản đầu không có máy chủ riêng để gắn món vào từng ô, **món đã mua dùng được ở cả ba ô**. Đây là ngoại lệ duy nhất của quy tắc "ba ô tách biệt hoàn toàn", chỉ áp dụng cho món mua bằng tiền thật. Khi có bản online, cách gắn món sẽ xét lại theo `14_online_migration.md`.

### Mua và khôi phục

1. Người chơi bấm mua ở thẻ "Gói" của SCR-13. Game gọi Google Play Billing qua plugin `GodotGooglePlayBilling`.
2. Google Play xác nhận thanh toán. Game cấp các quyền lợi của sản phẩm vào ô đang chơi theo hai loại ở trên, lưu, rồi báo Google Play xác nhận đơn hàng (acknowledge). Đơn không được xác nhận trong 3 ngày sẽ bị Google tự hoàn tiền, nên bước này bắt buộc.
3. Mỗi lần mở game có mạng, mỗi lần vào một ô, và khi người chơi bấm "Khôi phục món đã mua" ở Cài đặt, game hỏi Google Play danh sách sản phẩm đang sở hữu, đổi ra danh sách quyền lợi, rồi cấp cho ô đang chơi những quyền lợi còn thiếu (quyền lợi sở hữu) hoặc chưa có cờ (quyền lợi cấp một lần). Vì so theo quyền lợi và cờ, không bao giờ cấp hai lần.
4. Đổi máy hay cài lại game: đăng nhập cùng tài khoản Google trên máy là khôi phục được món đã mua, không cần đăng nhập gì thêm trong game.

Mua cần mạng (vì Google Play cần mạng), nhưng món đã cấp dùng offline bình thường. Không có màn đăng nhập riêng của game.

### Hoàn tiền

Khi Google hoàn tiền một đơn, món đó biến mất khỏi danh sách sở hữu trên Google Play. Theo quyết định đã chốt, game **không thu hồi** món đã cấp trong các ô hiện có; chỉ là ô chơi mới sẽ không được cấp món đó nữa.

### Bảo mật

Bản đầu không có máy chủ để xác minh đơn hàng, nên một bản game bị sửa có thể giả lập việc mua. Rủi ro này được chấp nhận vì hàng bán chỉ là ngoại hình và tiện ích trong game một người chơi; nó không làm thiệt người chơi khác. Khi có máy chủ ở bản online, việc xác minh chuyển lên máy chủ.

### Sao lưu

Bản đầu không có sao lưu đám mây của riêng game. Game bật tính năng sao lưu tự động của Android cho thư mục lưu, để người chơi đổi máy cùng tài khoản Google có cơ hội giữ được tiến độ; tính năng này phụ thuộc cài đặt máy của người chơi, nên không hứa chắc với người chơi.

### Bổ sung mục 12 — thời trang bản đầu

Thời trang theo ô độc lập, mỗi món một dạng hình cố định, không đổi theo cấp. Ô trống hiện trang bị thật; mặc lẻ từng ô. Thời trang **có chỉ số**, cộng vào trang bị thật, không thay thế; ẩn hình vẫn giữ chỉ số. Không cường hóa thời trang. Tổng chỉ số một bộ đề xuất ≤10–15% bộ trang bị cùng bậc, từng loại chỉ số đối chiếu tương ứng; không thêm loại chỉ số trang bị thường không có. Cách cộng/chuẩn hóa và trần chính xác chốt Mốc A, không cộng thô các đại lượng khác đơn vị. Toàn bộ số chỉ số là thiết kế riêng. Hai nguồn: mua vĩnh viễn Google Play dùng chung cả 3 ô nhân vật; boss/nhiệm vụ/giữ ải cho món có chỉ số tương đương nhưng hình khác, không để người không nạp kém hẳn. Vũ khí thời trang thay hình theo phái, vẫn hiện hiệu ứng mức cường hóa vũ khí thật. [Phạm vi sau]: biến hình thay cả người.

SKU/entitlement vĩnh viễn thuộc tài khoản Google Play, dùng chung 3 ô; mặc/bỏ/ẩn là trạng thái từng ô. Khôi phục/cấp lại idempotent. Gói bộ phải liệt kê từng entitlement theo ô, không cấp chỉ số lặp. Không ngân phiếu nạp bản đầu.
