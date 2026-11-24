import sys

STOPS = ["TAA", "TAG", "TGA"]

# 상보 염기 대응표 (N 등 그 외 문자는 그대로 둔다)
COMPLEMENT = {"A": "T", "T": "A", "G": "C", "C": "G"}

def reverse_complement(seq):
    """서열의 역상보 서열을 돌려준다."""
    return "".join(COMPLEMENT.get(base, base) for base in reversed(seq))

def find_orfs(seq, frame):
    orfs = []
    start = None

    for i in range(frame, len(seq) - 2, 3):
        codon = seq[i:i + 3]

        if codon == "ATG" and start is None:
            start = i
        elif codon in STOPS and start is not None:
            orfs.append((start, i + 3))
            start = None

    return orfs

def print_orfs(seq, label):
    """한 가닥 서열의 세 틀에서 ORF를 찾아 출력한다."""
    for frame in [0, 1, 2]:
        orfs = find_orfs(seq, frame)
        print(label, "틀", frame + 1, ":", orfs)
        for s, e in orfs:
            print("   ", seq[s:e], "길이", e - s)

seq = sys.argv[1].upper()

# 정방향 가닥 (+1, +2, +3 틀)
print_orfs(seq, "정방향(+)")

# 역상보 가닥 (-1, -2, -3 틀)
# 위치는 역상보 서열 기준 좌표이다.
rc_seq = reverse_complement(seq)
print_orfs(rc_seq, "역상보(-)")
