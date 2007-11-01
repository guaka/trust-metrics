import PredGraph
import TrustMetric
import Advogato
from helpers import get_name



def thresholder(TM_class, thr_function = 'threshold'):
    """Create new trust metric, based on old, but with thresholds."""

    class Threshold(TM_class):
        rescale = thr_function
        # not even: name = TM_class.__name__

        name = "Thresh" + TM_class.__name__
        path_name = TM_class.__name__
        
    return Threshold


if __name__ == "__main__":
    G = Advogato.Advogato()
    # pg0 = PredGraph.PredGraph(G, ThrGuakeMoleTM)
    pg = PredGraph.PredGraph(G, thresholder(TrustMetric.PageRankGlobalTM, 'thresholdPR'))
