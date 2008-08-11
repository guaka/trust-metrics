#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
USAGE:
   ./wikixml2graph.py xml_file [--history|--current] lang date [base_path|real<real_path>] [--hash] [--input-size bytes]
      Default base_path = home dir
      If base_path starts with 'real' graph will save in real_path
      If lang and date are both '-' wikixml2dot will read them from file name
      If xml_file is - it will use stdin
      input-size: useful if xml_file is stdin 
'''

from xml import sax
from trustlet.Dataset.Network import Network
from trustlet.helpers import *
from networkx import write_dot
from string import index, split
from sys import stdin,argv
import os,re,time
import urllib
from gzip import GzipFile


# set User-Agent (Wikiperdia doesn't give special pages to Python :@ )
class URLopener(urllib.FancyURLopener):
    version = "wikixml2graph/0"
urllib._urlopener = URLopener()

getpage = lambda url: urllib.urlopen(url).read()

printable = lambda o: ''.join([chr(ord(c)%128) for c in o])
node = lambda s: str(printable(s)).replace('"',r'\"').replace('\\',r'\\')

from socket import gethostname
hostname = gethostname()

i18n = {
    'vec':('Discussion utente','Utente'),
    'nap':('Discussioni utente','Utente'),
    'fur':('Discussion utent','Utent'),
    'eml':('Discussioni utente','Utente'),
    'it': ('Discussioni utente','Utente'),
    'en': ('User talk','User'),
    'simple':('User talk','User'),
    'la': ('Disputatio Usoris','Usor'),
}

def main():

    if '--current' in argv:
        WikiContentHandler = WikiCurrentContentHandler
        outputname = 'graphCurrent'
        
        argv.remove('--current')
    else:
        WikiContentHandler = WikiHistoryContentHandler
        outputname = 'graphHistory'
        
        if '--history' in argv:
            argv.remove('--history')
        
    if '--input-size' in argv[:-1]:
        i = argv.index('--input-size')
        inputsize = int(argv[i+1])
        del argv[i+1]
        del argv[i]
    else:
        inputsize = None

    if len(argv[1:]) >= 3:

        xml,lang,date = argv[1:4]
        if xml == '-':
            xml = stdin
            size = None
        else:
            size = os.stat(xml).st_size
            if (lang,date) == ('-','-'):
                s = os.path.split(xml)[1]

                lang = s[:s.index('wiki')]
                res = re.search('wiki-(\d{4})(\d{2})(\d{2})-',s)
                date = '-'.join([res.group(x) for x in xrange(1,4)])
                print lang,date

        if inputsize:
            size = inputsize

        assert isdate(date)

        if argv[4:]:
            base_path = argv[4]
        else:
            assert os.environ.has_key('HOME')
            base_path = os.environ['HOME']

        if base_path.startswith('real'):
            path = base_path[4:]
        else:
            path = os.path.join(base_path,'datasets','WikiNetwork',lang,date)
        mkpath(path)

        ch = WikiContentHandler(lang,xmlsize=size)

        sax.parse(xml,ch)

        pynet = del_ips(ch.getPyNetwork())

        assert save({'network':'Wiki','lang':lang,'date':date},pynet,os.path.join(path,outputname+'.c2'))
        #write_dot(pynet,os.path.join(path,outputname+'.dot'))
        #save_raw_graph(pynet,os.path.join(path,outputname+'.rawgraph'))

        users,bots = get_list_users(lang,os.path.join(base_path,'datasets','WikiNetwork'))
        lenusers = len(users)
        print 'Number of users of whole graph:',lenusers
        print 'Number of bots:',len(bots)
        f = file('wikixml2graph.log','a')
        f.write('Network: %s %s\n'%(lang,date))
        f.write('Number of users of whole graph: %d\n'%lenusers)
        f.write('Number of bots: %d\n'%len(bots))
        f.close()

        pynet = (
            list( set(pynet[0]) - set(bots) ),
            [x for x in pynet[1] if x[0] not in bots and x[1] not in bots]
            )

        assert save({'network':'Wiki','lang':lang,'date':date,'users':'nobots'},
                    pynet,os.path.join(path,outputname+'-nobots.c2'))

    else:
        print __doc__

def del_ips(pynetwork):
    nodes,edges = pynetwork

    nodes = [x for x in nodes if not isip(x)]
    edges = [x for x in edges if not isip(x[0]) and not isip(x[1])]

    return nodes,edges

def get_list_users(lang,cachepath=None,force=False):
    '''
    Return users and bots lists
     - cachepath is a directory
    '''
    url = 'http://%s.wikipedia.org/w/index.php?title=Special:ListUsers&limit=5000' % lang
    if not cachepath:
        cachepath = os.path.join(os.environ['HOME'],'.wikixml2graph','listusers.c2')
    else:
        assert not cachepath.endswith('.c2')
        cachepath = os.path.join(cachepath,'listusers.c2')
    re_user = re.compile('title="Utente:[^"]+">([^<]+)')
    re_bot = re.compile('title="Utente:[^"]+">([^<]+)</a>.*?Bot.*?</li>')

    # title="Utente:!! Roberto Valentino !! (pagina inesistente)">!! Roberto Valentino !!</a></li>

    MONTHS = 60*60*24*30
    WEEKS = 60*60*24*7

    users = []
    bots = []
    ll = 1
    pageurl = url
    count = 0
    while ll:
        print count
        page = load({'url':pageurl},cachepath)
        if page: t,page = page

        if not page or force or time.time()-t>2*WEEKS or not re.findall(re_user,page):
            page = getpage(pageurl)
            save({'url':pageurl},(time.time(),page),cachepath)
        newusers = re.findall(re_user,page)
        bots += re.findall(re_bot,page)
        if newusers:
            pageurl = url + '&' + urllib.urlencode({'offset':newusers[-1]})
            #print pageurl
        ll = len(newusers)
        count += ll
        users += newusers
    return users,bots
    

class WikiHistoryContentHandler(sax.handler.ContentHandler):
    def __init__(self,lang,xmlsize=None):
        sax.handler.ContentHandler.__init__(self)

        self.lang = lang
        
        #print info
        self.xmlsize = xmlsize
        self.count = 0
        self.last_perc_print=''

        self.read = False
        self.validdisc = False # valid discussion

        self.pages = []
        self.allusers = set()

    def startElement(self,name,attrs):
        
        #disable loading of contents
        if name == u'username':
            self.read = u'username'
            self.lusername = u''
        elif name == u'title':
            self.read = u'title'
            self.ltitle = u''
        else:
            self.read = False

    def endElement(self,name):

        if name == u'username' and self.validdisc:

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
            
            if title[0] in (i18n[self.lang][1],i18n[self.lang][0]) and title[1]==':' and title[2]:
                self.allusers.add(title[2])

    def characters(self,contents):
        if self.read == u'username':
            self.lusername += contents.strip()
        elif self.read == u'title':
            self.ltitle += contents.strip()

        if self.xmlsize:
            self.count += len(contents)
            perc = 100*self.count/self.xmlsize
            if perc != self.last_perc_print:
                print '>%d%% ~%d%%'%(perc,perc*100/48)
                self.last_perc_print = perc

    def getNetwork(self):
        W = Network()
        
        for user,authors in self.pages:
            W.add_node(node(user))
            for a,num_edit in authors.iteritems():
                # add node
                W.add_node(node(a))
                #add edges
                W.add_edge(node(user),node(a),{'value':str(num_edit)})
                
        return W

    def getPyNetwork(self):
        '''return list of edges'''
        nodes = []
        edges = []

        for user,authors in self.pages:
            if not authors:
                nodes.append(user)
            for a,num_edit in authors.iteritems():
                edges.append( (user,a,{'value':num_edit}) )
                
        return (nodes,edges)


class WikiCurrentContentHandler(sax.handler.ContentHandler):
    def __init__(self,lang,xmlsize=None):
        sax.handler.ContentHandler.__init__(self)

        self.lang = lang
        self.read = False
        self.validdisc = False # valid discussion
        self.xmlsize = xmlsize
        self.count = 0
        self.last_perc_print = ''

        self.allusers = set()

        self.network = Network()
        self.edges = []
        self.nodes = []

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
            if not collaborators:
                self.nodes.append(self.lusername)
            for u,n in collaborators:
                self.network.add_node(node(u))
                self.network.add_edge(node(u),node(self.lusername),{'value':str(n)})
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

        if self.xmlsize:
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

    exit = 0; start = 0
    search = i18n[lang][1]+":"
    io = len(search)

    while True:
        #search next user
        try:
            iu = index( rawWikiText, search, start ) #index of username
        except ValueError:
            break
            
        #begin of the username
        start = iu + io
        #find end of username with regex
        #username = re.findall( "[àòèéùìa-zA-Z0-9.-]+",rawWikiText[start:] )[0] # ¡bug!
        username = re.findall( "[^]|&/]+",rawWikiText[start:] )[0]
        #print 'debug',username
        if username == '' or username == None:
            print "Damn! I cannot be able to find the name!"
            print "This is the raw text:"
            print rawWikiText[start:start+30]
            import sys
           
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


def weight( list ):
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
    listweight = []
    tmp = list

    def update( list, val ):
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
        update( listweight, x )

    return listweight

#this function is not useful for now..
def getCharPosition( rawWikiText, search, start ):
        """
        return the position of the first character in rawWikiText,
        choosed from search. If doesn't find any end character,
        show 30 character after start position in rawWikiText,
        and get end character by standard input.
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
            import sys
           
            print "What is the end character? (all the character before first were ignored)"
            newdelimiter = sys.stdin.readline().strip()[0]
            
            try:
                end.append( index( rawWikiText, newdelimiter, start ) )
            except ValueError:
                print "Damn! you give me a wrong character!.."
                exit(0)

        end.sort()
        return end[0]


def save_raw_graph(pynetwork,path):
    '''save graph in a gzip compressed text file'''

    writelines = lambda f,lines: f.writelines([x+'\n' for x in lines])

    #version 0
    nodes,edges = pynetwork

    #f = GzipFile(path,'w')
    f = file(path,'w')
    writelines(f,['0',str(len(nodes)),str(len(edges))])
    writelines(f,nodes)
    for edge in edges:
        writelines(f,[edge[0],edge[1],str(edge[2]['value'])])
    f.close()

def load_raw_graph(path):
    '''load a pynetwork'''
    #f = GzipFile(path)
    f = file(path)
    version = f.readline()
    if version == '0':
        num_nodes = int(f.readline())
        num_edges = int(f.readline())
        nodes = []
        for i in xrange(num_nodes):
            nodes.append(f.readline())
        edges = []
        for i in xrange(num_edges):
            edges.append( (f.readline(),f.readline(),{'value':int(f.readline())}) )
        pynetwork = (nodes,edges)
    else:
        pynetwork = None
    f.close()
    return pynetwork

if __name__=="__main__":
    main()
