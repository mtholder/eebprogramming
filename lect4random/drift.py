#!/usr/bin/env python
import sys

VERBOSE_MODE = False
def debug(m):
    "We should probably use the logging module for this"
    if VERBOSE_MODE:
        sys.stderr.write("%(script)s: %(msg)s\n" % {'script' : sys.argv[0], 'msg' : m})

class Population(object):
    """An evolving population of organisms  -- really just a collection of alleles
    is enough for our purposes (hermaphroditic reproduction).
    """
    def __init__(self, allele_counts):
        self.n = sum(allele_counts)
        self.allele_counts = allele_counts
    def next_generation(self):
        pass
    def write_frequencies(self, outp):
        pass

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(description="Simulator of drift in allele frequencies in a simple four-species tree.")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action="store_true",
                      default=False,
                      help="Verbose execution mode")
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
    if options.verbose:
        VERBOSE_MODE = True
    # create the population that will be the parents of species a and b
    abParPop = Population(allele_counts)
    # create the population that will be the parents of species a and b
    cdParPop = Population(allele_counts)
    for i in xrange(options.internal):
        debug("internal generation %(gen)d" % {'gen' : i })
        abParPop.next_generation()
        cdParPop.next_generation()
    aPopulation = Population(abParPop.allele_counts)
    bPopulation = Population(abParPop.allele_counts)
    cPopulation = Population(cdParPop.allele_counts)
    dPopulation = Population(cdParPop.allele_counts)
    for i in xrange(options.terminal):
        debug("terminal generation %(gen)d" % {'gen' : i })
        aPopulation.next_generation()
        bPopulation.next_generation()
        cPopulation.next_generation()
        dPopulation.next_generation()

    output_stream = sys.stdout
    output_stream.write("A ")
    aPopulation.write_frequencies(output_stream)
    output_stream.write("\nB ")
    bPopulation.write_frequencies(output_stream)
    output_stream.write("\nC ")
    cPopulation.write_frequencies(output_stream)
    output_stream.write("\nD ")
    dPopulation.write_frequencies(output_stream)
    output_stream.write("\n")

