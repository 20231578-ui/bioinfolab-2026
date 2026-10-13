import sys
from fasta import read_fasta, length_stats

seqs = read_fasta(sys.argv[1])
stats = length_stats(seqs)

print("count:", stats["count"])
print("total:", stats["total"])
print("mean:", stats["mean"])
print("min:", stats["min"])
print("max:", stats["max"])
