import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from scipy.stats import linregress
import numpy as np
import pandas as pd
import itertools as it
import seaborn as sns

## ===================== draw figures =====================

def figure_one(save = False):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("MAGUS(iter)")

    # fig1a: MAGUS starting tree
    base = df[df["Method"].str.contains("magus_magus")][["Dataset", "SPFN", "SPFN_stderr", "Iteration"]]
    frame = base.pivot(index = "Dataset", columns = "Iteration", values = "SPFN")
    error = base.pivot(index = "Dataset", columns = "Iteration", values = "SPFN_stderr")
    frame.plot(ax = ax1, kind = "bar", xlabel = "Iteration", ylabel = "SPFN", yerr = error, ylim = (0, 0.35), rot = 0)

    # fig1b: ClustalOmega starting tree
    base = df[df["Method"].str.contains("magus_clustalo")][["Dataset", "SPFN", "SPFN_stderr", "Iteration"]]
    frame = base.pivot(index = "Dataset", columns = "Iteration", values = "SPFN")
    error = base.pivot(index = "Dataset", columns = "Iteration", values = "SPFN_stderr")
    frame.plot(ax = ax2, kind = "bar", xlabel = "Iteration", ylabel = "SPFN", yerr = error, ylim = (0, 0.35), rot = 0)

    if save:
        plt.savefig("fig1.pdf")
    else:
        plt.show()

def figure_two(save = False):
    fig, ax = plt.subplots()
    fig.suptitle("MAGUS vs MAGUS")

    base = df[df["Iteration"] >= 1][["Dataset", "SPFN", "SPFN_stderr", "Method"]]
    frame = base.pivot(index = "Dataset", columns = "Method", values = "SPFN")
    error = base.pivot(index = "Dataset", columns = "Method", values = "SPFN_stderr")
    frame.plot(ax = ax, kind = "bar", xlabel = "Method", ylabel = "SPFN", yerr = error, ylim = (0, 0.35), rot = 0)

    if save:
        plt.savefig("fig2.pdf")
    else:
        plt.show()

def figure_three(save = False):
    fig, axes = plt.subplots(1, 3)
    fig.suptitle("MAGUS vs All")

    datasets = ["ROSE", "RNASim"]
    for ax, data in zip(axes, datasets):
        frame = df1[((df1["Iteration"] == 1) | (df1["Iteration"] == 4) | (df1["Iteration"] == -1)) & (df1["Dataset"].str.contains(data))][["Dataset", "SPFN", "Method"]]
        sns.boxplot(ax = ax, x = "Dataset", y = "SPFN", hue = "Method", data = frame)
    base = df[((df["Iteration"] == 1) | (df["Iteration"] == 4) | (df["Iteration"] == -1)) & (df["Dataset"].str.contains("16S"))][["Dataset", "SPFN", "SPFN_stderr", "Method"]]
    frame = base.pivot(index = "Dataset", columns = "Method", values = "SPFN")
    error = base.pivot(index = "Dataset", columns = "Method", values = "SPFN_stderr")
    frame.plot(ax = axes[2], kind = "bar", xlabel = "Method", ylabel = "SPFN", yerr = error, ylim = (0, 1), rot = 0)

    if save:
        plt.savefig("fig3.pdf")
    else:
        plt.show()

def figure_four(save = False):
    fig, ax = plt.subplots()
    fig.suptitle("MAGUS vs All")

    base = df2[(df2["Iteration"] == 1) | (df2["Iteration"] == 4) | (df2["Iteration"] == -1)][["Dataset", "Runtime", "Runtime_stderr", "Method"]]
    frame = base.pivot(index = "Dataset", columns = "Method", values = "Runtime")
    error = base.pivot(index = "Dataset", columns = "Method", values = "Runtime_stderr")
    frame.plot(ax = ax, kind = "bar", xlabel = "Method", ylabel = "Runtime", yerr = error, rot = 0, logy = True)

    if save:
        plt.savefig("fig4.pdf")
    else:
        plt.show()

def figure_five(save = False):
    fig, ax = plt.subplots()
    fig.suptitle("MAGUS vs All")

    base = df4[~df4["Method"].str.contains("magus_default")]
    colors = iter([cm.cool(i) for i in np.linspace(0.05, 0.95, 8)])


    frame = base[(base["Iteration"] == 4) & ~(base["Method"].str.contains("guide"))].pivot(index = "Dataset", columns = "Method", values = "Runtime")
    error = base[(base["Iteration"] == 4) & ~(base["Method"].str.contains("guide"))].pivot(index = "Dataset", columns = "Method", values = "Runtime_stderr")
    frame.plot(ax = ax, kind = "bar", xlabel = "Method", ylabel = "Runtime", yerr = error, rot = 0, logy = False, color = next(colors))

    for i in reversed(range(1, 4)):
        frame = base[(base["Iteration"] == i) & ~(base["Method"].str.contains("guide"))].pivot(index = "Dataset", columns = "Method", values = "Runtime")
        error = base[(base["Iteration"] == i) & ~(base["Method"].str.contains("guide"))].pivot(index = "Dataset", columns = "Method", values = "Runtime_stderr")
        frame.plot(ax = ax, kind = "bar", xlabel = "Method", ylabel = "Runtime", yerr = error, rot = 0, logy = False, color = next(colors))

        frame = base[(base["Iteration"] == i) & (base["Method"].str.contains("guide"))].pivot(index = "Dataset", columns = "Method", values = "Runtime")
        error = base[(base["Iteration"] == i) & (base["Method"].str.contains("guide"))].pivot(index = "Dataset", columns = "Method", values = "Runtime_stderr")
        frame.plot(ax = ax, kind = "bar", xlabel = "Method", ylabel = "Runtime", yerr = error, rot = 0, logy = False, color = next(colors))

    # plot the time for initial method
    frame = base[base["Iteration"] == 0].pivot(index = "Dataset", columns = "Method", values = "Runtime")
    error = base[base["Iteration"] == 0].pivot(index = "Dataset", columns = "Method", values = "Runtime_stderr")
    frame.plot(ax = ax, kind = "bar", xlabel = "Method", ylabel = "Runtime", yerr = error, rot = 0, logy = False, color = next(colors))

    if save:
        plt.savefig("fig5.pdf")
    else:
        plt.show()
 
 
## ===================== prepocess the dataframe =====================

save = False
def stderr(x):
    return x.std() / np.sqrt(len(x))

df1 = pd.read_csv("Error.csv")
df2 = pd.read_csv("Timing.csv")

df = df1.groupby(by = ["Dataset", "Method", "Iteration"]).agg({
    "SPFN": ["mean", stderr],
    "SPFP": ["mean", stderr],
})
df.columns = ["SPFN", "SPFN_stderr", "SPFP", "SPFP_stderr"]
df = df.reset_index()

df2 = df2.groupby(by = ["Dataset", "Method", "Iteration"]).agg({
    "Runtime": ["mean", stderr],
})
df2.columns = ["Runtime", "Runtime_stderr"]
df2 = df2.reset_index()

df4 = pd.read_csv("MagusTiming.csv")
df4 = df4.groupby(by = ["Dataset", "Method", "Iteration"]).agg({
    "Runtime": ["mean", stderr],
})
df4.columns = ["Runtime", "Runtime_stderr"]
df4 = df4.reset_index()

# figure_one(save=save)
# figure_two(save=save)
# figure_three(save=save)
# figure_four(save=save)
figure_five(save=save)
