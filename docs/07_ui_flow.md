# Luồng tương tác

Tài liệu này mô tả người chơi đi từ màn này sang màn khác thế nào, và game phản ứng ra sao ở từng bước. Mã màn hình (SCR-xx) lấy từ `06_screens.md`. Sơ đồ viết bằng Mermaid; Codex dựng thành ảnh PNG lưu ở `design/flows/` khi cần duyệt (ví dụ bằng `mmdc` nếu máy có Mermaid CLI, hoặc dán vào trình xem Mermaid).

## F1 — Lần đầu mở game

Người chơi mới tải game đi thẳng vào câu chuyện, không bị bắt đăng nhập hay đọc hướng dẫn. Mười nhiệm vụ đầu là bài hướng dẫn trá hình (Phần 3 GDD).

```mermaid
flowchart LR
  A[SCR-01 Khởi động] --> B[SCR-02 Chọn ô]
  B -->|Chơi mới| C[SCR-18 Cutscene CS01]
  C --> D[SCR-05 Làng Hoa Lư, nhiệm vụ 1]
  D -->|Nhiệm vụ 1-9| E[Mở dần: đánh, thú cưỡi, cửa hàng, thức ăn]
  E -->|Nhiệm vụ 10| F[SCR-04 Chọn phái]
  F --> G[SCR-09c Kỹ năng: hướng dẫn kéo chiêu vào ô]
  G --> H[SCR-05 Chơi tiếp]
```

Mỗi hệ thống mới mở bằng một thẻ lớn giữa màn (SCR-05, thông báo mở hệ thống), rồi một mũi tên chỉ vào nút tương ứng cho tới khi người chơi chạm.

## F2 — Vòng chơi chính

```mermaid
flowchart TD
  A[SCR-10 Nhận nhiệm vụ từ NPC] --> B[SCR-05 Theo dõi nhiệm vụ, chạm để tìm đường]
  B --> C[Đánh quái, nhặt đồ]
  C -->|HP thấp| D[Dùng thuốc ô dùng nhanh]
  C -->|Ngã xuống| E[SCR-15 Thua trận]
  E -->|Về điểm hồi sinh| B
  C -->|Đủ số đếm| F[Dấu hỏi vàng trên NPC]
  F --> G[SCR-10 Trả nhiệm vụ]
  G --> H[SCR-16 Phần thưởng]
  H -->|Đồ mới| I[SCR-09b So sánh và mặc]
  H -->|Đủ đá, đủ tiền| J[SCR-12 Thợ rèn]
  I --> A
  J --> A
```

Game tự lưu ở các mốc: vào hoặc rời làng, xong nhiệm vụ, sau mỗi lần rèn hoặc mua bán, mỗi 2 phút, và khi ứng dụng xuống nền.

## F3 — Cường hóa ở thợ rèn

```mermaid
flowchart TD
  A[SCR-12 thẻ Cường hóa] --> B[Đặt món đồ]
  B -->|Đã đạt giới hạn cấp| X[Thông báo giới hạn, dừng]
  B --> C[Thêm đá thủ công hoặc Tự chọn đá]
  C --> D{Chế độ}
  D -->|Thường| E[Hiện phí tiền đồng]
  D -->|Rèn kỹ| F{Có Lệnh bài rèn kỹ?}
  F -->|Có| G[Dùng lệnh bài, không cần mạng]
  F -->|Không| Q{Phí ≤ ngân phiếu thưởng?}
  Q -->|Có| R[Trừ ngân phiếu thưởng khi bấm, không cần mạng]
  Q -->|Không| H{Có mạng?}
  H -->|Có| I[Giao dịch kết hợp qua máy chủ, xem F9]
  H -->|Không| Y[Rèn kỹ vô hiệu, gợi ý lệnh bài hoặc ngân phiếu thưởng]
  E --> J{Có bùa bảo hộ?}
  G --> J
  R --> J
  I --> J
  J -->|Không và có thể rớt cấp| K[Hiện cảnh báo rớt cấp]
  J -->|Có| L[Bấm búa]
  K --> L
  L --> M[Búa gõ 3 nhịp, khóa nút]
  M -->|Thành công| N[Lóe vàng, cấp mới]
  M -->|Thất bại| O[Tóe lửa đỏ, rớt về mốc an toàn hoặc giữ nguyên]
  N --> P[Lưu ngay]
  O --> P
```

Lưu ngay sau mỗi lần rèn, và trạng thái số ngẫu nhiên lưu trong file, để tắt game giữa chừng không đổi được kết quả. Cách này không chống được người cố tình chép đè file lưu cũ trước khi rèn; game offline chấp nhận giới hạn đó (GDD Phần 6, mục 1).

## F4 — Nạp tiền (bản có ngân phiếu nạp)

```mermaid
flowchart TD
  A[Bấm Nạp] --> B{Có mạng?}
  B -->|Không| X[SCR-13 trạng thái mất mạng]
  B -->|Có| C{Đã đăng nhập Google?}
  C -->|Chưa| D[SCR-19 Đăng nhập]
  D -->|Để sau| Z[Quay lại game offline, đúng chỗ đang chơi]
  D -->|Xong| E[SCR-13 thẻ Nạp]
  C -->|Rồi| E
  E --> F[Chọn gói và loại tiền nhận]
  F --> G[Hộp thanh toán Google Play]
  G -->|Hủy| E
  G -->|Đang chờ thanh toán| H[Ghi: sẽ cộng khi Google xác nhận]
  G -->|Đã trả| I[Gửi mã giao dịch lên máy chủ]
  I -->|Hợp lệ| J[Cộng tiền vào ô đang chơi, lưu, báo Google tiêu hao]
  I -->|Không hợp lệ| K[Báo lỗi, không cộng]
  I -->|Mất mạng giữa chừng| L[Giữ giao dịch, cộng ở lần mở game sau]
  J --> M[Thông báo thành công, sao lưu lên máy chủ]
```

Hoàn tiền đi theo luồng F10.

## F5 — Đánh boss

```mermaid
flowchart LR
  A[Nhiệm vụ chuẩn bị trước boss] --> B[SCR-03 Tải đấu trường]
  B --> C[Cutscene ngắn hoặc lời thoại mở màn]
  C --> D[SCR-06 Pha 1]
  D -->|60% máu| E[Chuyển pha 2]
  E -->|30% máu| F[Chuyển pha 3 nếu có]
  F --> G{Kết quả}
  D --> G
  G -->|Thắng| H[SCR-16 Phần thưởng và kết cục sứ quân]
  G -->|Thua| I[SCR-15, có nút Đánh lại]
  I -->|Đánh lại| D
```

## F6 — Giữ ải

```mermaid
flowchart TD
  A[Chọn ải từ NPC hoặc bản đồ vùng] --> B[SCR-07 Trước trận: chọn tướng, xem lương thảo]
  B --> C[Đợt 1]
  C --> D[20 giây chuẩn bị: dựng công trình]
  D --> E[Đợt kế tiếp]
  E -->|Còn đợt| D
  E -->|Cờ đổ| F[SCR-17 Thua]
  E -->|Qua đợt 8| G[SCR-17 Chấm sao và mở rương]
  G -->|Giữ lại| B
  G -->|Rời ải| H[Về bản đồ vùng]
  F -->|Giữ lại| B
```

## F7 — Xóa ô nhân vật

Xóa không khôi phục được, nên phải qua hai lần xác nhận (SCR-02). Ở bản đầu mọi ô đều chưa liên kết máy chủ, nên chỉ có nhánh "Chưa". Các nhánh còn lại thuộc bản có ngân phiếu nạp; quy tắc đầy đủ ở `12_ngan_phieu.md`, mục 9.

```mermaid
flowchart TD
  A[Bấm xóa ô] --> B{Ô từng liên kết máy chủ?}
  B -->|Chưa| C[Xác nhận 2 lần, xóa ngay, kể cả offline]
  B -->|Rồi| D{Có ngân phiếu nạp hoặc giao dịch chờ?}
  D -->|Có| E{Có mạng?}
  E -->|Không| F[Nút xóa vô hiệu: cần kết nối]
  E -->|Có| G[Xác nhận lần 2 với số dư thật từ máy chủ] --> H[Máy chủ xóa ô, máy xóa file]
  D -->|Không| I{Có mạng?}
  I -->|Có| H
  I -->|Không| J[Xóa trên máy, ghi lệnh chờ đồng bộ xóa vào index.json]
  J --> K[Lần đồng bộ kế gửi lệnh xóa]
  K -->|Ô sạch| L[Máy chủ xóa ô]
  K -->|Ô vẫn còn ngân phiếu nạp| M[Hộp: Khôi phục ô hoặc Xóa hẳn]
```

## F8 — Mất mạng và khôi phục

Game chơi offline. Chỉ ba nhóm hành động cần mạng: nạp, tiêu ngân phiếu nạp, sao lưu. Ngân phiếu thưởng tiêu offline bình thường (`12_ngan_phieu.md`). Khi mất mạng, các nút đó chuyển sang trạng thái mất mạng thay vì biến mất, để người chơi hiểu vì sao. Khi có mạng trở lại, game tự đồng bộ giao dịch treo và sao lưu, rồi hiện một thông báo nổi ngắn.

## F9 — Mua bằng ngân phiếu

Ở bản đầu chỉ có nhánh "G ≤ ngân phiếu thưởng"; mọi nhánh còn lại thuộc bản có ngân phiếu nạp.

Áp dụng cho cửa hàng ngân phiếu, phí Rèn kỹ và đổi ngân phiếu ra ngân lượng. Quy tắc đầy đủ ở `12_ngan_phieu.md`, mục 4 và 5. Điểm cốt lõi: khi cần cả hai nguồn, máy **không trừ gì** cho tới khi máy chủ xác nhận, và mỗi giao dịch có một mã duy nhất để không bị trừ hai lần.

```mermaid
flowchart TD
  A[Chọn món giá G] --> B{G ≤ ngân phiếu thưởng T?}
  B -->|Có| C[Trừ G từ thưởng ngay trên máy, giao món, lưu]
  B -->|Không| D{Có mạng?}
  D -->|Không| E[Nút vô hiệu: cần kết nối để dùng ngân phiếu nạp]
  D -->|Có| F{Đã đăng nhập?}
  F -->|Chưa| G2[SCR-19, Để sau thì quay lại game]
  F -->|Rồi| H[Tạo mã giao dịch, ghi mục đang chờ, giữ chỗ T]
  G2 -->|Đăng nhập xong| H
  H --> I[Gửi lên máy chủ]
  I -->|Máy chủ trừ G - T từ nạp, trả biên nhận| J[Trừ T, giao món, ghi mã đã áp dụng, lưu]
  I -->|Từ chối| K[Bỏ giữ chỗ, không trừ gì, báo lý do]
  I -->|Mất mạng hoặc tắt game| L[Mục đang chờ ở lại trong file lưu]
  L -->|Lần mở game kế có mạng| M[Hỏi máy chủ kết quả theo mã]
  M -->|Đã trừ| J
  M -->|Chưa có ghi nhận| K
```

## F10 — Hoàn tiền ngân phiếu nạp (bản có ngân phiếu nạp)

```mermaid
flowchart TD
  A[Google Play báo hoàn tiền cho một đơn hàng] --> B{Mã đơn đã xử lý hoàn tiền?}
  B -->|Rồi| C[Bỏ qua, không trừ lần nữa]
  B -->|Chưa| D[Máy chủ trừ ngân phiếu nạp của ô đã nhận, ghi sổ theo mã đơn]
  D --> E{Số dư nạp còn ≥ 0?}
  E -->|Có| F[Không ảnh hưởng gì thêm]
  E -->|Không| G[Số dư âm: khóa giao dịch dùng ngân phiếu nạp]
  G --> H[Lần đồng bộ kế: SCR-13 hiện dòng giải thích]
  G --> I[Lần nạp sau bù phần âm trước]
```

Không thu hồi món đã mua, không khóa gameplay, không đụng tới ngân phiếu thưởng.

## F11 — Đi nhanh bằng bản đồ vùng

```mermaid
flowchart LR
  A[Chạm bản đồ nhỏ ở SCR-05] --> B[SCR-14 Bản đồ vùng]
  B --> C{Đang trong boss, giữ ải, hộ tống, đuổi bắt?}
  C -->|Có| D[Điểm dịch chuyển xám, ghi lý do]
  C -->|Không| E[Chạm điểm dịch chuyển đã mở]
  E --> F[Hộp xác nhận Đi tới ...]
  F -->|Đồng ý| G[SCR-03 Tải bản đồ] --> H[SCR-05 tại điểm đã chọn]
  F -->|Hủy| B
```

## F12 — Đồng bộ và đối chiếu giao dịch (bản có ngân phiếu nạp)

Chạy mỗi lần mở game có mạng và đã đăng nhập, và mỗi khi có mạng trở lại. Không bao giờ chặn gameplay: nếu đang chơi thì chạy ngầm, xong hiện một thông báo nổi. Quy tắc ở `12_ngan_phieu.md`, mục 6.

```mermaid
flowchart TD
  A[Có mạng và đã đăng nhập] --> B[Gửi lệnh xóa đang chờ, giao dịch đang chờ]
  B --> C[Lấy sổ giao dịch của từng ô từ máy chủ]
  C --> D{Mã nào máy chủ có mà file lưu chưa có?}
  D -->|Không có| E[Cập nhật số dư nạp hiển thị, xong]
  D -->|Món vĩnh viễn| F[Cấp lại món còn thiếu]
  D -->|Món tiêu hao, tiền đổi| G[Áp dụng lại một lần, trừ phần thưởng]
  D -->|Dịch vụ Rèn kỹ| H[Máy chủ hoàn ngân phiếu nạp]
  F --> I[Ghi mã vào danh sách đã áp dụng, lưu]
  G --> I
  H --> I
  I --> J[Gửi xác nhận đã áp dụng] --> E
```

## F13 — Mua và khôi phục món vĩnh viễn (bản đầu)

Quy tắc ở `12_ngan_phieu.md`, mục 12. "Cấp" trong sơ đồ nghĩa là cấp theo quyền lợi: quyền lợi sở hữu cấp nếu ô chưa có, quyền lợi cấp một lần (khoản ngân phiếu thưởng của gói khởi đầu) cấp nếu ô chưa có cờ đã nhận.

```mermaid
flowchart TD
  A[SCR-13 thẻ Gói, chọn món] --> B{Có mạng?}
  B -->|Không| C[Nút Mua vô hiệu: cần kết nối để mua]
  B -->|Có| D[Hộp thanh toán Google Play]
  D -->|Hủy hoặc lỗi| A
  D -->|Thanh toán đang chờ| E[Ghi: sẽ nhận khi Google Play xác nhận]
  D -->|Đã trả| F[Cấp món vào ô đang chơi, lưu]
  F --> G[Báo Google Play xác nhận đơn hàng]
  H[Mở game có mạng, hoặc bấm Khôi phục món đã mua] --> I[Hỏi Google Play danh sách món đang sở hữu]
  I --> J{Quyền lợi nào ô chưa có hoặc chưa có cờ đã nhận?}
  J -->|Có| K[Cấp vào ô, lưu, thông báo nổi]
  J -->|Không| L[Không làm gì]
  E --> I
```

Hoàn tiền ở bản đầu: món biến mất khỏi danh sách sở hữu của Google Play; game không thu hồi món đã cấp, chỉ không cấp cho ô chơi mới.

## Tự soát luồng

- Mọi mũi tên đều đi tới một màn có trong `06_screens.md`.
- Mọi điểm rẽ nhánh đều có đủ các nhánh, kể cả nhánh lỗi và mất mạng.
- Không có ngõ cụt: từ mọi màn đều quay về được SCR-05 hoặc SCR-02.
- Những chỗ ghi "cần chốt" được liệt kê lại trong `11_design_freeze.md`.
