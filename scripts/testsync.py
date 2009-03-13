#!/usr/bin/env python

'''
script to test sync.py

Execute this on some clients to test if sync works in a concurrency environment.
'''

import sys
import os
import os.path as path
import time
import random
from socket import gethostname

from trustlet.helpers import save,load,read_c2

randomsleep = lambda x,y: time.sleep(random.randint(x,y))

PATH = path.join(os.environ['HOME'],'shared_datasets','sync.test.c2')
TESTCOMMENT = '--- Test Sync'

def main():
    if sys.argv[1:]:
        sync = sys.argv[1] + ' ' + TESTCOMMENT
    else:
        print 'Usage: ./testsync.py path/sync.py'
        exit(1)

    for cnt in xrange(1000):

        assert 0==os.system(sync)

        assert save({'cnt':cnt,'hname':gethostname()},time.time(),PATH)

        
        c2 = read_c2(PATH)

        #debug
        print cnt
        print c2
        print
        print [x for x in c2 if thishost(x)]

        if len([x for x in c2 if thishost(x)])==cnt+1:
            print 'Bug! Bug! Bug!'
        
        randomsleep(5,10)

def thishost(x):
    '''
    return True if x obj war inserted by this host
    '''
    for k,v in x:
        if k=='hname' and v==gethostname():
            return 1
    return 0

if __name__=="__main__":
    main()
