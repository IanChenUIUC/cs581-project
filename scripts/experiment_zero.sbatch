#!/usr/bin/env bash
#Experiment 0: Testing Scripts
#SBATCH --time=01:00:00			   # Job run time (hh:mm:ss)
#SBATCH --nodes=3			   # Number of nodes
#SBATCH --gres=gpu:0                       # Number of GPUs, use --gres=gpu:A10 to specify GPU model or --gres=gpu:A10:2 to specify both model and number of GPUs
#SBATCH --ntasks-per-node=16               # Number of cores per node
#SBATCH --account=25sp-cs581a-eng          # Account
#SBATCH --partition=eng-instruction        # Parititon
#SBATCH --output=$HOME/project/slurm/slurm-%j.out

# ==============================================================================
# Setup 
# ==============================================================================
rtt="$HOME/project/data/ROSE/1000M1/R0/rose.tt"
aln="$HOME/project/data/ROSE/1000M1/R0/rose.aln.true.fasta"
out="$HOME/project/output/E0"

declare -a input_files=(
"$HOME/project/data/ROSE/1000M1/R0/rose.aln.unalign.fasta"
"$HOME/project/data/ROSE/1000M1/R0/rose.aln.true.fasta"
"${out}/MagusAln.fasta"
"$HOME/project/data/ROSE/1000M1/R0/rose.aln.true.fasta"
"${out}/MagusAln.fasta"
"$HOME/project/data/ROSE/1000M1/R0/rose.aln.unalign.fasta"
)

declare -a output_files=(
"${out}/MagusAln.fasta"
"${out}/TrueAln_FastTreeNoML.tree"
"${out}/EstAln_FastTreeNoML.tree"
"${out}/TrueAln_FastTreeML.tree"
"${out}/EstAln_FastTreeML.tree"
"${out}/NoAln_ClustalO.tree"
)

declare -a error_files=(
"${out}/MagusAln_RF.csv"
"${out}/TrueAln_FastTreeNoML_RF.csv"
"${out}/EstAln_FastTreeNoML_RF.csv"
"${out}/TrueAln_FastTreeML_RF.csv"
"${out}/EstAln_FastTreeML_RF.csv"
"${out}/NoAln_ClustalO_RF.csv"
)

mkdir -p $out
source $HOME/.venv/bin/activate

# ==============================================================================
# Generate MAGUS alignment on 1000M1 ROSE (replicate 0)
# ==============================================================================
$HOME/methods/magus --recurse false -i ${input_files[0]} -o ${output_files[0]} -d $HOME/magus_temp/magus_working_dir-$SLURM_JOB_ID
 
# ==============================================================================
# Generate FastTree2 no ML on true and MAGUS alignments
# ==============================================================================
$HOME/methods/FastTree -nt -gtr -gamma -noml < ${input_files[1]} > ${output_files[1]}
$HOME/methods/FastTree -nt -gtr -gamma -noml < ${input_files[2]} > ${output_files[2]}

# ==============================================================================
# Generate FastTree2 (with and without ML) output_files on MAGUS alignments
# ==============================================================================
$HOME/methods/FastTree -nt -gtr -gamma < ${input_files[3]} > ${output_files[3]}
$HOME/methods/FastTree -nt -gtr -gamma < ${input_files[4]} > ${output_files[4]}

# ==============================================================================
# Generate ClustalOmega output_files on unaligned dataset
# ==============================================================================
$HOME/methods/clustalo --max-hmm-iterations=-1 -i ${input_files[5]} --guidetree-out=${output_files[5]}

# ==============================================================================
# Compare alignment accuracy between MAGUS and true
# ==============================================================================
java -jar $HOME/scripts/FastSP.jar -r $aln -e ${output_files[0]} > ${error_files[0]}

# ==============================================================================
# Compare tree error for all trees generated
# ==============================================================================
for i in {1..5}
do
	python3 $HOME/scripts/robinson_foulds.py ${output_files[i]} $rtt > ${error_files[i]}
done
