"""
This package contains all the function 
on the evolution of a network
"""

from trustlet import *
from networkx import read_dot
import os

stringtime2int = lambda s: int(time.mktime( (int(s[:4]), int(s[5:7]), int(s[8:10]), 0, 0, 0, 0, 0, 0) ))

def trustAverage( fromdate, todate, path ):
    """
    This function evaluate the trust average on more than one datasets.
    If you evaluate twice the same thing, the evaluate 
    function be able to remember it.
    
    Parameters:
    fromdate: initial date
    todate: finishdate
    path: path in wich I can find the network
          ex. /home/ciropom/datasets/AdvogatoNetwork
    """
    try:
        lsdate = os.listdir( path )
    except OSError:
        return None
    
    avg = lambda ls:float(sum(ls))/len(ls)
    #filtered date
    fdate = [x for x in lsdate if (fromdate <= x) and (x <= todate)]

    def eval( d ):
    #for d in fdate:
        #temporary path
        tpath = os.path.join( path, d )
        N = Network.WeightedNetwork( from_graph=networkx.read_dot( os.path.join( tpath, 'graph.dot' ) ) , make_base_path = False )
        #can be advogato/kaitiaki style, or directly with a integer weights 
        try:
            averagetrust = avg([_obs_app_jour_mas_map[val] for val in N.weights().keys()])
        except KeyError:
            try:
                averagetrust = avg([_color_map[val] for val in N.weights().keys()])
            except KeyError:
                averagetrust = avg([val for val in N.weights().values()])
                     
        return (stringtime2int(d),averagetrust)
        
    return splittask( eval, fdate )


if __name__ == "__main__":

    print trustAverage( "2000-01-01", "2005-01-01", "/home/ciropom/datasets/AdvogatoNetwork" )
