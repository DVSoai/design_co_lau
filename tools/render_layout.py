"""Vẽ bố cục bản đồ dạng lưới chữ thành ảnh PNG.

Cách dùng:
    python tools/render_layout.py design/maps/lay_dao_uc_v1.md design/maps/lay_dao_uc_v1.png

Script đọc khối mã đầu tiên có nhãn ```layout trong file Markdown.
Mỗi ký tự là một ô 32x32 trong game; ảnh vẽ mỗi ô 12x12 cho dễ xem.
"""
import re
import sys
from PIL import Image, ImageDraw

CELL = 12
COLORS = {
    '.': (225, 232, 240),  # trống
    '#': (125, 85, 55),    # nền đất, đá
    '=': (217, 178, 95),   # bục đứng được, nhảy xuyên từ dưới
    '~': (79, 143, 166),   # nước
    '^': (178, 58, 46),    # bẫy, chông, vùng nguy hiểm
    'L': (94, 148, 65),    # dây leo, thang
    'S': (46, 79, 163),    # điểm xuất hiện của người chơi
    'E': (107, 74, 140),   # lối ra sang bản đồ khác
    'N': (217, 165, 32),   # NPC
    'm': (230, 140, 120),  # vùng sinh quái thường
    'M': (200, 80, 60),    # vùng sinh tinh anh hoặc thủ lĩnh
    'B': (120, 20, 20),    # điểm boss
    'F': (244, 241, 232),  # cờ lau (giữ ải)
    'T': (150, 150, 150),  # ô dựng công trình (giữ ải)
    'G': (60, 60, 70),     # cổng địch xuất hiện (giữ ải)
    'c': (255, 215, 0),    # rương, vật phẩm nhiệm vụ
    'D': (90, 60, 40),     # cửa, cổng gỗ có thể phá
}

def main(src, out):
    text = open(src, encoding='utf-8').read()
    m = re.search(r"```layout\n(.*?)```", text, re.S)
    if not m:
        sys.exit('Không thấy khối ```layout trong file')
    rows = [r.rstrip('\n') for r in m.group(1).splitlines() if r.strip('\n')]
    w = max(len(r) for r in rows)
    h = len(rows)
    img = Image.new('RGB', (w * CELL, h * CELL), (255, 255, 255))
    d = ImageDraw.Draw(img)
    for y, row in enumerate(rows):
        for x in range(w):
            ch = row[x] if x < len(row) else '.'
            col = COLORS.get(ch, (255, 0, 255))
            d.rectangle([x * CELL, y * CELL, (x + 1) * CELL - 1, (y + 1) * CELL - 1], fill=col)
            if ch not in '.#=~':
                d.text((x * CELL + 3, y * CELL), ch, fill=(0, 0, 0))
    for x in range(0, w, 20):  # vạch mỗi 20 ô = một màn hình ngang
        d.line([x * CELL, 0, x * CELL, h * CELL], fill=(255, 255, 255), width=1)
    img.save(out)
    print(out, f'{w}x{h} ô')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
