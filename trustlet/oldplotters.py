#made by Danilo Tomasoni            

def plotparameters( tuplelist, path, onlyshow=False, title='Moletrust Accuracy',
                    xlabel='horizon', ylabel='abs error', log=False,
                    onlypoint=False, istogram=False ):
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

def prettyplot_old( data, path, **args):
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

    import Gnuplot
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
