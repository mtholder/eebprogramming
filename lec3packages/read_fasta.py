#!/usr/bin/env python
"An example of simple re parsing"


import sys
if len(sys.argv) != 2:
    sys.exit(sys.argv[0] + ": Expecting one command line argument -- a filename")
inp = open(sys.argv[1], 'rU')

identifiers = []
sequences = []

for line in inp:
    stripped = line.strip()
    if line.startswith('>'):
        identifiers.append(stripped[1:])
    else:
        if stripped:
            sequences.append(stripped)
print '\n'.join(identifiers)
print '\n'.join(sequences)

