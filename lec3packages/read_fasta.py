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


gi_numbers = []
accession_numbers = []
descriptions = []
for element in identifiers:
    broken_up = element.split("|")
    gi_numbers.append(broken_up[1])
    accession_numbers.append(broken_up[3])
    descriptions.append(broken_up[4].strip())


for index, element in enumerate(gi_numbers):
    print "gi =", element
    print "accession =", accession_numbers[index]
    print "description =", descriptions[index]
    print sequences[index]


