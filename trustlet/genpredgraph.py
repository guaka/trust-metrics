from trustlet import *
#from trustlet import PredGraph, AdvogatoNetwork
#from trustlet.helpers import get_name, getTrustMetrics, splittask
#from trustlet.trustmetrics import *


def main(path):
    A = AdvogatoNetwork( download=True, base_path=path )

    trustmetrics = getTrustMetrics( A )

    def eval( tm ):
        P = PredGraph( trustmetrics[tm] )
        return None
    
    splittask( eval , [tm for tm in trustmetrics], np=4 )
    
    return None


if __name__ == "__main__":
    #import sys
    #path = sys.argv[1:]
    #'/hardmnt/sra01/sra/salvetti'
    main(None)
