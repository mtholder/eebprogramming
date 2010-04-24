#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent import LoadSeqs, DNA
aln = LoadSeqs("data/long_testseqs.fasta", moltype=DNA)[:50]
print aln
naln = aln.rc()
print naln
