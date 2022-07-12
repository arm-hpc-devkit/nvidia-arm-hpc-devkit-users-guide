#!/usr/bin/env python3
#
# John Linford <john.linford@arm.com>
#

import os
import math
import multiprocessing


# Fraction of node memory to use
_MEMORY_FRACTION = 0.9

# Matrix element size in bytes
_SIZEOF_ELEMENT = 8

_TEMPLATE = """\
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any) 
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
%(N)d         Ns
1            # of NBs
%(NB)d           NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
%(P)d            Ps
%(Q)d            Qs
16.0         threshold
1            # of panel fact
2            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
1            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
##### This line (no. 32) is ignored (it serves as a separator). ######
0                               Number of additional problem sizes for PTRANS
1200 10000 30000                values of N
0                               number of additional blocking sizes for PTRANS
40 9 8 13 13 20 16 32 64        values of NB
"""

def int_factor(n):
    p = math.ceil(math.sqrt(n))
    while p:
        q = int(n/p)
        if p*q == n:
            return p, q
        p -= 1
    raise RuntimeError


def int_input(prompt, default=None):
    if default:
        default = str(default)
        val = input("%s [%s]: " % (prompt, default)) or default
    else:
        val = input("%s: " % prompt)
    return int(val)


def get_node_memory():
    try:
        return int((os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')) / (1024*1024))
    except ValueError:
        return 65536


def main():
    default_nodes = 1
    default_cores = multiprocessing.cpu_count()
    default_memory = get_node_memory()
    default_block = 192

    nodes = int_input("Number of nodes", default_nodes)
    cores_per_node = int_input("Cores per node", default_cores)
    memory_per_node = int_input("Memory per node (MB)", default_memory)
    block_size = int_input("Block size", default_block)

    cores = nodes * cores_per_node
    memory = nodes * memory_per_node
    
    N = int((_MEMORY_FRACTION * math.sqrt(memory * 1024**2 / _SIZEOF_ELEMENT)) / block_size) * block_size
    NB = block_size
    P, Q = int_factor(cores)

    fname = "HPL.dat_N%d_NB%d_P%d_Q%d" % (N, NB, P, Q)
    with open(fname, "w") as fout:
        fout.write(_TEMPLATE % {"N": N, "NB": NB, "P": P, "Q": Q})


if __name__ == "__main__":
    main()
