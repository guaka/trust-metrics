
"""
Basic and less basic analysis of graphs.
"""

import networkx
from networkx import component, cluster, path, cliques, centrality

class GraphProperties:
    """Graph properties."""
    def __init__(self, graph, slow_stuff = False):
        graph.info()

        # paolo - 20070919 - computing also the strongly connected
        # components directly on the directed graph. Changing a
        # directed graph into an undirected usually destroys a lot of
        # its structure and meaning. Let see.  while in the published
        # API there is a method
        # strongly_connected_component_subgraphs(graph), I don't have it
        # on my machine (probably I have an older networkx version),
        # so for now I commented the following code.  the method
        # strongly_connected_component_subgraphs(graph) was added on
        # 07/21/07. See https://networkx.lanl.gov/changeset/640 . On
        # my machine I have "python-networkx/feisty uptodate 0.32-2"
        # while on networkx svn there is already version 0.35.1

        if False:
            self.strongconcom_subgraphs = component.strongly_connected_component_subgraphs(graph)
            strongconcom_subgraph_size = map(len, self.strongconcom_subgraphs)     

            print "size of largest strongly connected components:",
            print ", ".join(map(str, strongconcom_subgraph_size[:10])), "..."
            print "%nodes in largest strongly connected component:",
            print 1.0 * strongconcom_subgraph_size[0] / len(graph)
        
        undir_graph = graph.to_undirected()
        self.concom_subgraphs = component.connected_component_subgraphs(undir_graph)
        concom_subgraph_size = map(len, self.concom_subgraphs)
        print "size of largest connected components:",
        print ", ".join(map(str, concom_subgraph_size[:10])), "..."
        
        print "%nodes in largest connected component:",
        print 1.0 * concom_subgraph_size[0] / len(graph)

        #only work on connected graphs, maybe we could run it on the
        #largest strongly connected component.

        #print "diameter:", distance.diameter(G)
        #print "radius:", distance.radius(graph)

        print "density:", networkx.density(graph)

        print "degree histogram:", networkx.degree_histogram(graph)[:15]

        print "average_clustering:", cluster.average_clustering(graph)

        print "transitivity:", cluster.transitivity(graph)

        if slow_stuff:
            #not yet in my networkx revision  -- try try except
            print "number_of_cliques", cliques.number_of_cliques(graph)

            """this returns a dict with the betweenness centrality of
            every node, maybe we want to compute the average
            betweenness centrality but before it is important to
            understand which measures usually are usually reported in
            papers as peculiar for capturing the characteristics and
            structure of a directed graph."""
            print "betweenness_centrality:",
            print centrality.betweenness_centrality(graph)

def analyze(graph):
    """Analyze graph."""
    return GraphProperties(graph)


def mean_shortest_path_length(graph):
    """Calculate mean shortest path lenght of graph."""
    apspl = path.all_pairs_shortest_path_length(graph)
    sum_of_paths = sum([sum(apspl[n].values()) for n in apspl])
    num_of_paths = sum(map(len, apspl.values()))
    return float(sum_of_paths) / num_of_paths


def reciprocity(graph):
    """Calculate reciprocity of graph, i.e. the ratio of the edges in
    one direction that have and edge going in the other direction."""
    return sum([graph.has_edge(e[1], e[0]) 
                for e in graph.edges_iter()]) / float(graph.number_of_edges())


def _trust_val(graph, a, b):
    """First attempt towards weighted reciprocity."""
    return graph.level_map[graph.get_edge(a, b).values()[0]]
    

#def reciprocity_diff(graph):
#    return 
    

if __name__ == "__main__":
    from Advogato import Advogato, SqueakFoundation
    test_graph = SqueakFoundation()
    graph_props = GraphProperties(test_graph)


