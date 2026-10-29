#!/usr/bin/env python3
"""Build-time copy only: canonical Markdown grids remain in design/maps/."""
from pathlib import Path
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'prototype/dao_uc/layouts'
NAMES={'field':'lay_dao_uc_v1.md','boss':'lay_dao_uc_boss_v1.md'}
manifest={}
for key,name in NAMES.items():
 src=ROOT/'design/maps'/name;dst=DEST/name;DEST.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(src,dst)
 assert src.read_bytes()==dst.read_bytes()
 grid=re.search(r'^```layout\s*\n(.*?)^```',src.read_text(),re.M|re.S)[1]
 manifest[key]={'file':name,'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'counts':{c:grid.count(c) for c in '#=^~L'},'width':len(grid.splitlines()[0]),'height':len(grid.splitlines())}
 print(f'OK byte-identical {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}; sha256={manifest[key]["sha256"]}; counts={manifest[key]["counts"]}')
(DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
