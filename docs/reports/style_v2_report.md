# STYLE-V2 — bảng thử nhân vật (30/10/2026)

**Chỉ thử phong cách, chưa chọn/duyệt.** Nhánhfeat/style-v2-test từ main4c2e368.
Không sửa thiết kế chuẩn, nhật ký05, asset list, prototype hay reference.
Đây là PNG tạo theo nét vector, **không phải SVG/path vector chỉnh sửa được**.

## Nguyên tắc từ tham khảo cơ chế thể loại (chỉ đọc)

1. Đường bao sẫm và hình khối tương phản giúp tay/chân/vũ khí nổi trên nền;
   yêu cầuSTYLE-V2là viền dày/đều, không lấy đường nét hay màu cụ thể từ nguồn.
2. Mảng tay/chân/nắm tay/bàn chân nên lớn và ít chi tiết, còn đọc được ở96/160px;
   trang phục và búi tóc vẫn là thiết kế Việt của dự án.
3. Dùng ít mảng bóng có ranh giới, tránh đưa vân vải/nét phác vào sprite nhỏ;
   số tông trong prompt là mục tiêu cần soát bằng mắt, không giả là đã đo đủ.
4. Viền/khối phải dùng được khi ghép pose hoặc tách mảnh có đệm khớp; tránh
   nếp/dải qua khuỷu/gối. Lượt này chưa dựng rig nên chưa chứng minh mối ghép kín.
5. Vệt chém có silhouette trắng đặc, cùng pha vũ khí; cung phải đọc rõ lưng/dây.
   Ảnh nguồn được soát chiều; không sao chép hình, mã, bảng số, tên hay trang phục
   nguồn tham khảo vào repo. Không đính kèm ảnh cắt từ nguồn tham khảo.

## Khối STYLE-V2 đã dùng

```text
STYLE-V2: bold clean vector-like cartoon art for a 2D side-scrolling mobile action RPG. Smooth solid dark brown-black outlines, visibly THICK AND UNIFORM, about 2–3 percent of the complete character height, including clear interior contour lines. Large simple solid shapes, FLAT earth colors, 2–3 sharply separated cel-shading tones and one clean highlight. Strong chunky limbs, oversized sturdy fists and broad bare feet, very few LARGE clothing folds. NO fabric grain, NO watercolor/gouache, NO soft painterly blending, NO sketch marks, NO fine hatching, NO tiny noisy details, NO gradients, NO pixel grid. Joint-friendly design: no elaborate folds/straps crossing elbow or knee seams; can later support either whole-pose layers or padded separate 2D skeletal pieces. A simple broad STRAIGHT DOUBLE-EDGED pointed sword, tiny plain crossguard and cord-wrapped grip, outline equally thick as the person. Slash trail is a SOLID OPAQUE WHITE CRESCENT with a thin dark contour, no speckles, blur or glow. A bow curves/bulges toward the enemy at RIGHT; string is behind at LEFT toward the archer. Northern Vietnam, tenth century, undyed cream cloth, earth-brown belt and knee-length pants, tan skin, black hair in a SMALL TOPKNOT. No ornate foreign costume.
```

Mỗi prompt còn có mô tả5tư thế, cận mặt, khóa tỉ lệ và AVOID nguyên văn từ
03_prompts/art bible. V1/V2/V3 là **nhãn mục tiêu prompt**, không chứng nhận tỉ lệ.
Các bảnb/c thay đổi khối/nét/tông trong cùng yêu cầu, không đổi trang phục game.

## Bảng9bản gốc và2bản thay

Tỉ lệ đo từ đỉnh búi đến cằm (KHÔNG tính cổ), chia chiều cao đỉnh búi–đế chân
ở idle. Mốc nguồn đã soát trên PNG và lưu `regions.json`; script chỉ tính phép chia.
Đây là phép đo landmark có sai số, không phải tự động nhận dạng giải phẫu.
Cằm được đối chiếu chỗ đường bao trước mặt thu về cổ. Không co đầu riêng để ép đạt.

| Bản | Mục tiêu (đầu/người) | Người cao bao nhiêu đầu, đo được | Đánh giá |
|---|---:|---:|---|
| v1_a | 1/3 | 3.358 | Đúng chiều kiếm/cung và trang phục; khối tay/chân rõ; chưa gần đủ3đầu. |
| v1_b | 1/3 | 3.534 | Đúng chiều/trang phục; thân–chân chắc; hai tư thế giơ/chém chạm nét ở chân, khó cắt rời; đầu nhỏ hơn mục tiêuV1. |
| v1_c | 1/3 | 3.299 | LOẠI tư thế giơ: mũi kiếm lên–ra trước, sai yêu cầu lên–ra sau. Giữ nguồn; có bảnthay_r1. |
| v2_a | 1/3.5 | 3.106 | Đúng chiều/trang phục; viền cục bộ rõ hơn; đầu lớn hơn mục tiêu3,5, dáng gần3,1đầu. |
| v2_b | 1/3.5 | 3.490 | Đúng chiều/trang phục, ratio gần3,5nhất; khối chạy chắc; nguồn có hai bàn chân giơ/chém chạm nét. |
| v2_c | 1/3.5 | 3.247 | LOẠI tư thế giơ: kiếm chĩa lên–ra trước; giữ nguồn; có bảnthay_r1. |
| v3_a | 1/4 | 3.392 | Đúng chiều/trang phục; dáng giơ khác các bản; chưa tới4đầu, còn nếp áo nhỏ. |
| v3_b | 1/4 | 3.623 | Đúng chiều/trang phục; gần4đầu nhất trong nhómV3 nhưng vẫn lệch; nhiều nếp áo hơn hướng tối giản. |
| v3_c | 1/4 | 3.336 | Đúng chiều/trang phục; khối mạnh nhưng đầu vẫn lớn so với mục tiêu4đầu, posechém hơi quay lưng3/4. |

Bản thay (hai lượt tối đa đã dùng; **không xóa/ghi đè bản sai**):

| Bản | Thay cho | Tỉ lệ đo | Nhận xét |
|---|---|---:|---|
| v1_c_r1 | v1_c | 3.428 | Đã sửa mũi giơ lên–ra sau; thêm quai đeo chéo, nếp áo nhiều hơn mong muốn; chưa đạt3đầu. |
| v2_c_r1 | v2_c | 3.335 | Đã sửa hướng giơ; đúng phục trang cơ bản; tay giơ gần mặt cần soát khi dựng động tác; gần3,34đầu. |

**Hạn chế chung:** cả nhóm chưa thể hiện ba mức đầu3/3,5/4tách biệt như mong muốn.
Các vũ khí/trang phục được soát bằng mắt, không có phép kiểm hướng tự động đáng tin
cho toàn tờ concept. Bóng/mặt vải vẫn có vài mảng chuyển mềm/nếp nhỏ ở một số bản.
Chưa coi bản nào đáp ứng toàn bộSTYLE-V2hoặc sẵn làm tài nguyên game.

## Kiểm viền cục bộ và cỡ hiển thị

Script đo độ dài đoạn sẫm đầu tiên trên3hàng ngang ở cẳng chân của idle:
alpha>127/maxRGB<100, rồi lấy trung vị. Đây là **bề dày chiếu ngang tại3vị trí**,
không phải bề dày vuông góc hay chứng nhận viền đều toàn thân. Nó cho thấy viền
còn thiếu so mục tiêu2–3%H; không sửa ảnh concept hay nới ngưỡng để gọi đạt.

| Bản | Trung vị viền nguồn (px) | % chiều cao người |
|---|---:|---:|
| v1_a | 4 | 0.805% |
| v1_b | 5 | 0.956% |
| v1_c | 5 | 1.031% |
| v2_a | 6 | 1.207% |
| v2_b | 5 | 0.988% |
| v2_c | 5 | 1.055% |
| v3_a | 5 | 0.963% |
| v3_b | 4 | 0.756% |
| v3_c | 5 | 1.027% |
| v1_c_r1 | 4 | 0.846% |
| v2_c_r1 | 5 | 0.967% |

## Hai hướng đề xuất để người dùng chọn tiếp

- **v2_b:** ratio đo gần3,5nhất, khối chạy/nắm tay chắc, tông tách rõ ở160px.
  Đây là đề xuất khuôn nét/khối; cần vẽ dày/đều hơn và tách khoảng trống giữa
  hai tư thế nguồn trước khi dùng cho hoạt ảnh. Không lấy chỗ bàn chân dính làmsprite.
- **v1_a:** mặt và trang phục dễ đọc, ít nếp hơn các bản thiên hình họa, hướng
  vũ khí rõ. Hợp làm seed cho hướng đầu lớn hơn; hiện≈3,36đầu, chưa đúng3đầu.
  Cần tăng/chuẩn hóa viền và quyết lại tỉ lệ khi người dùng chọn.

Đề xuất tương đối trong lượt thử, **không duyệt thay người dùng**. Nếu cần đúng
3mức hình học và độ dày2–3%, phải dựng/chỉnh bản tiếp theo; không giả các nguồn
lần này đã đạt. Đã dùng đủ2bản thay cho lỗi hướng, không sinh quá hạn.

## Bảng duyệt và nguồn tái tạo

- [style_v2_board.png](style_v2_board.png):2220×3355,11hàng (9gốc +2thay).
  Mỗi hàng: nguồn chỉ tách nền rồi thu nhỏ, cận mặt,5tư thế ở160/96px, v9ở160px.
  Nguồn gốc còn nguyên trong art/concept/style_v2, không chỉ lưu ảnh đã xử lý.
- [style_v2_160.png](style_v2_160.png):1620×260,đúng9vị trí160px, với v1_c_r1/
  v2_c_r1thay hai bản sai ở vị trí tương ứng. Tên file bản thật được ghi trên ảnh.
- [regions.json](../../art/concept/style_v2/regions.json): thành phần/mốc thân/cằm/đế;
  [measurements.json](../../art/concept/style_v2/measurements.json): hash, scale,
  tọa độ paste và số đo thực từscript.

160/96px lấy theo chiều cao **người**, không lấy cả mũi kiếm/vệt. Co đồng dạng
LANCZOS, không xoay/co giãn từng bộ phận. Mốc búi/đế cho từng tư thế chọn bằng
mắt trên ảnh nguồn; số hiển thị là span landmark, không phải đoGPUhay thử máy.
Hai nguồnv1_b/v2_bcó chân giơ/chém chạm nét: board phân vùng tại đường đã ghi
để xem từng tư thế, không vẽ bù pixel, không coi đây làspriteđã kín/đã đạt.
Nền lấy từ project: clearColor(0,14;0,19;0,23) và đất#7d5537củaĐàoÚcgreybox;
không sửa/chụp lại prototype. Ảnhv9là góc nghiêng thật trongref_dinh_bo_linh.png.

[tools/style_board.py](../../tools/style_board.py) chỉ key alpha mềm/khử xanh,
cắt theo mask/mốc, resize/ghép/ghi nhãn bằngPIL. **Không imagegencho bảng/kết quả.**
[tools/check_style_board.py](../../tools/check_style_board.py) đếm xanh tại alpha>0,
kiểm hash nguồn, hai kích thước bảng và các hệ số hiển thị.
[Nguyên đầu ra](style_v2_checks.txt); cũng chép vào commit message.
[Nhật ký/prompt nguyên văn](style_v2_log.md) là nhật ký tạm; không sửa05_log.md.
