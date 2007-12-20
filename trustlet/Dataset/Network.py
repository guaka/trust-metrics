import urllib
import os
from networkx.xdigraph import XDiGraph
from networkx import cluster

import numpy
import scipy

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

    def info(self):
        XDiGraph.info(self)
        print "Std deviation of in-degree:", scipy.std(([len(self.in_edges(n)) for n in self.nodes()]))
        print "Std deviation of out-degree:", scipy.std(([len(self.out_edges(n)) for n in self.nodes()]))
        print "Average clustering coefficient:", cluster.average_clustering(self)
        # todo: power-law exponent

    def in_degree_hist(self):
        """in-degree histogram, minor adaptation from networkx.function.degree_histogram"""
        degseq=self.in_degree()
        dmax=max(degseq)+1
        freq= [ 0 for d in xrange(dmax) ]
        for d in degseq:
            freq[d] += 1
        return freq

    def out_degree_hist(self):
        """out-degree histogram, minor adaptation from networkx.function.degree_histogram"""
        degseq=self.out_degree()
        dmax=max(degseq)+1
        freq= [ 0 for d in xrange(dmax) ]
        for d in degseq:
            freq[d] += 1
        return freq


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


