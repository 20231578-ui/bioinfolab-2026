"""GFF3 주석의 좌표로 contigs.fa에서 유전자 염기 서열을 잘라 FASTA로 출력한다.

사용법: python extract_gene.py <유전자 이름 또는 ID> [GFF 파일] [FASTA 파일]
  예) python src/extract_gene.py deoB
      python src/extract_gene.py EIHNLLIJ_00005 data/sample.gff data/contigs.fa

[좌표 변환]
GFF3 좌표는 1부터 세고, start와 end 위치를 모두 포함한다. (닫힌 구간 [start, end])
파이썬 문자열은 0부터 세고, 슬라이스의 끝 위치는 포함하지 않는다. (반열린 구간 [i, j))
따라서 GFF의 [start, end]는 파이썬에서 seq[start - 1 : end] 이다.
  - 시작: 1부터 세던 start를 0부터 세도록 1을 뺀다.
  - 끝: GFF의 end는 포함, 파이썬 슬라이스의 끝은 미포함이므로 end를 그대로 쓴다.
  - 길이: end - start + 1
역방향(-) 주석도 GFF에서는 항상 start <= end 로 적혀 있으므로
먼저 같은 방법으로 정방향 서열을 자른 뒤 역상보로 바꾸면 유전자 방향의 서열이 된다.
"""
import os
import sys

# lab07/src/fasta.py의 read_fasta를 쓰기 위해 경로를 추가한다.
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(SRC_DIR, "..", "..", "lab07", "src"))

from fasta import read_fasta
from find_orf import reverse_complement

# 기본 입력 파일 (lab13 폴더 기준)
DATA_DIR = os.path.join(SRC_DIR, "..", "data")
DEFAULT_GFF = os.path.join(DATA_DIR, "sample.gff")
DEFAULT_FASTA = os.path.join(DATA_DIR, "contigs.fa")

# 이름/ID로 비교할 속성 키
NAME_KEYS = ["ID", "Name", "gene", "locus_tag"]


def parse_attributes(text):
    """GFF 9번째 열 'key=value;key=value'를 딕셔너리로 바꾼다."""
    attrs = {}
    for item in text.split(";"):
        if "=" in item:
            key, value = item.split("=", 1)
            attrs[key] = value
    return attrs


def read_gff_features(filename):
    """GFF3 파일에서 주석 줄을 읽어 딕셔너리 목록으로 돌려준다."""
    features = []
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
            # ##FASTA 아래는 서열이므로 더 읽지 않는다.
            if line.startswith("##FASTA"):
                break
            if line.startswith("#") or line == "":
                continue
            cols = line.split("\t")
            if len(cols) < 9:
                continue
            features.append({
                "seqid": cols[0],
                "type": cols[2],
                "start": int(cols[3]),
                "end": int(cols[4]),
                "strand": cols[6],
                "attributes": parse_attributes(cols[8]),
            })
    return features


def find_features(features, query):
    """ID, Name, gene, locus_tag 중 하나가 query와 같은 주석을 모두 찾는다."""
    found = []
    for feat in features:
        attrs = feat["attributes"]
        if any(attrs.get(key) == query for key in NAME_KEYS):
            found.append(feat)
    return found


def extract_sequence(contigs, feat):
    """주석 좌표로 서열을 잘라내고, 역방향이면 역상보로 바꾼다."""
    contig_seq = contigs[feat["seqid"]]
    # GFF [start, end] (1부터, 끝 포함) -> 파이썬 [start-1, end) (0부터, 끝 미포함)
    seq = contig_seq[feat["start"] - 1:feat["end"]]
    if feat["strand"] == "-":
        seq = reverse_complement(seq)
    return seq


def fasta_header(feat):
    """'>ID 이름 seqid:start-end(strand)' 형식의 FASTA 헤더를 만든다."""
    attrs = feat["attributes"]
    fid = attrs.get("ID", attrs.get("locus_tag", "unknown"))
    parts = [">" + fid]
    if "Name" in attrs:
        parts.append(attrs["Name"])
    parts.append("{}:{}-{}({})".format(feat["seqid"], feat["start"],
                                       feat["end"], feat["strand"]))
    return " ".join(parts)


def print_fasta(header, seq, width=60):
    """서열을 width 글자씩 줄을 나눠 FASTA 형식으로 출력한다."""
    print(header)
    for i in range(0, len(seq), width):
        print(seq[i:i + width])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python extract_gene.py <유전자 이름 또는 ID> [GFF 파일] [FASTA 파일]",
              file=sys.stderr)
        sys.exit(1)

    query = sys.argv[1]
    gff_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_GFF
    fasta_file = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_FASTA

    matches = find_features(read_gff_features(gff_file), query)
    if not matches:
        print("'{}'에 해당하는 주석을 찾지 못했습니다.".format(query), file=sys.stderr)
        sys.exit(1)

    contigs = read_fasta(fasta_file)
    for feat in matches:
        if feat["seqid"] not in contigs:
            print("FASTA에 '{}' 서열이 없습니다.".format(feat["seqid"]), file=sys.stderr)
            continue
        print_fasta(fasta_header(feat), extract_sequence(contigs, feat))
