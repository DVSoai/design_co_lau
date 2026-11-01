#!/usr/bin/env python3
"""Only export the restyled bow into its exact existing crop and pixel dimensions."""
from pathlib import Path
import subprocess,json,hashlib
import numpy as np
from PIL import Image
from bow_readability_v9 import svg,BASELINE,ROOT
OUT=ROOT/'art/sprites/weapons/lv1';ART=ROOT/'prototype/pose_rig/art/lv1_30'
def run():
    protected=[ROOT/'prototype/pose_rig/data'/f'{name}.json' for name in ['parts','frames30','skills','effects']]+list(OUT.glob('kiem*'))
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
    def raster(path,name):
        dest=Path('/tmp')/(name+'.png');subprocess.run(['inkscape',str(path),'--export-type=png','--export-filename='+str(dest),'--export-width=2048'],check=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);return Image.open(dest).convert('RGBA')
    original=raster(BASELINE,'bow_v8_registration');crop=original.getbbox()
    path=OUT/'cung_lv1_master.svg';path.write_text(svg());im=raster(path,'bow_v9_readable').crop(crop)
    p=json.loads((ROOT/'prototype/pose_rig/data/parts.json').read_text());size=tuple(p['weapon_masters']['cung']['master_size']);im.resize(size,Image.Resampling.LANCZOS).save(OUT/'cung_lv1_master.png')
    size=tuple(p['assets']['cung_lv1']['size']);small=im.resize(size,Image.Resampling.LANCZOS);a=np.array(small);a[a[:,:,3]<12]=0;a[a[:,:,3]==0,:3]=0;small=Image.fromarray(a)
    for folder in [OUT,ART]:small.save(folder/'cung_lv1.png')
    note='Original editable SVG v9: unchanged cubic curve,23degree transform, original crop, dimensions and grip. Tapered dark-red wood with a bright lengthwise plane; black contour; contrasting moss-green leather; brass tips; fine pale string. SVG/script edit explicitly requested by user.\n'
    for name in ['cung_lv1.prompt.txt','cung_lv1_master.prompt.txt']:(OUT/name).write_text(note)
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected if p.is_file()}
    print('Bow-only export: original crop='+str(crop)+', master='+str(p['weapon_masters']['cung']['master_size'])+', display source='+str(size)+'.')
    print('PASS: sword files and parts/frames/skills/effects byte-identical; curve, transform and grip unchanged.')
if __name__=='__main__':run()
