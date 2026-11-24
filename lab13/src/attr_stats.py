import sys
from parse_gff import read_gff


def parse_attributes(text):
    # "이름=값;이름=값;..." 형태의 9번째 열을 딕셔너리로 바꾼다
    attrs = {}
    for item in text.split(";"):
        item = item.strip()
        # 빈 항목이나 '='가 없는 항목은 건너뛴다
        if item == "" or "=" not in item:
            continue
        # 값 안에 '='가 있을 수 있으므로 첫 번째 '='에서만 나눈다
        key, value = item.split("=", 1)
        attrs[key] = value
    return attrs


# GFF 파일을 읽어 CDS만 골라낸다
features = read_gff(sys.argv[1])
cds_list = [f for f in features if f["type"] == "CDS"]

total = len(cds_list)
product_count = 0
hypo_count = 0
gene_count = 0

for f in cds_list:
    attrs = parse_attributes(f["attributes"])

    # product 정보가 있는 CDS
    if "product" in attrs:
        product_count = product_count + 1
        # product가 hypothetical protein인 CDS
        if attrs["product"] == "hypothetical protein":
            hypo_count = hypo_count + 1

    # gene 이름이 붙어 있는 CDS
    if "gene" in attrs:
        gene_count = gene_count + 1

print()
print("=== CDS attributes 통계 ===")
print("전체 CDS 개수:", total)
if total == 0:
    print("CDS가 없습니다.")
    sys.exit()

print("product 정보가 있는 CDS:", product_count)
print(f"hypothetical protein CDS: {hypo_count} ({hypo_count / total * 100:.1f}%)")
print("gene 이름이 있는 CDS:", gene_count)
