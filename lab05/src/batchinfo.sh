#!/usr/bin/bash

echo -e "file\tcount"

for F in data/*.fasta

do 
    echo -e "$(echo "$F" | cut -d "/" -f 2)\t$(grep -c ">" "$F")"
done