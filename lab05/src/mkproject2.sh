#!/usr/bin/bash
# 프로젝트 폴더와 사용법을 출력한다. 
set -x
 
NAME=$1

if [ -z "$NAME" ]; then
    echo "사용법: $0 <폴더이름>"
    exit 1
fi

if [ -d "$NAME" ]
    then echo "오류: $NAME 폴더가 이미 있습니다."
    exit 1
fi

mkdir "$NAME"
echo "$NAME 폴더를 만들었습니다"