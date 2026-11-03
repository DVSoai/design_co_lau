#!/usr/bin/env python3
"""Cắt ảnh có sẵn và ghép thử, không sinh/vẽ lại nhân vật.

Cần Pillow, numpy, scipy. Ví dụ (nguồn ảnh nằm ngoài worktree):
  python3 tools/dbl_cat_ghep.py --source-dir /tmp/dbl_tam_goc \
    --source-commit 8764459003af23de08656ba254b42255435f55c4 \
    --server /workspace/ns-server --client /workspace/ns-201

Chạy lại giữ nguyên vị trí trong ghep/dbl_vi_tri.json để chỉnh tay.
--audit-only chỉ đếm và in bbox, không ghi ảnh. Bbox dùng [x0,y0,x1,y1),
đơn vị pixel ảnh gốc. Chỉ đọc ID hình từ bảng tham khảo, không dùng dx/dy.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from ref_render import find, load_frames, load_parts

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'art/concept/characters/chr_dbl_chibi_gemini'
# Số hàng/cột là hợp đồng kiểm đếm, không chia ô để ép số lượng thành phần.
SHEETS = {
    'tam_chan_8_hinh': ([4, 4], dict(enumerate(range(24, 32), 1))),
    'tam_than_a_10_hinh': ([3, 3, 4], {2: 7, 4: 9, 6: 8, 7: 10, 9: 12, 10: 13}),
    'tam_than_a_sua_2_hinh': ([2], {1: 11, 2: 6}),
    'tam_than_b_10_hinh': ([3, 3, 4], {1: 14, 3: 16, 6: 17, 7: 19, 9: 20}),
    'tam_than_b_sua_4_hinh': ([2, 2], {1: 15, 2: 18, 4: 21}),
}
# Dấu sao đè nét thật: không thể bỏ dấu mà giữ nguyên hình; không xuất mảnh đó.
DAMAGED = {('tam_than_a_10_hinh', 10): 'dấu sao đè vạt áo: không xuất dbl_13',
           ('tam_than_b_10_hinh', 10): 'dấu sao đè eo; hình không được gán số'}
# Neo đo trên CHÍNH ảnh cắt của bộ này: cổ áo, giữa đai; không lấy offset tham khảo.
# Tọa độ tỉ lệ trong bbox, được lưu thành pixel và có thể sửa trong JSON.
BODY_ANCHORS = {
    5: ((.56, .045), (.53, .57)),
    6: ((.46, .06), (.43, .56)), 7: ((.54, .04), (.53, .56)),
    8: ((.53, .07), (.53, .55)), 9: ((.54, .055), (.54, .57)),
    10: ((.53, .06), (.52, .55)), 11: ((.40, .055), (.40, .55)),
    12: ((.59, .40), (.60, .73)),
    14: ((.52, .045), (.51, .56)), 15: ((.51, .05), (.51, .56)),
    16: ((.52, .045), (.51, .56)), 17: ((.53, .07), (.53, .55)),
    18: ((.55, .30), (.55, .64)), 19: ((.53, .06), (.52, .55)),
    20: ((.59, .40), (.60, .73)), 21: ((.32, .06), (.38, .55)),
}


def key_mask(image):
    rgb = np.asarray(image.convert('RGB')).astype(np.int16)
    r, g, b = rgb.transpose(2, 0, 1)
    return ~((g > r + 18) & (g > b + 18) & (g > 75))


def components(path):
    image = Image.open(path).convert('RGBA')
    mask = key_mask(image) & (np.asarray(image)[:, :, 3] > 0)
    labels, _ = ndimage.label(mask)
    sizes = np.bincount(labels.ravel())
    if len(sizes) < 2:
        raise SystemExit(f'DỪNG: không có hình trong {path}')
    # Chữ và dấu sao rời nhỏ hơn nhiều so với bất kỳ hình người nào trên tấm.
    ids = np.flatnonzero(sizes >= sizes[1:].max() * .08)
    slices = ndimage.find_objects(labels)
    figures = []
    for idx in ids:
        if idx == 0:
            continue
        sy, sx = slices[idx - 1]
        bbox = [sx.start, sy.start, sx.stop, sy.stop]
        figures.append({'bbox': bbox, 'label': int(idx), 'area': int(sizes[idx]),
                        'cx': (sx.start + sx.stop) / 2, 'cy': (sy.start + sy.stop) / 2})
    return image, labels, figures


def ordered(figures, rows, filename):
    if len(figures) != sum(rows):
        raise SystemExit(f'DỪNG: {filename}: có {len(figures)} hình, cần {sum(rows)}; không đoán')
    # Tay giơ cao có thể vượt hàng. Nhóm theo tâm hình rồi sắp X trong hàng.
    pending = sorted(figures, key=lambda f: f['cy'])
    result = []
    offset = 0
    for row, count in enumerate(rows, 1):
        group = sorted(pending[offset:offset + count], key=lambda f: f['cx'])
        for col, fig in enumerate(group, 1):
            result.append(dict(fig, row=row, col=col))
        offset += count
    return result


def cropped(image, labels, fig):
    x0, y0, x1, y1 = fig['bbox']
    out = np.array(image.crop((x0, y0, x1, y1)))
    # Giữ đúng thành phần liền nhau; chữ/dấu sao rời không được đưa vào PNG.
    out[:, :, 3] = np.where(labels[y0:y1, x0:x1] == fig['label'], out[:, :, 3], 0)
    return Image.fromarray(out)


def collar_brown(image):
    a = np.array(image)
    r, g, b = a[:, :, :3].astype(np.int16).transpose(2, 0, 1)
    yy, xx = np.indices(r.shape)
    mask = ((b > r + 4) & (r < 75) & (b < 105) & (g < 95) &
            (yy < image.height * .23) & (xx > image.width * .20) &
            (xx < image.width * .70) & (a[:, :, 3] > 0))
    if not mask.any():
        raise SystemExit('DỪNG: không tìm được cổ áo xanh đen để đổi màu')
    # Chỉ đổi RGB trong vùng cổ áo; giữ nguyên alpha và độ sáng tương đối.
    light = a[:, :, :3].astype(float).mean(axis=2)
    for c, factor in enumerate((1.35, .94, .66)):
        a[:, :, c][mask] = np.clip(light[mask] * factor, 0, 255).astype('uint8')
    ys, xs = np.where(mask)
    print(f'  đổi riêng cổ áo: {mask.sum()} px; bbox={[int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)]}')
    return Image.fromarray(a)


def audit(source):
    audits = []
    for name, (rows, mapping) in SHEETS.items():
        path = source / (name + '.png')
        image, labels, figures = components(path)
        figures = ordered(figures, rows, path.name)
        print(f'TẤM {path.name}: {len(figures)}/{sum(rows)} hình; SHA256={hashlib.sha256(path.read_bytes()).hexdigest()}')
        for cell, fig in enumerate(figures, 1):
            target = mapping.get(cell)
            suffix = f'dbl_{target}' if target is not None else 'không gán số: bỏ qua'
            print(f'  hàng {fig["row"]} cột {fig["col"]}: bbox={fig["bbox"]}; diện tích={fig["area"]}; {suffix}')
            if (name, cell) in DAMAGED:
                print('  LƯU Ý:', DAMAGED[name, cell])
        audits.append((name, image, labels, figures, mapping, path))
    for idx in (32, 33, 35, 5, 23):
        path = BASE / f'dbl_{idx}.png'
        image, labels, figures = components(path)
        if len(figures) != 1:
            raise SystemExit(f'DỪNG: {path.name}: {len(figures)} hình, cần 1')
        print(f'ẢNH {path.name}: bbox={figures[0]["bbox"]}; SHA256={hashlib.sha256(path.read_bytes()).hexdigest()}')
        audits.append((path.stem, image, labels, figures, {1: idx}, path))
    return audits


def read_ids(server, client):
    frames = load_frames(find(client, 'Char.java'))
    parts = load_parts(find(server, 'nj_part'))
    # Chỉ lấy image ID ở cột 0. Không đọc offset để đặt mảnh.
    return {f: [parts[2][1][frames[f][0][0]][0],
                parts[0][1][frames[f][1][0]][0],
                parts[1][1][frames[f][2][0]][0]]
            for f in list(range(8)) + list(range(12, 30))}


def placements(pieces, frame_ids, manifest, source_commit):
    # Đo trên ảnh mẫu của chính bộ dbl, canvas 2048²:
    # đỉnh tóc y=175, cằm=1125, cổ=1120, đai=1440, sàn=1997.
    # Cả bộ dùng cùng đích 130/(1997-175), không có offset/bbox game ngoài.
    sample_factor = 130 / (1997 - 175)
    head_h = (1125 - 175) * sample_factor
    neck_waist = (1440 - 1120) * sample_factor
    waist_floor = (1997 - 1440) * sample_factor
    canvas = [220, 180]
    floor, center = 164, 110
    defaults = {}
    for frame, (head, leg, body) in frame_ids.items():
        hi, li, bi = (pieces[n] for n in (head, leg, body))
        hn = (.67, .997)  # đáy cằm ngay trên cổ áo, đo trên đầu của bộ này
        neck, waist = BODY_ANCHORS[body]
        bs = neck_waist / ((waist[1] - neck[1]) * bi.height)
        hs = head_h / hi.height
        # Chuẩn hóa từng mảnh bằng cùng đoạn eo-sàn của ảnh mẫu; không ép bbox tham khảo.
        ls = waist_floor / li.height
        lx = center - li.width * ls * .50
        ly = floor - li.height * ls
        waist_x, waist_y = center, ly + 1
        bx = waist_x - waist[0] * bi.width * bs
        by = waist_y - waist[1] * bi.height * bs
        nx, ny = bx + neck[0] * bi.width * bs, by + neck[1] * bi.height * bs
        hx, hy = nx - hn[0] * hi.width * hs, ny - hn[1] * hi.height * hs + 1
        idle = frame in (0, 1)
        order = ['leg', 'body', 'head'] if idle else ['leg', 'head', 'body']
        defaults[str(frame)] = {'parts': {'head': head, 'leg': leg, 'body': body},
                                'draw_condition': 'statusMe 1/6' if idle else 'statusMe khác 1/6', 'order': order,
                                'head': {'x': round(hx, 3), 'y': round(hy, 3), 'scale': hs},
                                'leg': {'x': round(lx, 3), 'y': round(ly, 3), 'scale': ls},
                                'body': {'x': round(bx, 3), 'y': round(by, 3), 'scale': bs}}
    return {'schema': 1, 'source_commit': source_commit, 'source_figures': manifest,
            'canvas': canvas, 'floor_y': floor,
            'sample': {'path': 'dbl_mau_bang_do.png', 'top_y': 175, 'chin_y': 1125,
                       'neck_y': 1120, 'waist_y': 1440, 'floor_y': 1997,
                       'neutral_target_height': 130, 'note': 'Neo do ảnh của bộ dbl; vị trí từng khung sửa trực tiếp bên dưới.'},
            'frames': defaults}


def render(pieces, config, frame_ids, out):
    cells, errors, stats = [], [], []
    for frame, expected in frame_ids.items():
        f = config['frames'][str(frame)]
        if [f['parts'][key] for key in ('head', 'leg', 'body')] != expected:
            raise SystemExit(f'DỪNG: JSON khung {frame}: ID mảnh không khớp bảng')
        cv = Image.new('RGBA', tuple(config['canvas']))
        layers = {}
        for key in ('head', 'leg', 'body'):
            p = f[key]
            im = pieces[f['parts'][key]]
            # Co giãn ĐỀU, không xoay, không sửa nét. Cỡ raster làm tròn tới pixel.
            im = im.resize((round(im.width * p['scale']), round(im.height * p['scale'])), Image.Resampling.LANCZOS)
            layer = Image.new('RGBA', cv.size)
            pos = (round(p['x']), round(p['y']))
            layer.alpha_composite(im, pos)
            layers[key] = layer
            if pos[0] < 0 or pos[1] < 0 or pos[0]+im.width > cv.width or pos[1]+im.height > cv.height:
                errors.append(f'{frame:02d}: lớp {key} vượt canvas')
        for key in f['order']:
            cv.alpha_composite(layers[key])
        bbox = cv.getbbox()
        height = bbox[3] - bbox[1]
        hb = layers['head'].getbbox()
        ratio = (hb[3] - hb[1]) / height
        lb = layers['leg'].getbbox()
        if lb[3] != config['floor_y']:
            errors.append(f'{frame:02d}: đáy chân={lb[3]}, sàn={config["floor_y"]}')
        # Đo phần miệng thực từ ảnh đầu: vùng này chỉ dùng phát hiện bị thân che,
        # không đổi nét và không làm căn cứ tự công nhận chất lượng thẩm mỹ.
        head_alpha = np.array(layers['head'])[:, :, 3]
        body_alpha = np.array(layers['body'])[:, :, 3]
        hx0, hy0, hx1, hy1 = hb
        mouth = np.zeros(head_alpha.shape, dtype=bool)
        mx0, mx1, my0, my1 = {32: (.58, .72, .875, .912),
                                    33: (.59, .71, .867, .890),
                                    35: (.59, .72, .880, .950)}[expected[0]]
        mouth[hy0+round((hy1-hy0)*my0):hy0+round((hy1-hy0)*my1),
              hx0+round((hx1-hx0)*mx0):hx0+round((hx1-hx0)*mx1)] = True
        if f['order'].index('body') > f['order'].index('head') and np.any(mouth & (head_alpha > 128) & (body_alpha > 128)):
            errors.append(f'{frame:02d}: thân có thể che miệng, cần nâng đầu bằng JSON')
        cv.save(out / f'dbl_khung_{frame:02d}.png')
        print(f'KHUNG {frame:02d}: đầu/chân/thân={expected}; cao={height}px; đầu/người={ratio:.4f}; thứ tự={"/".join(f["order"])}')
        stats.append({'frame': frame, 'parts': expected, 'height': height, 'head_ratio': ratio})
        cells.append((frame, expected, cv))
    # Tờ soát chỉ lấy PNG đã ghi trên đĩa; phóng NEAREST, không vẽ lại hình.
    zoom, columns = 3, 7
    cw, ch = config['canvas'][0]*zoom, config['canvas'][1]*zoom+35
    sheet = Image.new('RGB', (cw*columns, ch*((len(cells)+columns-1)//columns)), (62, 66, 72))
    draw = ImageDraw.Draw(sheet)
    for n, (frame, ids, _) in enumerate(cells):
        x, y = (n % columns)*cw, (n // columns)*ch
        disk = Image.open(out / f'dbl_khung_{frame:02d}.png').convert('RGBA')
        disk = disk.resize((disk.width*zoom, disk.height*zoom), Image.Resampling.NEAREST)
        sheet.paste(disk, (x, y+35), disk)
        draw.text((x+10, y+10), f'{frame:02d} | head {ids[0]} / leg {ids[1]} / body {ids[2]}', fill='white')
    sheet.save(out / 'to_soat.png')
    return errors, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, default=BASE/'tam_goc')
    parser.add_argument('--source-commit', default='local')
    parser.add_argument('--server', required=True)
    parser.add_argument('--client', required=True)
    parser.add_argument('--audit-only', action='store_true')
    args = parser.parse_args()
    print('NGUỒN TẤM:', args.source_dir.resolve())
    print('COMMIT NGUỒN:', args.source_commit)
    audits = audit(args.source_dir)  # Mọi kiểm đếm phải xong trước khi ghi mảnh.
    ids = read_ids(args.server, args.client)
    print('CHỈ LẤY ID MẢNH; không dùng khung kích thước hay dx/dy tham khảo.')
    if args.audit_only:
        return
    cat, out = BASE/'cat', BASE/'ghep'
    cat.mkdir(exist_ok=True)
    out.mkdir(exist_ok=True)
    pieces, manifest = {}, []
    for name, image, labels, figures, mapping, path in audits:
        for cell, fig in enumerate(figures, 1):
            idx = mapping.get(cell)
            if idx is None or (name, cell) in DAMAGED:
                continue
            im = cropped(image, labels, fig)
            if idx in (6, 11):
                print(f'MẢNH dbl_{idx}:')
                im = collar_brown(im)
            im.save(cat/f'dbl_{idx}.png')
            pieces[idx] = im
            manifest.append({'id': idx, 'source': name+'.png', 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                             'bbox': fig['bbox'], 'size': list(im.size), 'collar_recolored': idx in (6, 11)})
    expected_parts = set(range(5,22)) | set(range(23,34)) | {35}
    missing = sorted(expected_parts - set(pieces))
    used = {n for row in ids.values() for n in row}
    required_missing = sorted(used - set(pieces))
    print('MẢNH THIẾU:', missing)
    print('MẢNH THIẾU CẦN CHO KHUNG:', required_missing)
    if required_missing:
        raise SystemExit('DỪNG: thiếu mảnh cần ghép; không thay thế hình khác')
    path = out/'dbl_vi_tri.json'
    if path.exists():
        config = json.loads(path.read_text())
        print('GIỮ VỊ TRÍ CHỈNH TAY:', path.relative_to(ROOT))
        config['source_figures'] = manifest
    else:
        config = placements(pieces, ids, manifest, args.source_commit)
    errors, stats = render(pieces, config, ids, out)
    config['measured_frames'] = stats
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2)+'\n')
    print('KHUNG LỖI:', errors)
    print('CHƯA XỬ LÝ: dbl_13 bị dấu sao đè; khung 08–11 không ghép theo yêu cầu.')
    print(f'ĐÃ XUẤT: {len(pieces)} mảnh; {len(ids)} khung; ghep/dbl_vi_tri.json; ghep/to_soat.png.')
    print('CHỜ NGƯỜI DÙNG DUYỆT BẰNG MẮT; không tự kết luận đạt.')


if __name__ == '__main__':
    main()
