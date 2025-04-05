import sys
from Bio import SeqIO

def main():
    if len(sys.argv) != 3:
        print("incorrect arguments, exiting...")
        return 1

    records = SeqIO.parse(sys.argv[1], "fasta")
    count = SeqIO.write(records, sys.argv[2], "phylip")
    print(f"Converted {count} records")
    return 0

if __name__ == "__main__":
    main()
