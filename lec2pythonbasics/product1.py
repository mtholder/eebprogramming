#!/usr/bin/env python
import sys
program_name = sys.argv[0]
if len(sys.argv) > 3 or len(sys.argv) < 2:
    sys.exit(program_name + ": Expecting two arguments: <column index> [filename]")

col_index = int(sys.argv[1])

if len(sys.argv) == 3:
    filename = sys.argv[2]
    input_stream = open(filename, 'rU')
else:
    input_stream = sys.stdin

product = 1L
num_taxa = []
num_attachments = []
for line in input_stream:
    word_list = line.split()
    word_of_interest = word_list[col_index]
    number_of_interest = int(word_of_interest)
    first_word = word_list[0]
    num_attachments.append(number_of_interest)
    num_taxa.append(int(first_word))
    product = product * number_of_interest
print product


ntaxa_indices = range(len(num_taxa))
print "ntaxa_indices =", ntaxa_indices
for i in ntaxa_indices:
    print "product of columns for row", i, "is", num_taxa[i]*num_attachments[i]
