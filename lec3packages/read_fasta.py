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
        sequences.append(current_seq)
        identifiers.append(stripped[1:])
        current_seq = []
    else:
        if stripped:
            current_seq.append(stripped)
print '\n'.join(identifiers)
print '\n'.join(sequences)

