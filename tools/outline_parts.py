"""Bake outlines ONLY on the evaluated standing silhouette; no joint-cut borders.
No eye/nose/mouth patches. Source-derived dark facial pixels are preserved and reported.
"""
from pathlib import Path
import json,math,shutil
import numpy as np
from PIL import Image
from render_parts_scene import layers
from snap_pixel import load_groups
ROOT=Path(__file__).resolve().parents[1]
def main():
    data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());frame=data['idle']['frames'][0]
    size=(128,128);origin=(64,120);owner=np.full((128,128),'',object);union=np.zeros((128,128),bool)
    for id,layer in layers(frame,size,origin):
        a=np.asarray(layer)[:,:,3]>0;owner[a]=id;union|=a
    padded=np.pad(union,1);inside=padded[:-2,1:-1]&padded[2:,1:-1]&padded[1:-1,:-2]&padded[1:-1,2:];edge=union&~inside
    definition=json.loads((ROOT/'prototype/rig/data/parts.json').read_text());parts={p['id']:p for p in definition['parts']}
    raw=ROOT/'art/concept/characters/chr_dbl_parts_work/uniform_raw';out=ROOT/'art/sprites/characters/chr_dbl_parts';dest=ROOT/'prototype/rig/art_parts';groups=load_groups(ROOT/'art/reference/palette.gpl');outline=groups['outline'][0]
    counts={}
    for item in frame['geometry']:
        if item['kind']!='sprite':continue
        id=item['id'];p=parts[id];a=np.array(Image.open(raw/f'{id}.png').convert('RGBA'));m=item['transform'];count=0
        if id=='head':
            Image.fromarray(a).save(out/f'{id}.png');shutil.copyfile(out/f'{id}.png',dest/f'{id}.png');continue
        # Exclude the cut planes around proximal and distal joints from border painting.
        joints=[p['pivot']]+[[p['pivot'][i]+c['attach'][i] for i in range(2)] for c in parts.values() if c['parent']==id]
        for y,x in zip(*np.where(a[:,:,3]>0)):
            wx=m[0]*(x+.5)+m[2]*(y+.5)+m[4]+origin[0];wy=m[1]*(x+.5)+m[3]*(y+.5)+m[5]+origin[1];gx=int(math.floor(wx));gy=int(math.floor(wy))
            near_cut=any(abs(y-j[1])<=1 and abs(x-j[0])<=max(2,p['size'][0]/3) for j in joints)
            if 0<=gx<128 and 0<=gy<128 and owner[gy,gx]==id and edge[gy,gx] and not near_cut:
                a[y,x,:3]=outline;count+=1
        # Only source pieces visible in the standing frame get outlines; hidden bow remains material.
        Image.fromarray(a).save(out/f'{id}.png');shutil.copyfile(out/f'{id}.png',dest/f'{id}.png');counts[id]=count
    # Remove ONLY newly painted outline if it becomes internal in either standing pose.
    # Source-derived dark eye/nose/mouth pixels are never changed by this pass.
    protected=groups['outline']
    cleared=0
    for iteration in range(4):
        edits={}
        for name in ['idle','standing_neutral']:
            f=data[name]['frames'][0];composite=Image.new('RGBA',size);owners=np.full((128,128),'',object)
            items={i['id']:i for i in f['geometry'] if i['kind']=='sprite'}
            for id,layer in layers(f,size,origin):
                owners[np.array(layer)[:,:,3]>0]=id;composite.alpha_composite(layer)
            image=np.array(composite);mask=image[:,:,3]>0;pad=np.pad(mask,1);interior=mask&pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:]
            ink=np.zeros(mask.shape,bool)
            for colour in protected:ink|=np.all(image[:,:,:3]==colour,axis=2)
            for y,x in zip(*np.where(interior&ink)):
                id=owners[y,x]
                if id not in items or id=='head':continue
                m=items[id]['transform'];a,b,c,d,tx,ty=m;det=a*d-b*c;wx=x+.5-origin[0]-tx;wy=y+.5-origin[1]-ty
                sx=int(math.floor((d*wx-c*wy)/det));sy=int(math.floor((-b*wx+a*wy)/det))
                original=np.array(Image.open(raw/f'{id}.png').convert('RGBA'));current=np.array(Image.open(out/f'{id}.png').convert('RGBA'))
                for yy in range(max(0,sy-1),min(len(original),sy+2)):
                    for xx in range(max(0,sx-1),min(original.shape[1],sx+2)):
                        if tuple(current[yy,xx,:3]) in protected and tuple(original[yy,xx,:3]) not in protected:
                            edits.setdefault(id,[]).append((xx,yy))
        if not edits:break
        for id,coords in edits.items():
            current=np.array(Image.open(out/f'{id}.png').convert('RGBA'));original=np.array(Image.open(raw/f'{id}.png').convert('RGBA'))
            for x,y in set(coords):current[y,x]=original[y,x];cleared+=1
            Image.fromarray(current).save(out/f'{id}.png');shutil.copyfile(out/f'{id}.png',dest/f'{id}.png')
    print('Removed generated internal-outline samples:',cleared)
    print('Standing silhouette outline pixels painted per source piece:',counts)
    print('Cut planes and joint overdraw remain unoutlined; facial feature edit lists not read.')
if __name__=='__main__':main()
