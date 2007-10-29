import PredGraph
import TrustMetric
import Advogato
from helpers import get_name



def thresholder(TM_class, thr_function = 'threshold'):
    """Create new trust metric, based on old, but with thresholds."""

    class Threshold(TM_class):
        rescale = 'threshold'
        name = "thr" + TM_class.__name__

    return Threshold




                
ThrGuakeMoleTM = thresholder(TrustMetric.GuakaMoleTM)
ThrPageRankTM = thresholder(TrustMetric.PageRankTM0, 'lambda x: threshold(recur_log_rescale(x)))')

K = Advogato.Kaitiaki()

pg0 = PredGraph.PredGraph(K, ThrGuakeMoleTM)
pg1 = PredGraph.PredGraph(K, ThrPageRankTM)
