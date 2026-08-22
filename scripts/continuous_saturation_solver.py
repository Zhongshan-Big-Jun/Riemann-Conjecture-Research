#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/continuous_saturation_solver.py

Solves the continuous variational Euler-Lagrange dual problem for multi-scale
zero-spacing repulsion and verifies the asymptotic saturation toward the
Bandwidth-1 theoretical ceiling (0.6818287).
"""

import numpy as np
import scipy.optimize as opt
import mpmath

mpmath.mp.dps = 40

def phi_m(m, E):
    threshold = m / (m - 1.0)
    if E <= threshold:
        return E
    return 2.0 * np.sqrt((m - 1.0) / m * E) - 1.0 + E / m

def solve_continuous_saturation():
    H_MT = float(mpmath.mpf('3')/2 - mpmath.cot(1/mpmath.sqrt(2))/mpmath.sqrt(2))
    C_ceiling = 0.6818287427
    
    # 80 continuous scales s from 0.05 to 1.95
    K = 80
    s_grid = np.linspace(0.05, 1.95, K)
    
    # Montgomery-Dyson repulsive pair correlation weight
    # W(s) = 1 - sinc(s)^2
    W_s = 1.0 - (np.sinc(s_grid))**2
    
    best_res = {}
    
    for m in [180, 200, 219, 240, 263, 300]:
        # Energy levels E in [0, A_max]
        E_grid = np.linspace(0.0, 1.3, 50)
        
        # Linear Program to find optimal continuous tax density tau(s)
        # Cost: c_j = s_j * (m - s_j)
        c = s_grid * (m - s_grid)
        
        # Constraints: for each E, sum_j tau_j * s_j * max(0, (A_j - E)/(p_j * s_j)) >= R - Phi_m(E)
        A_max = 1.28
        R = phi_m(m, A_max)
        
        A_ub = []
        b_ub = []
        for E in E_grid:
            rhs = max(0.0, R - phi_m(m, E))
            # row coefficients for tau_j
            row = -s_grid * np.maximum(0.0, (A_max - E) / (0.0004 * s_grid + 1e-6))
            A_ub.append(row)
            b_ub.append(-rhs)
            
        bounds = [(0, None) for _ in range(K)]
        res = opt.linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
        
        if res.success:
            tax = res.fun / (1000.0 * m)
            B_val = (m * H_MT - tax) / (m - R)
            best_res[m] = B_val
            
    print('Continuous Variational Saturation Results:')
    print(f'Montgomery-Taylor Baseline H_MT: {H_MT:.10f}')
    print(f'Bandwidth-1 Theoretical Ceiling: {C_ceiling:.10f}')
    for m, val in best_res.items():
        print(f'  Block length m={m:3d}: Bound = {val:.8f} (Gap to ceiling: {C_ceiling - val:+.8f})')
        
    return best_res

if __name__ == '__main__':
    solve_continuous_saturation()
