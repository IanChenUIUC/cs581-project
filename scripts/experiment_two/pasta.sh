## Bash script for running MAGUS with iterations (does not do diagnostics)
## Expects the following variables to be set
# 	- $out 		(the output directory)
# 	- $unalign 	(the unaligned input file)
# 	- $time 	(the script for timing)
# 	- $d 		(the data type)

## Outputs
# 	- $out/iter{1-3}
# 		- align.fasta
# 		- timing.txt
# 		- guide.tree

for i in {3..3}
do
	if [ ! -f $out/iter$i/pastajob.marker001.unalign.aln ]; then
		rm -rf $out/iter$i
		mkdir -p $out/iter$i
		$time $out/iter$i/timing.txt $HOME/methods/pasta -d $d -i $unalign -o $out/iter$i --iter-limit=$i 
	fi
done
