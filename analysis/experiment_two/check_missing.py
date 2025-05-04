import glob
import os

import pandas as pd
import numpy as np
import itertools as it

# datasets
datasets = ["16S.3", "16S.B.ALL", "16S.M", "16S.T", "RNASim-1000", "RNASim-10000", "ROSE-1000L1", "ROSE-1000L2", "ROSE-1000L3", "ROSE-1000M2", "ROSE-1000M3"]
replicas = [1,      1,          1,          1,      10,             10,             10,             10,             10,         10,             10          ]

# magus variants
magus = ["magus_default", "magus_magus", "magus_clustalo"]
iters = [2,                 5,              5           ]

# all methods (besides pasta)
# methods = ["clustalo", "mafft", "muscle", "pasta/iter3"]
methods = ["clustalo", "mafft", "muscle"]
for m, i in zip(magus, iters):
    for i in range(i):
        methods.append(f"{m}/iter{i}")

base = os.path.join(os.path.expanduser("~"), "project", "output", "E2")
for (d, r), m in it.product(zip(datasets, replicas), methods):
    for r in range(r):
        cur = os.path.join(base, d, f"R{r}", m, "align.fasta")
        if not os.path.exists(cur):
            print(f"MISSING {d}/R{r}/{m}")
