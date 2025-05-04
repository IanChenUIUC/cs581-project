import glob
import os
import subprocess
import shutil

## setup
home = os.path.expanduser("~")
fastsp = os.path.join(home, "scripts", "FastSP.jar")

## copy all pasta alignments into align.fasta
pattern = os.path.join(home, "project", "output", "E2", "**", "pasta*.aln")
files = glob.glob(pattern, recursive = True)
for file in files:
    dest = os.path.join(os.path.dirname(file), "align.fasta")
    shutil.copy(file, dest)

## find all output alignments 
def find_reference_aln(dataset, replicate):
    if "16S" in dataset:
        return os.path.join(home, "project", "data", "16S", dataset, replicate, "true_align_clean.txt")
    if "ROSE" in dataset:
        return os.path.join(home, "project", "data", "ROSE", dataset.split("-")[1], replicate, "rose.aln.true.fasta")
    if "RNASim" in dataset:
        return os.path.join(home, "project", "data", "RNASim", dataset.split("-")[1], replicate, "true_align.txt")

    print("Could not parse reference, exiting...")
    exit(1)

pattern = os.path.join(home, "project", "output", "E2", "**", "align.fasta")
files = glob.glob(pattern, recursive = True)

for file in files:
    parent = os.path.abspath(os.path.join(file, os.pardir, "error.txt"))
    if os.path.exists(parent):
        continue

    # find the reference alignment -- find the dataset and do a mapping
    ref = find_reference_aln(file.split("/")[6], file.split("/")[7])

    # run FastSP 
    print(f"Comparing {ref=} with {file=}")
    out = subprocess.run(["java", "-jar", fastsp, "-r", ref, "-e", file], capture_output=True)

    # write FastSP results
    parent = os.path.abspath(os.path.join(file, os.pardir, "error.txt"))
    with open(parent, "wb") as error:
        error.write(out.stdout)
