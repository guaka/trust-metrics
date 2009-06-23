#!/usr/bin/env ipython

'''
getnetfinitynetwork <input> [[<names>] map]

input:
contains edges
<from> <to> <value>

names:
une name per line for nodes
'''

import sys
import os
import random
import re
from trustlet import *

f = file(sys.argv[1])
edges = [tuple(map(int,x.strip().split())) for x in f.readlines()]
f.close()

if sys.argv[2:]:
    f = file(sys.argv[2])
    names = [x.strip() for x in f.readlines()]
    random.shuffle(names)
    f.close()
else:
    names = []

oedges = []
obfuscation = {}

random.shuffle(edges)
cont = 0
for u,v,e in edges:
    if not u in obfuscation:
        if names:
            obfuscation[u] = names.pop()
        else:
            obfuscation[u] = cont
            cont += 1
    if not v in obfuscation:
        if names:
            obfuscation[v] = names.pop()
        else:
            obfuscation[v] = cont
            cont += 1
    oedges.append((obfuscation[u],obfuscation[v],e))

re_date = re.compile('netfinitynetwork-([0-9-]{10}).txt')

date = re_date.match(sys.argv[1]).group(1)

N = WeightedNetwork()

for u,v,e in oedges:
    N.add_node(u)
    N.add_node(v)
    N.add_edge(u,v,{'value':e})

N.filepath = os.path.join(relative_path(N.filepath,'datasets')[0].replace('datasets','shared_datasets'),'NetfinityNetwork',date)
N._cachedict = {'date':date}

N.save_c2()
print 'Saved in',N.filepath

if 'map' in sys.argv or 1:
    print 'Saved '+date+'.map'
    f = file(date+'.map','w')
    for k,v in obfuscation.iteritems():
        f.write(str(k)+' '+str(v)+'\n')
    f.close()
