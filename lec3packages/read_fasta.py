#!/usr/bin/env python
"An example of simple re parsing"


import sys
import re

class GenBankSequence(object):
    "Encapsulates the information that is contained in a genbank record."

    def __init__(self, gi, accession, species, locus, sequence):
        self.gi = gi
        self.accession = accession
        self.species = species
        self.locus = locus
        self.sequence = sequence
        self.reversed = False
        self.complemented = False
    def __str__(self):
        details = "(GI = " + self.gi + ", " + "Accession = " + self.accession
        if self.reversed:
            details = details + " Reversed"
        if self.complemented:
            details = details + " Complemented"
        details = details + ")"
        summary_lines = ["Sequence from GenBank",
                         "Species: " + self.species,
                         "Locus: " + self.locus,
                         details,
                         self.sequence]
        return '\n'.join(summary_lines)

    def reverse_and_complement(self):
        """Reverse and compelment the sequences (make it refer to the opposite
        strand).
        """
        self.reversed = not self.reversed
        self.complemented = not self.complemented
        a = list(self.sequence)
        a.reverse()
        rc_dict = {'A' : 'T', 'G' : 'C', 'C' : 'G', 'T' : 'A'}
        b = []
        for i in a:
            b.append(rc_dict[i])
        self.sequence = ''.join(b)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(sys.argv[0] + ": Expecting one command line argument -- a filename")
    inp = open(sys.argv[1], 'rU')

    identifiers = []
    sequences = []
    current_seq = []

    for line in inp:
        stripped = line.strip()
        if line.startswith('>'):
            if current_seq:
                sequences.append(''.join(current_seq))
            identifiers.append(stripped[1:])
            current_seq = []
        else:
            if stripped:
                current_seq.append(stripped)
    if current_seq:
        sequences.append(''.join(current_seq))

    assert(len(identifiers) == len(sequences))

    first_part = r'gi\|(\d+)\|gb\|([a-zA-Z0-9.]+)'
    second_part = r'\|\s*(\S+\s+\S+)\s+(\S.*\S)'
    third_part = r',\s*(\S.*\S)\s*'
    pattern = first_part + second_part + third_part
    identifier_pattern = re.compile(pattern)

    gi_numbers = []
    accession_numbers = []
    locus_list = []
    species_list = []
    for element in identifiers:
        match_object = identifier_pattern.match(element)
        if match_object:
            gi, acc, sp, locus, blah =  match_object.groups()
            print [gi, acc, sp, locus, blah]
            gi_numbers.append(gi)
            accession_numbers.append(acc)
            species_list.append(sp)
            locus_list.append(locus)
        else:
            print element, "does not match our search pattern"


    seq_objects = []
    for index, element in enumerate(gi_numbers):
        o = GenBankSequence(gi=element,
                            accession=accession_numbers[index],
                            species=species_list[index],
                            locus=locus_list[index],
                            sequence=sequences[index])
        seq_objects.append(o)
        print
        print str(o)
        o.reverse_and_complement()
        print
        print o
        o.reverse_and_complement()
        print
        print o


