#!/usr/bin/env python
"An example of simple re parsing"


import sys
if len(sys.argv) != 2:
    sys.exit(sys.argv[0] + ": Expecting one command line argument -- a filename")
inp = open(sys.argv[1], 'rU')

identifiers = []
sequences = []

for line in inp:
    if line.startswith('>'):
        identifiers.append(line.strip()[1:])
    else:
        sequences.append(line.strip())
print '\n'.join(identifiers)
print '\n'.join(sequences)

