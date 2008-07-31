#!/usr/bin/env python

import sys,os,pickle
from os import path
from trustlet.helpers import getfiles
from gzip import GzipFile

def main():
    
    files = filter(lambda x:x[0]!='-',sys.argv[1:])
    recursive = '-r' in sys.argv[1:] or '-R' in sys.argv[1:]

    if recursive:
        allfiles = []
        for file in files:
            if path.isdir(file):
                allfiles += getfiles(file)
            else:
                allfiles.append(file)
        files = allfiles

    for file in files:
        if not file.endswith('.c2'):
            continue
        print file
        for v in pickle.load(GzipFile(file)).values():
            print ' '+v.__str__()[:79]
            

if __name__=="__main__":
    main()
