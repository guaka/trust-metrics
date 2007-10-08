"""
Constantly evolving test stuff.

It will often reflect what guaka was working on in a specific
revision.  It might be removed in the future if trustlet ever reaches
a beta stage.

"""


from __init__ import *

recreate = True

def generate_tms(CG, G):
    return map(lambda tm: CG(G, tm, recreate = recreate),
               [PageRankTM0,
                #AdvogatoTM,
                IntersectionTM,
                GuakaMoleTM,
                GuakaMoleFullTM,
                PaoloMoleTM])


for G in [Kaitiaki(), SqueakFoundation(), AdvogatoTM]:
    pg = generate_tms(PredGraph, G)
    tg = generate_tms(TotalGraph, G)


