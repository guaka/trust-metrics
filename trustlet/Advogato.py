#!/usr/bin/env python

import Dataset
import os

class Advogato(Dataset.Network):
    def __init__(self):
        Dataset.Network.__init__(self)
        self.url = "http://www.advogato.org/person/graph.dot"
        self.file = 'graph.dot'
        self.filepath = os.path.join(self.path, self.file)
        
    def download(self):
        self.download_file(self.url, self.file)

    def load(self):
        import pydot
        if not os.path.exists(self.filepath):
            self.download()
        print "Loading graph.dot..."
        g = pydot.graph_from_dot_file(self.filepath)
    
if __name__ == "__main__":
    adv = Advogato()
    adv.load()
            
