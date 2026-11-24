import sys
from parse_gff import read_gff

# GFF 파일을 읽어 모든 주석을 가져온다
features = read_gff(sys.argv[1])

# type이 CDS인 주석만 골라낸다
cds_list = [f for f in features if f["type"] == "CDS"]

# 각 CDS의 길이를 end - start + 1 로 계산한다
for f in cds_list:
    f["length"] = f["end"] - f["start"] + 1

lengths = [f["length"] for f in cds_list]

print()
print("=== CDS 길이 통계 ===")
if len(lengths) == 0:
    print("CDS가 없습니다.")
    sys.exit()

# 개수, 평균, 최소, 최대 길이를 출력한다
print("CDS 개수:", len(lengths))
print("평균 길이:", round(sum(lengths) / len(lengths), 1))
print("최소 길이:", min(lengths))
print("최대 길이:", max(lengths))

# 정방향(+)과 역방향(-)의 개수를 각각 센다
plus = 0
minus = 0
for f in cds_list:
    if f["strand"] == "+":
        plus = plus + 1
    elif f["strand"] == "-":
        minus = minus + 1

print()
print("=== 방향별 개수 ===")
print("정방향(+):", plus)
print("역방향(-):", minus)

# 길이가 긴 순서로 정렬해 상위 다섯 개를 출력한다
longest = sorted(cds_list, key=lambda f: f["length"], reverse=True)[:5]

print()
print("=== 가장 긴 CDS 5개 ===")
for i, f in enumerate(longest, start=1):
    print(f"{i}. {f['seqid']}:{f['start']}-{f['end']} ({f['strand']}) 길이 {f['length']}")
    print("   attributes:", f["attributes"])
