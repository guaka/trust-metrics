
from networkx import *
from Dataset import Advogato
import page_rank
import numpy

from pprint import pprint

# http://localhost/src/networkx/reference/public/networkx.generators.classic-module.html


def exactPR(G):
    M = page_rank.google_matrix(G, alpha=0.9)
    e, ev = numpy.linalg.eig(M.T)
    p = numpy.array(ev[:,0] / ev[:,0].sum())[:,0]
    return p

def NXPR(G):
    pr = page_rank.page_rank(G,alpha=0.9,tol=1.0e-8)
    return pr.values()

def numpyPR(G):
    np = page_rank.page_rank_numpy(G,alpha=0.9)
    return np

def scipyPR(G):
    try:
        ns = page_rank.page_rank_scipy(G,alpha=0.9)
        return ns
    except "bad scipy":
        print "scipy not working"



def randomgraph():
    G = XDiGraph()
    edges = [(1,2), (1,3),
             (3,1), (3,2), (3,5),
             (4,5), (4,6),
             (5,4), (5,6),
             (6,4)]
    G.add_edges_from(edges)
    return G


"""
TODO: local pagerank!
"""


def value_on_edges(G):
    """Convert the graph: edges will have trust value, not a dict containing it."""
    H = XDiGraph()
    for e in G.edges():
        H.add_edge(e[0], e[1], G.trust_on_edge(e))
    return H

class BasicPageRank:
    """Basic PageRank class."""
    def __init__(self, H):
        self.G = value_on_edges(H) #get a graph with, on edges, only the trust values and not the dict so we can pass it to functions that compute pagerank
        self.pr = numpyPR(self.G)
        self.nodes = self.G.nodes()

    def __getitem__(self, node):
        """Now you can do

        >>> PR = OurPageRank(G)
        >>> for n in G.nodes()
        >>>     PR[n]
        """
        return self.pr[self.nodes.index(node)]


def pagerank_tm(G, node):
    pr = BasicPageRank(G)
    return pr[node]


if __name__ == "__main__":
    import TrustMetric, PredGraph
    from Dataset import Advogato
    G = Advogato.KaitiakiNetwork()
    PR = BasicPageRank(G)
    for n in G.nodes():
        print PR[n]
    pg = PredGraph.PredGraph(G, TrustMetric.PageRankTM0, True)
    
