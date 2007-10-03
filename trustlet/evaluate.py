import random
import os, sys, time
from pprint import pprint

from Advogato import *
from trustmetrics import *
from pylab import *
from networkx import *
from helpers import *

__doc__ = """

Warning, this file will be deprecated very soon!
Oh wait, that means it's actually deprecated already!


    Attention: Edges that are self loops might be problematic
    
    Problem: This only evaluates the trust metric for where there was
    an edge already. We should probably add another evaluation,
    e.g. the 'distrust' evaluation, on all possible edges where there
    was no edge already.

"""



def evaluate(G, trustmetric, debug_interval = 1, max_edges = 0):
    """Deprecated"""
    #error_graph = graph.get_nodes() # same nodes, no edges

    num_unpredicted_edges = abs_err = sqr_err = count = 0
    start_time = prev_time = time.time()
    print "start time:", start_time
    edges = G.edges()
    max_edges = max_edges or len(edges)
    for edge in edges:
        G.delete_edge(edge)
        a, b, dummy = edge
        real_trust = G.trust_on_edge(edge)
        predicted_trust = trustmetric(G, a, b)

        #error_graph.add_edge(predicted_trust as the value on edge (a, b))
        if predicted_trust is None:
            num_unpredicted_edges += 1
        else:
            abs_err += abs(predicted_trust - real_trust)
            sqr_err += (lambda x:x*x)(predicted_trust - real_trust)
            
        count += 1.
        if debug_interval == 1:
            print edge, predicted_trust

        if divmod(count, debug_interval)[1] == 0:
            t = time.time()
            acc = abs_err / count
            acc2 = sqr_err / count
            unpredicted = num_unpredicted_edges / count
            avg_t = (t - start_time) / count
            eta = avg_t * (max_edges - count)
            print 'cnt', int(count), 'acc', acc, 'acc2', acc2, 'unpredicted', unpredicted, "avg time:", avg_t, "ETA", hms(eta)
            prev_time = t
        G.add_edge(edge)
        if max_edges == count:
            break

    num_predicted_edges = max_edges - num_unpredicted_edges
    coverage = (num_predicted_edges * 1.0) / max_edges
    accuracy =  abs_err / (num_predicted_edges or 1)

    output = (trustmetric.__name__, accuracy, coverage)
    pprint (output)
    return output 



def evaluator(G, tm_list):
    """Deprecated"""
    return map(lambda tm: evaluate(G, tm), tm_list)

        
if __name__ == "__main__":
    G = Kaitiaki(comp_threshold = 3)
            
    if True:
        evaluations = evaluator(G,
                            [paolo_moletm, guakamoletm, outa_tm, outb_tm, intersection_tm, always_tm,
                             lambda g,a,b: (avg_or_none([edges_a_tm(g,a,b), intersection_tm(g,a,b)])), ebay_tm])
    else:
        evaluations = evaluator(G, [advogato_tm])
    pprint(evaluations)


   
