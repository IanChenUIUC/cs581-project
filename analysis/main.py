# ==========================================================================================================================================
# Alignment and Tree Error Dataframe (Wide Data Format)
# Col:  [0]Iteration   [1]Subset_Size   [2]Initial_Method       [3]GuideTree_Method [4]RFFN     [5]RFFP     [6]SPFN     [7]SPFP      
# Val:      {1-4}           {10-200}        {clustalo, magus}       {ft, ftnoml}        {0-1}       {0-1}       {0-1}       {0-1}
# ==========================================================================================================================================

import pandas as pd
import numpy as np
import itertools as it
import os

# iterations  = [1, 2, 3, 4]
iterations  = [1, 2, 3]
subsets     = [10, 25, 50, 100, 200]
initial     = ["magus", "clustalo"]
guide       = ["ft", "ftnoml"]

num_replicates = 5

data = {}
data["Iteration"] = []
data["Subset_Size"] = []
data["Initial_Method"] = []
data["GuideTree_Method"] = []
data["RFFN"] = []
data["RFFP"] = []
data["SPFN"] = []
data["SPFP"] = []

for (i, s, t, g) in it.product(iterations, subsets, initial, guide):
    spfn, spfp, rffn, rffp = 0, 0, 0, 0
    for r in range(3, 4):
        sp = f"~/project/output/E1/R{r}/iter{i}/{t}_{s}_{g}_sp.txt"
        if i == 1:
            rf = f"~/project/output/E1/R{r}/iter{i}/{t}_rf.csv"
        else:
            rf = f"~/project/output/E1/R{r}/iter{i}/{t}_{s}_{g}_rf.csv"

        with open(os.path.expanduser(sp), "r") as f:
            lines = f.readlines()
            spfn += float(lines[2].split(" ")[1])
            spfp += float(lines[3].split(" ")[1])

        with open(os.path.expanduser(rf), "r") as f:
            lines = f.readlines()
            rffn += float(lines[1].split(",")[0])
            rffn += float(lines[1].split(",")[1])

    data["Iteration"].append(i)
    data["Subset_Size"].append(s)
    data["Initial_Method"].append(t)
    data["GuideTree_Method"].append(g)
    data["RFFN"].append(rffn)
    data["RFFP"].append(rffp)
    data["SPFN"].append(spfn)
    data["SPFP"].append(spfp)

df = pd.DataFrame.from_dict(data)
print(df.head())
df.to_csv("Results.csv", index=False, float_format='%.4f')
