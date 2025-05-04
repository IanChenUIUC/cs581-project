## Removes all the '-' characters in the input alignment

# ROSE
declare -a model=( "1000M1" "1000M2" "1000M3" "1000L1" "1000L2" "1000L3" )

for m in ${model[@]}
do
	for r in {0..19}
	do
		in="$HOME/project/data/ROSE/${m}/R${r}/rose.aln.true.fasta"
		out="$HOME/project/data/ROSE/${m}/R${r}/rose.aln.unalign.fasta"
		echo "tr -d '-' < $in > $out"
		tr -d '-' < $in > $out
	done
done

# RNASim
declare -a model=( "1000" "10000" )

for m in ${model[@]}
do
	for r in {0..9}
	do
		in="$HOME/project/data/RNASim/${m}/R${r}/true_align.txt"
		out="$HOME/project/data/RNASim/${m}/R${r}/unalign.fasta"
		echo "tr -d '-' < $in > $out"
		tr -d '-' < $in > $out
	done
done

# Gutell
declare -a model=( "16S.B.ALL" "16S.3" "16S.M" "16S.T" )

for m in ${model[@]}
do
	for r in {0..0}
	do
		in="$HOME/project/data/16S/${m}/R${r}/true_align_clean.txt"
		out="$HOME/project/data/16S/${m}/R${r}/unalign.fasta"
		echo "tr -d '-' < $in > $out"
		tr -d '-' < $in > $out
	done
done
