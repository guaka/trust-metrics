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

try:
    from pylab import *
except:
    print "no pylab"
from networkx import *
from analysis import *


def display(methods, evals):
    from Table import Table
    tbl = Table([18] + [20] * len(methods))
    tbl.printHdr([" "] + methods)
    tbl.printSep()

    def display_what(thing):
        if type(thing) == float:
            return "%f" % thing
        if thing == 0:
            return 0
        else:
            return "%f %i" % (thing[1], thing[0])

    for tm in evals:
        tbl.printRow([tm] + map(display_what, evals[tm]))

def somemethods(G):
    ev_methods = ['coverage', 'abs_error', 'sqr_error', 'mean', 'std']

    evals = {}
    for tm in [GuakaMoleTM, IntersectionTM, PageRankTM0, AdvogatoTM]:
        pg = PredGraph(G, tm)
        evals[get_name(tm)] = [getattr(pg, f)()
                               for f in ev_methods]
    return ev_methods, evals


def evals_with_conds(G, method_cond):
    conds = ['and_cond(master, edge_to_connected_node(5))',
             'and_cond(master, not_cond(edge_to_connected_node(5)))',
             'and_cond(not_cond(master), edge_to_connected_node(5))']
    
    evals = {}
    for tm in [GuakaMoleTM, IntersectionTM, PageRankTM0, AdvogatoTM]:
        pg = PredGraph(G, tm)
        evals[get_name(tm)] = [getattr(pg, method_cond)(c)
                               for c in conds]
    return conds, evals
    
G = Kaitiaki()
#methods, evals = somemethods(G)
#display(methods, evals)

ev_methods = ['coverage_cond', 'abs_error_cond', 'mean_cond']
for m in ev_methods:
    conds, evals = evals_with_conds(G, m)
    display(conds, evals)

