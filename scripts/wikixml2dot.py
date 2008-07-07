#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
USAGE:
   ./wikixml2dot.py xml_file [--history|--current] lang date [base_path] [--hash]
      Default base_path = home dir
      If xml_file is - it will use stdin
'''

from xml import sax
from trustlet.Dataset.Network import Network
from trustlet.helpers import mkpath
from networkx import write_dot
from string import index, split
from sys import stdin,argv
import os,re

printable = lambda o: ''.join([chr(ord(c)%128) for c in o])
node = lambda s: str(printable(s))
hnode = lambda s: str(hash(s))

from socket import gethostname
hostname = gethostname()

i18n = {
    'vec':('Discussion utente','Utente'),
    'nap':('Discussioni utente','Utente'),
    'it': ('Discussioni utente','Utente'),
    'en': ('User talk','User'),
    'la': ('Disputatio Usoris','Usor'),
}

def main():

    if '--hash' in argv:
        globals()['node'] = hnode
        argv.remove('--hash')

    if '--current' in argv:
        WikiContentHandler = WikiCurrentContentHandler
        
        argv.remove('--current')
    else:
        WikiContentHandler = WikiHistoryContentHandler
        
        if '--history' in argv:
            argv.remove('--history')
        
    if len(argv[1:]) >= 3:

        xml,lang,date = argv[1:4]
        if xml == '-':
            xml = stdin

        assert re.match('^[\d]{4}-[\d]{2}-[\d]{2}$',date)

        if argv[4:]:
            base_path = argv[4]
        else:
            assert os.environ.has_key('HOME')
            base_path = os.environ['HOME']

        path = os.path.join(base_path,'datasets','WikiNetwork',lang,date)
        mkpath(path)

        ch = WikiContentHandler(lang=lang)

        sax.parse(xml,ch)
        write_dot(ch.getNetwork(),os.path.join(path,'graph.dot'))
    else:
        print __doc__
        
    exit(0)

    if hostname == 'etna2':
        ch = WikiHistoryContentHandler()
        #sax.parse(stdin,ch)
        sax.parse('/home/jonathan/Desktop/raid/vecwiki-20080625-pages-meta-history.xml',ch)
        #ch = WikiContentHandler(lang='nap')
        #sax.parse('/home/jonathan/Desktop/raid/napwiki-20080629-pages-meta-history.xml',ch)
        #ch = WikiContentHandler(lang='la')
        #sax.parse('/home/jonathan/Desktop/raid/lawiki-20080630-pages-meta-history.xml',ch)
        #print ch.getNetwork()
        write_dot(ch.getNetwork(),'graph.dot')

        #file('log','w').write(str(ch.pages))
    elif hostname == 'ciropom.homelinux.net':
        #print getCollaborators( test )
        pass

class WikiHistoryContentHandler(sax.handler.ContentHandler):
    def __init__(self,lang):
        sax.handler.ContentHandler.__init__(self)

        self.lang = lang
        self.read = False
        self.validdisc = False # valid discussion

        self.pages = []

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
            if d.has_key(self.lusername):
                d[self.lusername] += 1
            else:
                d[self.lusername] = 1
        elif name == u'title':

            ### 'Discussion utente:Paolo-da-skio'
            title = self.ltitle.partition(':')
            if title[:2] == (i18n[self.lang][0], ':') and title[2]:
                self.pages.append( (title[2],{}) ) # ( user, dict_edit )
                self.validdisc = True
            else:
                self.validdisc = False

    def characters(self,contents):
        if self.read == u'username':
            self.lusername += contents.strip()
        elif self.read == u'title':
            self.ltitle += contents.strip()

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


class WikiCurrentContentHandler(sax.handler.ContentHandler):
    def __init__(self,lang):
        sax.handler.ContentHandler.__init__(self)

        self.lang = lang
        self.read = False
        self.validdisc = False # valid discussion

        self.network = Network()

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
            for u,n in getCollaborators(self.ltext,self.lang):
                self.network.add_node(node(u))
                self.network.add_edge(node(u),node(self.lusername),{'value':str(n)})
        elif name == u'title':

            ### 'Discussion utente:Paolo-da-skio'
            title = self.ltitle.partition(':')
            if title[:2] == (i18n[self.lang][0], ':') and title[2]:
                self.lusername = title[2]
                self.validdisc = True
            else:
                self.validdisc = False

    def characters(self,contents):
        if self.read == u'username':
            self.lusername += contents.strip()
        elif self.read == u'title':
            self.ltitle += contents.strip()

    def getNetwork(self):        
        return self.network

def getCollaborators( rawWikiText, lang ):
    """
    return a list of tuple with ( user, value ), where user is the name of user
    that put a message on the page, and the value is the number of times that
    he appear in rawText passed.
    parameter:
       name: name of user 
       rawWikiText: text in wiki format (normally discussion in wiki)
    """

    resname = []

    exit = 0; start = 0; search = "User:"; io = 5

    def getEnd( rawWikiText, search, start ):
        """
        return the position of the first 'end character',
        choosed from search.
        """
        list = split( search , "," )
        end = []

        for delimiter in list:
            try:
                end.append( index( rawWikiText, delimiter, start ) )
            except ValueError:
                #print delimiter
                pass

        end.sort()
        return end[0]


    #try user, if there aren't, try Utente (italian)
    while exit < 2:
        #search next user
        try:
            iu = index( rawWikiText, search, start ) #index of username
        except ValueError:
            #if doesn't find, try to find "Utente:"
            #if doesn't find utente, exit
            exit += 1
            start = 0
            io = 7 #index offset from begin of "User:" and begin of Username
            try:
                search = i18n[lang][1]+":"
            except KeyError:
                pass

            continue
            

        #begin of the username
        start = iu + io
        end = getEnd( rawWikiText, "|,]", start ) #find end of username (search | or ], take the first one)
        username = rawWikiText[start:end]
        resname.append( username ) # list of all usernames (possibly more than one times for one)
        start += end - start + 1 # not consider the |
        
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


if __name__=="__main__":
    main()
