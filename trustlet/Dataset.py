
"""Abstraction class for Network dataset."""

import os
import urllib
from networkx.xdigraph import XDiGraph

#from numpy import *
import numpy

def dataset_dir():
    """Create datasets/ directory if needed."""
    if os.environ.has_key('HOME'):
        home = os.environ['HOME']
    dataset_path = os.path.join(home, 'datasets')
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    return dataset_path
        

class Network(XDiGraph):
    """
    Network dataset, extending networkx.xdigraph.XDiGraph
    see https://networkx.lanl.gov/reference/networkx/networkx.xgraph.XDiGraph-class.html
    """
    
    def __init__(self, make_base_path = True):
        '''Create directory for class name if needed'''

        XDiGraph.__init__(self, multiedges = False)
        if make_base_path:
            self.path = os.path.join(dataset_dir(), self.__class__.__name__)
            if not os.path.exists(self.path):
                os.mkdir(self.path)

    def download_file(self, url, filename):
        '''Download url to filename into the right path '''
        filepath = os.path.join(self.path, filename)
        print "Downloading %s to %s " % (url, filepath)
        retriever = urllib.urlretrieve(url, filepath)
        print retriever

    def _read_dot(self, filepath):
        """Read file."""
        import networkx
        print "Reading", filepath
        graph = networkx.read_dot(filepath)
        self._paste_graph(graph)
        
    def _paste_graph(self, graph):
        """Paste graph."""
        for node in graph.nodes():
            self.add_node(node)
        for edge in graph.edges():
            self.add_edge(edge)


    def ditch_components(self, threshold = 3):
        """Ditch components with less than [threshold] nodes"""
        from networkx.component import connected_component_subgraphs

        undir_graph = self.to_undirected()
        if len(undir_graph):
            concom_subgraphs = connected_component_subgraphs(undir_graph)[1:]
            n_remove = 0
            for subgraph in concom_subgraphs:
                if len(subgraph) <= threshold:
                    for node in subgraph:
                        n_remove += 1
                        self.delete_node(node)
            print "Thrown out", n_remove,
            print "nodes, fraction: ", 1.0 * n_remove / len(undir_graph)
        else:
            print "Empty graph, no components to ditch"

    def _sorted_edges(self):
        """sorted edges"""
        edges = self.edges()
        edges.sort()
        return edges

    def _edge_array(self, mapper = None):
        """numpy array of sorted edges, mapper is an optional function
        that will be applied to the edges"""
        return numpy.array(map(mapper, self._sorted_edges()))


class Dummy(Network):
    """A dummy dataset used for testing purposes, actually the dataset
    with 8 nodes discussed in
    http://www.ams.org/featurecolumn/archive/pagerank.html"""
    def __init__(self):
        Network.__init__(self)
        edges = [(1, 2),
                 (1, 3),
                 (2, 4),
                 (3, 2),
                 (3, 5),
                 (4, 2),
                 (4, 5),
                 (4, 6),
                 (5, 6),
                 (5, 7),
                 (5, 8),
                 (6, 8),
                 (7, 1),
                 (7, 5),
                 (7, 8),
                 (8, 6),
                 (8, 7),
                 ]
        for edge in edges:
            self.add_edge(edge[0], edge[1], 1.0)
        

class Dummy_Weighted(Network):
    """A dummy dataset used for testing purposes, actually the dataset
    with 8 nodes discussed in
    http://www.ams.org/featurecolumn/archive/pagerank.html
    But with weights on edges, so that it is like a trust network"""
    def __init__(self):
        Network.__init__(self)
        edges = [(1, 2, 0.6),
                 (1, 3, 0.6),
                 (2, 4, 0.6),
                 (3, 2, 0.6),
                 (3, 5, 0.6),
                 (4, 2, 0.6),
                 (4, 5, 0.6),
                 (4, 6, 0.6),
                 (5, 6, 0.6),
                 (5, 7, 0.6),
                 (5, 8, 0.6),
                 (6, 8, 0.6),
                 (7, 1, 22.0),
                 (7, 5, 0.6),
                 (7, 8, 0.6),
                 (8, 6, 0.6),
                 (8, 7, 0.6),
                 ]
        for edge in edges:
            self.add_edge(edge)    
        
