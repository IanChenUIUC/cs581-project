# UIUC CS 581 Course Project

Ian Chen

# Exploring the effect of Iteration on MAGUS

## MAGUS

MAGUS is a multiple sequence alignment (MSA) tool.
It is described [here](https://doi.org/10.1093/bioinformatics/btaa992).

## Iteration

MAGUS uses an initial guide tree, estimated from an initial alignment.
This project will test multiple iterations of MAGUS, feeding the output alignment of iteration i to estimate the guide tree for iteration i + 1.
