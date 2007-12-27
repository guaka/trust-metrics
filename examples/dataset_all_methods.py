"""
Create a network and call all its method on it.
"""

# make sure example can be run from examples/ directory
# import sys
# sys.path.append('../trustlet')

from trustlet.Dataset.Dummy import DummyNetwork, DummyWeightedNetwork
from trustlet.Dataset.Advogato import AdvogatoNetwork, SqueakFoundationNetwork



def call_all_methods(N):
    """Call a bunch of methods of the network."""
    
    def call_methods(method_names):
        """Helper, works with list or with just one."""

        for method_name in list(method_names):
            if hasattr(N, method_name):
                method = getattr(N, method_name)
                if hasattr(method, "__call__"):
                    print method_name, method()
                else:
                    print method_name, method #is not actually a method
            else:
                print N.__class__.__name__, "does not have the method", method_name

    print "\n\nNetwork: ", N.__class__.__name__

    call_methods(("number_of_nodes", "number_of_edges", "is_directed"))

    print "\ndegrees"
    call_methods(("avg_in_degree", "avg_out_degree", "std_in_degree", "std_out_degree"))
    #TODO: print "get_degree_correlation_coefficient()="+N.get_degree_correlation_coefficient()
    call_methods(("degree_histogram", "powerlaw_exponent"))

    print "\ncomponents"

    call_methods(("is_strongly_connected",
                  "is_connected",
                  "number_nodes_in_strongly_connected_component",
                  "number_nodes_in_connected_component",
                  "largest_strongly_connected_component",
                  "largest_connected_component",
                  "avg_distance",
                  "cluster_coefficient", #based on N.clustering() of networkx?
                  "average_clustering", #call the function cluster.average_clustering(N)
                  "transitivity()", # call the function cluster.transitivity(N)
                  # call path.all_pairs_shortest_path_length(G, cutoff=None) # also pay attention to the fact there are 2 or more connected components
                  "avg_node_node_shortest_distance",
                  ))

    print "\nweights on edges"
    call_methods(("is_weighted",
                  "has_discrete_weights",
                  "weights", # return a sorted array of the possible weight values (if discrete)
                  "min_possible_weight", 
                  "max_possible_weight", 
                  ))

    # TODO: return the number of edges whose value is the smallest of the possible values
    # print "get_number_of_edges(get_weights()[0])", N.get_number_of_edges(get_weights()[0])

    print "\nreciprocation"
    call_methods(("get_avg_reciprocity",
                  "print_reciprocity_matrix"))
    print "\ncontroversiality"

    # get the average controversiality of users with at least 3 incoming edges
    # controversiality could be simply the standard deviation of received trust statements
    # TODO: print "avg_controversiality(3)", N.get_avg_controversiality(3)
    
    # number of users whose controversiality is > 0.2 and received at least 2 incoming edges
    # TODO: print "get_number_of_controversial_nodes(3, 0.2)", N.get_number_of_controversial_nodes(3, 0.2)


# create some datasets
dummy = DummyNetwork()
dummy_weighted = DummyWeightedNetwork()

# unweighted = DummyUnweightedNetwork() #on unweighted networks, some methods should return nothing
# undirected = DummyUndirectedNetwork() #on undirected networks, some methods should return nothing
# unconnected_undirected_unweighted = DummyUnconnectedUndirectedUnweighted() # should read from "data/unconnected_undirected_unweighted.dot"
# unconnected_directed_weighted = DummyUnconnectedUndirectedUnweighted() # should read from "data/unconnected_directed_weighted.net"

squeak_network = SqueakFoundationNetwork()
# advogato_network = AdvogatoNetwork()

# datasets = [dummy, unweighted, undirected, unconnected_undirected_unweighted, unconnected_directed_weighted, advogato]
datasets = [dummy,
            dummy_weighted,
            squeak_network,
            # advogato_network,
            ]

for network in datasets:
    call_all_methods(network)
