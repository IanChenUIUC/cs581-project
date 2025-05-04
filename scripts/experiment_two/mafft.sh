## Bash script for running MAGUS with iterations (does not do diagnostics)
## Expects the following variables to be set
# 	- $out 		(the output directory)
# 	- $unalign 	(the unaligned input file)
# 	- $time 	(the script for timing)
# 	- $d 		(the data type)

## Outputs
# 	- $out/
# 		- align.fasta
# 		- timing.txt

if [ ! -f $out/align.fasta ]; then
	rm -rf $out
	mkdir -p $out
	$time $out/timing.txt $HOME/methods/mafft.sh --auto --thread 128 $unalign $out/align.fasta
fi
