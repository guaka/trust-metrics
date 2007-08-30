from trustlet.Advogato import get_graph_dot, Advogato
import random

class Random_tm:
    def predict_trust(self,graph,a,b):
        return random.random()

class Advogato_global_tm:
    pass

class Advogato_local_tm:
    pass

class Pagerank_tm:
    pass

class Ebay_tm:
    #predicted_trust(a,b)=average incoming links(b) # a does not matter
    pass

class Kasper_tm:
    #average outgoing links of a
    ## check the Jesus/Gandhi paradox: Jesus/Gandhi were good but too trustful, i.e. they were trusting also bad people and so do you if you trust their judgements.
    pass

class Zero_tm:
    pass

class One_tm:
    pass

class MoleTrust_tm:
    pass


def evaluate(Tm,graph):
    #error_graph=graph.get_nodes() # same nodes, no edges

    abs_error = 0
    not_predicted_edges = 0

    tm=Tm() # clever to pass the graph here, just once the TM is instantiated? 

    #Attention. Edges that are self loops might be problematic
    for edge in graph.edges():
        print "edge=",edge,
        graph.delete_edge(edge)

        #check if passing the graph all the time is not clever
        predicted_trust=tm.predict_trust(graph,edge[0],edge[1])

        if predicted_trust == None:
            not_predicted_edges += 1
        else:
            #add predicted_trust as the value on edge (A,B)
            abs_error += abs( predicted_trust - float(edge[2]['level']))

        print "error=",abs_error," real=",
        
        graph.add_edge(edge)

    print "Error=",abs_error

    num_edges = graph.number_of_edges()
    coverage = (num_edges - not_predicted_edges) / num_edges
    accuracy = abs_error / num_edges

import networkx

print "loading..."
#graph = get_graph_dot()
a = Advogato()
graph = networkx.read_dot(a.numbersfilepath)
print "end loading..."
evaluate(Random_tm,graph)

