SEQ="ATGCGATACGCTTGA"
LEN=${#SEQ}
GC=$(echo "$SEQ" | grep -o "[GC]" | wc -l)
 
echo $(( GC / LEN ))