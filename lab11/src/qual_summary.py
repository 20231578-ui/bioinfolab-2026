import sys
 
def read_fastq(filename):
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records
 
def mean_quality(qual):
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)
 
reads = read_fastq(sys.argv[1])
 
total = 0
for name, seq, qual in reads:
    q = mean_quality(qual)
    total = total + q
 
print("전체 read 평균 품질:", total / len(reads))