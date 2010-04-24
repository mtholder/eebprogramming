#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent import LoadSeqs, DNA, PROTEIN
seqs = {'hum': 'AAGCAGATCCAGGAAAGCAGCGAGAATGGCAGCCTGGCCGCGCGCCAGGAGAGGCAGGCCCAGGTCAACCTCACT',
        'mus': 'AAGCAGATCCAGGAGAGCGGCGAGAGCGGCAGCCTGGCCGCGCGGCAGGAGAGGCAGGCCCAAGTCAACCTCACG',
        'rat': 'CTGAACAAGCAGCCACTTTCAAACAAGAAA'}
unaligned_DNA = LoadSeqs(data=seqs, moltype = DNA, aligned = False)
print unaligned_DNA.toFasta()
unaligned_aa = unaligned_DNA.getTranslation()
print unaligned_aa.toFasta()
aligned_aa_seqs = {'hum': 'KQIQESSENGSLAARQERQAQVNLT',
        'mus': 'KQIQESGESGSLAARQERQAQVNLT',
        'rat': 'LNKQ------PLS---------NKK'}
aligned_aa = LoadSeqs(data = aligned_aa_seqs, moltype = PROTEIN)
aligned_DNA = aligned_aa.replaceSeqs(unaligned_DNA)
print aligned_DNA
