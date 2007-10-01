###############################################
# classier way of dealing with this
#
# 
# OBSERVATION: When calculating tm(G,a,b) it's not actually needed to
# pass the graph all the time, edge(a,b) can be removed in the trust
# metric class. For simple trust metrics this won't matter, but for
# more "advanced" ones like Advogato and PageRank this might
# considerably speed up things.


class TrustMetric:
    """A generic trust metric class"""
    def __init__(self, G):
        """Use this to plug in functional trust metrics"""
        self.G = G
        self._set_tm()
        
    def leave_one_out(self, e):
        self.G.delete_edge(e)
        trust_value = self.trustmetric(self.G, e[0], e[1])
        self.G.add_edge(e)
        return trust_value

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

class PageRankTM(TrustMetric):
    def __init__(self, G_orig):
        self.G = value_on_edges(G_orig)
        
    def leave_one_out(self, e_orig):
        edge = [e for e in self.G.edges() if e[0] == e_orig[0] and e[1] == e_orig[1]][0]
        self.G.delete_edge(edge)
        trust_value = pagerank_tm(self.G, e[1])
        self.G.add_edge(edge)
        return trust_value



