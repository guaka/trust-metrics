
from Advogato import *
from trustmetrics import *
from pylab import *
from networkx import *
from analysis import *
from evaluate import *

G = Advogato(comp_threshold = 7)
analyze(G)
evaluate(G, advogato_tm)

# G = Kaitiaki(comp_threshold = 0)
# analyze(G)
# evaluate(G, advogato_tm)

