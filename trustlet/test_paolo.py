"""
Constantly evolving test stuff.

It will often reflect what paolo was working on in a specific
revision.  It might be removed in the future if trustlet ever reaches
a beta stage.

"""
from __init__ import *
from pylab import *
from networkx import *
from analysis import *
from pprint import pprint

def ev(CG, G):
    return map(lambda tm: CG(G, tm),
               [AdvogatoTM,
                AdvogatoGlobalTM])

#G = K = Kaitiaki()
#G = S = SqueakFoundation()
G = A = Advogato()


#pg = PredGraph(A, PageRankTM0, recreate = False, predict_ratio=0.01)
#pg = PredGraph(G, AdvogatoGlobalTM, recreate = True, predict_ratio=0.01)
#pg = PredGraph(G, AdvogatoGlobalTM, recreate = True, predict_ratio=1.0)
pg = PredGraph(G, AdvogatoTM, recreate = True, predict_ratio=0.011)

#pg10 = PredGraph(G, MoletrustTM_horizon1_threshold0, recreate = False, predict_ratio=1.0)
#pg20 = PredGraph(G, MoletrustTM_horizon2_threshold0, recreate = False, predict_ratio=0.01)
#pg30 = PredGraph(G, MoletrustTM_horizon3_threshold0, recreate = False, predict_ratio=1.0)
#pg40 = PredGraph(G, MoletrustTM_horizon4_threshold0, recreate = False, predict_ratio=1.0)
#pg50 = PredGraph(G, MoletrustTM_horizon5_threshold0, recreate = False, predict_ratio=1.0)

#pg105 = PredGraph(G, MoletrustTM_horizon1_threshold05, recreate = False, predict_ratio=1.0)
#pg205 = PredGraph(G, MoletrustTM_horizon2_threshold05, recreate = False, predict_ratio=1.0)
#pg305 = PredGraph(G, MoletrustTM_horizon3_threshold05, recreate = False, predict_ratio=1.0)
#pg405 = PredGraph(G, MoletrustTM_horizon4_threshold05, recreate = False, predict_ratio=1.0)
#pg505 = PredGraph(G, MoletrustTM_horizon5_threshold05, recreate = False, predict_ratio=1.0)

#pga = ev(PredGraph, K, predict_ratio=0.1)

#for p in pga:
#   pprint (p.evaluate())

#p=pga[1]
#p.coverage_with_condition(every_edge)
