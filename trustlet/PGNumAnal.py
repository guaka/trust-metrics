

"""Analysis of PredGraphs through NumPy.  A lot faster."""


from math import sqrt
import PredGraph
UDF = PredGraph.UNDEFINED

class PGNumAnal:
    """Analysis of PredGraph through NumPy."""
    def __init__(self, pg):
        self.pg = pg
        self.orig = pg.orig_trust
        self.pred = pg.pred_trust
        self.defmask = self.pred != UDF
        self.origdef = self.orig[self.defmask]
        self.preddef = self.pred[self.defmask]

    def _apply_cond(self, a, b, cond):
        if cond is None:
            return (a, b)
        else:
            return (a[cond(a)], b[cond(a)])
    
    def abs_error(self, cond = None):
        orig, pred = self._apply_cond(self.origdef, self.preddef, cond)
        return len(pred) and sum(abs(pred - orig)) / len(pred)

    def rms_error(self, cond = None):
        orig, pred = self._apply_cond(self.origdef, self.preddef, cond)
        return len(pred) and sqrt(sum((lambda x: x*x)(pred - orig)) / len(pred))

    def coverage(self, cond = None):
        if cond is None:
            return len(self.origdef) / len(self.orig)
        undef = self.orig[cond(self.orig)]
        defnd = self.origdef[cond(self.origdef)]
        return len(undef) and 1.0 * len(defnd) / len(undef)
    
    def correct(self, cond = None):
        orig, pred = self._apply_cond(self.origdef, self.preddef, cond)
        return len(pred) and 1.0 * len(pred[pred == orig]) / len(pred)

    def has_cond(self, cond = None):
        if not cond is None:
            return len(self.pred[cond(self.pred)])
        return len(self.pred)

    def all_cond(self, cond = None):
        return [(func.__name__, func(cond)) for func in [self.has_cond, self.coverage, self.correct, self.abs_error, self.rms_error]]
    

    def cond_all_orig_levels(self):
        """This MF funktion doesn't do what it's supposed to do!"""
        vals = self.pg.dataset.level_map.values()
        vals.sort()
        print vals
        conds = [(lambda x: x == val) for val in vals]
        for c in conds:
            print c(1.0)  #ALL TRUE?!
        return conds

    def what_we_want(self):
        vals = self.pg.dataset.level_map.values()
        vals.sort()
        conds = [lambda x: x == val for val in vals]
        print conds, [l(1) for l in conds]
        return [(self.all_cond(l)) for l in
                [lambda x: True, #x == x,
                 lambda x: x == 0.4,
                 lambda x: x == 0.6,
                 lambda x: x == 0.8,
                 lambda x: x == 1.0,
                 ]
                ]
            

if __name__ == "__main__":
    import Advogato, PredGraph
    import TrustMetric, ThresholdTM
    G = Advogato.Advogato()
    pg = PredGraph.PredGraph(G, ThresholdTM.thresholder(TrustMetric.EbayTM))
    pa = PGNumAnal(pg)
    pa.what_we_want()
