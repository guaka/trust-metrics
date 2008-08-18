"""
These are implementations of relatively simple trust metrics and
some helper functions. All of these work tm(G,a,b) calculates the
trust that a can have in b. For global trust metrics a will be
ignored.
"""


from networkx import path
from sets import Set
import random

from advogato_tm import *
from pagerank_tm import *




###############################################
# helpers
#

def avg_or_none(in_list):
    """Return the average of a list, or 0.0 in case the
    list is empty or a list of Nones

    >>> avg_or_none(range(6))
    2.5

    >>> print avg_or_none([None] * 6)
    0.0
    """
    filt_list = [e
                 for e in in_list
                 if e is not None]
    if filt_list:
        return float(sum(filt_list)) / len(filt_list)
    else:
        return 0.0

def overlap(main_tm, fallback_tm):
    """overlap main_tm with fallback_tm
    
    """
    def overlap_tm(G, a, b):
        return main_tm(G, a, b) or fallback_tm(G, a, b)
    return overlap_tm


def rounder(tm, steps = 5):
    """Round off trust values to 0.0, 0.2, 0.4, 0.6, 0.8, 1.0."""
    def rounder_tm(G, a, b):
        trust = tm(G, a, b)
        if trust is None:
            return None
        return round(trust * steps) / float(steps)
    return rounder_tm


def weighted_average(l):
    """
    >>> weighted_average(map(lambda x: (1.0 * x, x*x), range(10)))
    7.1052631578947372
    """
    if not l:
        return 0
    num = dem = 0
    for a,b in l:
        num += a*b
        dem += b
    if not dem:
        return 0
    return num / dem

#####################
# The trust metric functions
#

function_tm = lambda f: (lambda G,a,b: f)

choice_tm = lambda l: function_tm(random.choice(l))
random_tm = function_tm(random.random())

never_tm = function_tm(0)
always_tm = function_tm(1)

def _test1():
    """
    >>> print never_tm(1, 1, 1)
    0

    >>> print always_tm(0, 0, 0)
    1

    >>> print choice_tm([3, 3, 3])(0,0,0)
    3
    """
    pass

def outa_tm(G, a, b):
    """Average outgoing links of a"""
    return avg_or_none(map(G.trust_on_edge, G.out_edges(a)))

def outb_tm(G, a, b):
    """Average outgoing links of b"""
    return avg_or_none(map(G.trust_on_edge, G.out_edges(b)))

def edges_a_tm(G, a, b):
    """Average of outgoing and incoming edges of a"""
    return avg_or_none(map(G.trust_on_edge, G.edges(a) + G.in_edges(a)))

def edges_b_tm(G, a, b):
    """Average of outgoing and incoming edges of b"""
    return avg_or_none(map(G.trust_on_edge, G.edges(b) + G.in_edges(b)))

def ebay_tm(G, a, b):
    """Average of incoming edges of b"""
    return avg_or_none(map(G.trust_on_edge, G.in_edges(b)))

def always_master(G, a, b):
    """Always return 1.0 (i.e. Master)"""
    return 1.0

def always_journeyer(G, a, b):
    """Always return 0.8 (i.e. Journeyer)"""
    return 0.8

def always_apprentice(G, a, b):
    """Always return 0.6 (i.e. Apprentice)"""
    return 0.6

def always_observer(G, a, b):
    """Always return 1.0 (i.e. Observer)"""
    return 0.4

def random_tm(G, a, b):
    """Return a random value between 0.4 and 1.0"""
    return random.random()*0.6+0.4

def wikiRandom_tm(G, a, b):
    """ Return a random number between 0.0 and 1.0 """
    return random.random()

def intersection_tm(G, a, b):
    """Find the intersection (nodes between a and b, say ni), and
    return the maximum of the minimum of the trust on the edges, i.e.
    max(min(t(a,ni),t(ni,b))), otherwise return avg of in and out
    edges of a (this choice seems arbitrary but it works well!)"""
    # Find the nodes between a and b (probably nicer with a filter)
    intersection = Set(G[a]).intersection(Set(map(lambda x: x[0], G.in_edges(b))))
    if not intersection:
        return edges_a_tm(G, a, b)
    else:
        outa = dict(map(lambda x: (x[1], G.trust_on_edge(x)), G.out_edges(a)))
        inb = dict(map(lambda x: (x[0], G.trust_on_edge(x)), G.in_edges(b)))
        # now take the maximum of the minimum
        return max(map(lambda i: min(outa[i], inb[i]), intersection))


def moletrust_generator(horizon = 6, pred_node_trust_threshold = 0.0,
                        edge_trust_threshold = 0.0):
    """Generate moletrust trust metric functions.

    Parameters:

      horizon: how many levels deep to search the network for a path
      (the bigger the horizon the slower the calculation)

      pred_node_trust_threshold: if an edge in the calculated chain
      has a trust value below this it will be discarded, because we
      know from this node on the chain is distrusted.

      edge_trust_threshold: an edge with trust < edge_trust_threshold
      will be thown out.
    """
    def moletrust_tm(G, a, b, rh = False):
        #it is useful to mark every moletrust with his horizon
        #on the datasets folder
        if rh:
            return horizon

        debug = False
        if debug:
            print "predict trust from", a, "to", b

        # Do something with connected_components here
        # UG = G.to_undirected()
        # subgraphs = connected_component_subgraphs(UG)
        # find a
        # if not b in subgraph_with_a:
        #   return 0.0
        
        # path_length_dict and trust_map should be cached in a very smart way
        path_length_dict = path.single_source_shortest_path_length(G, a, horizon)
        if not b in path_length_dict or path_length_dict[b] > horizon:
            return 0.0
        
        path_length_list = map(lambda (x,y): (y,x), path_length_dict.items())
        path_length_list.sort()  # order by distance

        # initialize trust map with node a and a bunch of empty dicts
        trust_map = [{a: 1.0}] + [{}] * horizon

        for (dist, node) in path_length_list[1:]:
            useful_in_edges = filter(lambda x: 
                                     x[0] in (trust_map[dist-1]), 
                                     G.in_edges(node))
            
            # We have to benchmark this, it could be a lot faster?
            #if len(useful_in_edges) == 1:
            #    pred_trust = G.trust_on_edge(useful_in_edges[0])

            # not considering the negative trust (or e.g. <0.5)
            # statements, very good for our accuracy! yay! big hugs!
            useful_in_edges = filter(lambda x: (G.trust_on_edge(x) >= 
                                                edge_trust_threshold), 
                                     useful_in_edges)
            
            for edge in useful_in_edges:
                if debug: 
                    print ("useful edge:", edge, 
                           "predecessor tvalue", trust_map[dist-1][edge[0]])
            pred_trust = weighted_average(map(lambda x: (G.trust_on_edge(x),
                                                         trust_map[dist-1][x[0]]),
                                              useful_in_edges))
            if node == b:
                return pred_trust

            # only keep edges over pred_node_trust_threshold
            if pred_trust >= pred_node_trust_threshold:
                trust_map[dist][node] = pred_trust
        return 0.0
    return moletrust_tm



paolomole_tm = moletrust_generator(horizon = 3, pred_node_trust_threshold = 0.5, edge_trust_threshold = 0)

guakamole_tm = moletrust_generator(horizon = 3, pred_node_trust_threshold = 0.5, edge_trust_threshold = 0.5)

guakamole_full_tm = overlap(guakamole_tm, intersection_tm)


###################

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

