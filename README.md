# 생물정보학실험 실습 저장소

Codespaces 로 열면 파이썬과 생물정보학 도구가 설치된 리눅스 환경이 준비된다.

## 시작하기

1. 초록색 `Code` 버튼 → `Codespaces` 탭 → **`New with options...`**
2. **Dev container configuration** 에서 그 주차에 맞는 환경을 고른다.
3. `Create codespace` 를 누른다.
4. 터미널에 환경 확인 결과가 자동으로 표시된다.

`Create codespace on main` 을 그냥 누르면 첫 번째 설정(기본)으로 열린다.
10~11주차처럼 다른 환경이 필요한 주에는 반드시 `New with options...` 를 쓴다.

## 주차별로 고를 환경

| 주차 | 고를 것 | 들어 있는 것 |
|------|---------|--------------|
| 02~07 | 1. 기본 | 파이썬, 리눅스 기본 명령어 |
| conda 실습 | 2. conda 실습 | micromamba (패키지는 직접 설치) |
| 08~09, 12~14 | 3. 서열 분석 | seqkit, blast, mafft, iqtree, fastqc, fastp |
| 10~11 | 4. 유전체 | 위 + shovill, prokka (무겁다) |

환경을 바꾸려면 기존 Codespace 를 지우고 새로 만들면서 다른 것을 고른다.
작업한 파일은 저장소에 커밋되어 있으므로 그대로 따라온다.

## 폴더 규칙

`lab-template` 폴더를 복사하여 주차별 작업 폴더를 만든다.

```
$ cp -r lab-template lab03
$ cd lab03
$ ls
data  doc  src
```

| 폴더 | 넣는 것 |
|------|---------|
| `data` | 내려받거나 만들어 낸 데이터 파일 |
| `doc` | 보고서, 결과 요약, 그림 |
| `src` | 직접 작성한 스크립트 (`.sh`, `.py`) |

## 길을 잃었을 때

```
$ cd
```

인자 없이 `cd` 만 입력하면 실습 작업 폴더로 돌아온다.
진짜 홈 폴더로 가려면 `cd ~` 를 쓴다.

## 매 실습이 끝나면

```
$ git add .
$ git commit -m "lab03 완료"
$ git push
```

그리고 화면 **왼쪽 아래**의 Codespaces 표시를 눌러 `Stop Current Codespace` 를 선택한다.
창을 그냥 닫으면 한동안 켜져 있으면서 무료 사용 시간이 소모된다.

## 주의

- `data` 폴더의 시퀀싱 데이터는 자동으로 저장소에서 제외된다(`.gitignore`).
  필요하면 명령어로 다시 내려받는다.
- 필요한 도구가 없으면 강의자에게 알린다. 직접 설치하지 않는다.
  다만 conda 실습 주차는 예외이며, 그때는 직접 설치하는 것이 과제이다.
