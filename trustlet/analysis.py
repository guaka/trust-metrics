
__doc__ = """
Basic and less basic analysis of graphs.
"""

from networkx import *

class graph_properties:
    def __init__(self, G):
        print "graph size:", len(G)
        print "edges:", len(G.edges())

        # paolo - 20070919 - computing also the strongly connected components directly on the directed graph. Changing a directed graph into an undirected usually destroys a lot of its structure and meaning. Let see.
        # while in the published API there is a method strongly_connected_component_subgraphs(G), I don't have it on my machine (probably I have an older networkx version), so for now I commented the following code.
        # the method strongly_connected_component_subgraphs(G) was added on 07/21/07. See https://networkx.lanl.gov/changeset/640 . On my machine I have "python-networkx/feisty uptodate 0.32-2" while on networkx svn there is already version 0.35.1      
        #self.strongconcom_subgraphs = component.strongly_connected_component_subgraphs(G)
        #strongconcom_subgraph_size = map(len, self.strongconcom_subgraphs)        
        #print "size of largest strongly connected components:", ", ".join(map(str, strongconcom_subgraph_size[:10])), "..."
        #print "%nodes in largest strongly connected component:", 1.0 * strongconcom_subgraph_size[0] / len(G)
        
        UG = G.to_undirected()
        self.concom_subgraphs = component.connected_component_subgraphs(UG)
        concom_subgraph_size = map(len, self.concom_subgraphs)
        print "size of largest connected components:", ", ".join(map(str, concom_subgraph_size[:10])), "..."
        print "%nodes in largest connected component:", 1.0 * concom_subgraph_size[0] / len(G)

        #only work on connected graphs, maybe we could run it on the largest strongly connected component.
        #print "diameter:", distance.diameter(G)
        #print "radius:", distance.radius(G)

        print "density:", density(G)

        print "degree histogram:", degree_histogram(G)[:15]

        print "average_clustering:", cluster.average_clustering(G)

        print "transitivity:", cluster.transitivity(G)

        #not yet in my networkx revision
        #print "number_of_cliques", cliques.number_of_cliques(G)

        #this return a dict with the betweenness centrality of every node, maybe we want to compute the average betweenness centrality but before it is important to understand which measures usually are usually reported in papers as peculiar for capturing the characteristics and structure of a directed graph.
        #print "betweenness_centrality:", centrality.betweenness_centrality(G)

def analyze(G):
    graph_props = graph_properties(G)

if __name__ == "__main__":
    from Advogato import Advogato
    advogato = Advogato('t', comp_threshold = 0)
    graph_props = graph_properties(advogato)


