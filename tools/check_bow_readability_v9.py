#!/usr/bin/env python3
"""Measure real H128 bow thickness and luminance contrast on viewer-background renders.

The background and complete character are independently rendered by Godot. No
SVG widths, authored endpoints, JSON anchors or declared grip points prove a pass.
"""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image
from scipy.ndimage import binary_erosion,map_coordinates
ROOT=Path(__file__).resolve().parents[1]
def premul(im):return np.dstack([im[:,:,:3]*im[:,:,3,None],im[:,:,3]])
def fraction(full,removed,isolated):
    back=premul(removed);fg=premul(isolated);ideal=fg+back*(1-isolated[:,:,3,None])-back;actual=premul(full)-back
    norm=(ideal*ideal).sum(2);out=np.zeros_like(norm);valid=norm>1e-7;out[valid]=np.clip((actual*ideal).sum(2)[valid]/norm[valid],0,1);return out

def luminance(rgb):
    linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
    return linear@np.array([.2126,.7152,.0722])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--renders',default='prototype/pose_rig/reports/ablation_v9');ap.add_argument('--out',default='prototype/pose_rig/reports/bow_v9_readability_results.json');args=ap.parse_args()
    folder=ROOT/args.renders;manifest=json.loads((folder/'manifest.json').read_text());failures=[];rows=[]
    def check(ok,msg):
        print(('PASS: ' if ok else 'FAIL: ')+msg)
        if not ok:failures.append(msg)
    def tiles(file):
        im=np.array(Image.open(folder/file).convert('RGBA'),float)/255
        return {name:im[(i//4)*256:(i//4+1)*256,(i%4)*256:(i%4+1)*256] for i,name in enumerate(manifest['variants'])}
    viewer=np.array(Image.open(ROOT/'prototype/pose_rig/reports/lv1_cung_frames_right.png').convert('RGB'))[0,0]
    cases=[e for e in manifest['entries'] if e['school']=='cung' and e['frame'] in [0,1,2,3,4,5,6,7,12,21]]
    check(len(cases)==20,'20 held bow poses, ten frames x two directions')
    for entry in cases:
        t=tiles(entry['file']);name=f'cung frame{entry["frame"]} dir{entry["direction"]}';w=t['weapon_only'];full=t['viewer_full'];empty=t['viewer_empty']
        check(np.all(np.rint(empty[:,:,:3]*255).astype(int)==viewer),name+' actual rendered empty background equals viewer screenshot corner '+str(viewer.tolist()))
        check(np.all(full[:,:,3]==1),name+' character really rendered over opaque viewer background')
        exposed=fraction(t['full'],t['no_weapon'],w)
        rr,gg,bb=w[:,:,:3].transpose(2,0,1);opaque=w[:,:,3]>.95
        red=opaque&(rr>100/255)&(rr>1.35*gg)&(gg>1.05*bb)
        green=(w[:,:,3]>.5)&(gg>1.12*rr)&(gg>1.15*bb)&(gg>65/255)
        gy,gx=np.where(green);check(len(gx)>3,name+' contrasting middle wrap detected from rendered green paint')
        if len(gx)<=3:continue
        centre=np.array([gx.mean(),gy.mean()]);y,x=np.where(red);points=np.c_[x,y].astype(float);widths=[];sample_points=[]
        # Each midpoint sample is on wood just beyond a wrap end, not on a declared joint.
        for side in [-1,1]:
            target_y=(gy.min()-4) if side<0 else (gy.max()+4)
            candidates=points[np.abs(points[:,1]-target_y)<=1]
            if not len(candidates):check(False,name+' no midpoint wood section on side'+str(side));continue
            point=candidates.mean(0);near=points[np.linalg.norm(points-point,axis=1)<=5]
            _,_,axes=np.linalg.svd(near-near.mean(0),full_matrices=False);tangent=axes[0];normal=np.array([-tangent[1],tangent[0]])
            offsets=np.arange(-10,10.001,.125);positions=point+offsets[:,None]*normal
            coords=np.array([positions[:,1],positions[:,0]])
            coverage=map_coordinates(w[:,:,3],coords,order=1,mode='constant',cval=0)
            visible=map_coordinates(exposed,coords,order=1,mode='constant',cval=0)
            # Integrate real rendered alpha across the normal. Bilinear subpixel
            # sampling avoids inflating a diagonal stroke by counting pixel cells.
            width=float((coverage*(visible>=.8)).sum()*.125);widths.append(width);sample_points.append(point.tolist())
            check(width>=4,f'{name} actual visible wood+outline midpoint side{side} thickness={width:.3f}px >=4')
        # Exclude black contour/antialias fringe by eroding the color region ONE pixel.
        # Test the MINIMUM contrast of all remaining exposed solid wood near the grip.
        yy,xx=np.indices(red.shape);near_middle=(xx-centre[0])**2+(yy-centre[1])**2<=(.24*128)**2
        core=binary_erosion(red)&near_middle&(exposed>=.95)
        check(core.sum()>=5,name+' real exposed interior wood sample count='+str(int(core.sum())))
        if not core.any():continue
        a=luminance(full[:,:,:3][core]);b=luminance(empty[:,:,:3][core]);contrasts=(np.maximum(a,b)+.05)/(np.minimum(a,b)+.05)
        minimum=float(contrasts.min());median=float(np.median(contrasts))
        check(minimum>=3,f'{name} full rendered solid wood / real viewer background MIN luminance contrast={minimum:.6f}:1 >=3:1; median={median:.6f}')
        rows.append({'frame':entry['frame'],'direction':entry['direction'],'thickness_px':widths,'sample_points_from_paint':sample_points,'solid_wood_samples':int(core.sum()),'contrast_min':minimum,'contrast_median':median,'viewer_background_rgb':viewer.tolist()})
    result={'failures':failures,'failure_count':len(failures),'measurements':rows,'method':'Real Godot viewer_full/viewer_empty + independent layer removals; minimum luminance contrast of exposed interior wood, excluding black contour and one-pixel antialias fringe.'}
    (ROOT/args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(f'Bow readability: held poses={len(rows)}, failures={len(failures)}');return bool(failures)
if __name__=='__main__':raise SystemExit(main())
