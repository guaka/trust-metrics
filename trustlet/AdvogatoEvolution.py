import re
from trustlet import *
from networkx import write_dot
import os

def evaluate( net ):
    """
    this function must be called first, it generate
    all the data used to plot the graphics.
    Before evaluate was successfully terminated
    You can call plotOverTime, and pass to it the result
    of evaluate function.
    If you evaluate twice the same thing, the evaluate 
    function be able to remember it.
    
    Parameters:
    net: the network on wich you would evaluate the history
    """

    return None

def plotOverTime( ls, toe ):
    """
    this function takes a list of error (the type is passed as second argument as a string)
    and plot it, with on x axes the time and y axes the list value.
    """
    return None

def parseTextData(loadpath,savepath):
    """
    this function parse a set of file, (it is in the 'path' passed as parameter)
    and create the correspond dataset, in datasets folder.
    """
    import os
    
    if not os.path.exists( loadpath ):
        raise IOError( "path %s does not exist" % loadpath )

    filelist = os.listdir( loadpath )
    
    def eval( f ):
    #for f in filelist:
        # I take the date from the name of file. (I love regular expression)
        date = '-'.join( [re.findall( '[0-9]{4}', f )[0], re.findall( '[0-9]{2}',  f )[2], re.findall('[0-9]{2}', f )[3]] )
        fd = file( os.path.join( loadpath, f ) ) #default is read
        net = Network.Network()
        
        for line in fd.readlines():
            line = line.strip()
            #parse the string in one line of code :)
            n1,n2,edge = line.split( ' ' )
            
            net.add_edge( n1,n2,{"level":edge})
            
        saved = os.path.join( savepath, date )
        os.mkdir( saved )
        write_dot( net, os.path.join( saved, 'graph.dot' ) )
        
        print "File %s computed and saved in %s" % (f,saved)
        return None

    return splittask( eval, [f for f in filelist], np=2 )


if __name__ == "__main__":
    parseTextData( '/home/ciropom/advogatoCerts','/home/ciropom/datasets/AdvogatoNetwork/' )
