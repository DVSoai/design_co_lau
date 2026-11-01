#!/usr/bin/env python3
"""Measure original alpha bboxes from a supplied folder or zip; never copy images.

python3 tools/measure_ref_bbox.py --source /absolute/source-or.zip --update
"""
from pathlib import Path
from io import BytesIO
import argparse,json,zipfile,hashlib
from PIL import Image

ITEMS={'kiem_cam_262':262,'cung_cam_283':283,'than_dung_5':5,'chan_dung_23':23,'than_danh_15':15,'chan_danh_31':31}
def measure(source):
    source=Path(source).resolve();archive=zipfile.ZipFile(source) if source.is_file() else None
    result={};rows=[]
    try:
        for name,icon in ITEMS.items():
            suffix=f'res/icon/4/{icon}.png'
            if archive:
                matches=[n for n in archive.namelist() if n.endswith(suffix)]
                if len(matches)!=1:raise ValueError(f'{suffix}: expected one entry, found {matches}')
                location=str(source)+'!/'+matches[0];data=archive.read(matches[0])
            else:
                matches=list(source.rglob(f'{icon}.png'));matches=[p for p in matches if p.as_posix().endswith(suffix)]
                if len(matches)!=1:raise ValueError(f'{suffix}: expected one file, found {matches}')
                location=str(matches[0]);data=matches[0].read_bytes()
            im=Image.open(BytesIO(data)).convert('RGBA');box=im.getchannel('A').getbbox()
            if box is None:raise ValueError(f'empty {location}')
            size=[box[2]-box[0],box[3]-box[1]];target=[round(v*128/131) for v in size];result[name]=target
            row={'name':name,'source':location,'source_bbox':list(box),'source_size':size,'scale':128/131,'target_128':target,'sha256':hashlib.sha256(data).hexdigest()};rows.append(row)
            print(json.dumps(row,ensure_ascii=False))
    finally:
        if archive:archive.close()
    return result,rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--update',action='store_true');ap.add_argument('--report');args=ap.parse_args()
    result,rows=measure(args.source)
    path=Path(__file__).resolve().parents[1]/'docs/ref/so_lieu_tham_khao.json';data=json.loads(path.read_text())
    if args.update:
        data['khung_kich_thuoc_128']=result
        data['khung_kich_thuoc_128_ghi_chu']='BBox alpha > 0 tại icon/4, nhân 128/131, làm tròn gần nhất; chỉ lưu số liệu, không lưu ảnh nguồn.'
        path.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
        print('Updated numeric khung_kich_thuoc_128:',json.dumps(result,ensure_ascii=False))
    else:
        assert data.get('khung_kich_thuoc_128')==result,'numeric reference table differs from actual measured source'
        print('PASS: all six numeric target bboxes equal the supplied original alpha measurements.')
    if args.report:Path(args.report).write_text(json.dumps({'scale':128/131,'rows':rows},ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
