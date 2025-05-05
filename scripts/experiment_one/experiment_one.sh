#!/usr/bin/env bash

for r in {0..9}
do
	rep=$r sbatch experiment_one.sbatch
done
