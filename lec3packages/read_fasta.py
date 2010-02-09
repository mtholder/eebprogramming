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

print '\n'.join(identifiers)
print '\n'.join(sequences)

for index, element in enumerate(identifiers):
    print element
    print sequences[index]


