#!/usr/bin/env python3
"""Dựng lại nhân vật/vũ khí/đòn đánh của game tham khảo từ zip nguồn NẰM NGOÀI repo.

Chỉ để đối chiếu cơ chế và tỉ lệ. Ảnh xuất ra thư mục tạm (mặc định /tmp/ref_render),
TUYỆT ĐỐI không commit ảnh/dữ liệu của game tham khảo vào repo.

Cách dùng:
  python3 tools/ref_render.py --server <thư mục giải nén zip server> --client <thư mục giải nén zip client> [--out /tmp/ref_render] [--zoom 4]
  (server chứa .../res/icon/1..4, .../res/cache/data/nj_part|nj_effect|nj_skill, nja.sql;
   client chứa .../src/Char.java)
"""
import argparse, json, os, re, struct
from pathlib import Path
from PIL import Image, ImageDraw

def find(root, name):
    for p in Path(root).rglob(name):
        return p
    raise SystemExit(f'không tìm thấy {name} trong {root}')

class R:
    def __init__(s, b): s.b, s.i = b, 0
    def u8(s): v = s.b[s.i]; s.i += 1; return v
    def s8(s): v = struct.unpack_from('>b', s.b, s.i)[0]; s.i += 1; return v
    def s16(s): v = struct.unpack_from('>h', s.b, s.i)[0]; s.i += 2; return v

def load_parts(p):
    r = R(p.read_bytes()); out = []
    for _ in range(r.s16()):
        t = r.s8(); n = {0: 8, 1: 18, 2: 10, 3: 2}[t]
        out.append((t, [(r.s16(), r.s8(), r.s8()) for _ in range(n)]))
    return out

def load_effects(p):
    r = R(p.read_bytes()); out = {}
    for _ in range(r.s16()):
        eid = r.s16(); out[eid] = [(r.s16(), r.s8(), r.s8()) for _ in range(r.s8())]
    return out

def load_skills(p):
    r = R(p.read_bytes()); out = {}
    for _ in range(r.s16()):
        idx = r.s16(); r.s16(); r.s8(); d = {}
        for k in ('ground', 'air'):
            d[k] = [[r.s8()] + [r.s16() for _ in range(12)] for _ in range(r.s8())]
        out[idx] = d
    return out

def load_frames(java):
    s = java.read_text(encoding='utf-8', errors='ignore')
    i = s.index('{', s.index('Class127 = new int[][][]')); depth = 0
    for j in range(i, len(s)):
        depth += {'{': 1, '}': -1}.get(s[j], 0)
        if depth == 0: break
    t = re.sub(r'new int\[3\]', '{0,0,0}', s[i:j + 1])
    return json.loads(t.replace('{', '[').replace('}', ']'))  # 30 khung × [đầu, chân, thân, vũ khí] {hình, dx, dy}

def load_skill_classes(sql):
    s = sql.read_text(encoding='utf-8', errors='ignore')
    seg = s[s.index('CREATE TABLE `skill`'):]
    seg = seg[:seg.index('CREATE TABLE', 30)]
    return {int(a): (int(c), n) for a, c, n in re.findall(r"\(\s*(\d+),\s*(\d+),\s*'([^']*)'", seg)}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--server', required=True); ap.add_argument('--client', required=True)
    ap.add_argument('--out', default='/tmp/ref_render'); ap.add_argument('--zoom', type=int, default=4)
    a = ap.parse_args(); Z = a.zoom; out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    data = find(a.server, 'nj_part').parent; icon = find(a.server, 'icon') / str(Z)
    parts = load_parts(data / 'nj_part'); efs = load_effects(data / 'nj_effect'); sks = load_skills(data / 'nj_skill')
    T = load_frames(find(a.client, 'Char.java')); cls = load_skill_classes(find(a.server, 'nja.sql'))
    HEAD, LEG, BODY = parts[2][1], parts[0][1], parts[1][1]
    WEAPON = {'kiem': parts[12][1], 'cung': parts[14][1]}   # phần vũ khí loại 3: 12 = kiếm, 14 = cung
    cache = {}
    def img(i):
        if i <= 0: return None
        if i not in cache:
            p = icon / f'{i}.png'; cache[i] = Image.open(p).convert('RGBA') if p.exists() else None
        return cache[i]
    def char(cv, f, cx, cy, weapon=None):
        layers = [(1, LEG), (2, BODY), (0, HEAD)] + ([(3, weapon)] if weapon else [])
        for li, part in layers:
            e = T[f][li]
            if not e or e[0] >= len(part): continue
            idx, dx, dy = e; iid, pdx, pdy = part[idx]; g = img(iid)
            if g: cv.alpha_composite(g, (cx + (dx + pdx) * Z, cy + (-dy + pdy) * Z))   # neo góc trên-trái, quay phải
    def sheet(cells, labels, name):
        w, h = cells[0].size; o = Image.new('RGB', (w * len(cells), h + 24), (40, 44, 52)); d = ImageDraw.Draw(o)
        for k, c in enumerate(cells): o.paste(c, (k * w, 0), c); d.text((k * w + 6, h + 6), labels[k], fill=(255, 255, 0))
        o.save(out / name); print('đã xuất', out / name, o.size)
    W, H = 70 * Z, 62 * Z; CX, CY = 25 * Z, 54 * Z
    # 1. 30 khung (không vũ khí) + tư thế cầm kiếm/cung lúc đứng, chạy, nhảy
    cells = []
    for f in range(30):
        cv = Image.new('RGBA', (W, H)); char(cv, f, CX, CY); cells.append(cv)
    sheet(cells, [f'{f:02d}' for f in range(30)], 'ref_30_khung.png')
    for school, wp in WEAPON.items():
        fs = [f for f in range(30) if T[f][3]]
        cells = []
        for f in fs:
            cv = Image.new('RGBA', (W, H)); char(cv, f, CX, CY, wp); cells.append(cv)
        sheet(cells, [f'{f:02d}' for f in fs], f'ref_cam_{school}.png')
    # 2. Đòn cơ bản: kiếm = lớp 1, cung = lớp 4 (bảng skill trong nja.sql, cột class)
    def attack(sid, name):
        s = sks[sid]['ground']; active = []; cells = []; labels = []
        for t in range(len(s) + 2):
            cv = Image.new('RGBA', (110 * Z, 70 * Z)); cx, cy = 30 * Z, 58 * Z
            fr = s[min(t, len(s) - 1)]
            if t < len(s):
                for k in (1, 4, 7):
                    if fr[k] in efs: active.append((fr[k], t, fr[k + 1], fr[k + 2]))
            char(cv, fr[0], cx, cy)
            for eid, t0, edx, edy in active:   # hiệu ứng: neo TÂM ảnh (anchor 3)
                j = t - t0; fl = efs[eid]
                if 0 <= j < len(fl):
                    iid, fdx, fdy = fl[j]; g = img(iid)
                    if g: cv.alpha_composite(g, (cx + (edx + fdx) * Z - g.width // 2, cy + (edy + fdy) * Z - g.height // 2))
            cells.append(cv); labels.append(f'nhịp {t + 1} khung {fr[0]}')
        sheet(cells, labels, name)
        print(name, 'nhịp:', [(f[0], f[1], f[4], f[7]) for f in s], '(khung thân, hiệu ứng 1..3)')
    for name, c in (('kiem', 1), ('cung', 4)):
        ids = sorted(i for i, (k, _) in cls.items() if k == c)
        print(f'lớp {c} ({name}) các chiêu:', [(i, cls[i][1]) for i in ids])
        attack(ids[0], f'ref_don_{name}.png')
    # 3. Số đo tỉ lệ
    def bbox_char(f):
        cv = Image.new('RGBA', (400, 400)); char(cv, f, 150, 300); return cv.getbbox()
    b = bbox_char(0); h = b[3] - b[1]; hd = img(HEAD[0][0]).getbbox()
    print(f'nhân vật khung 00: cao {h} px ở zoom {Z} ({h // Z} px gốc); đầu kèm tóc {hd[3] - hd[1]} px = {(hd[3] - hd[1]) / h:.2f} H')
    for school, wp in WEAPON.items():
        g = img(wp[1][0]); bb = g.getbbox(); print(f'{school} cầm tay: {bb[2] - bb[0]}×{bb[3] - bb[1]} px = dài {max(bb[2] - bb[0], bb[3] - bb[1]) / h:.2f} H')

if __name__ == '__main__':
    main()
