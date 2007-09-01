import random
import os, sys, time
from pprint import pprint
from sets import Set

from Advogato import Advogato
from networkx import path


"""
    Attention: Edges that are self loops might be problematic
    
    Problem: This only evaluates the trust metric for where there was
    an edge already. We should probably add another evaluation,
    e.g. the 'distrust' evaluation, on all possible edges where there
    was no edge already.

"""


def evaluate(graph, trustmetric, debug_interval = 1000):
    #error_graph = graph.get_nodes() # same nodes, no edges

    num_unpredicted_edges = abs_err = sqr_err = count = 0
    start_time = prev_time = time.time()
    for edge in graph.edges():
        graph.delete_edge(edge)

        predicted_trust = trustmetric(graph, edge[0], edge[1])

        #error_graph.add_edge(predicted_trust as the value on edge (a, b))
        if predicted_trust == None:
            num_unpredicted_edges += 1
        else:
            abs_err += abs(predicted_trust - trust_on_edge(edge))
            sqr_err += (lambda x:x*x)(abs(predicted_trust - trust_on_edge(edge)))
            
        count += 1.
        if divmod(count, debug_interval)[1] == 0:
            t = time.time()
            acc = abs_err / count
            acc2 = sqr_err / count
            unpredicted = num_unpredicted_edges / count
            print 'cnt', int(count), 'acc', acc, 'acc2', acc2, 'unpredicted', unpredicted, "avg time:", (t - start_time) / count
            prev_time = t
        graph.add_edge(edge)

    num_edges = graph.number_of_edges()
    num_predicted_edges = num_edges - num_unpredicted_edges
    coverage = (num_predicted_edges * 1.0) / num_edges
    accuracy =  abs_err / (num_predicted_edges or 1)

    output = (trustmetric.__name__, accuracy, coverage)
    pprint (output)
    return output 


def evaluator(graph, tm_list):
    return map(lambda tm: evaluate(graph, tm), tm_list)

###############################################
#
#
# helper functions
trust_on_edge = lambda x: float(x[2]['level'])

def avg_or_none(l):
    l = filter(lambda x: (x is not None), l)
    if l:
        return float(sum(l)) / len(l)
    else:
        return None

def trust_avg(a, b):
    if a is None and b is None:
        return None
    elif a is None:
        return b
    elif b is None:
        return a
    return (a + b) / 2.
            
#####################
# The trust metric functions
#

def outa_tm(G, a, b):
    #average outgoing links of a
    return avg_or_none(map(trust_on_edge, G.out_edges(a)))

def outb_tm(G, a, b):
    #average outgoing links of b
    return avg_or_none(map(trust_on_edge, G.out_edges(b)))

def edges_a_tm(G, a, b):
    return avg_or_none(map(trust_on_edge, G.edges(a) + G.in_edges(a)))

def edges_b_tm(G, a, b):
    return avg_or_none(map(trust_on_edge, G.edges(b) + G.in_edges(b)))

def ebay_tm(G, a, b):
    return avg_or_none(map(trust_on_edge, G.in_edges(b)))

def intersection_tm(G, a, b):
    intersection = Set(G[a]).intersection(Set(map(lambda x: x[0], G.in_edges(b))))
    if not intersection:
        return edges_a_tm(G, a, b)
    else:
        outa = dict(map(lambda x: (x[1], trust_on_edge(x)), G.out_edges(a)))
        inb = dict(map(lambda x: (x[0], trust_on_edge(x)), G.in_edges(b)))
        # now take the maximum of the minimum
        return max(map(lambda i: min(outa[i], inb[i]), intersection))


def weighted_average(l):
    if not l:
        return 0
    num = dem = 0
    for a,b in l:
        num += a*b
        dem += b
    if not dem:
        return 0
    return num / dem

def moletrust_generator(horizon = 3, trust_threshold = 0.5, difficult_case_threshold = 0.4):
    def moletrust_tm(G, a, b):
        debug = False
        if debug:
            print "predict trust from", a, "to", b

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
            #    pred_trust = trust_on_edge(useful_in_edges[0])

            # not considering the negative trust statements, very good for our accuracy! yay! big hugs!
            useful_in_edges = filter(lambda x: trust_on_edge(x) >= difficult_case_threshold, useful_in_edges)
            
            for edge in useful_in_edges:
                if debug: print "useful edge:", edge, "predecessor tvalue", trust_map[dist-1][edge[0]]
            pred_trust = weighted_average(map(lambda x: (trust_on_edge(x),
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

paolo_moletm = moletrust_generator(horizon = 3, trust_threshold = 0.5, difficult_case_threshold = 0)
guaka_moletm = moletrust_generator(horizon = 3, trust_threshold = 0.5, difficult_case_threshold = 0.5)


# we already have guakamole now!
def advogato_global_tm(graph, a, b):
    pass

def advogato_local_tm(graph, a, b):
    pass

def PageRank_tm(G, a, b):
    pass


if __name__ == "__main__":
    syntax_debugging = False
    if syntax_debugging:
        advogato = Advogato("tiny")
    else:
        advogato = Advogato()
            
    evaluations = evaluator(advogato,
                            [ # moletrust_tm,
                             outa_tm,
                             outb_tm,
                             intersection_tm,
                             lambda g,a,b: (trust_avg(edges_a_tm(g,a,b), intersection_tm(g,a,b))),
                             ebay_tm,
                             ])
    pprint(evaluations)

    simple_tms = [lambda G,a,b: random.random(),
                  lambda G,a,b: random.choice([0, 0.6, 0.8, 1]),
                  lambda G,a,b: 0,
                  lambda G,a,b: 0.6,
                  lambda G,a,b: 0.8,
                  lambda G,a,b: 0.9
                  ]

    # evals = evaluator(advogato, simple_tms)
    # pprint(evals)
   
