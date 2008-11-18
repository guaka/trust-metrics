#!/usr/bin/env python
"""
This package contains all the function 
on the evolution of a network
"""
from trustlet.helpers import *
from trustlet.conversion import dot
from trustlet.Dataset import Network,Advogato
from networkx import read_dot
import os,time,re
import os.path as path
import scipy
    
    
def trustvariance( K, d ):
    """
    This function evaluate the trust variance on more than one datasets.
    If you evaluate twice the same thing, the evaluate 
    function be able to remember it (if you call it with evolutionmap).
    
    Parameters:
    K = network
    d = date
    """

    return (d,scipy.var(K.weights_list()))

def var_plot(var, dpath, filename="trustVariance"):
    
    prettyplot( var, path.join(dpath,filename),
                title="Trust Variance on time", showlines=True,
                xlabel='date',ylabel='trust variance',
                comment=['Network: Advogato',
                         '>>> trustAverage( fromdate, todate, dpath, noObserver=False )']
                )



def trustaverage( K, d ):
    """
    This function evaluate the trust average on more than one datasets.
    If you evaluate twice the same thing, the evaluate 
    function be able to remember it.(if you call it with evolutionmap)
    
    Parameters:
    K = network
    d = date
    """

    weight = K.weights_list()
    #try to use some dictionary, because
    #sometimes the key is 'value' and sometimes is 'level'
    averagetrust = avg(weight)

    return (d,averagetrust)


def ta_plot(ta, dpath, filename="trustAverage"):
    prettyplot( ta, path.join(dpath,filename),
                title="Trust Average on time", showlines=True,
                xlabel='date',ylabel='trust average',
                comment=['Network: Advogato',
                         '>>> trustAverage( fromdate, todate, dpath, noObserver=False )'
            ]
                )

def evolutionmap(load_path,functions,range=None,debug=None):
    '''
    apply function function to each network in range range.
    If you want use cache `function` cannot be lambda functions.

    Parameters:
    load_path = path in wich the dates of the network are stored #ex. /home/ciropom/datasets/AdvogatoNetwork
    functions = list of functions to apply to each dataset #ex. [trustvariance,trustaverage...]
    range = tuple with at first the initial date, and at end the final date #ex. ('2000-01-01','2008-01-01')
    
    return a list of list of value where each list of the first list represent a function 'i',
           and the value in this list is the return value for each network in range, of the 'i' function passed
    '''
    cachepath = 'netevolution.c2'

    #check if the path ends with /
    if load_path[-1] == path.sep:
        lpath = load_path[:-1]
        
    if debug:
        deb = file( debug, 'w' ) #in debug file was stored the last function to be evaluated and on which network
        deb.close()


    dates = sorted(
        [date for date in os.listdir(lpath)
         if isdate(date) and ( path.exists(path.join(lpath,date,'graph.dot')) or \
                               path.exists(path.join(lpath,date,'graph.c2')) or \
                               path.exists(path.join(lpath,date,'graphHistory.c2')) ) ]
        )
    
    #if not dates:
    #    dates = [x for x in os.listdir(dpath)
    #             if isdate(x) and path.exists(path.join(dpath,x,'graphCurrent.c2'))]

    if not dates:
        print "There isn't any network in this path"
        return None

    if range:
        assert isdate(range[0]) and  isdate(range[1])
        dates = [x for x in dates if x>=range[0] and x<=range[1]]

    print 'There are %d networks' % len(dates)
    
    def task(date):        
        resdict = {} #dict of result
        calcfunctions = []

        #try to find the functions cached
        for i in xrange(len(functions)):
            if functions[i].__name__=='<lambda>':
                calcfunctions.append(functions[i])
            else:
                cachekey = {'function':functions[i].__name__,'date':date}
                cache = load(cachekey,path.join(lpath,cachepath))
                if cache:
                    resdict[functions[i].__name__] = cache
                    #do not calculate for functions cached
                else:
                    calcfunctions.append(functions[i])
        
        if not calcfunctions:
            #if is empty
            return resdict

        ton = os.path.split( lpath )[1] #wikinetwork/advogatonetwork...
        
        if debug:
            deb = file( debug, 'a' )
            deb.write( "evaluating functions "+str(calcfunctions)+"\non "+ton+" at date "+date+"\n" )
            deb.close()

        if ton != 'WikiNetwork':
            dotpath = path.join(lpath,date,'graph.dot')
            c2path = dotpath[:-3]+'c2'
    
            #convert in c2
            if path.exists( dotpath ):
                #debug
                if debug:
                    deb = file( debug, 'a' )
                    deb.write( "dot format detected! in network "+ton+" on date "+date+" converting in c2...\n" )
                    deb.close()
                #converting
                dot.to_c2(dotpath,c2path,{'network':ton,'date':date})
                os.remove( dotpath )

            #test what type of network I had to use
            try:
                networkclass = getattr( Advogato , ton )
            except AttributeError:
                try:
                    networkclass = getattr( Network , ton )
                except AttributeError:
                    if debug:
                        deb = file( debug, 'a' )
                        deb.write( "ERROR!: this type of network("+ton+") is not defined in trustlet.Dataset module\n" )
                        deb.close()
                    return None

            #load network
            K = networkclass(date=date)
           
            if not K:
                if debug:
                    deb = file( debug, 'a' )
                    deb.write( "ERROR!: cannot be able to load c2 on "+ton+" at date "+date+"\n" )
                    deb.close()
                else:
                    print "Error! can't load network",ton,"on date",date
                
                return None
            
            if K.number_of_nodes() == 0 or K.number_of_edges() == 0:
                if debug:
                    deb = file( debug, 'a' )
                    deb.write( "WARNING!: the network "+ton+" at date "+date+" may be wrong! check it\n" )
                    deb.close()

        elif path.exists( path.join(lpath,date,'graphHistory.c2') ):
            #load network
            try:

                lang = path.split( lpath )[1]

            except IndexError:
                if debug:
                    deb = file( debug, 'a' )
                    deb.write( "ERROR: Cannot find lang of this wikinetwork ("+date+")\n" )
                    deb.close()
                return None

            if not lang:
                print "Lang value is not usable, this is the path "+lpath+" exiting"
                return None

            K = Network.WikiNetwork( lang = lang, date = date, current = False, output=False ) #netevolution only with history
        else:
            if debug:
                deb = file( debug, 'a' )
                deb.write( "ERROR!: Cannot be able to load network! (date="+date+") on network "+ton+"\n" )
                deb.close()
            else:
                print "Cannot be able to load network! (date="+date+") on network "+ton
            return None


        for function in calcfunctions: #foreach functions that must be calculated on this network
            if debug:
                deb = file( debug, 'a' )
                deb.write( "processing "+date+"\non function "+function.__name__+"\n" )
                deb.close()

            if function.__name__!='<lambda>':
                print 'Task:',function.__name__,"on date:",date

            try:
                res = function(K,date)
            except:
                if debug:
                    deb = file( debug, 'a' )
                    deb.write( "ERROR!: Error applying "+function.__name__+" to the network "+date+"! Exiting\n" )
                    deb.close()
                else:
                    print "Error applying "+function.__name__+" to the network "+date+"! Exiting"
                continue

            if function.__name__!='<lambda>':
                if not save({'function':function.__name__,'date':date},res,path.join(lpath,cachepath)):
                    print "Warning! I cannot be able to save cache for function",function.__name__,"on date",date
            
            resdict[function.__name__] = res 

        return resdict

    #map list of result for each dataset in list of result for each function
    data_ordered = splittask(task,dates)
    nd = len( dates )
    nf = len( functions )
    
    func_ordered = []
    #prepare return value set to empty
    for fi in xrange( nf ):
        func_ordered.append( [] )

    #fill the return value
    for fi in xrange( nf ):
        for di in xrange( nd ):
            if data_ordered[di].has_key( functions[fi].__name__ ):
                func_ordered[fi].append( data_ordered[di][ functions[fi].__name__ ] )

    return func_ordered


def usersgrown(K,date):
        '''
        return the number of user for each network in date range
        '''
        return ( date,K.number_of_nodes() )
    

def plot_usersgrown(data,data_path='.'):
    '''
    data is the output of usersgrown
    >>> plot_usersgrown(usersgrown('trustlet/datasets/Advogato',range=('2000-01-01','2003-01-01')))
    '''
    fromdate = min(data,key=lambda x:x[0])[0]
    todate = max(data,key=lambda x:x[0])[0]
    prettyplot(data,path.join(data_path,'usersgrown (%s %s)'%(fromdate,todate)),
               title='Users Grown',
               xlabel='date [s] (from %s to %s)'%(fromdate,todate),
               ylabel='n. of users',
               showlines=True,
               comment='Network: Advogato'
               )


def numedges(K,date):
    '''
    return the number of user for each network in date range
    '''
    
    return ( date,K.number_of_edges() )
  
  
def plot_numedges(data,dpath='.'):
    '''
    >>> plot_*(*('trustlet/datasets/Advogato',range=('2000-01-01','2003-01-01')))
    '''
    fromdate = min(data,key=lambda x:x[0])[0]
    todate = max(data,key=lambda x:x[0])[0]
    prettyplot(data,path.join(dpath,'numedges (%s %s)'%(fromdate,todate)),
               title='Number of edges',
               xlabel='date [s] (from %s to %s)'%(fromdate,todate),
               ylabel='n. of edges',
               showlines=True,
               comment=['Network: Advogato','>>> plot_numedges(numedges(...))']
               )

def edgespernode(K,date):
    '''
    return the average number of edges for each user
    '''
    
    nodes = K.number_of_nodes()
    return ( date , 1.0*K.number_of_edges()/nodes )


def plot_edgespernode(data,dpath='.'):
    '''
    data is the output of edgespernode
    '''
    fromnnodes = min(data,key=lambda x:x[0])[0]
    tonnodes = max(data,key=lambda x:x[0])[0]
    prettyplot(data,path.join(dpath,'edgespernode (%s %s)'%(fromnnodes,tonnodes)),
               title='Average Edges per Node',
               xlabel='nodes',
               ylabel='number of edges per node',
               showlines=True,
               comment=['Network: Advogato','>>> plot_edgespernode(edgespernode(...))']
               )

def meandegree(K,date):
    return ( date,K.avg_degree() )


def plot_meandegree(data,data_path='.'):
    fromdate = min(data,key=lambda x:x[0])[0]
    todate = max(data,key=lambda x:x[0])[0]
    prettyplot(data, path.join( data_path,'meandegree (%s %s)'%(fromdate,todate) ),
               showlines=True,
               comment=['Network: Advogato','>>> plot_meandegree(meandegree(...))']
               )


def level_distribution(K,date):
    """
    see AdvogatoNetwork class
    this code (d = dict(...)) is copyed from there
    """
    if get_name( K ) != "WeightedNetwork":
        return None

    #level map = color map + obs_app_jour_mas map 
    level_map = Advogato._obs_app_jour_mas_map.copy()
    level_map.update(Advogato._color_map)

    # we use values()[0] instead of the key of dict because sometimes
    # the key is 'value' and sometimes it's 'level'
    # *need to fix this*
    d = dict(filter(lambda x:x[0],
                    map(lambda s: (s,
                                   len([e for e in K.edges_iter()
                                        if e[2].values()[0] == s])),
                        level_map)))
    #order k from higher to lower values (Master to Observer)
    l = [d[k] for k,v in sorted(level_map.items(),lambda x,y: cmp(y[1],x[1])) if k and d[k]]

    return ( date, map(lambda x:1.0*x/sum(l),l))


def plot_level_distribution(data,data_path='.'):

    # formatted data:
    # from: [(a,(b,c,d,e)), (a1,(b1,c1,d1,e1)), ...]
    # to:   [ [(a,b), (a1,b1), ...],[(a,c), (a1,c1), ...], [(a,d), ...], ... ]
    # lists of ['Master','Journeyer','Apprentice','Observer']

    if not data or not data[0] or not data[0][1]:
        return None

    f_data = [[],[],[],[]]
    for t in data:
        for i,l in enumerate(f_data):
            l.append((t[0],t[1][i]))
    r = (min(data,key=lambda x:x[0])[0],max(data,key=lambda x:x[0])[0])
    prettyplot(f_data,path.join(data_path,'level distribution (%s %s)'%r),
               title='Level distribution',
               xlabel='dates (from %s to %s)'%r,
               ylabel='percentage of edges',
               legend=['Master','Journeyer','Apprentice','Observer'],
               showlines=True,
               comment=['Network: Advogato',
                        '>>> plot_level_distribution(level_distribution(...))']
               )

def genericevaluation(path,functions,range=None):
    '''
    functions: list of function
    function: f(network) -> value on y axis

    genericevaluation implements cache support
    '''
    fs = []

    for function in functions:
        f = lambda K,date: (date,function(K))
        if function.__name__!='<lambda>':
            f.__name__ = 'generic(%s)'%function.__name__
            
        fs.append( f )

    return evolutionmap(path,fs,range)

def plot_genericevaluation(data,data_path='.',title='',comment=''):
    '''
    plot output of genericevolution

    example:

    >>> plot_genericevaluation(
            genericevaluation('path/AdvogatoNetwork',networkx.average_clustering ,None),
            '.', title='Average clustering'
            )
    '''
    if not data or None in data:
        return None

    fromdate = min(data,key=lambda x:x[0])[0]
    todate = max(data,key=lambda x:x[0])[0]
    if not title:
        title = 'Untitled'
    prettyplot(
        data,
        path.join(data_path,'%s (%s %s)'%(title,fromdate,todate)),
        title=title,
        showlines=True,
        comment=comment,
        )


def avgcontroversiality(K,min_in_degree=10):

    cont = [] # controversiality array

    for n in K.nodes_iter():
        in_edges = K.in_edges(n)
        
        if len(in_edges)<min_in_degree:
            continue

        cont.append(
            numpy.std([K.level_map[x[2].values()[0]] for x in in_edges])
            # We get the first value because the key is sometimes
            # 'value' and sometimes 'level'
        )

    if not cont:
        return None
    else:
        return avg(cont)

avgcont10 = lambda G: avgcontroversiality(G,10)
avgcont10.__name__ = 'avgcontroversiality-min_in_degree-10'

avgcont20 = lambda G: avgcontroversiality(G,20)
avgcont20.__name__ = 'avgcontroversiality-min_in_degree-20'

def createHTML( points ):
    """
    This function create a HTML document, that contains a graph using "SMILE timeplot"
    http://simile.mit.edu/timeplot
    
    There isn't necessary to install webserver or moreover, but it's necessary
    to have an internet connection (because the html file use a javascript remote script)
    Parameters:
       points: list of tuple
       returns: tuple with html in a string, data in another string. 
                
       NB: data must be written to a file named '.data'
           if you would write the html file
    """

    htmldoc = """<html><head>
  <title>Trustlet Evolution Graph</title>
    <script src="http://static.simile.mit.edu/timeplot/api/1.0/timeplot-api.js" 
       type="text/javascript"></script>

    <script language="Javascript1.2">
var timeplot;

function onLoad() {
  var eventSource = new Timeplot.DefaultEventSource();
  var plotInfo = [
    Timeplot.createPlotInfo({
      id: "plot1",
      dataSource: new Timeplot.ColumnSource(eventSource,1),
      timeGeometry: new Timeplot.DefaultTimeGeometry({
        gridColor: "#000000",
        axisLabelsPlacement: "top"
      }),
      lineColor: "#ff0000",
      fillColor: "#cc8080",
      showValues: true
    })
  ];
            
  timeplot = Timeplot.create(document.getElementById("trustlet-timeplot"), plotInfo);
  timeplot.loadText(".data", ",", eventSource);
}

var resizeTimerID = null;

function onResize() {
    if (resizeTimerID == null) {
        resizeTimerID = window.setTimeout(function() {
            resizeTimerID = null;
            timeplot.repaint();
        }, 100);
    }
}


    </script>
  </head>
  <body  onload="onLoad();" onresize="onResize();">

  <div id="trustlet-timeplot" style="height: 150px;"></div>

  </body></html>
"""

    data = "#Trustlet, autogenerated data file\n\n"
    
    for (x,y) in points:
        data += str(x)+","+str(y)+"\n" 

    return (htmldoc,data)


if __name__ == "__main__":    
    import sys,os
    if len(sys.argv) < 5:
        #prog startdate enddate path
        print "This script generate so many graphics with gnuplot (and generate .gnuplot file"
        print "useful to see the grown of the network in an interval of time"
        print "USAGE: netevolution startdate enddate dataset_path save_path [debug_path,html_file_path]"
        print "You can use '-' to skip {start,end}date"
        sys.exit(1)


    startdate = sys.argv[1] == '-' and '0000-00-00' or sys.argv[1]
    enddate = sys.argv[2] == '-' and '9999-99-99' or sys.argv[2]
    range = (startdate,enddate)
    dpath = sys.argv[3]
    savepath = sys.argv[4]

    if sys.argv[5:]:
        debugfile = sys.argv[5]
    else:
        debugfile = None

    mkpath(savepath)

    data = evolutionmap( dpath, [trustaverage,trustvariance,numedges,meandegree,usersgrown,edgespernode,level_distribution], (startdate,enddate) ,debugfile )
    if not data:
        sys.exit(1)

    ta_plot( data[0], savepath )
    var_plot( data[1], savepath )
    plot_numedges( data[2], savepath )
    plot_meandegree( data[3], savepath )
    plot_usersgrown( data[4], savepath )
    plot_edgespernode( data[5], savepath )
    plot_level_distribution( data[6], savepath )

    #generic evaluation
    eval1=lambda G:networkx.diameter(networkx.connected_component_subgraphs(G.to_undirected())[0])
    eval1.__name__='diameter-largest-connected-component'

    eval2=lambda G:networkx.radius(networkx.connected_component_subgraphs(G.to_undirected())[0])
    eval2.__name__='radius-largest-connected-component'
    
    eval4 = lambda G: avg(
        networkx.betweenness_centrality(G).values()
        )
    eval4.__name__ = 'betweenness_centrality-yes-normalized-no-weighted_edges'
    
    eval5 = lambda G: avg(
        networkx.betweenness_centrality(G).values()
        )
    eval5.__name__ = 'betweenness_centrality-yes-normalized-yes-weighted_edges'
    
    eval6 = lambda G: avg(
        networkx.betweenness_centrality(G,normalized=False).values()
        )
    eval6.__name__ = 'betweenness_centrality-no-normalized-no-weighted_edges'

    eval7 = lambda G: avg(
        networkx.closeness_centrality(G).values()
        )
    eval7.__name__ = 'closeness_centrality-no-weighted_edges'
    
    eval8 = lambda G: avg(
        networkx.closeness_centrality(G,weighted_edges=True).values()
        )
    eval8.__name__ = 'closeness_centrality-yes-weighted_edges'
    
    eval9 = lambda G: avg(
        networkx.newman_betweenness_centrality(G).values()
        )
    eval9.__name__ = 'newman_betweenness_centrality'
    
    
    eval10 = lambda G: networkx.number_connected_components(G.to_undirected())
    eval10.__name__ = 'number_connected_components'

    data = genericevaluation( dpath,
                              [networkx.average_clustering,eval1,eval2,networkx.density,eval4,eval5,eval6,eval7,eval8,eval9,eval10,avgcont20],
                              range )


    
    plot_genericevaluation( 
        data[0],
        savepath, title='average_clustering', comment='Function: nx.average_clustering'
        )


    plot_genericevaluation(
        data[1],
        savepath, title='diameter',
        comment='eval = nx.diameter(networkx.connected_component_subgraphs'
        '(G.to_undirected())[0])'
        )

    plot_genericevaluation(
        data[2],
        savepath, title='radius',
        comment='eval = nx.radius(networkx.connected_component_subgraphs'
                '(G.to_undirected())[0])'
        )

    plot_genericevaluation(
        data[3],
        savepath, title='density', comment='Function: nx.density'
        )

    plot_genericevaluation(
        data[4],
        savepath, title='betweenness_centrality yes-normalized no-weighted_edges',
        comment='eval = avg(nx.betweenness_centrality'
                '(G,normalized=True,weighted_edges=False).values())'
        )

    plot_genericevaluation(
        data[5],
        savepath, title='betweenness_centrality yes-normalized yes-weighted_edges',
        comment='eval = avg(nx.betweenness_centrality'
                '(G,normalized=True,weighted_edges=True).values())'
        ) 

    plot_genericevaluation(
        data[6],
        savepath, title='betweenness_centrality no-normalized no-weighted_edges',
        comment='eval = avg(nx.betweenness_centrality'
               '(G,normalized=False,weighted_edges=False).values())'
        )

    plot_genericevaluation(
        data[7],
        savepath, title='closeness_centrality no-weighted_edges',
        comment='eval = avg(nx.closeness_centrality'
                '(G,weighted_edges=False).values())'
        )

    plot_genericevaluation(
        data[8],
        savepath, title='closeness_centrality yes-weighted_edges',
        comment='eval = avg(nx.closeness_centrality'
                '(G,weighted_edges=True).values())'
        )

    plot_genericevaluation(
        data[9],
        savepath, title='newman betweenness centrality',
        comment='eval = avg(networkx.newman_betweenness_centrality(G).values())'
        )

    plot_genericevaluation(
        data[10],
        savepath, title='number_connected_components',
        comment='eval = nx.number_connected_components(G.to_undirected())'
        )

    
    plot_genericevaluation(
        data[11],
        savepath, title='avg of standard deviation in received trust (in degree=20)',
        comment='''\
cont = [] # controversiality array

for n in K.nodes_iter():
    in_edges = K.in_edges(n)

    # min_in_degree -> written in name of function
    if len(in_edges)<min_in_degree:
        continue

    cont.append(
        numpy.std([_obs_app_jour_mas_map[x[2]['level']] for x in in_edges])
    )

return avg(cont)'''
        )


    # can we erase this?
    if len(sys.argv) >= 7:
        html = sys.argv[6]
        f = file( path.join( savepath, html ) , 'w' )
        fd = file( path.join( savepath, '.data' ) , 'w' )

        html,data = createHTML( ta )
        f.write(html)
        fd.write(data)
        f.close()
        fd.close()
