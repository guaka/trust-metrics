
__doc__ = """Abstraction class for Network dataset."""

import os
import urllib
from networkx import component
from networkx.xdigraph import XDiGraph

from numpy import *


def dataset_dir():
    '''Create datasets/ directory if needed'''
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

        XDiGraph.__init__(self)
        if make_base_path:
            self.path = os.path.join(dataset_dir(), self.__class__.__name__)
            if not os.path.exists(self.path):
                os.mkdir(self.path)

    def download_file(self, url, file):
        '''Download url to filename into the right path '''
        filepath = os.path.join(self.path, file)
        print "Downloading %s to %s " % (url, filepath)
        p = urllib.urlretrieve(url, filepath)

    def _read_dot(self, filepath):
        import networkx
        graph = networkx.read_dot(filepath)
        self._paste_graph(graph)
        
    def _paste_graph(self, graph):
        for node in graph.nodes():
            self.add_node(node)
        for edge in graph.edges():
            self.add_edge(edge)


    def ditch_components(self, threshold = 3):
        """Ditch components with less than [threshold] nodes"""
        UG = self.to_undirected()
        if len(UG):
            concom_subgraphs = component.connected_component_subgraphs(UG)[1:]
            n_remove = 0
            for sg in concom_subgraphs:
                if len(sg) <= threshold:
                    for n in sg:
                        n_remove += 1
                        self.delete_node(n)
            print "Thrown out", n_remove, "nodes, fraction: ", 1.0 * n_remove / len(UG)
        else:
            print "Empty graph, no components to ditch"

    def _sorted_edges(self):
        """sorted edges"""
        e = self.edges()
        e.sort()
        return e

    def _edge_array(self, mapper):
        # problem when predtrust == None
        e = self._sorted_edges()
        a = array(map(mapper, e))
        return a

        

