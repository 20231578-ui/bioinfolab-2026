"""FASTA 파일의 서열 개수를 출력한다."""
import os
import sys

# lab07/src 폴더를 모듈 검색 경로에 추가해 read_fasta를 불러온다
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab07", "src"))
from fasta import read_fasta


def count_seqs(filename):
    """read_fasta로 읽은 서열의 개수를 돌려준다."""
    seqs = read_fasta(filename)
    return len(seqs)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 count_agent2.py FASTA파일")
        sys.exit(1)
    print(count_seqs(sys.argv[1]))
