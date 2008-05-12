from trustlet import PredGraph, TrustMetric, PageRankTM, AdvogatoLocal
from trustlet import AdvogatoGlobalTM, AdvogatoNetwork
from trustlet.helpers import get_name, getTrustMetrics
from trustlet.trustmetrics import *


def main():
    A = AdvogatoNetwork( download=True, base_path='/hardmnt/sra01/sra/salvetti' )

    trustmetrics = getTrustMetrics( A )

    for tm in trustmetrics:
        P = PredGraph( trustmetrics[tm] )


if __name__ == "__main__":
    main()
