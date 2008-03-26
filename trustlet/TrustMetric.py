"""

TrustMetric classes

These are initiated with the dataset that they're supposed to measure
trust on.

Classier way of dealing with this.

If you want to test 


 
OBSERVATION: When calculating tm(G,a,b) it's not actually needed to
pass the graph all the time, edge(a,b) can be removed in the trust
metric class. For simple trust metrics this won't matter, but for
more "advanced" ones like Advogato and PageRank this might
considerably speed up things.

"""

# FIX: don't use import *
from trustmetrics import *
from helpers import *


class TrustMetric:
    """
    A generic trust metric class.
    The avaiable trust metric functions are:
    always_master
    always_journeyer
    always_observer
    always_apprentice
    random_tm
    intersection_tm
    ebay_tm
    outa_tm
    outb_tm
    edges_a_tm
    DEPRECATED:
    pagerank_tm: for this tm call PageRankTM class.
    """

    # rescale the prediction graph, useful for PageRank
    rescale = False
    # DT
    def __init__(self, dataset , tm ):
        """
        Use this to plug in functional trust metrics
        tm : the trust metric function
        """
        self.dataset = dataset
        self.trustmetric = tm

     #   if hasattr(self, "_set_tm"):
     #      self._set_tm()

    #dt
    def get_tm(self):
        return self.trustmetric

    def __getattr__(self, name):
        if name == "name":
            if hasattr(self, name):
                return self.name
            
        if name == "path_name":
            if hasattr(self, name):
                return self.path_name
            else:
                return self.name
        raise AttributeError
        #return ""

    def calc(self, node1, node2):
        return self.trustmetric(self.dataset, node1, node2)

    def predict_edge(self, edge, leave_one_out = True):
        """Predict edge, leave_one_out or not."""
        if leave_one_out:
            self.dataset.delete_edge(edge)
        trust_value = self.calc(edge[0], edge[1])
        if leave_one_out:
            self.dataset.add_edge(edge)
        return trust_value            

    def leave_one_out(self, edge):
        """DEPRECATED

        The leave-one-out algorithm, for some trust metrics it's
        more efficient to subclass this."""
        return self.predict_edge(edge, leave_one_out = True)





# The following should be rewritten into a more generic class
# generator, e.g.
#
# def MoletrustTM_hor_thr(horizon, threshold):
#     class ClassThing
#         def getname(self):
#             return MoletrustTM_horizon1_threshold0
#     return ClassThing

#non serve a un cazzo
class MoleTrust(TrustMetric):
    #TODO: set some sensible default values.
    
    def __init__(self, dataset, horizon = 2, threshold = 0.3, edge_trust_threshold = 0):
        TrustMetric.__init__(self, dataset , moletrust_generator(horizon = horizon,
                                               pred_node_trust_threshold = threshold,
                                               edge_trust_threshold = edge_trust_threshold) )

MoleTrustTM = MoleTrust  # deprecated


class PageRankTM(TrustMetric):
    rescale = "recur_log_rescale"
    
    def __init__(self, dataset_orig ):
        self.dataset = dataset_orig
        # here it should calculate the PR values for all nodes
        
    def calc(self, n1, n2):
        # this should use precalculated values
        return pagerank_tm(self.dataset,n1, n2)

    def get_tm(self):
        return self

    def leave_one_out(self, e_orig):
        # DT
        # delete_edge solleva un eccezione se l'arco non esiste? se si sto codice non serve 
        edge = [e for e in self.dataset.edges() 
                if e[0] == e_orig[0] and e[1] == e_orig[1]][0]

        #for e in self.dataset.edges():
        #    if e[0] == e_orig[0] and e[1] == e_orig[1]:
        #        edge = e
        #        break
        
        self.dataset.delete_edge(edge) 
        trust_value = pagerank_tm(self.dataset, e[0] , e[1]) 
        self.dataset.add_edge(edge) 
        return trust_value


class PageRankTMfakeLeave1out(TrustMetric):
    rescale = "recur_log_rescale"
    
    def __init__(self, dataset_orig):
        self.dataset = dataset_orig  # beh, need to do something here
        # here it should calculate the PR values for all nodes
        raise NotImplemented
        
    def calc(self, n1, n2):
        # this should use precalculated values
        return pagerank_tm(self.dataset, n1 , n2)

    def leave_one_out(self, e_orig):
        # here it should just fetch the PR value for e_orig

        # the following stuff can be avoided
        edge = [e for e in self.dataset.edges() 
                if e[0] == e_orig[0] and e[1] == e_orig[1]][0]
        self.dataset.delete_edge(edge)
        trust_value = pagerank_tm(self.dataset, e[1])
        self.dataset.add_edge(edge)
        return trust_value

class PageRankGlobalTM(TrustMetric):
    rescale = "recur_log_rescale"
    
    def __init__(self, dataset):
        from pagerank_tm import BasicPageRank
        self.pagerank = BasicPageRank(dataset)
        
    def calc(self, n1, n2):
        return self.pagerank[n2]

    def leave_one_out(self, e_orig):
        """This is just a dummy."""
        return self.calc(None, e_orig[1])


class AdvogatoLocal(TrustMetric):
    """The advogato trust metric."""

    def __init__(self, dataset):
        self.dataset = dataset
        self.p = Profiles(Profile, DictCertifications)
        self.p.add_profiles_from_graph(dataset)

        levels = dataset.level_map.items()
        levels.sort(lambda a,b: cmp(a[1], b[1]))  # sort on trust value
        levels = map((lambda x: x[0]), levels)
        self.t = PymTrustMetric(AdvogatoCertInfo(levels), self.p)

    def leave_one_out(self, e):
        a, b, level = e
        level = level.values()[0]
        self.p.del_cert(a, 'like', b, level)
        r = self.t.tmetric_calc('like', [e[0]])
        self.p.add_cert(a, 'like', b, level)
                
        if b in r.keys():
            return self.dataset.level_map[r[b]]
        else:
            return None

AdvogatoLocalTM = AdvogatoTM = AdvogatoLocal # deprecated

class AdvogatoGlobalTM(TrustMetric):
    """The advogato trust metric, global, seeds: the 4 masters of advogato."""

    def __init__(self, dataset):
        self.dataset = dataset
        self.p = Profiles(Profile, DictCertifications)
        self.p.add_profiles_from_graph(dataset)
        
        levels = dataset.level_map.items()
        levels.sort(lambda a,b: cmp(a[1], b[1]))  # sort on trust value
        levels = map((lambda x: x[0]), levels)
        self.t = PymTrustMetric(AdvogatoCertInfo(levels), self.p)
        for s in self.dataset.advogato_seeds:
            assert s in dataset, "The seed node %s is not in the graph" % s
        self.pred_trust = self.t.tmetric_calc('like', 
                                              self.dataset.advogato_seeds)
        self.pred_trust_keys = self.pred_trust.keys()
        
    def leave_one_out(self, edge):
        # def predict_edge(self, e, leave_one_out = True) maybe...
        a, b, level = edge
            # level = level['level']
        if b in self.pred_trust_keys:
            return self.dataset.level_map[self.pred_trust[b]]
        else:
            return 0.4 # should depend on dataset.level_map

class AdvogatoTMDefaultObserver(AdvogatoTM):
    pass


class AdvogatoGlobalTMDefaultObserver(AdvogatoGlobalTM):
    pass


if __name__ == "__main__":
    from trustlet import *

    D = DummyNetwork()
    predgraphs = PredGraph( TrustMetric( D , ebay_tm ) )
    predgraphs.abs_error()
    
    

"""
class AlwaysMaster(TrustMetric):
    def _set_tm(self):
        self.trustmetric = always_master

class AlwaysJourneyer(TrustMetric):
    def _set_tm(self):
        self.trustmetric = always_journeyer

class AlwaysApprentice(TrustMetric):
    def _set_tm(self):
        self.trustmetric = always_apprentice

class AlwaysObserver(TrustMetric):
    def _set_tm(self):
        self.trustmetric = always_observer

class RandomTM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = random_tm

class IntersectionTM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = intersection_tm

class Ebay(TrustMetric):
    def _set_tm(self):
        self.trustmetric = ebay_tm

EbayTM = Ebay  # deprecated

class OutA_TM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = outa_tm

class OutB_TM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = outb_tm

class EdgesA_TM(TrustMetric):
    #Average of outgoing and incoming edges of a
    def _set_tm(self):
        self.trustmetric = edges_a_tm

class EdgesB_TM(TrustMetric):
    #Average of outgoing and incoming edges of b
    def _set_tm(self):
        self.trustmetric = edges_b_tm
"""
