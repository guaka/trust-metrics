#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
USAGE:
   ./wikixml2graph.py xml_file [base_path]
      [--current]
      [--distrust] [--threshold value|-t value] [--no-lists]
          Default base_path = home-dir/shared_datasets
          If --current isn't set, it'll use history xml
          If xml_file is no-graph will insert only lists of users in .c2
          distrust: force distrust graph creation (input file must be pages-meta-history)
          threshold: remove edge if weight is less then value
          no-lists: don't download list of users from wikipedia.org
'''

from xml import sax
from trustlet.Dataset.Network import Network,WeightedNetwork
from trustlet.helpers import *
from networkx import write_dot
from string import index, split
from sys import stdin,argv
import os,re,time
import urllib
from gzip import GzipFile
from trustlet.conversion import *

def main():

    if '--current' in argv:
        t = 'c'
        outputname = 'graphCurrent'
        
        argv.remove('--current')
    else:
        t = 'h'
        outputname = 'graphHistory'
        
        if '--history' in argv:
            argv.remove('--history')
        
    if '--distrust' in argv:
        argv.remove('--distrust')
        distrust = True
    else:
        distrust = False

    threshold = 0
    if '--threshold' in argv[:-1]:
        i = argv.index('--threshold')
        threshold = int(argv[i+1])
        del argv[i+1]
        del argv[i]
    elif '-t' in argv[:-1]:
        i = argv.index('-t')
        threshold = int(argv[i+1])
        del argv[i+1]
        del argv[i]

    if '--no-lists' in argv:
        argv.remove('--no-lists')
        downloadlists = False
    else:
        downloadlists = True

    if len(argv[1:]):

        xml = argv[1]
        filename = os.path.split(xml)[1] #rm dir
        size = os.stat(xml).st_size

        # lang, date
        s = os.path.split(xml)[1]
        lang = s[:s.index('wiki')]
        res = re.search('wiki-(\d{4})(\d{2})(\d{2})-',s)
        date = '-'.join([res.group(x) for x in xrange(1,4)])
        assert isdate(date)

        if argv[2:]:
            base_path = argv[2]
        else:
            assert os.environ.has_key('HOME')
            base_path = os.path.join(os.environ['HOME'],'shared_datasets')

        path = os.path.join(base_path,'WikiNetwork',lang,date)
        mkpath(path)

        output = os.path.join(path,outputname+'.c2')

        wikixml2graph(xml,output,t,distrust,threshold,downloadlists,True)

        print 'Output file:',output

    else:
        print __doc__

if __name__=="__main__":
    main()
