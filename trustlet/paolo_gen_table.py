from gen_table import *

G = SqueakFoundation()    
#G = Advogato()

evaluated_trust_metrics = [
                           AlwaysMaster, AlwaysJourneyer, AlwaysApprentice, AlwaysObserver,
                           RandomTM,
                           EbayTM, OutA_TM, OutB_TM, EdgesB_TM, EdgesA_TM,
                           MoletrustTM_horizon1_threshold0, MoletrustTM_horizon2_threshold0, MoletrustTM_horizon3_threshold0, MoletrustTM_horizon4_threshold0,
                           MoletrustTM_horizon1_threshold05, MoletrustTM_horizon2_threshold05, MoletrustTM_horizon3_threshold05, MoletrustTM_horizon4_threshold05,
                           #AdvogatoGlobalTM, AdvogatoTM,
                           #PageRankGlobalTM, PageRankTM0,
                           #GuakaMoleFullTM, GuakaMoleTM, PaoloMoleTM, IntersectionTM, 
                          ]
eval_measures = ['coverage_cond', 'abs_error_cond']
conds_on_edges = ['and_cond(master, edge_to_connected_node(5))',
                  'and_cond(master, not_cond(edge_to_connected_node(5)))',
                  'and_cond(not_cond(master), edge_to_connected_node(5))']

pred_graphs = map(lambda tm: PredGraph(G,tm), evaluated_trust_metrics)

for eval_measure in eval_measures:
    conds, evals = evals_with_conds(G, pred_graphs, eval_measure, conds_on_edges)
    display(eval_measure,conds, evals)
    
#methods, evals = somemethods(G)
#display(methods, evals)
