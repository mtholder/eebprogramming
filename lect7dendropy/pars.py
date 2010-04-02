#!/usr/bin/env python
import sys, logging
from dendropy.utility.messaging import get_logger
_LOG = get_logger('sankoff')
from dendropy import DataSet
_DEBUGGING = True

verbose = False
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-v', '--verbose',
                  dest='verbose',
                  action="store_true",
                  default=False,
                  help="Verbose execution mode")

    (options, args) = parser.parse_args()
    if len(args) == 0:
        sys.exit("Expecting a filename as an argument")

    if options.verbose:
        _LOG.setLevel(logging.DEBUG)

    tree_index = 0

    try:
        for f in args:
            fo = open(f, "rU")
            dataset = DataSet()
            dataset.read(stream=fo, schema="NEXUS")

            if len(dataset.taxon_sets) != 1:
                raise ValueError("Expecting one set of taxa in %s" % f)
            taxon_set = dataset.taxon_sets[0]

            if len(dataset.tree_lists) != 1:
                raise ValueError("Expecting one tree block in %s" % f)
            tree_list = dataset.tree_lists[0]

            if len(dataset.char_matrices) != 1:
                raise ValueError("Expecting one character matrix in %s" % f)
            char_mat = dataset.char_matrices[0]

            num_char = len(char_mat[0])
            taxon_to_state_set = char_mat.create_taxon_to_state_set_map()

            for taxon, chars in taxon_to_state_set.iteritems():
                _LOG.debug(taxon.label + ' ' + str(chars))
            for tree in tree_list:
                _LOG.debug(str(tree))
    except Exception as x:
        if _DEBUGGING:
            raise
        sys.exit(str(x))


