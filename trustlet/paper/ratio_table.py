from gen_table import *
from TrustMetric import *
import PredGraph
import Advogato
from ThresholdTM import thresholder


eval_measures = [
                 'yes_no_error_cond',
                 'root_mean_squared_error_cond',
                 'coverage_cond',
                 'abs_error_cond',
                 ]

G = Advogato.Advogato()
#G = Kaitiaki()
#G = SqueakFoundation()    

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

#for evaluated_trust_metric in [AdvogatoGlobalTM, thresholder(AdvogatoGlobalTM)]:
for evaluated_trust_metric in [AdvogatoTM, thresholder(AdvogatoTM)]:
    pred_graph = PredGraph.PredGraph(G, evaluated_trust_metric, predict_ratio = 0.02)
    for eval_measure in eval_measures:
        conds, evals = evals_with_conds([pred_graph], eval_measure, conds_on_edges)
        display(eval_measure,conds, evals)
    del pred_graph
