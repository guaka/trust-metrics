
__doc__ = """
Basic and less basic analysis of graphs.
"""

from networkx import *

class graph_properties:
    def __init__(self, G):
        print "graph size:", len(G)
        print "edges:", len(G.edges())
        
        UG = G.to_undirected()
        self.concom_subgraphs = component.connected_component_subgraphs(UG)
        subgraph_size = map(len, self.concom_subgraphs)
        print "size of largest components:", ", ".join(map(str, subgraph_size[:10])), "..."
        print "%nodes in largest component:", 1.0 * subgraph_size[0] / len(G)

        print "density:", density(G)

        print "degree histogram:", degree_histogram(G)[:15]

if __name__ == "__main__":
    from Advogato import Advogato
    advogato = Advogato('t', comp_threshold = 0)
    graph_props = graph_properties(advogato)


