#!/usr/bin/env python
import sys
program_name = sys.argv[0]
if len(sys.argv) > 3 or len(sys.argv) < 2:
    sys.exit(program_name + ": Expecting two arguments: <filename> <column index>")

col_index = int(sys.argv[1])

if len(sys.argv) == 3:
    filename = sys.argv[2]
    input_stream = open(filename, 'rU')
else:
    input_stream = sys.stdin

product = 1L
for line in input_stream:
    word_list = line.split()
    word_of_interest = word_list[col_index]
    number_of_interest = long(word_of_interest)
    product = product * number_of_interest
print product
