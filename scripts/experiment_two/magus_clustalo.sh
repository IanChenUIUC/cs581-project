## Bash script for running MAGUS with iterations (does not do diagnostics)
## Expects the following variables to be set
# 	- $out 		(the output directory)
# 	- $unalign 	(the unaligned input file)
# 	- $time 	(the script for timing)

## Outputs
# 	- $out/iter{0-4}
# 		- align.fasta
# 		- timing.txt
# 		- guide.tree

## Parameters
# 	- subset size 	= 100
# 	- guide tree 	= FastTree -noml
# 	- initialtree	= MAGUS default

magus_tmp=$HOME/magus_temp/magus_working_dir-$SLURM_JOB_ID

## estimate initial alignment (no timing, since included in the guide tree)
if [ ! -f $out/iter0/align.fasta ]; then
	rm -rf $out/iter0
	rm -rf $magus_tmp
	mkdir -p $out/iter0
	$HOME/methods/magus --recurse false --maxnumsubsets 200 -i $unalign -o $out/iter0/align.fasta --onlyinitialaln true -d $magus_tmp --overwrite
	
	## estimate guide tree
	rm -rf $magus_tmp
	$time $out/iter0/timing.txt $HOME/methods/clustalo --max-hmm-iterations=-1 -i $unalign --guidetree-out=$out/iter0/guide.tree
fi

## alignment for iter i
prev=iter0
for i in {1..4}
do
	cur=iter$i

	rm -rf $magus_tmp

	if [ ! -f $out/$cur/align.fasta ]; then
		rm -rf $out/$cur
		mkdir -p $out/$cur
		$time $out/$cur/timing.txt $HOME/methods/magus --recurse false --maxnumsubsets 200 --maxsubsetsize 100 -i $unalign -t $out/$prev/guide.tree -o $out/$cur/align.fasta -d $magus_tmp --overwrite
		$time $out/$cur/timing.txt $HOME/methods/FastTree.sh -nt -gtr -gamma -noml $out/$cur/align.fasta $out/$cur/guide.tree
	fi

	prev=$cur
done

rm -rf $magus_tmp
