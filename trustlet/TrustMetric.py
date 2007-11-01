"""

TrustMetric classes

These are initiated with the dataset that they're supposed to measure
trust on.

"""


###############################################
# classier way of dealing with this
#
# 
# OBSERVATION: When calculating tm(G,a,b) it's not actually needed to
# pass the graph all the time, edge(a,b) can be removed in the trust
# metric class. For simple trust metrics this won't matter, but for
# more "advanced" ones like Advogato and PageRank this might
# considerably speed up things.

from trustmetrics import *
from helpers import *

class TrustMetric:
    """A generic trust metric class"""

    # rescale the prediction graph, useful for PageRank
    rescale = False
    def __init__(self, G):
        """Use this to plug in functional trust metrics"""
        self.G = G
        self._set_tm()
        
    def __getattr__(self, name):
        if name == "name":
            if hasattr(self, name):
                return self.name
            else:
                raise AttributeError
        if name == "path_name":
            if hasattr(self, name):
                return self.path_name
            else:
                return self.name
        raise AttributeError

    def calc(self, n1, n2):
        return self.trustmetric(self.G, n1, n2)

    def leave_one_out(self, e):
        """The leave-one-out algorithm, for some trust metrics it's
        more efficient to subclass this."""
        self.G.delete_edge(e)
        trust_value = self.calc(e[0], e[1])
        self.G.add_edge(e)
        return trust_value


# turning functions into classes, I wish I could do 
class GuakaMoleTM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = guakamole_tm


class GuakaMoleFullTM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = guakamole_full_tm


class PaoloMoleTM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = paolomole_tm



# The following should be rewritten into a more generic class
# generator, e.g.
#
# def MoletrustTM_hor_thr(horizon, threshold):
#     class ClassThing
#         def getname(self):
#             return MoletrustTM_horizon1_threshold0
#     return ClassThing

class MoletrustTM_horizon1_threshold0(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor1_threshold0

class MoletrustTM_horizon2_threshold0(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor2_threshold0

class MoletrustTM_horizon3_threshold0(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor3_threshold0

class MoletrustTM_horizon4_threshold0(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor4_threshold0

class MoletrustTM_horizon5_threshold0(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor5_threshold0

class MoletrustTM_horizon1_threshold05(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor1_threshold05

class MoletrustTM_horizon2_threshold05(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor2_threshold05

class MoletrustTM_horizon3_threshold05(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor3_threshold05

class MoletrustTM_horizon4_threshold05(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor4_threshold05

class MoletrustTM_horizon5_threshold05(TrustMetric):
    def _set_tm(self):
        self.trustmetric = moletrust_tm_hor5_threshold05

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

class EbayTM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = ebay_tm

class OutA_TM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = outa_tm

class OutB_TM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = outb_tm

class EdgesA_TM(TrustMetric):
    """Average of outgoing and incoming edges of a"""
    def _set_tm(self):
        self.trustmetric = edges_a_tm

class EdgesB_TM(TrustMetric):
    """Average of outgoing and incoming edges of b"""
    def _set_tm(self):
        self.trustmetric = edges_b_tm

class PageRankTM0(TrustMetric):
    rescale = "recur_log_rescale"
    
    def __init__(self, G_orig):
        self.G = G_orig
        # here it should calculate the PR values for all nodes
        
    def calc(self, n1, n2):
        # this should use precalculated values
        return pagerank_tm(self.G, n2)

    def leave_one_out(self, e_orig):
        edge = [e for e in self.G.edges() if e[0] == e_orig[0] and e[1] == e_orig[1]][0]
        self.G.delete_edge(edge)
        trust_value = pagerank_tm(self.G, e[1])
        self.G.add_edge(edge)
        return trust_value


class PageRankTMfakeLeave1out(TrustMetric):
    rescale = "recur_log_rescale"
    
    def __init__(self, G_orig):
        self.G = G_orig  # beh, need to do something here
        # here it should calculate the PR values for all nodes
        raise NotImplemented
        
    def calc(self, n1, n2):
        # this should use precalculated values
        return pagerank_tm(self.G, n2)

    def leave_one_out(self, e_orig):
        # here it should just fetch the PR value for e_orig

        # the following stuff can be avoided
        edge = [e for e in self.G.edges() if e[0] == e_orig[0] and e[1] == e_orig[1]][0]
        self.G.delete_edge(edge)
        trust_value = pagerank_tm(self.G, e[1])
        self.G.add_edge(edge)
        return trust_value

class PageRankGlobalTM(TrustMetric):
    rescale = "recur_log_rescale"
    
    def __init__(self, G):
        from pagerank_tm import BasicPageRank
        self.pagerank = BasicPageRank(G)
        
    def calc(self, n1, n2):
        return self.pagerank[n2]

    def leave_one_out(self, e_orig):
        """This is just a dummy."""
        return self.calc(None, e_orig[1])


class AdvogatoTM(TrustMetric):
	"""The advogato trust metric."""

	def __init__(self, G):
		self.G = G
		self.p = Profiles(Profile, DictCertifications)
		self.p.add_profiles_from_graph(G)

		levels = G.level_map.items()
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
                    return self.G.level_map[r[b]]
		else:
                    return None


class AdvogatoGlobalTM(TrustMetric):
	"""The advogato trust metric, global, seeds: the 4 masters of advogato."""

	def __init__(self, G):
	    self.G = G
	    self.p = Profiles(Profile, DictCertifications)
	    self.p.add_profiles_from_graph(G)
	
	    levels = G.level_map.items()
	    levels.sort(lambda a,b: cmp(a[1], b[1]))  # sort on trust value
	    levels = map((lambda x: x[0]), levels)
	    self.t = PymTrustMetric(AdvogatoCertInfo(levels), self.p)
	    for s in self.G.advogato_seeds:
	        assert s in G, "the seed node %s is not in the graph and this is not allowed" % s
	    self.pred_trust = self.t.tmetric_calc('like', self.G.advogato_seeds)
	    
	    self.pred_trust_keys = self.pred_trust.keys()

	def leave_one_out(self, e):
	    a, b, level = e
	    # level = level['level']
	    if b in self.pred_trust_keys:
	        return self.G.level_map[self.pred_trust[b]]
	    else:
	        return 0.4 # should depend on G.level_map

if __name__ == "__main__":
    import Advogato, PredGraph
    
    GRAPH = Advogato.Advogato()
    PREDGRAPHS = PredGraph.PredGraph(GRAPH, PageRankGlobalTM)
    
    
