
import Dataset
from helpers import *

import os
import math
import time
from networkx import write_dot, XDiGraph

UNDEFINED = -37 * 37  #mayby use numpy.NaN?


class PredGraph(Dataset.Network):
    """Sorry, but, PredNetwork just sounds stupid"""
    def __init__(self, dataset, TM, recreate = False):
        Dataset.Network.__init__(self, make_base_path = False)

        self.dataset = dataset
        self.TM = TM
        
        filepath = reduce(os.path.join, [Dataset.dataset_dir(), get_name(dataset), get_name(TM), 'pred_graph.dot'])
        if not recreate and os.path.exists(filepath):
            self._read_dot(filepath)
        else:
            _classy_evaluate(dataset, TM)
            self._read_dot(filepath)  #should get the predgraph from _classy_evaluate instead

        if len(self.edges()) != len(self.dataset.edges()):
            raise "TROUBLE: #edges in dataset != #edges in predgraph!"

        # add orig trust value into self
        for e in self.dataset.edges():
            # for some RTFMing reason get_edge gives an ItemAttribute, not
            # dict, so we do some casting work here
            t = dict(self.get_edge(e[0], e[1]))
            t['orig'] = self.dataset.trust_on_edge(e)
            t['pred'] = (t['pred'] == 'None') and UNDEFINED or float(t['pred'])
            self.add_edge(e[0], e[1], t)
        
        self.orig_trust = self._trust_array('orig') #WAS: dataset._edge_array(self.dataset.trust_on_edge)
        self.pred_trust = self._trust_array()

        self.undef_mask = self.pred_trust == UNDEFINED
        self.def_mask = map(lambda x: not x, self.undef_mask)
        self.num_undefined = sum(self.undef_mask)
        self.num_defined = len(self.pred_trust) - self.num_undefined

    def _trust_array(self, which_one = 'pred'):
        def mapper(val):
            val = val[2][which_one]
            if val == 'None':
                return UNDEFINED
            else:
                return float(val)
        return self._edge_array(mapper)

    def coverage(self):
        return 1.0 - (1.0 * self.num_undefined / len(self.orig_trust))

    def mask_coverage(self):
        pass
    

    def abs_error(self):
        abs_error = self.def_mask * abs(self.pred_trust - self.orig_trust)
        return sum(abs_error) / self.num_defined

    def sqr_error(self):
        sqr_error = self.def_mask * (lambda x: (x*x))(self.pred_trust - self.orig_trust)
        return math.sqrt(sum(sqr_error) / self.num_defined)

    def evaluate(self):
        evals = [get_name(self.dataset), get_name(self.TM)]
        for f in [self.coverage, self.abs_error, self.sqr_error]:
            evals.append((f.__name__, f()))
        return evals


def _classy_evaluate(G, TM, debug_interval = 100, max_edges = 0):
    """this should be part of PredGraph class"""
    def output():
        if divmod(count, debug_interval)[1] == 0:
            print edge, predicted_trust
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

    tm = TM(G)
    max_edges = max_edges or len(G.edges())
    for edge in G.edges():
        predicted_trust = tm.leave_one_out(edge)
        # print predicted_trust
        pred_graph.add_edge(edge[0], edge[1], {'pred': str(predicted_trust)})
        if predicted_trust is None:
            num_unpredicted_edges += 1
        else:
            abs_err += abs(predicted_trust - G.trust_on_edge(edge))

        count += 1.
        output()
        if max_edges == count:
            break
    save_pred_graph()



if __name__ == "__main__":
    if False:
        # for later
        scale = (0.4, 1)
        pg = PredGraph("Kaitiaki", "PageRankTM")
        pr = pg._edge_array('pred')
        pr_normalized = (pr - min(pr)) / (max(pr) - min(pr))
        pr_scaled = scale[0] + pr_normalized * (scale[1] - scale[0])



