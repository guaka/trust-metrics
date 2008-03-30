#!/usr/bin/env python
#script per legare i file di sviluppo di trustlet con i file
#installati tramite link simbolici
#(in modo da non dover reinstallare trustlet ad ogni modifica)

"""# link.py [development path] [installation path]"""

from os.path import join,exists
import sys,os,os.path

DEFDEVPATH = './trustlet'
DEFINSPATH = '/usr/lib/python2.5/site-packages/trustlet/'

class Bug(Exception):
    pass

def main():
    if 'help' in sys.argv[1:] or '--help' in sys.argv[1:]:
        print __doc__
        sys.exit()
    try:
        devpath = sys.argv[1]
    except IndexError:
        devpath = DEFDEVPATH
    try:
        inspath = sys.argv[2]
    except IndexError:
        inspath = DEFINSPATH

    devpath = os.path.abspath(devpath)
    inspath = os.path.abspath(inspath)

    #print os.path.join(devpath,"qwe")
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
    #lista dei file da linkare
    
    for f in [join(inspath,f) for f in files]:
        os.remove(f)
    for f in files:
        if exists(join(devpath,f)) and f[-4:]!='.pyc':
            if os.system('ln -s ' + join(devpath,f) + ' ' + join(inspath,f)):
                raise Bug

if __name__=="__main__":
    main()
