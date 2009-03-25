
"""
Some very simple networks for testing.

"""

from Network import Network, WeightedNetwork
import os

_dummy_map = {
    'Observer': 0.4,
    'Apprentice': 0.6,
    'Journeyer': 0.8,
    'Master': 1.0,
    '' : 0.0
    }


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

        self.filepath = os.path.join(os.environ['HOME'],'datasets','DummyNetwork')
        self.date = '1970-01-01'
        
        edges = [(1, 2, "Master"),
                 (1, 3, "Journeyer"),
                 (2, 4, "Apprentice"),
                 (3, 2, "Observer"),
                 (3, 5, "Observer"),
                 (4, 2, "Apprentice"),
                 (4, 5, "Master"),
                 (4, 6, "Observer"),
                 (5, 6, "Apprentice"),
                 (5, 7, "Journeyer"),
                 (5, 8, "Journeyer"),
                 (6, 8, "Journeyer"),
                 (7, 1, "Apprentice"),
                 (7, 5, "Observer"),
                 (7, 8, "Master"),
                 (8, 6, "Apprentice"),
                 (8, 7, "Journeyer"),
                 ]
        for edge in edges:
            self.add_edge(edge[0], edge[1], {'level':edge[2]})    

        self.level_map = _dummy_map
        

if __name__ == "__main__":
    dwn = DummyWeightedNetwork()
    print dwn.weights()
