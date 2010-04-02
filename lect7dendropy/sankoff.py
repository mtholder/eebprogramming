#!/usr/bin/env python
import sys
from dendropy.utility.messaging import get_logger
from dendropy.treecalc import fitch_down_pass, fitch_up_pass
from dendropy import DataSet
from dendropy.utility.error import DataParseError
_DEBUGGING = True
_LOG = get_logger('sankoff')
verbose = False

def get_min_edge_costs(step_mat_row, child_costs):
    min_score = step_mat_row[0] + child_costs[0]
    for i in xrange(1, len(step_mat_row)):
        y = step_mat_row[i] + child_costs[i]
        if y < min_score:
            min_score = y
    return min_score

def get_min_cost(step_mat_row, left_costs, right_costs):
    lc =  get_min_edge_costs(step_mat_row, left_costs)
    rc = get_min_edge_costs(step_mat_row, right_costs)
    return lc + rc

def sankoff(postorder_node_list, step_matrix, taxa_to_state_set_map):
    max_cost = 0
    num_states = len(step_matrix)
    for row in step_matrix:
        for cell in row:
            if cell > max_cost:
                max_cost = cell
    impossible_cost = 1 + max_cost

    score = 0
    for nd in postorder_node_list:
        if nd.is_leaf():
            char_costs = []
            for char_ss in taxa_to_state_set_map[nd.taxon]:
                el = [impossible_cost]*num_states
                for s in char_ss:
                    el[s] = 0
                char_costs.append(el)
            nd.char_costs = char_costs
        else:
            assert len(nd.child_nodes()) == 2
            left_c, right_c = nd.child_nodes()
            char_costs = []
            num_patterns = len(left_c.char_costs)
            for pattern_index in xrange(num_patterns):
                left_costs = left_c.char_costs[pattern_index]
                right_costs = right_c.char_costs[pattern_index]
                el = []
                for anc_state in xrange(num_states):
                    c = get_min_cost(step_matrix[anc_state], left_costs, right_costs)
                    el.append(c)
                char_costs.append(el)
            nd.char_costs = char_costs
            if not nd.parent_node:
                score = 0
                for pattern_index in xrange(num_patterns):
                    score += min(nd.char_costs[pattern_index])
        #print nd.char_costs
    return score


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) == 0:
        sys.exit("Expecting a filename as an argument")

    char_index = 0
    char_mat_index = 0
    taxon_set_index = 0
    tree_list_index = 0
    tree_index = 0

    try:
        for f in args:
            fo = open(f, "rU")
            dataset = DataSet()
            try:
                dataset.read(stream=fo, schema="NEXUS")
            except DataParseError as dfe:
                raise ValueError(str(dfe))
            if len(dataset.taxon_sets) != 1:
                raise ValueError("Expecting one set of taxa in %s" % f)
            if len(dataset.tree_lists) != 1:
                raise ValueError("Expecting one tree in %s" % f)
            if len(dataset.char_matrices) != 1:
                raise ValueError("Expecting one character matrix in %s" % f)
            char_mat = dataset.char_matrices[char_mat_index]
            num_char = len(char_mat[0])
            taxon_set = dataset.taxon_sets[taxon_set_index]
            tree = dataset.tree_lists[tree_list_index][tree_index]
            p_score = 0
            state_alphabet = char_mat.state_alphabets[0]
            taxon_to_state_indices = char_mat.create_taxon_to_state_set_map()

            if not tree.is_rooted:
                raise ValueError("Tree must be rooted")

            root = tree.seed_node
            root_children = root.child_nodes()
            if len(root_children) != 2:
                raise ValueError("Expecting a binary rooted tree.  Root has more than 2 children!")


            node_list = [i for i in tree.postorder_node_iter()]
            for nd in node_list:
                c = nd.child_nodes()
                if c:
                    if len(c) != 2:
                        raise ValueError("Tree must be fully resolved")
            s_mat = [   [0, 1, 1, 1],
                        [1, 0, 1, 1],
                        [1, 1, 0, 1],
                        [1, 1, 1, 0],
                    ]
            s_mat = [   [0, 5, 1, 5],
                        [5, 0, 5, 1],
                        [1, 5, 0, 5],
                        [5, 1, 5, 0],
                    ]
            p_score = sankoff(node_list, step_matrix=s_mat, taxa_to_state_set_map=taxon_to_state_indices)
            print p_score
            sys.exit(0)
    except Exception as x:
        if _DEBUGGING:
            raise
        sys.exit(str(x))

