# -*- coding: utf-8 -*-
"""
atone_xip_mt.py — T3-open-A: the AtOne certificate content for the ξ′ MT-window constant
κ₁(1, vMT), vMT(s) = cos(√2·s).

Rigorous Arb enclosures (python-flint 0.9.0, ctx.dps = 200) for the exact AtOne constant:

  κ₁(1, vMT) = (∫vMT² + jWin(D1, 1, vMT)) / (∫vMT)² ,   (Lean Defs.kappaXi_one form)

with
  ∫vMT   = 2·sin(1/√2)/√2                                  (√2 = sqrt(2))
  ∫vMT²  = a  = 1/2 + sin(√2)/(2√2)
  ∫vMT⁴  = b  = 3/8 + sin(√2)/(2√2) + sin(2√2)/(16√2)
  vConv vMT r = ∫_{-1/2}^{1/2-r} cos(√2 s)·cos(√2(s+r)) ds
             = ½·(1−r)·cos(√2 r) + sin(√2(1−r))/(2√2)      (exact, product-to-sum)
  D1 s   = s − 4s² + Σ_k D1coeff k · s^{2k+3}              (Lean Defs.D1)
  jWin(D1,1,vMT) = 2·∫_0^1 D1(r)·vConv vMT r dr          (Lean Defs.jWin at lam=1)

Certified sandwich (mirror of Certificate/D1.lean + AtOne.lean):

  D1trunc 9 ≤ D1 ≤ D1trunc 9 + ε₉  on [0,1],  ε₉ = 1024/2990212875,
  vConv vMT r ≥ 0 for r ∈ [0,1],
  whence
     jWin(D1,1,vMT) ∈ [ J1 , J1 + ε₉·(∫vMT)² ],  J1 := 2∫₀¹ D1trunc9(r)·vConv vMT r dr ,
  and
     κ₁(1,vMT) ∈ [κ₉ , κ₉ + ε₉] ,  κ₉ := (∫vMT² + J1)·(∫vMT)^{-2} .

RIGOR in the quadrature: J1 is enclosed by a composite Simpson rule on a fine uniform
grid; the remainder is bounded via the EXACT symbolic 4th derivative of the integrand
(sympy, reduced to  A(r)·1 + B(r)·cos(√2 r) + C(r)·sin(√2 r)  with exact rational
coefficients), evaluated as an ARB INTERVAL over each panel. Interval arithmetic is a
rigorous range enclosure, so the Simpson remainder bound is rigorous. ∫vMT, a, b, and the
vConv values come from EXACT closed forms evaluated as ARB intervals (rigorous).

Everything reported is therefore a CERTIFIED enclosure, not mere numerical evidence.
mpmath quadrature is run only as an independent EVIDENCE cross-check.

Output protocol: FINITE_COMPUTATIONAL_RESULT — the math-level κ₉ sandwich is certified;
the exact remaining open items are the Lean formalization of the Fubini identity
2∫₀¹ vConv vMT = (∫vMT)² and the closed-form trig integral evaluations (recorded as
open Lean obligations M3-open-A).
"""
import math
import sympy as sp
import mpmath as mp
from flint import arb, ctx, fmpq

ctx.dps = 200
SQ2 = arb(2).sqrt()

# --------------------------------------------- D1 series exactly as Lean Defs.lean
def _fact(n):
    return math.factorial(n)

def D1coeff(k):
    """D1coeff k = 2*4^(k+1)*k!/(2k+2)!  (exact fmpq -> arb)."""
    n = 2 * (4 ** (k + 1)) * _fact(k)
    d = _fact(2 * k + 2)
    return arb(fmpq(n, d))

def D1coeff_frac(k):
    from fractions import Fraction
    return Fraction(2 * (4 ** (k + 1)) * _fact(k), _fact(2 * k + 2))

def D1trunc9(r):
    """Lean Defs.D1trunc 9: s - 4 s^2 + Σ_{k=0..8} D1coeff k · s^{2k+3}."""
    s = r
    tot = s - 4 * s * s
    for k in range(0, 9):
        tot += D1coeff(k) * s ** (2 * k + 3)
    return tot

EPS9 = arb("1024/2990212875")            # Lean Certificate/D1.lean eps9  (< 3.425e-7)

def enc(lo, hi):
    """rigorous enclosure [lo, hi] as an arb interval (arb(mid,rad) constructor semantics)."""
    return arb((lo + hi) / 2, (hi - lo) / 2)

def vConvMT(r):
    """closed form ½·(1−r)·cos(√2 r) + sin(√2(1−r))/√2   [NOT /(2√2)!]."""
    return arb("1/2") * ((1 - r) * (SQ2 * r).cos() + (SQ2 * (1 - r)).sin() / (SQ2))

def INT_VMT():
    return (arb(1) / SQ2).sin() * 2 / SQ2     # 2 sin(1/√2)/√2 = √2 sin(1/√2)

def A_INT():
    return arb("1/2") + SQ2.sin() / (2 * SQ2)  # ∫vMT²

def B_INT():
    return arb("3/8") + SQ2.sin() / (2 * SQ2) + (2 * SQ2).sin() / (16 * SQ2)  # ∫vMT⁴

# ------------------------------------------- exact symbolic 4th derivative of D1trunc9 * vConv
_tr = sp.symbols('r', real=True)
_ts = sp.sqrt(2)
_tvc = sp.Rational(1, 2) * ((1 - _tr) * sp.cos(_ts * _tr) + sp.sin(_ts * (1 - _tr)) / _ts)
_td9 = _tr - 4 * _tr ** 2
for _k in range(0, 9):
    _td9 += sp.Rational(D1coeff_frac(_k).numerator, D1coeff_frac(_k).denominator) * _tr ** (2 * _k + 3)
_tf4 = sp.expand(sp.diff(_td9 * _tvc, _tr, 4))
# reduce to  A(r) + B(r)*cos(s r) + C(r)*sin(s r)  (exact rational coeffs)
_cs = sp.cos(_ts); _sn = sp.sin(_ts)
_tcr = sp.cos(_ts * _tr); _tsr = sp.sin(_ts * _tr)
_tf4r = sp.expand(
    _tf4.replace(sp.cos(_ts * _tr - _ts), _tcr * _cs + _tsr * _sn)
         .replace(sp.sin(_ts * _tr - _ts), _tsr * _cs - _tcr * _sn))
_As = sp.S.Zero; _Bs = sp.S.Zero; _Cs = sp.S.Zero
for _term in sp.Add.make_args(_tf4r):
    _tg = _term.atoms(sp.cos, sp.sin)
    _tg = [t for t in _tg if _tr in t.free_symbols]   # only genuine functions of r
    if not _tg:
        _As += _term
        continue
    assert len(_tg) == 1, (_tg, _term)
    _t = _tg[0]
    _co = sp.cancel(_term / _t)
    if _t == _tcr:
        _Bs += _co
    elif _t == _tsr:
        _Cs += _co
    else:
        raise RuntimeError("unexpected " + str(_t))

def _poly_coeffs(poly):
    if poly == 0:
        return []
    return sp.Poly(poly, _tr).all_coeffs()   # high-order first; exact rationals

_Ac = _poly_coeffs(_As); _Bc = _poly_coeffs(_Bs); _Cc = _poly_coeffs(_Cs)

def _sym_to_arb(e):
    """rigorously evaluate a sympy constant expression (rational combo of 1, sin√2, cos√2)."""
    if isinstance(e, sp.Integer):
        return arb(int(e))
    if isinstance(e, sp.Rational):
        return arb(fmpq(int(e.p), int(e.q)))
    if e == _ts:
        return SQ2
    if isinstance(e, sp.Pow) and e.exp.is_integer:
        return _sym_to_arb(e.base) ** int(e.exp)
    if isinstance(e, sp.Mul):
        out = arb(1)
        for f in e.args:
            out = out * _sym_to_arb(f)
        return out
    if isinstance(e, sp.Add):
        out = arb(0)
        for f in e.args:
            out = out + _sym_to_arb(f)
        return out
    if isinstance(e, sp.sin) and len(e.args) == 1 and e.args[0] == _ts:
        return SQ2.sin()
    if isinstance(e, sp.cos) and len(e.args) == 1 and e.args[0] == _ts:
        return SQ2.cos()
    raise RuntimeError("cannot convert to arb: " + str(e))

def _eval_poly(coeffs, r):
    out = arb(0)
    for co in reversed(coeffs):
        out = out * r + _sym_to_arb(co)
    return out

# ========================================================= MA1 exact constants (rigorous)
Iv = INT_VMT(); a = A_INT(); b = B_INT()
print("============== EXACT CONSTANTS (ARB, rigorous) ==============")
for nm, val in [("INT_VMT (∫vMT)", Iv), ("A = ∫vMT^2", a), ("B = ∫vMT^4", b)]:
    print(f"{nm:22s} = {val.mid().str(60)}  (rad {val.rad().str(8)})")

mp.mp.dps = 60
q1 = mp.quad(lambda s: mp.cos(mp.sqrt(2) * s), [-mp.mpf(1) / 2, mp.mpf(1) / 2])
q2 = mp.quad(lambda s: mp.cos(mp.sqrt(2) * s) ** 2, [-mp.mpf(1) / 2, mp.mpf(1) / 2])
q4 = mp.quad(lambda s: mp.cos(mp.sqrt(2) * s) ** 4, [-mp.mpf(1) / 2, mp.mpf(1) / 2])
print("  EVIDENCE quad: ∫cos =", mp.nstr(q1, 40))
print("  EVIDENCE quad: ∫cos² =", mp.nstr(q2, 40), " (a =", mp.nstr(a.mid(), 40), ")")
print("  EVIDENCE quad: ∫cos⁴ =", mp.nstr(q4, 40), " (b =", mp.nstr(b.mid(), 40), ")")

# ========================================================= MA2 vConv closed form vs quadrature
print("============== vConv vMT closed form vs quadrature (EVIDENCE) ==============")
for rq in [mp.mpf(1) / 4, mp.mpf(1) / 2, mp.mpf(3) / 4, mp.mpf(1) / 5, mp.mpf(1) / 10]:
    q = mp.quad(lambda s: mp.cos(mp.sqrt(2) * s) * mp.cos(mp.sqrt(2) * (s + rq)),
                [-mp.mpf(1) / 2, mp.mpf(1) / 2 - rq])
    cf = mp.mpf(1) / 2 * ((1 - rq) * mp.cos(mp.sqrt(2) * rq) + mp.sin(mp.sqrt(2) * (1 - rq)) / mp.sqrt(2))
    print(f"  r={mp.nstr(rq, 6):8s} closed={mp.nstr(cf, 40)}  quad={mp.nstr(q, 40)}")

# ========================================================= MA3 J1 sandwich (rigorous)
print("============== J1 = 2∫_0^1 D1trunc9(r)·vConv vMT r dr (rigorous) ==============")
def integrand(r):
    return D1trunc9(r) * vConvMT(r)

# -------- rigorous global bound on max|f^{(4)}| on [0,1] via triangle inequality --------
# f4 = A(r) + cos(√2r)·B(r) + sin(√2r)·C(r)  with exact rational-coeff polynomials
# A,B,C (symbolic constants sin√2, cos√2 folded into the coefficients).
# For r ∈ [0,1]: |f4(r)| ≤ Σ|a_i| + Σ|b_j| + Σ|c_k|   (|cos|,|sin| ≤ 1, |r^i| ≤ 1).
def _poly_l1(coeffs):
    out = arb(0)
    for co in coeffs:
        out += abs(_sym_to_arb(co))
    return out

M4 = _poly_l1(_Ac) + _poly_l1(_Bc) + _poly_l1(_Cc)
M4_float = float(M4.mid())
print("rigorous global bound M4 = max|f^{(4)}| on [0,1] ≤", M4_float)

NQ = 20000
h = arb(1) / NQ
vals = [integrand(arb(0) + arb(1) * i / NQ) for i in range(NQ + 1)]
S = vals[0] + vals[NQ]
for i in range(1, NQ):
    if i % 2 == 1:
        S += 4 * vals[i]
    else:
        S += 2 * vals[i]
S = S * (1) / (3 * NQ)                     # composite Simpson of ∫_0^1 integrand
rem = M4 * h ** 4 / 180                     # global Simpson remainder bound
_J1_lo = S.mid() - S.rad() - rem
_J1_hi = S.mid() + S.rad() + rem
J1_int = enc(_J1_lo, _J1_hi)
J1_rig = 2 * J1_int                          # J1 = 2∫₀¹ D1trunc9·vConv
print("J1 = 2∫₀¹ D1trunc9·vConv enclosure:", J1_rig.mid().str(50), "  radius:", J1_rig.rad().str(10))

iv2 = Iv * Iv
tail = EPS9 * iv2
print("eps9 =", EPS9.mid().str(20))
print("(∫vMT)^2 =", iv2.mid().str(40))
print("eps9*(∫vMT)^2 =", tail.mid().str(40))

J1_lo = J1_rig.mid() - J1_rig.rad()
J1_hi = J1_rig.mid() + J1_rig.rad()
jw_lo_v = J1_lo                 # jWin(D1) >= J1  (D1trunc <= D1, vConv >= 0)
jw_hi_v = J1_hi + tail          # jWin(D1) <= J1 + tail
print("jWin(D1,1,vMT) ∈ [", jw_lo_v.mid().str(45), ",", jw_hi_v.mid().str(45), "]")

# ========================================================= MA4 kappa sandwich (rigorous)
print("============== κ₁(1,vMT) ∈ [κ₉, κ₉+ε₉] (rigorous) ==============")
Iv2_lo = iv2.mid() - iv2.rad(); Iv2_hi = iv2.mid() + iv2.rad()
a_lo = a.mid() - a.rad(); a_hi = a.mid() + a.rad()
# κ₉ = (a + J1)/(Iv)^2  enclosed: numerator interval = (a_lo+J1_lo, a_hi+J1_hi)
num_lo = a_lo + J1_lo
num_hi = a_hi + J1_hi
kap9_lo = num_lo / Iv2_hi       # / larger denom -> smaller
kap9_hi = num_hi / Iv2_lo       # / smaller denom -> larger
print("κ₉ = (∫vMT² + J1)/(∫vMT)² ∈ [", kap9_lo.mid().str(60), ",", kap9_hi.mid().str(60), "]")
print("κ₉ interval width:", (kap9_hi - kap9_lo).mid().str(5))
kap9_mid = (kap9_lo.mid() + kap9_hi.mid()) / 2

kap_lo_final = enc(kap9_lo.mid() - kap9_lo.rad(), kap9_lo.mid() + kap9_lo.rad())
kap_hi_final = kap9_hi + EPS9
print("\nCERTIFIED sandwich:  κ₁(1,vMT) ∈ [κ₉, κ₉+ε₉]")
print("  κ₉  ∈ [", kap9_lo.mid().str(70), ",", kap9_hi.mid().str(70), "]")
print("  κ₉+ε₉ ∈ [", (kap9_lo + EPS9).mid().str(70), ",", (kap9_hi + EPS9).mid().str(70), "]")

# ========================================================= MA5 cross-check H = 2 - kappa
print("============== H_xip = 2 − κ₁(1,vMT) cross-check vs canonical dps=120 ==============")
canon_H = mp.mpf('0.8678888651990519355503147104203403132225704976166306446')
canon_k = 2 - canon_H
H_lo = 2 - kap_hi_final
H_hi = 2 - kap9_lo
print("canonical κ₁(1,vMT) =", mp.nstr(canon_k, 70))
print("canonical H_xip_MT   =", mp.nstr(canon_H, 70))
print("this run  κ₉ mid     =", kap9_mid.str(70))
print("this run  κ upper    =", (kap9_hi + EPS9).mid().str(70))
print("this run  H lower    =", (2 - (kap9_hi + EPS9)).mid().str(70))
print("this run  H upper    =", (2 - kap9_lo).mid().str(70))
print("H ∈ [", H_lo.mid().str(45), ",", H_hi.mid().str(45), "]")
lo_num = (2 - (kap9_hi + EPS9)).mid() - (2 - (kap9_hi + EPS9)).rad() - 0
hi_num = (2 - kap9_lo).mid() + (2 - kap9_lo).rad()
print("canonical H inside enclosure:", (lo_num <= canon_H <= hi_num))

# kappa agreement with canonical value
print("\ncheck κ₁ ∈ [kap9_lo, kap9_hi+eps9] contains canonical κ₁:",
      (kap9_lo.mid() - kap9_lo.rad()) <= canon_k <= (kap9_hi.mid() + kap9_hi.rad() + EPS9.mid() + EPS9.rad()))

print("\nDONE")
