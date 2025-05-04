import glob
import os

import pandas as pd
import numpy as np
import itertools as it

# ==========================================================================================================================================
# Alignment and Tree Error Dataframe
# Col:  [0] Dataset     [1] Replicate  [2] Method   [3] Iteration   [4] SPFN    [5] SPFP
# ==========================================================================================================================================

## find all output alignments 

home = os.path.expanduser("~")
pattern = os.path.join(home, "project", "output", "E2", "**", "align.fasta")
files = glob.glob(pattern, recursive = True)

# # ====== get the accuracy results and write into Error.csv ============
# data = []
# for file in files:
#     filename = file.split("/")
#     dataset = filename[6]
#     replicate = filename[7]
#     method = "-".join(filename[8:-1])
# 
#     # get the iteration
#     iteration = -1
#     if "magus" in method:
#         iteration = int(str(os.path.dirname(file))[-1])
# 
#     # get the error data
#     if "iter0" in os.path.dirname(file):
#         continue
# 
#     error = os.path.join(os.path.dirname(file), "error.txt")
#     with open(error) as err:
#         lines = err.readlines()
#         spfn = float(lines[2].split(" ")[1])
#         spfp = float(lines[3].split(" ")[1])
# 
#     data.append([dataset, replicate, method, iteration, spfn, spfp])
# 
# df = pd.DataFrame(data, columns = ["Dataset", "Replicate", "Method", "Iteration", "SPFN", "SPFP"])
# df.to_csv("Error.csv", index=False, float_format='%.4f')
# 
# # ====== get the general timing results and write into Timing.csv ============
# data = []
# for file in files:
#     timing = os.path.join(os.path.dirname(file), "timing.txt")
#     filename = file.split("/")
#     dataset = filename[6]
#     replicate = filename[7]
#     method = "-".join(filename[8:-1])
# 
#     try:
#         iteration = int(str(os.path.dirname(file))[-1])
#     except Exception:
#         iteration = -1
# 
#     with open(timing) as time:
#         lines = time.readlines()
# 
#         # add the time to do the alignment
#         if iteration != 0:
#             runtime = float(lines[1].split(" ")[0])
# 
#         # add the time to do the guide tree estimation
#         if ("magus_clustalo" in method or "magus_magus" in method) and iteration != 4 and iteration != 0:
#             runtime += float(lines[3].split(" ")[0])
#         elif ("magus_clustalo" in method or "magus_magus" in method) and iteration == 0:
#             runtime += float(lines[-1].split(" ")[0])
#         elif "magus_default" in method:
#             runtime += float(lines[-1].split(" ")[0])
# 
#     data.append([dataset, replicate, method, iteration, runtime])
# 
# # for all magus iter 1, 2, 3, 4: add the prior runtime
# for j, (d, r, m, i, t) in enumerate(data):
#     if i < 1:
#         continue
# 
#     # find the row with (d, r, m, i - 1, t')
#     # add t' to t
#     for (v, w, x, y, z) in data:
#         if v != d or w != r or x[:-1] != m[:-1] or y != (i - 1):
#             continue
#         data[j][4] += z
#         break
# 
# df = pd.DataFrame(data, columns = ["Dataset", "Replicate", "Method", "Iteration", "Runtime"])
# df.to_csv("Timing.csv", index=False, float_format='%.4f')

# ====== get the magus specific timing results and write into MagusTiming.csv ============
data = []
for file in files:
    filename = file.split("/")
    dataset = filename[6]
    replicate = filename[7]
    method = "-".join(filename[8:-1])
    timing = os.path.join(os.path.dirname(file), "timing.txt")

    if "magus" not in method:
        continue

    iteration = int(str(os.path.dirname(file))[-1])
    with open(timing) as time:
        lines = time.readlines()

        # time for initial tree
        if iteration == 0:
            runtime = float(lines[-1].split(" ")[0])
            data.append([dataset, replicate, method + "initi", iteration, runtime])
            continue
        
        # time for alignment 
        runtime = float(lines[1].split(" ")[0])
        data.append([dataset, replicate, method, iteration, runtime])

        # time for guide tree (if not final)
        if ("magus_default" in method and iteration != 1) or ("magus_magus" in method and iteration != 4) or ("magus_clustalo" in method and iteration != 4):
            runtime = float(lines[-1].split(" ")[0])
            data.append([dataset, replicate, method + "guide", iteration, runtime])

# for all magus iter 1, 2, 3, 4: add the prior runtime
for j, (d, r, m, i, t) in enumerate(data):
    if "initi" in m:
        continue

    if "guide" in m:
        # find the alignment time for prev iteration
        for (v, w, x, y, z) in data:
            if v != d or w != r or x != m[:-5]:
                continue
            data[j][4] += z
            break
        continue
    
    # find the guide tree time for prev iteration
    for (v, w, x, y, z) in data:
        if v != d or w != r or ("guide" not in x and "initi" not in x) or x[:-6] != m[:-1] or y != (i - 1):
            continue
        data[j][4] += z
        break

df = pd.DataFrame(data, columns = ["Dataset", "Replicate", "Method", "Iteration", "Runtime"])
df.to_csv("MagusTiming.csv", index=False, float_format='%.4f')
