"""
Constantly evolving test stuff.

It will often reflect what guaka was working on in a specific
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

K = Kaitiaki()
S = SqueakFoundation()


#pg = PredGraph(K, PageRankTM0, recreate = True)

pga = ev(PredGraph, K)

for p in pga:
   pprint (p.evaluate())

#p=pga[1]
#p.coverage_with_condition(every_edge)

