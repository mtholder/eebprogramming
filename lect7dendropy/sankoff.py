#!/usr/bin/env python
import sys
from dendropy.utility.messaging import get_logger
_LOG = get_logger('sankoff')
from dendropy import DataSet
from dendropy.utility.error import DataParseError
_DEBUGGING = True
verbose = False

def get_min_edge_costs(step_mat_row, child_costs):
    min_score = step_mat_row[0] + child_costs[0]
    for i in xrange(1, len(step_mat_row)):
        y = step_mat_row[i] + child_costs[i]
        if y < min_score:
            min_score = y
    return min_score

def get_min_cost(step_mat_row, child_costs):
    total_cost = 0
    for e in child_costs:
        total_cost = total_cost + get_min_edge_costs(step_mat_row, e)
    return total_cost

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
            assert len(nd.child_nodes()) > 1
            child_list = nd.child_nodes()
            char_costs = []
            num_patterns = len(child_list[0].char_costs)
            for pattern_index in xrange(num_patterns):
                child_costs = []
                for c in child_list:
                    child_costs.append(c.char_costs[pattern_index])
                el = []
                for anc_state in xrange(num_states):
                    c = get_min_cost(step_matrix[anc_state], child_costs)
                    el.append(c)
                char_costs.append(el)
            nd.char_costs = char_costs
            if not nd.parent_node:
                score = 0
                for pattern_index in xrange(num_patterns):
                    score += min(nd.char_costs[pattern_index])
    return score

def pars_score_tree(tree, taxa_to_states, step_matrix=None):
    if step_matrix is None:
        step_matrix =  [ [0, 1, 1, 1],
                [1, 0, 1, 1],
                [1, 1, 0, 1],
                [1, 1, 1, 0],
            ]
    root = tree.seed_node
    root_children = root.child_nodes()
    node_list = [i for i in tree.postorder_node_iter()]
    return sankoff(node_list, step_matrix=step_matrix, taxa_to_state_set_map=taxa_to_states)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    (options, args) = parser.parse_args()
    if len(args) == 0:
        sys.exit("Expecting a filename as an argument")

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

            for n, tree in enumerate(tree_list):
                p_score = pars_score_tree(tree, taxon_to_state_set)
                print "Tree", n+1, p_score

    except Exception as x:
        if _DEBUGGING:
            raise
        sys.exit(str(x))





x='''    s_mat = [   [0, 5, 1, 5],
                [5, 0, 5, 1],
                [1, 5, 0, 5],
                [5, 1, 5, 0],
            ]
'''
