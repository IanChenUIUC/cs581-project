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

source $HOME/.venv/bin/activate

python3 $HOME/project/analysis/experiment_two/error.py

