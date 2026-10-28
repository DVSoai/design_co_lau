"""Measure manually identified anatomical landmarks on the actual side-view reference.
Segmentation detects the silhouette; neck and hip landmarks are explicitly manual,
not claimed to be inferred automatically from clothing pixels.
"""
from pathlib import Path
import hashlib, json
from PIL import Image
root = Path(__file__).resolve().parents[2]
p = root / 'art/reference/ref_dinh_bo_linh.png'
im = Image.open(p).convert('RGB')
box = (610, 20, 780, 570)
points = [(x,y) for y in range(box[1],box[3]) for x in range(box[0],box[2])
          if not (lambda c: c[1] > 240 and c[0] < 20 and c[2] < 20)(im.getpixel((x,y)))]
top, bottom = min(y for x,y in points), max(y for x,y in points)+1
# Half-open ranges; chosen visually at neck and waist/hip of the side view.
neck, hip = 174, 299
height = bottom-top
result = {'image':str(p.relative_to(root)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
          'image_size':list(im.size), 'side_roi':list(box), 'silhouette_y':[top,bottom],
          'manual_neck_y':neck, 'manual_hip_y':hip, 'height_source_px':height,
          'segments':{name:{'source_px':b-a, 'at_96_px':round((b-a)*96/height,3)}
                      for name,a,b in [('head_hair',top,neck),('torso',neck,hip),('legs_feet',hip,bottom)]}}
text=json.dumps(result,ensure_ascii=False,indent=2)
(root/'prototype/rig/reports/reference_measurements.json').write_text(text+'\n')
print(text)
