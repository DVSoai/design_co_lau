# Design Kit v2.4 — Cờ Lau Khởi Nghĩa

Bộ này dùng để hoàn thiện toàn bộ thiết kế game bằng Codex trước khi code: hình ảnh, mockup màn hình và trạng thái, luồng tương tác, bố cục bản đồ chơi được, đặc tả hoạt ảnh, storyboard nhiệm vụ và cutscene. Thiết kế xong khi qua mốc A của `docs/11_design_freeze.md`.

## Tổ chức repo

- **`design_co_lau`:** lưu tài liệu thiết kế, art nguồn, script và thư mục `prototype/` cho nguyên mẫu A0. Mã A0 là mã bỏ đi, chỉ dùng kiểm chứng thiết kế; không phát triển thành game thật.
- **`co_lau_game`:** repo riêng cho game thật, chỉ tạo sau khi Mốc A được duyệt. Nguyên mẫu A0 không thay thế việc duyệt Mốc A.
- **Chuyển art:** ảnh đã duyệt trong `art/approved/` được chép sang `co_lau_game/assets/` bằng script; mỗi lần chép phải ghi commit nguồn của `design_co_lau` để truy xuất nguồn gốc.
- **Chốt phiên bản:** khi qua Mốc A, gắn tag `design-vX.Y` cho bản thiết kế đã duyệt. Repo game ghi rõ tag thiết kế đang theo và giữ bản sao `docs/GDD.md` lấy từ đúng tag đó.

## Cách bắt đầu

1. Giải nén vào một thư mục riêng, ví dụ `D:\colau-design`, tách khỏi thư mục code game sau này.
2. Cài Python 3 và thư viện Pillow (`pip install pillow`) để chạy script dựng bố cục bản đồ.
3. Mở thư mục bằng Codex. Codex tự đọc `AGENTS.md`.
4. Gõ yêu cầu đầu tiên:

> Đọc AGENTS.md và các file trong docs. Làm giai đoạn 0 trong docs/02_asset_list.md: chạy ba ảnh khám phá phong cách theo khuôn P0, đúng ngoại lệ ghi trong AGENTS.md, lưu vào art/concept, ghi nhật ký, rồi cho tôi xem.

5. Chọn phong cách, làm ảnh gốc Đinh Bộ Lĩnh, rồi đi tiếp từng giai đoạn. Mỗi lần chỉ giao một nhóm nhỏ.

## Trong thư mục có gì

- `AGENTS.md` — luật làm việc cho Codex.
- `docs/01_art_bible.md` — phong cách, bảng màu, kích thước, trang phục, màu cờ.
- `docs/02_asset_list.md` — mọi hạng mục thiết kế, chia 8 giai đoạn sản xuất.
- `docs/03_prompts.md` — khuôn prompt P0 đến P17.
- `docs/04_review.md` — soát ảnh, chuyển thành sprite, bản quyền.
- `docs/05_log.md` — nhật ký thiết kế.
- `docs/06_screens.md` — 22 màn hình, bố cục, trạng thái, mẫu đặc tả.
- `docs/07_ui_flow.md` — 13 luồng tương tác bằng Mermaid.
- `docs/08_map_layout.md` — số đo di chuyển, quy ước lưới, hai bố cục mẫu (Đào Úc, ải Tam Điệp), danh sách 29 bản đồ.
- `docs/09_animation_spec.md` — động tác, số khung, khung gây sát thương cho nhân vật, 20 chiêu, quái, boss, hiệu ứng, giao diện.
- `docs/10_storyboard.md` — 25 cutscene, storyboard đầy đủ Hồi 1, bảng nhịp nhiệm vụ.
- `docs/11_design_freeze.md` — danh sách chốt thiết kế: mốc A trước khi code, mốc B trước khi phát hành.
- `docs/12_ngan_phieu.md` — nguyên tắc offline, hai nguồn ngân phiếu, giao dịch kết hợp, phục hồi giao dịch, hoàn tiền, xóa ô.
- `docs/13_thong_so.md` — mọi thông số và trạng thái Đề xuất, Tạm thời, Đã duyệt.
- `docs/14_online_migration.md` — chuẩn bị cho bản online sau này: id ổn định, luật đi qua lệnh, phiên bản dữ liệu, logic nào lên máy chủ, chuyển nhân vật.
- `docs/GDD.md` — tài liệu thiết kế game đầy đủ, **bản chính thức** (phiên bản 2.4); Word và PDF dựng từ đúng file này.
- `tools/render_layout.py` — dựng file bố cục bản đồ thành ảnh PNG.
- `art/` — ảnh concept, ảnh đã duyệt, ảnh tham chiếu, sprite chỉnh tay.
- `design/` — đặc tả màn hình, luồng, bố cục bản đồ, storyboard.

## Thay đổi ở v2.4

Bản sửa ngày 28/10/2026 (vẫn là v2.4): đồng bộ `14_online_migration.md` với bản đầu không có máy chủ (Google Play giữ quyền sở hữu, bản online xác minh lại, không tin file lưu); thêm mô hình sản phẩm và quyền lợi cho món bán qua Google Play, trong đó khoản ngân phiếu thưởng của gói khởi đầu cấp một lần cho mỗi ô; đánh dấu **[Phạm vi sau]** cho các mục của GDD chỉ dành cho bản có ngân phiếu nạp hoặc bản online.


- Chốt phạm vi bán ở bản đầu: chỉ bán món vĩnh viễn qua Google Play, không có ngân phiếu nạp, không có máy chủ riêng, không có màn đăng nhập. Món đã mua dùng được ở cả ba ô.
- `12_ngan_phieu.md` thêm mục 0 (phạm vi theo phiên bản) và mục 12 (bán món vĩnh viễn); phần ngân phiếu nạp giữ lại, đánh dấu là cho bản sau.
- SCR-13 tách bản đầu (thẻ Cửa hàng ngân phiếu và thẻ Gói) với bản có ngân phiếu nạp; SCR-08 thêm nút Khôi phục món đã mua; thêm luồng F13.
- Danh sách chốt thêm mốc C (trước khi bật ngân phiếu nạp); mốc A và B chỉ còn phạm vi bản đầu.

## Thay đổi ở v2.3

- Thêm `docs/14_online_migration.md` và GDD Phần 6, mục 7: chuẩn bị chuyển online mà không làm phần online bây giờ.
- Sửa mô tả lưu trạng thái số ngẫu nhiên: chặn được tắt game để rèn lại, nhưng không chặn được chép đè file lưu cũ; ghi rõ là giới hạn được chấp nhận.
- `12_ngan_phieu.md` mục 6: tách rõ bảo đảm cho quyền sở hữu vĩnh viễn, vật phẩm tiêu hao và dịch vụ đã thực hiện; ghi rõ giới hạn chống dùng lại vật phẩm tiêu hao khi khôi phục bản lưu cũ.

## Thay đổi ở v2.2

- GDD Phần 6 viết lại cho Godot 4 và GDScript (kiến trúc, dữ liệu, lưu game, thanh toán bằng plugin GodotGooglePlayBilling); bỏ hết Flutter, Flame, Dart.
- `docs/GDD.md` là bản chính thức, có số phiên bản ở dòng đầu; Word và PDF dựng từ đúng file này.
- `12_ngan_phieu.md`: thêm mục 6 phục hồi giao dịch khi file lưu mất, hỏng hoặc quay về bản cũ; viết lại mục 9 xóa ô có liên kết máy chủ (trạng thái chờ đồng bộ xóa, giữ định danh ô trên máy chủ); mục 10 phân biệt kiểm tra toàn vẹn với chống chỉnh sửa.
- SCR-02 thêm trạng thái xóa ô có liên kết máy chủ; F7 vẽ lại; thêm F12 đồng bộ và đối chiếu giao dịch.
- Thêm `13_thong_so.md`: mọi thông số có trạng thái Đề xuất, Tạm thời hoặc Đã duyệt.
- Danh sách chốt mốc A thêm mục thông số và tài liệu nguồn.

## Thay đổi ở v2.1

- Thêm nguyên tắc offline vào `AGENTS.md`: không thiết kế nào bắt có mạng hay đăng nhập để chơi.
- Thêm `docs/12_ngan_phieu.md`: ngân phiếu thưởng tiêu offline, ngân phiếu nạp do máy chủ giữ, cách hiển thị khi offline, giao dịch kết hợp do máy chủ xác nhận với mã chống trừ hai lần, hoàn tiền có sổ chống áp dụng hai lần.
- Bỏ hồi sinh tại chỗ; SCR-14 Bản đồ vùng có đi nhanh; SCR-22 Căn cứ Hoa Lư 4 công trình 3 cấp, không chờ xây; SCR-19 chỉ hiện khi người chơi chủ động.
- Thêm luồng F9 (mua bằng ngân phiếu), F10 (hoàn tiền), F11 (đi nhanh); sửa F3, F4, F8.
- Danh sách chốt tách thành mốc A (trước khi code) và mốc B (trước khi phát hành), ghi lại các quyết định đã chốt ngày 28/10/2026.

## Thay đổi ở v2 so với v1

- Mục tiêu đổi từ "sản xuất hình ảnh" thành "hoàn thiện toàn bộ thiết kế trước khi code", có danh sách chốt thiết kế.
- Ghi rõ các giai đoạn là thứ tự sản xuất thiết kế, không phải thứ tự lập trình.
- Ghi rõ hai ngoại lệ về khối STYLE và AVOID: khuôn P0 và tranh `cs03_3`.
- Thêm đặc tả màn hình và trạng thái, luồng tương tác, bố cục bản đồ, đặc tả hoạt ảnh, storyboard.
- Thêm khuôn P13b (trạng thái màn hình) và P17 (tranh cutscene), script dựng bố cục.
- Giữ nguyên phong cách pixel art chibi, bảng màu, khối STYLE và AVOID, và mô tả nhân vật của v1.
