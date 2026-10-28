# Skill tham khảo cho Cờ Lau

Bản nhập có chọn lọc ngày **28/10/2026**, chỉ để đọc. Không cài plugin,
không đăng ký hook và không chạy script đi kèm. Người dùng đã yêu cầu hai nguồn
này; điều đó không cho phép tự thêm addon/phụ thuộc mà ví dụ đề cập.
Đọc CONFLICTS.md trước mỗi lần áp dụng; docs dự án > AGENTS.md > skill.

## awesome-gamedev

Nguồn: https://github.com/gamedev-skills/awesome-gamedev-agent-skills

Commit: `19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9`. Giấy phép: **Apache-2.0; giữ LICENSE và NOTICE**.

Skill đã chép (đường dẫn thật):

- `awesome-gamedev/router/SKILL.md`
- `awesome-gamedev/skills/godot/godot-2d-movement/SKILL.md`
- `awesome-gamedev/skills/godot/godot-3d-essentials/SKILL.md`
- `awesome-gamedev/skills/godot/godot-animation/SKILL.md`
- `awesome-gamedev/skills/godot/godot-audio/SKILL.md`
- `awesome-gamedev/skills/godot/godot-csharp/SKILL.md`
- `awesome-gamedev/skills/godot/godot-export/SKILL.md`
- `awesome-gamedev/skills/godot/godot-gdscript/SKILL.md`
- `awesome-gamedev/skills/godot/godot-gdscript-headless-testing/SKILL.md`
- `awesome-gamedev/skills/godot/godot-multiplayer/SKILL.md`
- `awesome-gamedev/skills/godot/godot-nodes-scenes/SKILL.md`
- `awesome-gamedev/skills/godot/godot-physics/SKILL.md`
- `awesome-gamedev/skills/godot/godot-resources/SKILL.md`
- `awesome-gamedev/skills/godot/godot-shaders/SKILL.md`
- `awesome-gamedev/skills/godot/godot-signals-groups/SKILL.md`
- `awesome-gamedev/skills/godot/godot-tilemap/SKILL.md`
- `awesome-gamedev/skills/godot/godot-ui-control/SKILL.md`
- `awesome-gamedev/skills/disciplines/ai-behavior-trees-utility-ai/SKILL.md`
- `awesome-gamedev/skills/disciplines/audio-design/SKILL.md`
- `awesome-gamedev/skills/disciplines/camera-systems/SKILL.md`
- `awesome-gamedev/skills/disciplines/create-game-assets/SKILL.md`
- `awesome-gamedev/skills/disciplines/dialogue-systems/SKILL.md`
- `awesome-gamedev/skills/disciplines/game-ai/SKILL.md`
- `awesome-gamedev/skills/disciplines/game-feel/SKILL.md`
- `awesome-gamedev/skills/disciplines/game-ui-ux/SKILL.md`
- `awesome-gamedev/skills/disciplines/input-systems/SKILL.md`
- `awesome-gamedev/skills/disciplines/level-design/SKILL.md`
- `awesome-gamedev/skills/disciplines/performance-optimization/SKILL.md`
- `awesome-gamedev/skills/disciplines/physics-tuning/SKILL.md`
- `awesome-gamedev/skills/disciplines/procedural-gen/SKILL.md`
- `awesome-gamedev/skills/disciplines/save-systems/SKILL.md`
- `awesome-gamedev/skills/disciplines/shader-programming/SKILL.md`
- `awesome-gamedev/skills/genres/rpg/SKILL.md`
- `awesome-gamedev/skills/genres/platformer/SKILL.md`
- `awesome-gamedev/skills/workflows/prototype-fast/SKILL.md`

## godotprompter

Nguồn: https://github.com/jame581/godotprompter

Commit: `d7b26cdb5fae14d4ef7b713c5bf259395e75c3c6`. Giấy phép: **MIT; giữ LICENSE**.

Skill đã chép (đường dẫn thật):

- `godotprompter/skills/player-controller/SKILL.md`
- `godotprompter/skills/mobile-development/SKILL.md`
- `godotprompter/skills/responsive-ui/SKILL.md`
- `godotprompter/skills/hud-system/SKILL.md`
- `godotprompter/skills/save-load/SKILL.md`
- `godotprompter/skills/inventory-system/SKILL.md`
- `godotprompter/skills/state-machine/SKILL.md`
- `godotprompter/skills/resource-pattern/SKILL.md`
- `godotprompter/skills/scene-organization/SKILL.md`
- `godotprompter/skills/godot-testing/SKILL.md`
- `godotprompter/skills/export-pipeline/SKILL.md`
- `godotprompter/skills/animation-system/SKILL.md`
- `godotprompter/skills/beehave/SKILL.md`
- `godotprompter/skills/limboai/SKILL.md`
- `godotprompter/skills/phantom-camera/SKILL.md`
- `godotprompter/skills/dialogue-manager/SKILL.md`

awesome-gamedev gồm router, **16 Godot**, **15 discipline**, RPG/platformer và
prototype-fast; kèm docs/SKILL-FORMAT.md, docs/VERSION-SUPPORT.md. GodotPrompter
chỉ có **16 skill** yêu cầu, giữ cấu trúc `skills/<tên>/`.
Router có nhắc skill của engine khác nhưng không chép vì dự án chỉ dùng
**Godot 4.7.2**. Nhóm Godot .NET/3D/multiplayer được giữ trong đủ 16 skill nguồn
nhưng không tự mở phạm vi GDScript/2D/offline hiện tại.

## Rà soát và chứng cứ

- `AUDIT.md`: kết quả từng file và phần đã gỡ; `AUDIT.json`: commit, hash SHA-256 trước/sau và vùng dòng upstream.
- `CONFLICTS.md`: các xung đột và cách xử lý quyết định dự án thắng.
- `ADDED_FILES.txt`: danh sách file thêm mới, tạo từ lệnh Git thực tế sau khi stage.
- Chỉ chép SKILL.md và references/assets/scripts văn bản của skill, cộng tài liệu/giấy phép đã yêu cầu. Không có hooks/, commands/, agents/, plugin.json, marketplace hay cấu hình tự chạy.
- Cài đặt/tải mạng/CI tự chạy và lời gọi helper tự động đã gỡ. Ví dụ CLI thụ động còn lại chỉ để tra cứu; không có lệnh nào được chạy khi nhập.
- Ba helper .py được giữ dưới dạng văn bản mode 0644; chỉ phân tích AST, không thực thi. Không cài Pillow hoặc addon trong lần này.
- Link đến file không chép được đổi sang nguồn GitHub tại đúng commit; link là trích dẫn, không phải yêu cầu tự tải.

## Cập nhật sau này

1. Chọn commit mới của đúng nguồn và ghi lại commit/ngày/giấy phép; không cập nhật ngầm theo HEAD.
2. Chép lại đúng tập con đã liệt kê, chỉ SKILL.md và references/assets/scripts, giữ LICENSE/NOTICE. Không mang cấu hình tự chạy từ upstream sang.
3. **Chạy lại toàn bộ bước B3**: rà từng file, gỡ hướng dẫn cài/tải/tự động hóa/bỏ qua quy tắc nếu có; cập nhật CONFLICTS và báo cáo/hash trước–sau.
4. Xem diff để giữ các điều chỉnh dự án, bảo đảm không file nhị phân/symlink/cấu hình tự chạy lọt vào. Không chạy helper để kiểm tra nếu người dùng chưa yêu cầu.
5. Cập nhật README, AUDIT và sổ bên thứ ba; khi sang repo game phải đồng bộ THIRD_PARTY.md và giữ mục Skill tham khảo của AGENTS.md.
