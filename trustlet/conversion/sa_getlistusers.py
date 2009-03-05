#!/usr/bin/env python

import re
import time
import os
import os.path as path
import urllib
import cPickle as pickle
from gzip import GzipFile


# set User-Agent (Wikipedia doesn't give special pages to Python :@ )
class URLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.0.1) Gecko/2008071719 Firefox/3.0.1"
urllib._urlopener = URLopener()

def main():
    langs = i18n.keys()
    savepath = path.join(os.environ['HOME'],'.wikixml2graph')
    mkpath(savepath)

    dsave = []

    for lang in langs:
        print lang
        users,bots,busers = get_list_users(lang,force=True)
        print len(users),len(bots),len(busers)

        dsave.append((lang,users,bots,busers))

    name = '%.4d-%.2d-%.2d' % tuple(time.gmtime()[:3])

    f = GzipFile(name,'w')
    pickle.dump(dsave,f)
    f.close()
        
i18n = {
    'vec':('Discussion utente','Utente','Bot'),
    'nap':('Discussioni utente','Utente','Bot'),
    'fur':('Discussion utent','Utent','Bot'),
    'eml':('Discussioni utente','Utente','Bot'),
    'it': ('Discussioni utente','Utente','Bot'),
    'en': ('User talk','User','Bot'),
    'simple':('User talk','User','Bot'),
    'la': ('Disputatio Usoris','Usor','automaton'),
    'de': ('Benutzer Diskussion', 'Benutzer', 'Bot'),
    'fr' : ('Discussion Utilisateur', 'Utilisateur', 'Bot')
}

def save(*l,**ll):
    return None
def load(*l,**ll):
    return None

LIGHTLOG = True
def getpage(url):
    page = urllib.urlopen(url).read()
    #logging
    logpath = os.path.join(os.environ['HOME'],'.wikixml2graph','log')
    mkpath(logpath)
    if LIGHTLOG:
        file(os.path.join(logpath,'index'),'a').write("{'url':'%s'}: %s\n"%(url,time.asctime()))
    else:
        logname = os.path.split(tempnam())[1]
        logfullpath = os.path.join(logpath,logname)
        file(logfullpath,'w').write(page)
        file(os.path.join(logpath,'index'),'a').write('%s: %s %s\n'%(logname,time.asctime(),url))
    return page


def mkpath(fullpath,function=None):
    """
    makes all missed directory of a path

    def function(path)
    function will called for each created dir.
    path is the path of it.
    """
    if not fullpath: return
    if fullpath[-1] == os.path.sep:
        fullpath = fullpath[:-1]
    if fullpath and not os.path.exists(fullpath):
        assert not os.path.islink(fullpath),'link %s might be broken' % fullpath
        path = os.path.split(fullpath)[0]
        mkpath(path)

        os.mkdir(fullpath)
        if function:
            function(fullpath)

def get_list_users(lang,cachepath=None,force=False,verbose=False):
    '''
    Return users, bots and blocked users lists
     - cachepath is a directory
    '''
    url = 'http://%s.wikipedia.org/w/index.php?title=Special:ListUsers&limit=5000' % lang
    if not cachepath:
        cachepath = os.path.join(os.environ['HOME'],'.wikixml2graph','listusers.c2')
    else:
        assert not cachepath.endswith('.c2')
        cachepath = os.path.join(cachepath,'listusers.c2')

    re_user = re.compile('title="%s:[^"]+">([^<]+)'%i18n[lang][1])
    re_bot = re.compile('title="%s:[^"]+">([^<]+)</a>(.*?)</li>'%i18n[lang][1])

    # title="Utente:!! Roberto Valentino !! (pagina inesistente)">!! Roberto Valentino !!</a></li>

    MONTHS = 60*60*24*30
    WEEKS = 60*60*24*7

    users = []
    bots = []
    ll = 1
    pageurl = url
    count = 0
    if verbose:
        print 'Number of users read:'

    while ll:
        if verbose:
            print count

        page = load({'url':pageurl},cachepath)
        if page: t,page = page

        if not page or force or time.time()-t>2*WEEKS or not re.findall(re_user,page):
            page = getpage(pageurl)
            save({'url':pageurl},(time.time(),page),cachepath,version=3)
        newusers = re.findall(re_user,page)
        bots += [x[0] for x in re.findall(re_bot,page) if i18n[lang][2] in x[1]]
        if newusers:
            pageurl = url + '&' + urllib.urlencode({'offset':newusers[-1]})
            #print pageurl
        ll = len(newusers)
        count += ll
        users += newusers

    # get IPBlockList
    url = 'http://%s.wikipedia.org/wiki/Special:IPBlockList?limit=5000' % lang
    re_rows = re.compile('<li>(.*?)</li>')
    re_offset = re.compile('offset=(\d{14})\D+')
    busers = [] #blocked users
    pageurl = url
    
    if verbose:
        print 'Number of blocked users read:'

    while pageurl:
        if verbose:
            print len(busers)

        page = load({'url':pageurl},cachepath)
        if page: t,page = page

        if not page or force or time.time()-t>2*WEEKS or not re.findall(re_rows,page):
            page = getpage(pageurl)
            save({'url':pageurl},(time.time(),page),cachepath)

        for row in re.findall(re_rows,page):
            users12 = re.findall(re_user,row)
            if len(users12)>=2:
                # a user blocked another user
                busers.append(users12[1])

        try:
            newpageurl = url + '&offset=' + min(re.findall(re_offset,page))
            if newpageurl == pageurl:
                pageurl = None
            else:
                pageurl = newpageurl
            #print 'New url:',pageurl
        except ValueError:
            pageurl = None

    return users,bots,busers

if __name__=="__main__":
    main()
