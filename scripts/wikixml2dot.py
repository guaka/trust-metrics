#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml import sax
import re
from trustlet.Dataset.Network import Network
from networkx import write_dot
from string import index

#printable = lambda o: ''.join([c for c in o if ord(c)<128])
stacknames = lambda stack: [i[0] for i in stack]
stackdatas = lambda stack: [i[1][:50] for i in stack]

from socket import gethostname
hostname = gethostname()

def main():
    ch = WikiContentHandler()
    #sax.parse('vecwiki-20080408-pages-meta-current.xml',ch)
    if hostname == 'etna2':
        sax.parse('/home/jonathan/Desktop/raid/vecwiki-20080625-pages-meta-history.xml',ch)

    #print ch.pages

class WikiContentHandler(sax.handler.ContentHandler):
    def __init__(self,use_username=True):
        sax.handler.ContentHandler.__init__(self)
        self.cstack = []
        #self.characters = self.characters_ok
        self.pages = []
        if use_username:
            self._node = u'username'
        else:
            self._node = u'id'

    def startElement(self,name,attrs):
        self.cstack.append([name,u''])
        
        #disable loading of contents
        if name == u'text':
            pass
            #self.characters = None
        elif name == u'page':
            self.pages.append( ('',{}) ) # ( user, dict_edit )

        #print stacknames(self.cstack)
        #for name in attrs.getNames():
        #    print '>',name,attrs.getValue(name),attrs.getType(name)
        #print attrs.items()

    def endElement(self,name):
        storedName,contents = self.cstack.pop()
        assert name == storedName

        #print ' '*len(self.cstack)+name,self.cstack[-1][1]

        if name == self._node:
            assert self.cstack[-1][0] == u'contributor'
            #print stacknames(self.cstack)
            print self.cstack,'|',self.cstack[-1][1]

            key = self.cstack[-1][1]
            if self.pages[-1][1].has_key(key):
                self.pages[-1][1][key] += 1
            else:
                self.pages[-1][1][key] = 1
            #print self.pages[-1][1][key]
            
        elif name == u'text':
            pass
            #self.characters = self.characters_ok

    def characters(self,contents):
        #print 'contents','('+contents[:50]+')'
        #print '>>>',self.cstack[-1][0],'@'+contents+'@'
        self.cstack[-1][1] += contents.strip()
        #print '>>>',self.cstack[-1][0],'@'+self.cstack[-1][1]+'@'


def getCollaborators( name, rawWikiText ):
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

    #try user, if there aren't, try Utente (italian)
    while exit < 2:

        try:
            iu = index( rawWikiText, search, start )
        except ValueError:
            exit += 1
            start = 0
            io = 7
            search = "Utente:"
            if exit >= 2:
                continue

        start += iu + io
        end = index( rawWikiText, "|", start ) 
        username = rawWikiText[start:end]
        resname.append( username )
        start += end + 1 #not consider the |
    
    #return a list of tuple, the second value of tuple is the weight    
    return weight( resname )


def weight( list ):
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
