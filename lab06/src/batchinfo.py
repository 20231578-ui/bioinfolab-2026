import sys
import glob
folder = sys.argv[1]

print("file\tcount")
for path in sorted(glob.glob(folder + "/*.fasta")):
    n = 0
    with open(path) as f:
         for line in f:
             if line.startswith(">"):
                 n = n + 1
    print(path + "\t" + str(n))