#!/usr/bin/env python3
"""Put actual frames0..7 directly below matching reference cells, OUTSIDE repo."""
from pathlib import Path
import argparse,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--reference',type=Path,default=Path('/tmp/ref_render'));ap.add_argument('--renders',type=Path,default=ROOT/'prototype/pose_rig/reports/ablation_v10');ap.add_argument('--out',type=Path,default=Path('/tmp/ref_render'));args=ap.parse_args();out=args.out.resolve();assert not out.is_relative_to(ROOT),'Reference pixels must stay outside repository';out.mkdir(parents=True,exist_ok=True)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19)
    for school in ['kiem','cung']:
        reference=Image.open(args.reference/f'ref_cam_{school}.png').convert('RGB')
        for direction in [-1,1]:
            board=Image.new('RGBA',(2048,660),(32,40,51,255));draw=ImageDraw.Draw(board);draw.text((20,10),f'{school}: tham khảo / neutral H131 → H128; cùng góc nhìn',font=font,fill='white');draw.text((20,340),'Bản mới: Godot thật H128; frame0 + delta tham khảo ×512/131',font=font,fill='white')
            for frame in range(8):
                cell=reference.crop((frame*280,0,(frame+1)*280,248)).convert('RGBA');cell=cell.resize((round(280*128/131),round(248*128/131)),Image.Resampling.LANCZOS)
                aligned=Image.new('RGBA',(256,256));aligned.alpha_composite(cell,(round(128-100*128/131),round(210-216*128/131)))
                if direction<0:aligned=aligned.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                board.alpha_composite(aligned,(frame*256,40))
                own=Image.open(args.renders/f'{school}_{"left" if direction<0 else "right"}_{frame:02d}.png').convert('RGBA').crop((0,0,256,256));board.alpha_composite(own,(frame*256,375))
                draw.text((frame*256+105,305),f'{frame:02d}',font=font,fill='#ffe49a');draw.text((frame*256+105,635),f'{frame:02d}',font=font,fill='#ffe49a')
            path=out/f'held_v10_compare_{school}_{"left" if direction<0 else "right"}.png';board.convert('RGB').save(path);print('External reference/actual row comparison:',path,'2048x660; frames0–7 in matching columns')
if __name__=='__main__':main()
