#!/usr/bin/bash
set -x
 
for F in data/*.fasta
do
    echo "처리 중: $F"
    grep -c ">" $F
done