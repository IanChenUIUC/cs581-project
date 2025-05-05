# ==========================================================================================================================================
# Alignment and Tree Error Dataframe (Wide Data Format)
# Col:  [0]Iteration   [1]Subset_Size   [2]Initial_Method       [3]GuideTree_Method [4]RFFN     [5]RFFP     [6]SPFN     [7]SPFP      [8]Runtime         [9-12]StdDev
# Val:      {1-4}           {10-200}        {clustalo, magus}       {ft, ftnoml}        {0-1}       {0-1}       {0-1}       {0-1}           {seconds}       
# ==========================================================================================================================================

import pandas as pd
import numpy as np
import itertools as it
from datetime import datetime
import os

iterations  = [1, 2, 3, 4]
subsets     = [10, 25, 50, 100, 200]
initial     = ["magus", "clustalo"]
guide       = ["ft", "ftnoml"]

num_replicates = 10

data = {}
data["Iteration"] = []
data["Subset_Size"] = []
data["Initial_Method"] = []
data["GuideTree_Method"] = []
data["RFFN"] = []
data["RFFP"] = []
data["SPFN"] = []
data["SPFP"] = []
data["Runtime"] = []
data["Replicate"] = []

def search(l, s):
    # searches the list until it finds a line containing s
    # then returns the line afterwards
    for i in range(0, len(l), 3):
        if s in l[i]:
            return l[i+1]

def get_elapsed_time(l):
    s = l.split(" ")[2][:-7]
    dec = int(s.split(".")[1])
    second = int(s.split(".")[0].split(":")[1])
    minute = int(s.split(".")[0].split(":")[0])
    return minute * 60 + second

for (s, t, g) in it.product(subsets, initial, guide):
    # runtime[iteration][replicate]
    runtime = []

    for i in iterations:
        runtime.append([])

        for r in range(0, num_replicates):
            time = f"~/project/output/E1/R{r}/iter{i}/timing.txt"
            with open(os.path.expanduser(time)) as f:
                lines = f.readlines()

                # if i == 1, get the initial tree time
                # if i != 1, get the guide tree time
                rt = 0
                if i == 1:
                    line = search(lines, f"{t}_guide.tree")
                    rt += get_elapsed_time(line)
                    line = search(lines, f"{t}_{s}_ft_aln.fasta")
                    rt += get_elapsed_time(line)
                else:
                    line = search(lines, f"{t}_{s}_{g}_guide.tree")
                    rt += get_elapsed_time(line)
                    line = search(lines, f"{t}_{s}_{g}_aln.fasta")
                    rt += get_elapsed_time(line)
                runtime[-1].append(rt)

            sp = f"~/project/output/E1/R{r}/iter{i}/{t}_{s}_{g}_sp.txt"
            if i == 1:
                rf = f"~/project/output/E1/R{r}/iter{i}/{t}_rf.csv"
            else:
                rf = f"~/project/output/E1/R{r}/iter{i}/{t}_{s}_{g}_rf.csv"

            with open(os.path.expanduser(sp), "r") as f:
                lines = f.readlines()
                data["SPFN"].append(float(lines[2].split(" ")[1]))
                data["SPFP"].append(float(lines[3].split(" ")[1]))

            with open(os.path.expanduser(rf), "r") as f:
                lines = f.readlines()
                data["RFFN"].append(float(lines[1].split(",")[0]))
                data["RFFP"].append(float(lines[1].split(",")[1]))

            data["Iteration"].append(i)
            data["Subset_Size"].append(s)
            data["Initial_Method"].append(t)
            data["GuideTree_Method"].append(g)
            data["Runtime"].append(sum(runtime[j][r - 1] for j in range(i)))
            data["Replicate"].append(r)

df = pd.DataFrame.from_dict(data)
df.to_csv("Results.csv", index=False, float_format='%.4f')
