#!/usr/bin/env python

"""
This script calculate the graphics in gnuplot that compares pairs of network.
If there aren't parameters, it take all the trust metric, elsewhere you can
specify on command line space-separated name of trustmetric to leave out.
"""


from trustlet import *


def compareAllTrustMetrics( leaveOut = [], new_name=None,
                            cond=None,
                            network = None, #AdvogatoNetwork("2008-05-12") 
                            allInOne=True, 
                            path = ".", toe = "mae", np=None,
                            x_range=None,
                            y_range=None, ind=[3,5,10,15,20], plist = None ):
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
       network = the network on wich trustmetrics will be evaluated.
       allInOne = specify if the graph contains all trustmetrics (true case), else the script create
                  n graphs, where 'n' is the cartesian product of the trustmetrics set.
       path = the path where save the graphs
       x_range = tuple with the lowest limit and highest limit for x axes
       y_range = tuple with the lowest limit and highest limit for y axes
       ind = list of the indegree on wich you would calculate the graphs ,
             NB: the elements must be integers
       plist = list of tuple as this: [(name_predgraph1,predgraph1),....,(name_predgraphN,predgraphN)]
               if is set None, it is recalculated with the network passed. You must pass in each case the network parameter.
    """
    

    if not network or network == None:
        A = AdvogatoNetwork( date="2008-05-12" )
    else:
        A = network
        
    rename = {}

    if plist == None:
        tmlist = getTrustMetrics( A )
    
        for l in leaveOut:
            try:
                del tmlist[l]
            except KeyError:
                print "KeyError! ",l," not deleted"

        plist = []

        for tm in tmlist:
            if new_name == None or not new_name.has_key(tm):
                #create a fake dictionary map each tm in itself
                rename[tm] = tm
            elif new_name.has_key(tm):
                #add to rename the real dict
                rename[tm]=new_name[tm]

            plist.append( (tm,PredGraph( tmlist[tm] )) )
            
    else:
        for x in plist:
            tm = x[0]
            if new_name == None or not new_name.has_key(tm):
                #create a fake dictionary map each tm in itself
                rename[tm] = tm
            elif new_name.has_key(tm):
                #add to rename the real dict
                rename[tm]=new_name[tm]

        
    
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

    return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print "USAGE: ./printAllTMPerformance.py False|True True|False mae|rmse|percentage_wrong|coverage|all list_of_TrustMetric_to_include"
        print "Legend:"
        print "False|True: if False the list of trustMetric represent the tm that you want, else represent the trustmetric that you would to leave out."
        print "True|False: if true the trust metric were plotted in one graphics, else it were plotted pair to pair in different graphics."
        print "all|...: what kind of error you would calculate? choose one, or 'all' that plot in different graphics all the other error"
        print "list: the list of trustmetric name, space-separated" 
        print ""
        print "NB: the default network is AdvogatoNetwork, date 2008-05-12, if you wuold change it, you must use ipython, import this script,"
        print "    and call the function compareAllTrustMetrics by hand. For the informations about parameters," 
        print "    see the documentation of the function"
        exit(0)

    leaveOut = bool(sys.argv[1])
    allInOne = bool(sys.argv[2])
    toe = sys.argv[3]
    list = sys.argv[3:]

    if leaveOut:
        compareAllTrustMetrics( leaveOut=list, allInOne=allInOne, toe=toe )
    else:
        A = AdvogatoNetwork( date="2008-05-12" )
        
        tmlist = getAllTrustMetrics( A )
        plist = []

        for tm in list:
            plist.append( (tm, PredGraph( tmlist[tm] )) )

        compareAllTrustMetrics( plist = plist, allInOne=allInOne, toe=toe )
                          
