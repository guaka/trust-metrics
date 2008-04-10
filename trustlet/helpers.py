
"""Collection of random useful stuff."""
import math
import numpy
import os.path
import trustlet.TrustMetric
import trustlet.trustmetrics
from trustlet import *
#from trustlet import *
from threading import Thread
import datetime
import time
try:
    import scipy
except:
    print "no scipy"

UNDEFINED = -37 * 37  #mayby use numpy.NaN?





def hms(t_sec):
    """Convert time in seconds into Hour Minute Second format.

    >>> hms(30)
    0h0m30s
    >>> hms(100000)
    27h46m40s
    """
    t_sec = int(t_sec)
    mins, secs = divmod(t_sec, 60)
    hours, mins = divmod(mins, 60)
    return str(hours)+'h'+str(mins)+'m'+str(secs)+'s'


def est_datetime_arr(seconds):
    """Estimated datetime of arrival."""
    date = datetime.datetime.now() + datetime.timedelta(seconds = seconds)
    if seconds < 86400:
        return date.strftime("%H:%M:%S")
    return date.strftime("%H:%M:%S %A %d %B")


def get_name(obj):
    """Get name of object or class.

    >>> get_name(datetime)
    datetime
    """

    if hasattr(obj, "__name__"):
        if hasattr(obj, "name"):
            return obj.name
        return obj.__name__

    if hasattr(obj, "__class__"):
        if hasattr(obj, "get_name"):
            ret = obj.get_name()
        ret = get_name(obj.__class__)

    # se e` una classe generica, identifico il predgraph con la funzione tm
    if ret == "TrustMetric":
        if hasattr(obj, "get_tm" ):
            return obj.get_tm().__name__
        else:
            raise AttributeError
    else:
        return ret

def path_name(obj):
    """Name of the path where an object can be stored.
    
    TODO: add date."""
    if hasattr(obj, "path_name"):
        return obj.path_name
    else:
        return get_name(obj)

def mean_std(arr):
    """mean and std of array."""
    return (scipy.mean(arr), scipy.std(arr))

def threshold(arr):
    """Should use scaling here."""
    t_arr = arr.copy()
    for i, value in enumerate(arr):
        if value == UNDEFINED:
            pass
        elif value >= 0.9 and value < 1.0:
            t_arr[i] = 1.0
        elif value >= 0.7 and value < 0.9:
            t_arr[i] = 0.8
        elif value >= 0.5 and value < 0.7:
            t_arr[i] = 0.6
        elif value < 0.5:
            t_arr[i] = 0.4
    return t_arr

def thresholdPR(arr):
    """Should use scaling here."""
    arr = recur_log_rescale(arr)
    t_arr = arr.copy()
    for i, value in enumerate(arr):
        # print i,v
        if value == UNDEFINED:
            pass
        elif value > 0.8 and value < 1.0:
            t_arr[i] = 1.0
        elif value > 0.6 and value < 0.8:
            t_arr[i] = 0.8
        elif value > 0.4 and value < 0.6:
            t_arr[i] = 0.6
        elif value < 0.4:
            t_arr[i] = 0.4
    return t_arr


def rescale_array(orig_array, scale = (0, 1)):
    """Linearly rescale an array.

    >>> rescale_array(numpy.arange(3.))
    rescaling: (0.0, 2.0) to (0, 1)
    array([ 0. ,  0.5,  1. ])              
    """
    min_val, max_val = min(orig_array), max(orig_array)
    print "rescaling:", (min_val, max_val), "to", scale
    mult = (scale[1] - scale[0]) / (max_val - min_val)
    return scale[0] + (orig_array - min_val) * mult


def recf(func, num):
    """Recursivity.
    
    >>> recf(lambda x: x+1, 3)(10)
    13
    """
    if num == 1:
        return lambda x: func(x)
    else:
        return lambda x: func(recf(func, num - 1)(x))

def recur_log_rescale(arr):
    """Recursive log rescaling."""
    arr = rescale_array(arr)
    count = 0
    while scipy.mean(arr) <= 0.5 and count < 20:
        arr = numpy.log2(arr + 1)
        count += 1
    arr = rescale_array(arr, (0.4, 1.0))
    return arr
        

def indication_of_dist(arr, stepsize = 0.2):
    """Some kind of histogram-type info."""
    for start in numpy.arange(min(arr), max(arr), step = stepsize):
        print start, sum((arr >= start) * (arr < start + stepsize))

    
            
#made by Danilo Tomasoni


class BestMoletrustThreads( Thread ):
    def __init__(self, Net, horizon, l ):
        
        Thread.__init__(self)
        self.horizon = horizon
        self.ris = l #list
        
        if Net.__class__.__name__ == "KaitiakiNetwork" :
            self.K = KaitiakiNetwork(date=Net.date)
        else: 
            if Net.__class__.__name__ == "AdvogatoNetwork" :
                self.K = AdvogatoNetwork(date=Net.date)
            else:
                self.K = WeightedNetwork()

    def run(self):
        
        bestvalue = 1.0
        bestpnt = 0.0
        bestet = 0.0
        r = range(5)
        
        for pnt in r: #pred_node_trust_threshold
            for et in r: #edge_trust_treshold
                tm = trustlet.TrustMetric( self.K , 
                                           trustlet.moletrust_generator( self.horizon , float( pnt/10 ) , float( et/10 ) ) 
                                           )
                
                cnt = s = avg = 0
                
                for edge in tm.dataset.edges_iter():
                    orig_trust = tm.dataset.trust_on_edge(edge)
                    pred_trust = tm.leave_one_out(edge)
                    s = s + math.fabs( orig_trust - pred_trust )
                    cnt += 1
                    
                avg = float(s)/cnt
                    
                if avg < bestvalue:
                    bestvalue = avg
                    bestpnt = float( pnt/10 )
                    bestet = float( et/10 )
                    
        self.ris.append( (bestvalue,self.horizon,bestpnt,bestet) )
        print "Horizon ",self.horizon," calculated"
            


        
def bestMoletrustParameters( K, verbose = False, bestris = True ):
    """
    This function, print for a network passed, the best parameters
    for the moletrust_tm trustmetric
    parameters:
    network: the reference to the network
             on which you would calcolate the best parameters
    verbose: verbose mode, default false
    bestris: if true, return only the best ris, else return all the ris in this format
             (best_average_error,besthorizon,best_pred_node_trust_threshold,best_edge_trust_threshold)
    return a tuple with
    (besthorizon,best_pred_node_trust_threshold,best_edge_trust_threshold,best_average_error)
    """
    path = os.path.join(K.path, "bestMoletrustParameters" )
    #path = K.path

    try:
        fd = file( path+"bestparam", "r" )
        if bestris:
            return tuple(map( lambda x: float(x.strip()), fd.readline().split( "," )))
        
        all = []
        for i in fd.readlines():
            all.append( tuple(map(lambda x: float(x.strip()), i.split( "," ) )) )
            
        return all
    
    except IOError:
        pass

    ris = []

    #the9ull: I'd removed r = range(10)
    for h in xrange(10):
        BestMoletrustThreads(K,h,ris).start()

    #polling is better ;-)
    while( len(ris) < 10 ):
        time.sleep( 1 )


    #sort for the first value of the tuple
    ris.sort()
    fd = file( path+"bestparam", "w" )
    
    for i in xrange(10):
        (bestvalue,besthorizon,bestpnt,bestet) = ris[i]
        fd.write( ",".join([str(besthorizon),str(bestpnt),str(bestet),str(bestvalue)])+"\n" )
        
    fd.close()

    if bestris:
        (bestvalue,besthorizon,bestpnt,bestet) = ris[0]
        return (besthorizon,bestpnt,bestet,bestvalue)
    else:
        return ris


def errorTable( Network , verbose=True, sorted=False ):

    trustmetrics = {
        "intersection" : trustlet.TrustMetric( Network , trustlet.intersection_tm ),
        "edges a" : trustlet.TrustMetric( Network ,trustlet.edges_a_tm ),
        "ebay" : trustlet.TrustMetric( Network , trustlet.ebay_tm ),
        "out a" : trustlet.TrustMetric( Network , trustlet.outa_tm ),
        "out b" : trustlet.TrustMetric( Network , trustlet.outb_tm ),
        "random" : trustlet.TrustMetric( Network , trustlet.random_tm ),
        "moletrust standard" : trustlet.MoleTrustTM( Network ),
        "moletrust generator" : trustlet.TrustMetric( Network , 
                                             trustlet.moletrust_generator( 6 , 0.0 , 0.0 ) ),
        "pagerank" : trustlet.PageRankTM( Network )
        #"pagerank global": PageRankGlobalTM( K )
        }
    
    #lista delle righe della tabella
    t = []
    #numero di elementi
    cnt = 0
    tot = 0
    s = 0

    for tm in trustmetrics:
        P = trustlet.PredGraph( trustmetrics[tm] )
        """
        for edge in trustmetrics[tm].dataset.edges_iter():
            orig_trust = trustmetrics[tm].dataset.trust_on_edge(edge)
            pred_trust = trustmetrics[tm].leave_one_out(edge)
            tot += 1
            if orig_trust != pred_trust:
                s += 1
        """
        for i in range( len(P.orig_trust) ):
            if P.orig_trust[i] != P.pred_trust[i]:
                s += 1
            tot += 1
        
            
            
        #RMSE,coverage,MAE,wrong predict, trustmetric name
        t.insert(cnt,

                 (
                   (1.0 * s)/tot,
                   P.mean(),
                   P.sqr_error(),
                   P.coverage(),
                   tm
                 )

                 )


    if verbose:
        for row in t:
            print row[4], row[0], row[1], row[2], row[3]

    if sorted:
        t.sort()

    return t


def testTM( choice, singletrustm = False, verbose = False ):
    """
    This function test a single trustmetric or all the existence trustmetric, 
    on a specific network
    parameters:
    choice: the name of the network used for the test
                  possible value:
                  kaitiaki
                  dummy
                  advogato
                  squeakfoundation

    singletrustm: if false, check all the trustmetrics, else only the name of trustmetric passed
                  possible value:
                  intersection
                  edges a
                  ebay
                  out a
                  out b
                  random
                  moletrust standard
                  moletrust generator
                  pagerank

    verbose: verbose mode, true o false
    return a tuple, with the best trustmetric and it's average error 
    """

#questo e` uno switch ;-)
#assegno la network scelta alla variabile K
    K = {
        'kaitiaki': KaitiakiNetwork(date = "2008-03-20"),
        'dummy': DummyWeightedNetwork(),
        'advogato': AdvogatoNetwork(date = "2008-03-22"),
        'squeakfoundation' : SqueakFoundationNetwork( date = "2008-03-22" )
        }[choice]


    trustmetrics = {
        "intersection" : TrustMetric( K , intersection_tm ),
        "edges a" : TrustMetric( K , edges_a_tm ),
        "ebay" : TrustMetric( K , ebay_tm ),
        "out a" : TrustMetric( K , outa_tm ),
        "out b" : TrustMetric( K , outb_tm ),
        "random" : TrustMetric( K , random_tm ),
        "moletrust standard" : MoleTrustTM( K ),
        "moletrust generator" : TrustMetric( K , 
                                             moletrust_generator( 6 , 0.0 , 0.0 ) ),
        "pagerank" : PageRankTM( K )
        #"pagerank global": PageRankGlobalTM( K )
        }
    
    
    if singletrustm:
        trustmetric = {singletrustm: trustmetrics[singletrustm]}
    else:
        trustmetric = trustmetrics

#foreach trustmetric print the predicted value foreach node..
    bestname = ''
    bestvalue = 1.0

    for tm in trustmetric:
        sum = 0
        cnt = 0

        if verbose:
            print "------------- BEGIN ",tm,"--------\n"
        
        for edge in trustmetrics[tm].dataset.edges_iter():
        #valori per calcolare l'errore medio
            orig_trust = trustmetrics[tm].dataset.trust_on_edge(edge)
            pred_trust = trustmetrics[tm].leave_one_out(edge)
            sum = sum + math.fabs(orig_trust - pred_trust)
            cnt = cnt + 1
        
        #stampa la trustmetric e che arco cerca di predire
            if verbose:
                print "edge 1: ",edge[0],"edge 2: ",edge[1], '\n',"original trust: ",orig_trust,"predicted trust", pred_trust
    
            if float(sum/cnt) < bestvalue:
                bestvalue = float(sum/cnt)
                bestname = tm
        
        if verbose:
            print "average error: ", float(sum/cnt), "\n"
            print "------------- END ",tm,"--------\n"

    if verbose:
        print "+-----------------------------------------------------+"
        print "   the best trustmetric for this test is", bestname 
        print "   with the average error:", bestvalue      
        print "+-----------------------------------------------------+"
    
    return (bestname,bestvalue)
