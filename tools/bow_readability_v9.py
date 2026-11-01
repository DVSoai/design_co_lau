"""Restyle the existing bow curve only; endpoints, transform and grip stay fixed."""
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BASELINE=ROOT/'art/sprites/weapons/lv1/sources/cung_lv1_geometry_v8.svg'

def arc(t,sign):
    # Exact existing main cubic from tip to central grip, reflected for lower limb.
    p=np.array([[7,-59],[35,-47],[52,-26],[52,0]],float)
    if sign>0:p[:,1]*=-1
    q=(1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3]
    d=3*(1-t)**2*(p[1]-p[0])+6*(1-t)*t*(p[2]-p[1])+3*t*t*(p[3]-p[2]);d/=np.linalg.norm(d)
    return q,np.array([-d[1],d[0]])
def ribbon(sign,width_tip,width_middle,offset=0):
    left=[];right=[]
    for t in np.linspace(0,1,121):
        q,n=arc(float(t),sign);width=width_tip+(width_middle-width_tip)*np.sin(t*np.pi*.5)
        left.append(q+n*(offset+width*.5));right.append(q+n*(offset-width*.5))
    points=left+right[::-1]
    if width_middle<=4.0:
        # Preserve an opaque black edge inside the existing fixed right crop.
        angle=np.radians(23);toward=np.array([np.cos(angle),-np.sin(angle)])
        points=[v-toward*max(0,float(v@toward)-53.2) for v in points]
    return 'M'+' L'.join(f'{v[0]:.5f} {v[1]:.5f}' for v in points)+' Z'
def svg():
    # Preserve the original tip hooks/caps and the exact23deg offline rotation.
    s='<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="-130 -150 280 280"><g transform="rotate(23)" stroke="#16110e" stroke-linejoin="round">'
    s+='<path d="M0 -66 L0 66" stroke="#c3bfa7" stroke-width=".55" fill="none"/>'
    s+='<path d="M-3 -65 Q-8 -71 -1 -69 Q0 -63 7 -59 C35 -47 52 -26 52 0 C52 26 35 47 7 59 Q0 63 -1 69 Q-8 71 -3 65" stroke="#201810" stroke-width="5.2" stroke-linecap="round" fill="none"/>'
    s+='<path d="M-3 -65 Q-7 -69 -1 -68 Q0 -62 7 -59 C35 -47 52 -26 52 0 C52 26 35 47 7 59 Q0 62 -1 68 Q-7 69 -3 65" stroke="#c86455" stroke-width="1.7" stroke-linecap="round" fill="none"/>'
    for sign in [-1,1]:
        s+=f'<path d="{ribbon(sign,5.2,6.6)}" fill="#16110e" stroke="none"/>'
        s+=f'<path d="{ribbon(sign,1.7,4.0)}" fill="#c86455" stroke="none"/>'
        s+=f'<path d="{ribbon(sign,.55,1.0,offset=.75 if sign<0 else -.75)}" fill="#f1aa83" stroke="none"/>'
    s+='<path d="M48.5 -9 Q52 -10 55.5 -9 L55.5 9 Q52 10 48.5 9 Z" fill="#8a9e46" stroke-width="1.2"/>'
    for y in [-7,-4,-1,2,5]:s+=f'<path d="M49 {y} L55 {y+2}" stroke="#21371d" stroke-width=".65"/>'
    s+='<path d="M50 -7 L50.5 6" stroke="#7caa55" stroke-width=".7"/>'
    # Collar midpoint remains exactly[52,0], despite a longer contrasting wrap.
    for y in [-9,7]:s+=f'<path d="M49 {y} Q52 {y-1} 55 {y} L55 {y+2} L49 {y+2} Z" fill="#e3b658" stroke-width=".8"/>'
    # Unmodified end-cap paths from the existing original SVG.
    for sign in [-1,1]:
        s+=f'<path d="M0 {sign*61} L3 {sign*63} L-1 {sign*68} L-4 {sign*66} Z" fill="#d4a24c" stroke="#201810" stroke-width="1"/>'
        s+=f'<path d="M0 {sign*62} L1 {sign*64}" stroke="#fff0ad" stroke-width=".6"/>'
    return s+'</g></svg>'
