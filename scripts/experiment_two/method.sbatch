#!/usr/bin/env bash
#Experiment 2: method
#SBATCH --time=12:00:00			   # Job run time (hh:mm:ss)
#SBATCH --nodes=1			   # Number of nodes
#SBATCH --gres=gpu:0                       # Number of GPUs, use --gres=gpu:A10 to specify GPU model or --gres=gpu:A10:2 to specify both model and number of GPUs
#SBATCH --ntasks-per-node=64               # Number of cores per node
#SBATCH --mem-per-cpu=6750                 # Memory per core (value in MBs)
#SBATCH --account=25sp-cs581a-eng          # Account
#SBATCH --output=/u/ianchen3/project/slurm/slurm-%j.out
#SBATCH --partition=eng-instruction        # Parititon

# ==============================================================================
# Setup 
# ==============================================================================
time="$HOME/project/scripts/experiment_two/time.sh"

IFS=, read -r -a rose_models <<< "$ROSE_MODELS"
IFS=, read -r -a rose_replic <<< "$ROSE_REPLIS"
IFS=, read -r -a rnasim_models <<< "$RNASim_MODELS"
IFS=, read -r -a rnasim_replic <<< "$RNASim_REPLIS"
IFS=, read -r -a s_models <<< "$S_MODELS"

echo "Running Experiment two for $method"
echo "ROSE_MODELS=""$ROSE_MODELS"
echo "ROSE_REPLIS=""$ROSE_REPLIS"
echo "RNASim_MODELS=""$RNASim_MODELS"
echo "RNASim_REPLIS=""$RNASim_REPLIS"
echo "S_MODELS=""$S_MODELS"

source $HOME/.venv/bin/activate

# ==============================================================================
# ROSE
# ==============================================================================

for m in ${rose_models[@]}
do
	for r in ${rose_replic[@]}
	do
		out="$HOME/project/output/E2/ROSE-$m/R$r/$method"
		unalign="$HOME/project/data/ROSE/$m/R$r/rose.aln.unalign.fasta"
		out=$out unalign=$unalign time=$time d=dna $HOME/project/scripts/experiment_two/$method.sh
	done
done

# ==============================================================================
# RNASim
# ==============================================================================

for m in ${rnasim_models[@]}
do
	for r in ${rnasim_replic[@]}
	do
		out="$HOME/project/output/E2/RNASim-$m/R$r/$method"
		unalign="$HOME/project/data/RNASim/$m/R$r/unalign.fasta"
		out=$out unalign=$unalign time=$time d=rna $HOME/project/scripts/experiment_two/$method.sh
	done
done

# ==============================================================================
# Gutell
# ==============================================================================

for m in ${s_models[@]}
do
	r=0
	out="$HOME/project/output/E2/$m/R$r/$method"
	unalign="$HOME/project/data/16S/$m/R$r/unalign.fasta"
	out=$out unalign=$unalign time=$time d=dna $HOME/project/scripts/experiment_two/$method.sh
done
