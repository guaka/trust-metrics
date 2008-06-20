from gen_table import *
from trustlet.TrustMetric import *
from trustlet.PredGraph import *
from trustlet import AdvogatoNetwork

#G = Kaitiaki() #SqueakFoundation()    

G = AdvogatoNetwork(date="2007-08-27")

evaluated_trust_metrics = [
                           #AdvogatoGlobalTM(G), #AdvogatoTM,
                           #PageRankGlobalTM(G),
                           #PageRankTM0,
                           TrustMetric(G,always_master),TrustMetric( G, always_journeyer ),
                           TrustMetric(G,always_apprentice), TrustMetric(G,always_observer),
                           TrustMetric(G, random_tm),
                           TrustMetric(G,ebay_tm), TrustMetric(G,outa_tm), TrustMetric(G,outb_tm),
                           TrustMetric(G,edges_b_tm ),TrustMetric(G, edges_b_tm),
                           #TrustMetric(G,moletrust_generator(horizon=2)),
                           #TrustMetric(G,moletrust_generator(horizon=3)),
                           #TrustMetric(G,moletrust_generator(horizon=4)),
                           #TrustMetric(G,moletrust_generator(horizon=2,edge_trust_threshold=0.5)),
                           #TrustMetric(G,moletrust_generator(horizon=3,edge_trust_threshold=0.5)),
                           #TrustMetric(G,moletrust_generator(horizon=4,edge_trust_threshold=0.5))
                           #GuakaMoleFullTM, GuakaMoleTM, PaoloMoleTM, IntersectionTM, 
                          ]
eval_measures = ['coverage_cond', 'abs_error_cond', 'root_mean_squared_error_cond','yes_no_error_cond']


#conds_on_edges = ['and_cond(master, edge_to_connected_node(5))',
#                  'and_cond(master, not_cond(edge_to_connected_node(5)))',
#                  'and_cond(not_cond(master), edge_to_connected_node(5))']
conds_on_edges = ['every_edge',
                  'edge_to_controversial_node(10, 0.20)'
                  ]


pred_graphs = map(lambda tm: PredGraph(tm), evaluated_trust_metrics)

for eval_measure in eval_measures:
    conds, evals = evals_with_conds(pred_graphs, eval_measure, conds_on_edges)
    display(eval_measure,conds, evals)
    
#methods, evals = somemethods(G)
#display(methods, evals)
