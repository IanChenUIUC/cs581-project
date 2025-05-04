import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from scipy.stats import linregress
import numpy as np
import pandas as pd
import itertools as it
import seaborn as sns

df = pd.read_csv("Results.csv")
df["(SPFN+SPFP)/2"] = (df["SPFN"] + df["SPFP"]) / 2
df["(SPFN+SPFP)/2_se"] = ((df["SPFN_std"] ** 2 + df["SPFP_std"] ** 2) ** 0.5) / (np.sqrt(5))
df["(RFFN+RFFP)/2"] = (df["RFFN"] + df["RFFP"]) / 2
df["(RFFN+RFFP)/2_se"] = ((df["RFFN_std"] ** 2 + df["RFFP_std"] ** 2) ** 0.5) / (np.sqrt(5))
df["SPFN_se"] = df["SPFN_std"] / (np.sqrt(5))
df["SPFP_se"] = df["SPFP_std"] / (np.sqrt(5))
df["RFFN_se"] = df["RFFN_std"] / (np.sqrt(5))
df["RFFP_se"] = df["RFFP_std"] / (np.sqrt(5))

iterations = sorted(list(set(df["Iteration"])))
subsets = sorted(list(set(df["Subset_Size"])))
guide = sorted(list(set(df["GuideTree_Method"])))
initial = sorted(list(set(df["Initial_Method"])))

def figure_one(save = False):
    gs = gridspec.GridSpec(1, 2, width_ratios=[7, 3])
    fig = plt.figure()
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    fig.suptitle("Comparison across Starting Trees")

    # fig 1a: alignment accuracy across starting trees
    base = df[(df["Iteration"] == 1) & (df["GuideTree_Method"] == "ml")][["(SPFN+SPFP)/2", "(SPFN+SPFP)/2_se", "Subset_Size", "Initial_Method"]]
    frame = base.pivot(index = "Subset_Size", columns = "Initial_Method", values = "(SPFN+SPFP)/2")
    error = base.pivot(index = "Subset_Size", columns = "Initial_Method", values = "(SPFN+SPFP)/2_se")
    frame.plot(ax = ax1, kind = "bar", ylabel = "(SPFN+SPFP)/2", yerr = error, ylim = (0, 0.50), rot = 0)

    # fig 1b: tree accuracy across starting trees
    base = df[(df["Iteration"] == 1) & (df["GuideTree_Method"] == "ml") & (df["Subset_Size"] == 10)][["(RFFN+RFFP)/2", "(RFFN+RFFP)/2_se", "Initial_Method"]]
    base.plot(ax = ax2, kind = "bar", ylabel = "(RFFN+RFFP)/2", yerr = "(RFFN+RFFP)/2_se", ylim = (0, 0.50), x = "Initial_Method", y = "(RFFN+RFFP)/2", rot = 0)

    ax1.legend(fontsize = "small", frameon = False)
    ax2.legend().set_visible(False)
    plt.tight_layout()

    if save:
        plt.savefig("fig1.pdf")
    else:
        plt.show()

def figure_two(save = False):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.suptitle("Comparison across Guide Tree Methods")

    # fig 2a: alignment accuracy across initial method, with s = 100, iteration = 2
    base = df[(df["Subset_Size"] == 100) & (df["Iteration"] == 2)][["(SPFN+SPFP)/2", "(SPFN+SPFP)/2_se", "GuideTree_Method", "Initial_Method"]]
    frame = base.pivot(index = "Initial_Method", columns = "GuideTree_Method", values = "(SPFN+SPFP)/2")
    error = base.pivot(index = "Initial_Method", columns = "GuideTree_Method", values = "(SPFN+SPFP)/2_se")
    frame.plot(ax = ax1, kind = "bar", ylabel = "(SPFN+SPFP)/2", yerr = error, ylim = (0, 0.20), rot = 0)

    # fig 2b: alignment accuracy across subset size, with magus, iteration = 2
    base = df[(df["Initial_Method"] == "magus") & (df["Iteration"] == 2)][["(SPFN+SPFP)/2", "(SPFN+SPFP)/2_se", "GuideTree_Method", "Subset_Size"]]
    frame = base.pivot(index = "Subset_Size", columns = "GuideTree_Method", values = "(SPFN+SPFP)/2")
    error = base.pivot(index = "Subset_Size", columns = "GuideTree_Method", values = "(SPFN+SPFP)/2_se")
    frame.plot(ax = ax2, kind = "bar", ylabel = "(SPFN+SPFP)/2", yerr = error, ylim = (0, 0.20), rot = 0)

    # fig 2c: alignment accuracy across initial method, with s = 100, iteration = 4
    base = df[(df["Subset_Size"] == 100) & (df["Iteration"] == 4)][["(SPFN+SPFP)/2", "(SPFN+SPFP)/2_se", "GuideTree_Method", "Initial_Method"]]
    frame = base.pivot(index = "Initial_Method", columns = "GuideTree_Method", values = "(SPFN+SPFP)/2")
    error = base.pivot(index = "Initial_Method", columns = "GuideTree_Method", values = "(SPFN+SPFP)/2_se")
    frame.plot(ax = ax3, kind = "bar", ylabel = "(SPFN+SPFP)/2", yerr = error, ylim = (0, 0.20), rot = 0)

    # fig 2b: alignment accuracy across subset size, with magus, iteration = 4
    base = df[(df["Initial_Method"] == "magus") & (df["Iteration"] == 4)][["(SPFN+SPFP)/2", "(SPFN+SPFP)/2_se", "GuideTree_Method", "Subset_Size"]]
    frame = base.pivot(index = "Subset_Size", columns = "GuideTree_Method", values = "(SPFN+SPFP)/2")
    error = base.pivot(index = "Subset_Size", columns = "GuideTree_Method", values = "(SPFN+SPFP)/2_se")
    frame.plot(ax = ax4, kind = "bar", ylabel = "(SPFN+SPFP)/2", yerr = error, ylim = (0, 0.20), rot = 0)

    ax1.legend(fontsize = "small", frameon = False, ncol = 2)
    ax2.legend(fontsize = "small", frameon = False, ncol = 2)
    ax3.legend(fontsize = "small", frameon = False, ncol = 2)
    ax4.legend(fontsize = "small", frameon = False, ncol = 2)
    plt.tight_layout()

    if save:
        plt.savefig("fig2.pdf")
    else:
        plt.show()

def figure_three(save = False):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.suptitle("Comparison across Iterations (ClustalOmega)")

    # fig 2a: alignment accuracy across guide tree method, with s = 100
    base = df[(df["Subset_Size"] == 100) & (df["Initial_Method"] == "clustalo")][["SPFN", "SPFN_se", "Iteration", "GuideTree_Method"]]
    frame = base.pivot(index = "Iteration", columns = "GuideTree_Method", values = "SPFN")
    error = base.pivot(index = "Iteration", columns = "GuideTree_Method", values = "SPFN_se")
    frame.plot(ax = ax1, kind = "bar", ylabel = "SPFN", yerr = error, ylim = (0, 0.45), rot = 0)

    # fig 2b: alignment accuracy across subset size, with ML heuristic
    base = df[(df["GuideTree_Method"] == "ml") & (df["Initial_Method"] == "clustalo")][["SPFN", "SPFN_se", "Iteration", "Subset_Size"]]
    frame = base.pivot(index = "Iteration", columns = "Subset_Size", values = "SPFN")
    error = base.pivot(index = "Iteration", columns = "Subset_Size", values = "SPFN_se")
    frame.plot(ax = ax2, kind = "bar", ylabel = "SPFN", yerr = error, ylim = (0, 0.45), rot = 0)

    # fig 2c: alignment accuracy across guide tree method, with s = 100
    base = df[(df["Subset_Size"] == 100) & (df["Initial_Method"] == "clustalo")][["SPFP", "SPFP_se", "Iteration", "GuideTree_Method"]]
    frame = base.pivot(index = "Iteration", columns = "GuideTree_Method", values = "SPFP")
    error = base.pivot(index = "Iteration", columns = "GuideTree_Method", values = "SPFP_se")
    frame.plot(ax = ax3, kind = "bar", ylabel = "SPFP", yerr = error, ylim = (0, 0.45), rot = 0)

    # fig 2d: alignment accuracy across subset size, with ML heuristic
    base = df[(df["GuideTree_Method"] == "ml") & (df["Initial_Method"] == "clustalo")][["SPFP", "SPFP_se", "Iteration", "Subset_Size"]]
    frame = base.pivot(index = "Iteration", columns = "Subset_Size", values = "SPFP")
    error = base.pivot(index = "Iteration", columns = "Subset_Size", values = "SPFP_se")
    frame.plot(ax = ax4, kind = "bar", ylabel = "SPFP", yerr = error, ylim = (0, 0.45), rot = 0)

    ax1.legend(fontsize = "small", frameon = False)
    ax2.legend(fontsize = "small", frameon = False, ncol = 2)
    ax3.legend(fontsize = "small", frameon = False)
    ax4.legend(fontsize = "small", frameon = False, ncol = 2)
    plt.tight_layout()

    if save:
        plt.savefig("fig3.pdf")
    else:
        plt.show()
 
def figure_four(save = False):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.suptitle("Comparison across Iterations (MAGUS)")

    # fig 2a: alignment accuracy across guide tree method, with s = 100
    base = df[(df["Subset_Size"] == 100) & (df["Initial_Method"] == "magus")][["SPFN", "SPFN_se", "Iteration", "GuideTree_Method"]]
    frame = base.pivot(index = "Iteration", columns = "GuideTree_Method", values = "SPFN")
    error = base.pivot(index = "Iteration", columns = "GuideTree_Method", values = "SPFN_se")
    frame.plot(ax = ax1, kind = "bar", ylabel = "SPFN", yerr = error, ylim = (0, 0.20), rot = 0)

    # fig 2b: alignment accuracy across subset size, with ML heuristic
    base = df[(df["GuideTree_Method"] == "ml") & (df["Initial_Method"] == "magus")][["SPFN", "SPFN_se", "Iteration", "Subset_Size"]]
    frame = base.pivot(index = "Iteration", columns = "Subset_Size", values = "SPFN")
    error = base.pivot(index = "Iteration", columns = "Subset_Size", values = "SPFN_se")
    frame.plot(ax = ax2, kind = "bar", ylabel = "SPFN", yerr = error, ylim = (0, 0.20), rot = 0)

    # fig 2c: alignment accuracy across guide tree method, with s = 100
    base = df[(df["Subset_Size"] == 100) & (df["Initial_Method"] == "magus")][["SPFP", "SPFP_se", "Iteration", "GuideTree_Method"]]
    frame = base.pivot(index = "Iteration", columns = "GuideTree_Method", values = "SPFP")
    error = base.pivot(index = "Iteration", columns = "GuideTree_Method", values = "SPFP_se")
    frame.plot(ax = ax3, kind = "bar", ylabel = "SPFP", yerr = error, ylim = (0, 0.20), rot = 0)

    # fig 2d: alignment accuracy across subset size, with ML heuristic
    base = df[(df["GuideTree_Method"] == "ml") & (df["Initial_Method"] == "magus")][["SPFP", "SPFP_se", "Iteration", "Subset_Size"]]
    frame = base.pivot(index = "Iteration", columns = "Subset_Size", values = "SPFP")
    error = base.pivot(index = "Iteration", columns = "Subset_Size", values = "SPFP_se")
    frame.plot(ax = ax4, kind = "bar", ylabel = "SPFP", yerr = error, ylim = (0, 0.20), rot = 0)

    ax1.legend(fontsize = "small", frameon = False, ncol = 2)
    ax2.legend(fontsize = "small", frameon = False, ncol = 3)
    ax3.legend(fontsize = "small", frameon = False, ncol = 2)
    ax4.legend(fontsize = "small", frameon = False, ncol = 3)
    plt.tight_layout()

    if save:
        plt.savefig("fig4.pdf")
    else:
        plt.show()

def figure_five(save = False):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    fig.suptitle("Runtime Comparison of All Methods")

    index = ["1", "2", "3", "4"]
    markers = ['o', 's', '^', 'v', 'D', 'x', '+', '*', 'P', 'X']
    colors = [cm.cool(i) for i in np.linspace(0.05, 0.95, len(subsets))]
    for ((t, g), ax) in zip(it.product(initial, guide), (ax1, ax2, ax3, ax4)):
        print(t, g)
        for i, s in enumerate(subsets):
            data = {"Iteration": index}
            rows = df[(df["Subset_Size"] == s) & (df["GuideTree_Method"] == g) & (df["Initial_Method"] == t)]
            runtime = rows["Runtime"]
            data[f"{s}"] = list(runtime)

            frame = pd.DataFrame(data, index = index)
            frame.plot(ax = ax, color = [colors[i]], linewidth = 2, marker = markers[i], ylim = (300, 1250), xlabel = "Iteration", ylabel = "Runtime (sec)")

    ax1.legend().set_visible(False)
    ax2.legend().set_visible(False)
    ax3.legend().set_visible(False)
    ax4.legend().set_visible(False)

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.04), frameon=False)
    plt.tight_layout()

    if save:
        plt.savefig(f"fig5.pdf", bbox_inches = "tight")
    else:
        plt.show()

def figure_six(save = False):
    fig, ax = plt.subplots()
    fig.suptitle("Tree Error versus Alignment Error")

    sns.regplot(x=df["(RFFN+RFFP)/2"], y=df["(SPFN+SPFP)/2"])
    slope, intercept, r_value, p_value, std_err = linregress(df["(RFFN+RFFP)/2"], df["(SPFN+SPFP)/2"])
    r_squared = r_value**2
    print(r_squared)

    plt.tight_layout()
    if save:
        plt.savefig(f"fig6.pdf")
    else:
        plt.show()
    

save = True
figure_one(save=save)
# figure_two(save=save)
# figure_three(save=save)
# figure_four(save=save)
# figure_five(save=save)
# figure_six(save=save)
