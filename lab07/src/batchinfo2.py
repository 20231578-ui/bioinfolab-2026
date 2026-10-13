import sys
import glob
from fasta import read_fasta, gc_content

folder = sys.argv[1]
outfile = sys.argv[2]

files = glob.glob(folder + "/*.fasta")

with open(outfile, "w") as out:
    out.write("file\tcount\ttotal\tmean_gc\n")

    for filename in files:
        seqs = read_fasta(filename)

        count = len(seqs)
        total = sum(len(seq) for seq in seqs.values())

        if total > 0:
            gc = sum(
                gc_content(seq) * len(seq)
                for seq in seqs.values()
            ) / total
        else:
            gc = 0

        out.write(
            filename + "\t" +
            str(count) + "\t" +
            str(total) + "\t" +
            str(gc) + "\n"
        )
