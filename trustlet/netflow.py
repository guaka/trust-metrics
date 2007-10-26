import networkx
from networkx import path, search
import Advogato
import Dataset
from pprint import pprint
# see also 


class AdvFlowGraph:
    """To make it easier to reinit, and to reuse."""
    pass


def build_adv_flow_graph(G, cond = None):
    """Build a flow graph from a graph, as described in the Advogato
    trust metric paper:

    * add supersink
    * for every node: add N_node and P_node
    * set initial flow to 0
    """
    sources = G.advogato_seeds

    # This also ensures that there are no nodes named "source" or "supersink"
    neg, pos = lambda n: "N" + str(n), lambda n: "P" + str(n)

    G_flow = networkx.XDiGraph()
    G_flow.add_node("source")
    G_flow.add_node("supersink")
    for n in G.nodes_iter():
        G_flow.add_node(neg(n))
        G_flow.add_node(pos(n))
        cap_value = 2   # need to use distance to source here!
        for s in sources:
            for s2 in G[s]:
                if s2 == n:
                    cap_value = 200
                else:
                    for s3 in G[s2]:
                        if s3 == n:
                            cap_value = 50
                        else:
                            cap_value = 10
        if n in sources:
            # it's not clear yet if this is actually what is happening
            # in tmetric.c
            G_flow.add_edge("source", neg(n), {'flow': 0})
            cap_value = 800
        G_flow.add_edge(neg(n), pos(n), {'cap': cap_value - 1, 'flow': 0})
        G_flow.add_edge(neg(n), "supersink", {'cap': 1, 'flow': 0})
    for e in G.edges_iter():
        if not cond or cond(e):
            G_flow.add_edge(pos(e[0]), neg(e[1]), {'flow': 0})

    return G_flow


def all_paths(G, start = 'source', end = 'supersink'):
    """Find all paths from start to end.  Here a path is defined as a
    consecutive list of nodes, with edges from one node to the next,
    where all nodes are different.

    There _is_ a better way to do it."""

    def _paths(src, init_path = None):
        init_path = init_path or [src]
        for u,v,x in G.out_edges_iter(src):
            if v not in init_path:
                p = init_path + [v]
                if v == end:
                    # now here I would like to do a yield for the outer function
                    #print p
                    all_paths.append(p)
                print p
                _paths(v, p)

    all_paths = []
    _paths(start)
    return all_paths


def all_paths_iter(G, src = 'source', end = 'supersink', init_path = None):
    """Find all paths from start to end.  Here a path is defined as a
    consecutive list of nodes, with edges from one node to the next,
    where all nodes are different.

    There _is_ a better way to do it.

    Damn, recursive generator doesn't work!
    """

    print "called with:", src, end, init_path

    init_path = init_path or [src]
    for u,v,x in G.out_edges_iter(src):
        if v not in init_path:
            p = init_path + [v]
            print p
            if v == end:
                # now here I would like to do a yield for the outer function
                #print p
                yield p
            else:
                print 'call again with',
                print v, end, p
                all_paths_iter(G, v, end, p)
        else:
            print "httht"



def ford_fulkerson(G, source = 'source', sink = 'supersink'):
    """Ford-Fulkerson, (more or less) as found in
    http://en.wikipedia.org/wiki/Ford-Fulkerson_algorithm."""

    path_edges = lambda p: zip(p[:-1], p[1:])
    def change_flow(u, v, df):
        """Change flow on edge."""
        x = dict(G.get_edge(u, v) or {})
        x['flow'] += df
        G.add_edge(u, v, x)

    for p in all_paths(G, 'source', 'supersink'):
        print p
        cap_flow = [c for c in
                    filter(lambda x: x and x.has_key('cap'),
                           [G.get_edge(u, v) for u,v in path_edges(p)])]
        print cap_flow
    
        min_cap = min([c['cap'] - c['flow'] for c in cap_flow])
        if min_cap > 0:
            for u, v in path_edges(p):
                change_flow(u, v, min_cap)
                if G.has_edge(v, u):
                    change_flow(v, u, -min_cap)
                    
def nodes_with_flow(G):
    return map(lambda x: x[0][1:],
               filter(lambda x:
                      x[2].has_key('cap') and
                      x[2]['flow'] and
                      x[1] != 'supersink',
                      G.edges_iter()))


K = Advogato.Kaitiaki()
Kf = build_adv_flow_graph(K) 

#S = Advogato.SqueakFoundation()
#Sf = build_adv_flow_graph(S, lambda e: e[2]['level'] == 'Master')

print [p for p in all_paths_iter(Kf)]

if False:
    ford_fulkerson(Kf)

