#!/usr/bin/env python
'''
get some name's users from wikipedia
'''

import os,re

def read(url):
    if os.system('wget -O temp %s' % url):
        print "Error"
        return None
    data = file('temp').read()
    #os.remove('temp')
    return data
    

def geturl(lang,limit,offset=None):
    baseurl = 'http://%s.wikipedia.org/w/index.php?title=Special:Listusers&%slimit=%d'
    # ( lang, offset, limit )

    if offset:
        pass

    return baseurl % (lang,'',limit)



def getnames(lang='it',limit=None):
    #print geturl(lang,500)
    data = read(geturl(lang,500))
    file('users','w').write(data)
    users = []

    return []

if __name__=="__main__":
    print getnames(limit=100)
