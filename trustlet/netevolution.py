#!/usr/bin/env python
"""
This package contains all the function 
on the evolution of a network
"""
from trustlet.helpers import prettyplot,splittask,save,load
from trustlet.Dataset import Network
from trustlet.Dataset.Advogato import _color_map,_obs_app_jour_mas_map
from networkx import read_dot
import os,time,re

stringtime2int = lambda s: int(time.mktime( (int(s[:4]), int(s[5:7]), int(s[8:10]), 0, 0, 0, 0, 0, 0) ))
inttime2string = lambda i: "%.4d-%.2d-%.2d"%time.gmtime(i)[:3]

def no_observer(n1,n2,e):
    return e['level']!='Observer'


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
    
    def eval( K, d ):
    #for d in fdate:
        at = load( {'function':'trustAverage', 'date':d}, os.path.join(path,d) )
        if at != None:
            return (d,at)

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

        save( {'function':'trustAverage', 'date':d}, averagetrust ,os.path.join(path,d) )
        
        print "dataset of ",d ," Evaluated"
        return (d,averagetrust)
    
    if noObserver:
        return evolutionmap( path, eval, (fromdate,todate), no_observer )
    else:
        return evolutionmap( path, eval, (fromdate,todate) )

def ta_plot(ta, path, filename="trustAverage.png"):
    prettyplot( ta, os.path.join(path,filename), title="Trust Average on time", showlines=True, xlabel='date in seconds',ylabel='trust average')

def evolutionmap(path,function,range=None,filter_edges=None):
    '''
    apply function function to each network in range range.
    If you want use cache function and filter_edges cannot be lambda functions.
    '''
    cachepath = 'netevolution.c2'
    redate = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
    dates = [x for x in os.listdir(path) if re.match(redate,x) and os.path.exists(os.path.join(path,x,'graph.dot'))]

    if range:
        assert re.match(redate,range[0]) and  re.match(redate,range[1])
        dates = [x for x in dates if x>=range[0] and x<=range[1]]

    print "There are %d networks" % len(dates)

    def task(date):
        print date
        #cache
        if function.__name__=='<lambda>' or filter_edges and filter_edges.__name__=='<lambda>':
            print "i can't save cache with lambda funtions"
        else:
            cachekey = {'function':function.__name__,'date':date}
            if filter_edges:
                cachekey['filter edges'] = filter_edges.__name__
            cache = load(cachekey,path=os.path.join(path,cachepath))
            if cache:
                return cache
        
        G = read_dot(os.path.join(path,date,'graph.dot'))
        K = Network.WeightedNetwork()
        if filter_edges:
            for e in G.edges_iter():
                if filter_edges(*e):
                    K.add_edge(*e)
            print "keeped nodes %.2f%%" % (100.0 * len(K.edges()) / len(G.edges()))
        else:
            K.paste_graph(G)
        res = function(K,date)
        if function.__name__!='<lambda>' and not filter_edges or filter_edges.__name__!='<lambda>':
            if filter_edges:
                cachekey['filter edges'] = filter_edges.__name__
            save(cachekey,res,human=True,path=os.path.join(path,cachepath))
        return res

    #return [task(x) for x in dates]
    return splittask(task,dates)


def usersgrown(path,range=None):
    '''
    return the number of user for each network in date range
    '''
    def usersgrown(K,date):
        return ( stringtime2int(date),len(K.nodes()) )
        #return ( date,len(K.nodes()) )
    
    return evolutionmap(path,usersgrown,range)

def plot_usersgrown(data,path='.'):
    '''
    data is the output of usersgrown
    >>> plot_usersgrown(usersgrown('trustlet/datasets/Advogato',range=('2000-01-01','2003-01-01')))
    '''
    data.sort()
    fromdate = inttime2string(data[0][0])
    todate = inttime2string(data[-1][0])
    prettyplot(data,os.path.join(path,'usersgrown (%s %s).png'%(fromdate,todate)),
               title='Users Grown',
               xlabel='date [s] (from %s to %s)'%(fromdate,todate),
               ylabel='n. of users',
               showlines=True
               )

def edgespernode(path,range=None, noObserver=False):
    '''
    return the average number of edges for each user
    '''
    def edgespernode_nodes(K,date):
        nodes = len(K.nodes())
        return ( nodes , 1.0*len(K.edges())/nodes )
    
    if noObserver:
        return evolutionmap(path,edgespernode_nodes,range,no_observer)
    else:
        return evolutionmap(path,edgespernode_nodes,range)

def plot_edgespernode(data,path='.'):
    '''
    data is the output of edgespernode
    '''
    data.sort()
    fromnnodes = data[0][0]
    tonnodes = data[-1][0]
    prettyplot(data,os.path.join(path,'edgespernode (%d %d).png'%(fromnnodes,tonnodes)),
               title='Average Edges per Node',
               xlabel='nodes',
               ylabel='number of edges per node',
               showlines=True
               )

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
    path = sys.argv[3]
    savepath = sys.argv[4]    


    ta = trustAverage( startdate, enddate, path)
    ta.sort()
    
    ta_plot( [(stringtime2int(x),y) for (x,y) in ta], savepath )
    plot_edgespernode( edgespernode( path,(startdate,enddate) ), savepath )
    plot_usersgrown( usersgrown( path,(startdate,enddate) ), savepath )


    if len(sys.argv) == 6:
        html = sys.argv[5]
        f = file( os.path.join( savepath, html ) , 'w' )
        fd = file( os.path.join( savepath, '.data' ) , 'w' )

        html,data = createHTML( ta )
        f.write(html)
        fd.write(data)
        f.close()
        fd.close()
