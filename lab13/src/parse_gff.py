import sys
 
def read_gff(filename):
    features = []
 
    with open(filename) as f:
        for line in f:
            line = line.rstrip()
 
            if line.startswith("##FASTA"):
                break
            if line.startswith("#") or line == "":
                continue
 
            cols = line.split("\t")
            if len(cols) < 9:
                continue
 
            feature = {
                "seqid": cols[0],
                "type": cols[2],
                "start": int(cols[3]),
                "end": int(cols[4]),
                "strand": cols[6],
                "attributes": cols[8]
            }
            features.append(feature)
 
    return features
 
features = read_gff(sys.argv[1])
print("주석 개수:", len(features))
print("첫 주석:", features[0])