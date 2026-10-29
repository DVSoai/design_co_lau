"""Measure manually identified anatomical landmarks on the actual side-view reference.
Segmentation detects the silhouette; neck and hip landmarks are explicitly manual,
not claimed to be inferred automatically from clothing pixels.
"""
from pathlib import Path
import hashlib, json
from PIL import Image
root = Path(__file__).resolve().parents[2]
p = root / 'art/reference/ref_dinh_bo_linh.png'
im = Image.open(p).convert('RGB')
box = (610, 20, 780, 570)
points = [(x,y) for y in range(box[1],box[3]) for x in range(box[0],box[2])
          if not (lambda c: c[1] > 240 and c[0] < 20 and c[2] < 20)(im.getpixel((x,y)))]
top, bottom = min(y for x,y in points), max(y for x,y in points)+1
# Half-open ranges; chosen visually at neck and waist/hip of the side view.
neck, hip = 174, 299
height = bottom-top
result = {'image':str(p.relative_to(root)), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
          'image_size':list(im.size), 'side_roi':list(box), 'silhouette_y':[top,bottom],
          'manual_neck_y':neck, 'manual_hip_y':hip, 'height_source_px':height,
          'segments':{name:{'source_px':b-a, 'at_96_px':round((b-a)*96/height,3)}
                      for name,a,b in [('head_hair',top,neck),('torso',neck,hip),('legs_feet',hip,bottom)]}}
text=json.dumps(result,ensure_ascii=False,indent=2)
(root/'prototype/rig/reports/reference_measurements.json').write_text(text+'\n')
print(text)

# v3: manually declared anatomical sampling bands on the same side-view ROI.
# Shoulder=198, chest=240, hip under belt=330; collar174/hem360 map homologous
# cloth levels to the rig. These are visible-silhouette measurements, not hidden
# anatomy inferred through the near sleeve/arm. No weapon pixels enter the bands.
import sys,math,numpy as np
bands={'shoulder':198,'chest':240,'hip':330}
widths={}
for name,yy in bands.items():
    spans=[]
    for y in range(yy-1,yy+2):
        pixels=[x for x in range(box[0],box[2]) if not (lambda c:c[1]>240 and c[0]<20 and c[2]<20)(im.getpixel((x,y)))]
        spans.append(max(pixels)-min(pixels)+1)
    width=float(np.median(spans));widths[name]={'source_y':yy,'three_row_spans':spans,'width_px':width,'ratio':width/height,'target_at_96_px':width/height*96}
result['width_measurements']={'manual_collar_y':174,'manual_hem_y':360,'bands':widths,'method':'median visible side-silhouette span across y-1,y,y+1; source arms/cloth overlap disclosed'}
(root/'prototype/rig/reports/reference_measurements.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('REFERENCE WIDTHS:')
for name,row in widths.items():print(f'{name}: source y={row["source_y"]}, spans={row["three_row_spans"]}, w/H={row["width_px"]:g}/{height}={row["ratio"]:.6f}; at96={row["target_at_96_px"]:.3f}px')
if '--v3' in sys.argv:
    sys.path.insert(0,str(root/'tools'))
    from render_parts_scene import layers
    states={
      'before':(root/'prototype/rig/reports/v3_baseline/evaluated_art_frames.json',root/'prototype/rig/reports/v3_baseline/parts.json',root/'docs/reports/g1_parts_v3_before_idle_1x.png'),
      'after':(root/'prototype/rig/reports/evaluated_art_frames.json',root/'prototype/rig/data/parts.json',root/'prototype/rig/contact_sheets/art/chr_dbl_idle_art_1x.png')}
    measured={};pose_rows=[]
    for state,(frame_path,part_path,image_path) in states.items():
        frames=json.loads(frame_path.read_text());parts={p['id']:p for p in json.loads(part_path.read_text())['parts']}
        body=parts['body'];head=parts['head'];frame=frames['idle']['frames'][0]
        image=np.array(Image.open(image_path).convert('RGBA'));ys,xs=np.where(image[:,:,3]>0);actual_h=int(ys.max()-ys.min()+1)
        transform=next(g['transform'] for g in frame['geometry'] if g['kind']=='sprite' and g['id']=='body')
        a,b,c,d,tx,ty=transform;measured[state]={}
        for name,ref in widths.items():
            fraction=(ref['source_y']-174)/(360-174)
            local_y=head['attach'][1]+fraction*(body['size'][1]-body['pivot'][1]-head['attach'][1])
            row=math.floor(120+b*body['pivot'][0]+d*(body['pivot'][1]+local_y)+ty)
            xx=np.where(image[row,:,3]>0)[0];span=int(xx.max()-xx.min()+1);ratio=span/actual_h
            error=ratio/ref['ratio']-1
            measured[state][name]={'rendered_image':str(image_path.relative_to(root)),'image_row':row,'width':span,'height':actual_h,'ratio':ratio,'relative_error':error,'within_10_percent':abs(error)<=.1}
            print(f'{state} {name}: scene PNG row={row}; width/height={span}/{actual_h}={ratio:.6f}; reference={ref["ratio"]:.6f}; error={100*error:+.3f}%; {"PASS" if abs(error)<=.1 else "FAIL"}')
        for name in ['idle','turn','land']:
            for index,f in enumerate(frames[name]['frames']):
                joints=f['joints'];knees=[];soles=[]
                for side in ['near','far']:
                    hip=np.array(joints['thigh_'+side]);knee=np.array(joints['shin_'+side]);ankle=np.array(joints['foot_'+side]);u=knee-hip;v=ankle-knee
                    knees.append(math.degrees(math.acos(float(np.clip(u@v/(np.linalg.norm(u)*np.linalg.norm(v)),-1,1)))))
                    foot=parts['foot_'+side];t=next(g['transform'] for g in f['geometry'] if g['kind']=='sprite' and g['id']=='foot_'+side)
                    soles.append(max(t[1]*x+t[3]*y+t[5] for x,y in [(0,0),(foot['size'][0],0),tuple(foot['size']),(0,foot['size'][1])]))
                t=next(g['transform'] for g in f['geometry'] if g['kind']=='sprite' and g['id']=='body')
                torso=math.degrees(math.atan2(t[1],t[0]));hip_y=joints.get('hip',joints['body'])[1]
                row={'state':state,'clip':name,'frame':index+1,'knee_near':knees[0],'knee_far':knees[1],'torso_degrees':torso,'hip_y':hip_y,'torso_y':joints['body'][1],'sole_near_y':soles[0],'sole_far_y':soles[1]};pose_rows.append(row)
                print(f'{state} {name} frame{index+1}: knee={knees[0]:.5f}/{knees[1]:.5f} deg; body={torso:.5f} deg; hip_y={hip_y:.6f}; torso_y={joints["body"][1]:.6f}; soles={soles[0]:.6f}/{soles[1]:.6f}')
    report={'reference':result,'body_ratios':measured,'pose_rows':pose_rows}
    (root/'prototype/rig/reports/parts_v3_measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    # The before state is intentionally allowed to fail the new aesthetic gate;
    # it is evidence of the problem, not a failed current-build test.
    assert all(v['within_10_percent'] for v in measured['after'].values()),'after body ratios outside 10%'
    for r in pose_rows:
        if r['state']=='after' and (r['clip']=='idle' or (r['clip'] in ['turn','land'] and r['frame']==2)):
            assert max(r['knee_near'],r['knee_far'])<=5 and abs(r['torso_degrees'])<=2
            assert max(abs(r['sole_near_y']),abs(r['sole_far_y']))<.001
    idle=[r for r in pose_rows if r['state']=='after' and r['clip']=='idle']
    assert max(r['hip_y'] for r in idle)-min(r['hip_y'] for r in idle)<.001
    assert all(abs(r['torso_y']-idle[0]['torso_y']-offset)<.001 for r,offset in zip(idle,[0,-1,-2,-1]))
    print('V3 measurements: all current constraints PASS (historical before ratios printed separately)')
