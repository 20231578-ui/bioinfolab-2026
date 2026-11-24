"""정방향 세 틀과 역방향(역상보) 세 틀, 모두 여섯 개 번역틀에서 ORF를 찾는다.

사용법: python find_orf.py <DNA 서열>

[좌표 표시 방식]
- 모든 ORF의 위치는 '원래 입력 서열(정방향)' 기준으로 표시한다.
- GFF / Prokka 결과와 같게 1부터 세고, 끝 위치를 포함한다. (시작 <= 끝)
- 가닥은 +/- 로 따로 표시한다. 역방향(-) ORF는 원래 서열에서
  '끝' 쪽에 시작코돈(ATG의 상보 서열 CAT)이, '시작' 쪽에 정지코돈이 있다.

[역방향 좌표 변환]
서열 길이를 L, 역상보 서열에서 찾은 ORF를 [s, e) (0부터, 끝 미포함)라 하면
역상보를 만들 때 서열을 뒤집으므로 양 끝이 바뀌어
원래 서열 기준으로는 [L - e, L - s) 가 된다.
즉 reverse_complement(seq[L-e : L-s]) == rc_seq[s:e] 이다.
출력할 때는 1부터 세므로 (L - e + 1) ~ (L - s) 로 표시한다.
"""
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

def to_forward_coords(s, e, length):
    """역상보 서열 기준 [s, e) 좌표를 원래 서열 기준 [시작, 끝) 좌표로 바꾼다."""
    return length - e, length - s

def find_all_orfs(seq):
    """여섯 틀에서 ORF를 찾아 (가닥, 틀, 시작, 끝, ORF 서열) 목록으로 돌려준다.

    시작/끝은 원래 서열 기준 0부터 세는 [시작, 끝) 좌표이다.
    ORF 서열은 시작코돈부터 정지코돈까지 읽는 방향 그대로의 서열이다.
    """
    results = []
    length = len(seq)

    # 정방향 가닥 (+1, +2, +3 틀): 좌표를 그대로 쓴다.
    for frame in [0, 1, 2]:
        for s, e in find_orfs(seq, frame):
            results.append(("+", "+" + str(frame + 1), s, e, seq[s:e]))

    # 역상보 가닥 (-1, -2, -3 틀): 원래 서열 기준 좌표로 바꾼다.
    rc_seq = reverse_complement(seq)
    for frame in [0, 1, 2]:
        for s, e in find_orfs(rc_seq, frame):
            start, end = to_forward_coords(s, e, length)
            orf_seq = rc_seq[s:e]
            # 확인: 원래 서열의 해당 구간을 역상보하면 같은 ORF 서열이어야 한다.
            assert reverse_complement(seq[start:end]) == orf_seq
            results.append(("-", "-" + str(frame + 1), start, end, orf_seq))

    return results

def print_orfs(results):
    """ORF 목록을 1부터 세는 GFF 방식 좌표로 출력한다."""
    print("가닥", "틀", "시작", "끝", "길이", "서열", sep="\t")
    for strand, frame, start, end, orf_seq in results:
        # 0부터 세는 [start, end) -> 1부터 세고 끝 포함 (start+1 ~ end)
        print(strand, frame, start + 1, end, end - start, orf_seq, sep="\t")

if __name__ == "__main__":
    seq = sys.argv[1].upper()
    print("서열 길이:", len(seq))
    print_orfs(find_all_orfs(seq))
