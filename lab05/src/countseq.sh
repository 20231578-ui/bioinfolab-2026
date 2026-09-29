#!/usr/bin/bash
# countseq.sh — FASTA 파일의 서열 개수를 출력한다
# 사용법: countseq.sh <FASTA파일>

if [ -z "$1" ]
then
    echo "사용법: $0 <FASTA파일>"
    echo " 주어진 FASTA 파일의 서열 개수를 출력합니다."
    exit 1
fi

if [ ! -f "$1" ]
then
    echo "오류: 파일을 찾을 수 없습니다: $1"
    exit 1
fi

FILE="$1"
grep -c ">" "$FILE"