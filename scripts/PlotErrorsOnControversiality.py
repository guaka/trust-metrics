from trustlet import *

k = KaitiakiNetwork()
tm = TrustMetric( k , intersection_tm )
tm1 = PageRankTM( k )
p1 = PredGraph( tm )
p2 = PredGraph( tm1 )
tp = ('mae','rmse','coverage','percentage_wrong')

ls = p1.graphcontroversiality( 0.3,0.01,toe=tp[0], indegree=0 );
ls1 = p2.graphcontroversiality( 0.3,0.01,toe=tp[0], indegree=0 );


prettyplot( [ls,ls1], 'qwe.png' ,legend = ('intersection','PageRank'), showlines=True)
