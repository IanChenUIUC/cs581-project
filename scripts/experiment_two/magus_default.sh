## Bash script for running MAGUS (default) (does not do diagnostics)
## Expects the following variables to be set
# 	- $out 		(the output directory)
# 	- $unalign 	(the unaligned input file)
# 	- $time 	(the script for timing)

## Outputs
# 	- $out/iter{0-1}
# 		- align.fasta
# 		- timing.txt
# 		- guide.tree

magus_tmp=$HOME/magus_temp/magus_working_dir-$SLURM_JOB_ID


if [ ! -f $out/iter0/align.fasta ]; then
	rm -rf $out/iter0

	## estimate initial alignment (no timing, since included in the guide tree)
	rm -rf $out/$cur
	rm -rf $magus_tmp
	mkdir -p $out/iter0
	$HOME/methods/magus --recurse false --maxnumsubsets 200 -i $unalign -o $out/iter0/align.fasta --onlyinitialaln true -d $magus_tmp --overwrite

	## estimate guide tree
	rm -rf $magus_tmp
	$time $out/iter0/timing.txt $HOME/methods/magus --recurse false --maxnumsubsets 200 -i $unalign -o $out/iter0/guide.tree --onlyguidetree true -d $magus_tmp --overwrite
fi

## estimate alignment
if [ ! -f $out/iter1/align.fasta ]; then
	rm -rf $magus_tmp
	mkdir -p $out/iter1
	$time $out/iter1/timing.txt $HOME/methods/magus --recurse false --maxnumsubsets 200 -i $unalign -t $out/iter0/guide.tree -o $out/iter1/align.fasta -d $magus_tmp --overwrite
	rm -rf $magus_tmp
fi
