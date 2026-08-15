"""ramp_rate_verify.py — fast (dps=12), uses mp.quad on split domain."""
import mpmath as mp
mp.mp.dps = 12
SR2 = mp.sqrt(2); INV = 1/mp.sqrt(2)
def sinc(z): return mp.sin(z)/z
def kMT(x):
    return (sinc(INV-mp.pi*x)+sinc(INV+mp.pi*x))/(2*SR2*mp.sin(INV))
def rho(s):
    return mp.mpf(max(0.0,min(1.0,float(s))))
def integ(lam,L,w,x,u):
    return mp.cos(SR2*lam*u/L)*(rho((L/2-mp.fabs(u))/w)**2)*mp.cos(2*mp.pi*x*u/L)
def O_ramp(lam,L,w,x,maxdeg=20):
    L=mp.mpf(L); w=mp.mpf(w); x=mp.mpf(x)
    # split: left ramp band [-L/2, -L/2+w], bulk [-L/2+w, L/2-w] (ramp=1),
    # right ramp band [L/2-w, L/2].
    bl = -L/2; br = -L/2 + w   # left ramp band
    bL = -L/2 + w; bR = L/2 - w  # bulk (ramp = 1)
    rL = L/2 - w; rR = L/2      # right ramp band
    def fbulk(u): return mp.cos(SR2*lam*u/L)*mp.cos(2*mp.pi*x*u/L)
    bulk = mp.quad(fbulk, [bL, bR], maxdegree=maxdeg)
    def fLband(u): return integ(lam,L,w,x,u)
    lb = mp.quad(fLband, [bl, br], maxdegree=maxdeg)
    rb = mp.quad(fLband, [rL, rR], maxdegree=maxdeg)
    return bulk + lb + rb
lam=mp.mpf(1); w=mp.mpf(8)
print(f"ramp w=8, lam=1  (mp.quad maxdegree=20, dps=12)")
for xv in ['0.3','1.0','1.9']:
    x=mp.mpf(xv)
    print(f"--- x={xv} ---")
    for L in [100,1000,10000]:
        O0=O_ramp(lam,L,w,0); Ox=O_ramp(lam,L,w,x); r=Ox/O0; err=r-kMT(x)
        print(f"    L={L:6d} ratio={mp.nstr(r,9)} kMT={mp.nstr(kMT(x),9)} err={mp.nstr(err,6)} err*L={mp.nstr(err*L,6)}")
