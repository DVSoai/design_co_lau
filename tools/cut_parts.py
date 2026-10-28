#!/usr/bin/env python3
"""One isotropic source-to-character scale. No facial pixel edits. No greybox size fitting."""
import json,math,hashlib,shutil
from pathlib import Path
import numpy as np
from PIL import Image
from snap_pixel import green_mask,nearest,load_groups
ROOT=Path(__file__).resolve().parents[1]
GROUPS=['outline','skin','fabric','belt','pants']
# Anatomical/overlap landmarks in each source crop, selected visually, never inferred as ground truth.
LANDMARKS={
 'head':{'pivot':[83,218],'crop_bottom':219,'chin_y':197,'face_box':[80,105,200,198]},
 'body':{'pivot':[65,230],'neck':[65,16],'shoulder':[68,45]},
 'upper_arm_near':{'pivot':[42,12],'end':[45,214]},'upper_arm_far':{'pivot':[41,12],'end':[43,214]},
 'forearm_near':{'pivot':[30,10],'end':[31,153]},'forearm_far':{'pivot':[29,10],'end':[30,150]},
 'hand_near':{'pivot':[26,9],'grip':[42,65]},'hand_far':{'pivot':[25,9],'grip':[41,65]},
 'thigh_near':{'pivot':[65,12],'end':[64,188]},'thigh_far':{'pivot':[64,12],'end':[63,188]},
 'shin_near':{'pivot':[36,12],'end':[35,164]},'shin_far':{'pivot':[35,12],'end':[34,164]},
 'foot_near':{'pivot':[44,19],'ground':105},'foot_far':{'pivot':[43,19],'ground':105},
 'dao':{'pivot':[31,290]},'bow':{'pivot':[14,184],'top':[75,3],'bottom':[78,354]}}

def components(mask):
    seen=np.zeros(mask.shape,bool); result=[]; h,w=mask.shape
    for y,x in zip(*np.where(mask)):
        if seen[y,x]:continue
        todo=[(int(x),int(y))];seen[y,x]=True;points=[]
        while todo:
            xx,yy=todo.pop();points.append((xx,yy))
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx,ny=xx+dx,yy+dy
                if 0<=nx<w and 0<=ny<h and mask[ny,nx] and not seen[ny,nx]:
                    seen[ny,nx]=True;todo.append((nx,ny))
        result.append(points)
    return result

def matrix(a,pal):
    chars='0123456789ABCDEFG';lookup={tuple(c):chars[i] for i,c in enumerate(pal)}
    return '\n'.join(''.join(lookup[tuple(px[:3])] if px[3] else '.' for px in row) for row in a)

def sample_uniform(rgb,mask,s):
    h,w=mask.shape;out=np.zeros((math.ceil(h*s),math.ceil(w*s),4),np.uint8)
    for y in range(out.shape[0]):
        for x in range(out.shape[1]):
            x0=int(x/s);x1=min(w,math.ceil((x+1)/s));y0=int(y/s);y1=min(h,math.ceil((y+1)/s));tile=mask[y0:y1,x0:x1]
            if tile.size and tile.mean()>=.35:
                out[y,x,:3]=np.median(rgb[y0:y1,x0:x1][tile],axis=0);out[y,x,3]=255
    return out

def main():
    work=ROOT/'art/concept/characters/chr_dbl_parts_work';manifest=json.loads((work/'manifest.json').read_text());source=ROOT/manifest['source']
    rgb=np.array(Image.open(source).convert('RGB'));groups=load_groups(ROOT/'art/reference/palette.gpl');pal=[c for name in GROUPS for c in groups[name]]
    definition=json.loads((ROOT/'prototype/rig/data/parts_greybox.json').read_text());parts={p['id']:p for p in definition['parts']}
    # Neutral assembly along its actual source pivots: head->neck->hip->knee->ankle->sole.
    measures=[218,230-16,188-12,164-12,105-19];height=sum(measures);s=96/height
    print(f'SOURCE neutral assembly: head={measures[0]}, torso={measures[1]}, legs={sum(measures[2:])}; H={height}px; guide=24/24/48; s=96/{height}={s:.12f} on BOTH axes')
    print('Scaled anatomical spans:',[round(v*s,4) for v in [measures[0],measures[1],sum(measures[2:])]],'; no independent per-part scale')
    out=ROOT/'art/sprites/characters/chr_dbl_parts';dest=ROOT/'prototype/rig/art_parts';raw=work/'uniform_raw';raw.mkdir(exist_ok=True)
    rows=[];fills={};pivot={id:np.array(l['pivot'],float)*s for id,l in LANDMARKS.items()}
    for item in manifest['parts']:
        id=item['id'];box=item['source_box'];x0,y0,x1,y1=box;crop=rgb[y0:y1,x0:x1];mask=~green_mask(crop)
        if id=='head':crop=crop[:LANDMARKS[id]['crop_bottom']];mask=mask[:len(crop)]
        a=sample_uniform(crop,mask,s)
        # Palette role: dark source lines become material shadows, not seam ink.
        # On the face preserve the source-derived nearest colours; no feature patches.
        for y,x in zip(*np.where(a[:,:,3]>0)):
            palette=pal[2:]
            if id=='head':
                sx=(x+.5)/s;sy=(y+.5)/s
                face=(135<=sx<=173 and 123<=sy<=154) or (144<=sx<=180 and 160<=sy<=197) or (sx>172 and 100<=sy<=180)
                palette=pal if face else (pal[13:] if sy<180 else pal[2:6])
            a[y,x,:3]=nearest(a[y,x,:3],palette)
        # Hands/feet retain dark/mid/light skin by a luminance quantile mapping, not aspect changes.
        if id.startswith(('hand_','foot_')):
            ys,xs=np.where(a[:,:,3]>0);lum=a[ys,xs,:3].astype(float)@np.array([.2126,.7152,.0722]);order=np.argsort(lum,kind='stable')
            for rank,k in enumerate(order):a[ys[k],xs[k],:3]=pal[[2,4,5][min(2,rank*3//len(order))]]
        for cluster in components(a[:,:,3]>0):
            if len(cluster)<2:
                for x,y in cluster:a[y,x]=0
        Image.fromarray(a).save(raw/f'{id}.png');Image.fromarray(a).save(out/f'{id}.png');shutil.copyfile(out/f'{id}.png',dest/f'{id}.png')
        p=parts[id];old={k:p[k] for k in ['size','pivot','attach']};p['size']=[a.shape[1],a.shape[0]];p['pivot']=pivot[id].tolist()
        if id=='body':attach=np.array([0,-sum(measures[2:])*s])
        elif id=='head':attach=(np.array(LANDMARKS['body']['neck'])-LANDMARKS['body']['pivot'])*s
        elif id.startswith('upper_arm_'):attach=(np.array(LANDMARKS['body']['shoulder'])-LANDMARKS['body']['pivot'])*s
        elif id.startswith('thigh_'):attach=np.array([-1.5 if id.endswith('far') else 1.5,0])
        elif id in ['dao','bow']:
            parent=p['parent'];attach=(np.array(LANDMARKS[parent]['grip'])-LANDMARKS[parent]['pivot'])*s
        else:
            parent=p['parent'];attach=(np.array(LANDMARKS[parent]['end'])-LANDMARKS[parent]['pivot'])*s
        p['attach']=attach.tolist()
        if id.startswith('foot_'):p['angle_limit']=[-75,75]
        p['occluded_fill']='Unoutlined automatic material at true joint; no greybox frame fitting'
        rows.append({'id':id,'source_crop':box,'common_scale':s,'old':old,'new':{k:p[k] for k in ['size','pivot','attach']}})
        if p['parent'] and not id.startswith('foot_') and id not in ['dao','bow']:
            # Small hidden material disk under the joint, with NO outline.
            radius=min(3.0 if id.startswith('hand_') else 4.0,p['size'][0]/2)
            px,py=p['pivot'];patch=a[max(0,int(py-radius-1)):min(len(a),math.ceil(py+radius+2)),max(0,int(px-radius-1)):min(a.shape[1],math.ceil(px+radius+2))]
            inside=patch[patch[:,:,3]>0,:3]
            if not len(inside):inside=a[a[:,:,3]>0,:3]
            colour=nearest(np.median(inside,axis=0),pal[2:6] if id=='head' else pal[2:])
            fills[id]={'radius':radius,'color':'#'+''.join(f'{v:02X}' for v in colour),'method':'automatic unoutlined joint material, not a drawn body outline'}
        print(f'{id}: source={crop.shape[1]}x{crop.shape[0]} -> {p["size"]}; pivot={np.round(p["pivot"],3).tolist()}; attach={np.round(p["attach"],3).tolist()}; SAME s')
    definition['status']='Đề xuất — common-scale art measurements, chưa duyệt';definition['common_scale']=s;definition['source_height']=height;definition['source_spans']=measures;definition['parts']=list(parts.values());definition['rotation_center']=[0,-sum(measures[2:])*s]
    bow=LANDMARKS['bow'];definition['bow_string']['top']=((np.array(bow['top'])-bow['pivot'])*s).tolist();definition['bow_string']['bottom']=((np.array(bow['bottom'])-bow['pivot'])*s).tolist();definition['bow_string']['hand_anchor']=((np.array(LANDMARKS['hand_near']['grip'])-LANDMARKS['hand_near']['pivot'])*s).tolist()
    (ROOT/'prototype/rig/data/parts.json').write_text(json.dumps(definition,ensure_ascii=False,indent=2)+'\n');(dest/'joint_fill.json').write_text(json.dumps(fills,indent=2)+'\n')
    measurements={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scale':s,'height_source':height,'source_spans':measures,'guide':[24,24,48],'scaled_spans':[measures[0]*s,measures[1]*s,sum(measures[2:])*s],'landmarks_manual':LANDMARKS,'parts':rows,'neck_below_chin_px':(219-197)*s,'face_width_px':(200-80)*s,'head_width_px':parts['head']['size'][0]}
    (work/'uniform_measurements.json').write_text(json.dumps(measurements,ensure_ascii=False,indent=2)+'\n')
    head=np.array(Image.open(raw/'head.png'));text=matrix(head,pal);(work/'head_uniform_unedited.txt').write_text(text+'\n');Image.fromarray(head).save(work/'head_uniform_unedited.png')
    print('HEAD UNEDITED after common-scale sampling; no feature edit file read:');print(text)
    print('Palette:',{c:'#'+''.join(f'{v:02X}' for v in col) for c,col in zip('0123456789ABCDEFG',pal)})
    print(f'Head neck below chin: {measurements["neck_below_chin_px"]:.3f}px; source face span / frame width={measurements["face_width_px"]/parts["head"]["size"][0]:.3f}')
if __name__=='__main__':main()
