# Rà soát B3 — 28/10/2026

Rà toàn văn từng file đã chép bằng quét tĩnh; đọc đối chiếu các vùng khớp lệnh,
cài đặt, tự động hóa và quy tắc xung đột. Không chạy bất kỳ script đã nhập nào,
không cài addon/phụ thuộc và không đăng ký skill với hệ thống plugin.
Đây không phải chứng nhận hành vi khi thực thi các ví dụ; các ví dụ chỉ để đọc.

- Hai giấy phép gốc đã đọc và giữ nguyên: Apache-2.0 kèm NOTICE; MIT.
- Loại khỏi danh sách chép: mọi agents/, hooks/, commands/, plugin.json, cấu hình plugin/CI, symlink và file nhị phân. Không có file cấu hình tự chạy nào được nhập.
- Đã gỡ hướng dẫn cài addon/SDK/export template, tải Butler/SDK/artwork, mẫu CI tự chạy trên push và hướng dẫn tự gọi helper sau thay đổi. Vị trí gốc và lý do ở bảng dưới/AUDIT.json.
- Thêm thông báo chỉ tham khảo vào 51 SKILL.md; quyết định dự án thắng, không tự chạy helper hay cài phụ thuộc. Lệnh CLI thử nghiệm còn lại chỉ là ví dụ thụ động, cần yêu cầu rõ ràng của người dùng mới được chạy.
- Ba script Python chỉ dùng thư viện chuẩn/Pillow; quét AST không thấy API tải mạng, subprocess hay lệnh shell. asset_report chỉ đọc ảnh/in báo cáo; build_preview_sheet ghi ảnh đến đường dẫn --out do người gọi chọn; checker Godot chỉ đọc. Chỉ phân tích cú pháp/AST, **không chạy** các script này.
- Không phát hiện yêu cầu bỏ qua quy tắc cấp cao. Cảnh báo không nạp Resource không tin cậy được giữ vì là bảo vệ, không phải yêu cầu bỏ qua quy tắc.
- Link tới file ngoài tập con được đổi thành URL nguồn ở commit đã chép; không tự tải thêm file/skill đó. Metadata engine khác trong router/VERSION-SUPPORT là tham khảo, không đổi Godot 4.7.2.

Bảng VERSION-SUPPORT giữ nguyên: link tải chính thức là trích dẫn phiên bản, không phải lệnh tải. Bảng so sánh test framework được giữ, chỉ bỏ dòng cài đặt.

## Kết quả từng file

SHA-256 đầy đủ, vùng sửa theo số dòng upstream và bản đồ link ở AUDIT.json.
Số dòng [0,0] là thông báo/chỉnh cấu trúc hoặc định dạng, không giả là dòng upstream.

| File | Kết quả | SHA-256 bản đã rà (12 ký tự) |
|---|---|---|
| `awesome-gamedev/router/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `34eca0686014` |
| `awesome-gamedev/router/references/custom-engines.md` | Không phát hiện vùng cần gỡ | `0880a19b3e15` |
| `awesome-gamedev/router/references/engine-detection.md` | Không phát hiện vùng cần gỡ | `914b3fa795ec` |
| `awesome-gamedev/router/references/routing-table.md` | Không phát hiện vùng cần gỡ | `2048329d5c29` |
| `awesome-gamedev/skills/godot/godot-2d-movement/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `1fe7adeba0dc` |
| `awesome-gamedev/skills/godot/godot-2d-movement/references/controller-recipes.md` | Không phát hiện vùng cần gỡ | `bcf89d3e8a82` |
| `awesome-gamedev/skills/godot/godot-3d-essentials/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `04aba23abeb1` |
| `awesome-gamedev/skills/godot/godot-3d-essentials/references/scene-and-environment.md` | Không phát hiện vùng cần gỡ | `94d016b194b9` |
| `awesome-gamedev/skills/godot/godot-animation/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `b2503b88639f` |
| `awesome-gamedev/skills/godot/godot-animation/references/animation-tree-and-tween.md` | Không phát hiện vùng cần gỡ | `488900f89550` |
| `awesome-gamedev/skills/godot/godot-audio/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `d4bb6622aa6f` |
| `awesome-gamedev/skills/godot/godot-audio/references/buses-and-effects.md` | Không phát hiện vùng cần gỡ | `f84f5c91fc78` |
| `awesome-gamedev/skills/godot/godot-csharp/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `300a825e71e3` |
| `awesome-gamedev/skills/godot/godot-csharp/references/csharp-setup-and-interop.md` | Đã điều chỉnh; xem chi tiết bên dưới | `bb54a3c118a2` |
| `awesome-gamedev/skills/godot/godot-export/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `5dd24b028d02` |
| `awesome-gamedev/skills/godot/godot-export/references/presets-and-cli.md` | Đã điều chỉnh; xem chi tiết bên dưới | `e0bc95fd3ef3` |
| `awesome-gamedev/skills/godot/godot-gdscript/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `5481e4420f1e` |
| `awesome-gamedev/skills/godot/godot-gdscript/references/annotations-and-typing.md` | Không phát hiện vùng cần gỡ | `b905cae5114e` |
| `awesome-gamedev/skills/godot/godot-gdscript-headless-testing/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `e112a87254cc` |
| `awesome-gamedev/skills/godot/godot-multiplayer/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `7b2720ac03e7` |
| `awesome-gamedev/skills/godot/godot-multiplayer/references/replication-and-rpc.md` | Không phát hiện vùng cần gỡ | `05908f3ea13f` |
| `awesome-gamedev/skills/godot/godot-nodes-scenes/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `6157716d6a8d` |
| `awesome-gamedev/skills/godot/godot-nodes-scenes/references/tree-and-instancing.md` | Không phát hiện vùng cần gỡ | `be3c86180bd1` |
| `awesome-gamedev/skills/godot/godot-nodes-scenes/scripts/check_godot_project.py` | Đã điều chỉnh; xem chi tiết bên dưới | `8a407dba583c` |
| `awesome-gamedev/skills/godot/godot-physics/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `135334e78e4f` |
| `awesome-gamedev/skills/godot/godot-physics/references/bodies-and-queries.md` | Không phát hiện vùng cần gỡ | `5d1616f73d9f` |
| `awesome-gamedev/skills/godot/godot-resources/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `df1d7b40ce2d` |
| `awesome-gamedev/skills/godot/godot-resources/references/resource-patterns.md` | Không phát hiện vùng cần gỡ | `a848b0be5d5d` |
| `awesome-gamedev/skills/godot/godot-shaders/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `bb9d9bc6982a` |
| `awesome-gamedev/skills/godot/godot-shaders/references/shading-language.md` | Không phát hiện vùng cần gỡ | `406987a5728a` |
| `awesome-gamedev/skills/godot/godot-signals-groups/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `c985eee13e23` |
| `awesome-gamedev/skills/godot/godot-signals-groups/references/signal-patterns.md` | Không phát hiện vùng cần gỡ | `7f28a8fccf5a` |
| `awesome-gamedev/skills/godot/godot-tilemap/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `0b49ac69ec58` |
| `awesome-gamedev/skills/godot/godot-tilemap/references/tileset-and-terrains.md` | Không phát hiện vùng cần gỡ | `c2486c7bacdd` |
| `awesome-gamedev/skills/godot/godot-ui-control/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `1241cd35164e` |
| `awesome-gamedev/skills/godot/godot-ui-control/references/layout-and-theming.md` | Không phát hiện vùng cần gỡ | `5f54eed206cd` |
| `awesome-gamedev/skills/disciplines/ai-behavior-trees-utility-ai/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `325e88d675e2` |
| `awesome-gamedev/skills/disciplines/ai-behavior-trees-utility-ai/references/behavior-tree-core.md` | Không phát hiện vùng cần gỡ | `ba72c1400780` |
| `awesome-gamedev/skills/disciplines/ai-behavior-trees-utility-ai/references/best-practices-and-pitfalls.md` | Không phát hiện vùng cần gỡ | `8ff83984ad99` |
| `awesome-gamedev/skills/disciplines/ai-behavior-trees-utility-ai/references/practical-examples.md` | Không phát hiện vùng cần gỡ | `2b32bdd643a4` |
| `awesome-gamedev/skills/disciplines/ai-behavior-trees-utility-ai/references/utility-ai-system.md` | Không phát hiện vùng cần gỡ | `156ee87846a4` |
| `awesome-gamedev/skills/disciplines/audio-design/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `c8d49402167a` |
| `awesome-gamedev/skills/disciplines/audio-design/references/adaptive-music.md` | Không phát hiện vùng cần gỡ | `1aa1a14bc163` |
| `awesome-gamedev/skills/disciplines/camera-systems/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `49c8e63e5b10` |
| `awesome-gamedev/skills/disciplines/camera-systems/references/follow-and-framing.md` | Không phát hiện vùng cần gỡ | `7664d4ab898e` |
| `awesome-gamedev/skills/disciplines/create-game-assets/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `325a63243b7d` |
| `awesome-gamedev/skills/disciplines/create-game-assets/references/art-direction.md` | Không phát hiện vùng cần gỡ | `19b2ccb827ea` |
| `awesome-gamedev/skills/disciplines/create-game-assets/references/provenance.md` | Không phát hiện vùng cần gỡ | `098d3cf915cd` |
| `awesome-gamedev/skills/disciplines/create-game-assets/references/raster-pipeline.md` | Không phát hiện vùng cần gỡ | `d7a5714628fd` |
| `awesome-gamedev/skills/disciplines/create-game-assets/references/three-d-pipeline.md` | Không phát hiện vùng cần gỡ | `ee6ed7c373e1` |
| `awesome-gamedev/skills/disciplines/create-game-assets/assets/art-direction-brief.md` | Không phát hiện vùng cần gỡ | `6d5dc4f9f5fc` |
| `awesome-gamedev/skills/disciplines/create-game-assets/assets/asset-manifest.json` | Không phát hiện vùng cần gỡ | `6cce05638c11` |
| `awesome-gamedev/skills/disciplines/create-game-assets/scripts/asset_report.py` | Không phát hiện vùng cần gỡ | `99f4b38f9c4f` |
| `awesome-gamedev/skills/disciplines/create-game-assets/scripts/build_preview_sheet.py` | Không phát hiện vùng cần gỡ | `002a550a7b5f` |
| `awesome-gamedev/skills/disciplines/create-game-assets/scripts/requirements.txt` | Không phát hiện vùng cần gỡ | `bbced595a25d` |
| `awesome-gamedev/skills/disciplines/dialogue-systems/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `ad20c8a590b2` |
| `awesome-gamedev/skills/disciplines/dialogue-systems/references/ink-and-yarn.md` | Không phát hiện vùng cần gỡ | `c43275e04428` |
| `awesome-gamedev/skills/disciplines/dialogue-systems/references/runner.md` | Đã điều chỉnh; xem chi tiết bên dưới | `7dbe5a3f3e88` |
| `awesome-gamedev/skills/disciplines/game-ai/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `43f6319cb14a` |
| `awesome-gamedev/skills/disciplines/game-ai/references/behavior-trees.md` | Không phát hiện vùng cần gỡ | `eed3fdb94380` |
| `awesome-gamedev/skills/disciplines/game-ai/references/pathfinding.md` | Không phát hiện vùng cần gỡ | `75d6c8397fc5` |
| `awesome-gamedev/skills/disciplines/game-feel/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `ec7e7d640f54` |
| `awesome-gamedev/skills/disciplines/game-feel/references/feedback-recipes.md` | Không phát hiện vùng cần gỡ | `f8cca962733b` |
| `awesome-gamedev/skills/disciplines/game-ui-ux/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `29bf3c20276d` |
| `awesome-gamedev/skills/disciplines/game-ui-ux/references/layout-and-flow.md` | Không phát hiện vùng cần gỡ | `961fc8c8e45a` |
| `awesome-gamedev/skills/disciplines/input-systems/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `05c6c9832a3c` |
| `awesome-gamedev/skills/disciplines/input-systems/references/buffering-and-accessibility.md` | Đã điều chỉnh; xem chi tiết bên dưới | `cddb4433f7a8` |
| `awesome-gamedev/skills/disciplines/level-design/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `cdaf4a86992b` |
| `awesome-gamedev/skills/disciplines/level-design/references/pacing-and-flow.md` | Không phát hiện vùng cần gỡ | `e8e3940f585e` |
| `awesome-gamedev/skills/disciplines/performance-optimization/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `b8523cdf1372` |
| `awesome-gamedev/skills/disciplines/performance-optimization/references/profiling-and-budgets.md` | Không phát hiện vùng cần gỡ | `e68c43d5e66e` |
| `awesome-gamedev/skills/disciplines/physics-tuning/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `31268768e965` |
| `awesome-gamedev/skills/disciplines/physics-tuning/references/timestep-and-ccd.md` | Không phát hiện vùng cần gỡ | `de507b0bee47` |
| `awesome-gamedev/skills/disciplines/procedural-gen/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `326537c79602` |
| `awesome-gamedev/skills/disciplines/procedural-gen/references/dungeon-generation.md` | Không phát hiện vùng cần gỡ | `808451354e49` |
| `awesome-gamedev/skills/disciplines/procedural-gen/references/noise.md` | Không phát hiện vùng cần gỡ | `4f4da0458cde` |
| `awesome-gamedev/skills/disciplines/save-systems/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `ef877b359bd8` |
| `awesome-gamedev/skills/disciplines/save-systems/references/versioning-and-migration.md` | Đã điều chỉnh; xem chi tiết bên dưới | `31b969ba0830` |
| `awesome-gamedev/skills/disciplines/shader-programming/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `408ef75c4ad6` |
| `awesome-gamedev/skills/disciplines/shader-programming/references/effects.md` | Không phát hiện vùng cần gỡ | `af47d6efff37` |
| `awesome-gamedev/skills/genres/rpg/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `b549a00f0db3` |
| `awesome-gamedev/skills/genres/rpg/references/stats-combat-quests.md` | Không phát hiện vùng cần gỡ | `f48f556a5108` |
| `awesome-gamedev/skills/genres/platformer/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `48e5fc2c53f6` |
| `awesome-gamedev/skills/genres/platformer/references/feel-tuning.md` | Không phát hiện vùng cần gỡ | `687349451377` |
| `awesome-gamedev/skills/workflows/prototype-fast/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `b9a2f3a8897d` |
| `awesome-gamedev/LICENSE` | Không phát hiện vùng cần gỡ | `6f82dcfeb95a` |
| `awesome-gamedev/NOTICE` | Không phát hiện vùng cần gỡ | `2dcb65b1c5be` |
| `awesome-gamedev/docs/SKILL-FORMAT.md` | Đã điều chỉnh; xem chi tiết bên dưới | `a59eef46d3b5` |
| `awesome-gamedev/docs/VERSION-SUPPORT.md` | Không phát hiện vùng cần gỡ | `a8d30fe79b82` |
| `godotprompter/skills/player-controller/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `8bd8f2cbee12` |
| `godotprompter/skills/player-controller/references/common-movement-recipes.md` | Không phát hiện vùng cần gỡ | `51e97f43d253` |
| `godotprompter/skills/mobile-development/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `3acf237769e8` |
| `godotprompter/skills/mobile-development/references/crash-debugging.md` | Đã điều chỉnh; xem chi tiết bên dưới | `f3044652173d` |
| `godotprompter/skills/mobile-development/references/iap-and-ads.md` | Không phát hiện vùng cần gỡ | `3ddfa65196fe` |
| `godotprompter/skills/mobile-development/references/plugins.md` | Không phát hiện vùng cần gỡ | `d894d02d78a2` |
| `godotprompter/skills/responsive-ui/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `d0ffa5c622d1` |
| `godotprompter/skills/responsive-ui/references/adaptive-layouts.md` | Đã điều chỉnh; xem chi tiết bên dưới | `9fdff55177d7` |
| `godotprompter/skills/responsive-ui/references/dpi-scaling.md` | Đã điều chỉnh; xem chi tiết bên dưới | `ea171aa14623` |
| `godotprompter/skills/responsive-ui/references/mobile.md` | Đã điều chỉnh; xem chi tiết bên dưới | `25dd4c08b178` |
| `godotprompter/skills/responsive-ui/references/pixel-art-setup.md` | Đã điều chỉnh; xem chi tiết bên dưới | `56609799398e` |
| `godotprompter/skills/hud-system/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `00e62e4ec72d` |
| `godotprompter/skills/hud-system/references/damage-numbers.md` | Đã điều chỉnh; xem chi tiết bên dưới | `bb47aafd49fb` |
| `godotprompter/skills/hud-system/references/interaction-prompts.md` | Đã điều chỉnh; xem chi tiết bên dưới | `4b2cab8e2780` |
| `godotprompter/skills/hud-system/references/minimap.md` | Đã điều chỉnh; xem chi tiết bên dưới | `9b562c2bc641` |
| `godotprompter/skills/hud-system/references/notifications.md` | Đã điều chỉnh; xem chi tiết bên dưới | `a52663df2f55` |
| `godotprompter/skills/save-load/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `14b66b237c17` |
| `godotprompter/skills/save-load/references/configfile.md` | Đã điều chỉnh; xem chi tiết bên dưới | `f7270fdbfcb3` |
| `godotprompter/skills/save-load/references/json-saves.md` | Đã điều chỉnh; xem chi tiết bên dưới | `5f77522c1cea` |
| `godotprompter/skills/save-load/references/save-architecture.md` | Đã điều chỉnh; xem chi tiết bên dưới | `a2f0f0dee5af` |
| `godotprompter/skills/save-load/references/version-migration.md` | Đã điều chỉnh; xem chi tiết bên dưới | `8a578b5ca365` |
| `godotprompter/skills/inventory-system/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `278b26c8f558` |
| `godotprompter/skills/inventory-system/references/core-classes.md` | Không phát hiện vùng cần gỡ | `ba7d0a1b3200` |
| `godotprompter/skills/inventory-system/references/equipment.md` | Đã điều chỉnh; xem chi tiết bên dưới | `3841efe277c8` |
| `godotprompter/skills/inventory-system/references/serialization.md` | Đã điều chỉnh; xem chi tiết bên dưới | `34bb8fffe624` |
| `godotprompter/skills/inventory-system/references/ui-binding.md` | Đã điều chỉnh; xem chi tiết bên dưới | `bacb604f49cf` |
| `godotprompter/skills/state-machine/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `e17b591511d1` |
| `godotprompter/skills/state-machine/references/hierarchical-and-parallel.md` | Không phát hiện vùng cần gỡ | `4a21b680490e` |
| `godotprompter/skills/resource-pattern/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `7d819f90a6d3` |
| `godotprompter/skills/resource-pattern/references/collections.md` | Đã điều chỉnh; xem chi tiết bên dưới | `03b54994ad9c` |
| `godotprompter/skills/resource-pattern/references/configuration-pattern.md` | Đã điều chỉnh; xem chi tiết bên dưới | `358994b5d208` |
| `godotprompter/skills/resource-pattern/references/editor-integration.md` | Đã điều chỉnh; xem chi tiết bên dưới | `f4ad3ee24ab6` |
| `godotprompter/skills/resource-pattern/references/saving-resources.md` | Đã điều chỉnh; xem chi tiết bên dưới | `51aff93a0162` |
| `godotprompter/skills/resource-pattern/references/sharing-vs-unique.md` | Đã điều chỉnh; xem chi tiết bên dưới | `9c35c7d17059` |
| `godotprompter/skills/scene-organization/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `5a273ca7c67b` |
| `godotprompter/skills/godot-testing/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `428aa8a4e9c1` |
| `godotprompter/skills/godot-testing/references/running-tests.md` | Đã điều chỉnh; xem chi tiết bên dưới | `32b9217f9004` |
| `godotprompter/skills/godot-testing/references/tdd-workflow.md` | Đã điều chỉnh; xem chi tiết bên dưới | `71320d32947a` |
| `godotprompter/skills/godot-testing/references/testing-patterns.md` | Đã điều chỉnh; xem chi tiết bên dưới | `0477cb70c8f2` |
| `godotprompter/skills/export-pipeline/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `4b0e8f80b2ac` |
| `godotprompter/skills/export-pipeline/references/ci-cd-github-actions.md` | Đã điều chỉnh; xem chi tiết bên dưới | `fabc12c367e2` |
| `godotprompter/skills/export-pipeline/references/distribution-itch-steam.md` | Đã điều chỉnh; xem chi tiết bên dưới | `5a1890a5c7d8` |
| `godotprompter/skills/export-pipeline/references/steam-release-planning.md` | Không phát hiện vùng cần gỡ | `22578251c8f7` |
| `godotprompter/skills/export-pipeline/references/versioning.md` | Không phát hiện vùng cần gỡ | `4b2da3035da6` |
| `godotprompter/skills/animation-system/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `f341f9dadfbe` |
| `godotprompter/skills/animation-system/references/animation-markers.md` | Không phát hiện vùng cần gỡ | `1459b29bc9d6` |
| `godotprompter/skills/animation-system/references/blend-spaces.md` | Không phát hiện vùng cần gỡ | `f091c8d39312` |
| `godotprompter/skills/animation-system/references/bone-constraints.md` | Không phát hiện vùng cần gỡ | `cc1d52ebf0da` |
| `godotprompter/skills/animation-system/references/common-pitfalls.md` | Không phát hiện vùng cần gỡ | `3e42ef0f8619` |
| `godotprompter/skills/animation-system/references/common-recipes.md` | Không phát hiện vùng cần gỡ | `bf87c680e80f` |
| `godotprompter/skills/animation-system/references/ik-recipes.md` | Không phát hiện vùng cần gỡ | `d49c8a22123a` |
| `godotprompter/skills/animation-system/references/ik-solver-comparison.md` | Không phát hiện vùng cần gỡ | `057db3e39f6c` |
| `godotprompter/skills/animation-system/references/retargeting.md` | Không phát hiện vùng cần gỡ | `f317f406a4f3` |
| `godotprompter/skills/animation-system/references/skeleton-modifiers.md` | Không phát hiện vùng cần gỡ | `ef0c70868e71` |
| `godotprompter/skills/animation-system/references/sprite-animation.md` | Không phát hiện vùng cần gỡ | `400d5a9fcc8c` |
| `godotprompter/skills/animation-system/references/state-machine-examples.md` | Không phát hiện vùng cần gỡ | `a1f5889ca445` |
| `godotprompter/skills/beehave/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `409a9b9880b4` |
| `godotprompter/skills/beehave/references/custom-nodes.md` | Không phát hiện vùng cần gỡ | `50a80d18113a` |
| `godotprompter/skills/limboai/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `1a58f819735c` |
| `godotprompter/skills/limboai/references/hsm.md` | Không phát hiện vùng cần gỡ | `71f7a465dec0` |
| `godotprompter/skills/phantom-camera/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `ef7b6fe1b890` |
| `godotprompter/skills/phantom-camera/references/follow-modes.md` | Không phát hiện vùng cần gỡ | `daf024e8eea1` |
| `godotprompter/skills/dialogue-manager/SKILL.md` | Đã điều chỉnh; xem chi tiết bên dưới | `3b91b3b4d8a5` |
| `godotprompter/LICENSE` | Không phát hiện vùng cần gỡ | `075667c180b3` |

## Những phần đã gỡ/điều chỉnh

- `awesome-gamedev/router/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-2d-movement/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-3d-essentials/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-animation/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-audio/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-csharp/SKILL.md`: dòng 27–29: autonomous script/dependency execution instruction; dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-csharp/references/csharp-setup-and-interop.md`: dòng 5–17: installation/automatic workflow section: Project setup; dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `awesome-gamedev/skills/godot/godot-export/SKILL.md`: dòng 27–30: installation/network or autonomous execution instruction; dòng 99–99: installation/network or autonomous execution instruction; dòng 0–0: made frontmatter installation wording descriptive only; dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-export/references/presets-and-cli.md`: dòng 33–46: download/install command or automatic CI configuration block; dòng 77–78: installation/network or autonomous execution instruction; dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `awesome-gamedev/skills/godot/godot-gdscript/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-gdscript-headless-testing/SKILL.md`: dòng 135–151: download/install command or automatic CI configuration block; installation/automatic workflow section: 3. CI step (GitHub Actions) that gates on the exit code; dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-multiplayer/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-nodes-scenes/SKILL.md`: dòng 39–46: autonomous script/dependency execution instruction; dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-nodes-scenes/scripts/check_godot_project.py`: dòng 4–6: autonomous execution directive in helper docstring; installation/network or autonomous execution instruction; dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `awesome-gamedev/skills/godot/godot-physics/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-resources/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-shaders/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-signals-groups/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-tilemap/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/godot/godot-ui-control/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/ai-behavior-trees-utility-ai/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/audio-design/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/camera-systems/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/create-game-assets/SKILL.md`: dòng 97–100: autonomous script/dependency execution instruction; dòng 0–0: changed implicit helper invocation to passive reference; dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/dialogue-systems/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/dialogue-systems/references/runner.md`: dòng 0–0: converted omitted-file links to pinned upstream references; dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `awesome-gamedev/skills/disciplines/game-ai/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/game-feel/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/game-ui-ux/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/input-systems/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/input-systems/references/buffering-and-accessibility.md`: dòng 58–59: removed external artwork retrieval instruction; dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `awesome-gamedev/skills/disciplines/level-design/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/performance-optimization/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/physics-tuning/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/procedural-gen/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/disciplines/save-systems/SKILL.md`: dòng 0–0: added project precedence and no-execution notice; dòng 0–0: converted omitted-file links to pinned upstream references.
- `awesome-gamedev/skills/disciplines/save-systems/references/versioning-and-migration.md`: dòng 0–0: converted omitted-file links to pinned upstream references; dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `awesome-gamedev/skills/disciplines/shader-programming/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/genres/rpg/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/genres/platformer/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/skills/workflows/prototype-fast/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `awesome-gamedev/docs/SKILL-FORMAT.md`: dòng 117–118: installation/network or autonomous execution instruction; dòng 125–164: installation/automatic workflow section: Router and distribution wiring; installation/automatic workflow section: Validation; installation/automatic workflow section: `agents/openai.yaml`; dòng 0–0: converted omitted-file links to pinned upstream references; dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/player-controller/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/mobile-development/SKILL.md`: dòng 26–26: installation/network or autonomous execution instruction; dòng 28–28: installation/network or autonomous execution instruction; dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/mobile-development/references/crash-debugging.md`: dòng 9–9: installation/network or autonomous execution instruction; dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/responsive-ui/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/responsive-ui/references/adaptive-layouts.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/responsive-ui/references/dpi-scaling.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/responsive-ui/references/mobile.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/responsive-ui/references/pixel-art-setup.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/hud-system/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/hud-system/references/damage-numbers.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/hud-system/references/interaction-prompts.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/hud-system/references/minimap.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/hud-system/references/notifications.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/save-load/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/save-load/references/configfile.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/save-load/references/json-saves.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/save-load/references/save-architecture.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/save-load/references/version-migration.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/inventory-system/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/inventory-system/references/equipment.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/inventory-system/references/serialization.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/inventory-system/references/ui-binding.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/state-machine/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/resource-pattern/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/resource-pattern/references/collections.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/resource-pattern/references/configuration-pattern.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/resource-pattern/references/editor-integration.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/resource-pattern/references/saving-resources.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/resource-pattern/references/sharing-vs-unique.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/scene-organization/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/godot-testing/SKILL.md`: dòng 17–17: removed only the framework installation row; kept framework comparison table; dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/godot-testing/references/running-tests.md`: dòng 49–120: download/install command or automatic CI configuration block; installation/automatic workflow section: GitHub Actions CI; dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/godot-testing/references/tdd-workflow.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/godot-testing/references/testing-patterns.md`: dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/export-pipeline/SKILL.md`: dòng 20–21: installation/network or autonomous execution instruction; dòng 165–172: installation/automatic workflow section: 4. CI/CD with GitHub Actions; dòng 187–187: installation/network or autonomous execution instruction; dòng 210–220: installation/automatic workflow section: CI Workflow Note; dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/export-pipeline/references/ci-cd-github-actions.md`: dòng 7–79: download/install command or automatic CI configuration block; dòng 81–81: installation/network or autonomous execution instruction; dòng 0–0: trimmed trailing blank lines (format only); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/export-pipeline/references/distribution-itch-steam.md`: dòng 9–20: download/install command or automatic CI configuration block; installation/automatic workflow section: Install Butler; dòng 45–76: download/install command or automatic CI configuration block; installation/automatic workflow section: GitHub Actions — Deploy to itch.io; dòng 82–82: installation/network or autonomous execution instruction; dòng 81–81: removed remaining manual SDK download instruction (upstream line); dòng 0–0: added project precedence and no-execution notice to modified reference/helper.
- `godotprompter/skills/animation-system/SKILL.md`: dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/beehave/SKILL.md`: dòng 28–37: installation/automatic workflow section: 2. Install & enable; dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/limboai/SKILL.md`: dòng 26–62: installation/automatic workflow section: 2. Install & setup; dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/phantom-camera/SKILL.md`: dòng 29–49: installation/automatic workflow section: 2. Install & setup; dòng 0–0: added project precedence and no-execution notice.
- `godotprompter/skills/dialogue-manager/SKILL.md`: dòng 30–54: installation/automatic workflow section: 2. Install & setup; dòng 0–0: added project precedence and no-execution notice.

Tổng cộng: **153 file nguồn, 84 file điều chỉnh**, trong đó **21 file gỡ/đổi nội dung**; số còn lại chỉ banner/link/định dạng. Không đồng nghĩa mọi file điều chỉnh có mã nguy hiểm.
