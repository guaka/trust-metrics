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
               [PageRankTM0, #AdvogatoTM,
                IntersectionTM,
                GuakaMoleTM,
                GuakaMoleFullTM,
                PaoloMoleTM])

#K = Kaitiaki()
#S = SqueakFoundation()
A = Advogato()

#pg = PredGraph(A, PageRankTM0, recreate = True, predict_ratio=0.01)
pg = PredGraph(A, MoletrustTM_horizon1_threshold0, recreate = True, predict_ratio=1.0)
#pg = PredGraph(A, AdvogatoGlobalTM, recreate = True, predict_ratio=0.0001)
#pg = PredGraph(A, AdvogatoTM, recreate = True, predict_ratio=0.01)

#pga = ev(PredGraph, K, predict_ratio=0.1)

#for p in pga:
#   pprint (p.evaluate())

#p=pga[1]
#p.coverage_with_condition(every_edge)

