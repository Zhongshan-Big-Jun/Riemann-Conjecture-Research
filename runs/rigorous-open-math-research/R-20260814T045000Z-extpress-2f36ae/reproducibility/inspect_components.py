"""Inspect one-body surviving components and initial-box count for general k."""
import sys, os
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    *(['..']*5), 'literature','raw','zeta-simple-zeros','src'))
from zeta_simple_zeros.kernel import build_kernel_table, kernel_constants
from zeta_simple_zeros.rounding import down_ratio, down_add, down_mul, up_ratio
import math

def components_for(k, target_n, target_d, grid=4000, precision=128):
    d=k-1
    P_DEN=500*d
    cutoff=int(math.floor((target_n/target_d)*P_DEN*grid))+8
    table=build_kernel_table(grid, cutoff, precision)
    coeff1=down_ratio(2, d)  # 2/(k-1) span-1
    tu=up_ratio(target_n, target_d)
    surv=[]
    for idx in range(int(cutoff)):
        ub=down_ratio(idx, grid*P_DEN)
        ub=down_add(ub, down_mul(coeff1, table[idx]))
        if ub < tu:
            surv.append(idx)
    comps=[]
    for idx in surv:
        if not comps or idx>comps[-1][1]+1:
            comps.append([idx,idx])
        else:
            comps[-1][1]=idx
    comps=[(c[0],c[1]) for c in comps]
    return comps, cutoff, table

for (k,tnd) in [(7,(19,5000)),(9,(19,5000)),(9,(20,5000)),(9,(21,5000)),
                (9,(25,6000)), (9,(4,1000)), (9,(39,10000))]:
    comps, cutoff, table = components_for(k, tnd[0], tnd[1])
    nc=len(comps)
    print(f"k={k} target={tnd[0]}/{tnd[1]} ({tnd[0]/tnd[1]:.7f}): "
          f"cutoff_cells={cutoff} components={nc} -> initial_boxes={nc**(k-1)}")
    print(f"   comps (cells): {comps}")
# also show w values near the components to understand
print("\nw(lower of cell) at a few cells:")
tab=build_kernel_table(4000, 45610, 128)
for cell in [900, 1100, 3800, 4200, 6000, 8000, 10000, 16000]:
    print(f"  cell {cell} (x~{cell/4000:.3f}) w_lower={tab[cell]:.6f}")
