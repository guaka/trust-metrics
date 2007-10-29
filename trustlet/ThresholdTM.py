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

"""
better done in thr_table.py!

ThrRandomTM = thresholder(TrustMetric.RandomTM)
ThrEbayTM = thresholder(TrustMetric.EbayTM)
ThrOutA_TM = thresholder(TrustMetric.OutA_TM)
ThrOutB_TM = thresholder(TrustMetric.OutB_TM)
ThrEdgesA_TM = thresholder(TrustMetric.EdgesA_TM)
ThrEdgesB_TM = thresholder(TrustMetric.EdgesB_TM)
ThrMoletrustTM_horizon2_threshold0 = thresholder(TrustMetric.MoletrustTM_horizon2_threshold0)
ThrMoletrustTM_horizon3_threshold0 = thresholder(TrustMetric.MoletrustTM_horizon3_threshold0)
ThrMoletrustTM_horizon4_threshold0 = thresholder(TrustMetric.MoletrustTM_horizon4_threshold0)
ThrAdvogatoGlobalTM = thresholder(
"""

if __name__ == "main":
    K = Advogato.Kaitiaki()
    pg0 = PredGraph.PredGraph(K, ThrGuakeMoleTM)
    pg1 = PredGraph.PredGraph(K, ThrPageRankTM)
