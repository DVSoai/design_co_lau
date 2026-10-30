#!/usr/bin/env python3
"""Capture actual Godot viewer, never synthesize an approval image."""
from pathlib import Path
import argparse,os,subprocess,time,shlex
p=argparse.ArgumentParser();p.add_argument('--godot',default='godot');p.add_argument('--xvfb',default='Xvfb');p.add_argument('--display',default=':114');a=p.parse_args();root=Path(__file__).resolve().parents[1]
cmd=[a.xvfb,a.display,'-screen','0','1600x720x24','-nolisten','tcp','-ac'];print('$ '+shlex.join(cmd),flush=True)
with open('/tmp/lv1-capture-xvfb.log','w') as log:
 server=subprocess.Popen(cmd,stdout=log,stderr=log)
 env=dict(os.environ,DISPLAY=a.display,LIBGL_ALWAYS_SOFTWARE='1')
 try:
  for _ in range(50):
   if subprocess.run(['xdpyinfo'],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:break
   if server.poll() is not None:raise RuntimeError('Xvfb failed; see /tmp/lv1-capture-xvfb.log')
   time.sleep(.1)
  else:raise RuntimeError('Xvfb readiness timeout')
  for school in ['kiem','cung']:
   for direction in ['right','left']:
    for page in ['frames','attacks','compare']:
     cmd=[a.godot,'--audio-driver','Dummy','--path','prototype','--windowed','--resolution','1600x720','res://pose_rig/pose_rig.tscn','--','--capture-lv1']
     if school=='cung':cmd+=['--cung']
     if direction=='left':cmd+=['--left']
     if page!='frames':cmd+=['--'+page]
     print('$ '+shlex.join(cmd),flush=True)
     result=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=30)
     print(result.stdout,end='');print(result.stderr,end='');print('exit='+str(result.returncode),flush=True)
     if result.returncode or 'ERROR:' in result.stderr:raise RuntimeError('Godot capture failed')
 finally:
  server.terminate();server.wait(timeout=10)
print('Captured12 actual Godot PNGs: 2schools x2directions x3pages, all1600x720.')
