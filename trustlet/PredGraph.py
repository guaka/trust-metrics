
import Dataset
from helpers import *

import os
import math
import time
from networkx import write_dot, XDiGraph

try:
    import scipy
except:
    print "damn! no scipy!"

UNDEFINED = -37 * 37  #mayby use numpy.NaN?


class CalcGraph(Dataset.Network):
    """Generic calculation graph class"""

    def __init__(self, dataset, TM, recreate = False):
        """Create object from dataset using TM as trustmetric."""
        Dataset.Network.__init__(self, make_base_path = False)

        self.dataset, self.TM = dataset, TM

        self.start_time = time.time()
        self.path = reduce(os.path.join, [Dataset.dataset_dir(), get_name(dataset), get_name(TM)])
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.filepath = os.path.join(self.path, get_name(self) + '.dot')

        if not recreate and os.path.exists(self.filepath):
            self._read_dot(self.filepath)
        else:
            graph = self._generate()
            self._write_pred_graph_dot(graph)
        self._set_arrays()
        self._prepare()
        if self.TM.rescale:
            self._rescale()
        print "Init took", hms(time.time() - self.start_time)

    def _rescale(self):
        scale = (0.4, 1)  # probably for the dataset
        pt = self.pred_trust
        min_pt, max_pt = min(pt), max(pt)
        print "rescaling:", (min_pt, max_pt), "to", scale
        mult =  (scale[1] - scale[0]) / (max_pt - min_pt)
        pt_scaled = scale[0] + (pt - min_pt) * mult
        self.pred_trust = pt_scaled
        for e in self.edges_iter():
            t = dict(self.get_edge(e[0], e[1]))
            t['pred'] = scale[0] + (float(t['pred']) - min_pt) * mult
            self.add_edge(e[0], e[1], t)


    def _set_arrays(self):
        self.pred_trust = self._trust_array()
        self.undef_mask = self.pred_trust == UNDEFINED
        self.def_mask = map(lambda x: not x, self.undef_mask)
        self.num_undefined = sum(self.undef_mask)
        self.num_defined = len(self.pred_trust) - self.num_undefined

        
    def _trust_array(self, which_one = 'pred'):
        def mapper(val):
            val = val[2][which_one]
            return (val == 'None') and UNDEFINED or float(val)
        return self._edge_array(mapper)

    def _write_pred_graph_dot(self, pred_graph):
        print "Writing", self.filepath,
        print "-", len(pred_graph.nodes()), "nodes", len(pred_graph.edges()), "edges"
        write_dot(pred_graph, self.filepath)

    def mean_std(self):
        """Calculate mean and standard deviation."""
        only_def = []
        for e in self.pred_trust:
            if e != UNDEFINED:
                only_def.append(e)
        return scipy.mean(only_def), scipy.std(only_def)

    def coverage(self):
        """Return coverage, part of the graph that is defined."""
        return 1.0 - (1.0 * self.num_undefined / len(self.edges()))

    def evaluate(self):
        """Evaluate the graph."""
        evals = [(f.__name__, f())
                 for f in [self.coverage, self.mean_std]
                 ]
        evals.insert(0, (get_name(self.dataset), get_name(self.TM)))
        return evals

    def _time_indicator(self, count, moreinfo = ""):
        # print edge, predicted_trust
        avg_t = (time.time() - self.start_time) / count
        eta = avg_t * (len(self.dataset.edges()) - count)
        print '#', int(count), "avg time:", avg_t, "ETA", hms(eta), moreinfo
        

class TotalGraph(CalcGraph):
    """This graph should have edges for all nodes.
 
    Since these trust metrics are supposed to be used on the entire
    graph actually using them on the entire graph should give us some
    interesting data to play with.
    """
    def _generate(self):
        tg = self._predict_all()
        self._paste_graph(tg)
        return tg

    def _prepare(self):
        pass

    def _predict_all(self):
        count = 0
        pred_graph = XDiGraph()
        tm = self.TM(self.dataset)
        for n1 in self.dataset.nodes_iter():
            pred_graph.add_node(n1)
            for n2 in self.dataset.nodes():  #can't be _iter
                predicted_trust = tm.calc(n1, n2)
                pred_graph.add_edge(n1, n2, {'pred': str(predicted_trust)})
            count += 1.
            if divmod(count, 100)[1] == 0:
                self._time_indicator(count)
        return pred_graph


class PredGraph(CalcGraph):
    """Prediction graph, it contains a trust network with the original
    nodes and edges.  On an edge (a, b) there is both the original
    trust value ['orig'] from a to b but also the predicted trust
    value ['pred'] predicted by the trust metric for (a, b), by
    leaving out edge (a, b). If a prediction was not possible, the
    predicted trust is None."""

    def _generate(self):
        pg = self._predict_existing()
        self._paste_graph(pg)
        return pg
        
    def _prepare(self):
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
        
        self.orig_trust = self._trust_array('orig')

    def _predict_existing(self):
        """Predict existing nodes by leaving out the edge"""
        pred_graph = XDiGraph()
        for n in self.dataset.nodes():
            pred_graph.add_node(n)

        count = 0
        tm = self.TM(self.dataset)
        for edge in self.dataset.edges_iter():
            predicted_trust = tm.leave_one_out(edge)
            pred_graph.add_edge(edge[0], edge[1], {'pred': str(predicted_trust)})
            count += 1.
            if divmod(count, 100)[1] == 0:
                self._time_indicator(count, (edge, predicted_trust))
        return pred_graph

    def edges_cond_iter(self, condition):
        """Yield edges that satisfy condition."""
        for e in self.edges_iter():
            if condition(e):
                yield e

    def coverage_cond(self, condition):
        """Coverage of edges that satisfy condition."""
        num_predicted_edges = num_edges = 0
        for e in self.edges_cond(condition):
            num_edges+=1
            if e[2]['pred'] != UNDEFINED:
                num_predicted_edges+=1
        return num_edges and float(num_predicted_edges)/num_edges

    def abs_error_cond(self, condition):
        """Absolute error of edges satisfying condition."""
        abs_error = num_edges = 0
        for e in self.edges_cond_iter(condition):
            if e[2]['pred'] != UNDEFINED:
                abs_error += abs(e[2]['orig'] - e[2]['pred'])
                num_edges += 1
        return num_edges and abs_error / num_edges

    def abs_error(self):
        """Absolute error."""
        abs_error = self.def_mask * abs(self.pred_trust - self.orig_trust)
        return sum(abs_error) / self.num_defined

    def abs_error_map(self):
        return [self.abs_error_cond(lambda e: e[2]['orig'] == orig)
                for orig in  [0.4, 0.6, 0.8, 1.0]] # should be level_map or something

    def sqr_error(self):
        sqr_error = self.def_mask * (lambda x: (x*x))(self.pred_trust - self.orig_trust)
        return math.sqrt(sum(sqr_error) / self.num_defined)

    def evaluate(self):
        evals = [(f.__name__, f())
                 for f in [self.coverage, self.abs_error, self.abs_error_map, self.sqr_error, self.mean_std]]
        evals.insert(0, (get_name(self.dataset), get_name(self.TM)))
        return evals


def every_edge(edge):
    return True

