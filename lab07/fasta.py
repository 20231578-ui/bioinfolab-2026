def reverse_complement(seq):
    table = {"A": "T", "T": "A", "G": "C", "C": "G"}
    result = ""

    for base in seq:
        result = table[base] + result

    return result
