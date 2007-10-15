"""
Constantly evolving test stuff.

It will often reflect what guaka was working on in a specific
revision.  It might be removed in the future if trustlet ever reaches
a beta stage.

"""


from __init__ import *

try:
    from pylab import *
except:
    print "no pylab!"
from networkx import *
from analysis import *

from pprint import pprint



def ev(CG, G):
    return map(lambda tm: CG(G, tm),
               [
                IntersectionTM,
                GuakaMoleTM,
                GuakaMoleFullTM,
                PaoloMoleTM,
                PageRankTM0])

K = Kaitiaki()
S = SqueakFoundation()


#pg = PredGraph(K, PageRankTM0, recreate = True)

pga = ev(PredGraph, S)

for p in pga:
   pprint (p.evaluate())

#p=pga[1]
#p.coverage_with_condition(every_edge)

