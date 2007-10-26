import networkx
from networkx import path, search
import Advogato
import Dataset
import random
from pprint import pprint
# see also something else


cap_dict = { 0: 800,
             1: 200,
             2: 50,
             3: 12,
             4: 4,
             5: 2 }


def build_adv_flow_graph(G, seeds):
    """Build a flow graph from a graph, as described in the Advogato
    trust metric paper:

    * add supersink
    * for every node: add N_node and P_node
    * set initial flow to 0
    """
    # This also ensures that there are no nodes named "source" or "supersink"
    neg, pos = lambda n: "N" + str(n), lambda n: "P" + str(n)

    G_flow = networkx.XDiGraph()
    G_flow.add_node("source")
    G_flow.add_node("supersink")

    for src in seeds:
        if not src in G:
            seeds.remove(src)

    distance_map = {}
    for src in seeds:
        # build the distance map, we don't want to add a new source node to G,
        # so we have to get a temp_dist_map for every seed node
        temp_dist_map = path.single_source_shortest_path_length(G, src)
        for n,d in temp_dist_map.items():
            if distance_map.has_key(n):
                distance_map[n] = min(distance_map[n], d)
            else:
                distance_map[n] = d

    for n in G.nodes_iter():
        cap_value = 1
        if distance_map.has_key(n):
            dist = distance_map[n]
            if dist <= 5:
                cap_value = cap_dict[dist]
        if n in seeds:
            # it's not clear yet if this is actually what is happening
            # in tmetric.c
            G_flow.add_edge("source", neg(n), {'flow': 0})
            assert cap_value == 800
        G_flow.add_edge(neg(n), pos(n), {'cap': cap_value - 1, 'flow': 0})
        G_flow.add_edge(neg(n), "supersink", {'cap': 1, 'flow': 0})
    for e in G.edges_iter():
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
                # print p
                _paths(v, p)

    all_paths = []
    _paths(start)
    return all_paths


def all_paths_iter(G, src = 'source', end = 'supersink', init_path = None):
    """Find all paths from start to end.  Here a path is defined as a
    consecutive list of nodes, with edges from one node to the next,
    where all nodes are different.
    """

    init_path = init_path or [src]
    for u,v,x in G.out_edges_iter(src):
        if v not in init_path:
            p = init_path + [v]
            if v == end:
                yield p
            else:
                for r in all_paths_iter(G, v, end, p):
                    yield r
                

def all_paths_iter_cap(G, src = 'source', end = 'supersink', init_path = None):
    """Find all paths from start to end.  Here a path is defined as a
    consecutive list of nodes, with edges from one node to the next,
    where all nodes are different.
    
    This tries to eliminate paths with cap <= flow.
    """
    def path_has_cap(p):
        if len(p) < 2:
            return True
        cap_flow = [x['cap'] > x['flow']
                    for x in [G.get_edge(u,v)
                              for u,v in zip(p[:-1], p[1:])
                              ]
                    if x.has_key('cap')]
        print cap_flow
        return (not cap_flow or cap_flow[-1]
                and cap_flow[1:] == cap_flow[:-1])

    def has_cap(u, v):
        e = G.get_edge(u, v)
        return not e.has_key('cap') or e['cap'] > e['flow']

    init_path = init_path or [src]
    for u,v,x in G.out_edges_iter(src):
        if v not in init_path:
            if has_cap(u, v): # and path_has_cap(init_path + [v]):
                if v == end:
                    yield init_path + [v]
                else:
                    for r in all_paths_iter_cap(G, v, end, init_path + [v]):
                        yield r
            #else:
            #    print "SKIP", init_path
            
        


def ford_fulkerson(G, source = 'source', sink = 'supersink'):
    """Ford-Fulkerson, (more or less) as found in
    http://en.wikipedia.org/wiki/Ford-Fulkerson_algorithm."""

    path_edges = lambda p: zip(p[:-1], p[1:])
    def change_flow(u, v, df):
        """Change flow on edge."""
        x = dict(G.get_edge(u, v) or {})
        x['flow'] += df
        G.add_edge(u, v, x)

    for p in all_paths_iter_cap(G, 'source', 'supersink'):
        # print p

        cap_flow = [c for c in
                    filter(lambda x: x and x.has_key('cap'),
                           [G.get_edge(u, v) for u,v in path_edges(p)])]
    
        min_cap = min([c['cap'] - c['flow'] for c in cap_flow])
        if min_cap > 0:
            # print min_cap, p
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


def adv_trust_metric(G):
    G_lvl = networkx.DiGraph()
    node_levels = {}
    levels = G.level_map.items()
    levels.sort(lambda x,y: cmp(y[1], x[1]))
    for attr,lvl in levels:
        for e in G.edges_iter():
            if e[2].values()[0] == attr:
                ###########################3
                #if random.random() < 0.6:
                G_lvl.add_edge((e[0], e[1]))
                ###########################33
        print "len G_lvl:", len(G_lvl)
        G_flow = build_adv_flow_graph(G_lvl, G.advogato_seeds)
        ff = ford_fulkerson(G_flow)
        # break
        for n in nodes_with_flow(G_flow):
            if not node_levels.has_key(n):
                node_levels[n] = attr
    return node_levels


D = Dataset.Dummy()
K = Advogato.Kaitiaki()
S = Advogato.SqueakFoundation()

a = adv_trust_metric(K)
print a

#S = Advogato.SqueakFoundation()
#Sf = build_adv_flow_graph(S, lambda e: e[2]['level'] == 'Master')



