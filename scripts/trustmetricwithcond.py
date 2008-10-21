from printAllTrustMetricsPerformance import *

def leaveObserver( e ):
    return e[2]['level'] != 'Observer'


compareAllTrustMetrics( ["PageRankTM"], leaveObserver )
