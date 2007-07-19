#!/usr/bin/env python

import Dataset

class Advogato(Dataset.Network):
    def load_network(self):
        self.download("http://www.advogato.org/person/graph.dot", 'graph.dot')
        

if __name__ == "__main__":
    adv = Advogato()
    adv.load_network()
            
