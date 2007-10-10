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
                return "ni"
            
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

class IntersectionTM(TrustMetric):
    def _set_tm(self):
        self.trustmetric = intersection_tm

class PageRankTM0(TrustMetric):
    rescale = True
    
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
    rescale = True
    
    def __init__(self, G_orig):
        self.G = G_orig  # beh, need to do something here
        # here it should calculate the PR values for all nodes
        raise "not yet implemented"
        
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

