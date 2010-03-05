#!/usr/bin/env python
import sys
class Population(object):
    """An evolving population of organisms  -- really just a collection of alleles
    is enough for our purposes (hermaphroditic reproduction).
    """
    def __init__(self, allele_counts):
        self.n = sum(allele_counts)
        self.allele_counts = allele_counts


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(description="Simulator of drift in allele frequencies in a simple four-species tree.")
    parser.add_option('-i', '--internal-branch',
                      dest='internal',
                      type='int',
                      default=50,
                      help="Number of generations of evolution along the internal branches")
    parser.add_option('-t', '--terminal-branch',
                      dest='terminal',
                      type='int',
                      default=50,
                      help="Number of generations of evolution along the internal branches")
    parser.add_option('-c', '--counts',
                      dest='counts',
                      type='str',
                      default="50 50",
                      help="Initial counts of each allele (space separated)")
    options, args = parser.parse_args(sys.argv)
    try:
        allele_counts = [int(i) for i in options.counts.split()]
    except:
        sys.exit("Expecting the --counts (-c) option to be space-separated list of integers got %(val)s" % {'val':options.counts})
    if options.terminal < 0:
        sys.exit("The number of generations for the terminal branches must be non-negative")
    if options.internal < 0:
        sys.exit("The number of generations for the terminal branches must be non-negative")


