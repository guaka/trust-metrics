#!/usr/bin/env python

import time
import os
import threading
import optparse
import datetime
import urllib2

# http://download.wikimedia.org/eswiki/20090504/eswiki-20090504-pages-meta-current.xml.bz2
# http://download.wikimedia.org/furwiki/20090508/furwiki-20090508-pages-meta-history.xml.7z

# test: ./getwikixml.py fur -r 2009-05-08:2009-05-09 -d

TYPES = set(['pages-meta-current.xml.bz2','pages-meta-history.xml.7z'])

OUT = 'getwikixml.sh'

DIR = 'wikixml'

def main():
    
    o = optparse.OptionParser(usage='usage: %prog [options] langs')
    o.add_option('-r','--range',help='Set range: yyyy-mm-dd:yyyy-mm-dd')
    o.add_option('-d','--download',help='download now wiki dumps',default=False,action='store_true')
    o.add_option('-o','--directory',help='set download directory')
    o.add_option('-c','--cache',help='cache url request',dest='urlcachefile')
    opts, langs = o.parse_args()
    
    if opts.range:
        range = opts.range.split(':')

        range = [datetime.date(*map(int,r.split('-'))) for r in range]
    else:
        range = [datetime.date(2009,1,1),datetime.date(2010,1,1)]

        
    #print range   

    if range[1] > range[1].today():
        range[1] = range[1].today()

    if opts.download:
        l = [] # list of urls
        llock = threading.Lock() # list lock
        devent = threading.Event()

        thread = Download(l,llock,devent,opts.directory or DIR)
        thread.start()

    f = file(OUT,'w')

    f.write('#!/usr/bin\n')
    f.write('# Langs: '+', '.join(langs)+'\n')
    f.write('# Range: %s:%s\n'%tuple([r.isoformat() for r in range]))

    if opts.urlcachefile:
        incache,notincache = urlcacheload(opts.urlcachefile)

    for lang in langs:

        i = 0
        d = range[0]
        while d <= range[1]:

            #print '%.4d-%.2d-%.2d'%d.timetuple()[:3]

            for type in TYPES:

                url = 'http://download.wikimedia.org/%swiki/%.4d%.2d%.2d/%swiki-%.4d%.2d%.2d-%s' % (((lang,) + d.timetuple()[:3])*2 + (type,))

                if opts.urlcachefile and url in notincache:
                    print 'Skipped',url.split('/')[-1],'(cache)'
                    continue

                if not (opts.urlcachefile and url in incache):
                    try:
                        urllib2.urlopen(url).close()
                    except urllib2.HTTPError:
                        print 'Skipped',url.split('/')[-1]
                        if opts.urlcachefile:
                            notincache.add(url)               
                        continue

                print 'Added',url.split('/')[-1],opts.urlcachefile and url in incache and '(cache)' or ''
                f.write('wget %s\n'%url)

                if opts.urlcachefile:
                    incache.add(url)

                if opts.download:
                    
                    llock.acquire()

                    l.insert(0,url)
                    llock.release()

                    devent.set()

            i += 1
            d = range[0] + datetime.timedelta(i)

    if opts.download:
        llock.acquire()
        l.insert(0,False)
        llock.release()
        devent.set()

    f.close()

    if opts.urlcachefile:
        urlcachesave(opts.urlcachefile,incache,notincache)

class Download(threading.Thread):

    def __init__(self,l,llock,devent,dir):

        threading.Thread.__init__(self)

        self.list = l
        self.lock = llock
        self.download = devent
        self.dir = dir

        if not os.path.exists(dir):
            os.mkdir(dir)

    def run(self):

        while True:

            self.download.wait()

            self.lock.acquire()
            url = self.list.pop()
            count = len(self.list)
            if not self.list:
                self.download.clear()
            self.lock.release()

            if not url:
                break
            
            name = os.path.split(url)[1]

            if os.path.exists(os.path.join(self.dir,name)):
                print 'File yet downloaded'
                continue

            print 'Download: %s (%d)'%(name,count)
            
            i = urllib2.urlopen(url)
            o = file(os.path.join(self.dir,name),'w')

            b = '-'
            t = time.time()
            c = 0
            while b:
                b = i.read(10000)
                o.write(b)
                c += len(b)

            print 'Speed: %d B/s'%(c/int(time.time()-t))

            i.close()
            o.close()

def urlcacheload(path):
    if os.path.exists(path):
        cachef = file(path)
        cache = [x.strip() for x in cachef.readlines()]
        cachef.close()

        return set([x for x in cache if x[0]!='!']), set([x[1:] for x in cache if x[0]=='!'])
    else:
        return set(), set()

def urlcachesave(path,incache,notincache):
    cachef = file(path,'w')
    cachef.writelines(['%s\n'%x for x in sorted(incache)])
    cachef.writelines(['!%s\n'%x for x in sorted(notincache)])
    cachef.close()

if __name__=='__main__':
    main()
