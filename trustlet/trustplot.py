from trustlet import *


def plotOverToe(toe, tmlist):
    """
    This function plot a gnuplot graph, for more than one trustmetric
    over the same toe.
    Parameters:
       toe = single string with type of error ('mae','rmse','coverage','percentage_wrong')
       tmlist = list of trustmetric to plot
    """

    tp = ('mae','rmse','coverage','percentage_wrong')
    
    pg = []
    for tm in tmlist:
        pg.append( PredGraph( tm ) )

    c = []
    for p in pg:
        c.append(p.graphcontroversiality( 0.3,0.01,toe=toe ))

    legend = [get_name(x) for x in tmlist]

    prettyplot( c, 'TrustMetricsOverToe.png' ,legend = tuple(legend), showlines=True)
    
    return

def plotOverNet(tm, toelist):
    """
    This function plot more type of error over a single net
    Parameters:
       tm = a single trustmetric
       toelist = a list of type of error ('mae','rmse','coverage','percentage_wrong')
    """
    p = PredGraph( tm )

    c = p.graphcontroversiality( 0.3,0.01,toe=None )

    legend = [x for x in toelist]

    lsmae = lsrmse = lscoverage = lswp = None
    allist = [lsmae,lsrmse,lscoverage,lswp]

    if 'mae' in toelist:
        lsmae = [(c,mae) for (c,mae,rmse,coverage,wp) in c]
    
    if 'rmse' in toelist:
        lsrmse = [(c,rmse) for (c,mae,rmse,coverage,wp) in c]
    
    if 'coverage' in toelist:    
        lscoverage = [(c,coverage) for (c,mae,rmse,coverage,wp) in c]
   
    if 'percentage_wrong' in toelist:
        lswp = [(c,wp) for (c,mae,rmse,coverage,wp) in c]

    prettyplot( [x for x in allist if x], 'PlotTrustMetricOverNet.png' ,legend = tuple(toelist), showlines=True)
    
    return

if __name__ == "__main__":
    import sys

    #not implemented as script
    if len(sys.argv) < 5:
        print "USAGE: trustplot type [tmlist toe | tm toelist]"
        print "type = overNet | overToe"
        sys.exit(1)
