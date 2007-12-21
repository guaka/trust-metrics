
# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')


import Dataset.Network 
import networkx

import igraph

def read_GraphML(filename):
    iG = igraph.Graph.Read_GraphML(filename)
    return iG

def convert_from_igraph(iG):
    if iG.is_directed():
        G = networkx.xdigraph.XDiGraph()
    else:
        G = networkx.xdigraph.XGraph()

    G = XDiGraph()
    for v in iG.vs:
        G.add_node(v['id'])
    for e in iG.get_edgelist():
        G.add_edge(e[0], e[1])
    return G
        

iG = read_GraphML('simple-graphml.xml')
print iG
