#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml import sax
from string import index

def main():
    #parser = sax.make_parser()
    ch = WikiContentHandler()
    sax.parse('vecwiki-20080408-pages-meta-current.xml',ch)

['__doc__', '__getitem__', '__init__', '__len__', '__module__', '_attrs', 'copy', 'get', 'getLength', 'getNameByQName', 'getNames', 'getQNameByName', 'getQNames', 'getType', 'getValue', 'getValueByQName', 'has_key', 'items', 'keys', 'values']

class WikiContentHandler(sax.handler.ContentHandler):
    def __init__(self):
        sax.handler.ContentHandler.__init__(self)
        self.level = 0
    def startElement(self,name,attrs):
        self.level += 1
        print ' '*self.level+name
        for name in attrs.getNames():
            print '>',name,attrs.getValue(name),attrs.getType(name)
        #print attrs.items()
    def endElement(self,name):
        self.level -= 1
    def characters(self,contents):
        print str(contents)


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
