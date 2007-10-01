from networkx import path
from sets import Set
import random


from advogato_tm import *
from pagerank_tm import *
from TrustMetric import *

'''
done:
-- ebay like (simple unpersonalized average)
-- predict always "master"
-- guakamole

to verify:
-- moletrust (the trivial one I proposed, I can do this)
-- advogato

to implement:
-- pagerank (find adaptation)
-- more?
'''                          

###############################################
# helpers
#

def avg_or_none(l):
    """Return the average of a list, or None in case the
    list is empty or a list of Nones

    >>> avg_or_none(range(6))
    2.5

    >>> print avg_or_none([None] * 6)
    None
    """
    l = filter(lambda x: (x is not None), l)
    if l:
        return float(sum(l)) / len(l)
    else:
        return None

def overlap(main_tm, fallback_tm):
    """overlap main_tm with fallback_tm
    
    """
    def overlap_tm(G, a, b):
        return main_tm(G, a, b) or fallback_tm(G, a, b)
    return overlap_tm

def rounder(tm):
    """round off trust values to 0.0, 0.2, 0.4, 0.6, 0.8, 1.0"""
    def rounder_tm(G, a, b):
        trust = tm(G, a, b)
        if trust is None:
            return None
        return round(trust * 5)/5.
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

random_tm = lambda G,a,b: random.random()
choice_tm = lambda l: (lambda G,a,b: random.choice(l))
constant_tm = lambda c: (lambda G,a,b: c)

never_tm = constant_tm(0)
always_tm = constant_tm(1)

def outa_tm(G, a, b):
    #average outgoing links of a
    return avg_or_none(map(G.trust_on_edge, G.out_edges(a)))

def outb_tm(G, a, b):
    #average outgoing links of b
    return avg_or_none(map(G.trust_on_edge, G.out_edges(b)))

def edges_a_tm(G, a, b):
    return avg_or_none(map(G.trust_on_edge, G.edges(a) + G.in_edges(a)))

def edges_b_tm(G, a, b):
    return avg_or_none(map(G.trust_on_edge, G.edges(b) + G.in_edges(b)))

def ebay_tm(G, a, b):
    return avg_or_none(map(G.trust_on_edge, G.in_edges(b)))

def intersection_tm(G, a, b):
    # probably nicer with a filter:
    intersection = Set(G[a]).intersection(Set(map(lambda x: x[0], G.in_edges(b))))
    if not intersection:
        return edges_a_tm(G, a, b)
    else:
        outa = dict(map(lambda x: (x[1], G.trust_on_edge(x)), G.out_edges(a)))
        inb = dict(map(lambda x: (x[0], G.trust_on_edge(x)), G.in_edges(b)))
        # now take the maximum of the minimum
        return max(map(lambda i: min(outa[i], inb[i]), intersection))



def moletrust_generator(horizon = 3, trust_threshold = 0.5, difficult_case_threshold = 0.4):
    def moletrust_tm(G, a, b):
        debug = False
        if debug:
            print "predict trust from", a, "to", b

        # Do something with connected_components here
        # UG = G.to_undirected()
        # subgraphs = connected_component_subgraphs(UG)
        # find a
        # if not b in subgraph_with_a:
        #   return None
        
        # path_length_dict and trust_map should be cached in a very smart way
        path_length_dict = path.single_source_shortest_path_length(G, a, horizon)
        if not b in path_length_dict or path_length_dict[b] > horizon:
            return None
        
        path_length_list = map(lambda x: (path_length_dict[x], x), path_length_dict)
        path_length_list.sort()  # order by distance

        # initialize trust map with node a and a bunch of empty dicts
        trust_map = [{a: 1.0}] + [{}] * horizon

        for (dist, node) in path_length_list[1:]:
            useful_in_edges = filter(lambda x: x[0] in trust_map[dist-1], G.in_edges(node))
            
            # We have to benchmark this, it could be a lot faster?
            #if len(useful_in_edges) == 1:
            #    pred_trust = G.trust_on_edge(useful_in_edges[0])

            # not considering the negative trust statements, very good for our accuracy! yay! big hugs!
            useful_in_edges = filter(lambda x: G.trust_on_edge(x) >= difficult_case_threshold, useful_in_edges)
            
            for edge in useful_in_edges:
                if debug: print "useful edge:", edge, "predecessor tvalue", trust_map[dist-1][edge[0]]
            pred_trust = weighted_average(map(lambda x: (G.trust_on_edge(x),
                                                         trust_map[dist-1][x[0]]),
                                              useful_in_edges))
            # sys.stdin.read()
        
            if debug:
                print "pred trust of", node, ":", pred_trust

            if node == b:
                return pred_trust

            # only keep edges over trust_threshold
            if pred_trust >= trust_threshold:
                trust_map[dist][node] = pred_trust
        return None
    return moletrust_tm



paolomole_tm = moletrust_generator(horizon = 3, trust_threshold = 0.5, difficult_case_threshold = 0)

guakamole_tm = moletrust_generator(horizon = 3, trust_threshold = 0.5, difficult_case_threshold = 0.5)

guakamole_full_tm = overlap(guakamole_tm, intersection_tm)





###################3

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

