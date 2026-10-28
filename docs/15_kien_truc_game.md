# Kế hoạch kiến trúc co_lau_game

**Trạng thái: đề xuất, chờ duyệt ở Mốc A.** Đây là kế hoạch cấu trúc, chưa tạo mã
hoặc dự án game. Repo `co_lau_game` đã được người dùng tạo; chỉ bắt đầu triển khai
sau Mốc A. Không chép mã `prototype/` sang game thật. Môi trường đích: **Godot
4.7.2 Standard, GDScript, Android offline**.

## 1. Cấu trúc repo dự kiến

```text
co_lau_game/
├── assets/                    # chỉ ảnh đã duyệt, chép bằng script có ghi nguồn
├── data/                      # Resource .tres chỉ đọc lúc chạy
│   ├── items/
│   ├── skills/
│   ├── enemies/
│   ├── quests/
│   ├── maps/
│   ├── shops/
│   └── dialogue/
├── src/                       # lớp GDScript chia theo tính năng
│   ├── core/
│   ├── player/
│   ├── combat/
│   ├── enemies/
│   ├── npcs/
│   ├── quests/
│   ├── inventory/
│   ├── equipment/
│   ├── forge/
│   ├── base_hoa_lu/
│   ├── world/
│   ├── ui/
│   │   ├── scr_01/            # mỗi SCR-xx có một thư mục riêng
│   │   ├── scr_02/
│   │   └── ... scr_22/
│   ├── store/
│   └── save/
├── scenes/                    # .tscn, bố cục cảnh; tách khỏi lớp luật
│   ├── player/
│   ├── combat/
│   ├── enemies/
│   ├── world/
│   └── ui/                    # cảnh tương ứng các src/ui/scr_xx/
├── tests/                     # luật, save migration, dữ liệu, cảnh/headless
│   └── fixtures/              # file lưu mẫu theo từng save_version
├── tools/
│   └── agent-skills/          # bản tham khảo đã rà, chép từ repo thiết kế
├── docs/
│   └── GDD.md                 # bản sao từ tag thiết kế đang theo
├── project.godot              # chỉ tạo/cấu hình khi triển khai sau Mốc A
├── AGENTS.md
├── DESIGN_VERSION.md
└── THIRD_PARTY.md
```

`assets/` chỉ nhận ảnh trong `design_co_lau/art/approved/` qua script chuyển art;
script ghi commit nguồn, đường dẫn/version asset và kết quả kiểm vào manifest.
Không đưa concept, placeholder hay ảnh chưa duyệt vào đó. Chưa viết script chuyển
art ở bước lập kế hoạch này. Cấu hình số liệu nằm trong `data/`, không lẫn với ảnh.

Khi qua Mốc A, gắn tag `design-vX.Y` bên thiết kế. `DESIGN_VERSION.md` ghi tag và
commit chính xác, ngày đồng bộ cùng phiên bản dữ liệu; `docs/GDD.md` của game lấy
nguyên từ tag đó. Không tự theo nhánh main đang thay đổi cho một bản game đã chốt.

## 2. Ranh giới hệ thống và dữ liệu

Chia ba lớp: dữ liệu cấu hình → luật/trạng thái → scene/UI. Lớp luật nhận dữ liệu
đầu vào, bộ sinh số ngẫu nhiên và lệnh; không phụ thuộc node giao diện. UI/cảnh
không sửa thẳng trạng thái nhân vật. Quy tắc này theo `14_online_migration.md`.

### Autoload tối thiểu

| Autoload | Trách nhiệm | Không gánh thêm |
|---|---|---|
| GameState | Trạng thái runtime của ô đang chơi, do lệnh hợp lệ thay đổi | Không giữ toàn bộ scene hoặc sửa Resource gốc |
| SaveService | Chụp/lưu/đọc snapshot, migrate, khôi phục bản sao | Không tính luật chiến đấu hay mua hàng |
| EventBus | Signal sự kiện đã xảy ra giữa các tính năng | Không làm kho trạng thái hoặc chuỗi lệnh ẩn |
| Config | Đọc/kiểm/tra cứu Resource, ID và data_version | Không ghi dữ liệu người chơi vào .tres |

Không tự thêm AudioManager/Inventory/Camera/Billing thành autoload chỉ vì ví dụ
skill dùng singleton. Dịch vụ theo tính năng được tạo/inject bởi cảnh hoặc lớp
core phù hợp. Thêm autoload phải nêu phụ thuộc và được duyệt trong kế hoạch.

Các hệ thống giao tiếp qua **signal/EventBus** cho sự kiện (đã trúng đòn, hoàn tất
nhiệm vụ, thay trang bị). Lệnh có đầu vào/kết quả rõ ràng đi vào lớp xử lý sở hữu
luật; signal thông báo sau khi lệnh thành công. Không dùng broadcast để che ai
được quyền thay đổi dữ liệu. Kết nối/hủy kết nối theo vòng đời scene, tránh nhận
hai lần khi đổi màn. Mỗi SCR-xx có thư mục riêng trong `src/ui/`, và scene ghép
Control/Theme tương ứng trong `scenes/ui/`.

### Resource và file lưu

- Nội dung items, skills, enemies, quests, maps, shops, dialogue là các **Resource .tres** trong `res://data/`. Lớp định nghĩa Resource nằm cùng tính năng trong `src/`; số cân bằng/giá/tầm đánh không viết cứng trong mã.
- Các tên tệp/path không phải ID nghiệp vụ. Dùng ID ổn định `itm_*`, `skl_*`, `mob_*`, `bos_*`, `qst_*`, `map_*`, `npc_*`, `shp_*`, `bld_*`, `sku_*`, `ent_*` đúng `14_online_migration.md`. Kiểm ID trùng, tham chiếu thiếu và dữ liệu ngừng dùng trước build.
- Cấu hình chỉ đọc, được phát hành cùng game và có `data_version`. Trạng thái runtime là bản dữ liệu riêng; thay HP/trang bị không mutate Resource dùng chung cho nhiều bản thể.
- File lưu ở `user://`, là snapshot dữ liệu thuần có `save_version`, ID ô, ID từng món trang bị, tiến độ, tiền và seed/state RNG. Đề xuất JSON có schema, kiểm đầu vào, ghi an toàn và bản sao; không dùng Resource .tres của người dùng làm file lưu vì có thể nạp GDScript.
- Migration đi tuần tự giữa các save_version, test bằng fixtures cũ. Không xóa ID đã phát hành; ngừng dùng bằng cờ. Cấu hình Resource và dữ liệu lưu không dùng chung tệp/đối tượng.
- Bản đầu chơi offline, không đăng nhập bắt buộc, không backend hay ngân phiếu nạp. `src/store/` chỉ tích hợp món vĩnh viễn Google Play theo `12_ngan_phieu.md`, không kéo các phần online tương lai vào hiện tại.

**Điểm cần đồng bộ khi duyệt:** GDD Phần 6 và `14_online_migration.md` hiện còn
nói 12 nhóm JSON, layout thư mục cũ và một số autoload cũ. Kế hoạch này **đề xuất**
Resource .tres và src theo tính năng theo yêu cầu mới; trước khi qua Mốc A phải
đồng bộ tài liệu nguồn/định dạng dữ liệu, không coi việc thêm file này là duyệt
kiến trúc hoặc âm thầm chuyển định dạng. **Nhánh kế hoạch dựa trên main `5577fa5`**,
đã merge ký duyệt A0 và quy trình ghép bộ phận từ `docs/a0-signoff`. Bộ prototype
được nghiệm thu vẫn là commit `7973729`; hai commit có vai trò khác nhau.
Giữ nguyên toàn bộ nội dung A0/bộ phận trên main mới, tham chiếu `13_thong_so.md`
và art bible; không dùng ví dụ kỹ thuật của skill để thay bộ số đã chốt.

## 3. Nhân vật và hoạt ảnh ghép bộ phận

Chọn rig **Skeleton2D hoặc Node2D + AnimationPlayer** sau khi thử lát cắt được
phép; chưa chọn addon rig. `chr_dbl_parts` theo tỉ lệ người 96 px, gồm đầu kèm tóc,
thân, tay trên/dưới gần/xa, đùi/cẳng chân gần/xa, bàn tay và vũ khí; có điểm khớp,
phần vẽ bù và lớp gần/xa. `chr_dbl_anim_*` ghi vị trí/góc/thứ tự lớp từng khung,
thời lượng và hit/spawn theo `09_animation_spec.md`. Các bậc trang bị thay bộ
phận áo/quần/vũ khí, dùng chung khớp và dữ liệu động tác. Lộn đỉnh/chiêu lớn có
thể thêm khung riêng khi cần; không mang xoay nguyên sprite tạm vào thành phẩm.

Sprite/rig tách khỏi CharacterBody2D/Area2D: lộn không xoay hitbox. Claude/người
dùng duyệt bộ phận bằng báo cáo script và bằng mắt theo quyết định quy trình mới;
không tự duyệt vì có skill gợi ý một đường sản xuất khác. Lát cắt trong prototype
chỉ là ngoại lệ thử thiết kế đã cho phép, không phải khởi đầu code game thật.

## 4. Chính sách bên thứ ba

- Mã/addon/skill: chỉ **MIT, Apache-2.0 hoặc CC0**. Tài nguyên dùng các giấy phép này; **CC-BY** chỉ là ngoại lệ cho tài nguyên khi ghi công đầy đủ trong màn **Credits** và THIRD_PARTY.md.
- Cấm **GPL/AGPL/LGPL cho mã**, cấm **CC-BY-NC**, cấm **CC-BY-SA cho tài nguyên**, cấm thứ không rõ giấy phép. Không suy ra giấy phép addon từ giấy phép bài hướng dẫn.
- Mọi addon/tài nguyên/skill phải ghi **tên, phiên bản hoặc commit, giấy phép, nguồn** vào `THIRD_PARTY.md`. Với CC-BY thêm tác giả, nội dung ghi công và vị trí Credits. Giữ LICENSE/NOTICE bắt buộc, ghi mọi chỉnh sửa bản vendored.
- **Codex không tự thêm khi người dùng chưa duyệt.** Hai bộ skill dưới đây đã được yêu cầu đích danh trong lần này; việc nhập chúng không duyệt các addon mà chúng nhắc tới. Không tải/cài addon hoặc chạy script skill chỉ vì tài liệu có hướng dẫn.

### Addon đề xuất — chưa được thêm hoặc duyệt

| Addon | Mục đích đề xuất | Trạng thái |
|---|---|---|
| GUT hoặc gdUnit4 | Test runner cho luật/cảnh | cần kiểm tra bản hỗ trợ Godot 4.7 và giấy phép |
| Dialogic | Công cụ hội thoại, nếu phù hợp dữ liệu/luồng đã chốt | cần kiểm tra bản hỗ trợ Godot 4.7 và giấy phép |
| Phantom Camera | Camera, nếu core không đủ và vẫn giữ số A0 | cần kiểm tra bản hỗ trợ Godot 4.7 và giấy phép |
| Beehave hoặc LimboAI | Hành vi quái/AI, chọn theo nhu cầu | cần kiểm tra bản hỗ trợ Godot 4.7 và giấy phép |
| Godot State Charts | State machine nếu có lợi hơn core tự dựng | cần kiểm tra bản hỗ trợ Godot 4.7 và giấy phép |
| GodotGooglePlayBilling | Mua/khôi phục món vĩnh viễn trên Android | cần kiểm tra bản hỗ trợ Godot 4.7 và giấy phép |

Chưa pin phiên bản hoặc xác nhận giấy phép các addon trong bảng. Trước khi đề
xuất thêm, cần đối chiếu bản chính thức, tương thích 4.7.2, giấy phép của đúng
version và phụ thuộc bắc cầu; sau đó người dùng duyệt rồi mới nhập/cập nhật sổ.

### Skill tham khảo đã nhập vào repo thiết kế

| Tên | Nguồn | Commit | Giấy phép | Phạm vi |
|---|---|---|---|---|
| awesome-gamedev-agent-skills | https://github.com/gamedev-skills/awesome-gamedev-agent-skills | `19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9` | Apache-2.0, giữ LICENSE và NOTICE | Router, 16 Godot, 15 discipline, RPG/platformer, prototype-fast, 2 tài liệu định dạng/version |
| GodotPrompter | https://github.com/jame581/godotprompter | `d7b26cdb5fae14d4ef7b713c5bf259395e75c3c6` | MIT, giữ LICENSE | 16 skill được liệt kê trong tools/agent-skills/README.md |

Ngày chép: **28/10/2026**. Bản cục bộ đã gỡ phần cài đặt/tải mạng/tự động hóa và
thêm ràng buộc dự án. Đối chiếu `tools/agent-skills/AUDIT.md`, `AUDIT.json` và
`CONFLICTS.md`; không coi bản đã điều chỉnh là bản upstream nguyên vẹn. Khi tạo
repo game phải chép hai dòng nguồn/commit/license trên vào THIRD_PARTY.md thực.

## 5. Thứ tự dựng sau Mốc A

1. **core + save**: GameState/Config/EventBus/SaveService, phiên bản/ID và migration; test dữ liệu/lưu trước.
2. **player**: dựng mới theo số A0/Kiểu cổ điển đã chốt, rig tách va chạm; không chép code prototype.
3. **combat**: lệnh/sát thương/hộp đánh, thời điểm hit/cooldown, thứ tự lớp hiệu ứng.
4. **world/map Đào Úc**: scene/TileMapLayer từ bố cục đã duyệt, viewport 960–1200 và vùng che điều khiển.
5. **enemies**: một họ quái trước, AI/đòn báo trước, rồi mở rộng dữ liệu.
6. **ui HUD**: chuẩn A0/Theme thành phẩm; UI phát lệnh, nghe sự kiện, không sửa GameState trực tiếp.
7. **các hệ thống còn lại**: npcs, quests, inventory, equipment, forge, base_hoa_lu, store và các SCR-xx, từng lát chức năng có kiểm tra.

## 6. Chép skill và bàn giao repo game

Khi bắt đầu triển khai `co_lau_game` sau Mốc A, chép **tools/agent-skills/** từ bản
thiết kế đã duyệt, gồm giấy phép, README, CONFLICTS và hồ sơ rà soát. Giữ nguyên
mục **“Skill tham khảo”** của AGENTS.md trong repo game, gồm thứ tự ưu tiên và
điều kiện không chạy script khi chưa có yêu cầu. Không chép hooks/commands/agents,
plugin.json hoặc cấu hình tự chạy từ upstream vào repo game.

Ghi tag/commit thiết kế vào DESIGN_VERSION.md, giữ GDD.md đúng tag và THIRD_PARTY.md
đúng nguồn nhập. Không tự tạo file/mã game để minh họa kế hoạch này trước Mốc A.
