"""
Generate table to make Paolo happy.

Well, and me too actually.

http://www.trustlet.org/wiki/A_comparison_of_trust_metrics_on_Advogato_social_network


For a certain dataset we want to have a table in which the rows are
the different trust metrics and the columns the evaluation techniques.

Rows:
* PageRank
* Advogato
* some moletrusts
* ebay
* always 1

Columns:
* coverage
* mean_abs_error
* root_mean_squared_error
* mean_abs_error on [0.4, 0.6, 0.8, 1.0]

for datasets: Kaitiaki, SqueakFoundation, Advogato

""" 

from __init__ import *

from pylab import *
from networkx import *
from analysis import *

from pprint import pprint


G = Kaitiaki()

ev_methods = ['coverage', 'abs_error', 'abs_error_map', 'sqr_error', 'mean_std']

evals = []
for tm in [GuakaMoleTM, IntersectionTM, PageRankTM0, AdvogatoTM]:
    pg = PredGraph(G, tm)
    print pg.coverage()
    evals.append([(f, getattr(pg, f)())
                  for f in ev_methods])

pprint (evals)
        
