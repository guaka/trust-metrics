#!/usr/bin/env python
"""
This script take a list of dot files (or c2 files) that contains a graph
and create a default path with the information stored in the name of the file.
ex:
robots_net-graph-2008-07-24.dot --> robots_net/2008-07-24/graph.dot

You can use this script to automatically create a default structure for the datasets folder
"""
from trustlet.helpers import mkpath
from shutil import move
from os import remove,listdir
from os.path import join,split,sep,isdir
import re

def main( graphList ):
    
    redate = re.compile( "[0-9]{4}-[0-9]{2}-[0-9]{2}" )
    rename = re.compile( "[a-z_]+" )

    for graph in graphList:
        # check
        if isdir( graph ) or '.dot' not in graph:
            continue

        print "processing", graph

        path,graphname = split( graph )
        

        try:
            date = redate.findall( graphname )[0]
            name = rename.findall( graphname )[0]
        except:
            continue

        classname = name[0].upper()+name[1:]+'Network'

        dest = join( path , classname , date )
        mkpath( dest )
        move( graph, join( dest, "graph.dot" ) )
        


if __name__ == "__main__":
    import sys


    if len( sys.argv ) > 1:
        if sys.argv[1] == 'help':
            print """
This script take a list of dot files (or c2 files) that contains a graph
and create a default path with the information stored in the name of the file.
ex:
robots_net-graph-2008-07-24.dot --> robots_net/2008-07-24/graph.dot

You can use this script to automatically create a default structure for the datasets folder
"""

        main( sys.argv[1:] )
    else:
        print """
This script take a list of dot files (or c2 files) that contains a graph
and create a default path with the information stored in the name of the file.
ex:
robots_net-graph-2008-07-24.dot --> robots_net/2008-07-24/graph.dot

You can use this script to automatically create a default structure for the datasets folder
"""
        
