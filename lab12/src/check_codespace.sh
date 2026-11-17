#!/usr/bin/env bash
# =============================================================
#  Codespace 사용 확인 스크립트
#  사용법:  bash src/check_codespace.sh
#  결과는 doc/check_result.txt 에 저장된다.
# =============================================================

OUT="doc/check_result.txt"
mkdir -p doc

{
echo "=============================================="
echo " Codespace 사용 확인 결과"
echo "=============================================="
echo "생성 시각 : $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "사용자    : $(whoami)"
echo "호스트    : $(hostname)"
echo "작업 위치 : $(pwd)"
echo ""

echo "--- 1. 저장소 정보 ---"
REMOTE=$(git config --get remote.origin.url 2>/dev/null)
echo "원격 저장소 : ${REMOTE:-없음}"
echo "현재 브랜치 : $(git branch --show-current 2>/dev/null)"
echo "커밋 개수   : $(git rev-list --count HEAD 2>/dev/null || echo 0)"
echo "최근 커밋   : $(git log -1 --pretty='%h %s (%an, %ad)' --date=short 2>/dev/null)"
echo ""

echo "--- 2. 폴더 구조 ---"
for D in lab02 lab02/data lab02/doc lab02/src; do
    if [ -d "$D" ]; then
        N=$(find "$D" -maxdepth 1 -type f | wc -l)
        printf "  [ 있음 ] %-12s 파일 %s개\n" "$D" "$N"
    else
        printf "  [ 없음 ] %-12s\n" "$D"
    fi
done
echo ""

echo "--- 3. 만든 파일 목록 ---"
if [ -d lab02 ]; then
    find lab02 -type f -not -name '.gitkeep' | sort | sed 's/^/  /'
else
    echo "  lab02 폴더가 없습니다."
fi
echo ""

echo "--- 4. 도구 확인 ---"
for T in python3 seqkit fastqc fastp blastn mafft iqtree; do
    if command -v "$T" > /dev/null 2>&1; then
        printf "  [ OK ] %s\n" "$T"
    else
        printf "  [ 없음 ] %s\n" "$T"
    fi
done
echo ""

echo "--- 5. 명령어 실행 결과 ---"
echo "  python3 --version : $(python3 --version 2>&1)"
echo "  파일시스템 루트   : $(ls / | tr '\n' ' ')"
echo ""

echo "--- 6. 확인 코드 ---"
# 사용자 이름과 저장소 주소로 만든 값. 학생마다 다르다.
CODE=$(printf '%s|%s' "$(whoami)" "$REMOTE" | md5sum 2>/dev/null | cut -c1-12)
echo "  확인 코드 : ${CODE:-계산실패}"
echo ""
echo "=============================================="
echo " 이 파일을 git으로 올리고 구글클래스룸에도 제출한다."
echo "=============================================="
} > "$OUT"

cat "$OUT"
echo ""
echo ">>> 결과가 $OUT 에 저장되었습니다."
