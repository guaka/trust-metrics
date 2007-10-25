import networkx
from networkx import path, search
import Advogato
import Dataset
from pprint import pprint
# see also 



def build_adv_flow_graph(G):
    """Build a flow graph from a graph, as described in the Advogato
    trust metric paper:

    * add supersink
    * for every node: add node- and node+
    *
    """
    sources = G.advogato_seeds
    
    neg, pos = lambda n: "N_" + str(n), lambda n: "P_" + str(n)

    G_flow = networkx.XDiGraph()
    G_flow.add_node("source")
    G_flow.add_node("supersink")
    for n in G.nodes_iter():
        G_flow.add_node(neg(n))
        G_flow.add_node(pos(n))
        cap_value = 2   # need to use distance to source here!
        if n in sources:
            # it's not clear yet if this is actually what is happening
            # in tmetric.c
            G_flow.add_edge("source", neg(n))
            cap_value = 800
        G_flow.add_edge(neg(n), pos(n), { 'cap': cap_value - 1 })  
        G_flow.add_edge(neg(n), "supersink", { 'cap': 1 })

    for e in G.edges_iter():
        G_flow.add_edge(pos(e[0]), neg(e[1]))

    return G_flow




def ford_fulkerson(G):
    """Ford-Fulkerson, as found in
    http://en.wikipedia.org/wiki/Ford-Fulkerson_algorithm."""
    
    # init: set flow to 0
    for e in G.edges_iter():
        pass #e[2]['flow'] = 0

    dfs_succs = search.dfs_successor(G, 'source')
    node = 'source'

    def good_path_iter(node):
        for succ in dfs_succs[node]:
            if succ == 'supersink':
                yield [node, succ]
            yield [succ]
        



    while queue:
        n = queue.pop(0)
        for succ in n.successors_iter():
            queue.push

        p = path_with_capacity(G, paths_s_to_t)

        min_cap = min_cap_along_path(p)
        for u,v in p:
            f[u][v] = f[u][v] + min_cap
            f[v][u] = f[v][u] - min_cap
          

#G_orig = Advogato.Kaitiaki()
G_orig = Dataset.Dummy()
G_flow = build_adv_flow_graph(G_orig) 


def all_paths(G, start = 'source', end = 'supersink'):
    """Find all paths from start to end.  Here a path is defined as a
    consecutive list of nodes, with edges from one node to the next,
    where all nodes are different.

    There's probably a cleaner way to do it."""

    def _paths(src, init_path = None):
        if not init_path:
            init_path = [src]
        path_list = []
        for e in G.out_edges(src):
            n = e[1]
            if n not in init_path:
                # print "path:", init_path + [n]
                if n == end:
                    # now here I would like to do a yield for the outer function
                    all_paths.append(init_path + [n])  
                path_list += ([init_path + remaining_path + [n]
                               for remaining_path in _paths(n, init_path + [n])])
        # print "ret path_list", path_list
        return path_list
    all_paths = []
    _paths(start)
    return all_paths


p = all_paths(G_flow, 'source', 'supersink')
pprint (p)
#print ford_fulkerson(G_flow)
