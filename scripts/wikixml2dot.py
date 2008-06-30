#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml import sax

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

if __name__=="__main__":
    main()
