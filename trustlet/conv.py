

import netconv
import networkx as NX
from Dataset import Network

def read_pajek(filename):
    """Read pajek files into a WeightedNetwork."""
    
    n = netconv.Network()
    netconv.importPajek(n, filename)
    
    #G = NX.Graph()
    #netconv.netconv2NX(n, G)

    G = Network.Network()
    netconv.netconv2NX(n, G)

    return G


def read_dot(filename):
    """Read dot."""

    G = NX.read_dot(filename)
    N = Network.Network()
    N.paste_graph(G)
    return N


def read_graphml(filename):
    """Read graphML."""

    G = NX.read_graphml(filename)
    N = Network.Network()
    N.paste_graph(G)
    return N
    
