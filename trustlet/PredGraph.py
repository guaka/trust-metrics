
"""
Prediction graph
================


Analysis of trust metrics through predicting edges.

"""

from Dataset.Network import Network
from helpers import *
from TrustMetric import *

import os
import math
from random import random
import time

from networkx import XDiGraph
try:
    from networkx import write_dot
except:
    print "No networkx.write_dot, consider install pygraphviz"

try:
    import scipy
except:
    print "damn! no scipy!"


class CalcGraph(Network):
    """Generic calculation graph class"""

    def __init__(self, TM, recreate = False, predict_ratio = 1.0):
        """Create object from dataset using TM as trustmetric.
        predict_ratio is the part of the edges that will randomly be
        picked for prediction."""
        Network.__init__(self, make_base_path = False)

        self.TM = TM
        self.dataset = dataset = TM.dataset
        self.predict_ratio = predict_ratio

        self.start_time = time.time()

        if hasattr(dataset, "filepath"):
            self.path = os.path.join(os.path.split(dataset.filepath)[0],
                                     path_name(TM))
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            self.filepath = os.path.join(self.path, 
                                         get_name(self) + '.dot')

            if not recreate and os.path.exists(self.filepath):
                self._read_dot(self.filepath)
            else:
                graph = self._generate()
                self._write_pred_graph_dot(graph)
                
        self._set_arrays()
        self._prepare()
        if hasattr(self.TM, 'rescale') and self.TM.rescale:
            self._rescale()
        print "Init took", hms(time.time() - self.start_time)

    def get_name(self):
        """Override get_name."""
        name = self.__class__.__name__
        if self.predict_ratio != 1.0:
            name += "-r" + str(self.predict_ratio)
        return name

    def _rescale(self):
        """Rescale if needed."""
        # scale = (0.4, 1)  # probably for the dataset
        rescaler = eval(self.TM.rescale)  
        # rescaled = rescale_array(rescaler(self.pred_trust), scale)
        rescaled = rescaler(self.pred_trust)
        scale_dict = dict(zip(self.pred_trust, rescaled))
        for e in self.edges_iter():
            t = dict(self.get_edge(e[0], e[1]))
            # print idx, t['pred'], rescaled[idx]
            t['pred'] = scale_dict[t['pred']]
            self.add_edge(e[0], e[1], t)
        self.prescaled = self.pred_trust
        self.pred_trust = rescaled

    def _set_arrays(self):
        """Set some numpy arrays."""
        self.pred_trust = self._trust_array()
        self.undef_mask = self.pred_trust == UNDEFINED
        self.def_mask = map(lambda x: not x, self.undef_mask)
        self.num_undefined = sum(self.undef_mask)
        self.num_defined = len(self.pred_trust) - self.num_undefined

    def _trust_array(self, which_one = 'pred'):
        """Return numpy array of pred (default) or orig values."""
        def mapper(edge):
            val = edge[2][which_one]
            return ( (val == 'None') or (val == 0.0) ) and UNDEFINED or float(val)
        return self._edge_array(mapper)

    def _write_pred_graph_dot(self, pred_graph):
        """Write PredGraph.dot."""
        print "Writing", self.filepath,
        print "-", len(pred_graph.nodes()),
        print "nodes", len(pred_graph.edges()), "edges"
        write_dot(pred_graph, self.filepath)

    def _defined_list(self):
        """List of defined predictions."""
        only_def = []
        for edge in self.pred_trust:
            if edge != UNDEFINED:
                only_def.append(edge)
        return only_def

    def mean_std(self):
        """Calculate mean and standard deviation. DEPRECATED!"""
        dl = self._defined_list()
        return scipy.mean(dl), scipy.std(dl)

    def mean(self):
        """Mean value of predictions."""
        return scipy.mean(self._defined_list())

    def std(self):
        """Standard deviation of predictions."""
        return scipy.std(self._defined_list())

    def coverage(self):
        """Coverage, part of the graph that is defined."""
        return 1.0 - (1.0 * self.num_undefined / len(self.edges()))

    def evaluate(self):
        """Evaluate the graph. DEPRECATED"""
        evals = [(f.__name__, f())
                 for f in [self.coverage, self.mean_std]
                 ]
        evals.insert(0, (get_name(self.dataset), get_name(self.TM)))
        return evals

    def _time_indicator(self, count, moreinfo = ""):
        """Indicate time."""
        # print edge, predicted_trust
        avg_t = (time.time() - self.start_time) / count
        eta = avg_t * (len(self.dataset.edges()) - count)
        print '#', int(count), "avg time:", 
        print avg_t, "ETA", est_datetime_arr(eta), moreinfo
        


class PredGraph(CalcGraph):
    """Prediction graph, it contains a trust network with the original
    nodes and edges.  On an edge (a, b) there is both the original
    trust value ['orig'] from a to b but also the predicted trust
    value ['pred'] predicted by the trust metric for (a, b), by
    leaving out edge (a, b). If a prediction was not possible, the
    predicted trust is None."""

    def __init__(self, TM, leave_one_out = True, recreate = False, predict_ratio = 1.0):
        self.leave_one_out = leave_one_out
        CalcGraph.__init__(self, TM,
                           recreate = recreate,
                           predict_ratio = predict_ratio)

    def _generate(self):
        """Generate the prediction graph."""
        print "Generating", self.filepath
        pg = self._predict_existing()
        self._paste_graph(pg)
        return pg
        
    def _prepare(self):
        """Prepare. Data"""
        ratio = 1.0 * self.number_of_edges() / self.dataset.number_of_edges()

        # if True:  # check if self has orig
        if ratio == 1.0:
            # add orig trust value into self
            for e in self.dataset.edges_iter():
                # for some RTFMing reason get_edge gives an
                # ItemAttribute, not dict, so we do some casting
                # work here
                x = dict(self.get_edge(e[0], e[1]))
                x['orig'] = self.dataset.trust_on_edge(e)
                x['pred'] = (( (x['pred'] == 'None') or (x['pred'] == 0.0) ) and 
                             UNDEFINED or float(x['pred']))
                self.add_edge(e[0], e[1], x)
            self.orig_trust = self._trust_array('orig')
        else:
            print "#edges in dataset != #edges in predgraph!"
            print "actual ratio: ", ratio
            for e in self.edges_iter():
                x = dict(self.get_edge(e[0], e[1]))
                # for some reason the upper line (which is neater) 
                # doesn't work here
                orig_value = self.dataset.get_edge(e[0], e[1]).values()[0]
                x['orig'] = self.dataset.level_map[orig_value]
                x['pred'] = (( (x['pred'] == 'None') or (x['pred'] == 0.0) ) and
                             UNDEFINED or float(x['pred']))
                self.add_edge(e[0], e[1], x)
            self.orig_trust = self._trust_array('orig')

    def _predict_existing(self):
        """Predict existing nodes by leaving out the edge"""
        pred_graph = XDiGraph()  # could be avoided when working on self
        for n in self.dataset.nodes():
            pred_graph.add_node(n)

        count = 0
        tm = self.TM
        predicted_trust = None
        for edge in self.dataset.edges_iter():
            if (self.predict_ratio == 1.0 or
                random() <= self.predict_ratio):
                predicted_trust = tm.leave_one_out(edge)
                pred_graph.add_edge(edge[0], edge[1], 
                                    {'pred': str(predicted_trust)})
                                     #'orig': str(self.dataset.trust_on_edge(edge)})
                count += 1
                if divmod(count, 100)[1] == 0:
                    self._time_indicator(count, (edge, predicted_trust))
        return pred_graph
        

    def edges_cond_iter(self, condition):
        """Yield edges that satisfy condition, you can pass the
        condition as code or as a string if you please to do so."""
        if type(condition) == str:
            condition = eval(condition)
        for e in self.edges_iter():
            if condition(self, e):
                yield e

    def edges_cond(self, condition):
        """Return list of edges that satisfy condition."""
        return [e for e in self.edges_cond_iter(condition)]

    def coverage_cond(self, condition):
        """Coverage of edges that satisfy condition."""
        num_predicted_edges = num_edges = 0
        for e in self.edges_cond_iter(condition):
            num_edges += 1
            if e[2]['pred'] != UNDEFINED:
                num_predicted_edges += 1
        return num_edges and float(num_predicted_edges)/num_edges

    def abs_error_cond(self, condition):
        """Absolute error of edges satisfying condition."""
        abs_error = num_edges = 0
        for e in self.edges_cond_iter(condition):
            if e[2]['pred'] != UNDEFINED:
                abs_error += abs(e[2]['orig'] - e[2]['pred'])
                num_edges += 1
        return num_edges and (num_edges, abs_error / num_edges)

    def root_mean_squared_error_cond(self, condition):
        """Root Mean Squared error of edges satisfying condition."""
        abs_error = num_edges = 0.0
        for e in self.edges_cond_iter(condition):
            if e[2]['pred'] != UNDEFINED:
                abs_error += numpy.power(e[2]['orig'] - e[2]['pred'],2)
                num_edges += 1
        return num_edges and (num_edges, numpy.sqrt(abs_error / num_edges))

    def yes_no_error_cond(self, condition):
        """1 if the predicted edge is the same as the real edge, 0 if not"""
        yes_no_error = num_edges = 0.0
        for e in self.edges_cond_iter(condition):
            if e[2]['pred'] != UNDEFINED:
                if e[2]['orig'] == e[2]['pred']:
                    yes_no_error += 1
                num_edges += 1
        return num_edges and (num_edges, yes_no_error / num_edges)

    def mean_cond(self, condition):
        """Mean of edges satisfying condition."""
        num_edges = 0
        l = []
        # ugly
        for e in self.edges_cond_iter(condition):
            if e[2]['pred'] != UNDEFINED:
                l.append(e[2]['pred'])
                num_edges += 1
        return num_edges and (num_edges, scipy.mean(l))

    #deprecated, testTM is better ;-)
    def __abs_error(self):
        """Absolute error."""
        abs_error = self.def_mask * abs(self.pred_trust - self.orig_trust)
        return self.num_defined and (sum(abs_error) / self.num_defined)

    def sqr_error(self):
        """Root mean squared error."""
        sqr_error = self.def_mask * (lambda x: (x*x))(self.pred_trust -
                                                      self.orig_trust)
        return self.num_defined and math.sqrt(sum(sqr_error) / self.num_defined)


    #DT
    def testTM( self, singletrustm = True, np=4, onlybest=True, plot = False ):
        """
        This function test a single trust metric or all the trust metrics, 
        on a specific network
        
        parameters:
        singletrustm: if false, check all the trustmetrics, else only the trustmetric
                      in the predgraph class instance
        plot: plot or not an istogram with the results
        np: number of processors
        
        return a tuple, with the best trustmetric and it's average error, or if
        onlybest is set to False, all the trustmetric with his own MAE
        """
        
        if singletrustm:
            return self.__abs_error()
        
        lris = [] # list of results (performances), one for each trust metric evaluated

        K = self.TM.dataset
        path = self.dataset.path+'/TrustMetrics'

        trustmetrics = {
            "intersection_tm" : TrustMetric( K , intersection_tm ),
            "edges_a_tm" : TrustMetric( K , edges_a_tm ),
            "edges_b_tm" : TrustMetric( K , edges_b_tm ),
            "ebay_tm" : TrustMetric( K , ebay_tm ),
            "outa_tm" : TrustMetric( K , outa_tm ),
            "outb_tm" : TrustMetric( K , outb_tm ),
            "random_tm" : TrustMetric( K , random_tm ),
            "moletrust_tm" : TrustMetric( K , 
                                          moletrust_generator( 4 , 0.0 , 0.0 ) ),
            "PageRankTM" : PageRankTM( K )
            }

        #for each trust metric, print the predicted value for each edge
        bestname = ''
        bestvalue = 1.0

	#parameters:
	#path is the path on which to save the computation
	#tm is the trustMetric class 
	#tmname is the trust metric name, 
        #predgraph                                      
        def eval( (path,tm,tmname,predgraph) ):
            #tm = current tm
            #tmname = my predgraph tm

            evaltmname = get_name(tm)

            if evaltmname == tmname:
                return (predgraph.__abs_error(),tmname)

            sum = 0
            cnt = 0
            abs = load( {'tm':evaltmname},path+'/cache' )
            
            if abs != None:
                sum,cnt = abs
            else:
                for edge in tm.dataset.edges_iter():
                    #extract the original trust value and the predicted trust value in order to compute the absolute error in this prediction
                    orig_trust = tm.dataset.trust_on_edge(edge)
                    pred_trust = tm.leave_one_out(edge)
                    
                    sum = sum + math.fabs(orig_trust - pred_trust)
                    cnt = cnt + 1
                    
                save({'tm':evaltmname},(sum,cnt),path+'/cache')
                    
            return ( float(sum/cnt), evaltmname )

	# we use splittask so that we can split the computation in parallel across different processors (splittask is defined in helpers.py). Neet to check how much this is efficient or needed.
        lris = splittask( eval , [(path,trustmetrics[tm],get_name(self.TM),self) for tm in trustmetrics], np ) 

        if onlybest:
            lris.sort()
            return lris[0]
        else:
            if plot:
                
                plotparameters( [x for x in enumerate([x for (x,s) in lris])], path+'/TrustMetricsHistogram.png', 
                                title = 'MAE for each trustmetric on '+get_name(self.dataset)+' network',
                                xlabel='trust metrics',
                                ylabel='MAE',
                                istogram = True )

            fd = file( path+'/HistogramLegend', 'w' )
            fd.write( '\n'.join( [str(n)+': '+s for (n,s) in enumerate([y+' '+str(x) for (x,y) in lris])] ) )
            fd.close()

            lris.sort()

            return lris

                         
    def graphcontroversiality( self, maxc, step, indegree = 5, np=2, plot=False ):
        """
        This function save a graph with
        x axis: level of controversiality (max value = maxc)
        y axis: an error measure (MAE)
        parameter:
           maxc {maxcontroversiality} = the max value of controversiality
                                        in the graph
           step = from 0.0 to maxc with step == step
           indegree = the min indegree
           np = number of processes
           plot = if true, plot a graph of the results
        """
        def plot():
            plotparameters( tuplelist, self.path+'/error-controversiality-onlypoint.png',
                            title = 'MAE for each level of controversiality',
                            xlabel = 'controversiality', 
                            ylabel = 'MAE', onlypoint=True )

            plotparameters( tuplelist, self.path+'/error-controversiality.png',
                            title = 'MAE for each level of controversiality',
                            xlabel = 'controversiality', 
                            ylabel = 'MAE' )
            return None

        
        start = 0
        end = 1
        weight = 2

        i = 0.0
        r = []
        #create list of value from 0.0 to maxc (step = step) 
        while( i <= maxc ):
            r.append( round(i,5) )
            i += step
        #foreach controversiality level
        
        def eval( (net, max) ):    
           #calcolate the abs_error of the edges over the controversiality limit
           #and append it to tuplelist in a tuple (controversiality,abs_error)
            
            abs = load( {'func':'graphcontroversiality',
                        'controversiality_level':max},
                       net.path+'/cache'
                       )
            
            if abs != None:
                (sum,cnt) = abs
            else:
                sum = 0
                cnt = 0
                for e in net.edges_iter():
                    if cnt % 1000 == 0:
                        print "counter: ", cnt
                    if len( net.dataset.in_edges( e[end] )) < indegree:
                        continue
                    if net.dataset.node_controversiality( e[end] ) >= max: 
                        sum += math.fabs(e[weight]['orig'] - e[weight]['pred'])
                        cnt += 1
                       
                        
                ret = save( {'func':'graphcontroversiality',
                             'controversiality_level':max},
                            (sum,cnt),
                            net.path+'/cache'
                            )
                        
                if not ret:
                    print "Warning! i cannot be able to save this computation, check the permission"
                    print "for this path: "+self.path+"/cache"
                        
                print "MAE evaluated for %f controversiality" % max
            
            if cnt:
                return (max,float(sum)/cnt)
            else:
                return None

        tuplelist = splittask( eval, [(self,max) for max in r], np )

        if plot:
            plot()
        
        return tuplelist


    def evaluate(self):
        """A bunch of evaluations. DEPRECATED"""
        evals = [(f.__name__, f())
                 for f in [self.coverage, self.abs_error,
                           self.abs_error_map, self.sqr_error, self.mean_std]]
        evals.insert(0, (get_name(self.dataset), get_name(self.TM)))
        return evals

    def abs_error_map(self):
        """Deprecated"""
        return [self.abs_error_cond(lambda pg, e: e[2]['orig'] == orig)
                for orig in  [0.4, 0.6, 0.8, 1.0]]
        # should be level_map or something # or calling trust_on_edge()

    def abs_error_for_different_orig_nodes(self):
        return [(cond, self.abs_error_cond(cond)) for cond in
                ['master', 'journeyor', 'apprentice', 'observer']]

def edge_to_connected_node(number=5):
    """True if the node which is target of the edge received at least
    'number' incoming trust statements."""
    return lambda pg, edge: pg.in_degree(edge[1])>=number

def edge_to_controversial_node(number = 10, controversy = 0.2):
    """Condition for edges with target nodes with at least number
    in_edges and a standard deviation greater than controversy."""
    def func(pg, edge):
        edges_in_target = pg.in_edges(edge[1])
        if len(edges_in_target) < number:
            return False
        std = scipy.std(map(lambda e:e[2]['orig'], edges_in_target))
        return std >= controversy
    return func

every_edge = lambda pg, edge: True
master = lambda pg, edge: edge[2]['orig'] == 1.0
journeyer = lambda pg, edge: edge[2]['orig'] == 0.8
apprentice = lambda pg, edge: edge[2]['orig'] == 0.6
observer = lambda pg, edge: edge[2]['orig'] == 0.4

def and_cond(cond1, cond2):
    """cond1 and cond2"""
    return lambda pg, edge: cond1(pg, edge) and cond2(pg, edge)
    
def or_cond(cond1, cond2):
    """cond1 or cond2"""
    return lambda pg, edge: cond1(pg, edge) or cond2(pg, edge)

def not_cond(cond):
    """not cond"""
    return lambda pg, edge: not cond(pg, edge)

def in_edges_cond(node):
    return lambda pg, edge: edge[1] == node


if __name__ == "__main__":
    from trustlet import *
    K = AdvogatoNetwork( date="2008-04-28" )
    tm = TrustMetric( K , moletrust_generator(horizon=4) )
    P = PredGraph( tm )
    P.graphcontroversiality( 0.3 , 0.01, np=2 )
