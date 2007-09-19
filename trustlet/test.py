
from pprint import pprint
from Advogato import *
from trustmetrics import *
from pylab import *
from networkx import *
from analysis import *
from evaluate import *
from networkx.spectrum import *

#G = Advogato(comp_threshold = 7)
#analyze(G)
# evaluate(G, pagerank_tm)

G = Kaitiaki(comp_threshold = 0)
analyze(G)
# evaluate(G, advogato_tm)

e2 = classy_evaluate(G, GuakaMoleTM)
e1 = evaluate(G, guakamoletm)


# evaluate(G, advogato_tm)


