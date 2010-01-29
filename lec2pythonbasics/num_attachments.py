#!/usr/bin/env python
import sys

output_stream = open('a', 'w')

upper_limit = int(sys.argv[1])

def calc_num_attachment_points(n):
    return 2*n - 3
for i in range(3, upper_limit):
    num_attachments = calc_num_attachment_points(i)
    output_stream.write(str(i) + " " + str(num_attachments) + "\n")

