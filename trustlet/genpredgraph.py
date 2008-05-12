from trustlet.helpers import get_name, getTrustMetrics, splittask
from trustlet.trustmetrics import *


def main():
    A = AdvogatoNetwork( download=True, base_path='/hardmnt/sra01/sra/salvetti' )

    trustmetrics = getTrustMetrics( A )

    def eval( tm ):
        P = PredGraph( trustmetrics[tm] )
        return None
    
    splittask( eval , [tm for tm in trustmetrics], np=4 )
    
    return None


if __name__ == "__main__":
    main()
