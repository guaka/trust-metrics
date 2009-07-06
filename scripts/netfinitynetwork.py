#!/usr/bin/env python

'''
getnetfinitynetwork <input>

input:
contains edges
<from> <to> <value>

'''

import sys
import os
import re
from trustlet import *

f = file(sys.argv[1])
edges = [(lambda x: (x[0],x[1],int(x[2])))(x.strip().split()) for x in f if x.strip()]
f.close()

re_date = re.compile('netfinitynetwork-([0-9-]{10}).txt')

date = re_date.match(sys.argv[1]).group(1)

users = set([x[0] for x in edges])

N = WeightedNetwork()
U = WeightedNetwork()

for u,v,e in edges:
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
