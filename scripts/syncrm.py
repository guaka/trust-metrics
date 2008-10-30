#!/usr/bin/env python

'''
Works only if there are links datasets and .datasets in home dir
'''

import sys
import os
import shutil
import os.path as path

SVNRM = 'svn rm "%s"'
SVNCI = 'svn ci --username anybody --password a -m="auomatic commit (syncrm.py)"'
HOME = os.environ['HOME']

def main(args):
    if not args:
        return
    
    p = path.abspath(args[0])

    if not p.startswith(path.join(HOME,'datasets')):
        print 'Path to remove have to be in ~/datasets dir'
        return

    if path.isfile(p):
        os.remove(p)
    elif path.isdir(p):
        shutil.rmtree(p)
    else:
        assert 0,'File %s doesn\'t exists' % p

    # path to hidden path
    p = p.replace(path.join(HOME,'datasets'),path.join(HOME,'.datasets'))
    os.chdir(path.join(HOME,'.datasets'))
    
    assert not os.system(SVNRM % p),SVNRM % p
    assert not os.system(SVNCI)

if __name__=="__main__":
    main(sys.argv[1:])
