SEQ="ATGCGATACGCTTGA"
LEN=${#SEQ}
GC=$(echo "$SEQ" | grep -o "[GC]" | wc -l)
 
echo "scale=4; $GC / $LEN" | bc