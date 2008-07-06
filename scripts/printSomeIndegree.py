#!/usr/bin/env python
from trustlet import *

def compareAllTrustMetrics( leaveOut = [], 
                            cond=None,date = "2008-05-12", allInOne=True, 
                            path = ".", toe = "mae", np=None,
                            x_range=None,
                            y_range=None, ind=[3,5,10,15,20], plist=None ):
    """
    toe can have all possible values PredGraph.graphcontroversiality function, 
    and a special value "all" that indicates that you would calculate 4 graphs 
    with all errors measure.
    """

    if not plist:
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

    if toe == 'all':
        num = enumerate( ['mae','rmse','percentage_wrong','coverage'] )
    else:
        num = [(0,toe)]

    select = lambda tp,s: (tp[0],tp[s])

    for indegree in ind:
        print 'indegree:', indegree
        pointlist = []

        for p in plist:
            if toe == 'all':
                pointlist.append( ( get_name(p.TM) , p.graphcontroversiality( 0.3 , 0.01, toe=None, np=np, cond=cond,
                                                                              indegree = indegree )) )
            else:
                pointlist.append( ( get_name(p.TM) , p.graphcontroversiality( 0.3 , 0.01, toe=toe, np=np, cond=cond,
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



#from printAlltrustMetricsPerformance import compareAllTrustMetrics

def no_observer( e ):
    if type(e[2]['orig']) is float:
        return e[2]['orig'] != 0.4
    else:
        return e[2]['orig'] != 'Observer'

def func():
    A = AdvogatoNetwork( date="2008-05-12" )

    tmlist = getTrustMetrics( A )
    leaveOut=['PageRankTM','AdvogatoGlobalTM','AdvogatoLocal']
        
    for l in leaveOut:
        try:
            del tmlist[l]
        except KeyError:
            print "KeyError! ",l," not deleted"

    plist = []
            
    for tm in tmlist:
        plist.append( PredGraph( tmlist[tm] ) )
                
                
    compareAllTrustMetrics(
        cond=no_observer,
        path='./graphs',
        toe='all',
        np=4,
        plist=plist,
        ind=[3]
        )

    compareAllTrustMetrics(
        cond=no_observer,
        path='./graphs',
        toe='all',
        np=4,
        plist=plist,
        ind=[15]
        )
    compareAllTrustMetrics(
        cond=no_observer,
        path='./graphs',
        toe='all',
        np=4,
        plist=plist,
        ind=[20]
        )
    compareAllTrustMetrics(
        cond=no_observer,
        path='./graphs',
        toe='all',
        np=4,
        plist=plist,
        ind=[10]
        )
    compareAllTrustMetrics(
        cond=no_observer,
        path='./graphs',
        toe='all',
        np=4,
        plist=plist,
        ind=[1]
        )
    
func()
