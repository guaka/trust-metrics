#!/usr/bin/env python

import networkxfuture.page_rank as NX_future_page_rank
import networkx

# import numpy  # currently not used 

import trustlet.Advogato
a = trustlet.Advogato.Advogato()

G = networkx.DiGraph()

if False:
    edges=[(1,2),(1,3),\
           (3,1),(3,2),(3,5),\
           (4,5),(4,6),\
           (5,4),(5,6),\
           (6,4)]    
    G.add_edges_from(edges)
else:
    G = networkx.read_dot(a.filepath)

print "--> Numero nodi=%s" % len(G.nodes())

#M=my_page_rank.google_matrix(G,alpha=0.9)
#e,ev=numpy.linalg.eig(M.T)
#p=numpy.array(ev[:,0]/ev[:,0].sum())[:,0]
#print "exact  ", p

pr = NX_future_page_rank.page_rank(G,alpha=0.9,tol=1.0e-8)
print "networkx", pr.values()

#np=my_page_rank.page_rank_numpy(G,alpha=0.9)
#print "numpy  ", np

#ns=my_page_rank.page_rank_scipy(G,alpha=0.9)
#print "scipy  ", ns
