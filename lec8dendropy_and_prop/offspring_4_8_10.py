#!/usr/bin/env python
import math
import logging
from dendropy.utility.messaging import get_logger
_LOG = get_logger('offspring')

class SingleLocusGenotype(object):
    "object that has an allele 1 & an allele 2"
    def __init__(self, first, second):
        self.first = min(first, second)
        self.second = max(first, second)

    def __str__(self):
        return repr(self.first) + '/' + repr(self.second)

    def calcLnL(self, outcrossing_prob, allele_freq, mom_g):
        prob_offspring_given_selfing = self.calc_prob_offspring_given_selfing(mom_g)
        _LOG.debug(str(self) +  " from " + str(mom_g) +  " P(self) = " + str(prob_offspring_given_selfing))
        prob_offspring_given_outcrossing = self.calc_prob_offspring_given_outcrossing(allele_freq, mom_g)
        _LOG.debug(str(self) +  " from " + str(mom_g) +  " P(outcross) = " + str(prob_offspring_given_outcrossing))
        return math.log(((1.0 - outcrossing_prob) * prob_offspring_given_selfing) + (outcrossing_prob * prob_offspring_given_outcrossing))

    def calc_prob_offspring_given_selfing(self, mom_g):
        if mom_g.first == mom_g.second:
            # mom is homozygous
            if self.first == self.second and (self.first == mom_g.first):
                return 1.0
            return 0.0
        else:
            if (self.first == self.second):
                # mom is het
                # self is homozygous
                assert (self.first == mom_g.first) or (self.first == mom_g.second)
                return 0.25
            else:
                # mom is het
                # self is het
                if (self.first == mom_g.first) and (self.second == mom_g.second):
                    return 0.5
                else:
                    return 0.0
    def calc_prob_offspring_given_outcrossing(self, allele_freq, mom_g):
        _LOG.debug("Allele freq = " + str(allele_freq))
        _LOG.debug("Mom's genotype = " +  str(mom_g))
        _LOG.debug("Offspring's genotype = " + str(self))
        assert (self.first == mom_g.first) or (self.first == mom_g.second) or (self.second == mom_g.first) or (self.second == mom_g.second)
        if mom_g.first == mom_g.second:
            # mom is homozygous
            if (self.first == mom_g.first):
                return allele_freq[self.second]
            else:
                return allele_freq[self.first]
        else:
            if (self.first != mom_g.first) and (self.first != mom_g.second):
                return allele_freq[self.first]*0.5
            else:
            # second offspring allele mismatches
                if (self.second != mom_g.first) and (self.second != mom_g.second):
                    return allele_freq[self.second]*0.5
                else:
                    return 0.5 * (allele_freq[self.first] + allele_freq[self.second])


class Individual(object):
    "object that holds multilocus genotypes for each individual"
    def __init__(self, family, genotype_list, is_mom = False):
        self.family = family
        self.genotype_list = genotype_list
        if family is not None:
            if is_mom:
                family.add_mom(self)
            else:
                family.add_offspring(self)
    def __str__(self):
        x = "Individual with genotype = ["
        for locus in self.genotype_list:
            x = x + str(locus) + ', '
        return x + ']'
    def calcLnL(self, outcrossing_prob, population, mom):
        lnl = 0.0
        for n, genotype in enumerate(self.genotype_list):
            allele_freq = population.allele_freq_list[n]
            mom_g = mom.genotype_list[n]
            lnl = lnl + genotype.calcLnL(outcrossing_prob, allele_freq, mom_g)
        return lnl

class Family(object):
    "object that holds related maternal & offspring genotypes (or just offspring)"
    def __init__(self, name):
        self.name = name
        self.mom = None
        self.pop_name = None
        self.offspring = []
    def add_mom(self, mom):
        assert self.mom is None
        self.mom = mom
    def add_offspring(self, offspring):
        self.offspring.append(offspring)
    def __str__(self):
        r = ["Family " + self.name]
        r = ["  mom = " + str(self.mom)]
        for o in self.offspring:
            r.append(str(o))
        return "\n  ".join(r)
    def calcLnL(self, outcrossing_prob):
        lnl = 0.0
        for offspring in self.offspring:
            lnl = lnl + offspring.calcLnL(outcrossing_prob, self.population, self.mom)
        return lnl

class Population(object):
    def __init__(self, allele_freq_list):
        self.allele_freq_list = allele_freq_list

class CSVFileParseException(Exception):
    def __init__(self, stream, line, msg):
        self.filename = stream.name
        self.line = line
        self.msg = msg
    def __str__(self):
        return "Error parsing %s at line %d:\n  %s\n" % (self.filename, self.line, self.msg)

def parse_csv(stream, sep):
    "Reads a CSV file and returns a list of marker names and families"
    import csv
    reader = csv.reader(stream, delimiter=sep)
    line_iterator = iter(reader)
    # first line should be #num markers,groupname,groupingvar

    first_line = line_iterator.next()
    if len(first_line) < 3:
        raise CSVFileParseException(stream, 1, "Expecting at least three columns in the first line")

    word = first_line[0]
    try:
        num_markers = int(word)
    except:
        raise CSVFileParseException(stream, 1, 'Expecting a number of markers in the first cell of the first line (Found "%s")' % word)

    word = first_line[1]
    if word == '1':
        group_name = True
    elif word == '0':
        group_name = False
    else:
        raise CSVFileParseException(stream, 1, 'Expecting a 0 or 1 (to indicate additional grouping names) in the second column  of the first line (Found "%s")' % word)

    word = first_line[2]
    if word == '1':
        group_name = True
        raise CSVFileParseException(stream, 1, 'Group names not supported')
    elif word == '0':
        group_name = False
    else:
        raise CSVFileParseException(stream, 2, 'Expecting a 0 or 1 (to indicate additional grouping variable) in the third column  of the first line (Found "%s")' % word)

    second_line = line_iterator.next()
    if len(first_line) < num_markers:
        raise CSVFileParseException(stream, 2, "Expecting at least %s columns of marker names in the second line")
    marker_names = []
    for n, word in enumerate(second_line):
        if n >= num_markers:
            break
        if not word.strip():
            raise CSVFileParseException(stream, 2, "Found an empty cell in column %d of line 2 (expected a marker name)" % (1 + n))
        marker_names.append([word.strip(), 0])

    expected_line_len = 2 + 2*num_markers
    name_to_fam = {}
    for n, row in enumerate(line_iterator):
        if not row:
            continue # allow blank lines by skipping them
        if len(row) < expected_line_len:
            raise CSVFileParseException(stream, 3 + n, "Expecting at least %d columns, but found only" % (expected_line_len, len(row)))


        population = row[1]
        # find the appropriate family
        family_name = row[0]
        if family_name.endswith('!'):
            mom = True
            family_name = family_name[0:-1]
        else:
            mom = False

        key = (population, family_name)
        if key in name_to_fam:
            family = name_to_fam[key]
        else:
            family = Family(family_name)
            family.pop_name = population
            name_to_fam[key] = family

        assert population == family.pop_name

        offset = 2
        genotype_list = []
        for i in range(num_markers):
            try:
                first = int(row[offset])
            except:
                raise CSVFileParseException(stream, 3 + n, "Expecting a number for an allele in column %d, but found %s" % (offset+1, row[offset]))
            try:
                second = int(row[offset + 1])
            except:
                raise CSVFileParseException(stream, 3 + n, "Expecting a number for an allele in column %d, but found %s" % (offset+2, row[offset + 1]))
            genotype_list.append(SingleLocusGenotype(first, second))
            max_allele = max(first, second)
            info_for_this_locus = marker_names[i]
            info_for_this_locus[1] = max(max_allele, info_for_this_locus[1])
            offset = offset + 2
        ind = Individual(family, genotype_list, mom)
    return marker_names, name_to_fam.values()

def calcLnLForAllFamilies(outcrossing_prob, family_list):
    lnL = 0.0
    for fam in family_list:
        lnL = lnL + fam.calcLnL(outcrossing_prob)
        _LOG.debug(lnL)
    return lnL

#read the filename and return a list of families
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-v', '--verbose',
                  dest='verbose',
                  action="store_true",
                  default=False,
                  help="Verbose execution mode")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        sys.exit("Expecting a filename as an argument")
    import os
    if options.verbose:
        _LOG.setLevel(logging.DEBUG)
    fn = args[0]
    if not os.path.exists(fn):
        sys.exit("The file %s does not exist!\n" % fn)
    if not os.path.isfile(fn):
        sys.exit("The path %s is not a file!\n" % fn)
    inp = open(fn, 'rU')
    try:
        marker_names, families = parse_csv(inp, ',')
    except CSVFileParseException as x:
        sys.exit(str(x))

    # should be pop specific!!!!!
    all_loci_freqs = []
    for marker in marker_names:
        num_alleles = marker[1]
        freq = 1.0 / num_alleles
        _LOG.debug(freq)
        af = [0.0]
        for i in range(num_alleles):
            af.append(freq)
        _LOG.debug(af)
        all_loci_freqs.append(af)
    pop = Population(all_loci_freqs)

    outcrossing_prob = 0.1
    for fam in families:
        fam.population = pop # should be checking pop_name specific!!!!!
        _LOG.debug(fam)
        _LOG.debug(fam.mom)
        _LOG.debug(fam.population.allele_freq_list)


    highest_lnL = float('-inf')
    ml_outcrossing = 0.0
    num_outrossing_inc = 1001
    for outcrossing_prob_step in range(num_outrossing_inc):
        outcrossing_prob = float(outcrossing_prob_step)/(num_outrossing_inc - 1)
        lnL = calcLnLForAllFamilies(outcrossing_prob, families)
        print outcrossing_prob, lnL
        if lnL > highest_lnL:
            highest_lnL = lnL
            ml_outcrossing = outcrossing_prob

