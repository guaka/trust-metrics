from Advogato import Advogato
from sets import Set

def evaluate(trustmetric, graph):
    #error_graph = graph.get_nodes() # same nodes, no edges

    abs_error = 0
    not_predicted_edges = 0

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
            not_predicted_edges += 1
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
    coverage = (num_edges - not_predicted_edges) / num_edges
    print "name:", trustmetric.__name__, "accuracy=", abs_error / num_edges


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

#####################
# The trust metric functions
#

def outa_tm(G, a, b):
    #average outgoing links of a
    return avg_or_zero(map(trust_on_edge, G.edges(a)))

def outb_tm(G, a, b):
    #average outgoing links of b
    return avg_or_zero(map(trust_on_edge, G.edges(b)))

def ebay_tm(G, a, b):
    return avg_or_zero(map(trust_on_edge, G.in_edges(b)))


def intersection_tm(G, a, b):
    intersection = Set(G[a]).intersection(Set(map(lambda x: x[0], G.in_edges(b))))
    if not intersection:
        #somehow outa_tm up to now :)
        return outa_tm(G, a, b)
    else:
        dict_a = dict(map(lambda x: (x[1], float(x[2]['level'])), G.edges(a)))
        dict_b = dict(map(lambda x: (x[0], float(x[2]['level'])), G.in_edges(b)))
        # now take the maximum of the minimum
        return max(map(lambda i: min(dict_a[i], dict_b[i]), intersection))

def moletrust_tm():
    pass

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

    import random

    if False:
        # For extended testing
        evaluate(lambda G,a,b: random.random(), advogato)
        evaluate(lambda G,a,b: random.choice([0, 0.6, 0.8, 1]), advogato)
        evaluate(lambda G,a,b: 0, advogato)
        evaluate(lambda G,a,b: 0.6, advogato)
        evaluate(lambda G,a,b: 0.8, advogato)
        evaluate(lambda G,a,b: 0.9, advogato)

    evaluate(intersection_tm, advogato) # 0.128261310511
    evaluate(ebay_tm, advogato)
    evaluate(outa_tm, advogato)  # this is the best from these "funny" trust metrics
    evaluate(outb_tm, advogato)

