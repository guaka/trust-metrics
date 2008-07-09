#!/usr/bin/env python


'''
usage: convert_cache.py [src_path] dst_path

Default src_path is .
'''
from trustlet.helpers import convert_cache
import sys,os

def main():
    if len(sys.argv)==1 or '--help' in sys.argv[1:]:
        print __doc__
        exit()
    if len(sys.argv)==2:
        srcpath = '.'
        dstpath = argv[1]
    elif len(sys.argv)==3:
        srcpath = sys.argv[1]
        dstpath = sys.argv[2]
    convert_cache(srcpath,dstpath)

if __name__=="__main__":
    main()
