# qual_summary.py 사용 설명서

> 대상 파일: `lab11/src/qual_summary.py`
> 대상 독자: Python과 생물정보학을 처음 배우는 사람

---

## 1. 프로그램의 목적

`qual_summary.py`는 **FASTQ 파일을 읽어서 모든 read의 품질 점수(quality score)를 계산하고, 파일 전체의 평균 품질을 숫자 하나로 보여 주는 프로그램**입니다.

시퀀싱 장비가 읽은 염기 하나하나에는 "이 염기를 얼마나 정확하게 읽었는가"를 나타내는 품질 점수가 붙어 있습니다. 이 프로그램은 그 점수를 모두 모아 다음 한 가지를 알려 줍니다.

| 출력 항목 | 의미 |
|---|---|
| 전체 read 평균 품질 | 각 read의 평균 품질 점수를 구한 뒤, 그 값들을 다시 평균 낸 값 |

즉, "이 FASTQ 데이터가 전반적으로 믿을 만한 품질인가?"를 빠르게 확인하는 용도입니다. `parse_fastq.py`가 파일의 **내용**을 확인했다면, `qual_summary.py`는 파일의 **품질**을 확인합니다.

---

## 2. 배경 지식: FASTQ 구조와 Phred 품질 점수

### 2-1. FASTQ 파일 구조 (복습)

FASTQ 파일은 **4줄이 모여서 하나의 read**를 이룹니다. 실제 `lab11/data/SRR1553607_1.fastq` 파일의 첫 4줄은 다음과 같습니다.

```
@SRR1553607.1 1 length=101
GTTAGCGTTGTTGATCGCGACGCAACAACTGGTAAAGAATCTGGAAGAAGGATATCAGTTCAAACGCTCAAGCGAGATGATGGATATTTTTGAACGACTCA
+SRR1553607.1 1 length=101
BB@FFFFFHHHHHJJJJJJJJJJJJJJJJJJJGHIJJJJJJJJJHHHHHFFFFFEEEEEEEEEDDDDDDDDDDDDDDDDDEDDDDEDEEEDDDDDDDDDDD
```

| 줄 번호 | 내용 |
|---|---|
| 1번째 줄 | `@` + read 이름(ID) |
| 2번째 줄 | 염기서열 (A, C, G, T, N) |
| 3번째 줄 | `+` 구분선 |
| 4번째 줄 | **품질 문자열** ← 이 프로그램이 주로 사용하는 줄 |

2번째 줄(서열)과 4번째 줄(품질)의 길이는 항상 같습니다. 염기 하나에 품질 문자 하나가 짝을 이룹니다.

### 2-2. 품질 문자를 숫자로 바꾸는 방법 (Phred+33)

품질 문자열의 각 글자는 **숫자 점수를 문자로 바꿔 적은 것**입니다. 다음 공식으로 다시 숫자로 바꿉니다.

```
품질 점수(Q) = 문자의 ASCII 코드값 − 33
```

Python에서는 `ord()` 함수가 문자의 ASCII 코드값을 알려 줍니다.

| 품질 문자 | `ord(문자)` | Q = ord − 33 | 오류 확률 | 정확도 |
|---|---|---|---|---|
| `#` | 35 | 2 | 약 63% | 매우 낮음 |
| `+` | 43 | 10 | 1/10 | 90% |
| `5` | 53 | 20 | 1/100 | 99% |
| `?` | 63 | 30 | 1/1,000 | 99.9% |
| `B` | 66 | 33 | 약 1/2,000 | 99.95% |
| `I` | 73 | 40 | 1/10,000 | 99.99% |
| `J` | 74 | 41 | 약 1/12,600 | 99.992% |

Phred 점수 Q와 오류 확률 P의 관계는 `Q = −10 × log10(P)`입니다. **Q가 10 오르면 오류 확률은 10분의 1로 줄어듭니다.**

일반적인 기준은 다음과 같습니다.

- **Q30 이상**: 좋은 품질 (오류 1/1,000 이하)
- **Q20 ~ 30**: 보통 품질
- **Q20 미만**: 낮은 품질. 분석 전에 잘라내거나(trimming) 걸러내는(filtering) 경우가 많음

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
 7      for i in range(0, len(lines), 4):
 8          name = lines[i].rstrip()[1:]
 9          seq = lines[i + 1].rstrip()
10          qual = lines[i + 3].rstrip()
11          records.append((name, seq, qual))
12      return records
13
14  def mean_quality(qual):
15      scores = []
16      for ch in qual:
17          scores.append(ord(ch) - 33)
18      return sum(scores) / len(scores)
19
20  reads = read_fastq(sys.argv[1])
21
22  total = 0
23  for name, seq, qual in reads:
24      q = mean_quality(qual)
25      total = total + q
26
27  print("전체 read 평균 품질:", total / len(reads))
```

프로그램은 크게 세 부분으로 나뉩니다.

| 부분 | 줄 | 역할 |
|---|---|---|
| ① `read_fastq` 함수 | 3 ~ 12 | FASTQ 파일을 읽어 (이름, 서열, 품질) 목록으로 정리 |
| ② `mean_quality` 함수 | 14 ~ 18 | 품질 문자열 하나의 평균 점수 계산 |
| ③ 메인 실행부 | 20 ~ 27 | 모든 read의 평균 품질을 다시 평균 내어 출력 |

### 1번 줄: `import sys`
`sys` 모듈을 불러옵니다. **명령줄에서 입력한 파일 이름(`sys.argv`)**을 가져올 때 씁니다.

### 2, 13, 19, 21, 26번 줄: 빈 줄
코드를 보기 좋게 나누는 빈 줄입니다. 실행에는 영향이 없습니다.

---

### ① `read_fastq` 함수 (3 ~ 12번 줄)

`parse_fastq.py`에 있던 함수와 **똑같은 함수**입니다. 간단히 정리하면 다음과 같습니다.

### 3번 줄: `def read_fastq(filename):`
파일 경로 `filename`을 받아, 파일 안의 모든 read를 정리한 리스트를 돌려주는 함수를 정의합니다.

### 4번 줄: `records = []`
read 정보를 모아 둘 빈 리스트를 만듭니다.

### 5 ~ 6번 줄: `with open(filename) as f:` / `lines = f.readlines()`
파일을 열어 **모든 줄을 리스트 `lines`에 한꺼번에 저장**합니다. `with` 블록이 끝나면 파일은 자동으로 닫힙니다.

### 7번 줄: `for i in range(0, len(lines), 4):`
`i`를 0, 4, 8, ... 처럼 **4씩 늘리며** 반복합니다. `i`는 항상 각 read의 첫 줄(`@` 줄)을 가리킵니다.

### 8번 줄: `name = lines[i].rstrip()[1:]`
1번째 줄에서 줄바꿈을 지우고(`rstrip()`) 맨 앞의 `@`를 뺀(`[1:]`) **read 이름**을 저장합니다.

### 9번 줄: `seq = lines[i + 1].rstrip()`
2번째 줄, 즉 **염기서열**을 저장합니다.

### 10번 줄: `qual = lines[i + 3].rstrip()`
4번째 줄, 즉 **품질 문자열**을 저장합니다. (3번째 줄 `+`는 건너뜁니다.)

### 11번 줄: `records.append((name, seq, qual))`
세 값을 튜플 하나로 묶어 리스트에 추가합니다.

### 12번 줄: `return records`
완성된 리스트를 돌려줍니다.

---

### ② `mean_quality` 함수 (14 ~ 18번 줄)

이 프로그램에서 **새로 추가된 핵심 함수**입니다.

### 14번 줄: `def mean_quality(qual):`
품질 문자열 `qual` 하나(예: `"BB@FFFFF..."`)를 받아 **그 read의 평균 품질 점수**를 돌려주는 함수를 정의합니다.

### 15번 줄: `scores = []`
각 문자를 숫자로 바꾼 점수를 담을 빈 리스트를 만듭니다.

### 16번 줄: `for ch in qual:`
품질 문자열을 **한 글자씩** 꺼내 `ch`에 넣으며 반복합니다. 문자열에 `for`를 쓰면 글자 단위로 반복됩니다.

### 17번 줄: `scores.append(ord(ch) - 33)`
2-2절의 공식을 그대로 코드로 옮긴 줄입니다.
- `ord(ch)`: 문자의 ASCII 코드값 (예: `ord('B')` → 66)
- `- 33`: Phred+33 방식이므로 33을 뺌 (66 − 33 = **33**)
- `scores.append(...)`: 계산한 점수를 리스트에 추가

예를 들어 품질 문자열이 `"BB@F"`라면 다음과 같습니다.

| ch | ord(ch) | ord(ch) − 33 |
|---|---|---|
| `B` | 66 | 33 |
| `B` | 66 | 33 |
| `@` | 64 | 31 |
| `F` | 70 | 37 |

→ `scores = [33, 33, 31, 37]`

### 18번 줄: `return sum(scores) / len(scores)`
점수의 **합 ÷ 개수 = 평균**을 돌려줍니다.
위 예시라면 (33 + 33 + 31 + 37) / 4 = **33.5**

---

### ③ 메인 실행부 (20 ~ 27번 줄)

### 20번 줄: `reads = read_fastq(sys.argv[1])`
여기서부터 프로그램이 실제로 실행됩니다. 명령줄에서 입력한 파일 이름(`sys.argv[1]`)을 `read_fastq`에 넘겨 모든 read를 `reads`에 저장합니다.
예: `python3 src/qual_summary.py data/SRR1553607_1.fastq` → `sys.argv[1]` = `data/SRR1553607_1.fastq`

### 22번 줄: `total = 0`
각 read의 평균 품질을 **누적해서 더할 변수**를 0으로 준비합니다.

### 23번 줄: `for name, seq, qual in reads:`
`reads` 안의 튜플을 하나씩 꺼내면서 세 값을 각각 `name`, `seq`, `qual`에 나눠 담습니다(튜플 언패킹). 이 반복에서 실제로 쓰는 값은 `qual`뿐입니다.

### 24번 줄: `q = mean_quality(qual)`
현재 read의 품질 문자열로 **그 read의 평균 품질**을 계산합니다.

### 25번 줄: `total = total + q`
계산한 값을 `total`에 더합니다. 반복이 끝나면 `total`에는 **모든 read 평균 품질의 합**이 들어 있습니다.

### 27번 줄: `print("전체 read 평균 품질:", total / len(reads))`
`total`을 read 개수로 나눈 값, 즉 **read별 평균 품질들의 평균**을 출력합니다.

> 계산 흐름 정리
> 품질 문자 → (ord − 33) → 염기별 점수 → (read 안에서 평균) → read별 평균 품질 → (모든 read에 대해 평균) → **전체 평균 품질**

---

## 4. 실행 방법과 실행 예시

### 실행 방법

터미널에서 `lab11` 폴더로 이동한 뒤, 다음 형식으로 실행합니다.

```bash
python3 src/qual_summary.py <FASTQ 파일 경로>
```

### 실행 예시

```bash
cd /workspaces/bioinfolab-2026/lab11
python3 src/qual_summary.py data/SRR1553607_1.fastq
```

실제 출력:

```
전체 read 평균 품질: 33.4497222958299
```

두 번째 파일도 같은 방법으로 실행합니다.

```bash
python3 src/qual_summary.py data/SRR1553607_2.fastq
```

실제 출력:

```
전체 read 평균 품질: 30.830840894308746
```

> 참고: 두 파일은 각각 813,780줄이므로 read는 813,780 ÷ 4 = **203,445개**씩입니다. 실행에는 1초 남짓 걸립니다.

### 손으로 검산해 보기

첫 번째 read(`SRR1553607.1`)의 품질 문자열은 101글자이고, 점수를 모두 더하면 3,781입니다.

```
첫 read 평균 품질 = 3781 / 101 ≈ 37.44
```

이런 계산을 203,445개 read 전부에 대해 하고 평균을 낸 값이 33.45입니다.

### 자주 하는 실수

| 상황 | 결과 | 해결 |
|---|---|---|
| 파일 이름을 입력하지 않음 (`python3 src/qual_summary.py`) | `IndexError: list index out of range` | 실행할 때 FASTQ 파일 경로를 함께 입력 |
| 파일 경로를 잘못 입력 | `FileNotFoundError` | 현재 위치(`pwd`)와 파일 경로 확인 |
| 빈 파일을 입력 | 27번 줄에서 `ZeroDivisionError` (read 개수가 0) | 내용이 있는 FASTQ 파일 사용 |
| 품질 줄이 비어 있는 read가 있음 | 18번 줄에서 `ZeroDivisionError` | 파일이 손상되지 않았는지 확인 |
| `src` 폴더 안에서 실행 | `FileNotFoundError` | `lab11` 폴더에서 실행하거나 `../data/...`로 경로 수정 |

---

## 5. 실행 결과의 의미

| 파일 | 전체 평균 품질 | 오류 확률 (대략) | 해석 |
|---|---|---|---|
| `SRR1553607_1.fastq` (read 1) | **약 33.4** | 약 1/2,200 (정확도 약 99.95%) | Q30을 넘는 **좋은 품질** |
| `SRR1553607_2.fastq` (read 2) | **약 30.8** | 약 1/1,200 (정확도 약 99.92%) | Q30을 겨우 넘는 **양호한 품질** |

### 결과에서 알 수 있는 것

1. **두 파일 모두 평균 Q30 이상**이므로, 전체적으로 분석에 쓸 만한 데이터입니다.
2. **read 2(`_2`)가 read 1(`_1`)보다 품질이 낮습니다.** Illumina paired-end 시퀀싱에서 흔히 나타나는 현상입니다. read 2는 read 1을 다 읽은 뒤에 읽기 때문에, 그동안 시약이 소모되고 신호가 약해져 품질이 조금 떨어집니다.
3. 첫 read 하나의 평균(37.4)이 전체 평균(33.4)보다 높습니다. read마다 품질 차이가 있다는 뜻이고, 품질이 낮은 read도 섞여 있음을 짐작할 수 있습니다.

### 이 숫자만으로는 알 수 없는 것

- **read 안에서 위치별 품질 변화**: 보통 read의 끝부분(3′ 쪽)으로 갈수록 품질이 떨어지는데, 평균 하나로는 이를 볼 수 없습니다.
- **나쁜 read가 몇 개인지**: 평균이 높아도 품질이 아주 낮은 read가 일부 섞여 있을 수 있습니다.

이런 자세한 분석에는 보통 FastQC 같은 전문 도구를 사용합니다.

---

## 부록: 이 프로그램의 한계 (참고용)

- **메모리 사용**: `readlines()`로 파일 전체를 한 번에 메모리에 올리므로, 수 GB 크기의 실제 NGS 파일에서는 느리거나 메모리가 부족할 수 있습니다.
- **"평균의 평균" 방식**: read별 평균을 다시 평균 내므로, read 길이가 서로 다르면 모든 염기의 점수를 한꺼번에 평균 낸 값과 달라질 수 있습니다. (이 데이터처럼 read 길이가 모두 같으면 두 값이 같습니다.)
- **Phred+33만 지원**: 아주 오래된 Illumina 데이터(Phred+64 방식)를 넣으면 점수가 31만큼 높게 잘못 계산됩니다.
- **입력 검사 없음**: 파일 이름 누락, 빈 파일, 4줄 단위가 깨진 파일 등에 대한 오류 처리가 없습니다.
- **사용하지 않는 값**: `name`과 `seq`도 읽어 저장하지만, 품질 계산에는 쓰지 않습니다.
