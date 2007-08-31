from Advogato import Advogato
from sets import Set
from networkx import path
from pprint import pprint
import random

def evaluate(graph, trustmetric):
    #error_graph = graph.get_nodes() # same nodes, no edges

    abs_error = 0
    num_unpredicted_edges = 0

    # tm=TrustMetric() # clever to pass the graph here, just once the TM is instantiated? 

    i = 0
    """
    Attention: Edges that are self loops might be problematic
    
    Problem: This only evaluates the trust metric for where there was
    an edge already. We should probably add another evaluation,
    e.g. the 'distrust' evaluation, on all possible edges where there
    was no edge already.

    """
    for edge in graph.edges():
        #print "edge=",edge,
        graph.delete_edge(edge)

        predicted_trust = trustmetric(graph, edge[0], edge[1])

        if predicted_trust == None:
            num_unpredicted_edges += 1
        else:
            #add predicted_trust as the value on edge (A,B)
            abs_error += abs(predicted_trust - float(edge[2]['level']))

            """
            Maybe it's also interesting to keep track of an error
            value where too much trust is worse than not trusting
            enough?
            """
            
        i += 1
        if divmod(i, 3000)[1] == 0:
            print "acc=",abs_error / i #," real=",
        graph.add_edge(edge)

    # print "Error=",abs_error

    num_edges = graph.number_of_edges()
    num_predicted_edges = num_edges - num_unpredicted_edges
    coverage = (num_predicted_edges * 1.0) / num_edges
    accuracy =  abs_error / (num_predicted_edges or 1)

    output=(trustmetric.__name__, accuracy, coverage)
    pprint(output)
    return output 


def evaluator(graph, tm_list):
    return map(lambda tm: evaluate(graph, tm), tm_list)

###############################################
#
#
# helper functions
trust_on_edge = lambda x: float(x[2]['level'])

def avg_or_zero(l):
    if l:
        return sum(l) / len(l)
    else:
        return 0

def avg_or_none(l):
    if l:
        return sum(l) / len(l)
    else:
        return None

def trust_avg(a,b):
    if a is None:
        if b is None:
            return None
        else:
            return b
    else:
        if b is None:
            return a
        else:
            return (a + b) / 2
            
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
        outa = dict(map(lambda x: (x[1], float(x[2]['level'])), G.out_edges(a)))
        inb = dict(map(lambda x: (x[0], float(x[2]['level'])), G.in_edges(b)))
        # now take the maximum of the minimum
        return max(map(lambda i: min(outa[i], inb[i]), intersection))

def moletrust_tm(G,a,b):
    from networkx import path
    horizon = 3

    # Remember to remove all the edges with value < 0.6
    dict_of_paths = path.single_source_shortest_path_length(G,a,horizon)
    list_of_node_dist = map(lambda x: (dict_of_paths[x], x), dict_of_paths)
    list_of_node_dist.sort()

    dist_map = [{a: 1.0}]
    for (dist, node) in list_of_node_dist[1:]:
        print node, dist
        #get all the edges G.in_edges(node) and at distance dist-1

        in_edges = dict(map(lambda x: (x[0], trust_on_edge(x)), (advogato.in_edges(node))))
        useful_incoming_edges = Set(in_edges).intersection(dist_map[dist-1]
        
        dist_map[dist] = (node, trust_value)
        

    return 0

def advogato_global_tm(graph, a, b):
    pass

def advogato_local_tm(graph, a, b):
    pass

def Pagerank_tm(G, a, b):
    pass


if __name__ == "__main__":
    syntax_debugging = False
    if syntax_debugging:
        advogato = Advogato("tiny")
    else:
        advogato = Advogato()

    evaluations = evaluator(advogato,
                            [# edges_a_tm,
                             # edges_b_tm,
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
