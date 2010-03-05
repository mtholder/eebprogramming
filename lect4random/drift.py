#!/usr/bin/env python

class Population(object):
    """An evolving population of organisms  -- really just a collection of alleles
    is enough for our purposes (hermaphroditic reproduction).
    """
    def __init__(self, allele_counts):
        self.n = sum(allele_counts)
        self.allele_counts = allele_counts

