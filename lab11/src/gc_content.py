"""
gc_content.py
FASTQ 파일의 각 read에 대해 GC 비율과 평균 품질 점수를 계산하고,
GC 비율이 가장 낮은/높은 read 그룹의 품질이 전체 평균과 어떻게 다른지 비교한다.

사용법:
    python src/gc_content.py data/SRR1553607_1.fastq

출력 순서:
    1) read별 결과: 이름<TAB>GC비율(%)<TAB>평균품질
    2) 요약: 전체 평균 품질, GC 하위 10개 / 상위 10개 그룹의 평균 품질과 비교
"""

import sys

# 낮은/높은 그룹에서 고를 read의 개수
GROUP_SIZE = 10


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


def gc_percent(seq):
    """
    서열의 GC 비율(%)을 계산한다.
        GC 비율 = (G 개수 + C 개수) / 전체 염기 수 × 100

    소문자(g, c)로 적힌 서열도 있을 수 있으므로 upper()로 대문자로 바꾼 뒤 센다.
    길이가 0인 서열은 나눗셈을 할 수 없으므로 0.0을 돌려준다.
    """
    if len(seq) == 0:
        return 0.0
    seq = seq.upper()
    gc_count = seq.count("G") + seq.count("C")
    return gc_count / len(seq) * 100


def mean_quality(qual):
    """
    품질 문자열의 평균 Phred 품질 점수를 계산한다.

    FASTQ(Phred+33 방식)에서는 "품질 점수 + 33"을 ASCII 문자로 저장한다.
    따라서 문자의 ASCII 코드(ord)에서 33을 빼면 원래 점수가 된다.
        예) 'I' -> 73 - 33 = 40,  '#' -> 35 - 33 = 2
    """
    if len(qual) == 0:
        return 0.0
    scores = []
    for ch in qual:
        scores.append(ord(ch) - 33)
    return sum(scores) / len(scores)


def average(values):
    """숫자 리스트의 평균을 구한다. 리스트가 비어 있으면 0.0을 돌려준다."""
    if len(values) == 0:
        return 0.0
    return sum(values) / len(values)


# ---------------- 메인 실행 부분 ----------------

# 명령행 인자가 없으면 사용법을 알려주고 종료한다.
if len(sys.argv) < 2:
    print("사용법: python gc_content.py <FASTQ 파일>", file=sys.stderr)
    sys.exit(1)

reads = read_fastq(sys.argv[1])

# read가 하나도 없으면 더 계산할 것이 없으므로 종료한다.
if len(reads) == 0:
    print("read가 없습니다.")
    sys.exit(0)

# ---- 1) read별 GC 비율과 평균 품질 계산 및 출력 ----
# results에는 (원래 순서 번호, 이름, GC 비율, 평균 품질)을 저장한다.
# 원래 순서 번호(index)는 아래에서 GC 비율이 같은 read를 정렬할 때 사용한다.
results = []
print("read_name\tGC(%)\tmean_quality")
for index, (name, seq, qual) in enumerate(reads):
    gc = gc_percent(seq)
    mq = mean_quality(qual)
    results.append((index, name, gc, mq))
    print(f"{name}\t{gc:.2f}\t{mq:.2f}")

# ---- 2) 전체 read의 평균 품질 ----
# 각 read의 평균 품질을 다시 평균 낸 값이다. (read 하나를 1표로 취급)
all_quals = [mq for index, name, gc, mq in results]
overall_mean = average(all_quals)

# ---- 3) GC 비율 기준 정렬 ----
# 정렬 기준(key)을 (GC 비율, 원래 순서 번호)로 준다.
#   - 먼저 GC 비율이 낮은 순서로 정렬하고,
#   - GC 비율이 같으면 파일에 먼저 나온 read를 앞에 둔다.
# 이렇게 하면 동점이 있어도 실행할 때마다 항상 같은 결과가 나온다.
sorted_low = sorted(results, key=lambda r: (r[2], r[0]))

# GC가 높은 그룹은 GC 비율이 높은 순서로 정렬한다.
# -r[2]로 GC 비율만 내림차순으로 만들고, 동점일 때는 역시 파일 순서(r[0])를 따른다.
sorted_high = sorted(results, key=lambda r: (-r[2], r[0]))

# 리스트 슬라이싱 [:10]은 리스트 길이가 10보다 짧아도 오류가 나지 않고
# 있는 만큼만 가져온다. 그래서 read가 10개 미만이어도 안전하다.
low_group = sorted_low[:GROUP_SIZE]
high_group = sorted_high[:GROUP_SIZE]

low_mean = average([r[3] for r in low_group])
high_mean = average([r[3] for r in high_group])

# ---- 4) 요약 출력 ----
print()
print("===== 요약 =====")
print(f"전체 read 수\t{len(results)}")
print(f"전체 평균 품질\t{overall_mean:.2f}")

# read 수가 GROUP_SIZE의 2배보다 적으면 두 그룹에 같은 read가 겹쳐 들어간다.
if len(results) < GROUP_SIZE * 2:
    print(f"주의: read가 {GROUP_SIZE * 2}개 미만이라 GC 하위/상위 그룹에 겹치는 read가 있을 수 있습니다.")

print()
print(f"[GC 비율 하위 {len(low_group)}개 read]")
for index, name, gc, mq in low_group:
    print(f"{name}\t{gc:.2f}\t{mq:.2f}")
print(f"평균 품질\t{low_mean:.2f}\t(전체 대비 {low_mean - overall_mean:+.2f})")

print()
print(f"[GC 비율 상위 {len(high_group)}개 read]")
for index, name, gc, mq in high_group:
    print(f"{name}\t{gc:.2f}\t{mq:.2f}")
print(f"평균 품질\t{high_mean:.2f}\t(전체 대비 {high_mean - overall_mean:+.2f})")
