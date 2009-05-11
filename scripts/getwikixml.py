#!/usr/bin/env python

import time
import optparse
import datetime
import urllib2

# http://download.wikimedia.org/eswiki/20090504/eswiki-20090504-pages-meta-current.xml.bz2
# http://download.wikimedia.org/furwiki/20090508/furwiki-20090508-pages-meta-history.xml.7z

TYPES = set(['pages-meta-current.xml.bz2','pages-meta-history.xml.7z'])

OUT = 'getwikixml.sh'

def main():
    
    o = optparse.OptionParser(usage='usage: %prog [options] langs')
    o.add_option('-r','--range',help='Set range: yyyy-mm-dd:yyyy-mm-dd')
    opts, langs = o.parse_args()
    
    if opts.range:
        range = opts.range.split(':')

        range = [datetime.date(*map(int,r.split('-'))) for r in range]
        
        #print range
        
        f = file(OUT,'w')

        f.write('#!/usr/bin\n')

        for lang in langs:

            i = 0
            d = range[0]
            while d <= range[1]:

                #print '%.4d-%.2d-%.2d'%d.timetuple()[:3]

                for type in TYPES:

                    url = 'http://download.wikimedia.org/%swiki/%.4d%.2d%.2d/%swiki-%.4d%.2d%.2d-%s' % (((lang,) + d.timetuple()[:3])*2 + (type,))
                    
                    try:
                        urllib2.urlopen(url).close()
                    except urllib2.HTTPError:
                        print 'Skipped',url.split('/')[-1]
                        continue

                    print 'Added',url.split('/')[-1]
                    f.write('wget %s\n'%url)

                i += 1
                d = range[0] + datetime.timedelta(i)

        f.close()

if __name__=='__main__':
    main()
