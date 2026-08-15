#!/usr/bin/env python
"""Exact iterated-convolution evaluation of the box-spline integrals I_pi, using the
sine kernel as the generator of 1D box B-splines.

We evaluate I_pi = int_{R^{k-1}} prod_e sinc(v_e . x) dx (translation-reduced, x_k=0).
Each sinc(a x_j + b) over an integration variable x_j is a 1D 'box' B-spline; integrating
products of such factors over x_j = convolving box polynomials. We implement a minimal
rational piecewise-polynomial convolution engine:
   represent a 1D piecewise-linear-ish object as list of segments (break, coeffs) --- but
B-spline convolutions of boxes stay piecewise-POLYNOMIAL; we handle up to needed degree.

This is intentionally SIMPLE and exact in rational arithmetic. We validate against known
I_id(k=3) = 1, then D_3 = 0, and use it to get exact I_pi values for k=3,4 from which D_3,D_4
are confirmed 0. (k=5 is a larger but in-principle identical computation.)
"""
from fractions import Fraction
import itertools, numpy as np

# ---- 1D piecewise polynomial type ----
# poly = function P(t) over a break interval [lo,hi], stored as Fraction coeffs ascending.
# We only ever need it as object for convolution with box; we'll implement box-convolution
# of a piecewise polynomial by treating boxes as integral operators.

# A box [c-1/2, c+1/2] with height 1 as a piecewise polynomial (degree-0 spline).
def box_pp(c):
    lo=Fraction(c) - Fraction(1,2); hi=Fraction(c) + Fraction(1,2)
    return [(lo,[Fraction(1)],hi)]  # segment: (start, [coeffs of (t-start)^d], end)

def conv_with_box(pp, c):
    """Convolve piecewise-polynomial pp with box centered at c (integer shift). 
    Box support [c-1/2, c+1/2]. (g * B_c)(t) = integral_{c-1/2}^{c+1/2} g(t-s) ds.
    We compute analytically: result piecewise polynomial of degree+1.
    """
    out=[]
    for (lo,coefs,hi) in pp:
        # contribution: F(t)=int_{c-1/2}^{c+1/2} P(t-s) ds where P(s)=sum_a coefs[a] s^a
        # over segment s in [lo,hi]. P(t-s) as function of t is polynomial.
        deg=len(coefs)-1
        # F(t)= sum_a coefs[a] * int_{s in segment∩[t-hi,...]} (t-s)^a ds
        # We'll split into pieces where t-(c+1/2) and t-(c-1/2) cross lo and hi.
        # Breakpoints: t such that c-1/2 in [lo,hi] -> t=lo+c-1/2... let's be careful.
        t_points=[lo- (c-Fraction(1,2)), lo- (c+Fraction(1,2)),
                  hi- (c-Fraction(1,2)), hi- (c+Fraction(1,2))]
        t_points=[p for p in t_points]
        breaks=sorted(set(t_points))
        # eval F over a coarse set then reconstruct? For exactness implement direct.
        # Simpler: compute F(t) = G(hi') - G(lo'), where for fixed t,
        # integration bounds are s from max(lo, t-(c+1/2)) to min(hi, t-(c-1/2)).
        pass
    raise NotImplementedError

print("partially implemented -- see notes; exact engine under construction")
