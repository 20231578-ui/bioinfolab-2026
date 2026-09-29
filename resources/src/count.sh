#!/usr/bin/bash
# count.sh — 파일의 줄 수를 센다
# 사용법: bash src/count.sh <파일>

FILE=$1

wc -l $FILE
