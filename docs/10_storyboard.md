# Storyboard nhiệm vụ và cutscene

Theo Phần 6 của GDD, cutscene là **tranh tĩnh chuyển cảnh** chứ không phải hoạt hình đầy đủ: mỗi cutscene gồm 3 đến 6 tranh, có lia và phóng camera chậm, lời thoại chạy ở khung dưới (màn SCR-18). Tài liệu này có hai phần: storyboard cutscene, và bảng nhịp nhiệm vụ (mỗi nhiệm vụ chính diễn ra thế nào trên bản đồ).

Lời thoại chi tiết chưa viết (GDD ghi đây là việc còn phải chốt). Ở đây mỗi câu chỉ ghi **ý cần nói**; bản lời thoại thật viết sau, theo đúng ý này.

Mỗi tranh trong cutscene là một hạng mục ảnh mã `cs<số>_<tranh>` (ví dụ `cs01_1`), tạo bằng khuôn P17 trong `03_prompts.md`, cỡ 960×540, cùng phong cách game nhưng chi tiết hơn sprite.

Nhãn nguồn giữ đúng như GDD: *theo chính sử*, *theo giai thoại*, *mở rộng cho game*.

## 1. Danh sách cutscene

| Mã | Nhiệm vụ | Nội dung | Nguồn | Số tranh |
|---|---|---|---|---|
| CS01 | 1 | Cờ lau tập trận: Bộ Lĩnh nhỏ cầm cờ lau chỉ huy lũ trẻ chăn trâu | Theo giai thoại | 5 |
| CS02 | 3 | Mổ trâu khao quân | Theo giai thoại | 4 |
| CS03 | 3 | Cầu gãy và rồng vàng che chở | Theo giai thoại | 4 |
| CS04 | 9 | Tụ nghĩa Đào Úc với Đinh Điền, Nguyễn Bặc | Theo chính sử (họ là bạn đồng hương), chi tiết mở rộng | 4 |
| CS05 | 14 | Ngọn sào Đinh Liễn | Theo chính sử | 5 |
| CS06 | 15 | Quân Hậu Ngô rút lui, kết Hồi 1 | Mở rộng cho game | 3 |
| CS07 | 17 | Ra mắt Trần Lãm ở Bố Hải Khẩu | Theo chính sử, chi tiết mở rộng | 4 |
| CS08 | 25 | Trần Lãm nhận Bộ Lĩnh làm con nuôi | Theo chính sử | 4 |
| CS09 | 27 | Trần Lãm mất, Bộ Lĩnh thừa kế binh quyền | Theo chính sử | 5 |
| CS10 | 29 | Gặp Lê Hoàn | Theo chính sử (Lê Hoàn theo Đinh Liễn), chi tiết mở rộng | 3 |
| CS11 | 31 | Phạm Bạch Hổ quy phục sau đấu danh dự | Theo chính sử (quy phục), trận đấu mở rộng | 4 |
| CS12 | 34 | Ngô Xương Xí quy phục | Theo chính sử (quy phục), chi tiết mở rộng | 4 |
| CS13 | 37 | Nguyễn Bặc trải bản đồ tám sứ quân | Mở rộng cho game | 4 |
| CS14–CS21 | 39–54 | Kết cục từng sứ quân sau trận boss: Đỗ Cảnh Thạc, Nguyễn Siêu, Lã Đường, Lý Khuê, Nguyễn Thủ Tiệp, Nguyễn Khoan, Kiều Công Hãn, Kiều Thuận | Kết cục theo chính sử, cảnh mở rộng | 2 mỗi cảnh |
| CS22 | 48 | Nghị hòa Đường Lâm, Ngô Nhật Khánh quy phục | Theo chính sử (quy phục), chi tiết mở rộng | 4 |
| CS23 | 55 | Binh sĩ tôn hiệu Vạn Thắng Vương | Theo chính sử | 4 |
| CS24 | 59 | Lễ lên ngôi năm 968, quốc hiệu Đại Cồ Việt, đóng đô Hoa Lư | Theo chính sử | 6 |
| CS25 | 59 | Epilogue 968–979, kể ngắn, kết bằng lũ trẻ hát về ông vua cờ lau | Theo chính sử, cảnh cuối mở rộng | 5 |

## 2. Mẫu storyboard

Mỗi cutscene có file `design/storyboards/cs<số>.md`:

- **Mã, nhiệm vụ, bản đồ, nhân vật xuất hiện, nguồn.**
- **Mục tiêu cảm xúc** — một câu: người chơi phải thấy gì sau cảnh này.
- **Từng tranh:** khung hình (toàn cảnh, trung cảnh, cận cảnh); nội dung tranh; chuyển động camera (đứng yên, lia trái sang phải, phóng chậm vào…); âm thanh và nhạc; lời thoại (ý); thời lượng (giây, khi tự chạy).
- **Chuyển cảnh vào và ra:** cutscene nối vào màn chơi ở đâu.

## 3. Storyboard Hồi 1 (giai đoạn 2)

### CS01 — Cờ lau tập trận

Nhiệm vụ 1, cánh đồng ven làng Hoa Lư. Nhân vật: Bộ Lĩnh lúc nhỏ, lũ trẻ chăn trâu, mẹ Đàm thị. Mục tiêu cảm xúc: cậu bé chăn trâu có khí chất thủ lĩnh, và bông lau là biểu tượng của cả câu chuyện.

1. **Toàn cảnh**, bình minh trên núi đá vôi Hoa Lư soi bóng xuống đầm nước, đàn trâu gặm cỏ. Camera lia chậm từ trái sang phải. Sáo trúc mở đầu chủ đề nhạc. Không lời. 5 giây.
2. **Trung cảnh**, lũ trẻ chia hai phe trên bờ ruộng, đứa nào cũng cầm que tre. Phóng chậm vào. Tiếng trẻ hò reo. Ý: lũ trẻ cãi nhau ai làm tướng. 4 giây.
3. **Cận cảnh**, bàn tay Bộ Lĩnh bẻ một bông lau trắng giơ lên. Đứng yên. Gió thổi bông lau. Ý: Bộ Lĩnh nói lấy bông lau làm cờ, ai theo cờ thì là quân mình. 4 giây.
4. **Trung cảnh**, lũ trẻ khoanh tay làm kiệu khiêng Bộ Lĩnh, hai bên cầm hoa lau làm cờ. Lia theo đoàn. Đồng dao do lũ trẻ hát (tự sáng tác). 5 giây.
5. **Toàn cảnh**, mẹ Đàm thị đứng ở cổng làng nhìn ra cánh đồng. Đứng yên, mờ dần vào màn chơi. Ý: mẹ gọi con về, dặn đừng quên trông trâu nhà chú. 4 giây.

Chuyển vào màn chơi: Bộ Lĩnh cầm cờ lau đứng giữa bãi bù nhìn rơm, nhiệm vụ 1 bắt đầu (đánh ngã 10 bù nhìn).

### CS02 — Mổ trâu khao quân

Nhiệm vụ 3, bờ ruộng chiều tối. Nhân vật: Bộ Lĩnh, lũ trẻ, người chú. Mục tiêu cảm xúc: cậu bé dám làm việc lớn và chịu hậu quả; người chú khắc nghiệt nhưng không phải ác nhân.

1. **Trung cảnh**, lũ trẻ ngồi quanh đống lửa giữa đồng, đói và mệt sau trận giả. Lửa bập bùng. Ý: lũ trẻ than đói. 4 giây.
2. **Cận cảnh**, Bộ Lĩnh nhìn con trâu nhà chú, rồi quyết định. Không cho thấy cảnh giết trâu; chỉ cho thấy dao và ánh mắt. Tiếng trống trầm một nhịp. 4 giây.
3. **Toàn cảnh**, lũ trẻ ăn uống vui vẻ quanh lửa, Bộ Lĩnh ngồi ở giữa. Đàn bầu nhẹ. Ý: Bộ Lĩnh nói tướng phải lo cho quân no. 4 giây.
4. **Trung cảnh**, người chú cầm dao đứng trên bờ ruộng, giận dữ, bóng dài đổ xuống. Nhạc dồn. Ý: người chú quát hỏi trâu đâu. 3 giây.

Chuyển vào màn chơi: đuổi bắt, người chơi chạy thoát người chú qua cánh đồng tới bờ sông.

### CS03 — Cầu gãy và rồng vàng

Nhiệm vụ 3, bờ sông, đêm. Đây là cảnh huyền thoại duy nhất của game, phải được trình bày rõ là giai thoại: tranh nhòe như ký ức, có dòng chữ dẫn "Tương truyền…". Mục tiêu cảm xúc: ý niệm "mệnh trời" gắn với Bộ Lĩnh, mà không biến game thành truyện thần tiên.

1. **Trung cảnh**, Bộ Lĩnh chạy lên cầu tre, cầu gãy giữa chừng. Khựng hình. Tiếng tre gãy. 3 giây.
2. **Toàn cảnh**, cậu bé ngã xuống bùn ven sông, người chú đuổi tới bờ. Mưa nhẹ. 3 giây.
3. **Cận cảnh, tranh nhòe ánh vàng**, hình rồng vàng mờ ảo uốn quanh cậu bé trong bùn. Dòng dẫn: "Tương truyền, người chú thấy có rồng vàng che phủ cậu bé." Tiếng chiêng ngân xa. 5 giây.
4. **Trung cảnh**, người chú lùi lại, buông dao, quay đi. Mờ dần. Ý: người chú kinh hãi, từ đó không dám làm hại cháu. 4 giây.

Chuyển vào màn chơi: sáng hôm sau, Bộ Lĩnh tỉnh dậy ở chùa làng; nhiệm vụ 4 bắt đầu.

### CS04 — Tụ nghĩa Đào Úc

Nhiệm vụ 9, trại Đào Úc. Nhân vật: Bộ Lĩnh (đã lớn), Đinh Điền, Nguyễn Bặc. Mục tiêu cảm xúc: những người bạn đầu tiên đi theo vì phục tài, không vì quyền.

1. **Toàn cảnh**, trại tre ở Đào Úc, vài chục trai làng tập giáo. Lia chậm. Trống tập. 4 giây.
2. **Trung cảnh**, Đinh Điền cầm gậy gỗ thách đấu, Bộ Lĩnh nhận lời. Ý: Đinh Điền nói chỉ theo người thắng được mình. 3 giây.
3. **Trung cảnh** (sau trận đấu tay đôi trong màn chơi), Đinh Điền ngồi bệt dưới đất, cười lớn. Ý: Đinh Điền xin theo. 3 giây.
4. **Cận cảnh**, Nguyễn Bặc đặt ba thẻ tre lên bàn. Ý: Nguyễn Bặc hỏi ba câu về cách dùng người; trả lời xong thì ông theo. 4 giây.

Ghi chú: trận đấu tay đôi và ba câu hỏi diễn ra trong màn chơi giữa tranh 2 và 3, và sau tranh 4.

### CS05 — Ngọn sào Đinh Liễn

Nhiệm vụ 14, cổng Đào Úc. Nhân vật: Bộ Lĩnh, Đinh Liễn, tướng Hậu Ngô. Theo chính sử, khi quân nhà Ngô đánh Hoa Lư, Đinh Liễn đang làm con tin bị treo lên ngọn sào để ép Bộ Lĩnh hàng. Bộ Lĩnh không hàng; quân Ngô không giết Liễn. Mục tiêu cảm xúc: cái giá của chí lớn, và sự cứng rắn của Bộ Lĩnh mà sử ghi lại. Không có máu, không có cảnh hành hạ.

1. **Toàn cảnh**, quân Hậu Ngô dàn trước cổng Đào Úc, cờ đỏ nâu. Trống trận. 4 giây.
2. **Trung cảnh, nhìn lên**, Đinh Liễn bị trói treo trên ngọn sào tre cao giữa trận Ngô. Gió. 4 giây.
3. **Cận cảnh**, gương mặt Bộ Lĩnh trên lũy, nắm chặt cờ lau. Im lặng, chỉ có gió. Ý: tướng Ngô ra điều kiện hàng thì tha con. 4 giây.
4. **Trung cảnh**, Bộ Lĩnh giơ cờ ra lệnh giữ thành. Ý: Bộ Lĩnh trả lời rằng việc lớn không thể vì một đứa con mà bỏ. 4 giây.
5. **Toàn cảnh**, quân Ngô hạ sào, đưa Đinh Liễn về trại; quân Ngô bắt đầu công cổng. 3 giây.

Chuyển vào màn chơi: giữ ba cổng Đào Úc trước ba đợt quân Hậu Ngô.

Lưu ý khi viết lời thoại: cần đối chiếu đúng câu ghi trong *Đại Việt sử ký toàn thư* và chỉ dùng ý, không chép nguyên văn bản dịch hiện đại có bản quyền.

### CS06 — Quân Ngô rút lui

Nhiệm vụ 15, sau khi thắng tướng tiên phong Hậu Ngô. Mục tiêu cảm xúc: chiến thắng đầu tiên, và thời loạn mới chỉ bắt đầu.

1. **Toàn cảnh**, quân Ngô rút qua cánh đồng, cờ đỏ nâu ngả nghiêng. 4 giây.
2. **Trung cảnh**, Bộ Lĩnh, Đinh Điền, Nguyễn Bặc đứng trên lũy, cờ lau tung bay. Trống chiến thắng. 4 giây.
3. **Cận cảnh**, Nguyễn Bặc mở thư báo tin nhà Ngô suy yếu, các sứ quân nổi lên khắp nơi. Ý: phải xuống Bố Hải Khẩu tìm Trần Lãm. Mờ dần sang SCR-03 tải vùng ven biển. 5 giây.

## 4. Bảng nhịp nhiệm vụ

Mỗi nhiệm vụ chính có một mục ngắn: mở đầu (ai giao, ở đâu, vì sao), giữa (người chơi làm gì trên bản đồ nào, khó ở đâu), kết (phần thưởng, mở khóa, cutscene). Bảng nhịp lưu ở `design/storyboards/beats_hoi<số>.md`. Dưới đây là Hồi 1 làm mẫu; nội dung các bước lấy từ bảng nhiệm vụ ở Phần 3 GDD.

1. **Cờ lau tập trận** — CS01; đánh ngã 10 bù nhìn ở làng; mở đòn đánh và di chuyển.
2. **Con trâu nhà chú** — mẹ nhờ tìm trâu lạc ở cánh đồng chiêm; cưỡi trâu lùa 3 con về chuồng; mở thú cưỡi trâu.
3. **Mổ trâu khao quân** — CS02; màn đuổi bắt qua đồng tới bờ sông; CS03.
4. **Chào làng Hoa Lư** — Nguyễn Bặc dẫn đi chào thợ rèn, bà hàng cơm, ông lang, thợ may, sư trụ trì; mở các cửa hàng.
5. **Lương thực đầu tiên** — mua và ăn 2 cơm nắm; đánh chuột đồng, rắn nước; dạy thức ăn hồi máu.
6. **Vật liệu làm giáp** — nhặt da lợn rừng, lông nhím ở bến đò; nhận bộ giáp đầu tiên, dạy mặc đồ.
7. **Hái thuốc cứu người** — nhặt lá thuốc nam; dạy thuốc hồi phục và ô dùng nhanh.
8. **Thám thính quanh Hoa Lư** — đi tới bến đò, Tràng An, cánh đồng chiêm; mở bản đồ khu vực.
9. **Tụ nghĩa Đào Úc** — CS04; đấu tay đôi với Đinh Điền; trả lời ba câu hỏi của Nguyễn Bặc.
10. **Chọn binh pháp** — SCR-04 chọn phái; cộng điểm tiềm năng và kỹ năng có hướng dẫn.
11. **Bài học đầu tiên** — đánh chuột cống lớn, lợn rừng, hổ con; nhiệm vụ đánh quái đầu tiên dùng chiêu.
12. **Rèn lại binh khí** — cường hóa vũ khí, trang sức, y phục mỗi thứ một lần ở thợ rèn; mở cường hóa và luyện đá.
13. **Hào trưởng quanh vùng** — thắng 3 hào trưởng nhỏ; nhận danh hiệu Nghĩa sĩ.
14. **Ngọn sào Đinh Liễn** — CS05; giữ ba cổng Đào Úc trước ba đợt quân Hậu Ngô.
15. **Quân Ngô rút lui** — đánh tướng tiên phong Hậu Ngô; CS06; mở Hồi 2 và vùng ven biển.

## 5. Tự soát

- Mỗi cutscene có mục tiêu cảm xúc và nhãn nguồn.
- Không có máu me, hành hạ hay cảnh giết con vật hiện rõ.
- Cảnh huyền thoại duy nhất (CS03) được trình bày rõ là giai thoại.
- Mỗi tranh có khung hình, camera, âm thanh và ý lời thoại.
- Bảng nhịp khớp với bảng nhiệm vụ trong GDD về thứ tự, bản đồ và mở khóa.
