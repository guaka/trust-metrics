"""
Constantly evolving test stuff.

It will often reflect what guaka was working on in a specific
revision.  It might be removed in the future if trustlet ever reaches
a beta stage.

"""

from pprint import pprint
from Advogato import *
from TrustMetric import *
from pylab import *
from networkx import *
from analysis import *
from evaluate import *
from networkx.spectrum import *
from PredGraph import *

G = SqueakFoundation()

for TM in [GuakaMoleTM, IntersectionTM, GuakaMoleFullTM, PageRankTM]:
    e1 = PredGraph(G, TM)
    # e2 = classy_evaluate(G, TM)

