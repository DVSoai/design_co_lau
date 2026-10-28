extends RefCounted

# Các giá trị A0 chỉ là tạm thời; không chốt thông số thiết kế.
const RUN_SPEED := 200.0 # px/s
const ACCELERATION := 900.0 # px/s², cả tăng tốc và hãm
const JUMP_HEIGHT := 96.0 # px
const TIME_TO_APEX := 0.38 # s
const GRAVITY := 2.0 * JUMP_HEIGHT / (TIME_TO_APEX * TIME_TO_APEX) # px/s²
const JUMP_SPEED := -2.0 * JUMP_HEIGHT / TIME_TO_APEX # px/s
const COYOTE_TIME := 0.10 # s sau khi rời mép
const JUMP_BUFFER := 0.12 # s giữ yêu cầu nhảy trước khi chạm đất
const PLAYER_BOX := Vector2(24, 88) # px, rộng × cao; gốc ở chân
const SPRITE_OFFSET := Vector2(0, -56) # px; chân hình cách đáy PNG 8 px
# Chuyển động giả chỉ biến đổi Sprite2D, không đổi body/Area2D.
const FAKE_MOTION_ENABLED := true # bật mặc định; công tắc ⚙ chỉ đổi trong RAM
const IDLE_BOB_AMPLITUDE := 1.0 # px, biên độ ± theo trục y
const IDLE_BOB_PERIOD := 1.2 # s/chu kỳ
const RUN_BOB_AMPLITUDE := 2.0 # px, biên độ ± theo bước chân
const RUN_STEP_DISTANCE := 100.0 # px/chu kỳ: period = distance / abs(speed)
const RUN_LEAN_DEGREES := 4.0 # độ theo hướng vận tốc chạy
const RUN_MOTION_THRESHOLD := 1.0 # px/s, dưới ngưỡng này coi là đứng yên
const JUMP_SPRITE_SCALE := Vector2(0.9, 1.1) # tỉ lệ x/y lúc bật nhảy
const LAND_SPRITE_SCALE := Vector2(1.15, 0.85) # tỉ lệ x/y lúc chạm đất
const SPRITE_SCALE_RECOVERY := 0.1 # s, hồi tuyến tính về (1, 1)
const SLASH_SPRITE_SHIFT := 4.0 # px theo hướng nhìn trong cửa sổ trúng
const VIEWPORT := Vector2(960, 540) # px, khớp project.godot
const CAMERA_DEAD_ZONE := Vector2(100, 60) # px, nửa rộng × nửa cao
const CAMERA_LOOK_AHEAD := 100.0 # px theo hướng nhìn
const CAMERA_RESPONSE := 5.0 # 1/s, tốc độ tiến tới đích camera
const ATTACK_DURATION := 0.30 # s từ bắt đầu đến hết động tác
const HIT_START := 0.10 # s từ đầu đòn
const HIT_END := 0.20 # s từ đầu đòn; cuối cửa sổ trúng
const ATTACK_COOLDOWN := 0.15 # s sau khi hết động tác
const SLASH_BOX := Vector2(56, 56) # px, rộng × cao
const SLASH_OFFSET := Vector2(34, -52) # px từ chân, x theo hướng nhìn
const SLASH_ARC_RADIUS := 48.0 # px, vệt chém tạm
const DAMAGE := 10 # điểm sát thương/đòn
const DAMAGE_FLOAT_TIME := 0.65 # s
const DAMAGE_FLOAT_DISTANCE := 38.0 # px
const WORLD_SIZE := Vector2(2880, 540) # px, ba màn hình ngang
const SPAWN := Vector2(100, 460) # px
const FALL_RESET_Y := 720.0 # px; rơi khỏi bản đồ thì về điểm đầu
const DUMMY_POSITION := Vector2(490, 460) # px
const DUMMY_BOX := Vector2(32, 88) # px
const TOUCH_BUTTON_SIZE := Vector2(84, 84) # px trên viewport 960×540
const TOUCH_MARGIN := 24.0 # px
const TOUCH_GAP := 12.0 # px
# Hình học bản đồ: x, y, rộng, cao (px).
const TERRAIN := [
	Rect2(0, 460, 720, 80), Rect2(816, 460, 2064, 80),
	Rect2(280, 428, 64, 32), Rect2(1100, 428, 96, 32),
	Rect2(1196, 396, 96, 64), Rect2(1292, 364, 96, 96),
	Rect2(1550, 396, 150, 16), Rect2(1810, 364, 150, 16),
	Rect2(2070, 396, 150, 16),
]

# Bố cục điều khiển/HUD placeholder: đơn vị px logic nếu không ghi khác.
const HOLD_AUTO_JUMP := true # giữ nút để nhảy lại khi chạm đất
const VARIABLE_JUMP := false # nhả sớm giảm vận tốc đi lên
const JUMP_RELEASE_MULTIPLIER := 0.5 # tỉ lệ vận tốc khi nhả sớm
const DIAGONAL_SPIN_ENABLED := true # chỉ xoay Sprite2D
const DIAGONAL_SPIN_TURNS := 1.0 # vòng/nhảy; thời gian = 2 × TIME_TO_APEX
const HUD_VISIBLE := true # HUD giữ chỗ, không có hệ thống game
const DPAD_RIGHT_OFFSET_RATIO := 2.2 # lần d, khoảng lệch x giữa hai nút dưới
const DPAD_UP_OFFSET_RATIO := 1.35 # lần d, khoảng lệch y của nút ↑
const DIAGONAL_DEBUG_BORDER_WIDTH := 1.0 # px, chỉ vẽ viền vùng chéo khi F1
const DIAGONAL_WIDTH_RATIO := 0.9 # lần nút di chuyển
const SLASH_BUTTON_RATIO := 1.4 # lần nút di chuyển
const SMALL_BUTTON_RATIO := 0.65 # lần nút di chuyển
const SKILL_BUTTON_RATIO := 0.7 # lần nút di chuyển
const SKILL_COUNT := 5 # ô giữ chỗ
const SKILL_GAP := 6.0 # px
const TOUCH_FILL_ALPHA := 0.45 # độ trong mờ nền nút/HUD
const TOUCH_PRESSED_SCALE := 0.95 # tỉ lệ nút đang giữ
const TOUCH_FONT_SIZE := 22 # px logic
const TOUCH_BORDER_WIDTH := 2.0 # px
const TOUCH_BORDER := Color(0.72, 0.8, 0.9, 0.85) # màu/alpha viền bình thường
const TOUCH_PRESSED_BORDER := Color(1, 1, 1, 1) # màu/alpha viền đang chạm
const POTION_INITIAL_COUNT := 5 # số giữ chỗ, không tác động máu/nội lực
const GEAR_SIZE := Vector2(56, 56) # px
const HUD_MENU_SIZE := Vector2(56, 56) # px
const HUD_MAP_SIZE := Vector2(120, 80) # px
const HUD_LEVEL_SIZE := Vector2(56, 56) # px
const HUD_BAR_SIZE := Vector2(180, 18) # px
const HUD_BAR_GAP := 6.0 # px
const TUNING_PANEL_WIDTH := 438.0 # px
const TUNING_PANEL_MAX_HEIGHT := 366.0 # px
const TUNING_PANEL_MIN_HEIGHT := 120.0 # px
const COMBAT_EFFECT_Z := 20 # lớp vẽ trên thân nhân vật/hình nộm
const DAMAGE_TEXT_Z := 30 # lớp vẽ số sát thương

# Kiểu cổ điển; nhánh cũ dùng lại chiều cao cũ khi tắt công tắc.
const CLASSIC_CONTROLS := true # mặc định bật
const AIR_JUMP_ENABLED := true # khinh công, tối đa một lần mỗi cú nhảy
const LEGACY_JUMP_HEIGHT := 80.0 # px, mặc định của kiểu điều khiển cũ
const STOP_TIME := 0.08 # s, giảm tốc từ vận tốc hiện tại về 0
const TURN_TIME := 0.05 # s, nhịp đứng khi đổi mặt trên mặt đất
const APEX_FLIP_TIME := 0.2 # s/vòng lộn, chỉ Sprite2D
const FALL_SPEED_MULTIPLIER := 2.0 # lần |JUMP_SPEED|
const FALL_SPEED_MAX := FALL_SPEED_MULTIPLIER * absf(JUMP_SPEED) # px/s, suy ra
const CLASSIC_DIAGONAL_SPEED_RATIO := 0.8 # lần RUN_SPEED khi giữ vùng chéo
const AIR_JUMP_WINDOW_RATIO := 0.3 # lần |JUMP_SPEED|, chỉ khi còn đi lên
const AIR_JUMP_SPEED_RATIO := 0.7 # lần JUMP_SPEED của cú bật thêm
