#!/usr/bin/env python3
"""Run every standalone Godot test; helper RefCounted suites run through their wrappers."""
from pathlib import Path
import argparse, concurrent.futures, os, shlex, subprocess, sys

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--godot',default='godot')
    parser.add_argument('--out',default='prototype/pose_rig/reports/playtest_godot_checks.txt')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    files=sorted(p for p in (root/'prototype/tests').glob('*.gd') if p.read_text().startswith('extends SceneTree'))
    def run(p):
        cmd=[args.godot,'--headless','--fixed-fps','60','--path','prototype','--script','res://tests/'+p.name]
        try:
            result=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=90)
            out=result.stdout;code=result.returncode
        except subprocess.TimeoutExpired as exc:
            out=exc.stdout or b''
            if isinstance(out,bytes):out=out.decode(errors='replace')
            code=124
        failed=code!=0 or 'SCRIPT ERROR:' in out or 'ERROR:' in out or 'FAIL:' in out
        return p.name,'$ '+shlex.join(cmd)+'\n'+out+'exit='+str(code)+'\n',failed
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,files))
    path=root/args.out;path.parent.mkdir(parents=True,exist_ok=True)
    text='\n'.join(r[1] for r in results)
    failures=sum(r[2] for r in results)
    summary=f'Godot standalone suites={len(results)} passed={len(results)-failures} failed={failures}; classic_checks.gd runs through smoke/classic_headless wrappers.\n'
    path.write_text(text+'\n'+summary)
    for name,_,failed in results:print(('FAIL ' if failed else 'PASS ')+name)
    print(summary,end='')
    return bool(failures)

if __name__=='__main__':sys.exit(main())
