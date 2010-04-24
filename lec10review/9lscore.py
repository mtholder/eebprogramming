#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent.evolve.models import HKY85
from cogent import LoadSeqs, LoadTree
model = HKY85()
aln = LoadSeqs("data/primate_cdx2_promoter.fasta")
tree = LoadTree(tip_names=aln.Names)
lf = model.makeLikelihoodFunction(tree)
lf.setAlignment(aln)
lf.optimise(show_progress = False)
print lf
