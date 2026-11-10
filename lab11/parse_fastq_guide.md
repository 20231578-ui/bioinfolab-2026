# parse_fastq.py 사용 설명서

> 대상 파일: `lab11/src/parse_fastq.py`
> 대상 독자: Python과 생물정보학을 처음 배우는 사람

---

## 1. 프로그램의 목적

`parse_fastq.py`는 **FASTQ 파일을 읽어서 그 안에 들어 있는 read(시퀀싱 조각)들을 정리하고, 간단한 요약 정보를 화면에 보여 주는 프로그램**입니다.

차세대 염기서열 분석(NGS) 장비는 DNA를 수백만 개의 짧은 조각(read)으로 읽어 FASTQ 파일로 저장합니다. 이 프로그램은 그런 파일을 열어서 다음 네 가지를 알려 줍니다.

| 출력 항목 | 의미 |
|---|---|
| read 개수 | 파일 안에 들어 있는 read가 모두 몇 개인지 |
| 첫 read 이름 | 파일의 첫 번째 read의 이름(ID) |
| 첫 read 서열 | 첫 번째 read의 염기서열(A, C, G, T, N) |
| 첫 read 길이 | 첫 번째 read 서열이 몇 개의 염기로 되어 있는지 |

즉, "이 FASTQ 파일이 제대로 된 파일인지, 대략 어떤 데이터가 들어 있는지"를 빠르게 확인하는 용도입니다.

---

## 2. FASTQ 파일의 기본 구조

FASTQ 파일은 **4줄이 모여서 하나의 read**를 이룹니다. 이 4줄 묶음이 파일 끝까지 계속 반복됩니다.

실제 `lab11/data/SRR1553607_1.fastq` 파일의 첫 4줄은 다음과 같습니다.

```
@SRR1553607.1 1 length=101
GTTAGCGTTGTTGATCGCGACGCAACAACTGGTAAAGAATCTGGAAGAAGGATATCAGTTCAAACGCTCAAGCGAGATGATGGATATTTTTGAACGACTCA
+SRR1553607.1 1 length=101
BB@FFFFFHHHHHJJJJJJJJJJJJJJJJJJJGHIJJJJJJJJJHHHHHFFFFFEEEEEEEEEDDDDDDDDDDDDDDDDDEDDDDEDEEEDDDDDDDDDDD
```

| 줄 번호 | 시작 문자 | 내용 | 위 예시에서 |
|---|---|---|---|
| 1번째 줄 | `@` | **read 이름(ID)** 과 부가 정보 | `@SRR1553607.1 1 length=101` |
| 2번째 줄 | (없음) | **염기서열** (A, C, G, T, N) | `GTTAGCGTTG...` |
| 3번째 줄 | `+` | 구분선. 뒤에 이름이 다시 붙거나 `+`만 있음 | `+SRR1553607.1 1 length=101` |
| 4번째 줄 | (없음) | **품질 점수(quality)**. 2번째 줄의 각 염기를 얼마나 정확히 읽었는지를 문자 하나로 표현 | `BB@FFFFFHH...` |

알아 두면 좋은 점:

- 2번째 줄(서열)과 4번째 줄(품질)의 **길이는 항상 같습니다.** 염기 하나당 품질 문자 하나가 짝을 이루기 때문입니다.
- 품질 문자는 ASCII 코드값에서 33을 뺀 값이 품질 점수(Phred score)입니다. 예: `J` → 74 − 33 = 41(매우 정확), `B` → 66 − 33 = 33.
- 따라서 파일 전체 줄 수 ÷ 4 = read 개수입니다.
- 참고: 파일 이름의 `_1`, `_2`는 paired-end 시퀀싱에서 같은 DNA 조각을 양쪽 끝에서 읽은 짝(read 1, read 2)을 의미합니다.

---

## 3. 코드 전체 설명 (한 줄씩)

먼저 전체 코드입니다.

```python
 1  import sys
 2
 3  def read_fastq(filename):
 4      records = []
 5      with open(filename) as f:
 6          lines = f.readlines()
 7
 8      for i in range(0, len(lines), 4):
 9          name = lines[i].rstrip()[1:]
10          seq = lines[i + 1].rstrip()
11          qual = lines[i + 3].rstrip()
12          records.append((name, seq, qual))
13
14      return records
15
16  reads = read_fastq(sys.argv[1])
17  print("read 개수:", len(reads))
18  print("첫 read 이름:", reads[0][0])
19  print("첫 read 서열:", reads[0][1])
20  print("첫 read 길이:", len(reads[0][1]))
```

### 1번 줄 — `import sys`
`sys` 모듈을 불러옵니다. 이 프로그램에서는 **명령줄에서 입력한 파일 이름(`sys.argv`)** 을 가져오기 위해 사용합니다.

### 2번 줄 — 빈 줄
코드를 보기 좋게 나누기 위한 빈 줄입니다. 실행에는 영향이 없습니다. (7, 13, 15번 줄도 같습니다.)

### 3번 줄 — `def read_fastq(filename):`
`read_fastq`라는 **함수를 정의**합니다. `filename`(읽을 파일의 경로)을 받아서, 파일 안의 모든 read를 정리한 목록을 돌려줍니다. 3~14번 줄이 이 함수의 몸통입니다.

### 4번 줄 — `records = []`
read 정보를 모아 둘 **빈 리스트**를 만듭니다. 나중에 read 하나를 읽을 때마다 여기에 하나씩 추가합니다.

### 5번 줄 — `with open(filename) as f:`
파일을 **읽기 모드로 엽니다.** `with`를 쓰면 블록이 끝날 때 파일이 자동으로 닫히므로, 따로 `f.close()`를 쓰지 않아도 됩니다.

### 6번 줄 — `lines = f.readlines()`
파일의 **모든 줄을 한꺼번에 읽어서 리스트로 저장**합니다. 예를 들어 `lines[0]`은 첫 번째 줄, `lines[1]`은 두 번째 줄입니다. 각 줄 끝에는 줄바꿈 문자(`\n`)가 붙어 있습니다.

### 8번 줄 — `for i in range(0, len(lines), 4):`
`i`를 **0, 4, 8, 12, ... 처럼 4씩 증가**시키며 반복합니다. FASTQ는 4줄이 read 하나이므로, `i`는 항상 **각 read의 첫 번째 줄(@로 시작하는 줄)** 위치를 가리킵니다.

| 반복 | i | 가리키는 read |
|---|---|---|
| 1회차 | 0 | 1번째 read (0~3번 줄) |
| 2회차 | 4 | 2번째 read (4~7번 줄) |
| 3회차 | 8 | 3번째 read (8~11번 줄) |

### 9번 줄 — `name = lines[i].rstrip()[1:]`
read의 **이름**을 꺼냅니다.
- `lines[i]` : 4줄 중 1번째 줄 (`@SRR1553607.1 1 length=101\n`)
- `.rstrip()` : 줄 끝의 줄바꿈(`\n`)과 공백을 제거
- `[1:]` : 맨 앞 글자 `@`를 빼고 나머지만 가져옴

결과: `SRR1553607.1 1 length=101`

### 10번 줄 — `seq = lines[i + 1].rstrip()`
4줄 중 **2번째 줄(염기서열)** 을 꺼내고 줄 끝의 줄바꿈을 제거합니다.

### (11번 줄에 없는 것) — 3번째 줄 `lines[i + 2]`
3번째 줄(`+`로 시작하는 구분선)은 필요한 정보가 없으므로 **읽지 않고 건너뜁니다.**

### 11번 줄 — `qual = lines[i + 3].rstrip()`
4줄 중 **4번째 줄(품질 점수)** 을 꺼내고 줄 끝의 줄바꿈을 제거합니다.

### 12번 줄 — `records.append((name, seq, qual))`
이름, 서열, 품질 세 가지를 **튜플 하나로 묶어** `records` 리스트에 추가합니다.
예: `("SRR1553607.1 1 length=101", "GTTAGC...", "BB@FFF...")`

### 14번 줄 — `return records`
모든 read를 다 읽은 뒤, 완성된 `records` 리스트를 **함수 밖으로 돌려줍니다.**

### 16번 줄 — `reads = read_fastq(sys.argv[1])`
여기서부터 프로그램이 실제로 실행됩니다.
- `sys.argv`는 명령줄에 입력한 단어들의 리스트입니다.
  예: `python3 src/parse_fastq.py data/SRR1553607_1.fastq` →
  `sys.argv[0]` = `src/parse_fastq.py`, `sys.argv[1]` = `data/SRR1553607_1.fastq`
- 즉 **사용자가 입력한 파일 이름**을 `read_fastq` 함수에 넘기고, 결과를 `reads`에 저장합니다.

### 17번 줄 — `print("read 개수:", len(reads))`
`reads` 리스트의 길이 = **전체 read 개수**를 출력합니다.

### 18번 줄 — `print("첫 read 이름:", reads[0][0])`
`reads[0]`은 첫 번째 read의 튜플, 그 안의 `[0]`은 **이름**입니다.

### 19번 줄 — `print("첫 read 서열:", reads[0][1])`
첫 번째 read 튜플의 `[1]`, 즉 **염기서열**을 출력합니다.

### 20번 줄 — `print("첫 read 길이:", len(reads[0][1]))`
첫 번째 read 서열의 **글자 수(염기 개수)** 를 출력합니다.

> 튜플 번호 정리: `[0]` = 이름, `[1]` = 서열, `[2]` = 품질
> (품질 `[2]`는 저장은 되지만 이 프로그램에서는 출력하지 않습니다.)

---

## 4. 실행 방법과 실행 예시

### 실행 방법

터미널에서 `lab11` 폴더로 이동한 뒤, 다음 형식으로 실행합니다.

```bash
python3 src/parse_fastq.py <FASTQ 파일 경로>
```

### 실행 예시

```bash
cd /workspaces/bioinfolab-2026/lab11
python3 src/parse_fastq.py data/SRR1553607_1.fastq
```

출력 형태 (첫 read 정보는 실제 파일 내용 기준):

```
read 개수: (파일에 들어 있는 read 수)
첫 read 이름: SRR1553607.1 1 length=101
첫 read 서열: GTTAGCGTTGTTGATCGCGACGCAACAACTGGTAAAGAATCTGGAAGAAGGATATCAGTTCAAACGCTCAAGCGAGATGATGGATATTTTTGAACGACTCA
첫 read 길이: 101
```

두 번째 파일도 같은 방법으로 실행할 수 있습니다.

```bash
python3 src/parse_fastq.py data/SRR1553607_2.fastq
```

> 팁: read 개수가 맞는지 확인하고 싶다면 `wc -l data/SRR1553607_1.fastq`로 줄 수를 구한 뒤 4로 나눠 보세요. 같은 값이 나와야 합니다.

### 자주 하는 실수

| 상황 | 결과 | 해결 |
|---|---|---|
| 파일 이름을 입력하지 않음 (`python3 src/parse_fastq.py`) | `IndexError: list index out of range` | 실행할 때 FASTQ 파일 경로를 꼭 함께 입력 |
| 파일 경로를 잘못 입력 | `FileNotFoundError` | 현재 위치(`pwd`)와 파일 경로 확인 |
| 빈 파일을 입력 | 18번 줄에서 `IndexError` | 내용이 있는 FASTQ 파일 사용 |
| `src` 폴더 안에서 실행 | `FileNotFoundError` | `lab11` 폴더에서 실행하거나 `../data/...`로 경로 수정 |

---

## 5. 실행 결과의 의미

| 출력 | 의미 | 예시 값 해석 |
|---|---|---|
| **read 개수** | 파일에 담긴 read(시퀀싱 조각)의 총 개수. 파일 전체 줄 수 ÷ 4와 같습니다. 데이터 양을 가늠하는 기본 지표입니다. | 값이 클수록 시퀀싱 데이터가 많다는 뜻 |
| **첫 read 이름** | 첫 번째 read의 식별자. 맨 앞 `@`는 제거된 상태로 출력됩니다. | `SRR1553607.1 1 length=101` → `SRR1553607`은 NCBI SRA 실행(run) 번호, `.1`은 그 안의 1번째 read, `length=101`은 길이 101 |
| **첫 read 서열** | 시퀀서가 읽은 실제 DNA 염기서열 | A, C, G, T(판독 불가 시 N)로 구성 |
| **첫 read 길이** | 첫 read 서열의 염기 개수 | `101` → 101bp(염기쌍) 길이의 read. 이름의 `length=101`과 일치하므로 파일이 올바르게 읽혔음을 알 수 있음 |

---

## 부록: 이 프로그램의 한계 (참고용)

- **메모리 사용**: `readlines()`로 파일 전체를 한 번에 메모리에 올리므로, 수 GB 크기의 실제 NGS 파일에서는 느리거나 메모리가 부족할 수 있습니다.
- **입력 검사 없음**: 파일 이름 누락, 빈 파일, 4줄 단위가 깨진 파일 등에 대한 오류 처리가 없습니다.
- **품질 정보 미사용**: 품질 점수(`qual`)를 저장하지만 출력하거나 분석하지는 않습니다.
- **첫 read만 확인**: 길이는 첫 read만 보여 주므로, 모든 read의 길이가 같은지는 알 수 없습니다.
