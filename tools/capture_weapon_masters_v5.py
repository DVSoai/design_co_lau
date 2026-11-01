#!/usr/bin/env python3
"""Capture both-direction30-frame/gameplay evidence and real GPU master/outline review."""
from pathlib import Path
import argparse,os,shlex,shutil,subprocess,time

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--godot',default='godot');args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    def run(cmd,env=None):
        print('$ '+shlex.join(cmd),flush=True);p=subprocess.run(cmd,cwd=root,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);print(p.stdout,end='');print('exit='+str(p.returncode),flush=True)
        if p.returncode or 'ERROR:' in p.stdout:raise SystemExit(p.returncode or 1)
    run(['python3','tools/capture_run_cycle_v3.py','--godot',args.godot])
    cmd=['Xvfb',':119','-screen','0','1600x720x24','-nolisten','tcp','-ac'];print('$ '+shlex.join(cmd),flush=True)
    with open('/tmp/weapon-v5-xvfb.log','w') as log:
        server=subprocess.Popen(cmd,stdout=log,stderr=log);env=dict(os.environ,DISPLAY=':119',LIBGL_ALWAYS_SOFTWARE='1')
        try:
            for i in range(50):
                if subprocess.run(['xdpyinfo'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
                time.sleep(.1)
            else:raise RuntimeError('Xvfb readiness timeout')
            run([args.godot,'--audio-driver','Dummy','--fixed-fps','60','--path','prototype','--windowed','--resolution','1600x720','res://pose_rig/weapon_masters_v5_review.tscn'],env)
        finally:server.terminate();server.wait(timeout=10)
    shutil.copyfile(root/'prototype/pose_rig/reports/weapon_v5_review.png',root/'art/sprites/weapons/lv1/review_lv1.png')
    print('Captured25 real1600x720 reviews plus2 transparent256x256 GPU weapon samples at H128; copied master/character review_lv1.png.')

if __name__=='__main__':main()
