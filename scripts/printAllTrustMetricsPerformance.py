"""
This script calculate the graphics in gnuplot that compares pair of network.
If there aren't parameters, it take all the trust metric, elsewhere you can
specify on command line space-separated name of trustmetric to leave out.
"""


from trustlet import *


def compareAllTrustMetrics( leaveOut, cond=None ):
    
    A = AdvogatoNetwork( date="2008-05-12" )

    tmlist = getTrustMetrics( A )
    
    for l in leaveOut:
        del tmlist[l]

    plist = []
    
    for tm in tmlist:
        plist.append( PredGraph( tmlist[tm] ) )

    pointlist = []

    for p in plist:
        pointlist.append( ( get_name(p.TM) , p.graphcontroversiality( 0.3 , 0.01, toe="mae", np=2, cond=cond ) ) )

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


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        
        nleaveOut = len(sys.argv) - 1
        leaveOut = []
        for i in xrange(1,nleaveOut):
            leaveOut.append( sys.argv[i] )

        compareAllTrustMetrics( leaveOut )
    
    else:
    
        compareAllTrustMetrics( [] )
