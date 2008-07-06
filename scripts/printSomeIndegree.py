from printAlltrustMetricsPerformance import compareAllTrustMetrics

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
