
from Network import Network

class DummyNetwork(Network):
    """A dummy dataset used for testing purposes, actually the dataset
    with 8 nodes discussed in
    http://www.ams.org/featurecolumn/archive/pagerank.html"""

    advogato_seeds = [1]
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
        

class DummyWeightedNetwork(Network):
    """A dummy dataset used for testing purposes, actually the dataset
    with 8 nodes discussed in
    http://www.ams.org/featurecolumn/archive/pagerank.html
    But with weights on edges, so that it is like a trust network"""
    def __init__(self):
        Dataset.Network.__init__(self)
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
        
