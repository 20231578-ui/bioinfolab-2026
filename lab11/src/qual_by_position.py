"""
qual_by_position.py
FASTQ 파일의 모든 read를 읽어서, read 안의 "위치(position)"별 평균 품질 점수를 계산한다.

사용법:
    python src/qual_by_position.py data/SRR1553607_1.fastq

출력 형식 (탭으로 구분):
    위치<TAB>평균품질
    1       31.25
    2       31.80
    ...
"""

import sys


def read_fastq(filename):
    """
    FASTQ 파일을 읽어서 (이름, 서열, 품질문자열) 튜플의 리스트로 돌려준다.

    FASTQ 파일은 read 하나가 항상 4줄로 이루어져 있다.
        1번째 줄: @read이름
        2번째 줄: 염기서열 (예: ACGT...)
        3번째 줄: + (구분용 줄)
        4번째 줄: 품질 문자열 (서열의 각 염기마다 문자 1개씩)
    """
    records = []
    with open(filename) as f:
        lines = f.readlines()

    # 4줄씩 건너뛰면서 read 하나씩 처리한다.
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]   # 맨 앞의 '@'를 떼어낸다.
        seq = lines[i + 1].rstrip()    # 줄 끝의 줄바꿈 문자를 제거한다.
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))

    return records


def qual_to_scores(qual):
    """
    품질 문자열을 Phred 품질 점수(정수) 리스트로 바꾼다.

    FASTQ(Phred+33 방식)에서는 품질 점수에 33을 더한 값을 ASCII 문자로 저장한다.
    따라서 문자의 ASCII 코드(ord)에서 33을 빼면 원래 품질 점수가 된다.
        예) 'I' -> ord('I') = 73 -> 73 - 33 = 40
            '#' -> ord('#') = 35 -> 35 - 33 = 2
    """
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return scores


def mean_quality_by_position(reads):
    """
    모든 read에서 같은 위치의 품질 점수끼리 모아 위치별 평균을 계산한다.

    read마다 길이가 다를 수 있으므로(예: trimming 후),
    각 위치마다 "그 위치까지 길이가 있는 read의 개수"로 나누어야 한다.
    이를 위해 위치별로 두 개의 리스트를 관리한다.
        totals[i] : i번째 위치 품질 점수의 합계
        counts[i] : i번째 위치에 실제로 염기가 있는 read의 개수
    """
    totals = []
    counts = []

    for name, seq, qual in reads:
        scores = qual_to_scores(qual)

        # enumerate는 (위치 번호, 값)을 함께 준다. 위치 번호는 0부터 시작한다.
        for i, score in enumerate(scores):
            # 지금까지 본 read보다 더 긴 read가 나오면 리스트를 한 칸 늘려 준다.
            if i >= len(totals):
                totals.append(0)
                counts.append(0)

            totals[i] += score   # 이 위치의 점수를 합계에 더한다.
            counts[i] += 1       # 이 위치에 read가 하나 더 있음을 센다.

    # 위치별 평균 = 합계 / 그 위치에 존재하는 read 수
    means = []
    for i in range(len(totals)):
        means.append(totals[i] / counts[i])

    return means


# ---------------- 메인 실행 부분 ----------------

# 명령행 인자가 없으면 사용법을 알려주고 종료한다.
if len(sys.argv) < 2:
    print("사용법: python qual_by_position.py <FASTQ 파일>", file=sys.stderr)
    sys.exit(1)

reads = read_fastq(sys.argv[1])
means = mean_quality_by_position(reads)

# 위치는 사람이 읽기 쉽게 1부터 출력한다. (파이썬 인덱스는 0부터 시작)
for i, mean in enumerate(means):
    print(f"{i + 1}\t{mean:.2f}")
