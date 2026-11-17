def count_kmers(L, k):
    """서열 길이 L에서 길이 k인 k-mer의 개수를 반환한다."""
    # k가 L보다 크면 k-mer를 하나도 만들 수 없으므로 0
    if k > L:
        return 0
    return L - k + 1


def count_kmers_by_sliding(L, k):
    """길이 L인 서열에서 창(window)을 한 칸씩 밀며 k-mer를 직접 세어 본다."""
    seq = "A" * L  # 개수만 세면 되므로 임의의 서열 사용
    count = 0
    i = 0
    # 창의 끝(i + k)이 서열 끝을 넘지 않는 동안 반복
    while i + k <= len(seq):
        kmer = seq[i:i + k]
        count += 1
        i += 1
    return count


# 여러 (L, k) 조합에 대해 직접 센 결과와 함수 결과 비교
test_cases = [(10, 3), (10, 1), (10, 10), (5, 6), (20, 4), (1, 1), (0, 1), (100, 25)]

print(f"{'L':>4} {'k':>4} {'직접 계산':>8} {'함수 결과':>8}  일치")
all_ok = True
for L, k in test_cases:
    expected = count_kmers_by_sliding(L, k)
    result = count_kmers(L, k)
    ok = expected == result
    all_ok = all_ok and ok
    print(f"{L:>4} {k:>4} {expected:>10} {result:>10}  {'O' if ok else 'X'}")

print("모든 조합 일치:", all_ok)
