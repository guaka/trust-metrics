#!/usr/bin/env python

'''
Usage:
  diffc2.py one.c2 two.c2

Note: f1 > f2 means that f1 contains f2
'''


import sys
# not show: /usr/lib/python2.6/site-packages/networkx/hybrid.py:16: DeprecationWarning: the sets module is deprecated
stderr = sys.stderr
sys.stderr = file('/dev/null','w')
from trustlet.helpers import getfiles,read_c2
sys.stderr = stderr


def main():
    if len(sys.argv[1:]) != 2:
        print __doc__
        return

    one = read_c2(sys.argv[1])
    two = read_c2(sys.argv[2])

    k1 = set(one.keys())
    k2 = set(two.keys())

    onlyone = len(k1-k2)
    onlytwo = len(k2-k1)

    eq = diff = 0

    for k in k1 & k2:
        if one[k] == two[k]:
            eq += 1
        else:
            diff += 1

    if not diff:
        if onlyone and not onlytwo:
            f = (1,2)
        elif not onlyone and onlytwo:
            f = (2,1)
        elif not onlyone and not onlytwo:
            print 'Files are equals'
            return
        
        print '%s > %s' % (sys.argv[f[0]],sys.argv[f[1]])
    else:
        print 'Same values:',eq
        print 'Different values:',diff
        print 'Values only in %s:'%sys.argv[1],onlyone
        print 'Values only in %s:'%sys.argv[2],onlytwo

if __name__=='__main__':
    main()
