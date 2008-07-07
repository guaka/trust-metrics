"""
This script calculate the graphics in gnuplot that compares pair of network.
If there aren't parameters, it take all the trust metric, elsewhere you can
specify on command line space-separated name of trustmetric to leave out.
"""


from trustlet import *


def compareAllTrustMetrics( leaveOut = [], new_name=None,
                            cond=None,date = "2008-05-12", allInOne=True, 
                            path = ".", toe = "mae", np=None,
                            x_range=None,
                            y_range=None, ind=[3,5,10,15,20] ):
    """
    this function compare all the trust metric.
    Parameters:
       toe = can have all possible values PredGraph.graphcontroversiality function, 
             and a special value "all" that indicates that you would calculate 4 graphs 
             with all errors measure.
       leaveOut = list of TrustMetric name to exclude from comparation
       new_name = dictionary with as key the name of trustmetric to rename, 
                  and as value the new name of trustmetric to plot on graph.
       cond = function that takes an edge, and return True or False.
              if cond return True, the edge is included in the computation, instead not.
       date = the date in format aaaa-mm-dd of the advogatoNetwork, on wich trustmetrics will evaluate.
       allInOne = specify if the graph contains all trustmetrics (true case), else the script create
                  n graphs, where 'n' is the cartesian product of the trustmetrics set.
       path = the path where save the graphs
       x_range = tuple with the lowest limit and highest limit for x axes
       y_range = tuple with the lowest limit and highest limit for y axes
       ind = list with only one element (for an ignote bug the other were ignored)
             the elements must be integers, and indicates the indegree on wich you would calculate the graphs
       
    """

    A = AdvogatoNetwork( date=date )

    tmlist = getTrustMetrics( A )
    
    for l in leaveOut:
        try:
            del tmlist[l]
        except KeyError:
            print "KeyError! ",l," not deleted"

    plist = []
    rename = {}

    for tm in tmlist:
        if new_name == None or not new_name.has_key(tm):
            #create a fake dictionary map each tm in itself
            rename[tm] = tm
        elif new_name.has_key(tm):
            #add to rename the real dict
            rename[tm]=new_name[tm]

        plist.append( (tm,PredGraph( tmlist[tm] )) )
        
    
    if toe == 'all':
        num = enumerate( ['mae','rmse','percentage_wrong','coverage'] )
    else:
        num = [(0,toe)]

    select = lambda tp,s: (tp[0],tp[s])

    for indegree in ind:
        print 'indegree:', indegree
        pointlist = []

        for x in plist:
            name,p = x
            if toe == 'all':
                pointlist.append( ( rename[name] , p.graphcontroversiality( 0.3 , 0.01, toe=None, np=np, cond=cond,
                                                                              indegree = indegree )) )
            else:
                pointlist.append( ( rename[name] , p.graphcontroversiality( 0.3 , 0.01, toe=toe, np=np, cond=cond,
                                                                              indegree = indegree)) )
        for i in num:

            if allInOne:
            #all trust metrics in one graph
                prettyplot( [[select( x,i[0]+1 ) for x in ls if x] for (name,ls) in pointlist], 
                            os.path.join( path, i[1]+"All (indegree=%d).png"%indegree ),
                            legend=tuple([y for (y,x) in pointlist]),
                            showlines=True,
                            x_range=x_range,
                            y_range=y_range,
                            title='All trust metric for '+i[1]+' error (indegree=%d)'%indegree,
                            xlabel='controversiality',
                            ylabel=i[1])

            else:
            #each trust metric vs each trust metric
                for p in pointlist:
                    for q in pointlist:
                        if q[0] <= p[0]:
                            continue
                        else:
                            print q[0]+"_vs_"+p[0]
                            prettyplot( [q[1],p[1]], 
                                        os.path.join( path, q[0]+"_vs_"+p[0]+" (indegree=%d).png"%indegree ), 
                                        legend=(q[0],p[0]), 
                                        showlines=True,
                                        title=q[0]+"_vs_"+p[0]+" (indegree=%d).png"%indegree,
                                        x_range=x_range,
                                        y_range=y_range,
                                        xlabel='controversiality',
                                        ylabel=i[1] )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        
        compareAllTrustMetrics( sys.argv[1:] )
    
    else:
    
        compareAllTrustMetrics(y_range=(0.0,1.0),toe='all')
