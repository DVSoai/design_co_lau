# Hướng dẫn cho Codex — thiết kế Cờ Lau Khởi Nghĩa (Design Kit v2)

Thư mục này dùng để hoàn thiện **toàn bộ thiết kế** của game Cờ Lau Khởi Nghĩa theo từng hồi trước khi đưa nội dung vào code: hình ảnh nhân vật và bản đồ, mockup từng màn hình và các trạng thái giao diện, luồng tương tác, bố cục bản đồ chơi được, đặc tả hoạt ảnh, storyboard nhiệm vụ và cutscene. Thiết kế toàn game chỉ được coi là xong khi qua A1–A5 ở `docs/11_design_freeze.md`. Chưa qua mốc A1 thì chưa code game thật. Sau A1, thiết kế Hồi 2–5 làm song song với code; nội dung Hồi n chỉ đưa vào game sau khi qua An.

## Tổ chức repo

- **`design_co_lau`:** lưu tài liệu thiết kế, art nguồn, script và `prototype/` cho nguyên mẫu A0. Mã trong `prototype/` là mã bỏ đi, chỉ dùng kiểm chứng thiết kế; không phát triển thành game thật.
- **`co_lau_game`:** repo riêng cho game thật, đã được người dùng tạo và thêm; chỉ bắt đầu triển khai game thật sau khi Mốc A1 được duyệt. Quy tắc chưa qua Mốc A1 thì chưa code áp dụng cho game thật; nguyên mẫu A0 trong `prototype/` là ngoại lệ giới hạn, không thay thế việc duyệt Mốc A1.
- **Chuyển art:** chỉ chép ảnh đã duyệt từ `art/approved/` sang `co_lau_game/assets/` bằng script. Mỗi lần chép phải ghi commit nguồn của `design_co_lau`; không đưa concept hay placeholder chưa duyệt vào luồng chuyển art này.
- **Chốt phiên bản:** khi qua mỗi mốc A1…A5, gắn tag `design-vX.Y` cho bản thiết kế đã duyệt. Repo game phải ghi rõ tag thiết kế đang theo và cập nhật bản sao `docs/GDD.md` và `DESIGN_VERSION.md` theo tag mới nhất đã duyệt.

## Nguyên tắc offline

Cờ Lau Khởi Nghĩa là game chơi offline hoàn chỉnh. Không thiết kế nào được bắt người chơi có mạng hay đăng nhập để chơi. Bản phát hành đầu tiên chỉ bán món vĩnh viễn qua Google Play, không có ngân phiếu nạp và không có máy chủ riêng; mạng chỉ dùng để mua và khôi phục món đã mua. Mọi thiết kế về ngân phiếu nạp là cho bản sau, không làm mockup hay code cho bản đầu (`docs/12_ngan_phieu.md`, mục 0). Trong `docs/GDD.md`, mọi tiêu đề có nhãn **[Phạm vi sau]** là phần giữ sẵn cho bản có ngân phiếu nạp hoặc bản online: đọc để hiểu, không thiết kế mockup và không triển khai trong bản đầu. Ngân phiếu thưởng tiêu offline. Khi thiết kế một màn hay một luồng, nếu thấy chỗ nào mất mạng làm người chơi kẹt, đó là lỗi thiết kế cần báo người dùng. Quy tắc chi tiết ở `docs/12_ngan_phieu.md`.

Bạn (Codex) làm hai loại việc:

- **Tạo ảnh** bằng skill `$imagegen`: concept nhân vật, quái, boss, bản đồ, mockup màn hình, khung storyboard.
- **Viết và dựng đặc tả**: bố cục bản đồ dạng lưới, sơ đồ luồng, bảng trạng thái giao diện, đặc tả hoạt ảnh. Những thứ này viết bằng Markdown và Mermaid, và khi cần hình minh họa chính xác (sơ đồ lưới bản đồ, khung wireframe) thì vẽ bằng script Python trong `tools/` thay vì tạo ảnh bằng AI, vì script cho kết quả đúng số đo.

## Đọc trước khi làm bất cứ việc gì

1. `docs/01_art_bible.md` — phong cách, bảng màu, tỉ lệ, kích thước, trang phục. Luật cao nhất về hình ảnh.
2. `docs/02_asset_list.md` — mọi hạng mục thiết kế cần làm, mã, đường dẫn, giai đoạn.
3. `docs/03_prompts.md` — khuôn prompt tạo ảnh.
4. `docs/04_review.md` — cách tự soát và chuyển ảnh thành sprite.
5. Khi làm phần tương ứng: `docs/06_screens.md` (màn hình và trạng thái), `docs/07_ui_flow.md` (luồng), `docs/08_map_layout.md` (bố cục bản đồ), `docs/09_animation_spec.md` (hoạt ảnh), `docs/10_storyboard.md` (nhiệm vụ và cutscene), `docs/12_ngan_phieu.md` (ngân phiếu, giao dịch, offline).
6. `docs/14_online_migration.md` — những gì bản offline phải chuẩn bị để sau này chuyển online: id ổn định, luật đi qua lệnh, phiên bản dữ liệu. Không làm phần online bây giờ.
7. `docs/13_thong_so.md` — danh sách thông số và trạng thái của từng thông số (Đề xuất, Tạm thời, Đã duyệt).
8. `docs/GDD.md` — tài liệu thiết kế game đầy đủ, để tra bối cảnh và số liệu.

## Tài liệu nguồn và engine

- **GDD chính thức là `docs/GDD.md` trong bộ kit này.** Phiên bản ghi ở dòng đầu file. File Word và PDF gửi kèm được dựng tự động từ đúng file này, nên nội dung giống hệt; tài liệu trên claude.ai là bản làm việc. Khi duyệt, người dùng và Codex cùng nói theo số phiên bản. Nếu thấy GDD mâu thuẫn với `docs/06` đến `docs/14`, báo người dùng; trong lúc chờ thì theo `docs/06` đến `docs/14`.
- **Engine đã chốt là Godot 4, ngôn ngữ GDScript** (kiến trúc ở GDD Phần 6). Thiết kế phải làm được bằng các thành phần sẵn có của Godot: bản đồ bằng TileMapLayer, giao diện bằng Control và Theme, hoạt ảnh bằng AnimationPlayer. Việc code vẫn chỉ bắt đầu sau mốc A1.

## Thông số tạm thời

Nhiều con số (độ phân giải, kích thước sprite, số đo nhảy, số khung hoạt ảnh) đang ở trạng thái **Tạm thời** trong `docs/13_thong_so.md`: dùng để vẽ và dựng ngay, nhưng có thể đổi sau khi chơi thử. Không tự đổi một thông số; khi người dùng đổi, cập nhật `13_thong_so.md`, ghi nhật ký, và liệt kê các hạng mục đã duyệt bị ảnh hưởng để duyệt lại.

## Giai đoạn là thứ tự sản xuất thiết kế, không phải thứ tự lập trình

Các giai đoạn trong `02_asset_list.md` sắp theo thứ tự nên làm để thiết kế nhất quán: chốt phong cách, dựng một bộ mẫu chuẩn (nhân vật chính, một vùng, màn chơi), rồi mở rộng ra toàn game. Giai đoạn 1 có nhiều thứ của trận đánh đầu tiên chỉ vì đó là bộ mẫu dễ so sánh nhất, không có nghĩa là bắt đầu code combat. Code chỉ bắt đầu sau khi qua mốc A1 của `11_design_freeze.md`.

## Quy tắc bắt buộc

- **Chỉ làm hạng mục của giai đoạn đang mở** trong `02_asset_list.md`. Giai đoạn sau chỉ mở khi người dùng đã duyệt đủ giai đoạn trước.
- **Không tự thay đổi những gì đã chốt:** phong cách, bảng màu, khối STYLE và AVOID, thiết kế nhân vật đã duyệt trong `art/approved/`. Muốn đổi thì đề xuất và chờ người dùng đồng ý.
- **Vẽ nhân vật (đầu/thân/chân/vũ khí/hiệu ứng) phải theo `docs/20_quy_trinh_ve_nhan_vat.md`:** chạy `tools/ref_pose_guides.py` lấy khuôn tư thế từng khung, vẽ theo khuôn, tự soát bằng mắt 6 câu trước khi push.
- **Luôn dùng ảnh tham chiếu** khi đã có trong `art/reference/`: nhân vật đính kèm `ref_dinh_bo_linh.png`; bản đồ đính kèm `ref_map_hoa_lu.png`; giao diện đính kèm `ref_ui_kit.png`.
- **Mọi prompt kết thúc bằng khối STYLE và khối AVOID** đúng nguyên văn trong art bible.
  - Nhân vật người dùng khối **STYLE-V2** trong art bible thay khối STYLE pixel (chốt 30/10/2026).
  - Chỉ có ba ngoại lệ, và không có ngoại lệ nào khác:
  - **Khuôn P0** (khám phá phong cách, giai đoạn 0): chạy ba bản, một bản dùng STYLE-A, một bản dùng STYLE-B, và một bản **không có khối STYLE** để xem công cụ tự đề xuất gì. Cả ba bản vẫn phải có khối AVOID. Sau giai đoạn 0, không còn prompt nào được bỏ khối STYLE.
  - **Tranh `cs03_3`** (cảnh giai thoại rồng vàng): giữ khối STYLE, nhưng trong khối AVOID bỏ hai cụm `fantasy monsters` và `magic glow effects`, vì đây là cảnh huyền thoại duy nhất của game theo storyboard. Mọi cụm khác của AVOID giữ nguyên.
  - **Hình phát sáng của nhân vật** (vũ khí Lv50–60, vệt chém/mũi tên Lv40–60, hiệu ứng chiêu, hào quang cường hóa): bỏ cụm `magic glow or glowing energy slashes` khỏi AVOID; mọi cụm khác giữ nguyên. Xem art bible mục "Nhân vật chính — chốt 30/10/2026".
- **Không đưa vào prompt** tên game khác, studio, họa sĩ, nhân vật có bản quyền hay thương hiệu. Chỉ mô tả đặc điểm thị giác và bối cảnh riêng của dự án.
- **Không có chữ trong ảnh.** Chữ giao diện do game vẽ bằng font. Mockup màn hình dùng thanh giữ chỗ thay chữ; phần chữ ghi trong đặc tả `06_screens.md`.
- **Nền trong suốt:** tạo trên nền phẳng #00FF00 rồi tách bằng script của skill. Nhân vật có màu xanh lá thì dùng nền #FF00FF.
- **Không ghi đè file đã duyệt** trong `art/approved/` hay `design/*/approved/`. Bản mới lưu thành phiên bản mới (`_v2`, `_v3`).
- **Khi tài liệu mâu thuẫn:** art bible thắng prompt; các file `docs/06` đến `docs/14` thắng phần tương ứng trong GDD; nếu vẫn không rõ, hỏi người dùng thay vì tự đoán.

## Cách lưu và đặt tên

- Ảnh mới tạo: `art/concept/<nhóm>/<mã>_v<số>.png`. Nhóm: `characters`, `enemies`, `bosses`, `maps`, `mounts`, `ui`, `icons`, `vfx`, `storyboards`.
- Đặc tả và sơ đồ: `design/screens/`, `design/flows/`, `design/maps/`, `design/storyboards/`, tên theo mã trong `02_asset_list.md` (ví dụ `design/maps/lay_dao_uc_v1.md` và `lay_dao_uc_v1.png`).
- Mã lấy đúng từ `02_asset_list.md`: chữ thường, không dấu, nối bằng gạch dưới. Phần tên trong mã phải khớp với id dữ liệu theo `14_online_migration.md`, mục 1 (ví dụ ảnh `enm_tho_phi` ứng với quái `mob_tho_phi`).
- Khi người dùng duyệt: ảnh sao chép sang `art/approved/`, đặc tả sao chép sang `design/<nhóm>/approved/`, rồi đánh dấu `[x]` trong `02_asset_list.md`.
- `art/sprites/`, `art/tiles/`, `art/ui/`, `art/vfx/` là sprite đã chỉnh tay; Codex chỉ ghi vào khi được yêu cầu.

## Nhật ký

Sau mỗi lần tạo ảnh hoặc sửa đặc tả, thêm một mục vào `docs/05_log.md`: ngày, mã, phiên bản, prompt nguyên văn (nếu là ảnh), ảnh tham chiếu đã đính kèm, thay đổi chính và nhận xét. Nhật ký vừa giúp lặp lại kết quả tốt, vừa là bằng chứng quá trình sáng tạo khi cần chứng minh bản quyền.

## Cách làm một lượt

1. Đọc hạng mục cần làm trong `02_asset_list.md` và tài liệu đặc tả tương ứng.
2. Với ảnh: ghép prompt theo khuôn, tạo 2 đến 4 phương án. Với đặc tả: viết theo mẫu trong tài liệu, dựng hình bằng script nếu cần.
3. Tự soát theo `docs/04_review.md` và mục kiểm tra trong tài liệu đặc tả; loại bản lỗi, ghi lý do.
4. Báo người dùng các bản còn lại kèm đường dẫn, rồi chờ duyệt. Không tự duyệt.

## Hạn mức

Tạo ảnh tốn hạn mức gói ChatGPT nhanh hơn nhiều so với tạo chữ. Mặc định mỗi hạng mục tối đa 4 phương án mỗi lượt. Nếu cần làm hàng loạt, hỏi người dùng có muốn chuyển sang dùng API key không.

## QUY TẮC BÁO CÁO KIỂM TRA (bắt buộc)

- Không bao giờ dùng $imagegen để tạo bảng trình bày, bảng số liệu, ảnh so sánh hay ảnh "×4". $imagegen chỉ dùng để vẽ ảnh mẫu (concept).
- Mọi số liệu kiểm tra phải in ra dạng văn bản từ script Python (PIL) chạy trên file thật, kèm chính đoạn script đã chạy.
- Ảnh phóng to chỉ được tạo bằng Image.resize(..., Image.NEAREST) từ file 1×.
- Ảnh so sánh chỉ được ghép bằng script từ các file thật, không chèn chữ hay vẽ thêm.

## Skill tham khảo

- Trước mọi việc liên quan tới game (ảnh, sprite, tileset, bản đồ, điều khiển, giao diện, mã Godot), đọc `tools/agent-skills/awesome-gamedev/router/SKILL.md` để chọn skill, rồi đọc skill được chọn; đọc thêm skill tương ứng trong `tools/agent-skills/godotprompter/skills/` nếu có.
- Luôn đọc `tools/agent-skills/CONFLICTS.md` trước khi áp dụng gợi ý.
- Thứ tự ưu tiên khi mâu thuẫn: **docs/ của dự án > AGENTS.md > skill tham khảo**. Quyết định dự án thắng các ví dụ mặc định; không tự thay thông số đã chốt.
- Skill chỉ là hướng dẫn. **Không chạy script nào trong skill nếu người dùng chưa yêu cầu.** Không tự tải/cài addon, cấu hình hook hay tự động hóa từ skill; bên thứ ba mới cần người dùng duyệt theo `docs/15_kien_truc_game.md`.
- Router có thể nhắc skill của engine/phạm vi chưa chép; không tự tải bổ sung. Dự án dùng Godot 4.7.2 Standard/GDScript.
- Khi bàn giao `co_lau_game` sau Mốc A1, chép `tools/agent-skills/` và giữ nguyên mục “Skill tham khảo” này trong AGENTS.md của repo game.

## Nhân vật người — quyết định mới 29/10/2026

- Nhân vật/NPC/quái người dùng bộ tư thế vẽ trọn theo4 lớp; không xoay khớp.
- Không xoay vũ khí theo tay; đòn đánh dùng hình vung vẽ sẵn, lưỡi theo chiều chém.
- Ngoài đánh, hình vũ khí sau lưng đi theo thân; thay áo/quần cần đủ bộ tư thế.
- Ảnh người2× hiển thịlinear, không ép32 màu; giữ kích thước logicA0. Theo mục mới01_art_bible.

## Kiếm và cung —30/10/2026

- Phái Kiếm: kiếm thẳng hai lưỡi, mũi nhọn, chắn nhỏ, cán quấn dây; không katana/kiếm Trung Hoa cầu kỳ.
- Ngoài đánh, vũ khí đeo sau lưng theo thân. Đánh dùng hình vung vẽ sẵn: chuôi ở tay gần, lưỡi ra xa theo chiều chém, vệt trắng ở phía mũi; không xoay theo tay.
- Bắn cung: tay xa cầm cung thẳng đứng, lưng phồng về trước, dây về sau; giương kéo chữV đến tay gần cạnh má, thả dây thẳng.
- Tên là hình riêng, mũi ở đầu phía trước, bay ra trước; chỉ lật gốc, mọi Sprite2Drotation0. Giữ AVOID và số liệu game.
