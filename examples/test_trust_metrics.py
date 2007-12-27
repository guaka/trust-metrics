"""
Create networks, create trust metrics, test trust metrics on these datasets (also restricting to a certain percentage of edges)
"""

# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')

from Dataset.Advogato import *
from Dataset.Dummy import DummyNetwork

# create datasets
dummyNetwork = DummyNetwork()

# create trust metrics
EbayTM = EbayTM()
MT2 = Moletrust(2)

# create the predgraphs based on leave-one-out (also with ratios)
# predict 10% of edges with leave-one-out
pred_graph = PredGrap(dummyNetwork, MT2, 0.1) 

# show evaluation measures
predgraph.showTable()
predgraph.MAE()
