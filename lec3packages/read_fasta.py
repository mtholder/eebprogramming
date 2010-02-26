#!/usr/bin/env python
"An example of simple re parsing"


import sys
import re

class DNASequence(object):
    def __init__(self, sequence, species="<unknown>", locus="<unknown>"):
        self.species = species
        self.locus = locus
        self.sequence = sequence
        self.reversed = False
        self.complemented = False

    def get_header_str(self):
        return "Species: " + self.species + "\nLocus: " + self.locus

    def __str__(self):
        summary_lines = [self.get_header_str()
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

class GenBankSequence(DNASequence):
    "Encapsulates the information that is contained in a genbank record."

    def __init__(self, gi, accession, species, locus, sequence):
        DNASequence.__init__(self, sequence, species, locus)
        self.gi = gi
        self.accession = accession

    def get_header_str(self):
        details = "(GI = " + self.gi + ", " + "Accession = " + self.accession
        if self.reversed:
            details = details + " Reversed"
        if self.complemented:
            details = details + " Complemented"
        details + ")"
        summary_lines = ["Sequence from GenBank",
                         "Species: " + self.species,
                         "Locus: " + self.locus,
                         details]
        return '\n'.join(summary_lines)



def create_GBSeq_from_GenBankFasta(header, sequence):
    """Takes the GenBank Fasta header line, and the sequence and creates a new
    GenBankSequence object from that information.
    """
    first_part = r'gi\|(\d+)\|gb\|([a-zA-Z0-9.]+)'
    second_part = r'\|\s*(\S+\s+\S+)\s+(\S.*\S)'
    third_part = r',\s*(\S.*\S)\s*'
    pattern = first_part + second_part + third_part
    identifier_pattern = re.compile(pattern)

    match_object = identifier_pattern.match(header)
    if match_object:
        gi, acc, sp, locus, blah =  match_object.groups()
        return GenBankSequence(gi=gi,
                               accession=acc,
                               species=sp,
                               locus=locus,
                               sequence=sequence)
    else:
        print header, "does not match our search pattern"

def parse_gen_bank_fasta(input_stream):
    """Takes a file-like object that contains GenBank records in FASTA.  Returns a
    lists of GenBankSequence objects.
    """
    gbseq_objects = []
    current_seq = []
    identifier = None
    for line in inp:
        stripped = line.strip()
        if line.startswith('>'):
            if current_seq:
                full_seq = ''.join(current_seq)
                gbseq_o = create_GBSeq_from_GenBankFasta(identifier, full_seq)
                gbseq_objects.append(gbseq_o)
            identifier = stripped[1:]
            current_seq = []
        else:
            if stripped:
                current_seq.append(stripped)
    if current_seq:
        gbseq_o = create_GBSeq_from_GenBankFasta(identifier, full_seq)
        gbseq_objects.append(gbseq_o)

    return gbseq_objects

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(sys.argv[0] + ": Expecting one command line argument -- a filename")
    inp = open(sys.argv[1], 'rU')
    seq_objects = parse_gen_bank_fasta(inp)
    for o in seq_objects:
        print
        print str(o)
        o.reverse_and_complement()
        print
        print o
        o.reverse_and_complement()
        print
        print o


