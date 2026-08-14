"""Parallel k-point pressure certificate: split the top-level boxes across
worker processes (embarrassingly parallel: each initial box is an independent
branch-and-bound search; node/split/prune counts sum).

Same contract as verify_kpoint.py but uses multiprocessing.Pool over the
initial product boxes. Grid/precision must be justified in the paper trail.
"""
from __future__ import annotations
import argparse, itertools, math, os, sys, time
from multiprocessing import Pool, cpu_count
from typing import List, Optional, Sequence, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
    *(['..']*5), 'literature','raw','zeta-simple-zeros','src'))

from zeta_simple_zeros.kernel import (
    RangeMinimum, build_kernel_table, build_second_derivative_lower_table,
    kernel_constants, squared_kernel_derivatives, table_sha256)
from zeta_simple_zeros.report import VerificationReport
from zeta_simple_zeros.rounding import down_add, down_mul, down_ratio, up_ratio

# ---------------------------------------------------------------------------
# Worker: process a contiguous slice of the initial-box list, return partial tallies.
# We pass the prebuilt tables + constants via globals set by an initializer.
# ---------------------------------------------------------------------------
_worker = {}

def _init(k, grid, precision, target_n, target_d, second_start):
    from flint import fmpq
    d = k-1
    P_DEN = 500*d
    cutoff = int(math.floor((target_n/target_d)*P_DEN*grid))+8
    table = build_kernel_table(grid, cutoff, precision)
    ranges = RangeMinimum(table)
    second = build_second_derivative_lower_table(grid, cutoff, start_index=second_start, precision=precision)
    second_ranges = RangeMinimum(second)
    constants = kernel_constants()
    COEFF = {r: math.nextafter(2.0/(k-r), -math.inf) for r in range(1, d+1)}
    COEFF_UP = {r: math.nextafter(2.0/(k-r), math.inf) for r in range(1, d+1)}
    COEFF_RAT = {r: fmpq(2, k-r) for r in range(1, d+1)}
    _worker.update(dict(k=k, d=d, P_DEN=P_DEN, grid=grid, precision=precision,
        target_n=target_n, target_d=target_d, cutoff=cutoff, table=table,
        ranges=ranges, second_ranges=second_ranges, constants=constants,
        second_table=second, COEFF=COEFF, COEFF_UP=COEFF_UP,
        COEFF_RAT=COEFF_RAT, target_upper=up_ratio(target_n,target_d)))

# A box search running on a worker process (globals set by _init).
def _process_slice(args):
    boxes, use_tangent = args
    w = _worker
    d = w['d']; P_DEN=w['P_DEN']; grid=w['grid']
    target_upper=w['target_upper']
    ranges=w['ranges']; second_ranges=w['second_ranges']
    constants=w['constants']; table=w['table']
    COEFF=w['COEFF']; COEFF_UP=w['COEFF_UP']; COEFF_RAT=w['COEFF_RAT']
    target_n=w['target_n']; target_d=w['target_d']
    from flint import arb, fmpq

    def kernel_min(left,right):
        if right>=ranges.length: return 0.0
        return ranges.query(left,right)
    def second_min(left,right):
        if right>=second_ranges.length: return float("-inf")
        return second_ranges.query(left,right)
    def box_lower(box):
        lows=[p[0] for p in box]; highs=[p[1] for p in box]
        lp=[0]; hp=[0]
        for lo,hi in zip(lows,highs):
            lp.append(lp[-1]+lo); hp.append(hp[-1]+hi)
        result=down_ratio(lp[-1], grid*P_DEN)
        for span in range(1,d+1):
            coef=COEFF[span]
            for start in range(d-span+1):
                L=lp[start+span]-lp[start]
                R=hp[start+span]-hp[start]+span-1
                result=down_add(result, down_mul(coef, kernel_min(L,R)))
        return result
    def coeff_signed(span, lower):
        if lower==float("-inf"): return lower
        coef=COEFF[span] if lower>=0.0 else COEFF_UP[span]
        return math.nextafter(coef*lower, -math.inf)
    def in_heuristic(matrix):
        n=d; lower=[[0.0]*n for _ in range(n)]; diag=[0.0]*n
        for col in range(n):
            pivot=matrix[col][col]
            for pr in range(col): pivot-=lower[col][pr]*lower[col][pr]*diag[pr]
            if pivot<=1e-12: return False
            diag[col]=pivot; lower[col][col]=1.0
            for row in range(col+1,n):
                v=matrix[row][col]
                for pr in range(col): v-=lower[row][pr]*lower[col][pr]*diag[pr]
                lower[row][col]=v/pivot
        return True
    def exf(v):
        num,den=v.as_integer_ratio(); return arb(fmpq(num,den))
    def arb_PD(terms):
        n=d; mat=[[arb(0) for _ in range(n)] for _ in range(n)]
        for start,span,coef in terms:
            ex=exf(coef)
            for r in range(start,start+span):
                for c in range(start,start+span): mat[r][c]+=ex
        lo=[[arb(0) for _ in range(n)] for _ in range(n)]; diag=[arb(0) for _ in range(n)]
        for col in range(n):
            lo[col][col]=arb(1); pivot=mat[col][col]
            for pr in range(col): pivot-=lo[col][pr]*lo[col][pr]*diag[pr]
            if not (pivot>0): return False
            diag[col]=pivot
            for row in range(col+1,n):
                v=mat[row][col]
                for pr in range(col): v-=lo[row][pr]*lo[col][pr]*diag[pr]
                lo[row][col]=v/pivot
        return True
    def tangent(box):
        if not use_tangent: return None
        lows=[p[0] for p in box]; highs=[p[1] for p in box]
        lp=[0]; hp=[0]
        for lo,hi in zip(lows,highs): lp.append(lp[-1]+lo); hp.append(hp[-1]+hi)
        terms=[]; heur=[[0.0]*d for _ in range(d)]
        for span in range(1,d+1):
            for start in range(d-span+1):
                L=lp[start+span]-lp[start]; R=hp[start+span]-hp[start]+span-1
                s=coeff_signed(span, second_min(L,R))
                if s==float("-inf"): return None
                terms.append((start,span,s))
                for r in range(start,start+span):
                    for c in range(start,start+span): heur[r][c]+=s
        if not in_heuristic(heur): return None
        if not arb_PD(terms): return None
        mids=[fmpq(lo+hi+1,2*grid) for lo,hi in box]
        radii=[fmpq(hi-lo+1,2*grid) for lo,hi in box]
        value=sum((arb(p) for p in mids), arb(0))/P_DEN
        grad=[arb(fmpq(1,P_DEN)) for _ in range(d)]
        for span in range(1,d+1):
            coef=arb(COEFF_RAT[span])
            for start in range(d-span+1):
                pt=sum(mids[start:start+span], fmpq(0))
                pot,drv,_=squared_kernel_derivatives(arb(pt), constants)
                value+=coef*pot
                for cc in range(start,start+span): grad[cc]+=coef*drv
        lower=value
        for drv,rad in zip(grad,radii): lower-=drv.abs_upper()*arb(rad)
        return lower

    stack=[(box,0) for box in boxes]
    nodes=pruned=splits=maxd=0; pp=ip=tp=0
    while stack:
        box,depth=stack.pop()
        nodes+=1
        if depth>maxd: maxd=depth
        if sum(p[0] for p in box)>=w['cutoff']:
            pruned+=1; pp+=1; continue
        lower=box_lower(box)
        if lower>=target_upper:
            pruned+=1; ip+=1; continue
        tg=tangent(box)
        if tg is not None and tg>=arb(fmpq(target_n,target_d)):
            pruned+=1; tp+=1; continue
        widths=[r-l for l,r in box]
        if max(widths)==0:
            return dict(fail=True, box=box, lower=lower.hex())
        splits+=1
        ci=max(range(d), key=widths.__getitem__)
        L,R=box[ci]; mid=(L+R)//2
        lo=list(box); hi=list(box)
        lo[ci]=(L,mid); hi[ci]=(mid+1,R)
        stack.append((tuple(lo),depth+1)); stack.append((tuple(hi),depth+1))
    return dict(fail=False, nodes=nodes, pruned=pruned, splits=splits,
                max_depth=maxd, pp=pp, ip=ip, tp=tp)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('k',type=int)
    ap.add_argument('target')
    ap.add_argument('--grid',type=int,default=2000)
    ap.add_argument('--precision',type=int,default=128)
    ap.add_argument('--no-tangent',action='store_true')
    ap.add_argument('--workers',type=int,default=cpu_count())
    ap.add_argument('--out',type=str,default=None,
                    help='write the certificate report to this file (atomic write on success)')
    args=ap.parse_args()
    k=args.k; d=k-1; P_DEN=500*d
    tn,td=args.target.split('/'); target_n=int(tn); target_d=int(td)
    grid=args.grid
    cutoff=int(math.floor((target_n/target_d)*P_DEN*grid))+8
    second_start=min(int(0.95*grid), cutoff-2)
    # build components in a throwaway process is awkward; we need a table to find
    # surviving cells. Build table here (cheap) for component discovery, then pass
    # (rebuilt) to workers.
    table0=build_kernel_table(grid, cutoff, args.precision)
    target_upper=up_ratio(target_n,target_d)
    coeff1=down_ratio(2,d)
    surv=[]
    for idx in range(cutoff):
        ub=down_ratio(idx, grid*P_DEN)
        ub=down_add(ub, down_mul(coeff1, table0[idx]))
        if ub<target_upper: surv.append(idx)
    comps=[]
    for idx in surv:
        if not comps or idx>comps[-1][1]+1: comps.append([idx,idx])
        else: comps[-1][1]=idx
    comps=[(c[0],c[1]) for c in comps]
    boxes=[tuple(parts) for parts in itertools.product(comps, repeat=d)]
    initial=len(boxes)
    start=time.perf_counter()
    workers=min(args.workers, len(boxes))
    # Slice boxes for workers
    chunks=[boxes[i::workers] for i in range(workers)]
    with Pool(workers, initializer=_init,
              initargs=(k, grid, args.precision, target_n, target_d, second_start)) as pool:
        res=pool.map(_process_slice, [(ch,not args.no_tangent) for ch in chunks])
    fail=[r for r in res if r['fail']]
    if fail:
        print("FAILED at", fail[0]); sys.exit(2)
    nodes=sum(r['nodes'] for r in res); pruned=sum(r['pruned'] for r in res)
    splits=sum(r['splits'] for r in res); maxd=max(r['max_depth'] for r in res)
    pp=sum(r['pp'] for r in res); ip=sum(r['ip'] for r in res); tp=sum(r['tp'] for r in res)
    elapsed=time.perf_counter()-start
    comp_text=";".join(f"[{a},{b}]" for a,b in comps)
    second_table0=build_second_derivative_lower_table(grid,cutoff,second_start,args.precision)
    rep=VerificationReport(
        certificate=f"{k}-point", verified=True,
        target=f"F{d} >= {target_n}/{target_d}", grid=grid,
        precision_bits=args.precision,
        kernel_table_sha256=table_sha256(table0), nodes=nodes, pruned=pruned,
        splits=splits, maximum_depth=maxd, initial_boxes=initial,
        elapsed_seconds=elapsed,
        details={'k':k,'pressure_pruned':pp,'interval_pruned':ip,'tangent_pruned':tp,
                 'surviving_gap_components_cells':comp_text,
                 'surviving_gap_components_count':len(comps),
                 'workers':workers,
                 'second_derivative_table_sha256':table_sha256(second_table0)})
    print(rep.to_text())
    if args.out:
        import tempfile
        od = os.path.dirname(os.path.abspath(args.out)) or '.'
        os.makedirs(od, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=od, suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as fh:
                fh.write(rep.to_text())
            os.replace(tmp, args.out)
        except BaseException:
            try: os.unlink(tmp)
            except OSError: pass
            raise
        print("written:", args.out)

if __name__=='__main__':
    main()
