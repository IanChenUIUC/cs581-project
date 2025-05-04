#!/usr/bin/env bash
#Experiment 1: Parameter Tuning
#SBATCH --time=12:00:00			   # Job run time (hh:mm:ss)
#SBATCH --nodes=1			   # Number of nodes
#SBATCH --gres=gpu:0                       # Number of GPUs, use --gres=gpu:A10 to specify GPU model or --gres=gpu:A10:2 to specify both model and number of GPUs
#SBATCH --ntasks-per-node=16               # Number of cores per node
#SBATCH --account=25sp-cs581a-eng          # Account
#SBATCH --partition=eng-instruction        # Parititon
#SBATCH --output=/u/ianchen3/project/slurm/slurm-%j.out

# ==============================================================================
# Setup 
# ==============================================================================
time="$HOME/project/scripts/experiment_one/time.sh"

declare -a subset_size=( 200 100 50 25 10 )
declare -a initial_method=( "magus" "clustalo" )
declare -a guide_method=( "ft" "ftnoml" )

source $HOME/.venv/bin/activate

rtt="$HOME/project/data/ROSE/1000M1/R$rep/rose.tt"
aln="$HOME/project/data/ROSE/1000M1/R$rep/rose.aln.true.fasta"
unalign="$HOME/project/data/ROSE/1000M1/R$rep/rose.aln.unalign.fasta"

magus_tmp=$HOME/magus_temp/magus_working_dir-$SLURM_JOB_ID

# ==============================================================================
# Iteration 1
# ==============================================================================
out="$HOME/project/output/E1/R$rep/iter1"
mkdir -p $out

# magus and clustalo initial tree
$time "$out/timing.txt" $HOME/methods/magus --recurse false -i $unalign -o $out/magus_guide.tree --onlyguidetree true -d $magus_tmp --overwrite
$time "$out/timing.txt" $HOME/methods/clustalo --max-hmm-iterations=-1 -i $unalign --guidetree-out=$out/clustalo_guide.tree
rm -rf $magus_tmp

for m in ${initial_method[@]}
do
	# RF tree error
	python3 $HOME/scripts/robinson_foulds.py $out/${m}_guide.tree $rtt > $out/${m}_rf.csv

	for s in ${subset_size[@]}
	do
		# align using guide tree
		$time "$out/timing.txt" $HOME/methods/magus --recurse false --maxsubsetsize $s -i $unalign -t $out/${m}_guide.tree -o $out/${m}_${s}_ft_aln.fasta -d $magus_tmp --overwrite
		cp $out/${m}_${s}_ft_aln.fasta -d $out/${m}_${s}_ftnoml_aln.fasta
		# alignment error
		java -jar $HOME/scripts/FastSP.jar -r $aln -e $out/${m}_${s}_ft_aln.fasta > $out/${m}_${s}_ft_sp.txt
		java -jar $HOME/scripts/FastSP.jar -r $aln -e $out/${m}_${s}_ftnoml_aln.fasta > $out/${m}_${s}_ftnoml_sp.txt
		# clean magus run
		rm -rf $magus_tmp
	done
done

# ==============================================================================
# Iteration i = 2, 3, 4
# ==============================================================================
for i in {2..4}
do
	next="$HOME/project/output/E1/R$rep/iter$i"
	mkdir -p $next

	for s in ${subset_size[@]}
	do

		for m in ${initial_method[@]}
		do
			# fasttree guide tree with and without ml
			$time $next/timing.txt $HOME/methods/FastTree.sh -nt -gtr -gamma $out/${m}_${s}_ft_aln.fasta $next/${m}_${s}_ft_guide.tree
			$time $next/timing.txt $HOME/methods/FastTree.sh -nt -gtr -gamma -noml $out/${m}_${s}_ftnoml_aln.fasta $next/${m}_${s}_ftnoml_guide.tree

			for g in ${guide_method[@]}
			do
				# RF tree error
				python3 $HOME/scripts/robinson_foulds.py $next/${m}_${s}_${g}_guide.tree $rtt > $next/${m}_${s}_${g}_rf.csv
				# align using guide tree
				$time $next/timing.txt $HOME/methods/magus --recurse false --maxsubsetsize $s -i $unalign -t $next/${m}_${s}_${g}_guide.tree -o $next/${m}_${s}_${g}_aln.fasta -d $magus_tmp --overwrite
				# alignment error
				java -jar $HOME/scripts/FastSP.jar -r $aln -e $next/${m}_${s}_${g}_aln.fasta > $next/${m}_${s}_${g}_sp.txt
				# clean magus run
				rm -rf $magus_tmp
			done
		done
	done

	out=$next
done
