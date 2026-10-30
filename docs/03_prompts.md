# Khuôn prompt

Mỗi khuôn có mã P0 đến P17, được `02_asset_list.md` gọi tới. Khi ghép prompt, thay các chỗ trong ngoặc vuông bằng mô tả cụ thể, rồi thay `[STYLE]` và `[AVOID]` bằng nguyên văn hai khối trong `01_art_bible.md`. Prompt luôn bằng tiếng Anh.

Gọi skill bằng cách mở đầu yêu cầu với `$imagegen`, và đính kèm ảnh tham chiếu như `AGENTS.md` quy định.

## P0 — Khám phá phong cách (khuôn lịch sử, đã có ngoại lệ được duyệt)

Quy trình gốc dự kiến ba bản dưới đây; **P0 thực tế đã được duyệt theo quy trình điều chỉnh** (ba cột A pixel chibi, B pixel bán hiện đại, C vẽ tay; bỏ bản không STYLE). Xem `05_log.md`. Không chạy lại khuôn lịch sử này và không hiểu STYLE-B vẽ tay bên dưới là phong cách B đã duyệt:

1. `sty_explore_a`: thay `[STYLE]` bằng khối STYLE trong art bible (phương án A, pixel art).
2. `sty_explore_b`: thay `[STYLE]` bằng STYLE-B dưới đây (vẽ tay).
3. `sty_explore_free`: **xóa** `[STYLE]`, để công cụ tự đề xuất phong cách.

Cả ba bản đều **giữ nguyên khối AVOID**. Sau giai đoạn 0, mọi prompt bắt buộc có khối STYLE đã chốt.

```
Game key art mockup: a young Vietnamese warrior with a simple straight double-edged sword with a small crossguard and cord-wrapped grip stands on a dirt path beside a rice field at dawn, limestone karst mountains reflected in still water behind him, a bamboo-fenced village with thatched roofs on the left, a tall white reed-plume flag planted next to him. Side-scrolling camera, the character in the left third of the frame, a simple health bar and six round skill buttons as placeholder UI at the bottom right. [STYLE] [AVOID]
```

STYLE-B (vẽ tay):

```
Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.
```

## P1 — Ảnh gốc Đinh Bộ Lĩnh

```
Character turnaround sheet of the same young Vietnamese man, about 20 years old, determined calm face, tanned skin, black hair gathered in a small top knot at the crown of his head, no long flowing ponytail, plain undyed short-sleeve tunic and knee-length trousers, barefoot. Show front view, side view facing right, back view and a 3/4 view, standing neutral pose, evenly spaced on a plain flat green #00FF00 background, full body, same height in every view. [STYLE] [AVOID]
```

## P2 — Tách lớp theo bộ phận

```
Use the attached image as the style and proportion reference. Create a parts sheet of this character for a paper-doll animation system, side view facing right: head with hair, torso with arms, legs, shown as separate pieces with a small gap between them, plus the full assembled character at the end of the row. Plain flat green #00FF00 background. [STYLE] [AVOID]
```

## P3 — Bậc trang bị

```
Use the attached image as the style and proportion reference. Same character with exactly the same body shape, side view facing right and front view, now wearing: [TIER]. Show one version holding a simple straight double-edged sword with a small crossguard and cord-wrapped grip and one version holding a bow. Plain flat green #00FF00 background. [STYLE] [AVOID]
```

`[TIER]` theo bậc:

- **t1 (cấp 1):** `coarse brown hemp tunic, rolled-up trousers, straw rope belt, brown cloth head wrap, barefoot; weapon: simple straight double-edged iron sword with a small crossguard and cord-wrapped grip or a simple bamboo bow`
- **t2 (cấp 10):** `indigo-dyed cotton tunic, cloth leg wraps, straw sandals, red head wrap; weapon: plain straight double-edged iron sword with a small crossguard and cord-wrapped grip or a rattan-bound bamboo bow`
- **t3 (cấp 20):** `buffalo-leather chest guard over the indigo tunic, leather bracers, indigo head wrap; weapon: straight double-edged steel sword with a small crossguard and cord-wrapped grip or a horn-reinforced bow`
- **t4 (cấp 30):** `layered leather armor with bronze rivets, leather cap, leather boots; weapon: straight double-edged steel sword with a small bronze crossguard and cord-wrapped grip or a recurve bow with bronze tips`
- **t5 (cấp 40):** `iron scale armor over indigo cloth, simple rounded iron helmet, short dark cape; weapon: straight double-edged tempered-steel sword with a small crossguard and cord-wrapped grip or a large war bow`
- **t6 (cấp 50):** `iron scale armor with bronze trim and shoulder guards, helmet with a red cloth tassel, yellow sash; weapon: straight double-edged dark-steel sword with a small crossguard and cord-wrapped grip or a reinforced war bow`
- **t7 (cấp 60):** `general's armor in black lacquer and gold, a white reed-plume emblem on the chest plate, helmet with a white reed-plume crest, yellow cape; weapon: straight double-edged fine-steel sword with a small plain crossguard, subtle reed motif and cord-wrapped grip or a gold-trimmed war bow`

## P4 — Bảng động tác

Phái Kiếm:

```
Use the attached image as the character reference. Animation sprite sheet of this character with a simple straight double-edged sword with a small crossguard and cord-wrapped grip, side view facing right, plain flat green #00FF00 background, evenly spaced frames in rows: idle breathing (4 frames), run (6 frames), jump and fall (4 frames), three-hit sword combo (8 frames), heavy overhead slash (6 frames), hit reaction (2 frames), knocked down (4 frames). Same size and same foot baseline in every frame. [STYLE] [AVOID]
```

Phái Cung: thay đoạn động tác bằng `idle with bow (4 frames), run (6 frames), jump and fall (4 frames), quick shot (5 frames), charged shot (7 frames), shooting while running (6 frames), hit reaction (2 frames), knocked down (4 frames)`.

## P5 — Đồng minh và NPC

```
Use the attached image as the style and proportion reference. Character design of [WHO], front view and side view facing right, full body, plain flat green #00FF00 background. [STYLE] [AVOID]
```

`[WHO]`:

- **npc_dam_thi:** `a village mother in her 30s, simple brown blouse and long dark skirt, black hair wrapped in a cloth turban, warm but tired face`
- **npc_chu:** `a stern farmer uncle in his 40s, strong and harsh-looking but not evil, rolled sleeves, holding a farming knife`
- **npc_dinh_lien:** `a boy of about 12 who later grows into a young warrior, serious eyes, indigo tunic, small round shield`
- **npc_dinh_dien:** `a hot-tempered burly warrior in his 20s, broad shoulders, leather armor, heavy hardwood club, wild hair under a head wrap`
- **npc_nguyen_bac:** `a calm strategist in his 20s, slim, dark-blue long tunic over trousers, carries a bamboo scroll case and a short sword`
- **npc_le_hoan:** `a young cavalry officer in his early 20s, sharp alert face, light scale armor, bow on his back, a faint air of ambition`
- **npc_luu_co:** `a practical builder and steward in his 30s, rolled sleeves, carries a measuring rope and a wooden mallet`
- **npc_trinh_tu:** `a quartermaster in his 30s, round friendly face, carries rice sacks and a tally stick`
- **npc_tran_lam:** `an elderly warlord in his 60s, white topknot and beard, dignified, worn but fine bronze-trimmed armor, leans on a staff`
- **npc_ngo_chan_luu:** `a Buddhist monk in his 30s, shaved head, brown robe, wooden prayer beads, gentle wise face`
- **npc_ngo_xuong_xi:** `a young noble heir in his 20s, dignified but weary, fine dark robe with simple bronze ornaments, guarded by two soldiers`
- **npc_ngo_nhat_khanh:** `a proud aristocratic lord in his 30s, neat beard, rich indigo robe with a bronze belt`
- **npc_su_tru_tri:** `an old Buddhist abbot, shaved head, saffron-brown robe, holding a wooden fish drum`
- **npc_tho_ren:** `a muscular blacksmith in his 40s, leather apron, soot on arms, hammer and tongs`
- **npc_ba_hang_com:** `a cheerful old woman selling rice and food from bamboo baskets on a carrying pole`
- **npc_ong_lang:** `an old herbal healer with a herb basket and a small mortar`
- **npc_lai_buon:** `a river trader with a cloth bundle on his back and a wooden boat paddle`
- **npc_buon_ngua:** `a horse trader with a whip and a plain straw hat`

## P6 — Quái

```
Use the attached image as the style reference. Enemy sprite design for a side-scrolling action RPG: [ENEMY]. Side view facing left, idle pose and attack pose, plain flat green #00FF00 background, shown next to a faint grey silhouette of the main character for size. [STYLE] [AVOID]
```

Ví dụ `[ENEMY]`: `bandit with a machete`, `Later Ngo spearman in red-brown cloth armor`, `Later Ngo archer in red-brown cloth armor`, `field rat`, `water snake`, `paddy heron`, `wild boar with tusks`, `porcupine`, `rock macaque`, `cave bat`, `young tiger`, `striped adult tiger, larger, scar over one eye`, `straw scarecrow training dummy`, `swamp crocodile`, `pirate with a hook spear`, `river marine with a short spear and rattan shield`, `cavalry rider with a long spear`, `war elephant`. Lính của sứ quân thêm cụm `wearing [COLOR] cloth armor and carrying a small [COLOR] banner`, với màu theo bảng màu cờ trong art bible.

## P7 — Boss

```
Use the attached image as the style and proportion reference. Boss character design: [BOSS]. His army's banner color is [COLOR]. Front view and side view facing left, plus one dramatic attack pose, full body, plain flat green #00FF00 background. Larger and more detailed than normal enemies but in the same style. [STYLE] [AVOID]
```

- **bos_hau_ngo_tien_phong** (đỏ nâu): `a Later Ngo vanguard general in red-brown lacquered leather armor, commanding from a wooden rampart, holding a signal flag`
- **bos_hai_tac** (đen): `a scarred pirate chief on a ship deck, leather vest, swinging an iron grappling hook on a rope`
- **bos_pham_bach_ho** (trắng và xanh biển): `an old but powerful naval veteran in his 60s, white beard, standing on a boat, long spear, armor marked with a white tiger stripe pattern`
- **bos_do_canh_thac** (nâu đất): `a battle-hardened veteran general, heavy scale armor, commanding archers behind layered earthen walls`
- **bos_nguyen_sieu** (xanh nước): `a river-fort lord with a horn trumpet to summon reinforcements by boat, light armor, curved broadsword`
- **bos_la_duong** (cam): `a stocky warlord surrounded by a ring of infantry, big rattan shield and broad blade, shouting orders`
- **bos_ly_khue** (tím): `a nimble warlord fighting in narrow village lanes, long thrusting spear, cloth armor`
- **bos_nguyen_thu_tiep** (đỏ tươi): `a cavalry warlord riding a galloping chestnut horse, long spear, red cape`
- **bos_nguyen_khoan** (xanh rêu): `a marsh lord in reed-woven armor standing on a bamboo walkway over a swamp, three-pronged fishing spear`
- **bos_kieu_cong_han** (xanh lá đậm): `a forest warlord commanding hidden crossbowmen; second image: the same warlord riding a war elephant`
- **bos_kieu_thuan** (xanh lam): `the river lord of a three-river junction, standing on a wooden pier, long-handled halberd, a wave of water rising behind him`

## P8 — Chân dung hội thoại

```
Use the attached images as the style and character references. Dialogue portrait set, head and shoulders, facing slightly right, one portrait per character in a row: [NAMES]. For each, three expressions: neutral, angry, smiling. Plain flat green #00FF00 background. [STYLE] [AVOID]
```

## P9 — Cảnh nền bản đồ

```
Side-scrolling game background for [PLACE], wide panorama split into three parallax layers shown stacked from top to bottom: far layer (sky and distant mountains), middle layer ([MIDDLE]), near layer ([NEAR]). Each layer must tile seamlessly left to right. No characters. [STYLE] [AVOID]
```

## P10 — Tileset

```
Use the attached background as the style reference. Tileset sheet for a side-scrolling platformer set in [PLACE]: ground top tiles, ground fill, left and right ground edges, slopes up and down, floating platform pieces, [PROPS]. Arranged on a 32-pixel grid with clear gaps, plain flat green #00FF00 background. [STYLE] [AVOID]
```

`[PLACE]` / `[MIDDLE]` / `[NEAR]` / `[PROPS]`:

- **lang_hoa_lu:** `a 10th-century Vietnamese village among limestone karst` / `thatched-roof wooden houses on stilts, a banyan tree, a small wooden temple` / `bamboo fence, haystacks, a water buffalo` / `bamboo fence pieces, haystack, well, wooden market stall`
- **dong_chiem:** `low-lying flooded rice paddies` / `rows of rice paddies and a distant village tree line` / `rice stalks, mud dikes, a scarecrow` / `mud dike tiles, water tiles, rice clumps`
- **ben_do:** `a river ferry landing on the Hoang Long river` / `the river with a ferry boat and far bank` / `reeds, mooring posts, wild boar tracks` / `wooden landing planks, mooring post, rope`
- **trang_an:** `limestone karst towers and caves reflected in a river` / `cave mouths and a narrow river with a sampan` / `ferns, hanging vines, rocks` / `rock ledges, cave entrance, vines`
- **dao_uc:** `a rough frontier with a wooden fortified camp` / `earthen ramparts and watchtowers` / `wooden palisade, campfires` / `palisade tiles, wooden gate, watchtower base`
- **dam_dai_hoang:** `a misty swamp` / `reeds and dead trees in fog` / `water lilies, mud` / `mud tiles, reed clumps, floating logs`
- **bo_hai_khau, cua_bien, bai_boi:** `a river-mouth harbor and coastline` / `wooden piers, fishing boats, sails` / `nets, crab traps, rocks` / `pier planks, boat deck, nets`
- **song_dang_chau, binh_kieu:** `wide rivers and a moated earthen town` / `river with war boats, earthen walls` / `bamboo groves, reeds` / `river bank, wooden bridge, boat`
- **do_dong, tay_phu_liet:** `layered earthen fortresses on the Red River plain` / `multiple rings of earthen walls with archers` / `stakes, ditches, banners` / `earthen wall tiles, wooden stakes, gate`
- **te_giang, sieu_loai:** `riverside sandbanks and crowded villages` / `sandbanks and village rooftops` / `narrow village lanes, clay pots` / `sand tiles, lane walls, clay pots`
- **tien_du, phong_chau:** `rolling midland hills and dense forest` / `low green hills and tall forest` / `bushes hiding crossbowmen, wild flowers` / `hill slopes, forest floor, bushes`
- **tam_dai, hoi_ho:** `a marsh fortress and a three-river junction` / `bamboo walkways over swamp, river piers` / `reeds, tangled roots` / `bamboo walkway tiles, pier planks`
- **kinh_thanh:** `the royal citadel of Hoa Lu built with earthen walls joining limestone mountains` / `palace halls with clay-tiled roofs, yellow reed-plume banners` / `guards, stone lanterns` / `citadel wall tiles, palace steps, banners`
- **ao_canh:** `a dreamlike training vision inside a temple, painted in muted sepia tones` / `faded silhouettes of past battlefields` / `incense smoke, fallen banners` / `stone floor tiles, broken banner poles`

## P11 — Thú cưỡi

```
Use the attached image as the style and proportion reference. Mount design for a side-scrolling action RPG: [MOUNT], side view facing right, shown alone, with the main character riding it, and wearing mount gear ([GEAR]). Plain flat green #00FF00 background. [STYLE] [AVOID]
```

- **mnt_trau:** `a sturdy Vietnamese water buffalo with wide curved horns` / `woven saddle cloth, bronze bell, rope halter`
- **mnt_ngua:** `a small sturdy Vietnamese horse` / `leather saddle, bronze-studded bridle, chest armor`
- **mnt_voi:** `an Asian elephant` / `wooden howdah, cloth draping, bronze forehead plate`

## P12 — Bộ khung giao diện

```
Mobile game UI kit in landscape, theme of dark lacquered wood, woven bamboo and bronze trim with a subtle reed-plume motif: dialog box with portrait frame, item slot with normal, rare and legendary borders, round skill button with cooldown overlay, health and mana bars, tab buttons, confirm and cancel buttons, a copper coin with a square hole, a silver ingot and a paper banknote with a red seal as currency icons. Flat front view, no text. [STYLE] [AVOID]
```

## P13 — Màn giao diện

```
Use the attached UI kit as the style reference. Mobile game screen mockup in landscape 16:9: [SCREEN]. Use placeholder bars instead of any text. [STYLE] [AVOID]
```

`[SCREEN]` (bố cục theo Phần 5 của GDD):

- **ui_hud:** `gameplay screen in a frontier camp; top-left portrait with health and mana bars; top-right minimap with menu, bag and top-up buttons; right edge quest tracker panel; bottom-left virtual joystick and jump button; bottom-right a large attack button with six round skill buttons in an arc and a mount button; bottom center two quick-use potion slots and an auto-battle toggle; thin experience bar along the bottom edge`
- **ui_dialog:** `dialogue screen: NPC portrait on the left, dialogue box in the lower half, a column of four choice buttons on the right`
- **ui_shop:** `shop screen split in half: shop items in tabs on the left, player inventory grid on the right, buy and buy-many buttons`
- **ui_menu_tabs:** `character menu with seven tabs on the left edge, the character standing in the center surrounded by ten equipment slots`
- **ui_slot_select:** `title screen with three character save slots side by side, each showing the warrior in different gear, one empty slot with a plus button`
- **ui_blacksmith:** `blacksmith upgrade screen: left a large item slot holding a simple straight double-edged sword with a small crossguard and cord-wrapped grip and a grid of small slots holding whetstones; center a before and after stat panel and a large success-rate area; right an inventory grid; bottom a big hammer button; background a dim forge with an anvil`
- **ui_topup:** `premium shop screen with two tabs: a shop grid priced in banknotes with categories for charms, utilities, fashion and mounts, and a bundles tab of permanent items (a starter bundle chest, fashion sets, decorative mounts, a large leather bag) each with a preview button and a buy button; a banknote balance at the top`
- **ui_world_map:** `region map screen: a hand-drawn map of a river delta region with named map tiles connected by paths, a small reed flag marking the player, quest markers, travel point icons on villages and camps, region tabs along the top`
- **ui_base:** `base-building screen: a side view of a fortified camp among limestone mountains with four fixed building plots (barracks, granary, stable, forge), one plot selected with a panel showing level pips out of three, material slots and a build button`

## P14 — Biểu tượng vật phẩm

```
Use the attached UI kit as the style reference. Sheet of 16 inventory icons on a 64-pixel grid, each centered in its own cell: [ITEMS]. Plain flat green #00FF00 background. [STYLE] [AVOID]
```

Ví dụ `ico_set_01`: `grey whetstone, blue whetstone, purple whetstone, gold whetstone, protective temple talisman, rice ball, grilled fish, square sticky rice cake wrapped in leaves, herbal medicine bottle, buffalo-leather armor, iron scale armor, bamboo bow, iron broadsword, bronze ring, jade pendant, dark soul stone crystal`.

## P15 — Hiệu ứng

```
Use the attached image as the style reference. Visual effects sprite sheet for a side-scrolling action RPG, plain flat black background, evenly spaced frames in rows: [EFFECTS]. Grounded, physical effects only: dust, sparks, wind trails and blood-red impact flashes, no magic glow. [STYLE] [AVOID]
```

`vfx_basic`: `sword slash arc (5 frames), hit spark (4 frames), arrow in flight (1 frame) and arrow impact (3 frames), dizzy stars above a head for stun (4 frames), roots and ropes binding the feet for root (4 frames), dust puff when landing (4 frames), level-up rising light pillar (6 frames), upgrade success hammer flash in gold (6 frames), upgrade fail broken sparks in red (5 frames)`.

## P16 — Công trình giữ ải

```
Use the attached image as the style reference. Prop sheet for a tower-defense mode in a side-scrolling game: sharpened bamboo stake trap, bamboo barricade, wooden crossbow watchtower, war drum on a wooden stand, and a tall white reed-plume flag on a pole. Show each prop in a normal state and a damaged state. Plain flat green #00FF00 background. [STYLE] [AVOID]
```

## P13b — Trạng thái của một màn

Dùng khi một trạng thái làm bố cục khác hẳn (ví dụ thợ rèn đang rèn, nạp khi mất mạng). Đính kèm cả UI kit và mockup trạng thái bình thường của màn đó.

```
Use the attached UI kit and the attached screen mockup as references. Same screen, same layout and sizes, now showing this state: [STATE]. Change only what this state changes. Use placeholder bars instead of any text. [STYLE] [AVOID]
```

Ví dụ `[STATE]`: `the hammer is mid-swing, all buttons dimmed and locked`, `success: a gold flash over the item slot and the upgrade level increased`, `failure: red sparks and a cracked overlay on the item slot`, `no network: the whole panel dimmed with a large disconnected-plug icon in the center`.

## P17 — Tranh cutscene

Mỗi tranh theo đúng một mục trong storyboard (`10_storyboard.md`). Đính kèm ảnh gốc của các nhân vật có trong tranh.

```
Use the attached images as style and character references. Illustrated story panel for a cutscene, landscape 16:9, slightly more detailed than gameplay sprites but in the same style. Shot: [SHOT]. Scene: [SCENE]. Mood and lighting: [MOOD]. Leave the bottom fifth calm and uncluttered for a dialogue box. No text. [STYLE] [AVOID]
```

Ví dụ cho `cs01_3`: `[SHOT]` = `close-up`, `[SCENE]` = `a young boy's hand snapping off a white reed plume and raising it like a flag, rice field and limestone mountains blurred behind`, `[MOOD]` = `golden morning light, gentle wind`.

Riêng `cs03_3` (cảnh giai thoại rồng vàng) là ngoại lệ thứ hai trong `AGENTS.md`: thêm `the image looks like a hazy memory, soft blur and golden glow at the edges, a faint translucent golden dragon coiled protectively around the boy`, và dùng khối AVOID đã bỏ hai cụm `fantasy monsters`, `magic glow effects`.

## Pilot bộ tư thế vẽ trọn — ngoại lệ người dùng29/10/2026

Chỉ nhân vật người dùng STYLE-B vẽ tay bên dưới theo quyết định mới; không
đổi prompt bản đồ/vật thể. Mỗi lần luôn đính kèm `ref_dinh_bo_linh.png`.
Bốn prompt đã gửi nguyên văn (mỗi tờ1 lần, không có lần sinh bị loại):

### poses_body.prompt.txt

```text
Use the attached approved turnaround as the identity/proportion/costume reference, specifically the exact right-facing side profile (second figure). Production pose sheet, clean smooth high-resolution hand-painted art, NOT pixel art, no pixel palette quantization. Same young Vietnamese man, same small topknot and anatomy proportions. Flat pure #00FF00 green background, no gradients or shadows on background. Orthographic side view facing RIGHT in EVERY cell. Even grid, very wide empty green gutters, no overlap, no frames, absolutely no text/numbers. All body anatomy at the SAME SOURCE SCALE in every cell, as though the complete man would be 520 pixels tall; DO NOT enlarge small pieces to fill their cell. Clear neck/hip registration cut planes. No head or legs on torso sheet; no torso on legs sheet. 4 columns by 3 rows, EXACTLY 12 separate torso-with-BOTH-ARMS silhouettes. No heads, crop at base of neck; no legs, crop at tunic hem. Plain short-sleeved undyed cloth tunic over brown tied belt with belt tails; hands closed into fists with a grip hole, anatomically natural arms with visible elbows. Reading order left-to-right then down: 1 relaxed idle arms down; 2 subtly breathing idle arms down; 3 running left arm forward right back; 4 opposite passing run; 5 opposite extension run; 6 opposite run stride; 7 opposite passing; 8 return run extension; 9 jump takeoff both arms swept back; 10 falling arms slightly raised; 11 near arm bent overhead holding an imaginary raised sword with fist HIGH above shoulder, far arm behind; 12 near arm STRAIGHT FORWARD TO RIGHT at shoulder height, far arm behind. Draw NO weapons. Each torso remains vertical and seen strictly from side, hands never missing.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

### poses_head.prompt.txt

```text
Use the attached approved turnaround as the identity/proportion/costume reference, specifically the exact right-facing side profile (second figure). Production pose sheet, clean smooth high-resolution hand-painted art, NOT pixel art, no pixel palette quantization. Same young Vietnamese man, same small topknot and anatomy proportions. Flat pure #00FF00 green background, no gradients or shadows on background. Orthographic side view facing RIGHT in EVERY cell. Even grid, very wide empty green gutters, no overlap, no frames, absolutely no text/numbers. All body anatomy at the SAME SOURCE SCALE in every cell, as though the complete man would be 520 pixels tall; DO NOT enlarge small pieces to fill their cell. Clear neck/hip registration cut planes. No head or legs on torso sheet; no torso on legs sheet. 3 columns by 1 row, EXACTLY 3 separate right-facing profile heads from attached reference, with small neat topknot, black hair, same face, tan skin, cropped at base of neck. Expressions reading order: neutral calm; open mouth battle shout; hurt grimace. Keep IDENTICAL cranial shape and source scale; no torso, no shoulders.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

### poses_legs.prompt.txt

```text
Use the attached approved turnaround as the identity/proportion/costume reference, specifically the exact right-facing side profile (second figure). Production pose sheet, clean smooth high-resolution hand-painted art, NOT pixel art, no pixel palette quantization. Same young Vietnamese man, same small topknot and anatomy proportions. Flat pure #00FF00 green background, no gradients or shadows on background. Orthographic side view facing RIGHT in EVERY cell. Even grid, very wide empty green gutters, no overlap, no frames, absolutely no text/numbers. All body anatomy at the SAME SOURCE SCALE in every cell, as though the complete man would be 520 pixels tall; DO NOT enlarge small pieces to fill their cell. Clear neck/hip registration cut planes. No head or legs on torso sheet; no torso on legs sheet. 5 columns by 2 rows, EXACTLY 10 separate lower-body silhouettes. Start at hip just beneath tunic hem, show brown knee-length trousers, bare shins and barefoot feet. NO torso, arms, head or belt. Reading order: 1 neutral standing legs straight feet on same ground; 2 running stride front leg extended forward right, back leg behind; 3 run passing with back knee bent; 4 run opposite extension; 5 opposite stride; 6 opposite passing; 7 opposite extension; 8 airborne jump knees tucked; 9 airborne fall legs extended; 10 long sword slash stance with front foot to RIGHT and rear foot behind to LEFT, both soles on same level. Both legs fully drawn in every cell. Running 2-7 are six consecutive running beats.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```


## Kiếm/Cung — prompt đã gửi30/10/2026

Luôn đính kèm `art/reference/ref_dinh_bo_linh.png`, STYLE-B và AVOID nguyên văn.
Cung lần1 bị loại vì khoảng kéo dây quá ngắn; bốn prompt hiện hành bên dưới.

### rejected/weapon_cung_attempt1.prompt.txt

```text
Use the attached approved reference ONLY for this Vietnamese character identity, costume, proportions and rendering. Clean smooth high-resolution hand-painted side-view game art, NOT pixel art. Every view faces RIGHT. Flat pure green #00FF00 background, no background shadows. Even widely separated grid, no overlapping cells. Absolutely no labels, numbers, text, decorative frames. Objects at consistent source scale within the sheet. EXACTLY5 separate simple Vietnamese wooden bows, 5 columns by1 row. No people/hands or arrows. Brown wood with pale bowstring. Every shooting bow is VERTICAL and has upper/lower limb tips at the LEFT, with belly curved/bulging outward to the RIGHT. The FRONT/ENEMY is RIGHT and archer is LEFT. String is always LEFT of the wooden curved belly. Reading order: 1 diagonal back-carried bow (upper right to lower left); 2 relaxed upright bow with straight taut string on LEFT; 3 DRAWN bow, vertical wooden belly at RIGHT and string making a clear V-shaped line from upper limb tip LEFTWARDS to a drawing point far LEFT at cheek level, then back to lower limb tip; 4 RELEASED bow, vertical belly at RIGHT with a STRAIGHT VERTICAL STRING ON LEFT connecting limb tips; 5 READY bow, same vertical belly RIGHT and string LEFT with a separate nocked arrow pointing RIGHT at middle. Use same bow silhouette/size for2–5, tiny middle grip on rightmost belly at centre. Do NOT reverse curve or put string in front of the wooden belly. Bow height about two thirds of complete man.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

### weapon_kiem.prompt.txt

```text
Use the attached approved reference ONLY for this Vietnamese character identity, costume, proportions and rendering. Clean smooth high-resolution hand-painted side-view game art, NOT pixel art. Every view faces RIGHT. Flat pure green #00FF00 background, no background shadows. Even widely separated grid, no overlapping cells. Absolutely no labels, numbers, text, decorative frames. Objects at consistent source scale within the sheet. EXACTLY 6 separate weapons, 3 columns by2 rows. A simple STRAIGHT DOUBLE-EDGED SWORD, symmetrical straight blade tapering to a sharp point, SMALL plain crossguard, brown cord-wrapped grip. Limestone grey-green steel (#A5B8B0 main, #718B87 shadow, #D9DDD0 highlight), dark clean outline. NO curved blade, NO ornate fittings. Draw no people/hands. Each sword has a CLEAR GRIP and TIP. Reading order: 1 back-carried, handle at upper RIGHT, blade extends down LEFT behind body; 2 raised preparation, GRIP LOW RIGHT and pointed blade UP LEFT behind head; 3 middle swing, GRIP LOW LEFT and pointed blade UP RIGHT, white PHYSICAL slash trail immediately BEYOND/AROUND THE ADVANCING TIP ON THE RIGHT; 4 horizontal strike, GRIP LEFT and TIP RIGHT, long white physical slash trail immediately AHEAD OF the advancing TIP on the RIGHT; 5 finish, GRIP UP LEFT and TIP DOWN RIGHT, faint white physical trail near advancing tip bottom RIGHT; 6 straight thrust, GRIP LEFT and pointed blade RIGHT horizontally, no trail. All blade silhouettes STRAIGHT. Weapon length about half character height. Trails white brush-like physical motion, not glowing magic. Each cell must contain only its one sword plus its optional attached trail.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

### weapon_cung.prompt.txt

```text
Use the attached approved reference ONLY for this Vietnamese character identity, costume, proportions and rendering. Clean smooth high-resolution hand-painted side-view game art, NOT pixel art. Every view faces RIGHT. Flat pure green #00FF00 background, no background shadows. Even widely separated grid, no overlapping cells. Absolutely no labels, numbers, text, decorative frames. Objects at consistent source scale within the sheet. EXACTLY5 separate simple Vietnamese wooden bows, 3 columns by2 rows, last cell empty green. No people/hands or arrows. Brown wood with pale bowstring. Every shooting bow is VERTICAL and has upper/lower limb tips at the LEFT, with belly curved/bulging outward to the RIGHT. The FRONT/ENEMY is RIGHT and archer is LEFT. String is always LEFT of the wooden curved belly. Reading order: 1 diagonal back-carried bow (upper right to lower left); 2 relaxed upright bow with straight taut string on LEFT; 3 DRAWN bow, vertical wooden belly at RIGHT and string making a clear V-shaped line from upper limb tip LEFTWARDS to a drawing point far LEFT at cheek level, the horizontal draw distance from middle grip to pulled string point must be about 70 percent of the bow HEIGHT (deep wide V, long draw; very wide space allowed in the third cell), then back to lower limb tip; 4 RELEASED bow, vertical belly at RIGHT with a STRAIGHT VERTICAL STRING ON LEFT connecting limb tips; 5 READY bow, same vertical belly RIGHT and string LEFT with a separate nocked arrow pointing RIGHT at middle. All bow HEIGHTS must match, and the drawn bow is dramatically WIDER toward LEFT. Use same bow silhouette/size for2–5, tiny middle grip on rightmost belly at centre. Do NOT reverse curve or put string in front of the wooden belly. Bow height about two thirds of complete man.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

### arrow.prompt.txt

```text
Use the attached approved reference ONLY for this Vietnamese character identity, costume, proportions and rendering. Clean smooth high-resolution hand-painted side-view game art, NOT pixel art. Every view faces RIGHT. Flat pure green #00FF00 background, no background shadows. Even widely separated grid, no overlapping cells. Absolutely no labels, numbers, text, decorative frames. Objects at consistent source scale within the sheet. EXACTLY2 arrows,2 columns by1 row, generous green gap. Each is horizontally oriented LEFT to RIGHT. Simple wooden shaft, pale grey stone/steel arrowhead at far RIGHT, brown feather fletching at LEFT. First arrow whole in flight. Second arrow impacted/broken close to tip, with tip STILL RIGHT and feather tail LEFT. No bow, no people, no trails, no background. Full arrow clearly visible in each cell.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```

### poses_body_cung.prompt.txt

```text
Use the attached approved reference ONLY for this Vietnamese character identity, costume, proportions and rendering. Clean smooth high-resolution hand-painted side-view game art, NOT pixel art. Every view faces RIGHT. Flat pure green #00FF00 background, no background shadows. Even widely separated grid, no overlapping cells. Absolutely no labels, numbers, text, decorative frames. Objects at consistent source scale within the sheet. EXACTLY4 TORSO-WITH-BOTH-ARMS painted poses,4 columns by1 row, same undyed short sleeve tunic, brown tied belt and belt tails as attached reference. HEADLESS: crop across BASE OF NECK; LEGLESS: crop below tunic hem. No weapons/bows/strings/arrows drawn; these are separate sprites. All fists clearly drawn. Same torso height/width, source scale as a complete man about520px tall. Reading order: 1 bow rest, FAR ARM extended forward RIGHT horizontally at SHOULDER LEVEL with fist grasping imaginary vertical bow, near hand relaxed in front of chest; 2 drawing, FAR ARM straight forward RIGHT at SHOULDER LEVEL, near elbow points LEFT and near fist pulled beside cheek/neck ABOVE SHOULDER, drawing imaginary string LEFT; 3 release, FAR ARM stays extended RIGHT in exactly same position, near fist springs backward LEFT past neck; 4 running shoot, torso leans slightly RIGHT, far arm extended RIGHT shoulder height, near fist pulled to cheek. Important FAR holding hand is the RIGHTMOST hand, shooting arm has proper shoulder/elbow anatomy. Do not add a head just because the near fist is cheek height.

Style: hand-painted 2D game art for a side-scrolling mobile action RPG, slightly stylized proportions about 4 heads tall, clean ink outline, flat colors with soft gouache shading, light source from top-left. Setting: northern Vietnam in the 10th century, earthy palette of rice-field green, limestone grey, earth brown and straw yellow, with red reserved for battle and fire.

Avoid: Japanese covert-warrior or samurai clothing, katanas, Chinese imperial dragon robes, Nguyen-dynasty ao dai, conical palm-leaf hats with tassels, winged mandarin hats, multi-tiered curved palace roofs, stone castles with towers, red flags, fantasy monsters, magic glow or glowing energy slashes, modern objects, any text, letters, logos or watermarks.
```
