
"""Collection of random useful stuff."""
import math
import numpy
from trustlet.TrustMetric import *
from trustlet.trustmetrics import *
import trustlet
import Gnuplot
import os,sys,re
import datetime
import time
import marshal
#cache
import md5
import pickle
from gzip import GzipFile

try:
    import scipy
except:
    print "no scipy"

UNDEFINED = -37 * 37  #mayby use numpy.NaN?

def getTrustMetrics( net, trivial=False, advogato=True, allAdvogato=['Observer','Journeyer','Apprentice','Master']):
    """
    return all trust metric on network passed
    Parameters:
       trivial = if True, add the trivial function as always_master, always_observer...
       allAdvogatoLocalDefault = if True, and advogato is True, include AdvogatoLocalDefaultObserver/Journeyer/Master/Apprentice
       advogato = include advogato trust metrics
    """
    trustmetrics = {
        "random_tm": trustlet.TrustMetric( net , trustlet.random_tm ),
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
        

        if allAdvogato:
            levels = type(allAdvogato) is list and allAdvogato or net.level_map.keys()
            for level in levels:
                if level:
                    trustmetrics["AdvogatoLocalDefault"+level] = trustlet.AdvogatoLocal(net,level)

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

    
            
#made by Danilo Tomasoni            

def plotparameters( tuplelist, path, onlyshow=False, title='Moletrust Accuracy', xlabel='horizon', ylabel='abs error', log=False, onlypoint=False, istogram=False ):
    """
    Print a graphics of the list passed.
    path is the location in wich the png image will be saved,
    if you wouldn't save it, set the onlyshow parameter to True
    title parameter, set the title of the plot
    
    DEPRECATED (only because i don't like function signature)
    """
    g = Gnuplot.Gnuplot()
    g.title( title )
    
    if onlypoint:
        g('set parametric')
    else:
        g('set data style lines')
    
    if istogram:
        g('set style data boxes')    
        
    if log:
        g('set logscale y 1.5' )
    g.xlabel( xlabel )
    g.ylabel( ylabel )
    #first place horizon, sencond place abs error (converted in float)
    #i must delete the None object in list.
    
    points = map(lambda x:(float(x[0]),float(x[1])), [t for t in tuplelist if t])
    
    points.sort()
    g.plot( points )

    if not onlyshow:
        g('set terminal png')
        g('set filename '+path)
        #this doesn't work

        g.hardcopy(
            filename=path,
            terminal='png'
            )
    
    return None

def prettyplot( data, path, **args):
    """
    Print a graphics of the list passed.
    *path* is the location in wich the png image will be saved.

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
        log=False
        showlines=False (old onlypoint)
        istogram=False
        x_date=True
        x_range (tuple)
    """

    g = Gnuplot.Gnuplot(persist=1)
    try:
        g.title(args['title'])
    except KeyError:
        pass
    
    if args.has_key('showlines') and args['showlines']:
        #g('set data style lines')
        g('set data style linespoint')
    #else:
    #    g('set parametric')
    if args.has_key('istogram') and args['istogram']:
        g('set style data boxes')
    if args.has_key('log') and args['log']:
        g('set logscale y 1.5' )
    if args.has_key('xlabel'):
        g.xlabel(args['xlabel'])
    if args.has_key('ylabel'):
        g.ylabel(args['ylabel'])
    # setting format of x axis to date, as in http://theochem.ki.ku.dk/on_line_docs/gnuplot/gnuplot_16.html
    if args.has_key('x_date'):
        g('set xdata time')
        g('set timefmt "%Y-%m-%d"')
    if args.has_key('x_range'):
        if args['x_range'] != None:
            g('set xrange ['+str(args['x_range'][0])+':'+str(args['x_range'][1])+']')
    if args.has_key('y_range'):
        if args['y_range']:
            g('set yrange ['+str(args['y_range'][0])+':'+str(args['y_range'][1])+']')

    try:
        legend = args['legend']
    except:
        legend = None

    if not data:
        print "prettyplot: no input data"
        return
    if type(data) is list and type(data[0]) is list and data[0] and type(data[0][0]) is tuple:
        pointssets = [map(lambda x:(float(x[0]),float(x[1])), [t for t in set if t]) for set in data]
    else:
        pointssets = [map(lambda x:(float(x[0]),float(x[1])), [t for t in data if t])]
        if legend:
            legend = [legend]

    p = []
    for name,points in legend and zip(legend,pointssets) or zip([None for x in pointssets[0]],pointssets):
        points.sort()
        if name:
            p.append(Gnuplot.PlotItems.Data(points, title=name))
        else:
            p.append(Gnuplot.PlotItems.Data(points))
        
    g.plot(*p)

    g.hardcopy(
        filename=path,
        terminal='png'
        )

#test prettyplot
if 0 and __name__=="__main__":

    import Gnuplot

    gp = Gnuplot.Gnuplot(persist = 1)
    gp('set data style lines')
    
    data1 = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]    # The first data set (a quadratic)
    data2 = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]     # The second data set (a straight line)
    
    # Make the plot items
    plot1 = Gnuplot.PlotItems.Data(data1, with="lines", title="Quadratic")
    plot2 = Gnuplot.PlotItems.Data(data2, with="points 3", title=None)  # No title

    #gp.plot(plot1, plot2)
    #exit(0)

    if 1:
        s = prettyplot([[(0,0),(1,0.1),(2,0.2),(3,0.3)],[(0,1),(1,2),(2,3)]],'image.png',showlines=True,legend=['ciao',''],xlabel='X',ylabel='ErrORReeeee',istogram=True)
    else:
        s = prettyplot([(0,0),(1,0),(2,0),(0,1),(1,2),(2,3)],'image.png',legend='uno',showlines=True)
    print s
    exit(0)

def bestMoletrustParameters( K, verbose = False, bestris=True, maxhorizon = 5, force=False, np=4 ):
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
        plotparameters( map(lambda x:(x[1],x[0]), data) , path+'BestMoletrustGraphic.png' )
        plotparameters( map(lambda x:(x[1],x[-1]), data) , path+'BestMoletrusTimeGraphic.png', log=False, ylabel='time [s]', title='Time of computation' )
                

    path = os.path.join(K.path, "bestMoletrustParameters/" )
    
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


def testTM( net, bpath=None, np=4, onlybest=False, plot = False ):
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

    path = os.path.join(bpath,'TrustMetrics')
    if not os.path.exists(path):
        os.mkdir(path)

        #for each trust metric, print the predicted value for each edge
    trustmetrics = getTrustMetrics( net )
	#parameters:
	#path is the path on which to save the computation
	#tm is the trustMetric class 
	#tmname is the trust metric name, 
        #predgraph                                      
    def eval( (path,tm) ):
            #tm = current tm

        sum = 0
        cnt = 0
        abs = load( {'tm':tm},path+'/cache' )
        
        if abs != None:
            error = abs
        else:
            P = trustlet.PredGraph( trustmetrics[tm] )
            error = P.abs_error()
        
            save({'tm':tm},error,path+'/cache')
                    
        return ( error, tm )

	# we use splittask so that we can split the computation in parallel across different processors (splittask is defined in helpers.py). Neet to check how much this is efficient or needed.
    lris = splittask( eval , [(path,tm) for tm in trustmetrics], np ) 

    if onlybest:
        lris.sort()
        return lris[0]
    else:
        if plot:    
            plotparameters( [x for x in enumerate([x for (x,s) in lris])], path+'/TrustMetricsHistogram.png', 
                            title = 'MAE for each trustmetric on '+get_name(net)+' network',
                            xlabel='trust metrics',
                            ylabel='MAE',
                            istogram = True )
            
        fd = file( path+'/HistogramLegend', 'w' )
        fd.write( '\n'.join( [str(n)+': '+s for (n,s) in enumerate([y+' '+str(x) for (x,y) in lris])] ) )
        fd.close()
        
        lris.sort()

        return lris

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
isdate = lambda x: bool(re.match(redate,x))
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

def save(key,data,path='.',human=False):
    """
    Cache.
    It stores some *data*  identified by *key* into a file in *path*.
    If human=True it will save another file in plain text for human beings.
    DEPRECATED: You can set *time* (integer, in seconds) to indicate the
    time of computation.
    If path ends with '.c2' data will save in the new format (less files).
    human is not suported in the new format.
    """
    if path.endswith('.c2'):
        mkpath(os.path.split(path)[0])
        try:
            d = pickle.load(GzipFile(path))
        except:
            d = {}
        d[get_sign(key)] = data
        pickle.dump(d,GzipFile(path,'w'))

        #memory cache
        if not globals().has_key('cachedcache'):
            #print 'create cache'
            globals()['cachedcache'] = {}
        cache = globals()['cachedcache']
        cache[path] = d
    else:
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
    
def load(key,path='.'):
    """
    Cache.
    Loads data stored by save.
    """
    if os.path.isdir(path):
        try:
            data = pickle.load(file(os.path.join(path,get_sign(key))))
        except:
            return None
    elif os.path.isfile(path):
        #memory cache
        if not globals().has_key('cachedcache'):
            #print 'create cache'
            globals()['cachedcache'] = {}
        cache = globals()['cachedcache']

        if cache.has_key(path):
            #print 'found',path
            if cache[path].has_key(get_sign(key)):
                return cache[path][get_sign(key)]
            else:
                return None
        
        try:
            d = pickle.load(GzipFile(path))
            data = d[get_sign(key)]
        #except KeyError,IOError:
        except:
            return None

        #save in memory cache
        cache[path] = d
    else:
        return None
    return data

def erase_cachedcache():
    '''
    useful to reload cache from disc
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
        tmppath = os.tempnam()
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

if __name__=="__main__":
    from trustlet import *
    from pprint import pprint
    k = KaitiakiNetwork(download=True)
    testTM( k )
