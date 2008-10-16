#!/usr/bin/env python

'''\
shows one or more c2 files on shell.

lsc2 [-r] [file1 [file2] [...]]

-r: recursive
'''

import sys,os,pickle
import os.path as path
from trustlet.helpers import getfiles,read_c2
from gzip import GzipFile

def main():
    
    if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) == 1:
        print __doc__
        return

    files = filter(lambda x:x[0]!='-',sys.argv[1:])
    recursive = '-r' in sys.argv[1:] or '-R' in sys.argv[1:]

    if recursive:
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
        print file
        for k,v in read_c2(file).items():
            if type(k) is frozenset:
                print ' '+str(k)[:79]
            else:
                print ' '+str(v)[:79]
            

if __name__=="__main__":
    main()
