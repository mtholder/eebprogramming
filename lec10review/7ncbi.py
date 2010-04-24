#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent.db.ncbi import EUtils
db = EUtils(db="protein", rettype="gp")
query = '"VWf"[gene] AND homo[orgn]'
records = db[query].readlines()
import re
from cogent.parse.genbank import RichGenbankParser
parser = RichGenbankParser(records)
acc2seq = {}
rows = []
for accession, seq in parser:
    if len(seq) < 2800:
        continue
    species = seq.Info.species.split()
    seq_name = "%s.%s" % (species[0][0] + species[1][:3], accession)
    acc2seq[seq_name] = seq
print acc2seq
from cogent import LoadSeqs
seqs = LoadSeqs(data=acc2seq, aligned=False)
sh = seqs.NamedSeqs['Hsap.P04275']
print sh.toFasta()
print sh.Info.taxonomy
