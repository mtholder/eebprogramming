#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent import LoadSeqs, DNA
al = LoadSeqs('data/test2.fasta', moltype=DNA, aligned = False)
print al.toFasta()
pal = al.getTranslation()
print pal.toFasta()
