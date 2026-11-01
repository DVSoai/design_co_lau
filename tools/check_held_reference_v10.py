#!/usr/bin/env python3
"""Image-only held-grip displacement and hand contact from actual Godot RGBA."""
from pathlib import Path
import argparse,json
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
ROOT=Path(__file__).resolve().parents[1];HELD=[0,1,2,3,4,5,6,7,12,21]
def midpoint(w,school):
    r,g,b=w[:,:,:3].astype(float).transpose(2,0,1);a=w[:,:,3]>127
    if school=='kiem':
        mask=a&(r>=70)&(r<160)&(g>=35)&(g<115)&(r-g>20)&(g-b>10);y,x=np.where(mask)
        return np.array([x.mean(),y.mean()]) if len(x) else None
    y,x=np.where(a);yy=np.indices(a.shape)[0];span=y.max()-y.min();gold=a&(r>150)&(g>130)&(b<150)&(g>1.6*b)&(yy>y.min()+.15*span)&(yy<y.min()+.85*span)
    labs,n=label(binary_dilation(gold));points=[]
    for i in range(1,n+1):
        y,x=np.where((labs==i)&gold)
        if len(x)>=3:points.append((len(x),np.array([x.mean(),y.mean()])))
    points=sorted(points,key=lambda q:q[0],reverse=True)[:2]
    return (points[0][1]+points[1][1])*.5 if len(points)==2 else None
def alpha_centre(w):
    # Unchanged texture + translation only: whole-image alpha first moments move
    # exactly as the grip, without thresholding a tiny patterned leather region.
    alpha=w[:,:,3].astype(float);yy,xx=np.indices(alpha.shape);return np.array([(xx*alpha).sum(),(yy*alpha).sum()])/alpha.sum()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--renders',default='prototype/pose_rig/reports/ablation_v10');args=ap.parse_args();folder=ROOT/args.renders;m=json.loads((folder/'manifest.json').read_text());ref=json.loads((ROOT/'docs/ref/so_lieu_tham_khao.json').read_text())['bang_30_khung'];failures=[];rows=[]
    def check(ok,msg):
        print(('PASS: ' if ok else 'FAIL: ')+msg)
        if not ok:failures.append(msg)
    def tiles(file):
        im=np.array(Image.open(folder/file).convert('RGBA'));return {name:im[(i//4)*256:(i//4+1)*256,(i%4)*256:(i%4+1)*256] for i,name in enumerate(m['variants'])}
    controls={}
    for e in m['entries']:
        if e['frame']==0:controls[(e['school'],e['direction'])]=alpha_centre(tiles(e['file'])['weapon_only'])
    for e in m['entries']:
        if e['frame'] not in HELD:continue
        t=tiles(e['file']);school,frame,d=e['school'],e['frame'],e['direction'];name=f'{school} frame{frame} dir{d}';grip=midpoint(t['weapon_only'],school);origin=controls[(school,d)]
        check(grip is not None and origin is not None,name+' actual painted middle grip detected')
        if grip is None or origin is None:continue
        expected=np.array([d*(ref[frame]['vu_khi'][1]-ref[0]['vu_khi'][1]),-(ref[frame]['vu_khi'][2]-ref[0]['vu_khi'][2])])*512/131;actual=alpha_centre(t['weapon_only'])-origin;error=float(np.abs(actual-expected).max())
        check(error<=1,f'{name} real unchanged-texture alpha-moment / grip translation={actual.tolist()} expected={expected.tolist()} max-axis error={error:.6f}px <=1px raster sampling')
        if frame in range(2,7):check(-actual[0]*d>=10 and -actual[1]>=6,f'{name} ACTUAL retreat={-actual[0]*d:.6f}px>=10; rise={-actual[1]:.6f}px>=6')
        fingers=t['fingers_only'];r,g,b=fingers[:,:,:3].transpose(2,0,1);tan=(fingers[:,:,3]>127)&(r>=200)&(g>=100)&(b>=45);y,x=np.where(tan);palm=np.array([x.mean(),y.mean()]) if len(x) else None
        gap=float(np.linalg.norm(grip-palm)) if palm is not None else float('inf');check(gap<=1,f'{name} actual grip/palm CENTROID distance={gap:.6f}px <=1')
        # Verify the rendered hand really contributes to the complete layered image.
        delta=np.abs(t['full'].astype(int)-t['no_fingers'].astype(int)).max(2);check(bool(np.any((delta>2)&tan)),name+' foreground fingers replace grip pixels in actual full/no-fingers comparison')
        rows.append({'school':school,'frame':frame,'direction':d,'actual_delta_px':actual.tolist(),'reference_delta_px':expected.tolist(),'max_axis_error_px':error,'palm_gap_px':gap})
    (folder.parent/'held_v10_placement_image_results.json').write_text(json.dumps({'measurements':rows,'failures':failures,'failure_count':len(failures)},ensure_ascii=False,indent=2)+'\n');print(f'Reference-delta image acceptance: cases={len(rows)}, failures={len(failures)}');return bool(failures)
if __name__=='__main__':raise SystemExit(main())
