"""Join only actual Godot screenshots. No invented characters, labels or statistics."""
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
a=Image.open(R/'prototype/pose_rig/reports/scene_right.png').convert('RGB');b=Image.open(R/'prototype/pose_rig/reports/scene_left.png').convert('RGB')
assert a.size==b.size==(1600,720)
out=Image.new('RGB',(1600,1440));out.paste(a,(0,0));out.paste(b,(0,720));out.save(R/'docs/reports/g1_pose_sheets_compare.png')
print('Actual Godot screenshots: right1600x720 + left1600x720 -> g1_pose_sheets_compare.png1600x1440; no overpainting/imagegen')
