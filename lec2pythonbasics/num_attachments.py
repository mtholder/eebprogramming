#!/usr/bin/env python
output_stream = open('a', 'w')
def calc_num_attachment_points(n):
    return 2*n - 3
for i in range(3, 101):
    num_attachments = calc_num_attachment_points(i)
    output_stream.write(str(i) + " " + str(num_attachments) + "\n")

