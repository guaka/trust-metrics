"""
Constantly evolving test stuff.

It will often reflect what guaka was working on in a specific
revision.  It might be removed in the future if trustlet ever reaches
a beta stage.

"""


from PredGraph import PredGraph
from Advogato import Kaitiaki, SqueakFoundation, Advogato

recreate = True

def generate_tms(CG, G):
    return map(lambda tm: CG(G, tm, recreate = recreate),
               [PageRankTM0,
                #AdvogatoTM,
                IntersectionTM,
                GuakaMoleTM,
                GuakaMoleFullTM,
                PaoloMoleTM])


for G in [Kaitiaki(), SqueakFoundation(), Advogato()]:
    pg = generate_tms(PredGraph, G)


