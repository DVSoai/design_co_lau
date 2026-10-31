#!/usr/bin/env python3
"""Register independently redrawn run/air poses and centered slash artwork.

Only our authored PNGs are read here. Numeric source rows remain in frames30.json.
"""
from pathlib import Path
import math, json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, find_objects

R=Path(__file__).resolve().parents[1]
ART=R/'prototype/pose_rig/art/lv1_30'
OUT=R/'art/sprites/characters/lv1_30'
SRC=OUT/'sources'

def keyed(path):
    ar=np.array(Image.open(path).convert('RGBA'))
    r,g,b=ar[:,:,:3].astype(int).transpose(2,0,1)
    ar[(g>1.18*np.maximum(r,b))&(g>90)]=0
    return Image.fromarray(ar)

def refresh(p,f,ref):
    assets=p['assets']
    def save(id,im,anchors,source):
        # Resampling can reintroduce a few matte-colored edge pixels; remove those
        # after the final transform as well as before it, preserving blue skill art.
        ar=np.array(im);red,green,blue=ar[:,:,:3].astype(int).transpose(2,0,1)
        ar[(green>1.18*np.maximum(red,blue))&(green>90)]=0
        ar[ar[:,:,3]==0,:3]=0
        im=Image.fromarray(ar)
        im.save(ART/(id+'.png'));im.save(OUT/(id+'.png'))
        assets[id]={'file':id+'.png','size':list(im.size),'anchors':anchors,'source':source,'status':'drawn_unapproved'}
        (OUT/(id+'.prompt.txt')).write_text('Offline crop/registration of independently drawn source: '+json.dumps(source,ensure_ascii=False)+'\n')
    # Six connected silhouettes, not fixed grid cuts (extended toes cross cell boundaries).
    run=keyed(SRC/'run_strides_v1.png');labels,n=label(np.array(run)[:,:,3]>0)
    objects=find_objects(labels)
    pieces=sorted([(int((labels[s]==i+1).sum()),s) for i,s in enumerate(objects) if s],reverse=True,key=lambda x:x[0])[:6]
    pieces=sorted(pieces,key=lambda v:(int((v[1][0].start+v[1][0].stop)/2>run.height/2),v[1][1].start))
    for i,(_,slices) in enumerate(pieces):
        y,x=slices;box=(x.start,y.start,x.stop,y.stop);im=run.crop(box)
        # Waist center is measured from the top belt, not silhouette center of a wide stride.
        ar=np.array(im);belt=np.where(ar[min(12,im.height-1),:,3]>127)[0]
        hx=float((belt.min()+belt.max())/2);hy=19.0
        scale=65/(im.height-hy)
        feet=[]
        for side in [-1,1]:
            yy,xx=np.indices(ar.shape[:2]);mask=(ar[:,:,3]>127)&(yy>im.height*.45)&((xx<hx-15) if side<0 else (xx>hx+15))
            ys,xs=np.where(mask);bottom=ys.max();xs=xs[ys>bottom-9]
            feet.append([float(np.median(xs))*scale,float(bottom)*scale])
        size=(round(im.width*scale),round(im.height*scale))
        save('run_leg_%d'%i,im.resize(size,Image.Resampling.LANCZOS),{'hip':[hx*scale,hy*scale],'sole':[hx*scale,size[1]],'foot_left':feet[0],'foot_right':feet[1]}, {'sheet':'run_strides_v1','crop':list(box),'phase':i,'scale':scale})
    # Upright torso with a closed low fist; reuse the authored neutral torso without bending it.
    p['assets']['body_0']['anchors'].update(grip=[96,77],near_hand=[96,77])
    bow_body=keyed(SRC/'bow_low_torso_v1.png');box=bow_body.getbbox();bow_body=bow_body.crop(box)
    scale=50/(566-155)
    anchors={key:[(value[0]-box[0])*scale,(value[1]-box[1])*scale] for key,value in {'neck':(590,155),'hip':(570,566),'grip':(1330,595),'near_hand':(1330,595),'far_hand':(218,715),'back':(390,330)}.items()}
    resized=bow_body.resize((round(bow_body.width*scale),round(bow_body.height*scale)),Image.Resampling.LANCZOS)
    # Select the nearest painted palm pixel to its measured center, avoiding knuckle linework.
    ar=np.array(resized);gx,gy=anchors['grip'];yy,xx=np.indices(ar.shape[:2]);rr,gg,bb=ar[:,:,:3].astype(int).transpose(2,0,1)
    mask=(ar[:,:,3]>220)&(rr>155)&(gg>80)&(rr-gg>25)&((xx-gx)**2+(yy-gy)**2<64)
    ys,xs=np.where(mask);j=np.argmin((xs-xs.mean())**2+(ys-ys.mean())**2)
    for key in ['grip','near_hand']:anchors[key]=[float(xs[j]),float(ys[j])]
    save('body_hold_cung',resized,anchors,{'sheet':'bow_low_torso_v1','crop':list(box),'scale':scale})
    for i in range(2,8):
        row=f['frames'][i];row['layers']['legs']['asset']='run_leg_%d'%(i-2)
        row['layers']['body'].update(asset='body_0',cung_asset='body_hold_cung')
    for i in [0,1]:f['frames'][i]['layers']['body']['cung_asset']='body_hold_cung'
    # Split the new full poses along authored anatomical seams. All three parts
    # share a canvas and seam anchors, so their recomposition is pixel-exact.
    air=keyed(SRC/'air_poses_wind_v1.png')
    poses=[('roll',(210,15,595,495),(392,266),(313,385),(450,480),(480,330),
            [(200,0),(610,0),(610,280),(420,284),(370,257),(350,210),(200,210)],
            [(380,275),(470,265),(550,290),(550,450),(430,500),(260,490),(258,400),(315,370)],142),
           ('fall',(865,15,1335,600),(1110,266),(1030,328),(930,580),(1291,353),
            [(1030,0),(1335,0),(1335,280),(1160,290),(1100,260),(1070,200),(1025,155)],
            [(1045,320),(1200,285),(1250,365),(1190,480),(1080,530),(970,605),(850,605),(870,450),(920,350)],192)]
    for name,box,neck,hip,sole,grip,hpoly,lpoly,height in poses:
        im=air.crop(box);size=224 if name=='roll' else 256
        scale=height/im.height
        origin=np.array([(size-im.width*scale)/2,(size-im.height*scale)/2])
        point=lambda xy:list((np.array(xy)-box[:2])*scale+origin)
        head=Image.new('L',im.size);legs=Image.new('L',im.size)
        for mask,poly in [(head,hpoly),(legs,lpoly)]:ImageDraw.Draw(mask).polygon([(x-box[0],y-box[1]) for x,y in poly],fill=255)
        hm=np.array(head)>0;lm=(np.array(legs)>0)&~hm
        masks={'head':hm,'legs':lm,'body':~(hm|lm)}
        anc={'neck':point(neck),'hip':point(hip),'sole':point(sole),'grip':point(grip),'near_hand':point(grip),'far_hand':point(grip),'back':point(hip)}
        for layer,mask in masks.items():
            ar=np.array(im);ar[~mask]=0;piece=Image.fromarray(ar).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
            canvas=Image.new('RGBA',(size,size));canvas.alpha_composite(piece,tuple(np.round(origin).astype(int)))
            for turn in (range(4) if name=='roll' else range(1)):
                rotated=canvas.rotate(-90*turn,Image.Resampling.NEAREST,center=(size/2,size/2))
                angle=math.radians(90*turn);co,si=math.cos(angle),math.sin(angle)
                anchors={k:[size/2+co*(v[0]-size/2)-si*(v[1]-size/2),size/2+si*(v[0]-size/2)+co*(v[1]-size/2)] for k,v in anc.items()}
                save('%s_%s_%d'%(name,layer,turn),rotated,anchors,{'sheet':'air_poses_wind_v1','crop':list(box),'rotation_offline':90*turn,'layer':layer})
    # Calibrate the clenched low fist on actual skin, excluding its central crease.
    body=assets['fall_body_0'];im=np.array(Image.open(ART/body['file']))
    gx,gy=body['anchors']['grip'];yy,xx=np.indices(im.shape[:2]);r,g,b=im[:,:,:3].astype(int).transpose(2,0,1)
    mask=(im[:,:,3]>220)&(r>155)&(g>80)&(r-g>25)&((xx-gx)**2+(yy-gy)**2<100)
    ys,xs=np.where(mask);centre=np.array([xs.mean(),ys.mean()]);j=np.argmin((xs-centre[0])**2+(ys-centre[1])**2)
    for key in ['grip','near_hand','far_hand']:body['anchors'][key]=[float(xs[j]),float(ys[j])]
    for i in range(8,12):
        row=f['frames'][i]
        for layer in ['head','body','legs']:row['layers'][layer]['asset']='roll_%s_%d'%(layer,i-8)
        row['roll_origin']=[-56,-100]
    for layer in ['head','body','legs']:f['frames'][12]['layers'][layer]['asset']='fall_%s_0'%layer
    f['frames'][12]['layers']['body']['cung_asset']='fall_body_0'
    # The airborne held pose also uses a clenched fist, not the old open-hand torso.
    f['frames'][21]['layers']['body'].update(asset='fall_body_0',cung_asset='fall_body_0')
    f['clips']['jump']['frames']=[7];f['clips']['fall']['frames']=[12]
    wind=air.crop((120,520,665,995));wind=wind.resize((208,208),Image.Resampling.LANCZOS)
    p['roll_winds']=[]
    for i in range(4):
        id='roll_wind_%d'%i;p['roll_winds'].append(id)
        save(id,wind.rotate(-90*i,Image.Resampling.NEAREST),{'centre':[104,104]},{'sheet':'air_poses_wind_v1','effect':'separate_centered_wind','rotation_offline':90*i})
    # Rotate held weapons offline; grip will be buried by a foreground hand mask.
    for id,source,angle in [('sword_hold','sword',160),('sword_run','sword',160),('bow_hold','bow_idle',40)]:
        a=assets[source];im=Image.open(ART/a['file']);g=np.array(a['anchors']['grip']);C=np.array([192.,192.])
        old=math.degrees(math.atan2(*(np.array(a['anchors']['tip'])-g)[::-1])) if source=='sword' else 0
        # Bow top/bottom vector has an intrinsic lean: solve its final 40-degree axis.
        rotation=angle-old
        if source=='bow_idle':
            v=np.array(a['anchors']['top'])-a['anchors']['bottom'];rotation=40-math.degrees(math.atan2(v[0],-v[1]))
        cv=Image.new('RGBA',(384,384));cv.alpha_composite(im,tuple(np.round(C-g).astype(int)))
        cv=cv.rotate(-rotation,Image.Resampling.BICUBIC,center=tuple(C));r=math.radians(rotation);co,si=math.cos(r),math.sin(r)
        anchors={k:list(C+np.array([co*(v[0]-g[0])-si*(v[1]-g[1]),si*(v[0]-g[0])+co*(v[1]-g[1])])) for k,v in a['anchors'].items()}
        save(id,cv,anchors,{'own_asset':source,'held_angle':angle,'offline_rotation':rotation})
    # Independent broad white/blue effect art, using source offsets only for placement.
    sheet=keyed(SRC/'slash_crescent_surge_v1.png')
    crescent=sheet.crop((30,180,1000,710));crescent=crescent.crop(crescent.getbbox())
    surge=sheet.crop((1000,280,sheet.width,650));surge=surge.crop(surge.getbbox())
    p['numeric_trails']={}
    for action,blue in [('slash',False),('tram_kiem',True)]:
        p['numeric_trails'][action]={}
        for eid,source,phases in [('16',crescent,[(.65,.75,1),(1,1,1),(1,.85,1),(.8,.75,.55),(.65,.6,.22)]),('39',surge,[(1,1,1),(1,.8,.45)])]:
            ids=[]
            for i,(sx,sy,opacity) in enumerate(phases):
                w,h=(268,150) if eid=='16' else (156,64)
                if blue:w,h=round(w*1.08),round(h*1.13)
                im=source.resize((round(w*sx),round(h*sy)),Image.Resampling.LANCZOS)
                ar=np.array(im);rgb=ar[:,:,:3];dark=rgb.max(axis=2)<110
                if blue:
                    light=~dark;lum=rgb.mean(axis=2)/255
                    ar[light,0]=(75+145*lum[light]**3).astype('uint8');ar[light,1]=(175+75*lum[light]).astype('uint8');ar[light,2]=255
                ar[:,:,3]=(ar[:,:,3].astype(float)*opacity).astype('uint8')
                im=Image.fromarray(ar)
                id='trail_%s_%s_%d'%(action,eid,i);ids.append(id)
                save(id,im,{'centre':[im.width/2,im.height/2]},{'sheet':'slash_crescent_surge_v1','effect':int(eid),'phase':i,'core_alpha':opacity,'palette':'blue' if blue else 'white'})
            p['numeric_trails'][action][eid]=ids
    print('Motion art: six strides; upright run torso; buried held grips; 40deg low bow; tucked 90deg roll + centered wind; rise7/fall12; broad source16/39 trails.')
