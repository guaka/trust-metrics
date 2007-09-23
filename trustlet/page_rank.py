#!/usr/bin/env python
#    Copyright (C) 2004-2007 by 
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    Distributed under the terms of the GNU Lesser General Public License
#    http://www.gnu.org/copyleft/lesser.html
#    NetworkX:http://networkx.lanl.gov/. 
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""

import networkx as NX
from networkx.exception import NetworkXError

def page_rank(G,alpha=0.85,max_iter=100,tol=1.0e-4,nstart=None):
    """Return a dictionary keyed by node of the PageRank of G.
    
    PageRank computes the largest eigenvector of the stochastic
    adjacency matrix of G.

    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.   The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    A starting vector for the power iteration can be given in the
    dictionary nstart.

    This is a pure Python implementation.

    """
    if hasattr(G,"multiedges"):
        if G.multiedges==True:
            raise TypeError, \
                "page_rank not valid for graphs with multiedges."

    # create a copy in (right) stochastic form        
    W=stochastic(G)        

    # choose fixed starting vector if not given
    if nstart is None:
        x=dict.fromkeys(W,1.0/W.number_of_nodes())
    else:
        x=nstart
        # normalize starting vector to 1                
        s=1.0/sum(x.values())
        for k in x: x[k]*=s

    nnodes=W.number_of_nodes()
    # "dangling" nodes, no links out from them

    dangle=[n for n in W if sum(W.adj[n])==0.0]  # XGraph internals exposed   
    # pagerank power iteration: make up to max_iter iterations        
    for i in range(max_iter):
        xlast=x
        x=dict.fromkeys(xlast.keys(),0)
        danglesum=alpha/nnodes*sum(xlast[n] for n in dangle)
        teleportsum=(1.0-alpha)/nnodes*sum(xlast.values())
        for n in x:
            # this matrix multiply looks odd because it is
            # doing a left multiply x^T=xlast^T*W
            for nbr in W[n]:
                x[nbr]+=alpha*xlast[n]*W.adj[n][nbr] # XGraph internals exposed
            x[n]+=danglesum+teleportsum
        # normalize vector to 1                
        s=1.0/sum(x.values())
        for n in x: x[n]*=s
        # check convergence, l1 norm            
        err=sum([abs(x[n]-xlast[n]) for n in x])
        if err < n*tol:
            return x

    raise NetworkXError("page_rank: power iteration failed to converge in %d iterations."%(i+1))


def stochastic(G,inplace=False):
    """Return a version of the weighted graph G converted to a (right)
    stochastic representation.  That is, make all of the weights for the
    neighbors of a given node sum to 1.
    
    If inplace=True the conversion is done in place - no copy of the graph is
    made.  This will destroy the original graph G.

    """        
    # this is a hack, better handling to come in networkx-0.36 
    if inplace:
        W=G # copy, better be an XGraph
    else:
        if G.is_directed():
            W=NX.XDiGraph(G) # make a new XDiGraph
        else:
            W=NX.XGraph(G) # make a new XGraph
    for (u,v,d) in W.edges():
        if d is None:
            W.add_edge(u,v,1.0)

    # exposing graph/digraph internals here
    for n in W:
        print "W.adj[n].values():", W.adj[n].values()
        deg=float(sum(W.adj[n].values()))
        for p in W.adj[n]: 
            W.adj[n][p]/=deg
    return W

def google_matrix(G,alpha=0.85,nodelist=None):
    import numpy
    M=NX.to_numpy_matrix(G,nodelist=nodelist)
    (n,m)=M.shape # should be square
    # add constant to dangling nodes' row
    dangling=numpy.where(M.sum(axis=1)==0)
    for d in dangling[0]:
        M[d]=1.0/n
    # normalize        
    M=M/M.sum(axis=1)
    # add "teleportation"
    P=alpha*M+(1-alpha)*numpy.ones((n,n))/n
    return P
    
def page_rank_exact_numpy(G,alpha=0.85,nodelist=None):
    """PageRank using numpy and call to LAPACK eig()."""
    import numpy
    M=google_matrix(G,alpha,nodelist)
    e,ev=numpy.linalg.eig(M.T)
    m=e.argsort()[-1] # index of maximum eigenvalue
    x=numpy.array(ev[:,m])[:,m]
    return x

def page_rank_numpy(G,alpha=0.85,max_iter=100,tol=1.0e-4,nodelist=None):
    """Return a numpy array of the PageRank of G.
    
    PageRank computes the largest eigenvector of the stochastic
    adjacency matrix of G.

    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.   

    A starting vector for the power iteration can be given in the
    dictionary nstart.

    This implementation requires numpy.

    """
    import numpy
    M=google_matrix(G,alpha,nodelist)   
    (n,m)=M.shape # should be square
    x=numpy.ones((n))/n
    for i in range(max_iter):
        xlast=x
        x=numpy.dot(x,M)
        # check convergence, l1 norm            
        err=numpy.abs(x-xlast).sum()
        if err < n*tol:
            return numpy.asarray(x).flatten()

    raise NetworkXError("page_rank: power iteration failed to converge in %d iterations."%(i+1))



def page_rank_scipy(G,alpha=0.85,max_iter=100,tol=1.0e-4,nodelist=None):
    """Return a numpy array of the PageRank of G.
    
    PageRank computes the largest eigenvector of the stochastic
    adjacency matrix of G.

    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.   

    A starting vector for the power iteration can be given in the
    dictionary nstart.

    This implementation requires scipy.

    """
    import scipy.sparse
    M=NX.to_scipy_sparse_matrix(G,nodelist=nodelist)
    (n,m)=M.shape # should be square
    S=scipy.array(M.sum(axis=1)).flatten()
    index=scipy.where(S<>0)[0]
    for i in index:
        M[i,:]*=1.0/S[i]
    x=scipy.ones((n))/n  # initial guess
    dangle=scipy.array(scipy.where(M.sum(axis=1)==0,1.0/n,0)).flatten()
    for i in range(max_iter):
        xlast=x
        x=alpha*(M.rmatvec(x)+scipy.dot(dangle,xlast))+(1-alpha)*xlast.sum()/n
        # check convergence, l1 norm            
        err=scipy.absolute(x-xlast).sum()
        if err < n*tol:
            return x

    raise NetworkXError("page_rank: power iteration failed to converge in %d iterations."%(i+1))


if __name__ == "__main__":

    from networkx import *
    import numpy

    G=DiGraph()

    edges=[(1,2),(1,3),\
           (3,1),(3,2),(3,5),\
           (4,5),(4,6),\
           (5,4),(5,6),\
           (6,4)]
           

    G.add_edges_from(edges)

    M=google_matrix(G,alpha=0.9)
    e,ev=numpy.linalg.eig(M.T)
    p=numpy.array(ev[:,0]/ev[:,0].sum())[:,0]
    print "exact  ", p

    pr=page_rank(G,alpha=0.9,tol=1.0e-8)
    print "networkx", pr.values()

    np=page_rank_numpy(G,alpha=0.9)
    print "numpy  ", np

    ns=page_rank_scipy(G,alpha=0.9)
    print "scipy  ", ns
