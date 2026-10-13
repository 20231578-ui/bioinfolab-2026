# FASTA 도구 모음
 
## 함수 목록
 
### 1. read_fasta(filename)

FASTA 파일을 읽어서 '{이름: 서열}' 형태의 딕셔너리로 돌려준다. 

ex) 

'''python
seqs = read_fasta("data/seqs.fasta")

### 2. gc_content(seq)

주어진 서열에서 G와 C가 차지하는 비율을 계산해서 돌려준다. 

### 3. write_fasta(seqs, filename)

{이름: 서열} 형태를 가진 딕셔너리를 FASTA 파일로 저장한다. 

### 4. length_stats(seqs)

FASTA 서열의 개수, 전체 길이, 평균 길이, 가장 짧은 길이, 가장 긴 길이를 딕셔너리로 돌려준다. ㅒ

