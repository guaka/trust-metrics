
"""
Some very simple networks for testing.

"""

from Network import Network, WeightedNetwork

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
        

class DummyWeightedNetwork(WeightedNetwork):
    """A dummy dataset used for testing purposes, actually the dataset
    with 8 nodes discussed in
    http://www.ams.org/featurecolumn/archive/pagerank.html
    But with weights on edges, so that it is like a trust network"""
    def __init__(self):
        WeightedNetwork.__init__(self)
        edges = [(1, 2, 0.1),
                 (1, 3, 0.6),
                 (2, 4, 0.8),
                 (3, 2, 0.9),
                 (3, 5, 0.7),
                 (4, 2, 0.6),
                 (4, 5, 0.4),
                 (4, 6, 0.3),
                 (5, 6, 0.6),
                 (5, 7, 0.2),
                 (5, 8, 0.6),
                 (6, 8, 0.1),
                 (7, 1, 1.0),
                 (7, 5, 0.1),
                 (7, 8, 0.1),
                 (8, 6, 0.2),
                 (8, 7, 0.8),
                 ]
        for edge in edges:
            self.add_edge(edge)    
        

if __name__ == "__main__":
    dwn = DummyWeightedNetwork()
    print dwn.weights()
