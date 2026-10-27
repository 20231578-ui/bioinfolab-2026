"""FASTA 파일의 서열 개수를 출력한다."""
import sys


def count_seqs(filename):
    """FASTA 파일에서 '>'로 시작하는 줄의 개수를 돌려준다."""
    count = 0
    with open(filename) as f:
        for line in f:
            if line.startswith(">"):
                count = count + 1
    return count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 count_agent.py FASTA파일")
        sys.exit(1)
    print(count_seqs(sys.argv[1]))
