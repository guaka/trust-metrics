

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


def _nx_read_wrap(func):
    """Wrapper around networkx file read functions."""
    def nx_reader(filename):
        G = NX.__getattribute__(func)(filename)
        N = Network.Network()
        N.paste_graph(G)
        return N
    return nx_reader

# there should be a nicer way:

read_adjlist = _nx_read_wrap("read_adjlist")
read_dot = _nx_read_wrap("read_dot")
read_edgelist = _nx_read_wrap("read_edgelist")
read_gml = _nx_read_wrap("read_gml")
read_gpickle = _nx_read_wrap("read_gpickle")
read_graph6 = _nx_read_wrap("read_graph6")
read_graph6_list = _nx_read_wrap("read_graph6_list")
read_graphml = _nx_read_wrap("read_graphml")
read_leda = _nx_read_wrap("read_leda")
read_mulitline_adjlist = _nx_read_wrap("read_multiline_adjlist")
read_sparse6 = _nx_read_wrap("read_sparse6")
read_sparse6_list = _nx_read_wrap("read_sparse6_list")
read_yaml = _nx_read_wrap("read_yaml")

