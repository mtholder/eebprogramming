#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent import LoadSeqs, LoadTree
from cogent.evolve.models import HKY85
from cogent.maths import stats
aln = LoadSeqs(filename = "data/long_testseqs.fasta")
t = LoadTree(filename = "data/test.tree")
sm = HKY85()
lf = sm.makeLikelihoodFunction(t, digits=2, space=3)
lf.setLocalClock("Human", "HowlerMon")
lf.setAlignment(aln)
lf.optimise(show_progress=False)
lf.setName("clock")
print "lf =\n", lf
print "lf.getStatistics() =\n", lf.getStatistics()
opt_tr = lf.getAnnotatedTree()

print "opt_tr.getNewick() =\n", opt_tr.getNewick(with_distances=True)


null_lnL = lf.getLogLikelihood()
null_nfp = lf.getNumFreeParams()
lf.setParamRule('length', is_independent=True)
lf.optimise(show_progress=False)
lf.setName("non clock")
print lf
opt_tr = lf.getAnnotatedTree()
print "opt_tr.getNewick() =\n", opt_tr.getNewick(with_distances=True)

LR = 2 * (lf.getLogLikelihood() - null_lnL)
df = lf.getNumFreeParams() - null_nfp
P = stats.chisqprob(LR, df)
print "Likelihood ratio statistic = ", LR
print "degrees-of-freedom = ", df
print "probability = ", P

