
__doc__ = """Abstraction class for Network dataset."""

import os
import urllib
from networkx import component
from networkx.xdigraph import XDiGraph

class Network(XDiGraph):
    """
    Network dataset, extending networkx.xdigraph.XDiGraph
    see https://networkx.lanl.gov/reference/networkx/networkx.xgraph.XDiGraph-class.html
    """
    
    def __init__(self):
        '''Create directory for class name if needed'''

        XDiGraph.__init__(self)
        self.path = os.path.join(self.dataset_dir(), self.__class__.__name__)
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def dataset_dir(self):
        '''Create datasets/ directory if needed'''
        if os.environ.has_key('HOME'):
            home = os.environ['HOME']
        self.dataset_path = os.path.join(home, 'datasets')
        if not os.path.exists(self.dataset_path):
            os.mkdir(self.dataset_path)
        return self.dataset_path
        
    def download_file(self, url, file):
        '''Download url to filename into the right path '''
        filepath = os.path.join(self.path, file)
        print "Downloading %s to %s " % (url, filepath)
        p = urllib.urlretrieve(url, filepath)

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

