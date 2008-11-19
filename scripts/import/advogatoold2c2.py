#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
create c2 from certs text format:

raph miguel Master
raph jacob Journeyer
...

filename: advogato.org.certs-20030304

key of c2:
{'network':'Advogato','date','2003-03-04'}

USAGE
   ./advogatoold2c2.py [path_directory [bast_path_output]]
'''

import sys,os,re
from os.path import isfile,join
from trustlet.Dataset.Network import WeightedNetwork
from trustlet.helpers import pool,save
from trustlet.Dataset.Advogato import _obs_app_jour_mas_map,_color_map

refname = re.compile('advogato(?:\.org)?\.certs-(\d{4})(\d{2})(\d{2})')

levels = filter(None,_obs_app_jour_mas_map.keys())
colors = filter(None,_color_map.keys())

islevel = lambda x: x in levels
iscolor = lambda x: x in colors

if 'help' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
    print __doc__

if sys.argv[1:]:
    path = sys.argv[1]
else:
    path = os.curdir

if sys.argv[2:]:
    output_path = sys.argv[2]
else:
    output_path = os.curdir

for dataset in os.listdir(path):
    r = refname.match(dataset)
    if not r:
        continue
    date = '-'.join(r.groups())

    W = WeightedNetwork()

    key = None
    for line in file(join(path,dataset)):
        s,t,e =  line.split()

        if not key:
            if islevel(e):
                key = 'level'
            elif iscolor(e):
                key = 'color'
            else:
                assert False

        W.add_node(s)
        W.add_node(t)
        W.add_edge(s,t,pool({key:e}))
        
    assert save({'network':'Advogato','date':date},W,join(output_path,date,'graph.c2'))    
