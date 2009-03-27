#!/usr/bin/env python

'''\
shows one or more c2 files on shell.
'''
import sys
import os,pickle
import time
import os.path as path
from gzip import GzipFile
import optparse

# not show: /usr/lib/python2.6/site-packages/networkx/hybrid.py:16: DeprecationWarning: the sets module is deprecated
stderr = sys.stderr
sys.stderr = file('/dev/null','w')
from trustlet.helpers import getfiles,read_c2
sys.stderr = stderr

def main():
    
    o = optparse.OptionParser(usage='usage: %prog [-r] [file1 [file2] [...]]')
    o.add_option('-r','--recursive',help='recursive',default=False,action='store_true')
    o.add_option('-l','--short-line',help='trunc each line to 80 chars',default=False,action='store_true')
    o.add_option('-k','--keys',help='show keys',default=False,action='store_true')
    o.add_option('-v','--values',help='show values',default=False,action='store_true')
    o.add_option('-i','--info',help='show timestamps, hostnames, ...',default=False,action='store_true')
    o.add_option('-d','--debug',help='show debug info',default=False,action='store_true')
    o.add_option('-a','--all',help='enable all info',default=False,action='store_true')

    opts, files = o.parse_args()

    # enable all
    if opts.all:
        opts.keys = opts.values = opts.info = opts.debug = True

    # if no options is setted, enable keys
    if not any(opts.__dict__.values()):
        opts.keys = True

    if not files:
	o.print_help()
	return

    #format line
    line = opts.short_line and (lambda l: l[:80]) or (lambda l: l)

    if opts.recursive:
        allfiles = []
        for file in files:
            if path.isdir(file):
                for dir,ds,fs in os.walk(file):
                    allfiles += [path.join(dir,x) for x in fs]
        files = allfiles
    #print files
    for file in files:
        if not file.endswith('.c2'):
            continue
        if len(files)>1:
            print '_'*len(file)
            print file
            print
        
        c2 = read_c2(file)
        #info
        print 'Number of items',len(c2)
        for i,(k,v) in enumerate(c2.items()):
            print '~ Item %d ~'%i
            if opts.keys:
                print line('Key: '+str(k))
            if opts.values:
                if type(v) is dict and 'dt' in v:
                    print line('Value: '+str(v['dt']))
                else:
                    print line(str(v))
            if opts.info and type(v) is dict:
                if 'ts' in v:
                    print 'Timestamp:',time.ctime(v['ts'])
                else:
                    print 'No timestamp'
                if 'hn' in v:
                    print 'Hostname:',v['hn']
                else:
                    print 'No hostname'
            if opts.debug:
                if type(v) is dict and 'db' in v:
                    print line(' '+str(db))
                else:
                    print 'No debug info'

if __name__=="__main__":
    main()
