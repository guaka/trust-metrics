#!/usr/bin/env python


'''
usage: convert_cache.py [src_path] dst_path

Default src_path is .
'''
from trustlet.helpers import convert_cache,save,load,mkpath
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

if 'test' in sys.argv[1:]:
    data = [
        ({1:2,2:'due','3':-3},'ciao'),
        ({},range(5)),
        ({'q':'w','e':0.098},{}),
        ({0.1:2341222},[(1,2,3),{2:32}])
        ]

    mkpath('testcache')
    for k,v in data:
        save(k,v,'testcache')
        save(k,v,'testcache.c2')
    
    convert_cache('testcache','testcache_converted.c2')

    try:
        for k,v in data:
            v1 = load(k,'testcache')
            v2 = load(k,'testcache.c2')
            v2c = load(k,'testcache_converted.c2')
            
            assert v == v1
            assert v == v2
            assert v == v2c
            #print v,v2c
    finally:
        os.remove('testcache.c2')
        os.remove('testcache_converted.c2')
        os.system('rm -Rf testcache')

    exit()

if __name__=="__main__":
    main()
