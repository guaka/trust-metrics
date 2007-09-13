
from Advogato import *
from trustmetrics import *
from pylab import *
from networkx import *
from analysis import *
from evaluate import *

G = Advogato("tiny")
analyze(G)
evaluate(G, ebay_tm)

G = SqueakFoundation(comp_threshold = 0)
analyze(G)
evaluate(G, ebay_tm)


