"""
Create networks reading data from files, in different formats (dot, pajek, graphml, ...)
"""

# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')

from Dataset import *

#create a undirected unweighted network from a dot file 
UDUW=read_dot("data/undirected_unweighted.dot")
UDUW.info()

#create a undirected unweighted network from a dot file 
ErdosUDUW=read_dot("data/erdos971_undirected_unweighted.dot")
ErdosUDUW.info()

#create a directed weighted network from a dot file 
RagusaDW=read_dot("data/ragusa16_directed_weighted.net")
RagusaDW.info()
