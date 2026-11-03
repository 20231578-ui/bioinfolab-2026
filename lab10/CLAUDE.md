lab10/data 폴더에 식물 여덟 종의 rbcL 서열을 NCBI에서 받아 줘.
 
조건:
- wget 과 E-utilities 를 써. 다른 프로그램은 설치하지 마.
- 종마다 esearch 로 찾고, 검색어에 1300:1500[SLEN] 을 넣어.
- 검색 결과의 첫 번째 것만 받아.
- 종마다 FASTA(.fa) 와 GenBank(.gb) 를 둘 다 받아.
- 요청 사이에 sleep 1 을 넣어.
- 파일 이름은 아래 표를 따라.
 
학명-----우리말-----무리-----파일 이름
Arabidopsis thaliana-----애기장대-----속씨식물 쌍떡잎-----rbcL_arabidopsis
Panax ginseng-----인삼-----속씨식물 쌍떡잎-----rbcL_ginseng
Oryza sativa-----벼-----속씨식물 외떡잎-----rbcL_rice
Zea mays-----옥수수-----속씨식물 외떡잎-----rbcL_maize
Ginkgo biloba-----은행나무-----겉씨식물-----rbcL_ginkgo
Pinus thunbergii-----곰솔-----겉씨식물-----rbcL_pine
Adiantum capillus-veneris-----공작고사리-----양치식물-----rbcL_fern
Marchantia polymorpha-----우산이끼-----선태식물-----rbcL_liverwort


 
받기 전에 어떤 명령어를 쓸지 먼저 보여 줘.

## NCBI 에서 서열을 받을 때
- wget 과 E-utilities 를 쓴다. 주소는 반드시 큰따옴표로 감싼다.
- 반복해서 받을 때는 요청 사이에 sleep 1 을 넣는다.
- 유전자 하나를 받을 때는 [SLEN] 으로 길이를 제한한다.
- 받은 파일마다 VERSION 과 ORGANISM 을 확인하고 알려 준다.
- 검색 결과가 없으면 검색어를 바꾸지 말고 먼저 알려 준다.
 
## 라이브러리
- 서열 파일을 읽을 때 Biopython 의 SeqIO 를 써도 된다.
- 그 밖의 새 라이브러리는 쓰기 전에 물어본다.
