#!/usr/bin/env python

"""
Testing PageRank on a random graph.


Output is supposed to be something like:

exact   [ 0.03721197  0.05395735  0.04150565  0.37508082  0.20599833  0.28624589]
networkx [0.037211973379326385, 0.053957363787491913, 0.04150566302577844, 0.37508079842876135, 0.20599832787380884, 0.28624587350483305]
numpy   [ 0.03731123  0.0541298   0.04162124  0.37487935  0.20595249  0.2861059 ]
scipy   [ 0.03731123  0.0541298   0.04162124  0.37487935  0.20595249  0.2861059 ]

We could (should) use this for a test framework.

"""


import page_rank
import numpy

NX = page_rank.NX

#import trustlet.Advogato
#import trustlet.Dummy_dataset
#dataset = trustlet.Advogato.Advogato()
#dataset = trustlet.Dummy_dataset.Dummy_dataset()

# paolo - for me ONLY WORKS WITH PYTHON2.4


def test():
    G = NX.DiGraph()
    edges = [(1,2), (1,3),
             (3,1), (3,2), (3,5),
             (4,5), (4,6),
             (5,4), (5,6),
             (6,4)]
    G.add_edges_from(edges)

    M = page_rank.google_matrix(G, alpha=0.9)
    e, ev = numpy.linalg.eig(M.T)
    p = numpy.array(ev[:,0] / ev[:,0].sum())[:,0]
    print "exact  ", p

    pr = page_rank.page_rank(G,alpha=0.9,tol=1.0e-8)
    print "networkx", pr.values()

    np = page_rank.page_rank_numpy(G,alpha=0.9)
    print "numpy  ", np

    try:
        ns = page_rank.page_rank_scipy(G,alpha=0.9)
        print "scipy  ", ns
    except Error:
        print "scipy not working"


if __name__ == '__main__':
    test()


"""
#
# You can also comment huge chunks by making them into a string!  But
# it's probably nicer to put stuff in a function that you don't use.

G=NX.DiGraph()
G=NX.read_dot(dataset.filepath)
H=G.copy()
H.ban_multiedges() #pagerank does not work on multiedges graphs
print H.info()

print "the value on the edge MUST be a number, in order for to_numpy to work! TODO: convert advogato.dot so that edges values are numbers and not colors!"

M=page_rank.google_matrix(H,alpha=0.9)
e,ev=numpy.linalg.eig(M.T)
p=numpy.array(ev[:,0]/ev[:,0].sum())[:,0]
print "exact  ", p

pr=page_rank.page_rank(H,alpha=0.9,tol=1.0e-8)
print "networkx", pr.values()

np=my_page_rank.page_rank_numpy(H,alpha=0.9)
print "numpy  ", np

ns=my_page_rank.page_rank_scipy(H,alpha=0.9)
print "scipy  ", ns
"""
