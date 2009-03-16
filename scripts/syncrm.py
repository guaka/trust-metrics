#!/usr/bin/env python

'''
Remove file(s) from datasets dir
USAGE:
syncrm.py [[[[file0] file1] file2] ...]

Works only if there are datasets and .datasets links in home dir
'''

import sys
import os
import shutil
import os.path as path
from socket import gethostname

try:
    from sync import HIDDENDIR,DIR
except ImportError:
    HIDDENDIR = '.shared_datasets'
    DIR = 'shared_datasets'
    print 'Warning: sync.py not found'
    print 'Datasets dir:',DIR

HOSTNAME = gethostname()
SVNRM = 'svn rm --force "%s"'
SVNCI = 'svn ci --username anybody --password a -m "auomatic commit by %s (syncrm.py)"' % HOSTNAME
HOME = os.environ['HOME']

def main(args):
    if not args or '--help' in args or 'help' in args:
        print __doc__
        return

    ps = []
 
    for p in args:
        p = path.realpath(p)

        if not p.startswith(path.join(HOME,DIR)):
            print 'Path to remove have to be in %s dir' % path.join(HOME,DIR)
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
        ps.append(p.replace(path.join(HOME,DIR),path.join(HOME,HIDDENDIR)))

    os.chdir(path.join(HOME,HIDDENDIR))
    for p in ps:
        assert not os.system(SVNRM % p),SVNRM % p
    assert not os.system(SVNCI)

if __name__=="__main__":
    main(sys.argv[1:])
