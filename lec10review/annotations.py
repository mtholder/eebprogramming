#!/usr/bin/env python
# taken from http://pycogent.sourceforge.net/
from cogent import DNA
from cogent.core.annotation import Feature
s = DNA.makeSequence("AAGAAGAAGACCCCCAAAAAAAAAATTTTTTTTTTAAAAAAAAAAAAA", Name="Orig")
exon1 = s.addAnnotation(Feature, 'exon', 'fred', [(10,15)])
exon2 = s.addAnnotation(Feature, 'exon', 'trev', [(30,40)])
s[exon1]
exon1.getSlice()
exons = s.getAnnotationsMatching('exon')
print exons
print s.getRegionCoveringAll(exons)
print s.getRegionCoveringAll(exons).getShadow()
s.getRegionCoveringAll(exons).getSlice()
s[exon1, exon2]
print s.getRegionCoveringAll(exons+exons)
s[exon1, exon1, exon1, exon1, exon1]
s[15:20, 5:16]
exon1[0:3].getSlice()
c = s[exon1[4:]]+s
print len(c)
for feat in  c.annotations:
    print feat
print c[exon1]
len(s.annotations)
region = s.getRegionCoveringAll(exons)
len(s.annotations)
region.attach()
len(s.annotations)
region.detach()
len(s.annotations)
plus = DNA.makeSequence("AAGGGGAAAACCCCCAAAAAAAAAATTTTTTTTTTAAA", Name="plus")
plus_cds = plus.addAnnotation(Feature, 'CDS', 'gene',
                       [(2,6),(10,15),(25,35)])
print plus_cds.getSlice()
minus = plus.rc()
minus_cds = minus.getAnnotationsMatching('CDS')[0]
print minus_cds.getSlice()
from cogent import LoadSeqs
aln = LoadSeqs(data=[['x','-AAAAAAAAA'], ['y','TTTT--TTTT']])
print aln
exon = aln.getSeq('x').addAnnotation(Feature, 'exon', 'fred', [(3,8)])
aln_exons = aln.getAnnotationsFromSequence('x', 'exon')
aln_exons = aln.getAnnotationsFromAnySequence('exon')
print exon
print aln_exons[0]
print aln_exons[0].getSlice()
aln_exons[0].attach()
len(aln.annotations)
exons = aln.getProjectedAnnotations('y', 'exon')
print exons
print aln.getSeq('y')[exons[0].map.withoutGaps()]
aln = LoadSeqs(data=[['x', '-AAAAAAAAA'], ['y', 'TTTT--TTTT']])
s = DNA.makeSequence("AAAAAAAAA", Name="x")
exon = s.addAnnotation(Feature, 'exon', 'fred', [(3,8)])
exon = aln.getSeq('x').copyAnnotations(s)
aln_exons = list(aln.getAnnotationsFromSequence('x', 'exon'))
print aln_exons
aln = LoadSeqs(data=[['x', '-AAAAAAAAA'], ['y', '------TTTT']])
exon = aln.getSeq('x').addFeature('exon', 'fred', [(3,8)])
aln_exons = list(aln.getAnnotationsFromSequence('x', 'exon'))
print aln_exons
print aln_exons[0].getSlice()
aln = LoadSeqs(data=[['x', '-AAAAAAAAA'], ['y', 'TTTT--T---']])
exon = aln.getSeq('x').addFeature('exon', 'fred', [(3,8)])
aln_exons = list(aln.getAnnotationsFromSequence('x', 'exon'))
print aln_exons[0].getSlice()
aln = LoadSeqs(data=[['x', 'C-CCCAAAAA'], ['y', '-T----TTTT']])
print aln
exon = aln.getSeq('x').addFeature('exon', 'ex1', [(0,4)])
print exon
print exon.getSlice()
aln_exons = list(aln.getAnnotationsFromSequence('x', 'exon'))
print aln_exons
print aln_exons[0].getSlice()
print aln_exons[0].asOneSpan().getSlice()
all_exons = aln.getRegionCoveringAll(aln_exons)
coords = all_exons.getCoordinates()
assert coords == [(0,1),(2,5)]
aln = LoadSeqs(data=[['x', 'C-CCCAAAAAGGGAA'], ['y', '-T----TTTTG-GTT']])
print aln
exon = aln.getSeq('x').addFeature('exon', 'norwegian', [(0,4)])
print exon.getSlice()
repeat = aln.getSeq('x').addFeature('repeat', 'blue', [(9,12)])
print repeat.getSlice()
repeat = aln.getSeq('y').addFeature('repeat', 'frog', [(5,7)])
print repeat.getSlice()
print aln.getSeq('x').withMaskedAnnotations('exon', mask_char='?')
print aln.getSeq('x').withMaskedAnnotations('exon', mask_char='?',
                                         shadow=True)
print aln.getSeq('x').withMaskedAnnotations(['exon', 'repeat'],
                                           mask_char='?')
print aln.getSeq('x').withMaskedAnnotations(['exon', 'repeat'],
                                           mask_char='?', shadow=True)
print aln.getSeq('y').withMaskedAnnotations('exon', mask_char='?')
print aln.getSeq('y').withMaskedAnnotations('repeat', mask_char='?')
print aln.getSeq('y').withMaskedAnnotations('repeat', mask_char='?',
                                          shadow=True)
print aln.withMaskedAnnotations('exon', mask_char='?')
print aln.withMaskedAnnotations('exon', mask_char='?', shadow=True)
print aln.withMaskedAnnotations('repeat', mask_char='?')
print aln.withMaskedAnnotations('repeat', mask_char='?', shadow=True)
print aln.withMaskedAnnotations(['repeat', 'exon'], mask_char='?')
print aln.withMaskedAnnotations(['repeat', 'exon'],shadow=True)
data = [['human', 'CGAAACGTTT'], ['mouse', 'CTAAACGTCG']]
as_series = LoadSeqs(data = data)
as_items = LoadSeqs(data = data)
as_series.getSeq('human').addFeature('cpgsite', 'cpg', [(0,2), (5,7)])
as_series.getSeq('mouse').addFeature('cpgsite', 'cpg', [(5,7), (8,10)])
as_items.getSeq('human').addFeature('cpgsite', 'cpg', [(0,2)])
as_items.getSeq('human').addFeature('cpgsite', 'cpg', [(5,7)])
as_items.getSeq('mouse').addFeature('cpgsite', 'cpg', [(5,7)])
as_items.getSeq('mouse').addFeature('cpgsite', 'cpg', [(8,10)])
serial = as_series.withMaskedAnnotations(['cpgsite'])
print serial
itemwise = as_items.withMaskedAnnotations(['cpgsite'])
print itemwise
print plus.withMaskedAnnotations("CDS")
print minus.withMaskedAnnotations("CDS")
