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
pattern = r'gi\|(\d+)\|gb\|([a-zA-Z0-9.]+)'
identifier_pattern = re.compile(pattern)

gi_numbers = []
accession_numbers = []
descriptions = []
for element in identifiers:
    match_object = identifier_pattern.match(element)
    if match_object:
        print match_object.group(1)
        print match_object.group(2)
    else:
        print element, "does not match our search pattern"


#for index, element in enumerate(gi_numbers):
#    print "gi =", element
#    print "accession =", accession_numbers[index]
#    print "description =", descriptions[index]
#    print sequences[index]


