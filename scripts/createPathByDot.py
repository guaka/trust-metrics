#!/usr/bin/env python
"""
This script take a list of dot files (or c2 files) that contains a graph
and create a default path with the information stored in the name of the file.
ex:
robots_net-graph-2008-07-24.dot --> robots_net/2008-07-24/graph.dot
"""
from trustlet.helpers import mkpath
from shutil import move
from os import remove,listdir
from os.path import join,sep
import re

def main( graphList ):
    
    redate = re.compile( "[0-9]{4}-[0-9]{2}-[0-9]{2}" )
    rename = re.compile( "[a-z_]+" )

    for graph in graphList:
        print "processing", graph

        date = redate.findall( graph )[0]
        name = rename.findall( graph )[0]
        
        dest = join( "." , name , date )
        mkpath( dest )
        move( graph, join( dest, "graph.dot" ) )
        


if __name__ == "__main__":
    import sys

    if len( sys.argv ) > 1:
        main( sys.argv[1:] )
    else:
        #assume *
        main( listdir( "." ) )
        
