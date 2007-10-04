"""
Constantly evolving test stuff.

It will often reflect what guaka was working on in a specific
revision.  It might be removed in the future if trustlet ever reaches
a beta stage.

"""

from pprint import pprint

from Advogato import *
from TrustMetric import *
from PredGraph import *


from pylab import *
from networkx import *
from analysis import *


# from evaluate import * DEPRECATED

G = SqueakFoundation()

pga = map(lambda tm: PredGraph(G, tm),
          [GuakaMoleTM, IntersectionTM, GuakaMoleFullTM])

for p in pga:
    p.evaluate()
