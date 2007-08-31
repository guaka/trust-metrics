from trustlet.Advogato import get_graph_dot, Advogato


def evaluate(trustmetric, graph):
    #error_graph = graph.get_nodes() # same nodes, no edges

    abs_error = 0
    not_predicted_edges = 0

    # tm=TrustMetric() # clever to pass the graph here, just once the TM is instantiated? 

    i = 0
    #Attention. Edges that are self loops might be problematic
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
        if divmod(i, 10000)[1] == 0:
            print "acc=",abs_error / i #," real=",
        graph.add_edge(edge)

    print "Error=",abs_error

    num_edges = graph.number_of_edges()
    coverage = (num_edges - not_predicted_edges) / num_edges
    print "accuracy=",abs_error / num_edges

# in ipython use:
# reload(evaluate); evaluate.evaluate(Random_tm, graph)



def outa_tm(G, a, b):
    #average outgoing links of a
    trust_list = map(lambda x: float(x[2]['level']), G.edges(a))
    if trust_list:
        return sum(trust_list) / len(trust_list)
    else:
        return 0

def outb_tm(G, a, b):
    #average outgoing links of b
    trust_list = map(lambda x: float(x[2]['level']), G.edges(b))
    if trust_list:
        return sum(trust_list) / len(trust_list)
    else:
        return 0

## check the Jesus/Gandhi paradox: Jesus/Gandhi were good but too trustful, i.e. they were trusting also bad people and so do you if you trust their judgements.


def MoleTrust_tm():
    pass

def advogato_global_tm(graph, a, b):
    pass

def advogato_local_tm(graph, a, b):
    pass

class Pagerank_tm:
    pass

def ebay_tm(G, a, b):
    #predicted_trust(a,b)=average incoming links(b) # a does not matter
    pass



if __name__ == "__main__":
    import networkx
    a = Advogato()
    graph = networkx.read_dot(a.numbersfilepath)

    import random
    evaluate(lambda G,a,b: random.random(), graph)
    evaluate(lambda G,a,b: 0, graph)
    evaluate(lambda G,a,b: 0.6, graph)
    evaluate(lambda G,a,b: 0.8, graph)
    evaluate(lambda G,a,b: 0.9, graph)
    evaluate(outa_tm, graph)  # this is the best from these "funny" trust metrics
    evaluate(outb_tm, graph)
