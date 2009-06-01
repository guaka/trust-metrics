#!/usr/bin/env python

'''
Usage:
  diffc2.py one.c2 two.c2
'''


import sys
import optparse
# not show: /usr/lib/python2.6/site-packages/networkx/hybrid.py:16: DeprecationWarning: the sets module is deprecated
stderr = sys.stderr
sys.stderr = file('/dev/null','w')
from trustlet.helpers import getfiles,read_c2
sys.stderr = stderr


def main():
    
    o = optparse.OptionParser(usage='usage: %prog [-r] [file1 [file2] [...]]')
    o.add_option('-v','--verbose',help='print different values',default=False,action='store_true')

    opts, files = o.parse_args()

    if len(files) != 2:
        print __doc__
        return

    one = read_c2(files[0])
    two = read_c2(files[1])

    k1 = set(one.keys())
    k2 = set(two.keys())

    onlyone = len(k1-k2)
    onlytwo = len(k2-k1)

    eq =  0
    diff1 = 0 # one.c2 is newer
    diff2 = 0 # two.c2 is newer

    for k in k1 & k2:
        if one[k]['dt'] == two[k]['dt']:
            eq += 1
        else:
            if opts.verbose:
                print '1>',one[k]
                print '2<',two[k]

            if one[k]['ts'] > two[k]['ts']:
                diff1 += 1
            elif one[k]['ts'] < two[k]['ts']:
                diff2 += 1
            else:
                assert 0,'Same timestamp, different data. Improbably'

    diff = diff1 + diff2

    if not diff:
        if onlyone and not onlytwo:
            f = (0,1)
        elif not onlyone and onlytwo:
            f = (1,0)
        elif not onlyone and not onlytwo:
            print 'Files are equals'
            return
        
        print '%s > %s' % (files[f[0]],files[f[1]])
    else:

        # All different data is newer in `newer` c2 file
        if not diff2:
            newer = 0
        elif not diff1:
            newer = 1
        else:
            newer = 0

        if newer:
            print 'The newest c2 is',files[newer]
        print 'Same values:',eq
        print 'Different values:',diff
        print 'Values only in %s:'%files[0],onlyone
        print 'Values only in %s:'%files[1],onlytwo

if __name__=='__main__':
    main()
