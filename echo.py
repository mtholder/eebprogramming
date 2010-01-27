#!/usr/bin/env python
import sys
print "Number of command line arguments = %d" % (len(sys.argv) - 1)
for o, a in enumerate(sys.argv[1:]):
    print 'Arg %d = "%s"' % (1 + o, a)
print "End of arguments"
    
