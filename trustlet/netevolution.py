#!/usr/bin/env python
"""
This package contains all the function 
on the evolution of a network
"""
from trustlet.helpers import *
from trustlet.Dataset import Network
from trustlet.Dataset.Advogato import _color_map,_obs_app_jour_mas_map
from networkx import read_dot
import os,time,re

def trustAverage( fromdate, todate, path, noObserver=False ):
    """
    This function evaluate the trust average on more than one datasets.
    If you evaluate twice the same thing, the evaluate 
    function be able to remember it.
    
    Parameters:
    fromdate: initial date
    todate: finishdate
    path: path in wich I can find the network
          ex. /home/ciropom/datasets/AdvogatoNetwork
    returns: a list of tuple (x,y) that can be represented in a graph
    """
    try:
        lsdate = os.listdir( path )
    except OSError:
        return None
    
    avg = lambda ls:float(sum(ls))/len(ls)
    #filtered date
    
    def trustaverage( K, d ):
    #for d in fdate:

        # evolutionmap managa cache (use thae name of function 'trustaverage')

        #at = load( {'function':'trustAverage', 'date':d}, os.path.join(path,d) )
        #if at != None:
        #    return (d,at)

        print "Evaluating dataset of ", d
        #temporary path
        #can be advogato/kaitiaki style, or directly with a integer weights
        weight = K.weights()
        
        try:
            averagetrust = avg([_obs_app_jour_mas_map[val[0]] for val in [x.values() for x in weight]])
        except KeyError:
            try:
                averagetrust = avg([_color_map[val[0]] for val in [x.values() for x in weight]])
            except KeyError:
                averagetrust = avg([val[0] for val in [x.values() for x in weight]])

        #save( {'function':'trustAverage', 'date':d}, averagetrust ,os.path.join(path,d) )
        
        print "dataset of ",d ," Evaluated"
        return (d,averagetrust)
    
    if noObserver:
        return evolutionmap( path, trustaverage, (fromdate,todate), no_observer )
    else:
        return evolutionmap( path, trustaverage, (fromdate,todate) )

def ta_plot(ta, path, filename="trustAverage"):
    prettyplot( ta, os.path.join(path,filename),
                title="Trust Average on time", showlines=True,
                xlabel='date in seconds',ylabel='trust average',
                comment=['Network: Advogato',
                         '>>> trustAverage( fromdate, todate, path, noObserver=False )'
            ]
                )

def evolutionmap(path,function,range=None):
    '''
    apply function function to each network in range range.
    If you want use cache `function` cannot be lambda functions.
    '''
    cachepath = 'netevolution.c2'
    dates = [x for x in os.listdir(path)
             if isdate(x) and os.path.exists(os.path.join(path,x,'graph.dot'))]
    
    #if not dates:
    #    dates = [x for x in os.listdir(path)
    #             if isdate(x) and os.path.exists(os.path.join(path,x,'graphCurrent.c2'))]

    if not dates:
        print "There isn't any network in this path"
        return

    if range:
        assert isdate(range[0]) and  isdate(range[1])
        dates = [x for x in dates if x>=range[0] and x<=range[1]]

    if function.__name__!='<lambda>':
        print 'Task:',function.__name__
    print 'There are %d networks' % len(dates)
    
    def task(date):
        #cache
        if function.__name__=='<lambda>':
            print "i can't save cache with lambda funtions"
        else:
            cachekey = {'function':function.__name__,'date':date}
            cache = load(cachekey,path=os.path.join(path,cachepath))
            if cache:
                return cache
        #print date only if the function will computed
        print date
        G = read_dot(os.path.join(path,date,'graph.dot'))
        K = Network.WeightedNetwork()
        K.paste_graph(G)
        res = function(K,date)
        if function.__name__!='<lambda>':
            assert save(cachekey,res,os.path.join(path,cachepath))
        return res

    #return [task(x) for x in dates]
    return splittask(task,dates)


def usersgrown(path,range=None):
    '''
    return the number of user for each network in date range
    '''
    def usersgrown(K,date):
        return ( date,K.number_of_nodes() )
    
    return evolutionmap(path,usersgrown,range)

def plot_usersgrown(data,path='.'):
    '''
    data is the output of usersgrown
    >>> plot_usersgrown(usersgrown('trustlet/datasets/Advogato',range=('2000-01-01','2003-01-01')))
    '''
    fromdate = min(data,key=lambda x:x[0])[0]
    todate = max(data,key=lambda x:x[0])[0]
    prettyplot(data,os.path.join(path,'usersgrown (%s %s)'%(fromdate,todate)),
               title='Users Grown',
               xlabel='date [s] (from %s to %s)'%(fromdate,todate),
               ylabel='n. of users',
               showlines=True,
               comment='Network: Advogato'
               )


def numedges(path,range=None):
    '''
    return the number of user for each network in date range
    '''
    def numedges(K,date):
        return ( date,K.number_of_edges() )
    
    return evolutionmap(path,numedges,range)

def plot_numedges(data,path='.'):
    '''
    >>> plot_*(*('trustlet/datasets/Advogato',range=('2000-01-01','2003-01-01')))
    '''
    fromdate = min(data,key=lambda x:x[0])[0]
    todate = max(data,key=lambda x:x[0])[0]
    prettyplot(data,os.path.join(path,'numedges (%s %s)'%(fromdate,todate)),
               title='Number of edges',
               xlabel='date [s] (from %s to %s)'%(fromdate,todate),
               ylabel='n. of edges',
               showlines=True,
               comment=['Network: Advogato','>>> plot_numedges(numedges(...))']
               )

def edgespernode(path,range=None):
    '''
    return the average number of edges for each user
    '''
    def edgespernode(K,date):
        nodes = K.number_of_nodes()
        return ( date , 1.0*K.number_of_edges()/nodes )
    
    return evolutionmap(path,edgespernode,range)

def plot_edgespernode(data,path='.'):
    '''
    data is the output of edgespernode
    '''
    fromnnodes = min(data,key=lambda x:x[0])[0]
    tonnodes = max(data,key=lambda x:x[0])[0]
    prettyplot(data,os.path.join(path,'edgespernode (%s %s)'%(fromnnodes,tonnodes)),
               title='Average Edges per Node',
               xlabel='nodes',
               ylabel='number of edges per node',
               showlines=True,
               comment=['Network: Advogato','>>> plot_edgespernode(edgespernode(...))']
               )

def meandegree(path,range=None):
    def meandegree(K,date):
        return ( date,K.avg_degree() )
    
    return evolutionmap(path,meandegree,range)

def plot_meandegree(data,path='.'):
    fromdate = min(data,key=lambda x:x[0])[0]
    todate = max(data,key=lambda x:x[0])[0]
    prettyplot(data,os.path.join(path,'meandegree (%s %s)'%(fromdate,todate)),
               showlines=True,
               comment=['Network: Advogato','>>> plot_meandegree(meandegree(...))']
               )

def level_distribution(path,range=None):
    #'Master','Journeyer','Apprentice','Observer'
    '''
    Advogato only!
    '''

    def level_distribution(K,date):
        """
        *** don't try to understand this ***
        (rewrite this code is quicker)
        see AdvogatoNetwork class
        """
        d = dict(filter(lambda x:x[0],
                        map(lambda s: (s,
                                       len([e for e in K.edges_iter()
                                            if e[2].values()[0] == s])),
                            _obs_app_jour_mas_map)))
        l = [d['Master'],d['Journeyer'],d['Apprentice'],d['Observer']]
        return ( date, map(lambda x:1.0*x/sum(l),l))
    
    return evolutionmap(path,level_distribution,range)    


def plot_level_distribution(data,path='.'):

    # formatted data:
    # from: [(a,(b,c,d,e)), (a1,(b1,c1,d1,e1)), ...]
    # to:   [ [(a,b), (a1,b1), ...],[(a,c), (a1,c1), ...], [(a,d), ...], ... ]
    # lists of ['Master','Journeyer','Apprentice','Observer']
    f_data = [[],[],[],[]]
    for t in data:
        for i,l in enumerate(f_data):
            l.append((t[0],t[1][i]))
    r = (min(data,key=lambda x:x[0])[0],max(data,key=lambda x:x[0])[0])
    prettyplot(f_data,os.path.join(path,'level distribution (%s %s)'%r),
               title='Level distribution',
               xlabel='dates (from %s to %s)'%r,
               ylabel='percentage of edges',
               legend=['Master','Journeyer','Apprentice','Observer'],
               showlines=True,
               comment=['Network: Advogato',
                        '>>> plot_level_distribution(level_distribution(...))']
               )

def genericevaluation(path,function,range=None):
    '''
    function: f(network) -> value on y axis

    genericevaluation implements cache support
    '''
    f = lambda K,date: (date,function(K))
    if function.__name__!='<lambda>':
        f.__name__ = 'generic(%s)'%function.__name__
    return evolutionmap(path,f,range)

def plot_genericevaluation(data,path='.',title='',comment=''):
    '''
    plot output of genericevolution

    example:

    >>> plot_genericevaluation(
            genericevaluation('path/AdvogatoNetwork',networkx.average_clustering ,None),
            '.', title='Average clustering'
            )
    '''

    fromdate = min(data,key=lambda x:x[0])[0]
    todate = max(data,key=lambda x:x[0])[0]
    if not title:
        title = 'Untitled'
    prettyplot(
        data,
        os.path.join(path,'%s (%s %s)'%(title,fromdate,todate)),
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
            numpy.std([_obs_app_jour_mas_map[x[2]['level']] for x in in_edges])
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
        print "USAGE: netevolution startdate enddate dataset_path save_path [html file]"
        sys.exit(1)


    startdate = sys.argv[1]
    enddate = sys.argv[2]
    range = (startdate,enddate)
    path = sys.argv[3]
    savepath = sys.argv[4]

    mkpath(savepath)

    ta = trustAverage( startdate, enddate, path)
    ta_plot( ta, savepath )
    plot_numedges( numedges( path,range ), savepath )
    plot_meandegree( meandegree( path,range ), savepath )
    plot_usersgrown( usersgrown( path,range ), savepath )
    plot_edgespernode( edgespernode( path,range ), savepath )
    plot_level_distribution( level_distribution( path,range ), savepath )

    #generic evaluation

    if True or gethostname()=='sracls01':

        plot_genericevaluation(
            genericevaluation( path,networkx.average_clustering ,range ),
            savepath, title='average_clustering', comment='Function: nx.average_clustering'
            )
        
        eval=lambda G:networkx.diameter(networkx.connected_component_subgraphs(G.to_undirected())[0])
        eval.__name__='diameter-largest-connected-component'
        plot_genericevaluation(
            genericevaluation(path,eval,range),
            savepath, title='diameter',
            comment='eval = nx.diameter(networkx.connected_component_subgraphs'
            '(G.to_undirected())[0])'
            )

        eval=lambda G:networkx.radius(networkx.connected_component_subgraphs(G.to_undirected())[0])
        eval.__name__='radius-largest-connected-component'
        plot_genericevaluation(
            genericevaluation(path,eval,range),
            savepath, title='radius',
            comment='eval = nx.radius(networkx.connected_component_subgraphs'
                    '(G.to_undirected())[0])'
            )

        plot_genericevaluation(
            genericevaluation( path,networkx.density ,range ),
            savepath, title='density', comment='Function: nx.density'
            )

        eval = lambda G: avg(
            networkx.betweenness_centrality(G,normalized=True, weighted_edges=False).values()
            )
        eval.__name__ = 'betweenness_centrality-yes-normalized-no-weighted_edges'
        plot_genericevaluation(
            genericevaluation( path, eval ,range ),
            savepath, title='betweenness_centrality yes-normalized no-weighted_edges',
            comment='eval = avg(nx.betweenness_centrality'
                    '(G,normalized=True,weighted_edges=False).values())'
            )

        eval = lambda G: avg(
            networkx.betweenness_centrality(G,normalized=True, weighted_edges=True).values()
            )
        eval.__name__ = 'betweenness_centrality-yes-normalized-yes-weighted_edges'
        #plot_genericevaluation(
        #    genericevaluation( path, eval ,range ),
        #    savepath, title='betweenness_centrality yes-normalized yes-weighted_edges',
        #    comment='eval = avg(nx.betweenness_centrality'
        #            '(G,normalized=True,weighted_edges=True).values())'
        #    ) 

    #elif gethostname()=='sracls03':

        eval = lambda G: avg(
            networkx.betweenness_centrality(G,normalized=False, weighted_edges=False).values()
            )
        eval.__name__ = 'betweenness_centrality-no-normalized-no-weighted_edges'
        plot_genericevaluation(
            genericevaluation( path, eval ,range ),
            savepath, title='betweenness_centrality no-normalized no-weighted_edges',
            comment='eval = avg(nx.betweenness_centrality'
                   '(G,normalized=False,weighted_edges=False).values())'
            )

        eval = lambda G: avg(
            networkx.closeness_centrality(G,weighted_edges=False).values()
            )
        eval.__name__ = 'closeness_centrality-no-weighted_edges'
        plot_genericevaluation(
            genericevaluation( path, eval ,range ),
            savepath, title='closeness_centrality no-weighted_edges',
            comment='eval = avg(nx.closeness_centrality'
                    '(G,weighted_edges=False).values())'
            )

        eval = lambda G: avg(
            networkx.closeness_centrality(G,weighted_edges=True).values()
            )
        eval.__name__ = 'closeness_centrality-yes-weighted_edges'
        #plot_genericevaluation(
        #    genericevaluation( path, eval ,range ),
        #    savepath, title='closeness_centrality yes-weighted_edges',
        #    comment='eval = avg(nx.closeness_centrality'
        #            '(G,weighted_edges=True).values())'
        #    )

        eval = lambda G: avg(
            networkx.newman_betweenness_centrality(G).values()
            )
        eval.__name__ = 'newman_betweenness_centrality'
        plot_genericevaluation(
            genericevaluation( path, eval ,range ),
            savepath, title='newman betweenness centrality',
            comment='eval = avg(networkx.newman_betweenness_centrality(G).values())'
            )

        plot_genericevaluation(
            genericevaluation( path, networx.number_of_cliques ,range ),
            savepath, title='number of cliques',
            comment='Function: networkx.number_of_cliques'
            )

        eval = lambda G: networkx.number_connected_components(G.to_undirected())
        eval.__name__ = 'number_connected_components'
        plot_genericevaluation(
            genericevaluation( path, eval ,range ),
            savepath, title='number_connected_components',
            comment='eval = nx.number_connected_components(G.to_undirected())'
            )

        # avg of (standard deviation in trust received by a user
        # who received at least x trust statements)
        comment='''\
    cont = [] # controversiality array

    for n in K.nodes_iter():
        in_edges = K.in_edges(n)
        
        # min_in_degree -> writte in name of function
        if len(in_edges)<min_in_degree:
            continue

        cont.append(
            numpy.std([_obs_app_jour_mas_map[x[2]['level']] for x in in_edges])
        )

    return avg(cont)'''
        plot_genericevaluation(
            genericevaluation( path, avgcont20 ,range ),
            savepath, title='avg of standard deviation in received trust',
            comment=comment
            )


    # can we erase this?
    if len(sys.argv) == 6:
        html = sys.argv[5]
        f = file( os.path.join( savepath, html ) , 'w' )
        fd = file( os.path.join( savepath, '.data' ) , 'w' )

        html,data = createHTML( ta )
        f.write(html)
        fd.write(data)
        f.close()
        fd.close()
