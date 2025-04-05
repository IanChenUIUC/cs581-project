# Method Versions:

FastTree2.1: 
	- https://morgannprice.github.io/fasttree

FastME 2.1.6.4:
	- http://www.atgc-montpellier.fr/fastme/binaries.php

# Running Commands:

FastTree:
	~/methods/FastTree -nt [<-model>] <alignment> > <tree-file>

FastME:
	~/methods/FastME -m NJ [<-d model>] -i <alignment> -o <tree-file>

# Input Conversion:

FASTA to PHYLIP:
	python package, https://github.com/biopython/biopython/blob/master/README.rst

# Analysis Commands:

RF Distances:
	python package, https://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#robinson-foulds-distance

