"""Rasterize polygons exported by the evaluated Godot scene. No imagegen or pose reconstruction."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parent
source = json.loads((ROOT / 'reports/evaluated_frames.json').read_text())
for name, clip in source.items():
    width, height = 160, 160
    sheet = Image.new('RGB', (width * len(clip['frames']), height), '#202832')
    draw = ImageDraw.Draw(sheet)
    for index, frame in enumerate(clip['frames']):
        origin = (index * width + 80, 126)
        draw.line((index * width, origin[1], (index+1)*width-1, origin[1]), fill='#62707D')
        for part in sorted(frame['geometry'], key=lambda part: part['z']):
            points = [(x+origin[0], y+origin[1]) for x,y in part['points']]
            if part.get('kind') == 'line':
                draw.line(points, fill='#'+part['color'][:6], width=max(1, round(part['width'])))
            else:
                draw.polygon(points, fill='#'+part['color'][:6])
        draw.text((index*width+4, 4), f"{name} #{index+1}", fill='white')
        draw.text((index*width+4, 145), f"t={frame['time']:.3f}s", fill='white')
    target = ROOT / 'contact_sheets' / f'chr_dbl_anim_{name}.png'
    sheet.save(target)
    print(f'{target.relative_to(ROOT)}: {sheet.width}x{sheet.height}, {len(clip["frames"])} frames')
