#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
this script convert xml downloaded from www.download.wikimedia.org (history or current)
in c2 dataset format, usable by trustlet
'''

from xml import sax
from trustlet.Dataset.Network import Network,WeightedNetwork
from trustlet.helpers import *
from networkx import write_dot
from string import index, split
import hashlib
import sys
import os,re,time
import urllib
from gzip import GzipFile
try:
    from bz2 import BZ2File
    BZ2 = True
except ImportError:
    BZ2 = False

if os.system('which 7za &> /dev/null')==0:
    SevenzipFile = lambda name: os.popen('7za x "%s" -so 2> /dev/null' % name)
else:
    SevenzipFile = None

# set User-Agent (Wikipedia doesn't give special pages to Python :@ )
class URLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.0.1) Gecko/2008071719 Firefox/3.0.1"
urllib._urlopener = URLopener()

#getpage = lambda url: urllib.urlopen(url).read()
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

printable = lambda o: ''.join([chr(ord(c)%128) for c in o])
node = lambda s: str(printable(s)).replace('"',r'\"').replace('\\',r'\\')

#the right translation for "Discussion User" in the language in key
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

def wikixml2graph(src,dst,t,distrust=False,threshold=0,downloadlists=True,verbose=False):
    '''
    t -> h | c (history or current)
    '''

    assert dst.endswith('.c2')

    if t == 'c':
        WikiContentHandler = WikiCurrentContentHandler
        
    elif t == 'h':
        WikiContentHandler = WikiHistoryContentHandler

    filename = os.path.split(src)[1] #rm dir
    size = os.stat(src).st_size

    s = os.path.split(src)[1]
    lang = s[:s.index('wiki')]
    res = re.search('wiki-(\d{4})(\d{2})(\d{2})-',s)
    date = '-'.join([res.group(x) for x in xrange(1,4)])

    assert isdate(date)

    deleteafter = False
    # Support compressed file
    if type(src) is str:
        if src.endswith('.gz'):
            verbose = False
            src = GzipFile(src)
        elif BZ2 and src.endswith('.bz2'):
            src = BZ2File(src)
            verbose = False
        elif not BZ2 and src.endswith('.bz2'):
            if os.system( "bunzip2 -q -k "+src ):
                print 'install bz2'
                exit(1)

            src = src[:-3] # cut the last three chars
            deleteafter = True

        elif src.endswith('.7z'):
            verbose = False
            if SevenzipFile:
                src = SevenzipFile(src)
            else:
                print 'Install p7zip'
                exit(1)

    mkpath(os.path.split(dst)[0])

    
    ch = WikiContentHandler(lang,xmlsize=size,
                            inputfilename=filename,
                            forcedistrust=distrust,
                            threshold=threshold,
                            verbose=verbose)

    sax.parse(src,ch)
    #check!
    if deleteafter:
        os.remove( src )
    

    pynet = del_ips(ch.getPyNetwork())

    cachedict = {'network':'Wiki','lang':lang,'date':date}
    if threshold>1:
        cachedict['threshold'] = threshold

    # x^th percentile
    edges = pynet[1]
    edges.sort(lambda x,y: cmp(x[2],y[2]))
    perc90 = edges[len(edges)*9/10][2]
    perc95 = edges[len(edges)*95/100][2]
    #print [x[2] for x in edges[len(edges)*95/100:]]

    assert save(cachedict,pynet,dst)

    cachedict['%'] = 90
    assert save(cachedict,perc90,dst)
    cachedict['%'] = 95
    assert save(cachedict,perc95,dst)
    del cachedict['%']

    if hasattr(ch,'distrust') and ch.distrust:
        net = ch.getDistrustGraph()

        nodes = set(net.nodes())
        edges = net.edges()

        #if a node is in edges, isn't useful keep it in nodes
        for e in edges:
            nodes.discard(e[0])
            nodes.discard(e[1])

        assert save({'network':'DistrustWiki','lang':lang,'date':date},
                    (list(nodes),edges),
                    os.path.join(os.path.split(dst)[0],'graphDistrust.c2'))

    if not downloadlists:
        return

    users,bots,blockedusers = get_list_users(lang,
                                             os.path.join(os.environ['HOME'],'shared_datasets','WikiNetwork'))

    assert save({'lang':lang,'list':'bots'},bots,dst)
    assert save({'lang':lang,'list':'blockedusers'},blockedusers,dst)

    lenusers = len(users)
    assert save({'lang':lang,'info':'number of users'},lenusers,dst)

def del_ips(pynetwork):
    '''
    remove IPs from nodes and edges
    '''
    nodes,edges = pynetwork

    nodes = [x for x in nodes if not isip(x)]
    edges = [x for x in edges if not isip(x[0]) and not isip(x[1])]

    return nodes,edges

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
    

class WikiHistoryContentHandler(sax.handler.ContentHandler):

    def __init__(self,lang,xmlsize=None,inputfilename=None,forcedistrust=False,threshold=0,verbose=False):
        sax.handler.ContentHandler.__init__(self)

        self.lang = lang
        
        #print info
        self.xmlsize = xmlsize
        self.inputfilename = inputfilename
        self.count = 0
        self.last_perc_print=''

        self.read = False
        self.validdisc = False # valid discussion

        self.pages = []
        self.allusers = set()
        self.distrust = False
        self.threshold = threshold
        self.verbose = verbose

        if inputfilename:
            assert 'history' in inputfilename

        if inputfilename and 'pages-meta-history' in inputfilename or forcedistrust:
            if verbose:
                print "I'll create distrust graph"
            self.distrust = True

            self.dpages = [] #distrust pages list


    def startElement(self,name,attrs):
        
        #disable loading of contents
        if name == u'username':
            self.read = u'username'
            self.lusername = u''
        elif name == u'title':
            self.read = u'title'
            self.ltitle = u''

        elif self.distrust:
            #distrust network
            if name == 'page':
                self.dpages.append([])
            elif name == u'contributor':
                self.lusername = ''
                #clear username (obsolete)
            elif name == u'text':
                self.read = 'text'
                self.ltext = ''
            else:
                self.read = False
        else:
            self.read = False

    def endElement(self,name):

        if name == u'username':
            if self.validdisc:

                d = self.pages[-1][1]
                if self.lusername != self.pages[-1][0]:
                    #remove edges: userX -> userX
                    if d.has_key(self.lusername):
                        d[self.lusername] += 1
                    else:
                        d[self.lusername] = 1
        elif name == u'title':

            ### 'Discussion utente:Paolo-da-skio'
            ### 'Discussion utente:Paolo-da-skio/Subpage'
            title = self.ltitle.partition('/')[0].partition(':')
            if title[:2] == (i18n[self.lang][0], ':') and title[2]:
                #assert '/' not in title[2]
                self.pages.append( (title[2],{}) ) # ( user, dict_edit )
                self.validdisc = True
            else:
                self.validdisc = False
            
            # True if is a talk page or user page
            if title[0] in (i18n[self.lang][1],i18n[self.lang][0]) and title[1]==':' and title[2]:
                self.allusers.add(title[2])

        elif name == u'page' and self.validdisc:
            # erase edges if weight < self.threshold
            d = self.pages[-1][1] # dict edges of page named pages[-1][0]
            for k,v in d.items():
                if v<self.threshold:
                    del d[k]

        elif self.distrust and name == u'text':
            #distrust only
            if self.lusername:
                #print 'DEBUG',self.lusername #,md5.new(self.ltext.encode('utf-8')).hexdigest()
                self.dpages[-1].append((hashlib.md5(self.ltext.encode('utf-8')).digest(),self.lusername))

    def characters(self,contents):
        if self.read == u'username':
            self.lusername += contents.strip()
        elif self.read == u'title':
            self.ltitle += contents.strip()
        elif self.distrust and self.read == u'text':
            self.ltext += contents

        if self.xmlsize and self.verbose:
            self.count += len(contents)
            perc = 100*self.count/self.xmlsize
            if perc != self.last_perc_print:
                print '>%d%%'%perc
                self.last_perc_print = perc

    def getNetwork(self):
        W = Network()
        
        for user,authors in self.pages:
            W.add_node(node(user))
            for a,num_edit in authors.iteritems():
                # add node
                W.add_node(node(a))
                #add edges
                W.add_edge(node(user),node(a),pool({'value':str(num_edit)}))
                
        return W

    def getPyNetwork(self):
        '''return list of edges'''
        nodes = []
        edges = []

        for user,authors in self.pages:
            if not authors:
                nodes.append(user)
            for a,num_edit in authors.iteritems():
                edges.append( (user,a,num_edit) )
                
        return (nodes,edges)

    def getDistrustGraph(self):
        assert self.distrust
        
        return getRevertGraph(self.dpages)


class WikiCurrentContentHandler(sax.handler.ContentHandler):
    def __init__(self,lang,xmlsize=None,inputfilename=None,forcedistrust=False,threshold=0,verbose=False):
        sax.handler.ContentHandler.__init__(self)

        self.lang = lang
        self.read = False
        self.validdisc = False # valid discussion
        self.xmlsize = xmlsize
        self.inputfilename = inputfilename
        self.count = 0
        self.last_perc_print = ''
        self.threshold = threshold
        self.verbose = verbose
        
        self.allusers = set()

        self.network = Network()
        self.edges = []
        self.nodes = []
        
        if inputfilename:
            assert 'current' in inputfilename

    def startElement(self,name,attrs):
        
        #disable loading of contents
        if name == u'text':
            self.read = u'text'
            self.ltext = u''
        elif name == u'title':
            self.read = u'title'
            self.ltitle = u''
            self.lusername = u''
        else:
            self.read = False

    def endElement(self,name):

        if name == u'text' and self.validdisc:
            self.network.add_node(node(self.lusername))

            collaborators = getCollaborators(self.ltext,self.lang)
            if collaborators:
                self.nodes.append(self.lusername)
                for u,n in collaborators:
                    if n>=self.threshold:

                        try:
                            edge = self.network.get_edge(node(u),node(self.lusername))
                            n += int(edge['value'])
                        except NetworkXError:
                            pass

                        self.network.add_node(node(u))
                        self.network.add_edge(node(u),node(self.lusername),pool({'value':str(n)}))
                        self.edges.append( (u,self.lusername,n) )                        

        elif name == u'title':

            ### 'Discussion utente:Paolo-da-skio'
            title = self.ltitle.partition('/')[0].partition(':')
            if title[:2] == (i18n[self.lang][0], ':') and title[2]:
                self.lusername = title[2]
                self.validdisc = True
            else:
                self.validdisc = False

            if title[0] in (i18n[self.lang][1],i18n[self.lang][0]) and title[1] == ':' and title[2]:
                self.allusers.add(title[2])

    def characters(self,contents):
        if self.read == u'username':
            self.lusername += contents.strip()
        elif self.read == u'title':
            self.ltitle += contents.strip()
        elif self.read == u'text':
            self.ltext += contents.strip()

        if self.xmlsize and self.verbose:
            self.count += len(contents)
            perc = 100*self.count/self.xmlsize
            if perc != self.last_perc_print:
                print '>%d%% ~%d%%'%(perc,perc*100/88)
                self.last_perc_print = perc

    def getNetwork(self):        
        return self.network

    def getPyNetwork(self):
        '''return list of edges'''
        return (self.nodes,self.edges)


def getRevertGraph( PageList ):
    """
    This function create a Revert Graph starting from a list
    of tuple with (md5_of_revision,author_of_revision)
    the list must be ordered in cronological order.
    If you want to know more about revert graph go to
    http://www.trustlet.org/wiki/Understanding_Social_Dynamics_in_Wikipedia_with_Revert_Graph
    Parameters:
       PageList: list of tuple cronological ordered, so formed (md5_of_revision,author_of_revision)
       
    return: a WeightedNetwork with the Revert Graph (weight on edge is an int)
    """
    #list = [ [('a1122dd','user1'),('a1111dd','user2'),('a1122dd','user1')], [('ee1133','user3'),('dafxed','user1'),('xx','user3'),('xfsdjfa','user3'),('ee1133','user4')] ]
    
    G = WeightedNetwork( )
    
    def getBeforeVersion( index ):
        """
        Get the previously (cronologically) version of page that is equal to this version.
        Is used the sHistory, to improve performance (the algorithm doesn't scan all the list)
        """
        min = None

        for i in range( index , -1 , -1 ): #from ts of toCmp to 0.. es. toCmp, toCmp-1, toCmp-2 ... 0
            if sHistory[i][page] == sHistory[index][page]:
                min = sHistory[i][ts]
            else:
                break

        return min

    #label. it's only use is to make more user friendly the code
    page = 0
    user = 2
    ts = 1 #time stamp

    for rList in PageList: #for all pages

        history = [(a,x,b) for (x,(a,b)) in enumerate(rList)]
        sHistory = sorted( history ) #sorted history, (useful to reduce the time of computation)
        lsHistory = len( sHistory )
        
        for i in xrange(lsHistory):
            x = sHistory[i]

            #min and max is the lowerbound and upperbound revision in history, 
            #min and max has the same md5, between this value there are the reverts.
            max = x[ts]
            min = getBeforeVersion( i )
            
            if min > max: #then there aren't before version
                min = max #fix this particular case

            
            if min == None:
                print "OOps min == None! not good"
                continue

            for i in xrange( min, max ): #add all edges if not contraddictory

                if x[page] == history[i][page] or x[user] == history[i][user]:
                    continue 

                #if there isn't the edge, create it with weight 1
                #else update edge, and sum 1 to the current weight
                try: 
                    val = G.get_edge( x[user], history[i][user] )
                except NetworkXError:
                    G.add_edge( x[user], history[i][user], 1 )
                    continue
            
                G.add_edge( x[user], history[i][user], val+1 )
    return G

def getCollaborators( rawWikiText, lang ):
    """
    return a list of tuple with ( user, value ), where user is the name of user
    that put a message on the page, and the value is the number of times that
    he appear in rawText passed.
    parameter:
       lang: lang of wiki [it|nap|vec|en|la]
       rawWikiText: text in wiki format (normally discussion in wiki)
    """
    import re

    resname = []

    start = 0
    search = '[['+i18n[lang][1]+":"
    searchEn = '[['+i18n['en'][1]+":"
    io = len(search)

    while True:
        #search next user
        try:
            iu = index( rawWikiText, search, start ) #index of username
        except ValueError:
            if search == searchEn:
                break
            
            # now search for English signatures
            search = searchEn
            start = 0
            io = len(search)
            continue
            
        #begin of the username
        start = iu + io
        #find end of username with regex
        username = re.findall( "[^]|&/]+",rawWikiText[start:] )[0]
        
        if username == '' or username == None:
            print "Damn! I cannot be able to find the name!"
            print "This is the raw text:"
            print rawWikiText[start:start+30]
           
            print "What is the end character? (all the character before first were ignored)"
            newdelimiter = sys.stdin.readline().strip()[0]
            
            try:
                end.append( index( rawWikiText, newdelimiter, start ) )
            except ValueError:
                print "Damn! you give me a wrong character!.."
                exit(0)


        resname.append( username ) # list of all usernames (possibly more than one times for one)
        start += len(username) + 1 # not consider the end character
        
    #return a list of tuple, the second value of tuple is the weight    
    return weight( resname )


def weight( list, diz=False ):
    """
    takes a list of object and search for each object
    other occurrences of object equal to him.
    Return a list of tuple with (object,n) where object is object (repeated only once)
    and n is the number of times that he appear in list
    Parameter:
      list: list of object
    Example:
      weight( ["mario","pluto","mario"] )
      ---> [("mario",2),("pluto",1)]
    """
    if diz:
        listweight = {}
    else:
        listweight = []
    tmp = list

    def update( list, val, diz=False ):

        if diz:
            if list.has_key(val):
                new = list.get(val)
                new += 1
                list[val] = new
            else:
                list[val] = 1

        else:
            find = False
            
            for x in xrange(len(list)):
                if list[x][0] == val:
                    find = True
                    break

            if find:
                new = list[x][1] + 1
                del list[x]
                list.append( (val,new) )
            else:
                list.append( (val,1) )

        return

    for x in tmp:
        update( listweight, x, diz=diz )

    return listweight

#this function is not useful for now..
def getCharPosition( rawWikiText, search, start ):
        """
        return the position of the first character in rawWikiText,
        choosed from search. If doesn't find any end character,
        show 30 character after start position in rawWikiText,
        and get end character by standard input.
        Parameter:
           rawWikiText: wiki text
           search: string comma-separated, with the search character
           start: an integer with the start position in rawWikiText
        """
        list = split( search , "," )
        end = []

        for delimiter in list:
            try:
                end.append( index( rawWikiText, delimiter, start ) )
            except ValueError:
                #print delimiter
                pass

        if len(end) == 0:
            print "Damn! I cannot be able to find the end of the username!..."
            print "can you suggest me how is the end character of the username?"
            print "This is the raw text:"
            print rawWikiText[start:start+30]
           
            print "What is the end character? (all the character before first were ignored)"
            newdelimiter = sys.stdin.readline().strip()[0]
            
            try:
                end.append( index( rawWikiText, newdelimiter, start ) )
            except ValueError:
                print "Damn! you give me a wrong character!.."
                exit(0)

        end.sort()
        return end[0]

currentWikixml2graph = lambda src,dst: \
    wikixml2graph(src,dst,'c')

historyWikixml2graph = lambda src,dst: \
    wikixml2graph(src,dst,'h')
