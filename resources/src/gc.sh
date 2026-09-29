#!/usr/bin/bash
# gc.sh — FASTA 파일의 GC 개수와 비율을 출력한다
# 사용법: bash src/gc.sh

FILE="data/seq.fasta"

SEQ=$(grep -v ">" <"$FILE" | tr -d "\n")

GC=$(echo "$SEQ" | grep -o "[GC]" | wc -l)
LEN=${#SEQ}

echo "길이: $LEN"
echo "GC 개수: $GC"
