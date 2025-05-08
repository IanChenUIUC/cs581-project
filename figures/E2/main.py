import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import itertools as it
import more_itertools as mit
import seaborn as sns

## ===================== draw figures =====================

def figure_one(save = False):
    fig, ax = plt.subplots(constrained_layout = True)
    # fig.suptitle("MAGUS vs MAGUS")

    methods = ["magus_clustalo-iter1", "magus_clustalo-iter2", "magus_clustalo-iter3", "magus_clustalo-iter4", "magus_magus-iter1", "magus_magus-iter2", "magus_magus-iter3", "magus_magus-iter4", "magus_default-iter1"]
    labels = ["magus(clustalo, i=1)", "magus(clustalo, i=2)", "magus(clustalo, i=3)", "magus(clustalo, i=4)", "magus(magus, i=1)", "magus(magus, i=2)", "magus(magus, i=3)", "magus(magus, i=4)", "magus(default)"]
    datasets = ["ROSE-1000L2", "ROSE-1000M3", "RNASim-1000", "RNASim-10000", "ROSE-1000L1", "ROSE-1000M2", "ROSE-1000L3"]

    df = df1[~df1["Dataset"].str.contains("16S")]
    base = df[df["Iteration"] >= 1][["Dataset", "(FN+FP)/2", "Method"]]
    sns.boxplot(ax = ax, x = "Dataset", y = "(FN+FP)/2", hue = "Method", data = base, palette = "Set2", hue_order = methods, order = datasets)
    ax.set_ylim(bottom = 0)
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, loc = "upper left")

    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 1.5, fig.get_size_inches()[1])
        plt.savefig("fig1.pdf", bbox_inches="tight")
    else:
        plt.show()

def figure_two(save = False):
    fig = plt.figure(layout = "constrained")
    gs1, gs2 = gridspec.GridSpec(1, 2, width_ratios=[5, 2], figure = fig)
    axes = [fig.add_subplot(gs1), fig.add_subplot(gs2)]
    # fig.suptitle("MAGUS vs All")

    methods = ["mafft", "clustalo", "muscle", "pasta-iter3", "magus_default-iter1", "magus_clustalo-iter2", "magus_magus-iter1", "magus_clustalo-iter4", "magus_magus-iter4"]
    labels = ["mafft", "clustalo", "muscle", "pasta", "magus(default)", "magus(clustalo, i=2)", "magus(magus, i=1)", "magus(clustalo, i=4)", "magus(magus, i=4)"]
    datasets = [["ROSE-1000L2", "ROSE-1000M3", "ROSE-1000L1", "ROSE-1000M2", "ROSE-1000L3"], ["RNASim-1000", "RNASim-10000"]]
    for ax, data in zip(axes, datasets):
        frame = df1[df1["Dataset"].isin(data)][["Dataset", "(FN+FP)/2", "Method"]]
        frame = frame[frame["Method"].isin(methods)]
        sns.boxplot(ax = ax, x = "Dataset", y = "(FN+FP)/2", hue = "Method", data = frame, palette = "Set2", hue_order = methods, order = data)
        ax.set_ylim(0, 1)
        handles, _ = ax.get_legend_handles_labels()
        ax.legend(handles=handles, labels=labels)

    axes[0].legend().set_visible(False)
    axes[1].set_ylabel("")
    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 2, fig.get_size_inches()[1] * 2)
        plt.savefig("fig2a.pdf", bbox_inches="tight")
    else:
        plt.show()

    fig = plt.figure(layout = "constrained")
    gs1, gs2 = gridspec.GridSpec(1, 2, width_ratios=[5, 2], figure = fig)
    axes = [fig.add_subplot(gs1), fig.add_subplot(gs2)]

    methods = ["muscle", "pasta-iter3", "magus_default-iter1", "magus_clustalo-iter2", "magus_magus-iter1", "magus_clustalo-iter4", "magus_magus-iter4"]
    labels = ["muscle", "pasta", "magus(default)", "magus(clustalo, i=2)", "magus(magus, i=1)", "magus(clustalo, i=4)", "magus(magus, i=4)"]
    datasets = [["ROSE-1000L2", "ROSE-1000M3", "ROSE-1000L1", "ROSE-1000M2", "ROSE-1000L3"], ["RNASim-1000", "RNASim-10000"]]
    for ax, data in zip(axes, datasets):
        frame = df1[df1["Dataset"].isin(data)][["Dataset", "(FN+FP)/2", "Method"]]
        frame = frame[frame["Method"].isin(methods)]
        sns.boxplot(ax = ax, x = "Dataset", y = "(FN+FP)/2", hue = "Method", data = frame, palette = "Set2", hue_order = methods, order = data)
        ax.set_ylim(0, 0.26)
        handles, _ = ax.get_legend_handles_labels()
        ax.legend(handles=handles, labels=labels)

    axes[0].legend().set_visible(False)
    axes[1].set_ylabel("")
    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 2, fig.get_size_inches()[1] * 2)
        plt.savefig("fig2b.pdf", bbox_inches="tight")
    else:
        plt.show()

# def figure_two(save = False):
#     fig = plt.figure(layout = "constrained")
#     gs1, gs2, gs3, gs4 = gridspec.GridSpec(2, 2, width_ratios=[5, 2], figure = fig)
#     axes = [fig.add_subplot(gs1), fig.add_subplot(gs2), fig.add_subplot(gs3), fig.add_subplot(gs4)]
#     # fig.suptitle("MAGUS vs All")
# 
#     methods = ["mafft", "clustalo", "muscle", "pasta-iter3", "magus_default-iter1", "magus_clustalo-iter2", "magus_magus-iter1", "magus_clustalo-iter4", "magus_magus-iter4"]
#     labels = ["mafft", "clustalo", "muscle", "pasta", "magus(default)", "magus(clustalo, i=2)", "magus(magus, i=1)", "magus(clustalo, i=4)", "magus(magus, i=4)"]
#     datasets = [["ROSE-1000L2", "ROSE-1000M3", "ROSE-1000L1", "ROSE-1000M2", "ROSE-1000L3"], ["RNASim-1000", "RNASim-10000"]]
#     for ax, data in zip(axes, datasets):
#         frame = df1[df1["Dataset"].isin(data)][["Dataset", "(FN+FP)/2", "Method"]]
#         frame = frame[frame["Method"].isin(methods)]
#         sns.boxplot(ax = ax, x = "Dataset", y = "(FN+FP)/2", hue = "Method", data = frame, palette = "Set2", hue_order = methods, order = data)
#         ax.set_ylim(0, 1)
#         handles, _ = ax.get_legend_handles_labels()
#         ax.legend(handles=handles, labels=labels)
# 
#     methods = ["muscle", "pasta-iter3", "magus_default-iter1", "magus_clustalo-iter2", "magus_magus-iter1", "magus_clustalo-iter4", "magus_magus-iter4"]
#     labels = ["muscle", "pasta", "magus(default)", "magus(clustalo, i=2)", "magus(magus, i=1)", "magus(clustalo, i=4)", "magus(magus, i=4)"]
#     datasets = [["ROSE-1000L2", "ROSE-1000M3", "ROSE-1000L1", "ROSE-1000M2", "ROSE-1000L3"], ["RNASim-1000", "RNASim-10000"]]
#     for ax, data in zip(axes[2:], datasets):
#         frame = df1[df1["Dataset"].isin(data)][["Dataset", "(FN+FP)/2", "Method"]]
#         frame = frame[frame["Method"].isin(methods)]
#         sns.boxplot(ax = ax, x = "Dataset", y = "(FN+FP)/2", hue = "Method", data = frame, palette = "Set2", hue_order = methods, order = data)
#         ax.set_ylim(0, 0.26)
#         handles, _ = ax.get_legend_handles_labels()
#         ax.legend(handles=handles, labels=labels)
# 
#     axes[0].legend().set_visible(False)
#     axes[1].set_ylabel("")
#     axes[2].legend().set_visible(False)
#     axes[3].set_ylabel("")
#     if save:
#         fig.set_size_inches(fig.get_size_inches()[0] * 2, fig.get_size_inches()[1] * 2)
#         plt.savefig("fig2.pdf", bbox_inches="tight")
#     else:
#         plt.show()

def figure_three(save = False):
    fig = plt.figure(layout = "constrained")
    gs1, gs2 = gridspec.GridSpec(1, 2, width_ratios=[6, 1], figure = fig)
    ax1 = fig.add_subplot(gs1)
    ax2 = fig.add_subplot(gs2)
    # fig.suptitle("MAGUS vs All")
    
    datasets = ["ROSE-1000L2", "ROSE-1000M3", "RNASim-1000", "ROSE-1000L1", "ROSE-1000M2", "ROSE-1000L3"]
    base = df2[df2["Dataset"].isin(datasets)]
    methods = ["mafft", "clustalo", "muscle", "pasta-iter3", "magus_default-iter1", "magus_clustalo-iter2", "magus_magus-iter1", "magus_clustalo-iter4", "magus_magus-iter4"]
    labels = ["mafft", "clustalo", "muscle", "pasta", "magus(default)", "magus(clustalo, i=2)", "magus(magus, i=1)", "magus(clustalo, i=4)", "magus(magus, i=4)"]
    base = base[base["Method"].isin(methods)]
    sns.boxplot(ax = ax1, x = "Dataset", y = "Runtime", hue = "Method", data = base, palette = "Set2", hue_order = methods, order = datasets)
    ax1.set_ylabel("Runtime (sec)")
    handles, _ = ax1.get_legend_handles_labels()
    ax1.legend(handles=handles, labels=labels)

    base = df2[df2["Dataset"] == "RNASim-10000"]
    base = base[base["Method"].isin(methods)]
    sns.barplot(ax = ax2, x = "Dataset", y = "Runtime", hue = "Method", data = base, palette = "Set2", hue_order = methods)
    ax2.set_ylabel("")
    ax2.set_ylim(bottom = 1)
    ax2.set_yscale("log")
    ax2.legend().set_visible(False)

    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 1.5, fig.get_size_inches()[1])
        plt.savefig("fig3.pdf", bbox_inches="tight")
    else:
        plt.show()

def figure_four(save = False):
    fig, (ax1, ax2), = plt.subplots(1, 2, constrained_layout = True)
    # fig.suptitle("MAGUS vs All")

    methods = ["mafft", "clustalo", "muscle", "pasta-iter3", "magus_default-iter1", "magus_clustalo-iter2", "magus_magus-iter1", "magus_clustalo-iter4", "magus_magus-iter4"]
    labels = ["mafft", "clustalo", "muscle", "pasta", "magus(default)", "magus(clustalo, i=2)", "magus(magus, i=1)", "magus(clustalo, i=4)", "magus(magus, i=4)"]
    frame = df1[df1["Dataset"].str.contains("16S")][["Dataset", "(FN+FP)/2", "Method"]]
    frame = frame[frame["Method"].isin(methods)]
    sns.barplot(ax = ax1, x = "Dataset", y = "(FN+FP)/2", hue = "Method", data = frame, palette = "Set2", hue_order = methods)
    ax1.set_ylim(bottom = 0)
    handles, _ = ax1.get_legend_handles_labels()
    ax1.legend(handles=handles, labels=labels, ncols = 3)

    frame = df2[df2["Dataset"].str.contains("16S")][["Dataset", "Runtime", "Method"]]
    frame = frame[frame["Method"].isin(methods)]
    sns.barplot(ax = ax2, x = "Dataset", y = "Runtime", hue = "Method", data = frame, palette = "Set2", hue_order = methods)
    ax2.set_yscale("log")
    ax2.set_ylim(bottom = 1)
    ax2.set_ylabel("Runtime (sec)")
    ax2.legend().set_visible(False)

    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 3, fig.get_size_inches()[1] * 1.5)
        plt.savefig("fig4.pdf", bbox_inches="tight")
    else:
        plt.show()

def figure_five(save = False):
    def plot(base, ax, palettes):
        base1 = base[(base["Iteration"] == 4) & ~(base["Method"].str.contains("guide"))]
        sns.barplot(ax = ax, y = "Dataset", hue = "Method", x = "Runtime", orient = "h", data = base1, palette = next(palettes))

        for i in reversed(range(1, 4)):
            base1 = base[(base["Iteration"] == i) & (base["Method"].str.contains("guide"))]
            sns.barplot(ax = ax, y = "Dataset", hue = "Method", x = "Runtime", orient = "h", data = base1, palette = next(palettes))

            base1 = base[(base["Iteration"] == i) & ~(base["Method"].str.contains("guide"))]
            sns.barplot(ax = ax, y = "Dataset", hue = "Method", x = "Runtime", orient = "h", data = base1, palette = next(palettes))

        # plot the time for initial method
        base1 = base[(base["Iteration"] == 0)]
        sns.barplot(ax = ax, y = "Dataset", hue = "Method", x = "Runtime", orient = "h", data = base1, palette = next(palettes))
        ax.set_xlabel("Runtime (sec)")

    base = df3[df3["Method"].str.contains("magus_clustalo") | df3["Method"].str.contains("magus_magus")]
    base1 = base[~base["Dataset"].str.contains("16S") & ~(base["Dataset"] == "RNASim-10000")]
    base2 = base[base["Dataset"].str.contains("16S") | (base["Dataset"] == "RNASim-10000")]

    palette = sns.color_palette("Paired")
    palettes = it.cycle([[palette[0], palette[2]], [palette[1], palette[3]]])

    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout = True)
    # fig.suptitle("MAGUS vs All")
    plot(base1, ax1, palettes)
    plot(base2, ax2, palettes)

    handles, _ = ax1.get_legend_handles_labels()
    labels = ["MAGUS (clustalo)", "MAGUS (magus)", "Guide (clustalo)", "Guide (magus)"]
    ax1.legend(handles=handles[0:4], labels=labels)
    
    ax2.legend().set_visible(False)

    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 2, fig.get_size_inches()[1] * 1)
        plt.savefig("fig5.pdf", bbox_inches="tight")
    else:
        plt.show()
 
 
## ===================== prepocess the dataframe =====================

def stderr(x):
    return x.std() / np.sqrt(len(x))

df1 = pd.read_csv("Error.csv")
df1["(FN+FP)/2"] = (df1["SPFN"] + df1["SPFP"]) / 2

df2 = pd.read_csv("Timing.csv")

df3 = pd.read_csv("MagusTiming.csv")
df3 = df3[~(df3["Dataset"] == "16S.M")]
df3 = df3.groupby(by = ["Dataset", "Method", "Iteration"]).agg({
    "Runtime": ["mean", stderr],
})
df3.columns = ["Runtime", "Runtime_stderr"]
df3 = df3.reset_index()

save = True
figure_one(save=save)
# figure_two(save=save)
# figure_three(save=save)
# figure_four(save=save)
# figure_five(save=save)
