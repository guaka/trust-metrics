
"""Collection of random useful stuff."""
import math
import numpy
from trustlet.TrustMetric import *
from trustlet.trustmetrics import *
import trustlet
import os,sys,re
import datetime
import time
import marshal
#cache
import md5
import cPickle as pickle
from gzip import GzipFile
from socket import gethostname

try:
    import scipy
except:
    print "no scipy"

UNDEFINED = -37 * 37  #mayby use numpy.NaN?

avg = lambda l: 1.0*sum(l)/len(l)

def getTrustMetrics( net, trivial=False, advogato=True, allAdvogato=['Observer','Journeyer','Apprentice','Master']):
    """
    return all trust metric on network passed
    Parameters:
       trivial = if True, add the trivial function as always_master, always_observer...
       allAdvogatoLocalDefault = if True, and advogato is True, include AdvogatoLocalDefaultObserver/Journeyer/Master/Apprentice
       advogato = include advogato trust metrics
    """
    trustmetrics = {
        "ebay_tm":trustlet.TrustMetric( net , trustlet.ebay_tm ),
        "edges_a_tm":trustlet.TrustMetric( net , trustlet.edges_a_tm ),
        "edges_b_tm":trustlet.TrustMetric( net , trustlet.edges_b_tm ),
        "outa_tm":trustlet.TrustMetric( net , trustlet.outa_tm ),
        "outb_tm":trustlet.TrustMetric( net , trustlet.outb_tm ),
        #"PageRankTM":trustlet.PageRankTM(net),
        "moletrust_2":trustlet.TrustMetric( net , trustlet.moletrust_generator(horizon=2)),
        "moletrust_3":trustlet.TrustMetric( net , trustlet.moletrust_generator(horizon=3)),
        "moletrust_4":trustlet.TrustMetric( net , trustlet.moletrust_generator(horizon=4))
        }

    if advogato:
        trustmetrics["AdvogatoLocal"]=trustlet.AdvogatoLocal(net)
        trustmetrics["AdvogatoGlobalTM"]=trustlet.AdvogatoGlobalTM(net)
        trustmetrics["random_tm"] = trustlet.TrustMetric( net , trustlet.random_tm )

        if allAdvogato:
            levels = type(allAdvogato) is list and allAdvogato or net.level_map.keys()
            for level in levels:
                if level:
                    trustmetrics["AdvogatoLocalDefault"+level] = trustlet.AdvogatoLocal(net,level)

    else:
        trustmetrics["random_tm"] = trustlet.TrustMetric( net , trustlet.wikiRandom_tm )


    if trivial:
        trustmetrics["always_master"] = trustlet.TrustMetric( net , trustlet.always_master)
        trustmetrics["always_journeyer"] = trustlet.TrustMetric( net , trustlet.always_journeyer)
        trustmetrics["always_observer"] = trustlet.TrustMetric( net , trustlet.always_observer)
        trustmetrics["always_apprentice"] = trustlet.TrustMetric( net , trustlet.always_apprentice)
        trustmetrics["intersection_tm"] = trustlet.TrustMetric( net , trustlet.intersection_tm )
    
    return trustmetrics


def allAdvogatoPg( leaveOut = [], date = "2008-05-12" ):
    """
    return all predgraph on advogatoNetwork
    """

    A = trustlet.AdvogatoNetwork( date=date )
    tmlist = getTrustMetrics( A )
    
    for l in leaveOut:
        try:
            del tmlist[l]
        except KeyError:
            print "KeyError!", l ," not deleted"

    plist = {}
    
    for tm in tmlist:
        plist[tm] = trustlet.PredGraph( tmlist[tm] )

    return plist



def human_time(t):
    from time import gmtime #(tm_year, tm_mon, tm_mday, tm_hour, tm_min,
                            # tm_sec, tm_wday, tm_yday, tm_isdst)
    tt = gmtime(t)
    #(days,hours,mins,secs)
    return (t/24/60/60,tt[3],tt[4],tt[5])

def str_time(t):
    days,hours,mins,secs = human_time(t)
    s = []
    if days:
        s.append(str(days)+'d')
    if hours:
        s.append(str(hours)+'h')
    if mins:
        s.append(str(mins)+'m')
    s.append(str(secs)+'s')
    return ' '.join(s)

hms = str_time

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
            #if ret == 'PredGraph':
            #    ret += 'Upth'+str(obj.dataset.upthreshold)
        if hasattr(obj, "defaultPredict") and obj.defaultPredict:
            ret = get_name(obj.__class__)+'Default'+obj.defaultPredict
        else:
            ret = get_name(obj.__class__)

    # se e` una classe generica, identifico il predgraph con la funzione tm
    if ret == "TrustMetric":
        if hasattr(obj, "get_tm" ):
            if obj.get_tm().__name__ == "moletrust_tm":
                                                  #call the function with return horizon = True
                return obj.get_tm().__name__[:-2]+str( (obj.get_tm())([],[],[],rh=True) )
            else:
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
        return get_name(obj).replace('DefaultApprentice','') \
            .replace('DefaultJourneyer','') \
            .replace('DefaultMaster','') \
            .replace('DefaultObserver','') \
            .replace('DefaultFalse','')

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

#test prettyplot
if 0 and __name__=="__main__":
    if 1:
        prettyplot([("2008-01-02",34),("2008-01-05",33),("2008-01-09",34),("2008-02-15",100),("2008-09-05",2)],
                   'prova',legend='ciao',xlabel='X',ylabel='ErrORReeeee',plotnow=True,
                   histogram=True,comment='Grafico di prova')
        #prettyplot([[(0,0),(1,0.1),(2,0.2),(3,0.3)],[(0,1),(1,2),(2,3)]],'prova',showlines=True,legend=['ciao',''],xlabel='X',ylabel='ErrORReeeee',x_range=(0,13),y_range=(-5,12),plotnow=True)
    else:
        prettyplot([(0,0),(1,0),(2,0),(0,1),(1,2),(2,3)],'prova',plotnow=True)
    exit(0)


def prettyplot( data, path, **args):
    """
    Print a graphics of the list passed.
    *path* is the location in wich the script will be saved.

    *data* is ...
        a list of points
        [(x0,y0),(x1,y1),...]
    or ...
        a set of list of points
        [ [(ax0,ay0),(ax1,ay1),...] , [(bx0,by0),(bx1,by1),...] , ...]
        each list will plot on the same graph
    
    other args:
        legend='' (describes data. It is a string or a list of strings (one for each set))
        title=''
        xlabel=''
        ylabel=''
        log='' (logaritmic axis in a string, e.g. 'x' | 'y' | 'xy')
            xlogscale (float)
            ylogscale (float)
        showlines=True (old onlypoint)
        histogram=False
        x_range (from,to)
        y_range (from,to)

        plotnow=True (create png image)
        comment='' (a string to describe graph)
    """

    assert not path.endswith('.png')
    if args.has_key('istogram'):
        print '*** histogram, not istogram ;) ***'
        args['histogram'] = args['istogram']

    if path.endswith('.gnuplot'):
        path = path[:-8]

    addquotes = lambda x: '"'+str(x)+'"'

    #append
    a = lambda x: script.append(x)
    ac = lambda x: comments.append(x)

    comments = []
    script = [] #script

    try:
        a('set title "%s"'%args['title'])
        ac('Title: '+args['title'])
    except KeyError:
        pass

    ac('Date: '+time.asctime())
    
    if args.has_key('showlines') and args['showlines']:
        #a('set data style lines')
        a('set data style linespoint')
    if args.has_key('histogram') and args['histogram']:
        a('set style data boxes')
    if args.has_key('log') and args['log']:
        #set axis scales
        if args.has_key('xlogscale'):
            xscale = float(args['xlogscale'])
        else:
            xscale = 1.5
        if args.has_key('ylogscale'):
            yscale = float(args['ylogscale'])
        else:
            yscale = 1.5

        if 'x' in args['log']:
            a('set logscale x %f'%xscale )
        if 'y' in args['log']:
            a('set logscale y %f'%yscale )
    if args.has_key('xlabel'):
        a('set xlabel "%s"'%args['xlabel'])
    if args.has_key('ylabel'):
        a('set ylabel "%s"'%args['ylabel'])
    try:
        legend = args['legend']
    except:
        legend = None

    if not data:
        print "prettyplot: no input data"
        return
    #formatting data
    if type(data) is list and type(data[0]) is list and data[0] and type(data[0][0]) is tuple:
        #only one list of points
        data = [map(lambda x:(x[0],x[1]), [t for t in set if t]) for set in data]
    else:
        data = [map(lambda x:(x[0],x[1]), [t for t in data if t])]
        if legend:
            legend = [legend]

    # check if first x value is a date
    if isdate(data[0][0][0]):
        # setting format of x axis to date,
        # as in http://theochem.ki.ku.dk/on_line_docs/gnuplot/gnuplot_16.html
        a('set xdata time')
        a('set timefmt "%Y-%m-%d"')

    if args.has_key('x_range'):
        if args['x_range']:
            if isdate(args['x_range'][0]):
                assert isdate(args['x_range'][1])
                args['x_range'] = tuple(map(addquotes,args['x_range']))
            a('set xrange [%s:%s]'%args['x_range'])
    if args.has_key('y_range'):
        if args['y_range']:
            a('set yrange [%s:%s]'%args['y_range'])

    a('set terminal png')
    a('set output "%s.png"'%os.path.split(path)[1]) #to file
    outputline = 'set output "%s.png"'%path #to gnuplot
    outputindex = len(script) - 1 #line to change

    if legend:
        a('plot '+', '.join(['"-" using 1:2 title "%s"'%x for x in legend]))
    else:
        a('plot '+', '.join(['"-" using 1:2 title ""' for x in data]))

    for points in data:
        #sorting: useful with lines
        points.sort(lambda x,y:cmp(x[0],y[0]))
        for point in points:
            a(' '.join(map(str,point)))
        a('e')
        
    if args.has_key('comment'):
        if type(args['comment']) is str:
            args['comment'] = args['comment'].split('\n')
        for line in args['comment']:
            ac(line)

    f = file(path+'.gnuplot','w')
    f.writelines(['#!/usr/bin/env gnuplot\n']+
                 ['# '+x+'\n' for x in comments]+
                 ['\n'])
    f.writelines([x+'\n' for x in script])
    f.close()

    if not os.system('which gnuplot > /dev/null') and (not args.has_key('plotnow') or args['plotnow']):
        script[outputindex] = outputline #change the path of output
        gnuplot = os.popen('gnuplot','w')
        gnuplot.writelines([x+'\n' for x in script])
        gnuplot.close()

def bestMoletrustParameters( K, verbose = False, bestris=True, maxhorizon = 5, force=False, np=1 ):
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
    np: number of processes it is creating
    return a tuple with
    (best_average_error,besthorizon,best_pred_node_trust_threshold,best_edge_trust_threshold)
    or a list of tuples like this
    """

    def plot(data):
        prettyplot( map(lambda x:(x[1],x[0]), data) , path+'BestMoletrustGraphic' )
        prettyplot( map(lambda x:(x[1],x[-1]), data) , path+'BestMoletrusTimeGraphic', log=False, ylabel='time [s]', title='Time of computation' )
                
    path = os.path.join(K.path, "bestMoletrustParameters/" )
    cache_path = os.path.join( path,"cache.c2" )
    
    if not os.path.exists( path ):
        os.mkdir( path )


    maxhorizon += 1 #set maxhorizon to maxhorizon
    r = range(maxhorizon) #values of horizon
    ris = []
    pipes = []

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
                                          'et':float( et/maxhorizon )} , cache_path )
                        #yes
                        if avgsaved != None:
                            avg = avgsaved
                        #no, calcolate this and save
                        else:
                            tm = trustlet.TrustMetric( K , 
                                                       trustlet.moletrust_generator( horizon , float( pnt/maxhorizon ) , float( et/maxhorizon ) ) 
                                                       )
                
                            #cnt = s = 0
                            avg = trustlet.PredGraph( tm ).abs_error()
                            #for edge in tm.dataset.edges_iter():
                            #    orig_trust = tm.dataset.trust_on_edge(edge)
                            #    pred_trust = tm.leave_one_out(edge)
                            #    s = s + math.fabs( orig_trust - pred_trust )
                            #    cnt += 1
                    
                            #avg = float(s)/cnt
                            #save avg
                            ret = save(
                                {'func':'bestmoletrust',
                                  'horizon':horizon,
                                  'pnt':float( pnt/maxhorizon ),
                                  'et':float( et/maxhorizon )},
                                 
                                avg, 
                                cache_path
                                )
                            if not ret:
                                print "Warning! i cannot be able to save this computation, check the permission"
                                print "for the "+cache_path+"path"
                            
                    
                        if avg < bestvalue:
                            bestvalue = avg
                            bestpnt = float( pnt/maxhorizon )
                            bestet = float( et/maxhorizon )
                
                os.write(write,",".join((str(bestvalue),str(horizon),str(bestpnt),str(bestet),str(time.time()-t)))+"|")
                print "Horizon ",horizon," calculated"
            os.close(write)
            #return #son dies
            #print "pipe closed"
            os._exit(0)
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
    fd = file( os.path.join( path,"bestparam" ), "w" )
    
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
        #"pagerank" : trustlet.PageRankTM( Network )
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
        
        for i in xrange( len(P.orig_trust) ):
            if round(P.orig_trust[i],1) != round(P.pred_trust[i],1):
                s += 1
            tot += 1
        
            
            
        #wrong predict,MAE,coverage,RMSE, trustmetric name
        if cond == False:
            t.insert(cnt,

                    (
                    (1.0 * s)/tot,
                    P.abs_error(),
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


def testTM( net, bpath=None, np=None, onlybest=False, plot = False ):
    """
    This function test a single trust metric or all the trust metrics, 
    on a specific network
    
    parameters:
    net: the network on wich calculate the errors
    plot: plot or not an istogram with the results. 
          It works only if onlybest is set to false
    np: number of processors
    bpath: the path in witch there are the predgraph dot

    return a tuple, with the best trustmetric and it's average error, or if
    onlybest is set to False, all the trustmetric with his own MAE
    """
    
    lris = [] # list of results (performances), one for each trust metric evaluated

    if bpath == None:
        bpath = net.path

    path = os.path.join(bpath,'TestTrustMetrics')
    if not os.path.exists(path):
        os.mkdir(path)

        #for each trust metric, print the predicted value for each edge
    nname = get_name( net )
    print "Retrieving all the trust metrics avaiable for this network..."
    
    if 'Advogato' in nname or 'Kaitiaki' in nname or 'Squeakfoundation' in nname or 'Robots_net' in nname:
        trustmetrics = getTrustMetrics( net, allAdvogato=net.level_map.keys() )
    else:
        trustmetrics = getTrustMetrics( net, advogato=False )
	#parameters:
	#path is the path on which to save the computation
	#tm is the trustMetric class 
	#tmname is the trust metric name, 
        #predgraph                                      
    def eval( (path,tm) ):
            #tm = current tm

        sum = 0
        cnt = 0
        abs = load( {'tm':tm},os.path.join( path,'cache.c2' ) )
        
        if abs != None:
            error = abs
        else:
            error = trustlet.PredGraph( trustmetrics[tm] ).abs_error()
        
            save({'tm':tm},error,os.path.join( path,'cache.c2' ) )
                    
        return ( error, tm )

    # we use splittask so that we can split the computation in
    # parallel across different processors (splittask is defined
    # in helpers.py). Neet to check how much this is efficient or needed.
    print "Evaluating...."
    lris = splittask( eval , [(path,tm) for tm in trustmetrics], np ) 

    if onlybest:
        lris.sort()
        return lris[0]
    else:
        if plot:    
            prettyplot( [x for x in enumerate([x for (x,s) in lris])], os.path.join( path,'TrustMetricsHistogram' ), 
                        title = 'MAE for each trustmetric on '+get_name(net)+' network',
                        xlabel='trust metrics',
                        ylabel='MAE',
                        histogram = True )
            
        fd = file( os.path.join( path,'HistogramLegend' ), 'w' )
        fd.write( '\n'.join( [str(n)+': '+s for (n,s) in enumerate([y+' '+str(x) for (x,y) in lris])] ) )
        fd.close()
        
        lris.sort()

        return lris

def tempnam():
    '''soppress warning'''
    stderr = sys.stderr
    sys.stderr = file('/dev/null','w')
    name = os.tempnam()
    sys.stderr = stderr
    return name

def getnp():
    """Return None or the number of processors"""
    try:
        return len([None for x in file('/proc/cpuinfo').readlines() if x.startswith('processor')])
    except IOError:
        return None

def splittask(function,input,np=None):
    """
    create <np> processes with <input>[i] data,
    the result will return in a list.

    splittask(function,input) is equivalent to [function(x) for x in input]
    """

    if not np:
        np = getnp()
        if not np:
            np = 4

    result = []
    pipes = []

    if np==1:
        #doesn't create other processes
        return [function(x) for x in input]

    for proc in xrange(np):
        read,write = os.pipe()
        pinput = map(lambda x: input[x],xrange(proc,len(input),np))
        #print 'pinput',pinput
        if os.fork()==0:
            #son
            res = []
            for data in pinput:
                res.append(function(data))
            os.write(write,marshal.dumps(res))
            os.close(write)
            #sys.exit() # ipython trap this -_-
            os._exit(0) # ipython DOESN'T trap this ^_^
        else:
            #save pipe
            pipes.append(read)
            os.close(write)

    #wait responce from sons
    try:
        for pipe in pipes:
            buffer = '_'
            s = ''
            while buffer:
                buffer = os.read(pipe,1000)
                s += buffer
            result += marshal.loads(s)
    except EOFError:
        print "A son process is dead"
        print "splittask says: it's not my fault!"
        exit(1)

    return result

"""data: output of pred_graph.cont_num_of_edges()"""
plot_cont_num_of_edges = lambda data,indegree,dirpath='.': \
    prettylot(data,os.path.join(dirpath,'controv num of edges (indegree=%d).png'%indegree),
               title='Number of edges by controversiality (indegree=%d)'%indegree,
               xlabel='controversiality',
               ylabel='# edges',
               showlines=True)

plot_cont_type_of_edges = lambda data,indegree,dirpath='.',no_observer=False: \
    prettyplot(data,os.path.join(dirpath,'controv type of edges (indegree=%d%s).png'%(indegree,(no_observer and ' no observer' or ''))),
                                 title='Type of edges by controversiality (indegree=%d%s)'%(indegree,(no_observer and ' no observer' or '')),
                                 xlabel='controversiality',
                                 ylabel='% edges',
                                 legend=['master','journeyer','apprentice'] + (no_observer and [] or ['observer']),
                                 x_range=(0.0,0.38),
                                 showlines=True)
               
def plot_cont_graphs(pg, dirpath='.', numbers=None):
    def fix_conttypeofedges_data(d,no_observer=False):
        """
        d: [(cont, master, journeyer, apprentice, observer), ... ]
        output: [(cont, master), (cont,journeyer), ...]
        """
        if no_observer:
            cut = lambda t: t[1:-1]
        else:
            cut = lambda t: t[1:]
        def perc(t):
            s = sum(t)
            if s:
                return [1.0*x/s for x in t]
            else:
                return [0.0 for x in t]
        return (lambda x: no_observer and x[:3] or x)([
            [(x[0],perc(cut(x))[0]) for x in d],
            [(x[0],perc(cut(x))[1]) for x in d],
            [(x[0],perc(cut(x))[2]) for x in d],
            [(x[0],perc(cut(x))[-1]) for x in d], # this value is wrong if no_observer, but it will cut
            ])
    
    mkpath(dirpath)
    if not numbers:
        numbers = [1,3,5,10,15,20,50,100]
    for i in numbers:
        plot_cont_num_of_edges( pg.cont_num_of_edges(number=i), i, dirpath )
        plot_cont_type_of_edges( fix_conttypeofedges_data(pg.cont_type_of_edges(number=i)),
                                 i, dirpath )
        plot_cont_type_of_edges( fix_conttypeofedges_data(pg.cont_type_of_edges(number=i),no_observer=True),
                                 i, dirpath, no_observer=True )

if False:
    pg = PredGraph(TrustMetric(AdvogatoNetwork(date='2008-05-12'),ebay_tm))
    values = []
    plot_cont_num_of_edges( plot_cont_num_of_edges( pg.cont_num_of_edges(values=values) ))

def xfloatrange(*args):
    """xfloatrange([start,] stop[, step]) -> list of floatss (like xrange)"""
    if len(args)==1:
        start = 0.0
        end = args[0]
        step = 1.0
    elif len(args)==2:
        start = args[0]
        end = args[1]
        step = 1.0
    elif len(args)==3:
        start,end,step = args
    else:
        assert 0
    while(start<=end):
        yield float(start)
        start += step

floatrange = lambda *args: [x for x in xfloatrange(*args)]

def mkpath(fullpath):
    """
    makes all missed directory of a path
    """
    if not fullpath: return
    if fullpath[-1] == os.path.sep:
        fullpath = fullpath[:-1]
    if fullpath and not os.path.exists(fullpath):
        path = os.path.split(fullpath)[0]
        mkpath(path)
        os.mkdir(fullpath)

redate = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
isdate = lambda x: bool(re.match(redate,str(x)))
remd5 = re.compile('^[0-9a-fA-F]{32}$')
ismd5 = lambda x: bool(re.match(remd5,x))
reip = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
                  '(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
isip = lambda x: bool(re.match(reip,x))

class Progress:
    '''
    print percentage of done work
    '''
    def __init__(self,total,roundval=0,description=''):
        '''
        roundval: number of significant digits
        description: will be printed before percentage
        '''
        self.desc = description
        self.roundval = roundval
        self.print_format = '%.'+str(roundval)+'f%%'
        if description:
            self.print_format = description + ' ' + self.print_format
        self.total = total
        self.last_print = ''
        
    def __call__(self,done_work):
        val = round(100.0 * done_work / self.total, self.roundval)
        if val != self.last_print:
            self.last_print = val
            print self.print_format % val

def getfiles(basedir,dir=''):
    join = os.path.join
    curpath = join(basedir,dir)
    ret = []
    for f in os.listdir(curpath):
        if os.path.isdir(join(curpath,f)):
            ret += getfiles(basedir,join(dir,f))
        else:
            ret.append(join(dir,f))
    return ret

# == cache ==
# save and restore data into/from cache
# - `key` is a dictionary
# - `data` can be anything (i hope)

def get_sign(key,mdfive=True):
    """
    Cache.
    Generate an unique key given a dictionary.
    If mdfive is True it will return an alphanumeric
    key of 32 chars
    """
    s = ''
    listkeys = key.keys()
    listkeys.sort()
    for k in listkeys:
        s+=str(k)+'='+str(key[k])+','
    if mdfive:
        return md5.new(s[:-1]).hexdigest()
    else:
        return s[:-1]

def hashable(x):
    """
    Cache.
    Return an hashable object that can be used as key in dictionary cache.
    """
    if type(x) in (str,tuple,frozenset,int,float):
        return x
    if type(x) is list:
        return (list,)+tuple(x)
    if type(x) is set:
        return frozenset(x)
    if type(x) is dict:
        tupleslist = []
        for k,v in x.iteritems():
            tupleslist.append( (k,v) )
        return frozenset(tupleslist)

    raise TypeError,"I don't know this type"

def save(key,data,path='.',human=False,version=3):
    """
    Cache.
    It stores some *data*  identified by *key* into a file in *path*.
    If human=True it will save another file in plain text for human beings.
    DEPRECATED: You can set *time* (integer, in seconds) to indicate the
    time of computation.
    If path ends with '.c2' data will save in the new format (less files).
    human is not suported in the new format.
    """

    def lock():
        TIMEOUT = 300 # 5min
        def readall(fname):
            try:
                f = file(fname)
                data = f.read()
                f.close()
            except:
                data = ''
            return data or '0.0'
        def writeall(fname,data):
            f = file(fname,'w')
            f.write(data)
            f.close()
        while True:
            if not os.path.isfile(path+'.lock') or time.time()-float(readall(path+'.lock'))>TIMEOUT:
                writeall(path+'.lock',str(time.time()))
                return

            time.sleep(1)

    def unlock():
        try:
            os.remove(path+'.lock')
        except OSError:
            pass

    if path.endswith('.c2'):
        mkpath(os.path.split(path)[0])
        lock()
        try:
            # I can't use cachedcache because data might be obsolete.
            d = pickle.load(GzipFile(path))
        except:
            d = {}
        #new version
        if version==3:
            # yet beta
            gen_key = hashable
        else:
            gen_key = get_sign

        d[gen_key(key)] = data
        pickle.dump(d,GzipFile(path,'w'))
        unlock()

        #memory cache
        if not globals().has_key('cachedcache'):
            #print 'create cache'
            globals()['cachedcache'] = {}
        cache = globals()['cachedcache']
        cache[path] = d
    else:
        #version 1
        print "WARNING: don't use this cache version!"
        print "Add .c2 in path"
        mkpath(path)
        try:
            if human:
                f = file(os.path.join(path,get_sign(key,False)),'w')
                f.writelines([str(x)[:100]+'='+str(key[x])[:100]+'\n' for x in key])
                if type(human) is str:
                    f.write('comment: '+human)
                f.write('data: '+str(data))

            f = file(os.path.join(path,get_sign(key)),'w')
            pickle.dump(data,f)
            f.close()
        except IOError,pickle.PicklingError: #,TypeError: # I' can't catch TypeError O.o why?
            print 'picking error'
            return False
    return True
    
def load(key,path='.',fault=None):
    """
    Cache.
    Loads data stored by save.
    fault is the value returned if key is not stored in cache.
    """

    if os.path.isdir(path):
        try:
            data = pickle.load(file(os.path.join(path,get_sign(key))))
        except:
            return fault
    elif os.path.isfile(path):
        #memory cache
        if not globals().has_key('cachedcache'):
            #print 'create cache'
            globals()['cachedcache'] = {}
        cache = globals()['cachedcache']

        if cache.has_key(path):
            #print 'found',path
            if cache[path].has_key(get_sign(key)):
                #version 2
                return cache[path][get_sign(key)]
            elif cache[path].has_key(hashable(key)):
                #version 3
                return cache[path][hashable(key)]
            else:
                return fault
        
        try:
            d = pickle.load(GzipFile(path))
        except:
            return fault
        
        if d.has_key(get_sign(key)):
            #version 2
            data = d[get_sign(key)]
        elif d.has_key(hashable(key)):
            #version 3
            data = d[hashable(key)]
        else:
            return fault

        #save in memory cache
        cache[path] = d
    else:
        return fault

    return data

def erase_cachedcache():
    '''
    useful to reload cache from disc
    * doesn't work *
    '''
    globals()['cachedcache'] = {}

def convert_cache(path1,path2):
    '''
    from version 1 to 2
    * this function doesn't work *
    '''
    join = os.path.join
    oldcache = [(x,pickle.load(file(join(path1,x)))) \
                    for x in os.listdir(path1) if ismd5(x) and os.path.isfile(join(path1,x))]
    newcache = {}
    for k,v in oldcache:
        newcache[k] = v
    pickle.dump(newcache,GzipFile(path2,'w'))

def merge_cache(path1,path2):
    c1 = pickle.load(GzipFile(path1))
    c2 = pickle.load(GzipFile(path2))
    c1.update(c2)
    pickle.dump(c1,GzipFile(path1+'+'+os.path.split(path2)[1],'w'))

def read_c2(path):
    '''return all cache dictionary'''
    return pickle.load(GzipFile(path))

def cached_read_dot(filepath,force=False):
    '''
    If graph had been read yet this function avoid to reload it from file system.
    This function can load bz2 compressed dot
    '''
    if not globals().has_key('globalgraphscache'):
        globals()['globalgraphscache'] = {}
    cache = globals()['globalgraphscache']

    if cache.has_key(filepath) and not force:
        return cache[filepath]

    from networkx import read_dot
    
    if os.path.exists(filepath+'.bz2') and not os.path.exists(filepath):
        tmppath = tempnam()
        f = file(tmppath,'w')
        try:
            from bz2 import BZ2File
            f.write(BZ2File(filepath+'.bz2').read())
            f.close()
        except ImportError:
            os.system('bzcat "%s" > "%s"' % (filepath,tmppath))
        cache[filepath] = read_dot(tmppath)
    else:
        cache[filepath] = read_dot(filepath)

    return cache[filepath]

def relative_path( path, folder ):
    """
    split a path relatively to the passed folder
    es.
    
    In: relative_path( '/home/ciropom/Scrivania' , 'ciropom' )
    Out: ('/home','Scrivania/')
    """
    toadd = ''; relpathlist = [] ; relpath = ''

    while( os.path.split( path )[1] != folder ):
        path,toadd = os.path.split( path )
        relpathlist.append( toadd )

    relpathlist.reverse()
        
    for i in relpathlist:
        relpath = os.path.join( relpath, i )
        
    return (path,relpath)


def getNetworkList( datasetPath ):
    """
    get a list of network avaiable on www.trustlet.org
    Parameters:
       datasetPath = path in wich is located your datasets directory (maybe in the home directory)
    
    NB: this function use the internet connection. If you haven't an internet connection enabled
        you cannot use it.
    """
    path = os.path.realpath( datasetPath )
    
    os.chdir( path )

    name = tempnam()
    
    if os.system( 'svn list -R > '+name ) != 0:
        print "svn error! check your internet connection"
        return None
    
    fd = file( name )
    lines = fd.readlines()
    paths = []
    fd.close()
    
    os.remove( name )

    for line in lines:
        sline = line.strip()
        if sline[-1] == '/':
            sline = sline[0:-1] #remove /
        
        while sline != '':
            if os.path.isdir( sline ):
                if sline not in paths:
                    paths.append( sline )
                break
            else:
                sline = os.path.split( sline )[0]

    return paths

def pool(o,poolname='generic'):
    '''
    This function is useful to save memory if `o' is a
    read-only and mutability object.
    If `o' is in pool, this function return it without
    waste memory.
    poolname is the pool to use.
    '''
    poolname = 'pool_'+poolname
    if not globals().has_key(poolname):
        globals()[poolname] = {}
    pool = globals()[poolname]
    key = hashable(o)
    
    if key in pool:
        return pool[key]
    pool[key] = o
    return o
    
if __name__=="__main__":
    from trustlet import *
    #test pool
    q = {1:2,2:2,3:2}
    w = {1:2,2:2,3:2}
    e = {1:2,2:2,3:2}
    r = {1:1,2:1,3:1}
    t = {1:3,2:3,3:3}

    l = []
    l.append(pool(q))
    l.append(pool(w))
    l.append(pool(e))
    l.append(pool(r))
    l.append(pool(t))

    t['qweqwe'] = 1

    print l
