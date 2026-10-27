# lab07 요약: 함수와 파일

lab07에서는 **함수를 만들어 재사용**하고, 함수들을 **모듈(`fasta.py`)로 모아** 여러 스크립트에서 `import`해 쓰는 방법을 익혔다. 또한 FASTA 파일을 읽고, 결과를 FASTA/TSV 파일로 저장하는 실습을 했다.

## 폴더 구조

```
lab07/
├── data/   # 입력 FASTA (seqs.fasta, seqs2.fasta, lower.fasta)
├── doc/    # 실행 결과 (summary.tsv, batch.tsv, long.fasta)
└── src/    # 함수 모듈과 스크립트
```

## 1. 함수 기초

### `print` vs `return` (`fseqlen.py`)

```python
def length_print(seq):
    print(len(seq))      # 화면에 출력만 하고 None을 돌려줌

def length_return(seq):
    return len(seq)      # 값을 돌려주므로 변수에 저장해 다시 쓸 수 있음
```

- `a = length_print("ATGC")` → `a`는 `None`
- `b = length_return("ATGC")` → `b`는 `4`
- **다른 코드에서 결과를 이어서 쓰려면 `return`을 사용해야 한다.**

### GC 비율 함수 (`fgc.py`)

```python
def gc_content(seq):
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)
```

### 역상보 서열 (`lab07/fasta.py`)

딕셔너리로 염기 짝을 정하고, 앞쪽에 붙여 나가며 서열을 뒤집는다.

```python
def reverse_complement(seq):
    table = {"A": "T", "T": "A", "G": "C", "C": "G"}
    result = ""
    for base in seq:
        result = table[base] + result
    return result
```

## 2. 모듈 만들기: `src/fasta.py`

자주 쓰는 함수를 한 파일에 모아 두고 `from fasta import ...`로 불러 쓴다.

| 함수 | 하는 일 | 반환값 |
|---|---|---|
| `read_fasta(filename)` | FASTA 파일을 읽음 (`>` 줄은 이름, 나머지는 서열을 대문자로 이어 붙임) | `{이름: 서열}` 딕셔너리 |
| `gc_content(seq)` | G+C 비율 계산 (빈 서열이면 0.0) | 0~1 사이 실수 |
| `write_fasta(seqs, filename)` | 딕셔너리를 FASTA 형식으로 저장 | 없음 |
| `length_stats(seqs)` | 서열 길이 통계 | `count`, `total`, `mean`, `min`, `max` 딕셔너리 |

### `if __name__ == "__main__":`

- 파일을 **직접 실행**할 때만 아래 코드가 동작하고, 다른 파일에서 **`import`할 때는 실행되지 않는다.**
- `tool.py`로 이 차이를 확인했고, `fasta.py`는 직접 실행하면 각 서열의 이름·길이·GC 비율을 출력한다.

```bash
python fasta.py ../data/seqs.fasta
```

### 파일 입출력 핵심

```python
with open(filename) as f:          # 읽기 — 블록이 끝나면 자동으로 닫힘
    for line in f:
        line = line.rstrip()       # 줄 끝 개행 제거

with open(filename, "w") as out:   # 쓰기 ("w"는 기존 내용을 덮어씀)
    out.write("text\n")            # 개행은 직접 넣어야 함
```

## 3. 모듈을 활용한 스크립트

모든 스크립트는 `sys.argv`로 명령줄 인자를 받는다. (`sys.argv[0]`은 스크립트 이름, `[1]`부터 사용자 인자)

| 스크립트 | 사용법 | 기능 |
|---|---|---|
| `countseq2.py` | `python countseq2.py 입력.fasta` | 서열 개수 출력 |
| `seqlen2.py` | `python seqlen2.py 입력.fasta` | 각 서열 길이 출력 |
| `stats.py` | `python stats.py 입력.fasta` | 길이 통계(count/total/mean/min/max) 출력 |
| `filter_fasta.py` | `python filter_fasta.py 입력.fasta 최소길이 출력.fasta` | 최소 길이 이상인 서열만 골라 FASTA로 저장 |
| `summary.py` | `python summary.py 입력.fasta 출력.tsv` | 서열별 이름·길이·GC를 TSV로 저장 |
| `batchinfo2.py` | `python batchinfo2.py 폴더 출력.tsv` | 폴더 안 모든 `*.fasta`의 개수·총길이·평균 GC를 TSV로 저장 |

### 사용된 주요 기법

- **필터링**: 조건에 맞는 항목만 새 딕셔너리에 담기 (`filter_fasta.py`)
- **TSV 출력**: 헤더를 먼저 쓰고, 값은 `str()`로 바꿔 `\t`로 연결 (`summary.py`)
- **여러 파일 처리**: `glob.glob(folder + "/*.fasta")`로 파일 목록을 얻어 반복 (`batchinfo2.py`)
- **가중 평균 GC**: 서열마다 GC 비율 × 길이를 더한 뒤 총 길이로 나눔 → 긴 서열이 더 큰 비중을 가짐

## 4. 실행 결과 (`doc/`)

`summary.tsv` — `seqs.fasta`의 서열별 요약

| name | length | gc |
|---|---|---|
| gene1 | 30 | 0.5 |
| gene2 | 15 | 0.4667 |
| gene3 | 22 | 0.5455 |

`long.fasta` — 길이 필터를 통과한 서열(gene1, gene3)만 저장됨 (gene2는 15bp로 제외)

`batch.tsv` — `data/` 폴더의 파일별 요약

| file | count | total | mean_gc |
|---|---|---|---|
| data/seqs2.fasta | 2 | 8 | 0.5 |
| data/seqs.fasta | 3 | 67 | 0.507 |
| data/lower.fasta | 2 | 20 | 0.65 |

> `lower.fasta`처럼 소문자 서열도 `read_fasta`에서 `.upper()`로 변환하므로 GC 계산이 올바르게 된다.

## 5. 정리 및 느낀 점

- 함수로 기능을 나누고 모듈로 묶어 두면, 새 작업은 몇 줄의 스크립트만으로 해결할 수 있다.
- `return`으로 값을 돌려줘야 다른 함수/스크립트에서 재사용할 수 있다.
- 아직 각 함수의 입력과 출력이 익숙하지 않으므로, 예시를 더 실행해 보며 익혀야 한다. (`src/README.md`)
- 보완할 점: `fasta.py`에서 `write_fasta`, `length_stats`가 `if __name__ == "__main__":` 블록 **아래**에 있다. 동작에는 문제없지만, 함수 정의를 모두 위에 두고 실행 블록은 파일 맨 끝에 두는 것이 일반적이다. 또 `length_stats`는 빈 딕셔너리를 받으면 0으로 나누기 오류가 난다.
