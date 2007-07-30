import networkxfuture.page_rank as page_rank
import numpy

NX = page_rank.NX

#import trustlet.Advogato
#import trustlet.Dummy_dataset
#dataset = trustlet.Advogato.Advogato()
#dataset = trustlet.Dummy_dataset.Dummy_dataset()

# paolo - for me ONLY WORKS WITH PYTHON2.4

#G=NX.DiGraph()
#G=NX.read_dot(dataset.filepath)
#H=G.copy()
#H.ban_multiedges() #pagerank does not work on multiedges graphs
#print H.info()

#print "the value on the edge MUST be a number, in order for to_numpy to work! TODO: convert advogato.dot so that edges values are numbers and not colors!"

#M=page_rank.google_matrix(H,alpha=0.9)
#e,ev=numpy.linalg.eig(M.T)
#p=numpy.array(ev[:,0]/ev[:,0].sum())[:,0]
#print "exact  ", p

#pr=page_rank.page_rank(H,alpha=0.9,tol=1.0e-8)
#print "networkx", pr.values()

#np=my_page_rank.page_rank_numpy(H,alpha=0.9)
#print "numpy  ", np

#ns=my_page_rank.page_rank_scipy(H,alpha=0.9)
#print "scipy  ", ns

G=NX.DiGraph()

edges=[(1,2),(1,3),\
       (3,1),(3,2),(3,5),\
       (4,5),(4,6),\
       (5,4),(5,6),\
       (6,4)]


G.add_edges_from(edges)

M=page_rank.google_matrix(G,alpha=0.9)
e,ev=numpy.linalg.eig(M.T)
p=numpy.array(ev[:,0]/ev[:,0].sum())[:,0]
print "exact  ", p

pr=page_rank.page_rank(G,alpha=0.9,tol=1.0e-8)
print "networkx", pr.values()

np=page_rank.page_rank_numpy(G,alpha=0.9)
print "numpy  ", np

ns=page_rank.page_rank_scipy(G,alpha=0.9)
print "scipy  ", ns
