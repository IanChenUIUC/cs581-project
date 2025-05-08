import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from scipy.stats import linregress
import numpy as np
import pandas as pd
import itertools as it
import seaborn as sns

df = pd.read_csv("Results.csv")
df["RF"] = (df["RFFN"] + df["RFFP"]) / 2
df["(FN+FP)/2"] = (df["SPFN"] + df["SPFP"]) / 2

iterations = sorted(list(set(df["Iteration"])))
subsets = sorted(list(set(df["Subset_Size"])))
guide = sorted(list(set(df["GuideTree_Method"])))
initial = sorted(list(set(df["Initial_Method"])))

def figure_one(save = False):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout = True)
    # fig.suptitle("Subset Size")

    base = df[(df["Initial_Method"] == "magus") & (df["GuideTree_Method"] == "ml")]
    sns.boxplot(ax = ax1, x = "Iteration", y = "(FN+FP)/2", hue = "Subset_Size", data = base, palette = "Set2")
    ax1.legend().set_visible(False)
    ax1.set_ylim((0, 0.26))
    ax1.set_title("MAGUS(magus, ml)")

    base = df[(df["Initial_Method"] == "magus") & (df["GuideTree_Method"] == "noml")]
    sns.boxplot(ax = ax2, x = "Iteration", y = "(FN+FP)/2", hue = "Subset_Size", data = base, palette = "Set2")
    ax2.legend().set_visible(False)
    ax2.set_ylim((0, 0.26))
    ax2.set_title("MAGUS(magus, noml)")

    base = df[(df["Initial_Method"] == "clustalo") & (df["GuideTree_Method"] == "ml")]
    sns.boxplot(ax = ax3, x = "Iteration", y = "(FN+FP)/2", hue = "Subset_Size", data = base, palette = "Set2")
    ax3.legend().set_visible(False)
    ax3.set_ylim((0, 0.52))
    ax3.set_title("MAGUS(clustalo, ml)")

    base = df[(df["Initial_Method"] == "clustalo") & (df["GuideTree_Method"] == "noml")]
    sns.boxplot(ax = ax4, x = "Iteration", y = "(FN+FP)/2", hue = "Subset_Size", data = base, palette = "Set2")
    ax4.set_ylim((0, 0.52))
    ax4.set_title("MAGUS(clustalo, noml)")

    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 2, fig.get_size_inches()[1] * 2)
        plt.savefig("fig1.pdf", bbox_inches="tight")
    else:
        plt.show()

def figure_two(save = False):
    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout = True)
    # fig.suptitle("Guide Tree Method")

    base = df[(df["Initial_Method"] == "magus") & (df["Subset_Size"] == 100)]
    sns.boxplot(ax = ax1, x = "Iteration", y = "(FN+FP)/2", hue = "GuideTree_Method", data = base, palette = "Set2")
    ax1.legend().set_visible(False)
    ax1.set_ylim((0, 0.52))
    ax1.set_title("MAGUS(magus, s=100)")

    base = df[(df["Initial_Method"] == "clustalo") & (df["Subset_Size"] == 100)]
    sns.boxplot(ax = ax2, x = "Iteration", y = "(FN+FP)/2", hue = "GuideTree_Method", data = base, palette = "Set2")
    ax2.set_ylim((0, 0.52))
    ax2.set_title("MAGUS(clustalo, s=100)")

    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 2, fig.get_size_inches()[1])
        plt.savefig("fig2.pdf", bbox_inches="tight")
    else:
        plt.show()

def figure_three(save = False):
    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout = True)
    # fig.suptitle("Guide Tree Method")

    base = df[(df["Initial_Method"] == "magus") & (df["Subset_Size"] == 100)]
    sns.boxplot(ax = ax1, x = "Iteration", y = "Runtime", hue = "GuideTree_Method", data = base, palette = "Set2")
    ax1.legend().set_visible(False)
    ax1.set_ylim((250, 1200))
    ax1.set_ylabel("Runtime (sec)")
    ax1.set_title("MAGUS(magus, s=100)")

    base = df[(df["Initial_Method"] == "clustalo") & (df["Subset_Size"] == 100)]
    sns.boxplot(ax = ax2, x = "Iteration", y = "Runtime", hue = "GuideTree_Method", data = base, palette = "Set2")
    ax2.set_ylim((250, 1200))
    ax2.set_title("MAGUS(clustalo, s=100)")
    ax2.set_ylabel("Runtime (sec)")

    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 2, fig.get_size_inches()[1])
        plt.savefig("fig3.pdf", bbox_inches="tight")
    else:
        plt.show()

def figure_four(save = False):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, constrained_layout = True)
    # fig.suptitle("Iteration Method")

    base = df[(df["Initial_Method"] == "magus") & (df["Subset_Size"] == 50)]
    sns.boxplot(ax = ax1, x = "GuideTree_Method", y = "(FN+FP)/2", hue = "Iteration", data = base, palette = "Set2")
    ax1.legend().set_visible(False)
    ax1.set_ylim((0, 0.52))
    ax1.set_title("MAGUS(magus, s=50)")

    base = df[(df["Initial_Method"] == "clustalo") & (df["Subset_Size"] == 50)]
    sns.boxplot(ax = ax2, x = "GuideTree_Method", y = "(FN+FP)/2", hue = "Iteration", data = base, palette = "Set2")
    ax2.set_ylim((0, 0.52))
    ax2.set_title("MAGUS(clustalo, s=50)")

    base = df[(df["Initial_Method"] == "magus") & (df["Subset_Size"] == 50)]
    sns.boxplot(ax = ax3, x = "GuideTree_Method", y = "RF", hue = "Iteration", data = base, palette = "Set2")
    ax3.legend().set_visible(False)
    ax3.set_ylim((0, 0.38))
    ax3.set_title("MAGUS(magus, s=50)")

    base = df[(df["Initial_Method"] == "clustalo") & (df["Subset_Size"] == 50)]
    sns.boxplot(ax = ax4, x = "GuideTree_Method", y = "RF", hue = "Iteration", data = base, palette = "Set2")
    ax4.set_ylim((0, 0.38))
    ax4.set_title("MAGUS(clustalo, s=50)")

    if save:
        fig.set_size_inches(fig.get_size_inches()[0] * 2, fig.get_size_inches()[1] * 2)
        plt.savefig("fig4.pdf", bbox_inches="tight")
    else:
        plt.show()

def figure_five(save = False):
    fig, ax = plt.subplots()
    # fig.suptitle("Tree Error versus Alignment Error")

    sns.scatterplot(ax = ax, x="RF", y="(FN+FP)/2", hue = "Subset_Size", marker = "v", data = df)
    sns.regplot(ax = ax, x="RF", y="(FN+FP)/2", scatter = False, data = df)
    # slope, intercept, r_value, p_value, std_err = linregress(df["RF"], df["(FN+FP)/2"])
    # r_squared = r_value**2
    # print(r_squared)

    plt.tight_layout()
    if save:
        plt.savefig(f"fig5.pdf")
    else:
        plt.show()

save = True
# figure_one(save=save)
# figure_two(save=save)
# figure_three(save=save)
figure_four(save=save)
# figure_five(save=save)
