#!/usr/bin/bash

FILE="$1"
    echo "파일: $FILE"
    echo "서열 개수: $(grep -c ">" "$FILE")"
   

grep ">" "$FILE" | cut -d " " -f1 | tr -d ">"
    echo "총 염기수 (대략): $(grep -v ">" "$FILE" | tr -d "\n" | wc -c)"