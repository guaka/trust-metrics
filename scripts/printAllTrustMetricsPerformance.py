from trustlet import *

A = AdvogatoNetwork( date="2008-05-12" )

tmlist = getTrustMetrics( A )
del tmlist["PageRankTM"]

plist = []

for tm in tmlist:
    plist.append( PredGraph( tmlist[tm] ) )

pointlist = []

for p in plist:
    pointlist.append( ( get_name(p.TM) , p.graphcontroversiality( 0.3 , 0.01, toe="mae", np=2 ) ) )

for p in pointlist:
    for q in pointlist:
        if q[0] <= p[0]:
            continue
        else:
            print q[0]+"_vs_"+p[0]
            prettyplot( [q[1],p[1]], 
                        "/home/ciropom/graphs/"+q[0]+"_vs_"+p[0]+".png", 
                        legend=(q[0],p[0]), 
                        showlines=True )
