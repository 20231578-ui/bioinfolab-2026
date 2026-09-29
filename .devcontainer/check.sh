#!/usr/bin/env bash
# Codespace 가 처음 만들어질 때 한 번 실행된다.
# 어떤 환경으로 열렸는지, 도구가 들어 있는지 보여 준다.

echo ""
echo "=============================================="
echo "  생물정보학실험 실습 환경"
echo "=============================================="

check() {
    if command -v "$1" > /dev/null 2>&1; then
        printf "  [ OK ] %s\n" "$1"
    else
        printf "  [  -  ] %s\n" "$1"
    fi
}

echo "  기본"
check python3
check git
check wget

echo ""
echo "  conda"
check micromamba

echo ""
echo "  서열 분석"
check seqkit
check blastn
check mafft
check iqtree
check fastqc
check fastp

echo ""
echo "  유전체"
check shovill
check prokka

echo ""
echo "  [  -  ] 표시는 이 환경에 없는 도구입니다. 정상입니다."
echo "  그 주차에 맞는 환경을 골랐는지 확인하세요."
echo ""
echo "  작업 폴더 : ${MYHOME:-$(pwd)}"
echo "  돌아오려면 : cd"
echo "  끝나면 왼쪽 아래에서 Codespace 를 정지하세요."
echo "=============================================="
echo ""
