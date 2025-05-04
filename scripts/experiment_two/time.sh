# ./time.sh <output-file> <command>
outfile=$1
shift 1
echo "$@" >> $outfile
/usr/bin/time -f "%e %P %M" -o $outfile -a $@
