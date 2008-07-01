#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
USAGE:
   ./wikixml2dot.py xml_file lang [base_path]
      Default base_path = .
      If xml_file is - it will use stdin

(* not written yet *)
'''

from xml import sax
from trustlet.Dataset.Network import Network
from networkx import write_dot
from string import index, split
from sys import stdin,argv

#printable = lambda o: ''.join([c for c in o if ord(c)<128])

from socket import gethostname
hostname = gethostname()

i18n = {
    'vec':('Discussion utente',),
    'nap':('Discussioni utente',),
    'it': ('Discussioni utente',),
    'en': ('User talk',),
    'la': ('Disputatio Usoris',),
}

def main():

    if hostname == 'etna2':
        ch = WikiContentHandler()
        #sax.parse(stdin,ch)
        sax.parse('/home/jonathan/Desktop/raid/vecwiki-20080625-pages-meta-history.xml',ch)
        #ch = WikiContentHandler(lang='nap')
        #sax.parse('/home/jonathan/Desktop/raid/napwiki-20080629-pages-meta-history.xml',ch)
        #ch = WikiContentHandler(lang='la')
        #sax.parse('/home/jonathan/Desktop/raid/lawiki-20080630-pages-meta-history.xml',ch)

        #file('log','w').write(str(ch.pages))
    elif hostname == 'ciropom.homelinux.net':
        #print getCollaborators( test )
        pass

class WikiContentHandler(sax.handler.ContentHandler):
    def __init__(self,use_username=True,lang='vec'):
        sax.handler.ContentHandler.__init__(self)

        self.lang = lang
        self.read = False
        self.validdisc = False # valid discussion

        self.pages = []

        if use_username:
            self._node = u'username'
        else:
            self._node = u'id'

    def startElement(self,name,attrs):
        
        #disable loading of contents
        if name == self._node:
            self.read = self._node
            self.lusername = u''
        elif name == u'title':
            self.read = u'title'
            self.ltitle = u''
        else:
            self.read = False

    def endElement(self,name):

        if name == self._node and self.validdisc:

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
        if self.read == self._node:
            self.lusername += contents.strip()
        elif self.read == u'title':
            self.ltitle += contents.strip()

    def getNetwork(self):
        W = Network()
        
        for user,authors in self.pages:
            W.add_node(user)
            for a,num_edit in authors.iteritems():
                # add node
                W.add_node(a)
                #add edges
                W.add_edge(user,a,{'value':str(num_edit)})
                
        return W
                

def getCollaborators( rawWikiText ):
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
            search = "Utente:"
            if exit >= 2:
                continue
        #begin of the username
        start = iu + io
        end = getEnd( rawWikiText, "|,]", start ) #find end of username (search | or ], take the first one)
        username = rawWikiText[start:end]
        resname.append( username ) #list of all usernames (possibly more than one times for one)
        start += end - start + 1 #not consider the |
        
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
