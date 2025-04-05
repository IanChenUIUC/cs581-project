import sys
import ete3

def main():
    if len(sys.argv) != 3:
        print("incorrect arguments, exiting...")
        return 1

    with open(sys.argv[1], "r") as f:
        t1 = ete3.Tree(f.read())
    with open(sys.argv[2], "r") as f:
        t2 = ete3.Tree(f.read())

    rf, max_rf, common_leaves, parts_t1, parts_t2, *_ = t1.robinson_foulds(t2, unrooted_trees = True)
    rf_FP = len(parts_t1 - parts_t2) / len(parts_t1)
    rf_FN = len(parts_t2 - parts_t1) / len(parts_t2)

    print("rf_FN,rf_FP")
    print(rf_FN, rf_FP, sep=",")
    return 0

if __name__ == "__main__":
    main()
