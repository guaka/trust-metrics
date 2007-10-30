import PredGraph
import TrustMetric
import Advogato
from helpers import get_name



def thresholder(TM_class, thr_function = 'threshold'):
    """Create new trust metric, based on old, but with thresholds."""

    class Threshold(TM_class):
        rescale = 'threshold'
        # not even: name = TM_class.__name__
        name = TM_class.__name__

    return Threshold


ThrGuakeMoleTM = thresholder(TrustMetric.GuakaMoleTM)
ThrPageRankTM = thresholder(TrustMetric.PageRankTM0, 'thresholdPR')


if __name__ == "__main__":
    G = Advogato.Advogato()
    pg0 = PredGraph.PredGraph(G, ThrGuakeMoleTM)
    # pg1 = PredGraph.PredGraph(G, ThrPageRankTM)
