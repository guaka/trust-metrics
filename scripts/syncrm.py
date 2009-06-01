#!/usr/bin/env python

import os
import optparse

def remove(f):

    print 'Removed',f
    f = file(f,'w')
    f.write('removed')
    f.close()    

def main():
    
    o = optparse.OptionParser(usage='usage: %prog [-r] [[[file1 [file2]] dir1] ...] ')
    o.add_option('-r','--recursive',default=False,action='store_true')
    
    opts, args = o.parse_args()

    for name in args:
        if os.path.isdir(name) and opts.recursive:
            for path,dirs,files in os.walk(name):
                for file in files:
                    remove(os.path.join(path,file))
        if os.path.isfile(name):
            remove(name)

main()

