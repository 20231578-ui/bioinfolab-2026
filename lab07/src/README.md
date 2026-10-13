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

FASTA 서열의 개수, 전체 길이, 평균 길이, 가장 짧은 길이, 가장 긴 길이를 딕셔너리로 돌려준다. 

### 5. 추가하고 싶은 함수/부족한 점

아직 이 함수들을 쓰는 것이 익숙하지 않고, 무엇을 의미하고, 무엇이 출력되는지 아직 정확히 알지 못하기 때문에 부족한 부분을 보완하기 위해 예시로 더 사용하며 공부해야할 것 같다. 

