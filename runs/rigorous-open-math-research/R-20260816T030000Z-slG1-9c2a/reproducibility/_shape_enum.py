"""Analyze the shape structure for each set partition of {0..k-1} in the tr(G^k)
trace moment. Prints, for each partition pi with b blocks:
  - the block list
  - the cycle edge endpoint labels (block id per position)
  - loop edges (same block on both ends -> factor K(0)=1)
  - the line-graph degree of each block (counting distinct line connections)
  - an estimate of how it reduces (degree>=3 => star-type).
This is a PRE-CURSOR to the exact integral; no numerics here.
"""
import itertools
from collections import Counter
import sys

def partitions(n):
    def rec(i, blocks):
        if i == n:
            yield tuple(frozenset(b) for b in blocks)
            return
        for idx,b in enumerate(blocks):
            b2=[x for x in blocks]; b2[idx]=b|{i}
            yield from rec(i+1,b2)
        yield from rec(i+1,blocks+[frozenset([i])])
    yield from rec(1,[frozenset([0])])

def blockid(pos, blocks):
    for i,blk in enumerate(blocks):
        if pos in blk: return i
    raise ValueError

def shape_info(k, blocks):
    b=len(blocks); nblk={p:blockid(p,blocks) for p in range(k)}
    edges=[]  # (bi,bj) for each cycle edge a->a+1
    loops=0
    for a in range(k):
        i=nblk[a]; j=nblk[(a+1)%k]
        if i==j: loops+=1
        else: edges.append((i,j))
    # line adjacency counts (multiset of endpoints per block)
    deg=Counter()
    for (i,j) in edges:
        deg[i]+=1; deg[j]+=1
    # determinant rho_b: det over b blocks (b distinct points)
    return b, loops, edges, deg

if __name__=="__main__":
    k=int(sys.argv[1]) if len(sys.argv)>1 else 5
    allp=list(partitions(k))
    print(f"k={k}: {len(allp)} set partitions")
    groups={}
    for blocks in allp:
        b,loops,edges,deg=shape_info(k,blocks)
        # canonical signature: sizes of blocks + degree count
        sizes=sorted(len(x) for x in blocks)
        sig=(tuple(sizes), tuple(sorted(edges)))
        groups.setdefault(sig,[]).append((blocks,deg))
    print(f"distinct (size-sig, edge-set) shapes: {len(groups)}")
    for sig,items in groups.items():
        sizes,edges=sig
        blocks,deg=items[0]
        star=[i for i in range(len(deg)) if deg[i]>=3 and edges.count(i)>=0] 
        print(f"  sizes={sizes} edges={edges} deg={dict(deg)} n=({len(items)})")
    print("total multiplicities sum:", sum(len(g) for g in groups.values()))
