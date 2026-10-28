"""Measure actual PNG palette/face colours and outline inside evaluated standing silhouette."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from render_parts_scene import layers
from snap_pixel import load_groups
ROOT=Path(__file__).resolve().parents[1]
def main():
    groups=load_groups(ROOT/'art/reference/palette.gpl');data=json.loads((ROOT/'prototype/rig/reports/evaluated_art_frames.json').read_text());results={};failure=0
    for name in ['idle','standing_neutral']:
        im=Image.new('RGBA',(128,128));owners=np.full((128,128),'',object)
        for id,layer in layers(data[name]['frames'][0],(128,128),(64,120)):
            owners[np.array(layer)[:,:,3]>0]=id;im.alpha_composite(layer)
        a=np.array(im);mask=a[:,:,3]>0;p=np.pad(mask,1);inner=mask&p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]
        dark=np.zeros(mask.shape,bool)
        # O is stroke; Claude explicitly uses H as hair fill, report it separately.
        dark=np.all(a[:,:,:3]==groups['outline'][0],axis=2)
        hair_fill=int((inner&np.all(a[:,:,:3]==groups['outline'][1],axis=2)).sum())
        print(name,'H hair-fill pixels inside silhouette:',hair_fill)
        coords=[]
        items={i['id']:i for i in data[name]['frames'][0]['geometry'] if i['kind']=='sprite'}
        for y,x in zip(*np.where(inner&dark)):
            id=str(owners[y,x]);point={'x':int(x),'y':int(y),'part':id}
            if id in items:
                aa,b,c,d,tx,ty=items[id]['transform'];det=aa*d-b*c;wx=x+.5-64-tx;wy=y+.5-120-ty
                point['texture_x']=int(np.floor((d*wx-c*wy)/det));point['texture_y']=int(np.floor((-b*wx+aa*wy)/det))
            coords.append(point)
        ys,xs=np.where(mask);h=int(ys.max()-ys.min()+1);results[name]={'height_px':h,'interior_outline_count':len(coords),'positions':coords,'opaque_pixels':int(mask.sum()),'interior_outline_percent':round(100*len(coords)/int(mask.sum()),4)}
        print(f'{name}: height={h}px; internal outline pixels={len(coords)}; positions={coords}')
        # Claude's supplied head intentionally uses outline colours as hair fill.
        # Report them, but only reject unintended interior ink outside immutable head.
        failure+=any(c['part']!='head' for c in coords)
        if name=='standing_neutral':failure+=h!=96
    head=np.array(Image.open(ROOT/'art/sprites/characters/chr_dbl_parts/head.png').convert('RGBA'));skin=np.zeros(head.shape[:2],bool)
    for colour in groups['skin']:skin|=np.all(head[:,:,:3]==colour,axis=2)&(head[:,:,3]>0)
    measured=json.loads((ROOT/'art/concept/characters/chr_dbl_parts_work/uniform_measurements.json').read_text());skin[int(measured['landmarks_manual']['head']['chin_y']*measured['scale'])+1:]=False
    ys,xs=np.where(skin);span=int(xs.max()-xs.min()+1);ratio=span/head.shape[1]
    print(f'Head face skin span={span}/{head.shape[1]}={ratio:.4f}; neck below chin={measured["neck_below_chin_px"]:.4f}px; Claude pixel matrix applied unchanged')
    results['face']={'width':span,'frame_width':head.shape[1],'ratio':ratio,'neck_below_chin':measured['neck_below_chin_px']};failure+=ratio<.4 or not 2<=measured['neck_below_chin_px']<=3
    for id in ['hand_near','hand_far','foot_near','foot_far']:
        a=np.array(Image.open(ROOT/f'art/sprites/characters/chr_dbl_parts/{id}.png').convert('RGBA'));counts={label:int(np.all(a[:,:,:3]==colour,axis=2).sum()) for label,colour in [('dark',groups['skin'][0]),('mid',groups['skin'][2]),('light',groups['skin'][3])]}
        print(f'{id}: skin counts {counts}');failure+=not all(counts.values());results[id]=counts
    results['failures']=int(failure);(ROOT/'prototype/rig/reports/uniform_art_checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    print('Uniform-art checks failures:',failure);raise SystemExit(1 if failure else 0)
if __name__=='__main__':main()
