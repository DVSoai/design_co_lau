"""Verify actual scene geometry, occlusion and reflected contact sheets using PIL."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
root = Path(__file__).resolve().parents[1]
data = json.loads((root/'reports/evaluated_frames.json').read_text())
for name,clip in data.items():
    image = Image.open(root/'contact_sheets'/f'chr_dbl_anim_{name}.png')
    assert image.size == (160*len(clip['frames']),160),name
for name in ['shoot','shoot_left']:
    for index,frame in enumerate(data[name]['frames']):
        mask = Image.new('I',(160,160),0); draw = ImageDraw.Draw(mask)
        ids = {part['id']:i+1 for i,part in enumerate(frame['geometry'])}
        for part in sorted(frame['geometry'],key=lambda p:p['z']):
            points=[(x+80,y+126) for x,y in part['points']]
            if part.get('kind')=='line': draw.line(points,fill=ids[part['id']],width=1)
            else: draw.polygon(points,fill=ids[part['id']])
        counts={name:sum(mask.getpixel((x,y))==ids[name] for y in range(160) for x in range(160)) for name in ['upper_arm_far','forearm_far','hand_far']}
        assert all(count>=5 for count in counts.values()),(name,index,counts)
        print(f'PASS: {name} frame {index+1}: visible far-arm pixels {counts}')
for name in ['run','shoot']:
    for a,b in zip(data[name]['frames'],data[name+'_left']['frames']):
        by_id={p['id']:p for p in b['geometry']}
        for right in a['geometry']:
            left=by_id[right['id']]
            assert left['z']==right['z']
            for (x,y),(lx,ly) in zip(right['points'],left['points']):
                assert abs(x+lx)<0.001 and abs(y-ly)<0.001,(name,right['id'])
    print(f'PASS: {name}_left is evaluated scene mirror; identical layer order')
print('Contact-sheet checks: 0 failures')
