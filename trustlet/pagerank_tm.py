
from networkx.spectrum import *
from networkx.xdigraph import XDiGraph

# http://localhost/src/networkx/reference/public/networkx.generators.classic-module.html

def pagerank_tm(G, a, b):
    H = XDiGraph()
    nodes = G.nodes()
    for n in nodes:
        H.add_node(n)
    for e in G.edges():
        H.add_edge(e[0], e[1], G.level_map[e[2]['level']])
    adj_spec = adjacency_spectrum(H)
    return adj_spec[nodes.index(b)]

