# Running Commands:

## FastTree
	~/methods/FastTree -nt -gtr -gamma [<alignment>] > [<tree-file>]

## FastTree (no ML)
	~/methods/FastTree -nt -noml -gtr -gamma [<alignment>] > [<tree-file>]

## MAFFT PartTree
	~/methods/mafft --help

## MAGUS
	~/methods/magus --help

# Analysis Commands:

## Tree Error
	python3 ~/projects/scripts/robinson_foulds.py [<estimated tree>] [<true tree>]

The exact script can be found in the `scripts/robinson_foulds.py` file.
It uses the `ete3` python [package](https://pypi.org/project/ete3/) (version 3.13), which was installed through `pip`.
See the [tutorial](https://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#robinson-foulds-distance) here.

## Alignment Error
	java -jar ~/methods/FastSP.jar -r reference_alignment_file -e estimated_alignment_file

# Datasets

## ROSE (1000M1-M4, 1000L1-L3)
These datasets were used in the original MAGUS paper and can be downloaded from the [Illinois Data Bank](https://doi.org/10.13012/B2IDB-2643961_V1)

## RNASim (1'000 and 10'000 sequence subsets)
These datasets were used in the original MAGUS paper and can be downloaded from the [Illinois Data Bank](https://doi.org/10.13012/B2IDB-2643961_V1)

## 16S (16S.3, 16S.T, 16S.B.ALL)
These datasets were used in the original MAGUS paper and can be downloaded from the [Illinois Data Bank](https://doi.org/10.13012/B2IDB-2643961_V1)

# Installation

## MAFFT
I downloaded MAFFT v7.526 [here](https://gitlab.com/sysimm/mafft) and following the directions exactly to build from source (non-default location, no root account needed).

## MAGUS
I downloaded MAGUS v0.2.0 [here](https://github.com/vlasmirnov/MAGUS). Here, I had to modify the `main.py` slightly; I changed the relative imports to absolute imports. See below.
```
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from magus import __version__

from magus.align.aligner import mainAlignmentTask
from magus.configuration import buildConfigs, Configs
from magus.tasks import manager
```

## MUSCLE
I downloaded muscle v5.3 by running `wget` on the linux [release](https://github.com/rcedgar/muscle/releases/tag/v5.3)

## FastTree
I installed FastTree v2.1.11 by running `wget` on the [Linux 64-bit executable (+SSE)](https://morgannprice.github.io/fasttree/FastTree)

## FastSP
I installed FastSP v1.7.1 by running `wget` on the [jar file](https://github.com/smirarab/FastSP/blob/master/FastSP.jar)
