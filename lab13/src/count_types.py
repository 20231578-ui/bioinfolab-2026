import sys
from parse_gff import read_gff
 
features = read_gff(sys.argv[1])
 
counts = {}
for f in features:
    t = f["type"]
    if t in counts:
        counts[t] = counts[t] + 1
    else:
        counts[t] = 1
 
for t in counts:
    print(t, counts[t], sep="\t")
