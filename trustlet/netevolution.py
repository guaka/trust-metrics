"""
This package contains all the function 
on the evolution of a network
"""

from trustlet import *
from trustlet.Advogato
from networkx import read_dot
import os,time,re

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
        at = load( {'function':'trustAverage', 'date':d}, os.path.join(path,d) )
        if at != None:
            return (stringtime2int(d),at)

        #temporary path
        tpath = os.path.join( path, d )
        N = Network.WeightedNetwork()
        N.paste_graph( networkx.read_dot( os.path.join( tpath, 'graph.dot' ) ) )
        #can be advogato/kaitiaki style, or directly with a integer weights
        weight = N.weights()
        
        try:
            averagetrust = avg([_obs_app_jour_mas_map[val] for val in [x.values() for x in weight]])
        except KeyError:
            try:
                averagetrust = avg([_color_map[val] for val in [x.values() for x in weight]])
            except KeyError:
                averagetrust = avg([val for val in [x.values() for x in weight]])

        save( {'function':'trustAverage', 'date':d}, averagetrust ,os.path.join(path,d) )
        return (stringtime2int(d),averagetrust)
        
    return splittask( eval, fdate )

def usersgrown(path,range=None):
    '''
    return the number of user for each network in date range
    '''
    redate = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
    dates = [x for x in os.listdir(path) if re.match(redate,x)]

    if range:
        dates = [x for x in dates if x>=range[0] and x<=range[1]]

    #print dates

    def eval(date):
        print date
        #cache
        nnodes = load({'function':'usersgrown','date':date},path=os.path.join(path,'cache'))
        if nnodes:
            return ( stringtime2int(date), nnodes )
        
        t=time.time()
        G = read_dot(os.path.join(os.path.join(path,date),'graph.dot'))
        K = Network.WeightedNetwork(make_base_path=False,from_graph=G)
        nnodes = len(K.nodes())
        save({'function':'usersgrown','date':date},nnodes,time=time.time()-t,human=True,path=os.path.join(path,'cache'))
        return ( stringtime2int(date), nnodes )

    #return [eval(x) for x in dates]
    return splittask(eval,dates)


if __name__ == "__main__":

    print trustAverage( "2000-01-01", "2005-01-01", "/home/ciropom/datasets/AdvogatoNetwork" )
