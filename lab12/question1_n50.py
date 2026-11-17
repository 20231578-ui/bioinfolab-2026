# contig 길이 목록
contigs = [12, 3, 20, 8, 1, 15, 6]

# 1. 길이를 내림차순으로 정렬
sorted_contigs = sorted(contigs, reverse=True)
print("1. 내림차순 정렬:", sorted_contigs)

# 2. 전체 길이와 그 절반 계산
total = sum(sorted_contigs)
half = total / 2
print(f"2. 전체 길이: {total}, 절반: {half}")

# 3. 큰 contig부터 누적해서 더하기
print("3. 누적 합 계산:")
cumulative = 0
n50 = None
for length in sorted_contigs:
    cumulative += length
    print(f"   + {length:>2} -> 누적 {cumulative}")
    # 4. 누적 길이가 절반 이상이 되는 순간의 contig 길이가 N50
    if cumulative >= half:
        n50 = length
        print(f"   누적 {cumulative} >= 절반 {half} 이므로 여기서 멈춤")
        break

print(f"4. N50 = {n50}")
