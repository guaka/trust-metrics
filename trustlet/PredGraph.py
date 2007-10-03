
from Dataset import *
from evaluate import *
from helpers import *



class PredGraph(Network):
    """Sorry, but, PredNetwork just sounds stupid"""
    def __init__(self, dataset, TM, recreate = False):
        Network.__init__(self, make_base_path = False)
        
        filepath = reduce(os.path.join, [dataset_dir(), get_name(dataset), get_name(TM), 'pred_graph.dot'])
        if not recreate and os.path.exists(filepath):
            self._read_dot(filepath)
        else:
            _classy_evaluate(dataset, TM)



def _classy_evaluate(G, TM, debug_interval = 1, max_edges = 0):
    """this should be part of PredGraph class"""
    def output():
        if debug_interval == 1:
            print edge, predicted_trust

        if divmod(count, debug_interval)[1] == 0:
            t = time.time()
            acc = abs_err / count
            # acc2 = sqr_err / count
            unpredicted = num_unpredicted_edges / count
            avg_t = (t - start_time) / count
            eta = avg_t * (max_edges - count)
            print 'cnt', int(count), 'acc', acc, 'unpredicted', unpredicted, "avg time:", avg_t, "ETA", hms(eta)
            prev_time = t

    def save_pred_graph():
        gtm_path = os.path.join(G.path, get_name(TM))
        if not os.path.exists(gtm_path):
            os.mkdir(gtm_path)
        pred_path = os.path.join(gtm_path, "pred_graph.dot")
        print "Saving error graph as", pred_path
        # G.G = pred_graph
        write_dot(pred_graph, pred_path)

    pred_graph = XDiGraph()
    for n in G.nodes():
        pred_graph.add_node(n)

    num_unpredicted_edges = abs_err = sqr_err = count = 0
    start_time = prev_time = time.time()
    print "start time:", start_time
    tm = TM(G)
    max_edges = max_edges or len(G.edges())
    for edge in G.edges():
        predicted_trust = tm.leave_one_out(edge)
        print predicted_trust
        pred_graph.add_edge(edge[0], edge[1], {'predtrust': str(predicted_trust)})
        if predicted_trust is None:
            num_unpredicted_edges += 1
        else:
            abs_err += abs(predicted_trust - G.trust_on_edge(edge))

        count += 1.
        output()
        if max_edges == count:
            break

    num_predicted_edges = max_edges - num_unpredicted_edges
    coverage = (num_predicted_edges * 1.0) / max_edges
    accuracy = abs_err / (num_predicted_edges or 1)

    output = (TM.__name__, accuracy, coverage)
    pprint (output)
    
    save_pred_graph()

    return output 


if __name__ == "__main__":
    

    if False:
        # for later
        scale = (0.4, 1)
        pg = PredGraph("Kaitiaki", "PageRankTM")
        pr = pg._edge_array('predtrust')
        pr_normalized = (pr - min(pr)) / (max(pr) - min(pr))
        pr_scaled = scale[0] + pr_normalized * (scale[1] - scale[0])



