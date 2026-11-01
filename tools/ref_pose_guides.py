#!/usr/bin/env python3
"""Tạo KHUÔN TƯ THẾ (pose guide) cho từng khung từ số liệu game tham khảo.

Mỗi khung xuất một ảnh chỉ có BÓNG PHẲNG theo màu lớp (không có nét vẽ, mặt, màu áo của
game tham khảo), đã đổi về cỡ nhân vật Cờ Lau:
  đầu = đỏ, thân (kèm tay) = xanh lá, chân = xanh dương, vũ khí cầm tay = vàng,
  khung bao từng lớp + tâm khung bao, gốc chân (dấu thập trắng), vạch chiều cao.
Dùng làm ảnh đính kèm khi tạo ảnh ("giữ đúng dáng và vị trí các mảng màu này") và để tự soát.

Ảnh chỉ để trong thư mục tạm, KHÔNG commit.

  python3 tools/ref_pose_guides.py --server <giải nén zip server> --client <giải nén zip client> \
      [--out /tmp/ref_pose] [--scale 2]
  --scale 1 → người cao ~128 px (cỡ hiển thị); 2 → ~256 px (cỡ vẽ nguồn, khuyên dùng).
Xuất: khung_00.png … khung_29.png (bản không vũ khí), khung_XX_kiem.png / khung_XX_cung.png
(khung có vũ khí cầm tay), bang_khuon.png (tờ tổng 30 khung), khuon.json (khung bao từng lớp).
"""
import argparse, json, importlib.util
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ref_render', HERE / 'ref_render.py')
rr = importlib.util.module_from_spec(spec); spec.loader.exec_module(rr)

COLORS = {'dau': (220, 60, 60), 'than': (60, 170, 80), 'chan': (60, 110, 220), 'vu_khi': (235, 190, 40)}
LAYER_INDEX = {'dau': 0, 'chan': 1, 'than': 2, 'vu_khi': 3}
DRAW_ORDER = ['chan', 'than', 'dau', 'vu_khi']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--server', required=True); ap.add_argument('--client', required=True)
    ap.add_argument('--out', default='/tmp/ref_pose'); ap.add_argument('--scale', type=float, default=2)
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    data = rr.find(a.server, 'nj_part').parent; icon = rr.find(a.server, 'icon') / '4'
    parts = rr.load_parts(data / 'nj_part'); T = rr.load_frames(rr.find(a.client, 'Char.java'))
    sets = {'dau': parts[2][1], 'chan': parts[0][1], 'than': parts[1][1]}
    weapons = {'kiem': parts[12][1], 'cung': parts[14][1]}
    Z = 4                                   # ảnh icon/4
    k = 128 / 131 * a.scale                 # đổi 131 px (người tham khảo ở icon/4) → 128 px × scale
    W, H = int(200 * a.scale), int(200 * a.scale)
    GX, GY = W // 2, int(H * 0.85)          # gốc chân trên canvas khuôn
    cache = {}

    def mask(iid):
        if iid not in cache:
            p = icon / f'{iid}.png'
            if not p.exists(): cache[iid] = None
            else:
                im = Image.open(p).convert('RGBA')
                cache[iid] = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
        return cache[iid]

    report = {}
    sheet_cells = []
    for f in range(30):
        variants = [None] + (['kiem', 'cung'] if T[f][3] and T[f][3][0] else [])
        for wv in variants:
            cv = Image.new('RGBA', (W, H), (24, 28, 36, 255)); d = ImageDraw.Draw(cv)
            boxes = {}
            for name in DRAW_ORDER:
                part = weapons[wv] if name == 'vu_khi' and wv else sets.get(name)
                if part is None: continue
                e = T[f][LAYER_INDEX[name]]
                if not e or e[0] >= len(part): continue
                idx, dx, dy = e; iid, pdx, pdy = part[idx]
                g = mask(iid)
                if g is None or iid <= 0: continue
                unit = Z * k                       # 1 đơn vị gốc → px trên khuôn
                x = GX + round((dx + pdx) * unit)
                y = GY + round((-dy + pdy) * unit)
                flat = Image.new('RGBA', g.size, COLORS[name] + (255,))
                flat.putalpha(g.split()[3].point(lambda v: 210 if v > 40 else 0))
                cv.alpha_composite(flat, (x, y))
                bb = g.getbbox()
                if bb:
                    b = (x + bb[0], y + bb[1], x + bb[2], y + bb[3])
                    d.rectangle(b, outline=COLORS[name] + (255,), width=1)
                    boxes[name] = {'x': b[0] - GX, 'y': b[1] - GY, 'w': b[2] - b[0], 'h': b[3] - b[1],
                                   'anh_tham_khao': iid, 'khung_dx_dy': [dx, dy], 'hinh_dx_dy': [pdx, pdy]}
            # gốc chân + vạch chiều cao 128·scale
            d.line((GX - 8, GY, GX + 8, GY), fill='white'); d.line((GX, GY - 8, GX, GY + 8), fill='white')
            top = GY - round(128 * a.scale); d.line((8, top, 24, top), fill='white'); d.line((16, top, 16, GY), fill=(255, 255, 255, 90))
            d.text((6, 4), f'khung {f:02d}' + (f' {wv}' if wv else ''), fill='white')
            name = f'khung_{f:02d}' + (f'_{wv}' if wv else '') + '.png'
            cv.save(out / name); report[name[:-4]] = boxes
            if wv is None: sheet_cells.append(cv.resize((W // 2, H // 2)))
    cols = 10; cw, ch = sheet_cells[0].size
    sheet = Image.new('RGBA', (cols * cw, 3 * ch), (24, 28, 36, 255))
    for i, c in enumerate(sheet_cells): sheet.paste(c, ((i % cols) * cw, (i // cols) * ch))
    sheet.save(out / 'bang_khuon.png')
    (out / 'khuon.json').write_text(json.dumps({'scale': a.scale, 'goc_chan': [GX, GY], 'nguoi_cao_px': round(128 * a.scale),
                                                 'khung': report}, ensure_ascii=False, indent=1))
    print(f'Đã xuất {len(report)} khuôn + bang_khuon.png + khuon.json vào {out}')


if __name__ == '__main__':
    main()
