#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Script to convert xml of Wikipedia dataset in a/some graph(s)
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
import optparse
from trustlet.conversion import *

def main():

    p = optparse.OptionParser(usage="usage: %prog [options] files")

    p.add_option("-b", "--base-path", help='Output directory')
    p.add_option("-c", "--current", help='Input file is current xml', action='store_true', default=False)
    p.add_option("-d", "--distrust", help='Compute also distrust graph (input have to be pages-meta-hisory xml)', action='store_true', default=False)
    p.add_option("-t", "--threshold", help='remove edge if weight is less then value', default=0, dest='value')
    p.add_option("-l", "--lists", help='download list of users from wikipedia.org', action='store_true', default=False)

    opts, files = p.parse_args()

    if opts.current:
        t = 'c'
        outputname = 'graphCurrent'
    else:
        t = 'h'
        outputname = 'graphHistory'

    if files:

        params = []

        print 'Output file(s):'

        for xml in files:

            filename = os.path.split(xml)[1] #rm dir
            size = os.stat(xml).st_size

            # lang, date
            s = os.path.split(xml)[1]
            lang = s[:s.index('wiki')]
            res = re.search('wiki-(\d{4})(\d{2})(\d{2})-',s)
            date = '-'.join([res.group(x) for x in xrange(1,4)])
            assert isdate(date)

            if not opts.base_path:
                assert os.environ.has_key('HOME')
                opts.base_path = os.path.join(os.environ['HOME'],'shared_datasets')

            path = os.path.join(opts.base_path,'WikiNetwork',lang,date)
            mkpath(path)

            output = os.path.join(path,outputname+'.c2')

            params.append((xml,output,t,opts.distrust,opts.value,opts.lists,True))

            print output

        splittask(lambda x: wikixml2graph(*x),params)

    else:
        print 'use --help'

if __name__=="__main__":
    main()
