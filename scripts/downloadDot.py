#!/usr/bin/env python

"""
this script download from trustlet.org all the datasets of a type of network (Supported: advogato, kaitiaki, squeakfoundation, robots_net)
and optionally use createPathByDot script to create the directory tree
"""
import sys,os
from createPathByDot import createTreeFolder
from trustlet.helpers import mkpath

def downloadDot( savepath, nettype, createTree ):
    
    mkpath( savepath )

    try:
        os.chdir( savepath )
    except:
        print "bad path"
        sys.exit(1)

    print "Downloading...."
    print "wget -rND -R index* "+os.path.join( "http://www.trustlet.org/datasets/", nettype )+os.path.sep
    
    try:
        os.system( "wget -r -nd -R index* "+os.path.join( "http://www.trustlet.org/datasets/", nettype )+os.path.sep ) 
    except:
        print "To use this script you must have wget installed"
        sys.exit(1)
    
    if createTree:
        createTreeFolder( os.listdir( '.' ) )
    
    return



if __name__ == "__main__":
    
    path = '.'
    name = 'advogato'
    tree = False
    nameposition = pathposition = -1

    for i in xrange( len(sys.argv) ):
        if '-n' == sys.argv[i] or '--name' == sys.argv[i]:
            nameposition = i
            
        if '-p' == sys.argv[i] or '--save-path' == sys.argv[i]:
            pathposition = i

    
    if '-n' in sys.argv or '--name' in sys.argv:

        try:
            name = sys.argv[nameposition+1]
        except:
            print "I cannot be able to understand the name of network"
            sys.exit(1)

            
    if '-t' in sys.argv or '--create-directory-tree' in sys.argv:
        tree = True
    else:
        tree = False

    if '-p' in sys.argv or '--save-path' in sys.argv:
        try:
            path = sys.argv[pathposition+1]
        except:
            print "I cannot be able to find the path"
            sys.exit(1)

    downloadDot( path, name, tree )

    sys.exit(0)
