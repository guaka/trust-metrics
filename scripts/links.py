#!/usr/bin/env python

"""
Makes symbolic links from development path (local svn
repository directory) to installation path in order to
avoid reinstallation of trustlet every change.
"""

USAGE = """\
USAGE:
# link.py [development path [installation path]]\
"""

from os.path import join,exists
import sys,os,os.path

class Bug(Exception):
    pass

DEBUG = False

DEFDEVPATH = './trustlet'
DEFINSPATH = '/usr/lib/python2.5/site-packages/trustlet/'

def main():

    if DEBUG:
        print "DEBUG MODE"
    if 'help' in sys.argv[1:] or '--help' in sys.argv[1:]:
        print USAGE
        sys.exit()
    
    print "links.py is dangerous!"
    print "backup your installation dir!"
    raw_input("Press enter key to continue.")

    try:
        devpath = sys.argv[1]
    except IndexError:
        devpath = DEFDEVPATH
        print 'default development path:',DEFDEVPATH
    try:
        inspath = sys.argv[2]
    except IndexError:
        inspath = DEFINSPATH
        print 'default installation path:',DEFINSPATH

    devpath = os.path.abspath(devpath)
    inspath = os.path.abspath(inspath)

    def getfiles(basedir,dir=''):
        curpath = join(basedir,dir)
        ret = []
        for f in os.listdir(curpath):
            if os.path.isdir(join(curpath,f)):
                ret += getfiles(basedir,join(dir,f))
            else:
                ret.append(join(dir,f))
        return ret
        #print file

    files = getfiles(inspath)
    #list of files to link

    for f in files:
        if DEBUG:
            print "os.remove(%s)" % join(inspath,f)
        else:
            os.remove(join(inspath,f))
        if exists(join(devpath,f)) and f[-4:]!='.pyc':
            #doesn't exist os.sln()?
            if DEBUG:
                print 'ln -s ' + join(devpath,f) + ' ' + join(inspath,f)
            elif os.system('ln -s ' + join(devpath,f) + ' ' + join(inspath,f)):
                raise Bug

if __name__=="__main__":
    main()
