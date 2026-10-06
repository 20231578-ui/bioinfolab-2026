import sys

if len(sys.argv) < 3:
    print("사용법: python3 shortlines.py <FASTA파일> <최소길이>")
    sys.exit(1)

filename = sys.argv[1]
minlen = sys.argv[2]

if not minlen.isdigit():
    print("오류: 최소 길이는 숫자여야 합니다.")
    sys.exit(1)

n = 0

with open(filename) as f:
    for line in f:
        line = line.rstrip()

        if not line.startswith(">"):
            if len(line) < int(minlen):
                n = n + 1

print(n)