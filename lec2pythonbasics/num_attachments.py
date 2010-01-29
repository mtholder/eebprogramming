#!/usr/bin/env python
import sys
program_name = sys.argv[0]
if len(sys.argv) > 3 or len(sys.argv) < 2:
    sys.exit(program_name + ": Expecting two arguments: <num_taxa> [filename]")

upper_limit = int(sys.argv[1])

if len(sys.argv) == 3:
    filename = sys.argv[2]
    output_stream = open(filename, 'w')
else:
    output_stream = sys.stdout

def calc_num_attachment_points(n):
    return 2*n - 3
for i in range(3, upper_limit):
    num_attachments = calc_num_attachment_points(i)
    output_stream.write(str(i) + " " + str(num_attachments) + "\n")

