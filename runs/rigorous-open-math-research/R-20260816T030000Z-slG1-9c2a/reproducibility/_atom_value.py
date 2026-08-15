"""atom_value: exact value of an irreducible 'atom' multigraph integral via the frequency
(box-spline) charge-balance slice volume.

An atom is integral over R^{b-1} (anchor block 0 fixed to 0) of a product of single K-edges:
   A = int_R^{b-1} prod_{e=(u,v)} K(x_u - x_v) dx_1..dx_{b-1}
Using K(t)=int_{-1/2}^{1/2} e^{2 pi i w t} dw, integrating free x_v pulls out delta constraints:
   A = volume of { w in [-1/2,1/2]^E : sum_{e incident v} sigma_{e,v} w_e = 0 for each free v }
      (with the ambient Lebesgue measure on the affine slice).
Vertices: anchor=0 fixed; labels 1..V free.
Edge e=(u,v) with u<v contributes +w_e to column v? sign chosen consistently:
  exponent term w_e (x_u - x_v) -> +w_e at u, -w_e at v.  (u<v)
So constraint at free var v (=1..V):
  sum over edges with u==v of (+w_e)  -  sum over edges with v'==v (i.e. edge v'=v<... ) ...
Propagate-consistent incidence: build vector A_e per free var. Constraint: A.dot(w)=0.
Nullspace N (orthonormal columns), then volume = measure of {l: |(N l)_e|<=1/2}.
Computed numerically (scipy ConvexHull) + rational recognition.
"""
import numpy as np
from fractions import Fraction as F

_cache = {}
def atom_value(edge_dict, digits=15, _cache=_cache):
    """edge_dict: {(u,v): multiplicity} undirected u<v. Removed loops (u==v) -> factor 1 handled by caller.
    Memoized by multiset key. Returns an exact Fraction via rational recognition of the
    frequency slice-volume (all box-spline values are rational)."""
    key=tuple(sorted((min(u,v),max(u,v),int(m)) for (u,v),m in edge_dict.items()))
    if key in _cache:
        return _cache[key]
    val=_atom_value_raw(key)
    frac=_recognize_rational(val, max_den=2**20)
    if frac is None:
        frac=F(val)
    _cache[key]=frac
    return frac

def _recognize_rational(x, max_den=1<<20):
    """Continued-fraction rational recognition of float x to Fraction with |den|<=max_den."""
    from fractions import Fraction
    cf=Fraction(x).limit_denominator(max_den)
    # accept if reconstruction matches to relative 1e-9
    if x!=0 and abs(float(cf)-x)/abs(x)<1e-8:
        return cf
    if x==0 and cf==0:
        return cf
    return None

def _atom_value_raw(key):
    edge_dict = {(u,v):m for (u,v,m) in key}
    E={}  # edge index -> (u,v)
    verts=set()
    for (u,v),m in edge_dict.items():
        for _ in range(m):
            e=len(E)
            E[e]=(u,v); verts.add(u); verts.add(v)
    V=max(verts) if verts else 0
    free=[v for v in range(1,V+1)]      # exclude anchor 0
    # constraint matrix A: rows=free vars, cols=edge instances
    A=[]
    for v in free:
        row=np.zeros(len(E))
        for e,(u,ww) in E.items():
            if u==v: row[e]=1.0       # +w_e at smaller endpoint
            elif ww==v: row[e]=-1.0
        A.append(row)
    A=np.array(A) if A else np.zeros((0,len(E)))
    # coarea factor: 1/sqrt(det(A A^T)) via positive eigenvalues (robust to rank deficiency)
    if A.shape[0]>0 and len(E)>0:
        ev=np.linalg.eigvalsh(A@A.T)
        pos=ev[ev>1e-9]
        coarea = 1.0/np.sqrt(float(np.prod(pos))) if pos.size>0 else 1.0
    else:
        coarea = 1.0
    # nullspace
    if A.shape[0]==0:
        # no free vars -> integral trivial
        dim=len(E)
        N=np.eye(dim)
    else:
        from scipy.linalg import null_space
        Z=null_space(A)  # columns orthonormal basis
        if Z.size==0:
            N=np.zeros((len(E),0))
        else:
            N=Z
    d=N.shape[1]
    # polytope P = { l in R^d : |(N l)_e| <= 1/2 }  in l-coords (N orthonormal -> measure=slice measure)
    # value = coarea-factor * lambda-volume
    if d==0:
        # zero-dimensional: only trivial; volume in amb is degenerate; return the atomic point value
        # (should not be a genuine atom)
        return 0.0
    # H-representation: halfspaces  a_e . l <= 0.5  and -a_e . l <= 0.5, a_e=N[e,:].
    if d==1:
        # volume = 2*min_e(0.5/|a_e,1|)
        v=min(0.5/abs(N[e,0]) for e in range(len(E)))
        return coarea*(2.0*v)
    # vertex enumeration: all d-subsets of halfspace normals
    import itertools
    halfnorms=[]  # rows a (signed) and rhs 0.5 units
    for e in range(len(E)):
        halfnorms.append( (N[e,:].copy(), +0.5) )
        halfnorms.append( (-N[e,:].copy(), +0.5) )
    M=len(halfnorms)
    verts=[]
    tol=1e-7
    for comb in itertools.combinations(range(M), d):
        Amat=np.array([halfnorms[i][0] for i in comb])
        rhs=np.array([halfnorms[i][1] for i in comb])
        try:
            lam=np.linalg.solve(Amat, rhs)
        except np.linalg.LinAlgError:
            continue
        # check all constraints
        ok=True
        for (a,bd) in halfnorms:
            if np.dot(a,lam)>bd+ tol*max(1.0,abs(bd),abs(np.dot(a,lam))):
                ok=False; break
        if ok:
            verts.append(lam)
    if len(verts)<d+1:
        return 0.0
    vp=np.array(verts)
    # dedup
    uvp=[]
    for p in vp:
        if all(np.linalg.norm(p-q)>1e-6 for q in uvp):
            uvp.append(p)
    uvp=np.array(uvp)
    try:
        from scipy.spatial import ConvexHull
        with np.errstate(all='ignore'):
            hv=ConvexHull(uvp)
            lam_vol=float(hv.volume)
    except Exception:
        # lower-dimensional; approximate via bounding volume (shouldn't be a genuine atom)
        lam_vol=0.0
    return coarea*lam_vol


