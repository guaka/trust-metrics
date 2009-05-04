# -*- coding: utf-8 -*-

"""Collection of random useful stuff."""
import math
import sys
import numpy
from trustlet.TrustMetric import *
from trustlet.trustmetrics import *
from trustlet.Dataset.Network import *
from trustlet.Dataset.Advogato import *
from trustlet.Dataset.Dummy import *
import trustlet
import os,re
import datetime
import time
import marshal
import threading
#cache
import re
from hashlib import md5
import cPickle as pickle
from gzip import GzipFile
from socket import gethostname

try:
    import scipy
except:
    print "no scipy"

UNDEFINED = -37 * 37  #mayby use numpy.NaN?

avg = lambda l: 1.0*sum(l)/len(l)
mtime = lambda f: int(os.stat(f).st_mtime)


def getTrustMetrics( net, trivial=False, advogato=True, allAdvogato=None):
    """
    return all trust metric on network passed
    Parameters:
       trivial = if True, add the trivial function as always_master,
       always_observer...
       allAdvogatoLocalDefault = if True, and advogato is True, include
       AdvogatoLocalDefaultObserver/Journeyer/Master/Apprentice
       advogato = include advogato trust metrics
    """

    if allAdvogato:
        print "Warning! obsolete parameter alladvogato"

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

        if hasattr( net, "level_map" ):
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
    exit()


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

    mkpath(os.path.split(path)[0])

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
        if not data or not data[0]:
            print "prettyplot: no input data"
            return
        if legend:
            legend = [legend]

    # check if first x value is a date
    if isdate(data[0][0][0]):
        # setting format of x axis to date,
        # as in http://theochem.ki.ku.dk/on_line_docs/gnuplot/gnuplot_16.html
        a('set xdata time')
        a('set timefmt "%Y-%m-%d"')
        a('set format x "%m/%y"')

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
        prettyplot( map(lambda x:(x[1],x[0]), data) , path+'BestMoletrustGraphic', showlines=True )
        prettyplot( map(lambda x:(x[1],x[-1]), data) , path+'BestMoletrusTimeGraphic', log=False, showlines=True, ylabel='time [s]', title='Time of computation' )
                
    path = os.path.join(K.path, "bestMoletrustParameters/" )
    cache_path = os.path.join( path,"cache.c2" )
    
    if "Wiki" in get_name( K ):
        advogato = False
    else:
        advogato = True

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
                            if advogato:
                                avg = trustlet.PredGraph( tm ).abs_error()
                            else:
                                avg = trustlet.WikiPredGraph( tm ).abs_error()
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
        if not cond:
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
        advogato = True
    else:
        advogato = False
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
            if advogato:
                error = trustlet.PredGraph( trustmetrics[tm] ).abs_error()
            else:
                error = trustlet.WikiPredGraph( trustmetrics[tm] ).abs_error()

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
        return len([None for x in file('/proc/cpuinfo') if x.startswith('processor')])
    except IOError:
        return None

def splittask(function,input,np=None,showperc=True,notasksout=False):
    """
    create <np> processes with <input>[i] data,
    the result will return in a list.

    splittask(function,input) is equivalent to [function(x) for x in input]

    Params:
      if showperc it will print percentage of tasks done.
      if notasksout stdout of son will suppressed.
    """

    if not np:
        if os.environ.has_key('NP'):
            np = int(os.environ['NP'])
        else:
            np = getnp()
            if not np:
                np = 2

    np = min(np,len(input))

    result = []
    pipes = []
    pids = []

    if np==1:
        #doesn't create other processes
        return [function(x) for x in input]

    for proc in xrange(np):
        read,write = os.pipe()
        pinput = map(lambda x: input[x],xrange(proc,len(input),np))
        #print 'pinput',pinput
        pid = os.fork()
        if not pid:
            #son
            res = []
            if showperc:
                perc = Progress(len(pinput),1,'Percentage son # %d:'%os.getpid())
            if notasksout:
                stdout = sys.stdout
                devnull = file('/dev/null','w')

            for i,data in enumerate(pinput):
                if notasksout:
                    #remove standard output
                    sys.stdout = devnull
                #exec task
                res.append(function(data))
                if notasksout:
                    sys.stdout = stdout

                if showperc:
                    perc(i+1)
            os.write(write,marshal.dumps(res))
            os.close(write)
            #sys.exit() # ipython trap this -_-
            os._exit(0) # ipython DOESN'T trap this ^_^
        else:
            #save pipe
            pipes.append(read)
            pids.append(pid)
            os.close(write)

    #wait responce from sons
    try:
        for pipe in pipes:
            buffer = '_'
            s = ''
            while buffer:
                buffer = os.read(pipe,1000)
                s += buffer
            result.append(marshal.loads(s))
    except EOFError:
        print "A son process is dead"
        print "splittask says: it's not my fault!"
        print "I'm terminating other process ..."
        for pid in pids:
            try:
                os.kill(pid,15) # SIGTERM (SIGKILL = 9)
            except OSError:
                # process yet dead
                pass
        print "Done."
        exit()

    flatres = []
    while any(result):
        for l in result:
            if l:
                flatres.append(l[0])
                del l[0]

    return flatres

def powersplittask(function,input,np=None,showperc=True,notasksout=False):
    """

    DOESN'T WORK YET

    create <np> processes with <input>[i] data,
    the result will return in a list.

    splittask(function,input) is equivalent to [function(x) for x in input]

    Params:
      if showperc it will print percentage of tasks done.
      if notasksout stdout of son will suppressed.
    """

    lock = threading.Lock()
    tasks = set(range(len(input))) # remain tasks

    if not np:
        if os.environ.has_key('NP'):
            np = int(os.environ['NP'])
        else:
            np = getnp()
            if not np:
                np = 2

    result = []
    pipes = []
    controlpipes = []
    pids = []


    class Control(threading.Thread):
        def __init__(self,ctrlr,ctrlw):
            threading.Thread.__init__(self)
            self.ctrlr = ctrlr
            self.ctrlw = ctrlw

        def run(self):
            while True:
                lock.acquire()
                if len(tasks):
                    n = tasks.pop()
                    lock.release()
                else:
                    os.close(self.ctrlw) # tasks ends
                    os.close(self.ctrlr)
                    lock.release()
                    break

                assert os.write(self.ctrlw,str(n))

                #wait for something
                os.read(self.ctrlr,1000)

    if np==1:
        #doesn't create other processes
        return [function(x) for x in input]

    for proc in xrange(np):
        read,write = os.pipe()
        #pinput = map(lambda x: input[x],xrange(proc,len(input),np))

        # control thread (instead of pinput)
        ctrl_new_task = os.pipe()
        ctrl_continue = os.pipe()

        control = Control(ctrl_continue[0],ctrl_new_task[1])
        control.run()

        #print 'pinput',pinput
        pid = os.fork()
        if not pid:
            #son
            res = []
            if notasksout:
                stdout = sys.stdout
                devnull = file('/dev/null','w')

            while True:
                i = os.read(crtlr_new_task[0],1000)
                if not i:
                    break

                if notasksout:
                    #remove standard output
                    sys.stdout = devnull
                #exec task
                res.append(function(input[int(i)]))
                if notasksout:
                    sys.stdout = stdout

                assert os.write(ctrl_continue[1],i)

            os.write(write,marshal.dumps(res))
            os.close(write)
            #sys.exit() # ipython trap this -_-
            os._exit(0) # ipython DOESN'T trap this ^_^
        else:
            #save pipe
            pipes.append(read)
            pids.append(pid)
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
        print "I'm terminating other process ..."
        for pid in pids:
            try:
                os.kill(pid,15) # SIGTERM (SIGKILL = 9)
            except OSError:
                # process yet dead
                pass
        print "Done."
        exit()

    return result


"""data: output of pred_graph.cont_num_of_edges()"""
plot_cont_num_of_edges = lambda data,indegree,dirpath='.': \
    prettyplot(data,os.path.join(dirpath,'controv num of edges (indegree=%d).png'%indegree),
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

def mkpath(fullpath,function=None):
    """
    makes all missed directory of a path

    def function(path)
    function will called for each created dir.
    path is the path of it.
    """
    if not fullpath: return
    if fullpath[-1] == os.path.sep:
        fullpath = fullpath[:-1]
    if fullpath and not os.path.exists(fullpath):
        assert not os.path.islink(fullpath),'link %s might be broken' % fullpath
        path = os.path.split(fullpath)[0]
        mkpath(path)

        os.mkdir(fullpath)
        if function:
            function(fullpath)

redate = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
isdate = lambda x: bool(re.match(redate,str(x)))
remd5 = re.compile('^[0-9a-fA-F]{32}$')
ismd5 = lambda x: bool(re.match(remd5,x))
reip = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
                  '(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
isip = lambda x: bool(re.match(reip,x))

repid = re.compile("\d+\.c2") # match `int`.c2

#converts date in seconds from Epoch
mktimefromdate = lambda date: time.mktime(tuple(map(int,date.split('-'))) + (0,)*6)

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
    '''
    return a list of files (relative path)
    in basedir
    (why not use os.walk?)
    '''
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

    raise TypeError,"I don't know this type "+str(type(x))

def save(key,data,path,version=False,threadsafe=True,meta=None):
    """
    Cache.
    It stores some *data*  identified by *key* into a file in *path*.
    version: store the version of code that has generated data.
    meta: other info to put into c2 on key. Use read_c2() to get them
        I advise to use a dictionary with description on keys
    return: true in case of success, false in other cases
    """

    #debug
    #file(path+'.debug','w').write(str(data))

    # used by safe_save because it implements this
    if threadsafe:
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
    else:
        def lock():
            pass
        def unlock():
            pass

    # check if stored value is newer
    intversion = version is False and -1 or version

    c = load(key,path,info=True)
    #print c,key,path

    if type(c) is dict and 'vr' in c and c['vr']>intversion:
        #print 'not saved.'
        return True

    mkpath(os.path.split(path)[0])
    lock()
    try:
        # workaround?
        d = pickle.load(GzipFile(path))
    except IOError:
        d = {}

    d[hashable(key)] = {'dt':data,'ts':time.time(),'hn':gethostname()}

    if meta:
        d[hashable(key)]['mt'] = meta

    if version is not False:
        d[hashable(key)]['vr'] = version

    # dt: data
    # ts: timestamp
    # hn: hostname
    # mt: meta
    # vr: version

    ###
    #debug = file('debug')
    ###
    pickle.dump(d,GzipFile(path,'w'))
    unlock()

    #memory cache
    if not globals().has_key('cachedcache'):
        #print 'create cache'
        globals()['cachedcache'] = {}
    cache = globals()['cachedcache']
    cache[path] = (mtime(path),d)
    return True
    
def safe_save(key,data,path,*args,**argd):
    '''
    safe_save() is thread-safe version of save()
    Only version 3 is supported.
    '''
    
    assert path.endswith('.c2'),'Path doesn\'t ends with .c2'
    
    path = path[:-2] + str(os.getpid()) + '.c2'
    
    return save(key,data,path,threadsafe=False,*args,**argd)

def safe_merge(path,delete=True):
    '''
    merge files created by safe_save into the original c2 (path)
    '''

    assert path.endswith('.c2'),'Path doesn\'t ends with .c2'

    fullpath = path
    path,name = os.path.split(fullpath)
    if not path:
        path = os.curdir

    #             get name.                   get pid.c2
    f = lambda x: x.startswith(name[:-2]) and repid.match(x[len(name)-2:])

    files = [os.path.join(path,x) for x in filter(f,os.listdir(path))]
    #added by ciropom to fix a bug.. you don't store in "files" the path, but only the file name
    
    if not files:
        return

    merge_cache(files+[fullpath],fullpath)


    for file in files:
        if delete:
            print file
            os.remove(file)

def load(key,path,version=False,fault=None,cachedcache=True,info=False):
    """
    Cache.
    Loads data stored by save.
    fault is the value returned if key is not stored in cache.
    If info will return data and metadata (data: load(...)['dt'])
    """

    #print '                   ',path
    #return fault

    def onlydata(x):
        if hasattr(x,'has_key') and x.has_key('dt'):
            return x['dt']

        print 'Warning: old cache format'
        return x

    getret = info and (lambda x: x) or onlydata


    def checkversion(x):
        if version is False:
            return getret(x)

        if not hasattr(x,'has_key') or not x.has_key('vr') or x['vr']!=version:
            return fault
        else:
            return getret(x)

    #memory cache
    if not globals().has_key('cachedcache'):
        #print 'create cache'
        globals()['cachedcache'] = {}
    cache = globals()['cachedcache']


    if os.path.exists(path) and cache.has_key(path) and cachedcache and mtime(path) == cache[path][0]:
        # check if cachedcache is valid -> mtime()...

        if cache[path][1].has_key(hashable(key)):
            #xprint 'DEBUG: cachedcache hit'
            return checkversion(cache[path][1][hashable(key)])

    #if cachedcache: print 'DEBUG: cachedcache fault'

    try:
        d = pickle.load(GzipFile(path))
    except:
        return fault

    if d.has_key(hashable(key)):
        data = d[hashable(key)]
    else:
        return fault

    #save in memory cache
    cache[path] = (mtime(path),d) # (mtime,data)
    #print '*****************************',type(data)
    #return None
    return checkversion(data)

def erase_cachedcache():
    '''
    useful to reload cache from disc
    * doesn't work *
    '''
    globals()['cachedcache'] = {}

def merge_cache(source, target):
    '''
    source = [c0,c1,c2,c3,...,cn]
    
    Priority:
      highter version or newer items are kept. If version and timestamp is the same, first are kept
      c0 > c1 > c2 > ... > cn
      (Theoric behaviour. This never happen)

    source: list of filepath to merge
    target: filename of output

    If target doesn't also into sorce list, its data will lost.
    '''
    cachel = splittask(read_c2,source+[target],showperc=False)

    merge = {}

    #print cachel

    for cfile in cachel[:-1]:
        #print cfile
        # for each tuple
        for k,v in cfile.iteritems():
            #print k,merge.has_key(k)
            if not k in merge:
                merge[k] = v
            else:                
                #vr_merge = 'vr' not in merge[k] and -1 or merge[k]['vr']
                #vr_cfile = 'vr' not in cfile[k] and -1 or cfile[k]['vr']
                #print k,vr_merge,vr_cfile

                if 'vr' in merge[k] and 'vr' not in cfile[k]:
                    continue

                if 'vr' not in merge[k] and 'vr' in cfile[k]:
                    merge[k] = v
                    continue

                if 'vr' in merge[k] and 'vr' in cfile[k]:
                    if merge[k]['vr']<cfile[k]['vr']:
                        merge[k] = v
                        continue

                    if merge[k]['vr']>cfile[k]['vr']:
                        continue
                
                if merge[k]['ts'] < cfile[k]['ts']:
                    merge[k] = v

    if merge != cachel[-1]:
        #print 'Merged'
        write_c2(target,merge)
        return True
    else:
        #print 'Not merged'
        return False


def merge_cache_old(srcpath , dstpath , mpath=None, ignoreerrors=False, priority=2):
    '''
    mpath: new destination file (merged path).
    if mpath is None, *dstpath* will be used
    if `srcpath` and `dstpath` file cache has the same
    key will keep the `dstpath` value for that key.
    (To give priority to srcpath set priority to 1)
    
    ¡¡ EDIT !!

    We will keep newest data, if we know timestamp (old data hasn't it)
    '''

    try:
        f1 = GzipFile(srcpath)
        s = pickle.load(f1)
        f1.close()
    except IOError:
        if ignoreerrors:
            s = {}
        else:
            print 'File %s corrupted' % srcpath
            return
    
    
    try:
        f2 = GzipFile(dstpath)
        d = pickle.load(f2)
        f2.close()
    except IOError:
        if ignoreerrors:
            d = {}
        else:
            print 'File %s corrupted' % dstpath
            return
    

    # Priority: c2
    # if c1 and c2 has the same key will keep the c2
    # value for that key
    if priority==1:
        s,d = d,s

    modified = False
    for k,v in s.iteritems():
        if not d.has_key(k) or s[k]!=d[k] and s[k]['ts']>d[k]['ts']:
            # s[k] is newer than d[k]
            modified = True
            d[k] = s[k]

    # Write file onfy if needed
    if modified:

        if not mpath:
            mpath = dstpath
    
        f = GzipFile(mpath ,'w')
        pickle.dump(d,f)
        f.close()


def read_c2(path):
    '''return all cache dictionary'''
    try:
        return pickle.load(GzipFile(path))
    except: #  EOFError,IOError
        return {}

def write_c2(path,data):
    '''write a c2 from a dict'''
    f = GzipFile(path,'w')
    pickle.dump(data,f)
    f.close()

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

def relative_path( path, folder, debug=False ):
    """
    split a path relatively to the passed folder
    debug: print some informations
    es.

    In: relative_path( '/home/ciropom/Scrivania' , 'ciropom' )
    Out: ('/home/ciropom','Scrivania/')
    """
    ROOT = '/'

    if path.find( "/"+folder ) == -1:
        return None #folder does not exists in path

    toadd = ''; relpathlist = [] ; relpath = ''

    while( path and os.path.split( path )[1] != folder ):
        if path == ROOT:
            if debug:
                print "The folder "+folder+" is not in the path "+path
            return None
    
        path,toadd = os.path.split( path )
        relpathlist.append( toadd )

    relpathlist.reverse()
        
    for i in relpathlist:
        relpath = os.path.join( relpath, i )
        
    assert path,'folder not in path'
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

def svn_update(path,user='anybody',passwd='a'):
    """
    update svn of path
    """

    curdir = os.path.abspath('.')
    if os.path.isfile(path):
        path,name = os.path.split(path)
    else:
        name = ''

    try:
        os.chdir( path )
    except OSError:
        return False

    if user:
        user = ' --username '+user
    if passwd:
        passwd = ' --password '+passwd

    res =  not os.system( "svn%s%s up %s > /dev/null" % (user,passwd,name) )

    # reset directory
    os.chdir(curdir)
    return res

def toNetwork( data , key=None, net=None ):
    """
    convert a tuple of two list
    (the first that contains the nodes [as string],
    and the second that contains a tuple formed in this way (nodes1,nodes2,val)
    where 'val' is the weight on the edge.)
    The key is a string that represent the key of the dictionary on the edge

    parameters:
    data: tuple with two list
    key: string with key value of dictionary on edge
    net: network instance in which i must add the nodes/edges, if don't set is WeightedNetwork
    """
    ANetwork = set() #avaiable network
    ANetwork.add( WikiNetwork )
    ANetwork.add( WeightedNetwork )
    ANetwork.add( Network )
    ANetwork.add( AdvogatoNetwork )
    ANetwork.add( KaitiakiNetwork )
    ANetwork.add( SqueakfoundationNetwork )
    ANetwork.add( Robots_netNetwork )
    ANetwork.add( DummyWeightedNetwork )
    ANetwork.add( DummyNetwork )
    ANetwork.add( networkx.xdigraph.XDiGraph )

    rname = re.compile( '[^"]+' ) #erase "

    if not (type(data) is tuple and
            type(data[0]) is list and
            type(data[1]) is list and
            data[1] and
            type(data[1][0]) is tuple):
        if type(data) in ANetwork:
            return data #if it is just a network i return it simply
        else:
            raise IOError( "Data type is not a tuple with two list, or the list of edges is empty. this is the type of data passed: "+str(type(data)) )

    #create Network
    nodes = data[0]
    edges = data[1]
    if net == None:
        w = trustlet.Dataset.Network.WeightedNetwork()
    else:
        w = net

    for name in nodes:
        print name
        w.add_node( rname.findall(name)[0] )

    if key:
        for link in edges:
            w.add_edge( link[0], link[1], {key:link[2]} )
    else:
        for link in edges:
            w.add_edge( link[0], link[1], link[2] )

    return w

def toPynetwork(N):
    '''
    Given a Network return c2 network format (i.e. (nodes,edge) )
    '''
    nodes = set(N.nodes())
    edges = []

    for e in N.edges_iter():
        if e[0] in nodes:
            nodes.remove(e[0])
        if e[1] in nodes:
            nodes.remove(e[1])

        if 'value' in e[2]:
            v = 'value'
        elif 'color' in e[2]:
            v = 'color'
        elif 'level' in e[2]:
            v = 'level'
        else:
            assert 0,'I don\'t know this Network (%s)'%str(e)

        edges.append( (e[0],e[1],e[2][v]) )

    return (list(nodes),edges)

def md5file(filename):
    f = file(filename)
    a = md5.new()
    a.update(f.read())
    f.close()
    return a.digest()

eprint = lambda x: sys.stderr.write(str(x)+'\n')

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
