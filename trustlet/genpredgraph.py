from trustlet import PredGraph, TrustMetric, PageRankTM, AdvogatoLocal
from trustlet import AdvogatoGlobalTM, AdvogatoNetwork
from trustlet.helpers import get_name
from trustlet.trustmetrics import *


def main():
    A = AdvogatoNetwork( download=True, base_path='/hardmnt/sra01/sra/salvetti' )

    trustmetrics = {
        "random_tm": TrustMetric( A , random_tm ),
        "intersection_tm":TrustMetric( A , intersection_tm ),
        "ebay_tm":TrustMetric( A , ebay_tm ),
        "edges_a_tm":TrustMetric( A , edges_a_tm ),
        "outa_tm":TrustMetric( A , outa_tm ),
        "outb_tm":TrustMetric( A , outb_tm ),
        "PageRankTM":PageRankTM(A),
        "moletrust_3":TrustMetric( A , moletrust_generator(horizon=3)),
        "moletrust_4":TrustMetric( A , moletrust_generator(horizon=4)),
        "AdvogatoLocal":AdvogatoLocal(A),
        "AdvogatoGlobalTM":AdvogatoGlobalTM(A)
        }
    
    for tm in trustmetrics:
        P = PredGraph( trustmetrics[tm] )


if __name__ == "__main__":
    main()
