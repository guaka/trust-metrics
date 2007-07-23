import networkxfuture.page_rank
from networkx import *
from numpy import *
# import numpy 

import trustlet.Advogato
a = trustlet.Advogato.Advogato()

G=DiGraph()

if 0==1:
    edges=[(1,2),(1,3),\
           (3,1),(3,2),(3,5),\
           (4,5),(4,6),\
           (5,4),(5,6),\
           (6,4)]    
    G.add_edges_from(edges)
else:
    G=read_dot(a.filepath) # better use advogato object

print "--> Numero nodi=%s" % len(G.nodes())

#M=my_page_rank.google_matrix(G,alpha=0.9)
#e,ev=numpy.linalg.eig(M.T)
#p=numpy.array(ev[:,0]/ev[:,0].sum())[:,0]
#print "exact  ", p

pr=networkxfuture.page_rank.page_rank(G,alpha=0.9,tol=1.0e-8)
print "networkx", pr.values()

#np=my_page_rank.page_rank_numpy(G,alpha=0.9)
#print "numpy  ", np

#ns=my_page_rank.page_rank_scipy(G,alpha=0.9)
#print "scipy  ", ns
