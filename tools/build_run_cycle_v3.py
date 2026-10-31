#!/usr/bin/env python3
"""Update only frames2..7 from independently drawn running art; retain all other poses."""
from pathlib import Path
import copy,json,math
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects

R=Path(__file__).resolve().parents[1];D=R/'prototype/pose_rig/data'
ART=R/'prototype/pose_rig/art/lv1_30';OUT=R/'art/sprites/characters/lv1_30';SRC=OUT/'sources'

def clean(im):
    a=np.array(im.convert('RGBA'));r,g,b=a[:,:,:3].astype(int).transpose(2,0,1)
    a[(g>1.18*np.maximum(r,b))&(g>90)]=0;a[a[:,:,3]==0,:3]=0
    return Image.fromarray(a)

def components(im,count,rows):
    labels,n=label(np.array(im)[:,:,3]>0)
    sizes=np.bincount(labels.ravel());ids=np.argsort(sizes[1:])[-count:]+1
    parts=[]
    for id in ids:
        y,x=np.where(labels==id);box=(int(x.min()),int(y.min()),int(x.max())+1,int(y.max())+1)
        a=np.array(im);a[labels!=id]=0
        parts.append((box,Image.fromarray(a)))
    return sorted(parts,key=lambda it:(min(rows-1,int(((it[0][1]+it[0][3])/2)/im.height*rows)),it[0][0]))

def run():
    p=json.loads((D/'parts.json').read_text());f=json.loads((D/'frames30.json').read_text())
    original=copy.deepcopy(f);old_assets=copy.deepcopy(p['assets'])
    ref=json.loads((R/'docs/ref/so_lieu_tham_khao.json').read_text())
    H=p['presentation']['standing_height_source'];C=np.array([160.,150.])
    def save(id,im,anchors,source):
        im=clean(im);im.save(ART/(id+'.png'));im.save(OUT/(id+'.png'))
        p['assets'][id]={'file':id+'.png','size':list(im.size),'anchors':anchors,'source':source,'status':'drawn_unapproved'}
        (OUT/(id+'.prompt.txt')).write_text('Offline registration of original run artwork: '+json.dumps(source,ensure_ascii=False)+'\n')
    legs=clean(Image.open(SRC/'run_v3_legs.png'))
    for i,(box,full) in enumerate(components(legs,6,2)):
        cut=full.crop(box);a=np.array(cut);band=np.where(a[min(14,cut.height-1),:,3]>127)[0]
        hx=float((band.min()+band.max())/2);hy=22.;scale=65/(cut.height-hy)
        points=[]
        for side in [-1,1]:
            yy,xx=np.indices(a.shape[:2]);mask=(a[:,:,3]>127)&(yy>cut.height*.38)&((xx<hx-15) if side<0 else (xx>hx+15))
            ys,xs=np.where(mask);bottom=ys.max();xs=xs[ys>bottom-10]
            points.append([float(np.median(xs))*scale,float(bottom)*scale])
        size=(round(cut.width*scale),round(cut.height*scale))
        save('run_v3_legs_%d'%i,cut.resize(size,Image.Resampling.LANCZOS),{'hip':[hx*scale,hy*scale],'sole':[hx*scale,size[1]],'foot_left':points[0],'foot_right':points[1]}, {'sheet':'run_v3_legs','crop':list(box),'phase':i,'scale':scale})
    sword=clean(Image.open(SRC/'run_v3_sword_torsos.png'));bow=clean(Image.open(SRC/'run_v3_torsos.png'))
    sword_parts=components(sword,6,2);bow_parts=components(bow,12,4)[6:]
    # Measured source points: exposed neck cut, belt/hip center, held fist, free fist.
    sword_marks=[((332,138),(280,326),(80,356),(488,188)),((830,140),(775,326),(568,358),(988,267)),((1320,145),(1270,330),(1073,358),(1480,367)),((390,587),(350,779),(495,835),(58,635)),((885,590),(839,785),(978,837),(567,587)),((1320,585),(1270,780),(1075,805),(1460,802))]
    bow_marks=[((292,614),(238,766),(384,797),(400,659)),((720,615),(665,770),(790,798),(844,697)),((1150,615),(1100,768),(1208,803),(1273,770)),((300,904),(245,1061),(450,1095),(55,1020)),((720,904),(664,1060),(860,1092),(508,1023)),((1140,905),(1094,1066),(1270,1090),(944,1095))]
    def transform(im,marks):
        neck,hip,grip,free=map(lambda v:np.array(v,float),marks);v=neck-hip
        dx=50*math.sin(math.radians(12));dy=-50*math.cos(math.radians(12));sx=50/np.linalg.norm(v)
        A=np.array([[sx,(dx-sx*v[0])/v[1]],[0,dy/v[1]]]);inverse=np.linalg.inv(A);offset=hip-inverse@C
        result=im.transform((320,256),Image.Transform.AFFINE,tuple(inverse[0])+tuple([offset[0]])+tuple(inverse[1])+tuple([offset[1]]),Image.Resampling.BICUBIC)
        return result,{k:list(C+A@(point-hip)) for k,point in [('neck',neck),('hip',hip),('grip',grip),('near_hand',grip),('far_hand',free),('free_hand',free),('back',hip+[-30,-30])]},A
    # Reuse the newly drawn low rear weapon arm for the two back-swing poses.
    arm_mask=Image.new('L',sword.size)
    ImageDraw.Draw(arm_mask).polygon([(250,170),(195,148),(120,215),(74,289),(35,351),(45,400),(111,405),(145,340),(165,300),(221,260),(250,214)],fill=255)
    arm=np.array(sword_parts[0][1]);arm[np.array(arm_mask)==0]=0
    arm_image,arm_anchors,_=transform(Image.fromarray(arm),sword_marks[0])
    for school,items,marks_list in [('kiem',sword_parts,sword_marks),('cung',bow_parts,bow_marks)]:
        for i,((box,im),marks) in enumerate(zip(items,marks_list)):
            if school=='kiem' and i in [3,4]:
                erase=Image.new('L',im.size)
                poly=([(420,640),(475,685),(548,850),(490,895),(440,820),(403,705)] if i==3 else [(900,645),(950,700),(1030,795),(1025,895),(955,910),(905,810),(875,710)])
                ImageDraw.Draw(erase).polygon(poly,fill=255);a=np.array(im);a[np.array(erase)>0]=0;im=Image.fromarray(a)
            image,anchors,A=transform(im,marks)
            if school=='kiem' and i in [3,4]:
                image.alpha_composite(arm_image)
                for key in ['grip','near_hand']:anchors[key]=arm_anchors[key][:]
            # Shorten only the central coat tails, never a hand or forearm.
            ar=np.array(image);yy,xx=np.indices(ar.shape[:2]);coat=(yy>154)&(xx>115)&(xx<205)
            for key in ['grip','free_hand']:
                gx,gy=anchors[key];coat&=(xx-gx)**2+(yy-gy)**2>14**2
            tail=ar.copy();tail[~coat]=0;ar[coat]=0;image=Image.fromarray(ar)
            piece=Image.fromarray(tail).crop((0,154,320,256)).resize((320,41),Image.Resampling.LANCZOS)
            image.alpha_composite(piece,(0,154))
            # Locate fist registration on actual opaque skin, not on a knuckle crease.
            ar=np.array(image);r,g,b=ar[:,:,:3].astype(int).transpose(2,0,1)
            for key in ['grip','free_hand']:
                gx,gy=anchors[key];mask=(ar[:,:,3]>220)&(r>155)&(g>80)&(r-g>25)&((xx-gx)**2+(yy-gy)**2<8**2)
                ys,xs=np.where(mask)
                if not len(xs):raise RuntimeError('%s frame%d %s missing painted fist'%(school,i,key))
                at=np.argmin((xs-xs.mean())**2+(ys-ys.mean())**2);anchors[key]=[float(xs[at]),float(ys[at])]
            anchors['near_hand']=anchors['grip'][:];anchors['far_hand']=anchors['free_hand'][:]
            save('run_v3_%s_body_%d'%(school,i),image,anchors,{'sheet':'run_v3_sword_torsos' if school=='kiem' else 'run_v3_torsos','phase':i,'lean_offline_degrees':12,'short_coat_factor':.4,'held_arm_component':bool(school=='kiem' and i in [3,4])})
    # Carry the bow by the lower wooden limb when running; this keeps the bow ahead
    # and its lower tip above the feet without moving the fist away from the wood.
    bow_asset=copy.deepcopy(p['assets']['bow_hold']);im=Image.open(ART/bow_asset['file']);a=np.array(im)
    target=np.array(bow_asset['anchors']['grip'])*.25+np.array(bow_asset['anchors']['bottom'])*.75
    r,g,b=a[:,:,:3].astype(int).transpose(2,0,1);ys,xs=np.where((a[:,:,3]>220)&(r>65)&(r-g>10)&(g>b)&(b<120))
    j=np.argmin((xs-target[0])**2+(ys-target[1])**2);bow_asset['anchors']['grip']=[float(xs[j]),float(ys[j])]
    save('run_v3_bow',im,bow_asset['anchors'],{'own_asset':'bow_hold','carry_grip':'lower_wood_limb','angle_from_vertical':40})
    neutral=p['assets'][p['levels']['1']['legs'][0]]['anchors'];standing=(np.array(neutral['hip'])-neutral['sole'])*.5
    for i in range(6):
        row=f['frames'][i+2];row['layers']['legs']['asset']='run_v3_legs_%d'%i
        row['layers']['body'].update(asset='run_v3_kiem_body_%d'%i,cung_asset='run_v3_cung_body_%d'%i)
        row['held_hand']='grip';row['held_weapon_z']={'kiem':-1,'cung':3}
        row['layers']['weapon']['cung_asset']='run_v3_bow'
        for school in ['kiem','cung']:
            ids={'head':p['levels']['1']['head'][row['layers']['head']['image']],'legs':'run_v3_legs_%d'%i,'body':'run_v3_%s_body_%d'%(school,i),'weapon':p['levels']['1']['run_weapon'] if school=='kiem' else 'run_v3_bow'}
            anchor=lambda layer,key:np.array(p['assets'][ids[layer]]['anchors'][key])*.5
            src=row['reference']['than'];base=ref['bang_30_khung'][0]['than'];hip=standing+np.array([src[1]-base[1],base[2]-src[2]])*3
            positions={'legs':hip-anchor('legs','hip'),'body':hip-anchor('body','hip')}
            positions['head']=positions['body']+anchor('body','neck')-anchor('head','neck')
            positions['weapon']=positions['body']+anchor('body','grip')-anchor('weapon','grip')
            for layer,key in [('head','dau'),('body','than'),('legs','chan'),('weapon','vu_khi')]:
                raw=row['reference'][key];dx,dy=ref['do_lech_hinh_bo_mac_dinh'][school if layer=='weapon' else key][raw[0]]
                origin=np.array([raw[1]+dx,-raw[2]+dy])*3
                row['registrations'][school][layer]=list(positions[layer]-origin)
    assert all(row==original['frames'][i] for i,row in enumerate(f['frames']) if i not in range(2,8))
    assert all(p['assets'][id]==value for id,value in old_assets.items() if not id.startswith('run_v3_'))
    (D/'parts.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n');(D/'frames30.json').write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
    print('Run-only update: rows2..7, twelve authored 12deg torsos, six new legs; all other frame rows and existing assets preserved.')

if __name__=='__main__':run()
