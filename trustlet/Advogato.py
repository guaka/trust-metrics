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
        self.download(self.url, self.file)

    def load(self):
        import pydot
        g = pydot.graph_from_dot_file(os.path.join(self.path, self.file))
    


if __name__ == "__main__":
    adv = Advogato()
    adv.load()
            
