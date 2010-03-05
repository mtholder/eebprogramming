#!/usr/bin/env python
import sys
import random
import cStringIO

VERBOSE_MODE = False
RNG = random.Random()
def debug(m):
    "We should probably use the logging module for this"
    if VERBOSE_MODE:
        sys.stderr.write("%(script)s: %(msg)s\n" % {'script' : sys.argv[0], 'msg' : m})

def select_random_index(probabilities):
    "Returns an index in proportion to its probability"
    u = RNG.random()
    for n, p in enumerate(probabilities):
        u = u - p
        if u < 0.0:
            return n
    return n

class Population(object):
    """An evolving population of organisms  -- really just a collection of alleles
    is enough for our purposes (hermaphroditic reproduction).
    """
    def __init__(self, allele_counts):
        self.n = sum(allele_counts)
        self.allele_counts = allele_counts

    def next_generation(self):
        allele_freq = self.get_allele_frequncies()
        next_gen_counts = [0]*len(allele_freq)
        for i in xrange(self.n):
            index = select_random_index(allele_freq)
            next_gen_counts[index] = next_gen_counts[index] + 1
        self.allele_counts = next_gen_counts

    def get_allele_frequncies(self):
        allele_freq = []
        for c in self.allele_counts:
            freq = float(c)/self.n
            allele_freq.append(freq)
        return allele_freq

    def write_frequencies(self, outp):
        allele_freq = self.get_allele_frequncies()
        as_str = []
        for c in allele_freq:
            s = "%(freq)3.4f" % {'freq' : c}
            as_str.append(s)
        msg = " ".join(as_str)
        outp.write(msg)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(description="Simulator of drift in allele frequencies in a simple four-species tree.")
    parser.add_option('-v', '--verbose',
                      dest='verbose',
                      action="store_true",
                      default=False,
                      help="Verbose execution mode")
    parser.add_option('-s', '--seed',
                      dest='seed',
                      type='int',
                      default=0,
                      help="Random number generator seed")
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
        allele_counts = []
        for i in options.counts.split():
            allele_counts.append(int(i))
    except:
        sys.exit("Expecting the --counts (-c) option to be space-separated list of integers got %(val)s" % {'val':options.counts})
    if options.terminal < 0:
        sys.exit("The number of generations for the terminal branches must be non-negative")
    if options.internal < 0:
        sys.exit("The number of generations for the terminal branches must be non-negative")
    if options.verbose:
        VERBOSE_MODE = True

    # seed the random number generator, and print out the seed to stderr
    if options.seed < 2:
        import time
        seed = int(time.time()*1000)
    else:
        seed = options.seed
    sys.stderr.write("seed = %(seed)d\n" % {'seed' : seed})
    RNG.seed(seed)

    # create the population that will be the parents of species a and b
    abParPop = Population(allele_counts)
    # create the population that will be the parents of species a and b
    cdParPop = Population(allele_counts)
    for i in xrange(options.internal):
        f_str = cStringIO.StringIO()
        abParPop.write_frequencies(f_str)
        f_str.write(' ')
        cdParPop.write_frequencies(f_str)
        to_print = {'gen' : i, 'freq_strings' : f_str.getvalue()}
        debug("internal generation %(gen)d: %(freq_strings)s" % to_print)
        abParPop.next_generation()
        cdParPop.next_generation()
    aPopulation = Population(abParPop.allele_counts)
    bPopulation = Population(abParPop.allele_counts)
    cPopulation = Population(cdParPop.allele_counts)
    dPopulation = Population(cdParPop.allele_counts)
    for i in xrange(options.terminal):
        f_str = cStringIO.StringIO()
        aPopulation.write_frequencies(f_str)
        f_str.write(' ')
        bPopulation.write_frequencies(f_str)
        f_str.write(' ')
        cPopulation.write_frequencies(f_str)
        f_str.write(' ')
        dPopulation.write_frequencies(f_str)
        to_print = {'gen' : i, 'freq_strings' : f_str.getvalue()}
        debug("terminal generation %(gen)d: %(freq_strings)s" % to_print)
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

