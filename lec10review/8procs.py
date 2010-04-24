#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent.app.mafft import align_unaligned_seqs as mafft_align_unaligned_seqs
from cogent.core.moltype import DNA
from cogent import LoadSeqs
from cogent.app.raxml import build_tree_from_alignment as raxml_build_tree
unaligned_seqs = LoadSeqs(filename='data/test2.fasta', aligned=False)
aln = mafft_align_unaligned_seqs(unaligned_seqs, DNA)
#raxml_tree = raxml_build_tree(aln, DNA)
#print raxml_tree
