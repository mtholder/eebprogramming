#!/usr/bin/env python

def fasta_reader(inp):
    "FASTA-reading generator"
    name = None
    seq = []
    for line in inp:
        if line.startswith('>'):
            if name is not None:
                yield name, ''.join(seq)
            name = line[1:-1]
            seq = []
        else:
            seq.append(line.strip())
    yield name, ''.join(seq)
    
import sys
file_obj = open(sys.argv[1], 'rU')
for n, s in fasta_reader(file_obj):
    print n, s[:10], "...", s[-10:]
        
