#!/usr/bin/env python
"""b=2 shapes for k=6 reduce analytically to J = c_m - c_{m+2}, m = #cycle block-crossings.
Verified exactly against the box-spline engine on a sample. Sums the 31 b=2 partitions exactly.
Result: m_6^{b=2} = 4297/630; m_6^{b<=2} = 4927/630 (with b=1 -> 1)."""
from fractions import Fraction as F
from collections import defaultdict
from math import comb, factorial

# exact c_{2n} = B_{2n}(0) = 1/(2n-1)! sum_{k=0}^{n-1} (-1)^k C(2n,k)(n-k)^{2n-1}
def c_2n(n):
    m = 2 * n
    s = 0
    for k in range(n):
        s += (-1) ** k * comb(m, k) * (n - k) ** (m - 1)
    return F(s, factorial(m - 1))

C = {2: c_2n(1), 4: c_2n(2), 6: c_2n(3), 8: c_2n(4), 10: c_2n(5), 12: c_2n(6)}
print("c_2n values:")
for key in sorted(C):
    print(f"  c_{key} = {C[key]} = {float(C[key]):.12f}")
print("\nc_12 =", C[12], "= 655177/1663200 ?", C[12] == F(655177, 1663200))


def partitions_of(n):
    def rec(i, blocks):
        if i == n:
            yield tuple(frozenset(b) for b in blocks)
            return
        seen = set()
        for j, bb in enumerate(blocks):
            key = frozenset(bb)
            if key in seen:
                continue
            seen.add(key)
            b2 = [x for x in blocks]
            b2[j] = bb | {i}
            yield from rec(i + 1, b2)
        yield from rec(i + 1, blocks + [frozenset([i])])
    return list(rec(1, [frozenset([0])]))


def cross_edges(blocks, k=6):
    bid = {}
    for i, b in enumerate(blocks):
        for e in b:
            bid[e] = i
    idx = [bid[a] for a in range(k)]
    return sum(1 for a in range(k) if idx[a] != idx[(a + 1) % k])


def main():
    parts = [list(bl) for bl in partitions_of(6) if len(bl) == 2]
    bym = defaultdict(lambda: [0, F(0)])   # m -> (count, sum-of-J)
    for bl in parts:
        m = cross_edges(bl)
        J = C[m] - C[m + 2]
        assert m in (2, 4, 6), m
        bym[m][0] += 1
        bym[m][1] += J
    total = F(0)
    print(f"\nb=2 partitions for k=6: {len(parts)}")
    for m in sorted(bym):
        cnt, s = bym[m]
        print(f"  m={m}: count={cnt} J_per_part={C[m]-C[m+2]} sum={s}")
        total += s
    print(f"m_6^(b=2) = {total} = {float(total):.9f}")
    print(f"m_6^(b<=2) = {1 + total} = {float(1 + total):.9f}   (b=1 contribution = 1)")
    assert total == F(4297, 630)

main()
