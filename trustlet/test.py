
from pprint import pprint
from Advogato import *
from trustmetrics import *
from pylab import *
from networkx import *
from analysis import *
from evaluate import *
from networkx.spectrum import *

G = Advogato(comp_threshold = 7)
#analyze(G)
# evaluate(G, advogato_tm)

# e1 = evaluate(G, advogato_tm)

for TM in [AdvogatoTM]:
    e2 = classy_evaluate(G, TM)
#e1 = evaluate(G, guakamole_tm)


# evaluate(G, advogato_tm)


