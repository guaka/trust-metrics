#!/usr/bin/env python

#recursive delete

import os

def rec_delete(path):
    """
    return list of .svn path folder start in this directory
    """
    list = []
    print path

    for x in os.listdir(path):
        abspath = os.path.join( path,x )

        if os.path.isdir(abspath) and '.svn' not in abspath:
            list = list + rec_delete( abspath )

        if os.path.isdir(abspath) and '.svn' in abspath:
            list.append(abspath)
        

    return list

if __name__ == '__main__':
    
    import sys
    from shutil import rmtree

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '.'

    l = rec_delete(path)
    
    for x in l:
        rmtree( x )

    print ".svn folder removed!"
    
