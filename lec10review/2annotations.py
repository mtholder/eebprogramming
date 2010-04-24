#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent import DNA
s = DNA.makeSequence("aagaagaagacccccaaaaaaaaaattttttttttaaaaaaaaaaaaa", Name="Orig")
exon1 = s.addFeature('exon', 'exon1', [(10,15)])
exon2 = s.addFeature('exon', 'exon2', [(30,40)])
from cogent.core.annotation import Feature
s2=DNA.makeSequence("aagaagaagacccccaaaaaaaaaattttttttttaaaaaaaaaaaaa", Name="Orig2")
exon3 = s2.addAnnotation(Feature, 'exon', 'exon1', [(35,40)])
s[exon1]
exons = s.getAnnotationsMatching('exon')
print exons
print s.getRegionCoveringAll(exons)
s.getRegionCoveringAll(exons).getSlice()
print s.getRegionCoveringAll(exons).getShadow().getSlice()
print exon1[0:3].getSlice()
