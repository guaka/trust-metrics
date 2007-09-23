import random
import os, sys, time
from pprint import pprint

from Advogato import *
from trustmetrics import *
from pylab import *
from networkx import *

"""
    Attention: Edges that are self loops might be problematic
    
    Problem: This only evaluates the trust metric for where there was
    an edge already. We should probably add another evaluation,
    e.g. the 'distrust' evaluation, on all possible edges where there
    was no edge already.

"""

def hms(t):
    t = int(t)
    m, s = divmod(t, 60)
    h, m = divmod(m, 60)
    return str(h)+'h'+str(m)+'m'+str(s)+'s'



def evaluate(graph, trustmetric, debug_interval = 1, max_edges = 0):
    #error_graph = graph.get_nodes() # same nodes, no edges

    num_unpredicted_edges = abs_err = sqr_err = count = 0
    start_time = prev_time = time.time()
    print "start time:", start_time
    edges = graph.edges()
    max_edges = max_edges or len(edges)
    for edge in edges:
        graph.delete_edge(edge)
        a, b, dummy = edge
        real_trust = graph.trust_on_edge(edge)
        predicted_trust = trustmetric(graph, a, b)

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
        graph.add_edge(edge)
        if max_edges == count:
            break

    num_predicted_edges = max_edges - num_unpredicted_edges
    coverage = (num_predicted_edges * 1.0) / max_edges
    accuracy =  abs_err / (num_predicted_edges or 1)

    output = (trustmetric.__name__, accuracy, coverage)
    pprint (output)
    return output 



def classy_evaluate(G, TM, debug_interval = 1, max_edges = 0):
    def output():
        if debug_interval == 1:
            print edge, predicted_trust

        if divmod(count, debug_interval)[1] == 0:
            t = time.time()
            acc = abs_err / count
            # acc2 = sqr_err / count
            unpredicted = num_unpredicted_edges / count
            avg_t = (t - start_time) / count
            eta = avg_t * (max_edges - count)
            print 'cnt', int(count), 'acc', acc, 'unpredicted', unpredicted, "avg time:", avg_t, "ETA", hms(eta)
            prev_time = t

    def save_pred_graph():
        gtm_path = os.path.join(G.path, TM.__name__)
        if not os.path.exists(gtm_path):
            os.mkdir(gtm_path)
        pred_path = os.path.join(gtm_path, "pred_graph.dot")
        print "Saving error graph as", pred_path
        G.G = pred_graph
        write_dot(pred_graph, pred_path)

    pred_graph = XDiGraph()
    for n in G.nodes():
        pred_graph.add_node(n)

    num_unpredicted_edges = abs_err = sqr_err = count = 0
    start_time = prev_time = time.time()
    print "start time:", start_time
    tm = TM(G)
    max_edges = max_edges or len(G.edges())
    for edge in G.edges():
        predicted_trust = tm.leave_one_out(edge)
        print predicted_trust
        pred_graph.add_edge(edge[0], edge[1], {'predtrust': str(predicted_trust)})
        if predicted_trust is None:
            num_unpredicted_edges += 1
        else:
            abs_err += abs(predicted_trust - G.trust_on_edge(edge))

        count += 1.
        output()
        if max_edges == count:
            break

    num_predicted_edges = max_edges - num_unpredicted_edges
    coverage = (num_predicted_edges * 1.0) / max_edges
    accuracy = abs_err / (num_predicted_edges or 1)

    output = (TM.__name__, accuracy, coverage)
    pprint (output)
    
    save_pred_graph()

    return output 

def evaluator(G, tm_list):
    return map(lambda tm: evaluate(G, tm), tm_list)




if __name__ == "__main__":
    G = Kaitiaki(comp_threshold = 3)
            
    if True:
        evaluations = evaluator(G,
                            [paolo_moletm, guakamoletm, outa_tm, outb_tm, intersection_tm,
                             lambda g,a,b: (avg_or_none([edges_a_tm(g,a,b), intersection_tm(g,a,b)])), ebay_tm])
    else:
        evaluations = evaluator(G, [advogato_tm])
    pprint(evaluations)


   
