#!/usr/bin/env ipython

'''
getnetfinitynetwork <input> [<names>]

input:
contains edges
<from> <to> <value>

names:
une name per line for nodes

If obfuscation.map is present, it will be used.
'''

import sys
import os
import random
import re
from trustlet import *

f = file(sys.argv[1])
edges = [(lambda x: (x[0],x[1],int(x[2])))(x.strip().split()) for x in f if x.strip()]
f.close()

if sys.argv[2:]:
    f = file(sys.argv[2])
    names = set([x.strip() for x in f.readlines() if x.strip() and x.strip()[0]!='#'])
    f.close()
else:
    names = []

oedges = []
obfuscation = {}

if os.path.isfile('obfuscation.map'):
    print 'Reading obfuscation'
    f = file('obfuscation.map')

    for x in f:
        n,o = x.strip().split()
        assert n not in obfuscation
        obfuscation[n] = o
    f.close()

names.difference_update(set(obfuscation.itervalues()))

random.shuffle(edges)
cont = 0
for u,v,e in edges:
    if not u in obfuscation:
        if names:
            obfuscation[u] = names.pop()
        else:
            obfuscation[u] = str(cont)
            cont += 1
    if not v in obfuscation:
        if names:
            obfuscation[v] = names.pop()
        else:
            obfuscation[v] = str(cont)
            cont += 1
    oedges.append((obfuscation[u],obfuscation[v],e))

re_date = re.compile('netfinitynetwork-([0-9-]{10}).txt')

date = re_date.match(sys.argv[1]).group(1)

users = set([x[0] for x in oedges])

N = WeightedNetwork()
U = WeightedNetwork()

for u,v,e in oedges:
    N.add_node(u)
    N.add_node(v)
    N.add_edge(u,v,{'value':e})

    if v in users:
        U.add_node(u)
        U.add_node(v)
        U.add_edge(u,v,{'value':e})
        

U.filepath = N.filepath = os.path.join(relative_path(N.filepath,'datasets')[0].replace('datasets','shared_datasets'),'NetfinityNetwork',date)
N._cachedict = {'date':date}
U._cachedict = {'date':date,'type':'users'}

N.save_c2()
U.save_c2()
print 'Saved in',N.filepath

f = file('obfuscation.map','w')
for k,v in obfuscation.iteritems():
    f.write(str(k)+' '+str(v)+'\n')
f.close()
