def gc_content(seq):
    gc = seq.count("G") + seq.count("C")
    return gc / len(seq)
 
# 부르기
print(gc_content("ATGCGATACGCTTGA"))
print(gc_content("GGGGCCCC"))