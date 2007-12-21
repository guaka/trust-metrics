"""
Create a network and call all its method on it.
"""

# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')

from Dataset.Dummy import DummyNetwork

# create some datasets
D = DummyNetwork()
NW = DummyUnweightedNetwork() #on unweighted networks, some methods should return nothing
UD = DummyUndirectedNetwork() #on undirected networks, some methods should return nothing

datasets = [D,U]

def call_all_methods(N):
    print "#--------------------------------------------"
    print "# Network: ",N.__name__
    print "get_number_of_nodes()="+N.get_number_of_nodes()
    print "get_number_of_edges()="+N.get_number_of_edges()
    print "is_directed()="+N.is_directed()
    print "avg_in_degree()="+N.avg_in_degree()
    print "avg_out_degree()="+N.avg_out_degree()
    print "stddev_in_degree()="+N.avg_in_degree()
    print "stddev_out_degree()="+N.avg_out_degree()
    print "clustering()="+N.clustering()
    print "get_number_nodes_in_strongly_connected_component()="+N.get_number_nodes_in_strongly_connected_component()
    print "get_number_nodes_in_connected_component()="+N.get_number_nodes_in_connected_component()
    print "avg_distance()="+N.get_number_nodes_in_connected_component()
    print ".... more in a second"

for network in networks:
    call_all_methods(network)
