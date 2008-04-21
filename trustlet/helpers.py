
"""Collection of random useful stuff."""
import math
import numpy
import os.path
import trustlet.TrustMetric
import trustlet.trustmetrics
import Gnuplot
import os,sys
import datetime
import time
#cache
import md5
import pickle

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

def plotparameters( tuplelist, path, onlyshow=False, title='Moletrust Accuracy', xlabel='horizon', ylabel='abs error', log=False, onlypoint=False ):
    """
    Print a graphics of the list passed.
    path is the location in wich the png image will be saved,
    if you wouldn't save it, set the onlyshow parameter to True
    title parameter, set the title of the plot
    """
    g = Gnuplot.Gnuplot()
    g.title( title )
    if onlypoint:
        g('set parametric')
    else:
        g('set data style lines')
    if log:
        g('set logscale y 1.5' )
    g.xlabel( xlabel )
    g.ylabel( ylabel )
    #first place horizon, sencond place abs error (converted in float)
    points = map(lambda x:(float(x[0]),float(x[1])), tuplelist)
    points.sort()
    g.plot( points )
    if not onlyshow:
        g.hardcopy(
            filename=path,
            terminal='png'
            )
    
    return None

#this function *doesn't work* with ipython
#(because it traps sys.exit())
def bestMoletrustParameters( K, verbose = False, bestris=True, maxhorizon = 5, force=False ):
    """
    This function, print for a network passed, the best parameters
    for the moletrust_tm trustmetric
    parameters:
    K: the reference to the network
       on which you would calcolate the best parameters
    verbose: verbose mode, default false
    bestris: return only the best 
    maxhorizon: test horizons from 0 to maxhorizon,
                NB: if the result was already stored only this
                    was returned. If you want recalculate, set
                    force=True
    force: don't load precomputed result
    return a tuple with
    (best_average_error,besthorizon,best_pred_node_trust_threshold,best_edge_trust_threshold)
    or a list of tuples like this
    """

    def plot(data):
        plotparameters( map(lambda x:(x[1],x[0]), data) , path+'BestMoletrustGraphic.png' )
        plotparameters( map(lambda x:(x[1],x[-1]), data) , path+'BestMoletrusTimeGraphic.png', log=False, ylabel='time [s]', title='Time of computation' )
                

    path = os.path.join(K.path, "bestMoletrustParameters/" )
    
    if not os.path.exists( path ):
        os.mkdir( path )


    maxhorizon += 1 #set maxhorizon to maxhorizon
    r = range(maxhorizon) #values of horizon
    ris = []
    pipes = []
    np = 2 #number of processes

    for proc in xrange(np):
        read,write = os.pipe()
        horizones = range(proc,len(r),np)
        if os.fork()==0:
            #son

            for horizon in horizones:
                
                t = time.time()
                bestvalue = 1.0
                bestpnt = 0.0
                bestet = 0.0
                for pnt in r: #pred_node_trust_threshold
                    for et in r: #edge_trust_treshold
                        #there are saved values?
                        avgsaved = load( {'func':'bestmoletrust',
                                          'horizon':horizon,
                                          'pnt':float( pnt/maxhorizon ),
                                          'et':float( et/maxhorizon )} , path+"/cache" )
                        #yes
                        if avgsaved != None:
                            avg = avgsaved
                        #no, calcolate this and save
                        else:
                            tm = trustlet.TrustMetric( K , 
                                                       trustlet.moletrust_generator( horizon , float( pnt/maxhorizon ) , float( et/maxhorizon ) ) 
                                                       )
                
                            cnt = s = 0
                
                            for edge in tm.dataset.edges_iter():
                                orig_trust = tm.dataset.trust_on_edge(edge)
                                pred_trust = tm.leave_one_out(edge)
                                s = s + math.fabs( orig_trust - pred_trust )
                                cnt += 1
                    
                            avg = float(s)/cnt
                            #save avg
                            ret = save(
                                {'func':'bestmoletrust',
                                  'horizon':horizon,
                                  'pnt':float( pnt/maxhorizon ),
                                  'et':float( et/maxhorizon )},
                                 
                                avg, 
                                path+"/cache"
                                )
                            if not ret:
                                print "Warning! i cannot be able to save this computation, check the permission"
                                print "for the "+path+"/cache"+"path"
                            
                    
                        if avg < bestvalue:
                            bestvalue = avg
                            bestpnt = float( pnt/maxhorizon )
                            bestet = float( et/maxhorizon )
                
                os.write(write,",".join((str(bestvalue),str(horizon),str(bestpnt),str(bestet),str(time.time()-t)))+"|")
                print "Horizon ",horizon," calculated"
            os.close(write)
            #return #son dies
            #print "pipe closed"
            sys.exit() # ipython trap this -_-
        else:
            #save pipe
            pipes.append((read,len(horizones)))

    #wait responce from sons
    for pipe,n in pipes:
        #when I wrote that I hadn't know how to works pipes
        s = ''
        #counts the |s
        while s.count('|')<n:
            s += os.read(pipe,100)
        os.close(pipe)
        s = s[:-1] # |
        for i in s.split("|"):
            ris.append(tuple(i.split(",")))

    #sort for the first value of the tuple
    ris.sort()
    fd = file( path+"bestparam", "w" )
    
    #writes on file computed values
    for i in xrange(maxhorizon):
        fd.write( ",".join([str(x) for x in ris[i]])+"\n" )
    fd.close()

    plot(ris)

    #converts strings in floats
    ris = [tuple(map(float,tt)) for tt in ris]

    if bestris:
        return ris[0]
    else:
        return ris



def errorTable( Network , verbose=True, sorted=False, cond=False ):
    """
    return for each trustmetric evaluated on the network passed this values:
    wrong predict,MAE,coverage,RMSE, trustmetric name
    it is a function to see how much powerful is a trustmetric
    parameters:
       Network: the network on which are calculated the trustmetric
       verbose: print comment, and the result on standard output
       sorted: sort the result, for the first value on the tuple (wrong predict)
       cond: function that take two parameters (network and edge). It's used to choose
             which edge to include
    """


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
        
        for i in range( len(P.orig_trust) ):
            if round(P.orig_trust[i],1) != round(P.pred_trust[i],1):
                s += 1
            tot += 1
        
            
            
        #wrong predict,MAE,coverage,RMSE, trustmetric name
        if cond == False:
            t.insert(cnt,

                    (
                    (1.0 * s)/tot,
                    P.testTM(),
                    P.sqr_error(),
                    P.coverage(),
                    tm
                    )
                     
                     )
        else:
            t.insert(cnt,

                    (
                    (1.0 * s)/tot,
                    P.abs_error_cond(cond),
                    P.root_mean_squared_error_cond(cond),
                    P.coverage_cond(cond),
                    tm
                    )
                     
                     )
        cnt += 1


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


def splittask(function,input,np=2):
    """
    create <np> processes with <input>[i] data,
    the result will return in a list
    """

    ris = []
    pipes = []

    for proc in xrange(np):
        read,write = os.pipe()
        pinput = map(lambda x: input[x],xrange(proc,len(input),np))
        if os.fork()==0:
            #son
            res = []
            for data in pinput:
                res.append(function(data))
            os.write(write,pickle.dumps(res))
            os.close(write)
            #sys.exit() # ipython trap this -_-
            os._exit(0) # ipython DOESN'T trap this ^_^
        else:
            #save pipe
            pipes.append(read)
            os.close(write)

    #wait responce from sons
    ris = []
    for pipe in pipes:
        buffer = '_'
        s = ''
        while buffer:
            buffer = os.read(pipe,100)
            s += buffer
        ris += pickle.loads(s)

    return ris

# == cache ==
# save and restore data into/from cache
# - `key` is a dictionary
# - `data` can be anything (i hope)

def mkpath(fullpath):
    if not fullpath: return
    if not os.path.exists(fullpath):
        path = os.path.split(fullpath)[0]
        mkpath(path)
        os.mkdir(fullpath)

def get_sign(key):
    s = ''
    listkeys = key.keys()
    listkeys.sort()
    for k in listkeys:
        s+=str(k)+'='+str(key[k])+','
    return md5.new(s[:-1]).hexdigest()

def save(key,data,path='.',savekey=False):
    mkpath(path)
    try:
        pickle.dump(data,file(os.path.join(path,get_sign(key)),'w'))
        if savekey:
            file(os.path.join(path,get_sign(key))+'.key','w').writelines([str(x)[:100]+'='+str(key[x])[:100]+'\n' for x in key])
    except IOError,UnpickingError:
        return False
    return True
    
def load(key,path='.'):
    try:
        return pickle.load(file(os.path.join(path,get_sign(key))))
    except IOError:
        return None

def clear(key,path='.'):
    fullpath = os.path.join(path,get_sign(key))
    os.remove(fullpath)
    if os.path.exists(fullpath+'.key'):
        os.remove(fullpath+'.key')

if __name__=="__main__":
    #from trustlet import *
    #from pprint import pprint
    #k = KaitiakiNetwork(download=True)
    #pprint(bestMoletrustParameters(k,bestris=False,force=False,maxhorizon=10))
    
    print len(splittask(float,range(10)))

