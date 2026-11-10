"""
check_paired.py
paired-end FASTQ 파일 두 개(_1, _2)가 올바르게 짝을 이루는지 확인한다.

paired-end 시퀀싱에서는 DNA 조각 하나의 양 끝을 각각 읽어서
두 파일에 나누어 저장한다. 그래서 두 파일은
    - read 개수가 같아야 하고,
    - 같은 순서(위치)에 있는 read끼리 이름이 같아야 한다.
(단, 이름 끝의 /1, /2 나 Illumina 형식의 1:N:..., 2:N:... 같은
 "몇 번째 mate인지" 표시는 서로 다르므로 비교에서 제외한다.)

사용법:
    python src/check_paired.py data/SRR1553607_1.fastq data/SRR1553607_2.fastq
"""

import sys


def read_fastq_names(filename):
    """
    FASTQ 파일을 읽어서 read 이름(헤더 줄)의 리스트를 돌려준다.

    FASTQ 파일은 read 하나가 항상 4줄로 이루어져 있다.
        1번째 줄: @read이름
        2번째 줄: 염기서열
        3번째 줄: + (구분용 줄)
        4번째 줄: 품질 문자열
    짝 확인에는 이름만 필요하므로 1번째 줄만 모은다.
    """
    names = []
    with open(filename) as f:
        # enumerate로 줄 번호(0부터 시작)와 줄 내용을 함께 얻는다.
        for line_no, line in enumerate(f):
            # 줄 번호를 4로 나눈 나머지가 0이면 read의 첫 줄(이름 줄)이다.
            if line_no % 4 == 0:
                line = line.rstrip()       # 줄 끝 줄바꿈 문자 제거
                if line == "":             # 파일 끝의 빈 줄은 건너뛴다.
                    continue
                names.append(line[1:])     # 맨 앞의 '@'를 떼어낸다.
    return names


def base_name(full_name):
    """
    read 이름에서 mate 구분 정보를 제거한 "기본 이름"을 돌려준다.

    예시:
        'SRR1553607.1 1 length=101'           -> 'SRR1553607.1'
        'read123/1'                           -> 'read123'
        'M00123:5:000:1:1101:15589:1331 1:N:0:1'
                                              -> 'M00123:5:000:1:1101:15589:1331'

    방법:
        1) 공백을 기준으로 나눈 첫 번째 덩어리만 사용한다.
           Illumina 형식의 '1:N:0:...' / '2:N:0:...' 나
           SRA 형식의 ' 1 length=101' 같은 부가 정보는
           공백 뒤에 오므로 이 단계에서 사라진다.
        2) 남은 이름이 '/1' 또는 '/2'로 끝나면 그 두 글자를 잘라낸다.
    """
    # split()은 공백(스페이스, 탭)을 기준으로 문자열을 나눈다.
    # [0]은 그중 첫 번째 덩어리, 즉 read의 실제 ID이다.
    name = full_name.split()[0]

    # 예전 Illumina 형식: 이름 끝에 /1, /2 가 붙는다.
    if name.endswith("/1") or name.endswith("/2"):
        name = name[:-2]   # 마지막 두 글자('/1' 또는 '/2')를 잘라낸다.

    return name


def main():
    # 명령행 인자 확인: sys.argv[0]은 스크립트 이름, [1]과 [2]가 파일 경로이다.
    if len(sys.argv) != 3:
        print("사용법: python src/check_paired.py <read1.fastq> <read2.fastq>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    # 1) 두 파일에서 read 이름을 각각 읽는다.
    names1 = read_fastq_names(file1)
    names2 = read_fastq_names(file2)

    count1 = len(names1)
    count2 = len(names2)

    # 짝이 맞는지 기록하는 변수. 문제가 하나라도 발견되면 False로 바꾼다.
    is_paired = True

    # 2) read 개수 비교
    if count1 != count2:
        is_paired = False
        print(f"[개수 불일치] {file1}: {count1}개, {file2}: {count2}개")

    # 3) 같은 위치의 read끼리 이름 비교
    #    두 파일 중 짧은 쪽 길이만큼만 1:1로 비교할 수 있다.
    n_compare = min(count1, count2)
    mismatch_count = 0

    for i in range(n_compare):
        # mate 표시를 뗀 기본 이름끼리 비교한다.
        if base_name(names1[i]) != base_name(names2[i]):
            is_paired = False
            mismatch_count += 1
            # 위치는 사람이 보기 쉽게 1번부터 센다.
            print(f"[이름 불일치] {i + 1}번째 read: "
                  f"'{names1[i]}'  vs  '{names2[i]}'")

    # 4) 개수가 달라서 한쪽에만 남아 있는 read를 출력한다.
    #    (짝이 없는 read들)
    for i in range(n_compare, count1):
        print(f"[짝 없음] {i + 1}번째 read는 {file1}에만 있음: '{names1[i]}'")
    for i in range(n_compare, count2):
        print(f"[짝 없음] {i + 1}번째 read는 {file2}에만 있음: '{names2[i]}'")

    # 5) 최종 결과 출력
    print()
    print("===== 결과 =====")
    print(f"{file1} read 개수: {count1}")
    print(f"{file2} read 개수: {count2}")
    print(f"이름 불일치 개수: {mismatch_count}")
    if is_paired:
        print("paired 여부: O (모든 read가 올바르게 짝을 이룹니다)")
    else:
        print("paired 여부: X (짝이 맞지 않는 read가 있습니다)")


# 이 파일을 직접 실행했을 때만 main()을 호출한다.
if __name__ == "__main__":
    main()
