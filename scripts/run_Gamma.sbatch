#!/usr/bin/env bash
#Homework #6 Test Scripts
#SBATCH --time=01:00:00			   # Job run time (hh:mm:ss)
#SBATCH --nodes=1			   # Number of nodes
#SBATCH --gres=gpu:1                       # Number of GPUs, use --gres=gpu:A10 to specify GPU model or --gres=gpu:A10:2 to specify both model and number of GPUs
#SBATCH --ntasks-per-node=1                # Number of cores per node
#SBATCH --account=25sp-cs581a-eng          # Account
#SBATCH --partition=eng-instruction        # Parititon

num_replicates=4

# FastTree stuff
declare -a FT_names=(
"FastTreeJC"
"FastTreeGTR"
)

declare -a FT_commands=( 
"$HOME/methods/FastTree -gamma -nt"
"$HOME/methods/FastTree -gamma -gtr -nt"
)

FT_num=1

# NJ stuff
declare -a NJ_names=(
"NeighborJoinJC"
"NeighborJoinGM"
"NeighborJoinHam"
)

declare -a NJ_commands=( 
"$HOME/methods/FastME -g -m NJ -d JC69"
"$HOME/methods/FastME -g -m NJ -d LogDet"
"$HOME/methods/FastME -g -m NJ -d p-distance"
)

NJ_num=2

# Variables
output_dir="$HOME/hw6/output/Gamma/"
rf_calc="python3 $HOME/hw6/scripts/robinson_foulds.py"
data_dir="$HOME/data/sate_journal/"

declare -a model_conditions=(
"1000M1"
"1000M4"
)

# Generating .phy files
phy_convert="python3 $HOME/hw6/scripts/fasta2phylip.py"

# for model in ${model_conditions[@]}
# do
# 	for i in $(seq 0 $num_replicates)
# 	do
# 		${phy_convert} "${data_dir}${model}/R${i}/rose.aln.true.fasta" "${data_dir}${model}/R${i}/rose.aln.true.phy"
# 	done
# done

# Running FastTree Commands (Gamma)
for model in ${model_conditions[@]}
do
	for i in $(seq 0 $num_replicates)
	do
		for j in $(seq 0 $FT_num)
		do
			mkdir -p "${output_dir}${model}/${FT_names[j]}_R${i}"
			${FT_commands[j]} < "${data_dir}${model}/R${i}/rose.aln.true.fasta"  > "${output_dir}${model}/${FT_names[j]}_R${i}/estimated.tt"
			${rf_calc} "${output_dir}${model}/${FT_names[j]}_R${i}/estimated.tt" "${data_dir}${model}/R${i}/rose.tt" > "${output_dir}${model}/${FT_names[j]}_R${i}/error.csv"
		done
	done
done

# NJ (on nucleotides) (Gamma)
for model in ${model_conditions[@]}
do
	for i in $(seq 0 $num_replicates)
	do
		for j in $(seq 0 $NJ_num)
		do
			mkdir -p "${output_dir}${model}/${NJ_names[j]}_R${i}"
			${NJ_commands[j]} -i "${data_dir}${model}/R${i}/rose.aln.true.phy"  -o "${output_dir}${model}/${NJ_names[j]}_R${i}/estimated.tt"
			${rf_calc} "${output_dir}${model}/${NJ_names[j]}_R${i}/estimated.tt" "${data_dir}${model}/R${i}/rose.tt" > "${output_dir}${model}/${NJ_names[j]}_R${i}/error.csv"
		done
	done
done
