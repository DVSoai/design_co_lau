# G1 — Kiếm/Cung (30/10/2026), bản thử chưa duyệt

Nhánh `feat/g1-kiem-cung` từ main `4c2e368` (PR23 đã merge).
Đổi tên phái/vũ khí sang Kiếm, Trảm Kiếm/ Kiếm Tâm; giữ số liệu/cơ chế/chiêu khác.
Rig16mảnh đã dừng, IDs/data/hình trong `prototype/rig/` giữ nguyên.

## Tài liệu và nguồn hình

Đồng bộ GDD, art bible, prompts, asset list, màn chọn phái, animation,
checklist tên phái, rig đặc tả, ngoại hình, ID ví dụ migration, README/AGENTS.
Không đổi con số GDD hoặc trạng thái checkbox. Vật phẩm/kỹ năng ví dụ dự kiến
đổi sangitm_kiem_t1/skl_kiem_tram_kiem; không sửa ID của rig lịch sử.

Kiếm:6 hình thẳng hai lưỡi, chắn nhỏ, cán quấn dây;3pha tiến tới dùng hình vung
kèm vệt trắng ở mũi, hình giơ riêng và hình đâm riêng. Cung:5hình lưng trước/dây
sau, giương chữV sâu, thả dây thẳng;2tên riêng và4thân kèm tay bắn.
STYLE-B/AVOID nguyên văn, luôn đính kèm ref_dinh_bo_linh.png.
Nguồn/prompt ở art/concept/characters/chr_dbl_poses, PNG2× ở art/sprites/characters/chr_dbl_poses.

Kiếm/thân bắn/tên: mỗi tờ1lần. Cung:2lần, loại lần1 vì khoảng kéo dây không tới
tay gần ở tỉ lệ nhân vật. Giữ PNG/prompt lần1 trong rejected/, prompt hiện hành
cạnh PNG và docs/03_prompts. Không sửa tay từng tư thế lẻ bằng imagegen.
Source cũ chỉ giữ làm lịch sử; dao_1…6 đã xóa khỏi art sprite và runtime pilot.
Không chép hình/mã/bảng số hay tên của nguồn tham khảo vào repo hoặc commit.

## Tham khảo cơ chế thể loại — điều rút ra và nơi áp dụng

1. Khung nên chọn hình tư thế và độ lệch riêng từng lớp; không nội suy góc xương.
   Áp vào frames.json, pose_actor.gd, test mọi Sprite2Drotation0 và chỉ lật gốc.
2. Vũ khí cần mốc chuôi/mũi độc lập với hình thân; phép lật giữ quan hệ tay–vũ khí.
   Áp vào source_regions/anchors và kiểm signed-forward cùng khoảng cách tay.
3. Vệt chém là hình vẽ cùng góc của pha, cần đặt theo hướng mũi đang lao tới.
   Áp vào weapon_kiem4pha slash, không dùng một kiếm xoay bằng mã.
4. Hình cung cần phân biệt lưng/dây, giương/thả bằng tranh khác nhau; điểm kéo
   phải thật sự gần tay. Áp vào tờ cung sinh lại và mốc belly/string/near_hand.
5. Tên bay nên tách khỏi bộ hình người và có sự kiện sinh riêng; đổi bộ tư thế
   theo phái. Áp vào arrowSprite, sự kiện spawn pha thả và hai bộ clip Kiếm/Cung.

Chỉ đối chiếu nguyên tắc; không kết luận công cụ họ dùng để vẽ. Một số mã hình
nguồn có nội dung khác cách phân nhóm dự kiến, nên soát bằng hình thực thay vì
coi số mã là phân loại chuẩn. Không đưa ảnh cắt từ nguồn tham khảo vào báo cáo.

## Cắt, mốc và tỉ lệ

[Script](../../tools/cut_pose_sheets.py) dùng lại key alpha mềm và khử xanh, tách
thành phần liền khối; vùng sở hữu dựa tâm component trong box đã chọn bằng mắt.
Gom riêng vệt/ảnh tên bị vỡ cùng pha; không làm mất trail chỉ vì nó không nối lưỡi.
Không xoay/biến dạng tư thế để khớp. Hệ số xuất chung sau đăng ký toàn tờ:
192/559=0,343470483005. Đăng ký mới: kiếm0,5; cung0,63; tên0,2; thân bắn0,9.
Hệ số thực lần lượt≈0,171735/0,216386/0,068694/0,309123; giữaspect từng tờ.
Các nguồn AI nguyên bản không đồng tỉ lệ; không tuyên bố chỉ co một hệ số trực
 tiếp từ mọi PNG nguyên bản. Nguồn chung đầu/thân/chân của pilot trước giữ nguyên.

Mốc nguồn chọn bằng mắt, ghi số tại [source_regions.json](../../prototype/pose_rig/data/source_regions.json);
mốc ảnh2× tại [anchors.json](../../art/sprites/characters/chr_dbl_poses/anchors.json).
Kiếmgrip/tip; cunggrip/belly/string; têntail/tip; thân bắnneck/hip/near_hand/far_hand.
Đế đặt y0, hông/ cổ khớp theo mốc; tay gần giữ chuôi kiếm, tay xa giữ cung.
Bản idle đóng khung256×256 cao192px/mép16px, tương ứng128/96/8logic.
Filterlinear và scale0,5 cố định; mọirotation0, gốc chỉ lật±1.

## Thời gian và phạm vi pilot

Giữ idle4/6fps, run6/12fps, jump2/0,38s, fall2/12fps; khác hình đeo sau lưng
Kiếm/Cung. Slash4pha0,30s như pilot trước.
Thrust2pha×0,05s là **Đề xuất mới cho xem thử**,09chưa có nhịp đâm độc lập;
không thay thời gian chiêu đâm có sẵn hoặc giá trịgame.
Shoot3pha[2/15,1/15,2/15] giữ tổng5/15s, tên sinh đầu pha3 ở3/15s (slot4).
Run_shoot2pha[2/12,4/12] giữ tổng6/12s, tên sinh đầu pha2 ở2/12s (slot3).
Tên240logicpx/s **Đề xuất chỉ demo** trong frames.json, không sửa tuningA0.
Hai khung thrust dùng chung hình đâm, jump/fall cũng lặp hình như pilot trước;
chưa vẽ combo thành phẩm/hurt hoặc triển khai damage/cancel/gameplay mới.

Viewer có chọn phái, động tác, đổi hướng, bật/tắt vũ khí và VềA0.
Bấm **Nhân vật tư thế (thử)** từ A0, hoặc chạy scene pose_rig trực tiếp.
Không sửa scene_switch hay bất kỳ file của rig cũ; không thay nhân vật A0/Đào Úc.

## Ảnh duyệt từ scene thật

[Ảnh ghép](g1_kiem_cung_compare.png): trênquayphải, dướiquaytrái; mỗi ảnh nguồn
1600×720 chụp Godot4.7.2/Mesa llvmpipe quaXvfb. Có idle hai phái, mọi4slash,
2thrust,3shoot. Chỉ nối ảnh viewport bằng [script](../../tools/compare_pose_captures.py),
không vẽ đè hoặc dùng imagegen cho ảnh kết quả.
Nguồn chụp ở prototype/pose_rig/reports/kiem_cung_right.png và kiem_cung_left.png.

## Kiểm tra và giới hạn

6 test Godot gồm smoke/classic_headless/rig_smoke/dao_uc/pose_rig/weapon_direction.
Test mới78cặp khung/hướng; chuôi ở tay sai số0, mũi tiến đúng hướng,
giương cao hơn chuôi; lưng cung trước dây, nắm tay xa0px; dây kéo cách tay gần
1,828016px khi đứng,2,449103px khi chạy (≤3px). Tên sinh đúng pha thả, đầu/mũi
ở trước và đi thêm24px sau0,1s ở cảhaihướng. Không đổi rotation.

KiểmPNG thật không còn xanh nền theo G>R+40,G>B+40 tại alpha>0, in kích thước/
hệ số/màu/alpha. Alpha mềm được giữ có chủ đích; không ép palette32 màu.
Rà tên còn2dòng: artbible130nói vũ khí lính địch/đạo cụ, GDD107cụm lịch sử
"binh đao"; không phải tên phái người chơi. Nguyên văn grep và lý do từng dòng
trong [checks](g1_kiem_cung_checks.txt), cùng đầu ra tất cả lệnh; chép cả vào commit.
[Checker hướng](../../prototype/tests/weapon_direction_checks.gd),
[checkerPNG](../../tools/check_pose_sheets.py),
[actor](../../prototype/pose_rig/pose_actor.gd), [viewer](../../prototype/pose_rig/viewer.gd).

Không tự duyệt mỹ thuật: phép đo mốc/hình học không thay kiểm bằng mắt,
không chứng minh toàn bộ cảm giác chuyển động hay thửAndroid. Không đổi
prototype/config, dao_uc, rigcũ hoặc art/reference; nhật ký/báo cáo cũ giữ byte.
