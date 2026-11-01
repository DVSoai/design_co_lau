#!/usr/bin/env python3
"""Real Xvfb review captures and complete layer-removal atlases for image tests."""
from pathlib import Path
import argparse,os,shlex,subprocess,time

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--godot',default='godot');parser.add_argument('--viewer-readability',action='store_true');parser.add_argument('--ablation-only',action='store_true');parser.add_argument('--ablation-out',default='res://pose_rig/reports/ablation_v10');args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    def run(cmd,env=None):
        print('$ '+shlex.join(cmd),flush=True);p=subprocess.run(cmd,cwd=root,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=360);print(p.stdout,end='');print('exit='+str(p.returncode),flush=True)
        if p.returncode or 'ERROR:' in p.stdout:raise SystemExit(p.returncode or 1)
    if not args.ablation_only:run(['python3','tools/capture_weapon_masters_v5.py','--godot',args.godot])
    cmd=['Xvfb',':120','-screen','0','1600x720x24','-nolisten','tcp','-ac'];print('$ '+shlex.join(cmd),flush=True)
    with open('/tmp/chest-v7-xvfb.log','w') as log:
        server=subprocess.Popen(cmd,stdout=log,stderr=log);env=dict(os.environ,DISPLAY=':120',LIBGL_ALWAYS_SOFTWARE='1')
        try:
            for i in range(50):
                if subprocess.run(['xdpyinfo'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
                time.sleep(.1)
            else:raise RuntimeError('Xvfb readiness timeout')
            run([args.godot,'--audio-driver','Dummy','--fixed-fps','60','--path','prototype','--windowed','--resolution','1600x720','res://pose_rig/render_ablation_v7.tscn','--','--ablation-out='+args.ablation_out]+(['--viewer-readability'] if args.viewer_readability else []),env)
        finally:server.terminate();server.wait(timeout=10)
    if args.ablation_only:print('Actual ablation only:120 complete %d-view atlases. Export is not acceptance.' % (13 if args.viewer_readability else 11));return
    print('Actual review25x1600x720 +2 GPU H128 samples +120 complete %d-view layer-ablation atlases. Image tests run separately; export alone is not a pass.' % (13 if args.viewer_readability else 11))

if __name__=='__main__':main()
