#!/usr/bin/env python

"""
this script download from trustlet.org all the datasets of a type of network (Supported: advogato, kaitiaki, squeakfoundation, robots_net)
and optionally use createPathByDot script to create the directory tree
"""
import sys,os
from createPathByDot import createTreeFolder
from trustlet.helpers import mkpath

def downloadDot( savepath, nettype, wget, createTree ):
    
    mkpath( savepath )

    try:
        os.chdir( savepath )
    except:
        print "bad path"
        sys.exit(1)

    print "Downloading...."
    if not wget:
        command = "wget -r -nd -R index* "+os.path.join( "http://www.trustlet.org/datasets/", nettype )+os.path.sep
    else:
        command = wget+" -r -nd -R *.html,*.php "+os.path.join( "http://www.trustlet.org/datasets/", nettype )+os.path.sep

    print command

    try:
        os.system( command ) 
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
    wget = None

    nameposition = pathposition = wgetposition = -1

    argc = len(sys.argv)

    if argc == 1 or "--help" in sys.argv or "-h" in sys.argv:
        print "USAGE: python downloadDot.py [-n|--name] network_name [-p|--save-path] path [-t|--create-directory-tree]"
        print "NB: if you haven't wget installed you can pass another parameter [--wget-bin|-w] path_to_wget_bin"
        sys.exit(0)


    for i in xrange( len(sys.argv) ):
        if '-n' == sys.argv[i] or '--name' == sys.argv[i]:
            nameposition = i
        
        if '-w' == sys.argv[i] or '--wget-bin' == sys.argv[i]:
            wget = sys.argv[i+1]
    
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

    downloadDot( path, name, wget, tree )

    sys.exit(0)
