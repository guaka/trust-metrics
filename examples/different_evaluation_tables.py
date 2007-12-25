"""
Once we have a PredGraph already computed (read from file), we get many different tables from it
"""

# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')

#create datasets
dummyNetwork=DummyNetwork()

#create trust metrics
EbayTM=EbayTM()
MT2=Moletrust(2)
MT3=Moletrust(3)
AdvogatoLocalTM=AdvogatoLocalTM()
PagerankTM=PagerankTM()
AlwaysMaster=ConstantTM(1.0)


#create the predgraphs based on leave-one-out (also with ratios)
pred_graph=PredGrap(dummyNetwork,MT2,0.1,generate=false) #predict 10% of edges with leave-one-out

#


#NOW something more generic, able to create predgraph for different trust metrics (on a single dataset) and evaluated with different evaluation measures
# and only on edges satisfying certain conditions.
#
#for example, i would like to quickly see:
# for different trust metrics (on the rows), show a table with different evaluation measures (on columns), 
#  one table for different conditions (multiplicity) 
# 

evaluated_trust_metrics = [ # an array of already created objects which correspond to trust metrics
                            EbayTM,
                            MT2,
                            MT3,
                            AdvogatoLocalTM
                          ]
eval_measures = [#'coverage_cond',
                 #'abs_error_cond',
                 'yes_no_error_cond',
                 'root_mean_squared_error_cond',
                 ]


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

# for example the method might be the generic
#predGraph.getPredictionTable(rows=[array of trust metrics],columns=[array of evaluation measures],multiplicity=array of conditions on edges,precision=number_of_decimals)
#that will generate for example
#%% Condition=controversial_edges(0.3,0.5)     number of edges= 2367
#                  |  fraction wrong predictions  |         MAE |        RMSE           |    Coverage   | #edgeswithprediction
#AdvogatoLocal     |    0.343423                  |  0.11134342 |  0.322343423          |     1.00      | 2367
#AlwaysMaster      |    0.343423                  |  0.11134342 |  0.322343423          |     0.50      | 1186
#Ebay              |    0.887 555                 |  0.11134342 |  0.322343423          |     1.00      | 2367
#Moletrust3_0.4    |    0.343444                  |  0.11134342 |  0.322343423          |     1.00      | 2367
#%% Condition=every_edge()                     number of edges= 51344
#                  |  fraction wrong predictions  |         MAE |        RMSE           |    Coverage   | #edgeswithprediction
#AdvogatoLocal     |    0.343423                  |  0.11134342 |  0.322343423          |     1.00      | 51344
#AlwaysMaster      |    0.343423                  |  0.11134342 |  0.322343423          |     0.84      | 50222
#Ebay              |    0.887 555                 |  0.11134342 |  0.322343423          |     1.00      | 51344
#Moletrust3_0.4    |    0.343444                  |  0.11134342 |  0.322343423          |     1.00      | 51344



for eval_measure in eval_measures:
    for evaluated_trust_metric in evaluated_trust_metrics:
        pred_graph = PredGraph.PredGraph(G,evaluated_trust_metric)
        conds, evals = evals_with_conds([pred_graph], eval_measure, conds_on_edges)
        display(eval_measure,conds, evals)
        pred_graph = None #possibly freeing the memory
