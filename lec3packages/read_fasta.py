#!/usr/bin/env python
"An example of simple re parsing"


import sys
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

import re
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


#for index, element in enumerate(gi_numbers):
#    print "gi =", element
#    print "accession =", accession_numbers[index]
#    print "description =", descriptions[index]
#    print sequences[index]


