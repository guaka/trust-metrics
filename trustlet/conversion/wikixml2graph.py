# -*- coding: utf-8 -*-
'''
this script convert xml downloaded from www.download.wikimedia.org (history or current)
in c2 dataset format, usable by trustlet
'''

from xml import sax
from trustlet.Dataset.Network import Network,WeightedNetwork
from trustlet.helpers import *
from string import index, split
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
elif os.system('which 7zr &> /dev/null')==0:
    SevenzipFile = lambda name: os.popen('7zr x "%s" -so 2> /dev/null' % name)
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

# BEGIN OF THE FUNCTION TO MANIPULATE i18n

#the right translation for "Discussion User" in the language in key
i18n = load('language_parameters', os.path.join( os.environ['HOME'], 'shared_datasets', 'WikiNetwork', 'languageparameters.c2' ), fault=False ) 

def addWikiLanguage(key,definition):
    """
    add a language to the list of supported language for wikixml2graph
    key: name of language, it MUST be the string before 'wiki-...' in the xml file name.
         ex. emlwiki-20090101-pages-meta-current.xml --> key = 'eml'
    definition:
         a tuple of 3 strings, 
         the first one is how you can say 'User talk' in the language specified,
         the second one is how you can say 'User' in the language,
         the third one is how you can say 'Bot' (A 'Bot' is an artificial user, a program registered for some reasons) in the language.
         definition for the language 'en', must be like this: ('User talk','User','Bot') 
    """
    if type(definition) is tuple and definition.__len__() == 3:
        i18n[key] = definition
        if not save('language_parameters', i18n, os.path.join( os.environ['HOME'], 'shared_datasets', 'WikiNetwork', 'languageparameters.c2' ) ):
            raise IOError( "Write of changes failed! check the permission to write in this path "+os.path.join( os.environ['HOME'], 'shared_datasets', 'WikiNetwork')) 
    else:
        raise Exception( "Wrong definition! it must be a tuple with three values, check the documentation of this function" )

    return True

def listWikiLanguage():
    """
    print the list of current supported language for wikixml2graph
    """
    import pprint
    pprint.pprint( i18n.keys() )

def deleteWikiLanguage(key,temporary=True):
    """
    delete a language from the list of supported language for wikixml2graph
    warning! if you set temporary to False, the delete will be permanent,
    and will be propagated in each client that use trustlet.
    use this function carefully (with great power comes great responsibility)
    temporary = the deletion is temporary or not, if is set to false,
                the changes is permanent. If is set to true, the changes
                is temporary and simply reloading the environment you can rollback
                the changes
    key = the language to delete
    """
    if not key in i18n:
        raise KeyError("This language is not present in the list of supported languages")

    del i18n[key]
    if not temporary:
        if not save('language_parameters', i18n, os.path.join( os.environ['HOME'], 'shared_datasets', 'WikiNetwork', 'languageparameters.c2' ) ):
            raise IOError( "Write of changes failed! check the permission to write in this path "+os.path.join( os.environ['HOME'], 'shared_datasets', 'WikiNetwork')) 

    return True

# END OF THE FUNCTION TO MANIPULATE i18n


def wikixml2graph(src,dst,distrust=False,threshold=0,downloadlists=True,verbose=False):
    '''
    This function is the only one that have to be called directly in this module.
    The other ones are only helpers for this one.
    This function is able to take a gzipped, 7zipped, or bzipped xml downloaded
    from www.download.wikimedia.org understand:
    1. what is the lang of the network (from the filename)
    2. what is the data in which the snapshot would be taken (from the filename)
    3. if it is current or history (from the filename)
    4. if is possible to create a distrust-graph (only for xml with pages)
    and unzip it, parse it, and create in the right folder (your_home/shared_datasets/WikiNetwork/lang/date/ )
    the c2 file with the network. (and if possible, the c2 with the distrust graph)
    threshold = the minimum weight on edges (the edges with weight < threshold, will be deleted)
    downloadlist = download the list of bots, and the list of blockedusers
    '''

    if not i18n:
        raise IOError( os.path.join( os.environ['HOME'], 'shared_datasets', 'WikiNetwork', 'languageparameters.c2' )+" does not exists! you have to sync your current directory (with sync_trustlet)") 


    assert dst.endswith('.c2')
    srcname = os.path.split(src)[1]

    if 'current' in srcname:
        WikiContentHandler = WikiCurrentContentHandler
        
    elif 'history' in srcname:
        WikiContentHandler = WikiHistoryContentHandler
    else:
        raise Error("I cannot understand the type of network (current or history?)")

    filename = os.path.split(src)[1] #rm dir
    size = os.stat(src).st_size

    s = os.path.split(src)[1]
    lang = s[:s.index('wiki')]
    assert lang in i18n, "The lang "+lang+" is not supported! (you can add it using the function addWikiLanguage in this package)"
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
            if os.system( "bunzip2 -q -k -f "+src ):
                print 'an error has occourred! possible reason:'
                print '1. install bz2'
                print '2. no space left on device (in order to decompress your bzip)'
                print 'NB: consider install python-bz2'
                exit(1)

            src = src[:-4] # cut the last three chars
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
    
    if not pynet[0] or not pynet[1]:
        raise Exception( "Conversion failed! no edges or no nodes in this network, you might check the line in the i18n corresponding to the "+i18n[lang]+" language" )

    cachedict = {'network':'Wiki','lang':lang,'date':date}
    if threshold>1:
        cachedict['threshold'] = threshold

    # x^th percentile
    edges = pynet[1]
    edges.sort(lambda x,y: cmp(x[2],y[2]))
    perc90 = edges[len(edges)*9/10][2]
    perc95 = edges[len(edges)*95/100][2]

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
    """
    This class handle the xml for a wiki history dump 
    """
    #startElement: is called when a tag begin, and give as parameter the name and the attributes of the tag
    #endElement: is called when a tag end, and give as parameter the name of the tag
    #characters: is called between start and end of a tag. as parameter will be given the data between tag
    #getNetwork: return a Network with the data calculated
    #getPyNetwork: return a tuple with two list:
    #              1. list of string that represent the nodes
    #              2. list of tuple that represent the edges (who_edit,who_receive_edit,numbers_of_edit_of_who_edit)
    
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

        # list of tuple (owner_of_talk_page,dict(key=user,value=n_of_times_that_user_edit_page))
        self.pages = []
        #set of all users
        self.allusers = set()
        self.distrust = False
        self.threshold = threshold
        self.verbose = verbose
        self.i18n = i18n[self.lang]
        self.i18n = (self.i18n[0].lower(),self.i18n[1].lower(),self.i18n[2].lower())

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
            #set what I'm reading in order to check in endelement
            self.read = u'username'
            self.lusername = u''
        elif name == u'title':
            #set what I'm reading in order to check in endelement
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
                #the users who have edited the last page
                d = self.pages[-1][1]
                if self.lusername != self.pages[-1][0]:
                    #remove edges: userX -> userX
                    if d.has_key(self.lusername):
                        d[self.lusername] += 1
                    else:
                        d[self.lusername] = 1
                        
        elif name == u'title':
            #TODO: duplicated code (see the same function in the Current Handler)?
            ### 'Discussion utente:Paolo-da-skio'
            ### 'Discussion utente:Paolo-da-skio/Subpage'
            title = self.ltitle.split('/')[0].split(':')
            #  comparison case insensitive
            title[0] = title[0].lower()

            # if the discussion is in english or in the language of this wiki, and name of user is not ''
            if (len(title) > 1) and (( title[0] == self.i18n[0]) or (title[0] == i18n['en'][0].lower()) ) and title[1]:
                # if the tag is <title> it means that this is the begin of a new talk page
                self.pages.append( (title[1],{}) ) # ( user, dict_edit )
                self.validdisc = True
                
            else:
                self.validdisc = False
            
            # True if is a talk page or user page                 add talk and user page in english
            if len(title) > 1 and title[0] in (self.i18n[1], self.i18n[0], i18n['en'][0].lower(), i18n['en'][1].lower()) and title[1]:
                self.allusers.add(title[1])

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

                #self.dpages[-1].append((hashlib.md5(self.ltext.encode('utf-8')).digest(),self.lusername)) #old
                self.dpages[-1].append((hash(self.ltext.encode('utf-8')),self.lusername))

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
                # add edge from 'a' who have done the edit
                # a 'user' who receive the edit
                W.add_edge(node(a),node(user),pool({'value':str(num_edit)}))
                
        return W

    def getPyNetwork(self):
        '''return list of edges'''
        nodes = []
        edges = []

        for user,authors in self.pages:
            if not authors:
                nodes.append(user)
            for a,num_edit in authors.iteritems():
                edges.append( (a,user,num_edit) )
                
        return (nodes,edges)

    def getDistrustGraph(self):
        assert self.distrust
        
        return getRevertGraph(self.dpages)


class WikiCurrentContentHandler(sax.handler.ContentHandler):
    """
    This class handle the xml for a wiki current dump 
    """
    
    # startElement: is called when a tag begin, and give as parameter the name and the attributes of the tag
    # endElement: is called when a tag end, and give as parameter the name of the tag
    #characters: is called between start and end of a tag. as parameter will be given the data between tag
    #getNetwork: return a Network with the data calculated
    #getPyNetwork: return a tuple with two list:
    #              1. list of string that represent the nodes
    #              2. list of tuple that represent the edges (who_edit,who_receive_edit,numbers_of_edit_of_who_edit)

    def __init__(self,lang,xmlsize=None,inputfilename=None,forcedistrust=False,threshold=0,verbose=False):
        sax.handler.ContentHandler.__init__(self)
        #lang of wikipedia network
        self.lang = lang
        self.read = False
        self.validdisc = False # valid discussion
        self.xmlsize = xmlsize
        self.inputfilename = inputfilename
        self.count = 0
        self.last_perc_print = ''
        self.threshold = threshold
        self.verbose = verbose
        #set parse parameter for this language
        self.i18n = i18n[self.lang]
        #made the comparison case insensitive
        self.i18n = (self.i18n[0].lower(), self.i18n[1].lower(),self.i18n[2].lower() )
        
        self.allusers = set()
        
        #this three parameters contains the Network,
        #the first as XDiGraph
        #the second/third as list of tuple
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
            #see documentation of getCollaborators
            collaborators = getCollaborators(self.ltext,self.lang)
            if collaborators:
                self.nodes.append(self.lusername)
                for u,n in collaborators:
                    #only if the number of edit is higher than the threshold
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
            title = self.ltitle.split('/')[0].split(':')
            #  comparison case insensitive
            title[0] = title[0].lower()

            # if the discussion is in english or in the language of this wiki, and name of user is not ''
            if (len(title) > 1) and (( title[0] == self.i18n[0]) or (title[0] == i18n['en'][0].lower()) ) and title[1]:
                self.lusername = title[1]
                self.validdisc = True
            else:
                self.validdisc = False

            # True if is a talk page or user page                 add talk and user page in english
            if len(title) > 1 and title[0] in (self.i18n[1],self.i18n[0],i18n['en'][0].lower(), i18n['en'][1].lower() ) and title[1]:
                self.allusers.add(title[1])

    def characters(self,contents):
        #fill the value

        if self.read == u'username':
            self.lusername += contents.strip()
        elif self.read == u'title':
            self.ltitle += contents.strip()
        elif self.read == u'text':
            self.ltext += contents.strip()

        #print an approximation of the percentage of computation
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
