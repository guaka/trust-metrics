"""
Create networks, create trust metrics, test trust metrics on these datasets (also restricting to a certain percentage of edges)
"""

# make sure example can be run from examples/ directory

from trustlet import *


# create datasets
dummy_network = DummyNetwork()

# create trust metrics
# create the predgraphs based on leave-one-out (also with ratios)
# predict 10% of edges with leave-one-out
pred_graph = PredGraph(MoleTrustTM(dummy_network, horizon = 2, threshold = 0.5),
                       # predict_ratio = 0.5
                       )

# show evaluation measures
pred_graph.abs_error()
# pred_graph.show_table()


# create trust metrics
# create the predgraphs based on leave-one-out (also with ratios)
# predict 10% of edges with leave-one-out
pred_graph = PredGraph(MoleTrustTM(dummy_network, horizon = 2, threshold = 0.5),
                       leave_one_out = False,
                       # predict_ratio = 0.5
                       )

# show evaluation measures
pred_graph.abs_error()
# pred_graph.show_table()
