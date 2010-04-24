#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent.core.profile import Profile
from cogent import LoadSeqs, RNA
aln = LoadSeqs("data/trna_profile.fasta", moltype=RNA)
print len(aln.Seqs)
print len(aln)
pf = aln.getPosFreqs()
print pf.prettyPrint(include_header=True, column_limit=6, col_sep='   ')
pf.normalizePositions()
print pf.prettyPrint(include_header=True, column_limit=6, col_sep='   ')
print pf.isValid()
print '\n'.join(['%s: %.3f'%(c,f) for (c,f) in zip(pf.CharOrder, pf.dataAt(4)) if f!=0])
print pf.toConsensus(fully_degenerate=False)
pf.Alphabet=RNA
print "to consensus"
print pf.toConsensus(fully_degenerate=True)
print pf.toConsensus(cutoff=0.8)
print pf.toConsensus(cutoff=0.6)
loop_profile = Profile(pf.Data[54:60,:], Alphabet=RNA, CharOrder=pf.CharOrder)
print loop_profile.prettyPrint(include_header=True, column_limit=6, col_sep='   ')
yeast = RNA.Sequence('GCGGAUUUAGCUCAGUU-GGGAGAGCGCCAGACUGAAGAUCUGGAGGUCCUGUGUUCGAUCCACAGAAUUCGCACCA')
scores = loop_profile.score(yeast)
print scores
print max(scores)
print scores.argmax()
