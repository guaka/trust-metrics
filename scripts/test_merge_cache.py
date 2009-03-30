#!/usr/bin/env python

'''
test merge cache.
Check if multiple c2 + merge 
'''

import os
import random
from trustlet import *

NVALUES = 100
NKEYS = 30
NC2 = 10

path = lambda x: '/tmp/test%d.c2'%x

# we'll generate random data that will put in data and in c2
data = {}

os.system('touch /tmp/test0.c2')
os.system('rm /tmp/test*.c2')

kk = []
pp = set()

for i in xrange(NVALUES):
    k = random.randint(0,NKEYS)
    kk.append(k)
    v = random.random()
    p = path(random.randint(0,NC2))
    pp.add(p)
    print k,v,p
    assert save(k,v,p)
    data[k] = v

#print len(data),len(kk)
#print sorted(kk)
pp = list(pp)

out = pp[random.randint(0,NC2)]
#out = '/tmp/testout.c2'

#print 'Output file',out

merge_cache(pp,out)
#merge_cache(pp,out)

c2 = read_c2(out)

for k,v in c2.iteritems():
    assert k in data
    assert data[k] == v['dt']
