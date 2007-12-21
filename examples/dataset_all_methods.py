"""
Create a network and call all its method on it.
"""

# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')

from Dataset.Dummy import DummyNetwork

# create some datasets
dummy = DummyNetwork()
unweighted = DummyUnweightedNetwork() #on unweighted networks, some methods should return nothing
undirected = DummyUndirectedNetwork() #on undirected networks, some methods should return nothing
unconnected_undirected_unweighted = DummyUnconnectedUndirectedUnweighted() # should read from "data/unconnected_undirected_unweighted.dot"
unconnected_directed_weighted = DummyUnconnectedUndirectedUnweighted() # should read from "data/unconnected_directed_weighted.net"
advogato_network = Advogato()

datasets = [dummy, unweighted , undirected, unconnected_undirected_unweighted, unconnected_directed_weighted, advogato]

def call_all_methods(N):
    print "#--------------------------------------------"
    print "# Network: ",N.__name__
    print "get_number_of_nodes()="+N.get_number_of_nodes()
    print "get_number_of_edges()="+N.get_number_of_edges()
    print "is_directed()="+N.is_directed()
    print "------- degrees ----------------"
    print "avg_in_degree()="+N.avg_in_degree()
    print "avg_out_degree()="+N.avg_out_degree()
    print "stddev_in_degree()="+N.avg_in_degree()
    print "stddev_out_degree()="+N.avg_out_degree()
    print "get_degree_correlation_coefficient()="+N.get_degree_correlation_coefficient()
    print "degree_histogram()="+N.degree_histogram() # see https://networkx.lanl.gov/reference/networkx/networkx.function-module.html#degree_histogram
    print "get_powerlaw_exponent()="+N.get_powerlaw_exponent()
    print "------- components -------------"
    print "is_strongly_connected()="+N.is_strongly_connected() # this method should simply call the function component.is_strongly_connected(N), Remove this comment when implemented 
    print "is_connected()="+N.is_connected() # this method should simply call the function component.is_connected(N), Remove this comment when implemented 
    print "get_number_nodes_in_strongly_connected_component()="+N.get_number_nodes_in_strongly_connected_component()
    print "get_number_nodes_in_connected_component()="+N.get_number_nodes_in_connected_component()
    print "get_largest_strongly_connected_component()="+N.get_largest_strongly_connected_component()
    print "get_largest_connected_component()="+N.get_largest_connected_component()
    print "avg_distance()="+N.get_number_nodes_in_connected_component()
    print "get_cluster_coefficient()="+N.get_cluster_coefficient() #based on N.clustering() of networkx? 
    print "average_clustering()="+N.average_clustering() # this method should simply call the function cluster.average_clustering(N), Remove this comment when implemented
    print "transitivity()="+N.transitivity() # this method should simply call the function cluster.transitivity(N), Remove this comment when implemented
    print "avg_node_node_shortest_distance()="+N.avg_node_node_shortest_distance() # should probably call path.all_pairs_shortest_path_length(G, cutoff=None) # also pay attention to the fact there are 2 or more connected components
    print "--------- weights on edges --------"
    print "is_weighted()="+N.is_weighted()
    print "has_discrete_weights()="+N.has_discrete_weights()
    print "get_weights()="+N.get_weights() # return a sorted array of the possible weight values (if discrete)
    print "get_min_possible_weigh()="+N.get_min_possible_weigh()
    print "get_max_possible_weigh()="+N.get_max_possible_weigh()
    print "get_number_of_edges(get_weights()[0])="+N.get_number_of_edges(get_weights()[0]) #return the number of edges whose value is the smallest of the possible values
    print "--------- reciprocation -----------"
    print "get_avg_reciprocity()="+N.get_avg_reciprocity()
    print "print_reciprocity_matrix()="+print_reciprocity_matrix()

    print ".... phew!"
    
for network in networks:
    call_all_methods(network)
