#!/usr/bin/env python3
"""Real Godot/Xvfb captures: baseline viewer/gameplay plus128px run strip and live running."""
from pathlib import Path
import argparse,os,shlex,subprocess,time

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--godot',default='godot');args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    def run(cmd,env=None):
        print('$ '+shlex.join(cmd),flush=True)
        r=subprocess.run(cmd,cwd=root,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=90)
        print(r.stdout,end='');print('exit='+str(r.returncode),flush=True)
        if r.returncode or 'ERROR:' in r.stdout:raise SystemExit(r.returncode or 1)
    run(['python3','tools/capture_motion_review.py','--godot',args.godot])
    cmd=['Xvfb',':118','-screen','0','1600x720x24','-nolisten','tcp','-ac'];print('$ '+shlex.join(cmd),flush=True)
    with open('/tmp/run-v3-xvfb.log','w') as log:
        server=subprocess.Popen(cmd,stdout=log,stderr=log);env=dict(os.environ,DISPLAY=':118',LIBGL_ALWAYS_SOFTWARE='1')
        try:
            for i in range(50):
                if subprocess.run(['xdpyinfo'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
                if server.poll() is not None:raise RuntimeError('Xvfb startup failed')
                time.sleep(.1)
            else:raise RuntimeError('Xvfb readiness timeout')
            for school in ['kiem','cung']:
                for direction in ['right','left']:
                    for scene,flags in [('run_cycle_v3_review',[]),('play_test',['--capture-play','--run'])]:
                        cmd=[args.godot,'--audio-driver','Dummy','--fixed-fps','60','--path','prototype','--windowed','--resolution','1600x720','res://pose_rig/'+scene+'.tscn','--']+flags
                        if school=='cung':cmd+=['--cung']
                        if direction=='left':cmd+=['--left']
                        run(cmd,env)
        finally:server.terminate();server.wait(timeout=10)
    print('Captured24 real1600x720 PNGs: baseline16, focused run strips4, actual-input live running4; both schools/directions.')

if __name__=='__main__':main()
