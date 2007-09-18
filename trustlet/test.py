
from pprint import pprint
from Advogato import *
from trustmetrics import *
from pylab import *
from networkx import *
from analysis import *
from evaluate import *
from networkx.spectrum import *

G = Advogato("tiny", comp_threshold = 7)
analyze(G)
evaluate(G, pagerank_tm)

# evaluate(G, advogato_tm)

# G = Kaitiaki(comp_threshold = 0)
# analyze(G)
# evaluate(G, advogato_tm)

