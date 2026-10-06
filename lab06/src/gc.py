seq = "ATGCGATACGCTTGA"
gc = seq.count("G") + seq.count("C")
 
print("길이:", len(seq))
print("GC 개수:", gc)
print("GC 비율:", gc / len(seq))
print("GC 비율(넷째 자리):", round(gc / len(seq), 4))