from trustlet import *

A = AdvogatoNetwork( date="2008-05-12" )

tmlist = getTrustMetrics( A )
del tmlist["PageRankTM"]

plist = []

for tm in tmlist:
    plist.append( PredGraph( tmlist[tm] ) )

pointlist = []

for p in plist:
    print get_name(p.TM)
    pointlist.append( p.graphcontroversiality( 0.3 , 0.01, toe="mae", np=2 ) )

prettyplot( pointlist, "/home/ciropom/AllTrustMetric.png", legend=tuple( [tm for tm in tmlist] ) )
