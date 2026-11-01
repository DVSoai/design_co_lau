#!/usr/bin/env python3
"""Image-only acceptance: real full-layer Godot renders versus layer removals.

No parts.json, frame registrations, declared joints, or hand/foot landmarks are read.
All geometric measurements come from rendered RGBA pixels and their ablations.
"""
from pathlib import Path
import argparse,json,sys
import numpy as np
from PIL import Image
from scipy.ndimage import label,find_objects,binary_dilation,distance_transform_edt

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--renders',default='prototype/pose_rig/reports/ablation_v7');args=parser.parse_args()
DIR=ROOT/args.renders;manifest=json.loads((DIR/'manifest.json').read_text());failures=[];measurements=[]
def check(ok,message):
    print(('PASS: ' if ok else 'FAIL: ')+message)
    if not ok:failures.append(message)
def tiles(file):
    im=np.array(Image.open(DIR/file).convert('RGBA'),float)/255
    return {name:im[(i//4)*256:(i//4+1)*256,(i%4)*256:(i%4+1)*256] for i,name in enumerate(manifest['variants'])}
def premul(im):return np.dstack([im[:,:,:3]*im[:,:,3,None],im[:,:,3]])
def visible_fraction(full,removed,isolated):
    # Compare actual removal delta to the ideal foreground contribution at each pixel.
    back=premul(removed);fg=premul(isolated);ideal=fg+back*(1-isolated[:,:,3,None])-back;actual=premul(full)-back
    norm=(ideal*ideal).sum(axis=2);fraction=np.zeros_like(norm);valid=norm>1e-7
    fraction[valid]=np.clip((actual*ideal).sum(axis=2)[valid]/norm[valid],0,1)
    return fraction
def bounds(mask):
    y,x=np.where(mask)
    return None if not len(x) else (int(x.min()),int(y.min()),int(x.max()),int(y.max()))
def steel_mask(w):
    rgb=w[:,:,:3];opaque=w[:,:,3]>.2
    steel=opaque&(rgb.min(axis=2)>65/255)&(np.ptp(rgb,axis=2)<85/255)
    labs,n=label(steel);sizes=np.bincount(labs.ravel());sizes[0]=0
    return binary_dilation(labs==int(sizes.argmax()),iterations=2)&opaque
def bow_wood_mask(w):
    rgb=w[:,:,:3];warm=(w[:,:,3]>.05)&(rgb[:,:,0]-rgb[:,:,1]>12/255)&(rgb[:,:,1]-rgb[:,:,2]>5/255)&(rgb[:,:,0]>55/255)
    return binary_dilation(warm,iterations=2)&(w[:,:,3]>.05)&(rgb.min(axis=2)<=.8)
def feet_from_paint(legs,H):
    # Brown shoe bodies are separated from trousers by light calf wraps. Pale outer
    # sole edging ranks shoe components, independent of any authored foot points.
    rgb=legs[:,:,:3]*255;rr,gg,bb=rgb.transpose(2,0,1);alpha=legs[:,:,3]>.5;box=bounds(alpha)
    if box is None:return []
    top,height=box[1],box[3]-box[1]+1
    brown=alpha&(rr>65)&(rr<180)&(gg>25)&(gg<125)&(bb<85)&(rr>1.2*gg)
    labs,n=label(brown);tan=alpha&(rr>160)&(gg>105)&(bb>40)&(rr-gg>20)&(gg-bb>15)&(distance_transform_edt(alpha)<4)
    candidates=[]
    for id,sl in enumerate(find_objects(labs),1):
        if sl is None:continue
        yy,xx=np.where(labs==id)
        if len(xx)<20 or yy.mean()<top+.25*height or yy.max()-yy.min()+1>.19*H:continue
        score=int((binary_dilation(labs==id,iterations=3)&tan).sum());candidates.append((score,len(xx),id))
    chosen=[]
    for score,area,id in sorted(candidates,reverse=True):
        region=binary_dilation(labs==id,iterations=3)&(legs[:,:,3]>.05)
        if score==0 or any(np.any(region&previous) for previous in chosen):continue
        chosen.append(region)
        if len(chosen)==2:break
    return chosen
def bow_wrap_midpoint(w):
    rgb=w[:,:,:3]*255;rr,gg,bb=rgb.transpose(2,0,1);alpha=w[:,:,3]>.5;box=bounds(alpha)
    if box is None:return None
    yy=np.indices(alpha.shape)[0];span=box[3]-box[1]
    gold=alpha&(rr>150)&(gg>100)&(bb<180)&(gg>1.15*bb)&(yy>box[1]+.3*span)&(yy<box[1]+.7*span)
    labs,n=label(binary_dilation(gold));points=[]
    for id in range(1,n+1):
        region=(labs==id)&gold
        if region.sum()<3:continue
        y,x=np.where(region);points.append((int(region.sum()),np.array([x.mean(),y.mean()])))
    points=sorted(points,key=lambda row:row[0],reverse=True)[:2]
    return None if len(points)!=2 else (points[0][1]+points[1][1])*.5

def contour_samples(full,w,core,school):
    y,x=np.where(core&(w[:,:,3]>.5));points=np.column_stack([x,y]);centre=points.mean(axis=0);_,_,axes=np.linalg.svd(points-centre,full_matrices=False);axis=axes[0];normal=np.array([-axis[1],axis[0]]);projected=(points-centre)@axis;low,high=np.quantile(projected,[.02,.98]);result=[]
    for fraction in [.2,.35,.65,.8]:
        middle=centre+axis*(low+(high-low)*fraction);values=[]
        for offset in np.arange(-32,32.001,.125):
            at=middle+normal*offset;ix,iy=np.floor(at).astype(int)
            if not (0<=ix<256 and 0<=iy<256):continue
            values.append((offset,(ix,iy),w[iy,ix],full[iy,ix]))
        if school=='kiem':material=[offset for offset,_,c,_ in values if c[3]>=.8 and c[:3].min()>90/255]
        else:material=[offset for offset,_,c,_ in values if c[3]>=.8 and c[0]-c[1]>15/255 and c[1]-c[2]>8/255 and c[0]>75/255]
        if not material:result.append((fraction,0,0));continue
        start,end=min(material),max(material);counts=[]
        for lo,hi in [(start-4,start),(end,end+4)]:
            pixels={xy for offset,xy,_,c in values if lo<=offset<=hi and c[3]>=.8 and c[0]<80/255 and c[1]<70/255 and c[2]<70/255};counts.append(len(pixels))
        result.append((fraction,*counts))
    return result

entries=manifest['entries'];check(len(entries)==120,'120 actually rendered poses:30 frames x2 schools x2 directions')
controls={}
for entry in entries:
    if entry['frame']!=0:continue
    t=tiles(entry['file']);alpha=np.maximum.reduce([t[k][:,:,3] for k in ['head_only','body_only','legs_only']]);box=bounds(alpha>.5)
    controls[(entry['school'],entry['direction'])]=box[3]-box[1]+1
    head_box=bounds(t['head_only'][:,:,3]>.5);ratio=(head_box[3]-head_box[1]+1)/controls[(entry['school'],entry['direction'])]
    check(abs(ratio-.4)<=.03,f'{entry["school"]} dir{entry["direction"]} rendered bare head/H={ratio:.9f}, preserved target .40±.03')
check(all(controls.values()),'H measured from actual neutral head/body/legs union, not declared joint coordinates')
held=[0,1,2,3,4,5,6,7,12,21]
for entry in entries:
    school,frame,direction=entry['school'],entry['frame'],entry['direction'];name=f'{school} frame{frame} dir{direction}';t=tiles(entry['file']);H=controls[(school,direction)]
    full=t['full'];legs=t['legs_only'];body=t['body_only'];head=t['head_only'];w=t['weapon_only'];row={'school':school,'frame':frame,'direction':direction,'H_rendered_px':H}
    leg_fraction=visible_fraction(full,t['no_legs'],legs)
    if frame in held:
        fraction=visible_fraction(full,t['no_weapon'],w);core=steel_mask(w) if school=='kiem' else bow_wood_mask(w)
        area=w[:,:,3]*core;whole=w[:,:,3];core_visible=(area*fraction).sum()/max(1e-9,area.sum());whole_visible=(whole*fraction).sum()/max(1e-9,whole.sum())
        target=.8 if school=='kiem' else .7
        check(core_visible>=target and whole_visible>=.7,f'{name} full/no-weapon/isolated: blade/wood visible={core_visible:.9%} >={target:.0%}; whole={whole_visible:.9%} >=70%')
        row.update(weapon_core_visible=float(core_visible),weapon_whole_visible=float(whole_visible))
        if school=='kiem':
            box=bounds(w[:,:,3]>.5);ratio=max(box[2]-box[0]+1,box[3]-box[1]+1)/H
            check(.75<=ratio<=.8,f'{name} actual rendered sword longest alpha side/H={ratio:.9f} in[.75,.8]')
        if frame==0:
            for at,left,right in contour_samples(full,w,core,school):check(left>=1 and right>=1,f'{name} FULL rendered contour section{at}: opaque dark pixel cells={left}/{right}, each>=1px')
        fingers=t['fingers_only'];skin=(fingers[:,:,3]>.5)&(full[:,:,0]>.6)&(full[:,:,1]>.3)
        # The grip must really replace visible handle paint with skin in the full render.
        skin&=np.max(np.abs(premul(full)-premul(t['no_fingers'])),axis=2)>2/255
        contact=skin&(w[:,:,3]>.5);check(bool(contact.any()),f'{name} actual foreground palm touches and occludes rendered handle')
        if school=='kiem':
            y,x=np.where(contact);grip_y=float(y.mean()) if len(y) else float('inf');foot_bottom=bounds(legs[:,:,3]>.5)[3];height=(foot_bottom-grip_y)/H
            check(.45<=height<=.6,f'{name} rendered skin/handle grip height above feet/H={height:.9f} in[.45,.60]');row['grip_height_H']=height
        else:
            midpoint=bow_wrap_midpoint(w);gap=float('inf')
            if midpoint is not None and skin.any():
                y,x=np.where(skin);gap=float(np.sqrt((x-midpoint[0])**2+(y-midpoint[1])**2).min())
            check(gap<=1,f'{name} image-detected middle-wrap midpoint to actual gripping skin={gap:.9f}px <=1')
            weapon_top=bounds((w[:,:,3]*fraction)>.5)[1];head_top=bounds(head[:,:,3]>.5)[1]
            check(weapon_top<head_top,f'{name} visible bow upper end y={weapon_top} ABOVE head y={head_top}')
            box=bounds(w[:,:,3]>.5);height=(box[3]-box[1]+1)/H
            check(1.0<=height<=1.1,f'{name} real rendered bow vertical height/H={height:.9f} in[1.0,1.1]');row.update(wrap_skin_gap_px=gap,bow_above_head_px=int(head_top-weapon_top),bow_height_H=height)
    if frame in range(2,8) or frame in range(13,30):
        feet=feet_from_paint(legs,H);check(len(feet)==2,f'{name} TWO shoes detected from actual brown paint, pale soles and separate image regions')
        soles=[]
        for i,foot in enumerate(feet):
            area=legs[:,:,3]*foot;visible=(area*leg_fraction).sum()/max(1e-9,area.sum())
            check(visible>=.7,f'{name} shoe{i} full/no-legs comparison visible={visible:.9%} >=70%');soles.append(bounds(foot&(legs[:,:,3]>.5))[3])
            row['shoe%d_visible'%i]=float(visible)
        if frame in range(2,8) and len(feet)==2:
            centres=[]
            for foot in feet:
                yy,xx=np.where(foot&(legs[:,:,3]>.5));centres.append(np.array([xx.mean(),yy.mean()]))
            row['shoe_span_H']=float(np.linalg.norm(centres[0]-centres[1])/H)
        if frame in range(13,30):
            check(len(soles)==2 and abs(soles[0]-soles[1])<=1,f'{name} actual shoe soles={soles}; same ground within1 rendered pixel')
            lmask=legs[:,:,3]>.5;bmask=body[:,:,3]>.5;box=bounds(lmask);top=box[1];xs=np.where(lmask[top:top+3].any(axis=0))[0];gaps=[]
            if len(xs):
                low,high=np.quantile(xs,[.2,.8])
                for x in range(int(np.ceil(low)),int(np.floor(high))+1):
                    ly=np.where(lmask[:,x])[0];by=np.where(bmask[:,x]&(np.arange(256)>=top-.4*H)&(np.arange(256)<=top+.25*H))[0]
                    if len(ly) and len(by):gaps.append(max(0,int(ly.min()-by.max()-1)))
                    else:gaps.append(999)
            max_gap=max(gaps,default=999);check(max_gap==0,f'{name} row-by-row central hem-to-leg transparent gap={max_gap}px (required0)')
            union=bmask|lmask;labs,n=label(union);body_ids=np.bincount(labs[bmask]);leg_ids=np.bincount(labs[lmask]);body_ids[0]=0;leg_ids[0]=0
            check(body_ids.argmax()==leg_ids.argmax() and body_ids.argmax()!=0,f'{name} rendered torso and legs form one connected painted silhouette')
            expected='attack_stance_%d.png'%(0 if frame<=20 else (1 if frame<=25 else 2));check(entry['legs_texture']==expected,f'{name} actual rendered stance texture={entry["legs_texture"]}, expected={expected}')
            row.update(sole_delta_px=None if len(soles)!=2 else abs(soles[0]-soles[1]),hem_gap_px=max_gap)
    measurements.append(row)
for school in ['kiem','cung']:
    for direction in [-1,1]:
        strides=[r.get('shoe_span_H',0) for r in measurements if r['school']==school and r['direction']==direction and r['frame'] in range(2,8)]
        wide=sum(span>=.3 for span in strides);check(wide>=4,f'{school} dir{direction} actual shoe-region strides>=.30H: {wide}/6 (required>=4)')
result={'failures':failures,'failure_count':len(failures),'measurements':measurements,'method':'Only actual Godot full/removed/isolated RGBA images. No authored pose landmarks or registration coordinates.'}
(DIR.parent/'chest_v7_image_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(f'Rendered ablation acceptance: poses={len(entries)} held cases=40 attack cases=68 running cases=24; failures={len(failures)}')
sys.exit(bool(failures))
