
"""Abstraction class for Network."""

import os
import urllib
from networkx.xdigraph import XDiGraph

class Network(XDiGraph):
    """
    This should probably extend NetworkX.XGraph

    see https://networkx.lanl.gov/reference/networkx/networkx.xgraph.XGraph-class.html
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
