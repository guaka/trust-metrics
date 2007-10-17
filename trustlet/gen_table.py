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


def display(eval_measure, methods, evals):
    from Table import Table
    tbl = Table([18] + [20] * len(methods))
    tbl.printHdr([" " + eval_measure] + methods)
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
    for tm in [GuakaMoleTM, IntersectionTM, PageRankTM0, PageRankGlobalTM, AdvogatoTM]:
        pg = PredGraph(G, tm)
        evals[get_name(tm)] = [getattr(pg, f)()
                               for f in ev_methods]
    return ev_methods, evals


def evals_with_conds(G, pred_graphs, eval_measure ,conds_on_edges):
    evals = {}
    for pg in pred_graphs:
        evals[get_name(pg.TM)] = [getattr(pg, eval_measure)(c)
                                  for c in conds_on_edges]
    return conds_on_edges, evals

if __name__ == "__main__":
    G = SqueakFoundation()    
    #G = Advogato()

    evaluated_trust_metrics = [EbayTM, OutA_TM]
    #evaluated_trust_metrics = [EbayTM, OutA_TM, OutB_TM, EdgesB_TM, EdgesA_TM,MoletrustTM_horizon1_threshold0, MoletrustTM_horizon2_threshold0, MoletrustTM_horizon3_threshold0, MoletrustTM_horizon3_threshold0, MoletrustTM_horizon4_threshold0]
    eval_measures = ['coverage_cond', 'abs_error_cond']
    conds_on_edges = ['and_cond(master, edge_to_connected_node(5))',
                      'and_cond(master, not_cond(edge_to_connected_node(5)))',
                      'and_cond(not_cond(master), edge_to_connected_node(5))']
    #evaluated_trust_metrics = [GuakaMoleTM, IntersectionTM, PageRankGlobalTM, AdvogatoGlobalTM]
    # choose!
    #AdvogatoGlobalTM  EdgesB_TM        MoletrustTM_horizon1_threshold0   MoletrustTM_horizon4_threshold0   OutB_TM
    #AdvogatoTM        MoletrustTM_horizon2_threshold0   MoletrustTM_horizon4_threshold05  PageRankGlobalTM
    #AlwaysMaster      GuakaMoleFullTM  MoletrustTM_horizon2_threshold05  MoletrustTM_horizon5_threshold0   PageRankTM0
    #EbayTM            GuakaMoleTM      MoletrustTM_horizon3_threshold0   MoletrustTM_horizon5_threshold05  PaoloMoleTM
    #EdgesA_TM         IntersectionTM   MoletrustTM_horizon3_threshold05  OutA_TM                           RandomTM

    pred_graphs = map(lambda tm: PredGraph(G,tm), evaluated_trust_metrics)

    for eval_measure in eval_measures:
        conds, evals = evals_with_conds(G, pred_graphs, eval_measure, conds_on_edges)
        display(eval_measure,conds, evals)
        
    #methods, evals = somemethods(G)
    #display(methods, evals)
