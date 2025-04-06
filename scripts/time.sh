# ./time.sh <output-file> <command>
echo $2 >> $1
/usr/bin/time -o $1 -a $2
