"""
Create networks, create trust metrics, test trust metrics on these datasets (also restricting to a certain percentage of edges)
"""

# make sure example can be run from examples/ directory

from trustlet import *


# create datasets
dummy_network = AdvogatoNetwork(download=True,date='2008-05-12')

# create trust metrics
# create the predgraphs based on leave-one-out (also with ratios)
# predict 10% of edges with leave-one-out
pred_graph = PredGraph(TrustMetric( dummy_network,moletrust_generator( horizon = 2, pred_node_trust_threshold = 0.5) )
                       # predict_ratio = 0.5
                       )

# show evaluation measures
print ""
print "abs_error: ",pred_graph.abs_error()
#pred_graph.show_table()


# create trust metrics
# create the predgraphs based on leave-one-out (also with ratios)
# predict 10% of edges with leave-one-out
pred_graph = PredGraph(TrustMetric(dummy_network, moletrust_generator(horizon = 3, pred_node_trust_threshold = 0.5) )
                       # predict_ratio = 0.5
                       )

# show evaluation measures
print ""
print "abs_error: ",pred_graph.abs_error()
#pred_graph.show_table()
