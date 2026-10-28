#!/usr/bin/env python3
"""Audit an actual sprite PNG against a 32-color GPL palette and a NEAREST ×4."""
import argparse
from collections import Counter
from pathlib import Path
from PIL import Image
import numpy as np

BG = (0,255,0)

def load_gpl(path):
    colors=[]
    for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
        parts=line.split()
        if len(parts)>=3 and all(x.isdigit() for x in parts[:3]):
            colors.append(tuple(map(int,parts[:3])))
    return colors

def palette_groups(path):
    groups={}
    for line in Path(path).read_text(encoding='utf-8-sig').splitlines():
        parts=line.split()
        if len(parts)>=4 and all(x.isdigit() for x in parts[:3]):
            groups[tuple(map(int,parts[:3]))]=parts[3]
    return groups

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--sprite',required=True)
    ap.add_argument('--palette',required=True)
    ap.add_argument('--x4',required=True)
    args=ap.parse_args()
    raw=Image.open(args.sprite).convert('RGBA')
    rgb=np.asarray(raw)[...,:3]
    alpha=np.asarray(raw)[...,3]
    mask=np.any(rgb != np.array(BG),axis=2)
    yy,xx=np.where(mask)
    if not len(xx):
        raise ValueError('Empty sprite')
    bbox=(int(xx.min()),int(yy.min()),int(xx.max())+1,int(yy.max())+1)
    height=bbox[3]-bbox[1]
    margin=raw.height-bbox[3]
    counts=Counter(tuple(map(int,p)) for p in rgb.reshape(-1,3))
    pal=set(load_gpl(args.palette))
    color_groups=palette_groups(args.palette)
    forbidden={"limestone","young_rice","ripe_rice","water","reed_red","highlight"}
    forbidden_count=sum(n for c,n in counts.items() if c!=BG and color_groups.get(c) in forbidden)
    outside=sum(v for c,v in counts.items() if c!=BG and c not in pal)
    semi=int(((alpha>0)&(alpha<255)).sum())
    nonopaque=int((alpha!=255).sum())
    # BG color exact for all background pixels: count any transparent pixels as invalid.
    bad_bg=nonopaque
    actual_x4=Image.open(args.x4).convert('RGB')
    expected_x4=raw.convert('RGB').resize((512,512),Image.Resampling.NEAREST)
    x4_equal=actual_x4.size==(512,512) and np.array_equal(np.asarray(actual_x4),np.asarray(expected_x4))
    print(f'sprite={args.sprite}')
    print(f'size={raw.width}x{raw.height}')
    print(f'bbox_exclusive={bbox}')
    print(f'character_height={height}')
    print(f'bottom_margin={margin}')
    print(f'palette_colors={len(pal)}')
    print(f'unique_colors_including_background={len(counts)}')
    print(f'outside_palette_pixels={outside}')
    print(f'nonopaque_pixels={nonopaque}')
    print(f'semitransparent_pixels={semi}')
    print(f'background_other_than_00FF00={bad_bg}')
    print(f'x4_nearest_exact_match={x4_equal}')
    print('group_pixel_counts:')
    group_counts=Counter()
    for color,count in counts.items():
        if color!=BG:group_counts[color_groups.get(color,'OUTSIDE_PALETTE')]+=count
    for name,count in sorted(group_counts.items()):print(f'  {name} {count}')
    print(f'forbidden_group_pixels={forbidden_count}')
    print('pixel_counts:')
    for c,count in sorted(counts.items()):
        print(f'  #{c[0]:02X}{c[1]:02X}{c[2]:02X} {count}')
    print(f'TOTAL={sum(counts.values())}')
    ok=(raw.size==(128,128) and height==96 and margin==8 and outside==0 and forbidden_count==0 and nonopaque==0 and sum(counts.values())==16384 and x4_equal)
    print(f'PASS={ok}')
    if not ok:
        raise SystemExit(1)

if __name__=='__main__':
    main()
