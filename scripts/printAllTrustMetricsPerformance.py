"""
This script calculate the graphics in gnuplot that compares pair of network.
If there aren't parameters, it take all the trust metric, elsewhere you can
specify on command line space-separated name of trustmetric to leave out.
"""


from trustlet import *


def compareAllTrustMetrics( leaveOut = [], 
                            cond=None,date = "2008-05-12", allInOne=True, 
                            path = "/home/ciropom/graphs", toe = "mae", np=1,
                            x_range=(0.0,0.5),
                            y_range=None ):
    
    A = AdvogatoNetwork( date=date )

    tmlist = getTrustMetrics( A )
    
    for l in leaveOut:
        try:
            del tmlist[l]
        except KeyError:
            print "KeyError! ",l," not deleted"
    plist = []
    
    for tm in tmlist:
        plist.append( PredGraph( tmlist[tm] ) )

    pointlist = []

    for p in plist:
        pointlist.append( ( get_name(p.TM) , p.graphcontroversiality( 0.3 , 0.01, toe=toe, np=np, cond=cond )) )

    if allInOne:
        prettyplot( [x for (y,x) in pointlist], 
                    os.path.join( path, toe+"All.png" ),
                    legend=tuple([y for (y,x) in pointlist]),
                    showlines=True,
                    x_range=x_range,
                    y_range=y_range,
                    title='All trust metric for '+toe+' error',
                    xlabel='controversiality',
                    ylabel=toe)

    else:
        for p in pointlist:
            for q in pointlist:
                if q[0] <= p[0]:
                    continue
                else:
                    print q[0]+"_vs_"+p[0]
                    prettyplot( [q[1],p[1]], 
                                os.path.join( path, q[0]+"_vs_"+p[0]+".png" ), 
                                legend=(q[0],p[0]), 
                                showlines=True,
                                x_range=x_range,
                                y_range=y_range,
                                xlabel='controversiality',
                                ylabel=toe )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        
        nleaveOut = len(sys.argv) - 1
        leaveOut = []
        for i in xrange(1,nleaveOut):
            leaveOut.append( sys.argv[i] )

        compareAllTrustMetrics( leaveOut )
    
    else:
    
        compareAllTrustMetrics()
