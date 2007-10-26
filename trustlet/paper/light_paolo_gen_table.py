from gen_table import *
from TrustMetric import *
import PredGraph
import Advogato

evaluated_trust_metrics = [
                           AlwaysMaster, AlwaysJourneyer, AlwaysApprentice, AlwaysObserver,
                           RandomTM,
                           EbayTM,
                           OutA_TM, OutB_TM, EdgesB_TM, EdgesA_TM,
                           MoletrustTM_horizon2_threshold0,
                           MoletrustTM_horizon3_threshold0, MoletrustTM_horizon4_threshold0,
                           MoletrustTM_horizon2_threshold05, MoletrustTM_horizon3_threshold05, MoletrustTM_horizon4_threshold05,
                           AdvogatoGlobalTM,
                           #AdvogatoTM,
                           PageRankGlobalTM,
                           #PageRankTM0,
                           #GuakaMoleFullTM, GuakaMoleTM, PaoloMoleTM, IntersectionTM, 
                          ]
eval_measures = ['coverage_cond', 'abs_error_cond', 'yes_no_error_cond']

#G = Advogato.Advogato()
G = Kaitiaki() #SqueakFoundation()    

#conds_on_edges = ['and_cond(master, edge_to_connected_node(5))',
#                  'and_cond(master, not_cond(edge_to_connected_node(5)))',
#                  'and_cond(not_cond(master), edge_to_connected_node(5))']
conds_on_edges = ['every_edge',
                  'edge_to_connected_node(5)',
                  'edge_to_connected_node(15)',
                  'edge_to_connected_node(25)',
                  'edge_to_connected_node(35)',
                  'edge_to_controversial_node(20, 0.05)',
                  'edge_to_controversial_node(20, 0.1)',
                  'edge_to_controversial_node(20, 0.15)',
                  'edge_to_controversial_node(20, 0.2)',
                  'edge_to_controversial_node(10, 0.05)',
                  'edge_to_controversial_node(10, 0.10)',
                  'edge_to_controversial_node(10, 0.15)',
                  'edge_to_controversial_node(10, 0.20)',
                  'edge_to_controversial_node(10, 0.25)',
                  'edge_to_controversial_node(5, 0.05)',
                  'edge_to_controversial_node(5, 0.10)',
                  'edge_to_controversial_node(5, 0.15)',
                  'edge_to_controversial_node(5, 0.20)',
                  'edge_to_controversial_node(5, 0.25)',
                  'master',
                  'observer',
                  'journeyer',
                  'apprentice',
                  ]


eval_measure=eval_measures[1]
for evaluated_trust_metric in evaluated_trust_metrics:
    pred_graph = PredGraph.PredGraph(G,evaluated_trust_metric)
    conds, evals = evals_with_conds([pred_graph], eval_measure, conds_on_edges)
    display(eval_measure,conds, evals)
    pred_graph = None #possibly freeing the memory

eval_measure=eval_measures[0]
for evaluated_trust_metric in evaluated_trust_metrics:
    pred_graph = PredGraph.PredGraph(G,evaluated_trust_metric)
    conds, evals = evals_with_conds([pred_graph], eval_measure, conds_on_edges)
    display(eval_measure,conds, evals)
    pred_graph = None #possibly freeing the memory

#pred_graphs = map(lambda tm: PredGraph.PredGraph(G,tm), evaluated_trust_metrics)

#for eval_measure in eval_measures:
#    conds, evals = evals_with_conds(pred_graphs, eval_measure, conds_on_edges)
#    display(eval_measure,conds, evals)
    
#methods, evals = somemethods(G)
#display(methods, evals)
