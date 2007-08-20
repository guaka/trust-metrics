#!/usr/bin/env python

import page_rank as NX_future_page_rank
import networkx
import sys

import trustlet.Advogato
a = trustlet.Advogato.Advogato()

print "Starting reading the dataset"

#G=networkx.generators.random_graphs.erdos_renyi_graph(10,0.15)
#G = networkx.read_dot(a.filepath)
G = networkx.read_dot("/home/phauly/datasets/Advogato/graph03.dot")
print "network is of type="+type(G)
G=networkx.DiGraph(G) #cast a XDiGraph into a Graph, maybe this is not needed for pagerank to work, maybe it is needed
#G.ban_multiedges() #pagerank doesn't work on multiedge graphs

print "Finished reading the dataset --> Number of nodes of dataset = %s" % len(G.nodes())

#print G.edges()

print "Do you want to run numpy.linalg.eig? (y/n) [It might be very heavy]"
answer=sys.stdin.readline()[:-1]
if answer == "y":
    import numpy
    M=NX_future_page_rank.google_matrix(G,alpha=0.9)
    e,ev=numpy.linalg.eig(M.T)
    p=numpy.array(ev[:,0]/ev[:,0].sum())[:,0]
    print "exact  ", p

print "Do you want to run page_rank? (y/n) [It might be very heavy]"
answer=sys.stdin.readline()[:-1]
if answer == "y":
    pr = NX_future_page_rank.page_rank(G,alpha=0.9,tol=1.0e-8)
    print "networkx", pr.values()

print "Do you want to run page_rank numpy? (y/n) [It might be very heavy]"
answer=sys.stdin.readline()[:-1]
if answer == "y":
    np=NX_future_page_rank.page_rank_numpy(G,alpha=0.9)
    print "numpy  ", np

print "Do you want to run page_rank scipy? (y/n) [It might be very heavy]"
answer=sys.stdin.readline()[:-1]
if answer == "y":
    ns=NX_future_page_rank.page_rank_scipy(G,alpha=0.9)
    print "scipy  ", ns
