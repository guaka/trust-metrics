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

    ps = []
 
    for p in args:
        p = path.abspath(p)

        if not p.startswith(path.join(HOME,'datasets')):
            print 'Path to remove have to be in ~/datasets dir'
            print '(%s)'%p
            return

        if path.isfile(p):
            os.remove(p)
        elif path.isdir(p):
            shutil.rmtree(p)
        else:
            print 'File %s doesn\'t exists' % p
            continue

        # path to hidden path
        ps.append(p.replace(path.join(HOME,'datasets'),path.join(HOME,'.datasets')))

    os.chdir(path.join(HOME,'.datasets'))
    for p in ps:
        assert not os.system(SVNRM % p),SVNRM % p
    assert not os.system(SVNCI)

if __name__=="__main__":
    main(sys.argv[1:])
