#!/usr/bin/env python
import sys

def get_input_stream():
    """Returns a file-like object for reading.

    If a command line argument is supplied, it is interpreted as a file to be
    read.  If no argument is used, then the function returns stdin."""
    if len(sys.argv) > 2:
        sys.exit(sys.argv[0] + ": Expecting one command line argument -- a filename")
    elif len(sys.argv) == 2:
        return open(sys.argv[1], 'rU')
    else:
        return sys.stdin

def read_sequence_from_stream(inp):
    """Parses a simple text file with a sequence and returns the sequence as
    a string.

    Simply concatenates the lines of the file - this does not validate the string
    as valid nucleotide sequence data."""
    rna_sequence_list = []
    for line in inp:
        rna_sequence_list.append(line.strip())
    return ''.join(rna_sequence_list)


def translate_seq(rna, code):
    """Returns the sequence of amino acids for the rna sequence using the code
    dict supplied.  This function translates the `rna` in frame (assuming that
    the caller has found the start codon.
    """
    aa_list = []
    base_list = list(rna)
    while True:
        if len(base_list) > 2:
            codon = ''.join(base_list[0:3])
            del base_list[0:3]
        else:
            break
        aa = genetic_code[codon]
        if aa == '*':
            break
        aa_list.append(aa)
    return ''.join(aa_list)

def get_all_translations(rna_sequence, genetic_code):
    """Returns a list of all possible translations of `rna_sequence` given
    a dict `genetic_code` that maps codons to amino acids.

    The value '*' in the dict is used to specify a stop codon.
    """
    num_bases = len(rna_sequence)
    last_first_base_index = num_bases - 3

    polypeptide_list = []
    for i in xrange(last_first_base_index + 1):
        i_end = i + 3
        next_three = rna_sequence[i:i_end]
        if next_three == 'AUG':
            polypeptide = translate_seq(rna_sequence[i:], genetic_code)
            polypeptide_list.append(polypeptide)
    return polypeptide_list

def reverse_and_complement(s):
    """Takes an RNA sequence and returns the reversed and complemented form.

    Presumably `s` is formed by transcribing a DNA sequence.  If the same DNA
    sequence was transcribed in the opposite direction, you would get the RNA
    sequence that this function returns.
    """
    rna_list = list(s)
    rna_list.reverse()
    rev_c = []
    complement = {'A' : 'U', 'C' : 'G', 'G': 'C', 'U': 'A'}
    for i in rna_list:
        rev_c.append(complement[i])
    return ''.join(rev_c)

def display_list(x, offset=1):
    """Prints a line for each element in `x`  Each line consists of:
    str(index + `offset`) x[index]
    thus the user sees the elements of the list labelled by their position.
    """
    for n, pp in enumerate(x):
        print offset + n, pp

genetic_code = {'GUC': 'V', 'ACC': 'T', 'GUA': 'V', 'GUG': 'V', 'ACU': 'T', 'AAC': 'N', 'CCU': 'P', 'UGG': 'W', 'AGC': 'S', 'AUC': 'I', 'CAU': 'H', 'AAU': 'N', 'AGU': 'S', 'GUU': 'V', 'CAC': 'H', 'ACG': 'T', 'CCG': 'P', 'CCA': 'P', 'ACA': 'T', 'CCC': 'P', 'UGU': 'C', 'GGU': 'G', 'UCU': 'S', 'GCG': 'A', 'UGC': 'C', 'CAG': 'Q', 'GAU': 'D', 'UAU': 'Y', 'CGG': 'R', 'UCG': 'S', 'AGG': 'R', 'GGG': 'G', 'UCC': 'S', 'UCA': 'S', 'UAA': '*', 'GGA': 'G', 'UAC': 'Y', 'GAC': 'D', 'UAG': '*', 'AUA': 'I', 'GCA': 'A', 'CUU': 'L', 'GGC': 'G', 'AUG': 'M', 'CUG': 'L', 'GAG': 'E', 'CUC': 'L', 'AGA': 'R', 'CUA': 'L', 'GCC': 'A', 'AAA': 'K', 'AAG': 'K', 'CAA': 'Q', 'UUU': 'F', 'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'GCU': 'A', 'GAA': 'E', 'AUU': 'I', 'UUG': 'L', 'UUA': 'L', 'UGA': '*', 'UUC': 'F'}




inp = get_input_stream()

rna_sequence = read_sequence_from_stream(inp)

num_bases = len(rna_sequence)
if num_bases < 3:
    sys.exit()

# We'll number the possible translations.  First we'll get the translation of
# one strand...
polypeptide_list = get_all_translations(rna_sequence, genetic_code)

# and print them out...
display_list(polypeptide_list)

# We don't want to start numbering the reverse strand translations at 1, so
#   we'll store the "offset" the number of polypeptides that we have already
#   printed out.
offset = len(polypeptide_list)

# Now we reverse and complement...
rev_c_seq = reverse_and_complement(rna_sequence)

# translate the other strand...
polypeptide_list = get_all_translations(rev_c_seq, genetic_code)

# Let the user know that we have switched to
sys.stderr.write("After " + str(offset) + " polypeptides, we will translate the other strand\n")

display_list(polypeptide_list, offset=offset)
