#!/usr/bin/env python
# -*- coding: utf-8

# Copyright (c) 2007 Kasper Souren
#
# MaemoDict is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


description = """msocial - social networking tool(s) using microformats

Copyright 2007 by Kasper Souren 
(kasper.souren@gmail.com)

Available under the GNU General Public License
"""


todo = """
 * Plug into Django
  . settings, contacting other members
  . OpenID
  . email confirmation (or is OpenID enough?)
  . are connections signed up locally?
 * Add more microid/microformat sites
  . Wikitravel
  . Flickr
  . ..  
"""


def fetch_page(url):
    from urllib import urlopen
    p = urlopen(url)
    return "".join(p.readlines())

def microid(url, email):
    """Calculate microid, see http://microid.org"""
    from hashlib import sha1 # python 2.5
    # for <2.5: import sha
    sha1_hex = lambda s: sha1(s).hexdigest()
    return 'mailto+http:sha1:' +  sha1_hex(sha1_hex('mailto:' + email) + sha1_hex(url))


from HTMLParser import HTMLParser

class mHTMLParser(HTMLParser):
    """Parse (X)HTML, looking for microformats"""
    meta = {}
    XFN = {}
    hCard = {}
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tag = tag
        self.attr_dict = attr_dict
        if tag == 'meta':
            if attr_dict.has_key('name') and attr_dict.has_key('content'):
                self.meta[attr_dict['name']] = attr_dict['content']
        if tag == 'a' and attr_dict.has_key('rel'):
            self.XFN[attr_dict['href']] = attr_dict['rel']

    def handle_data(self, data):
        def check(tag, attr, value):
            return (self.tag == tag and
                    self.attr_dict.has_key(attr) and
                    self.attr_dict[attr] == value)
        
        if hasattr(self, 'tag'):
            if check('div', 'class', 'fn org'):
                self.hCard['fn_org'] = data
            if check('span', 'class', 'locality'):
                self.hCard['locality'] = data
            if check('div', 'class', 'country-name'):
                self.hCard['country-name'] = data

    def handle_endtag(self, tag):
        self.tag = self.attr_dict = None


class mMember:
    def __init__(self, nick, email):
        self.nick = nick
        self.email = email

    def add_CS_profile(self, nick = None):
        self.CS_profile = CS_user(nick or self.nick, self.email)


    def confirm_email(self):
        pass


class mFormatMember:
    def __repr__(self):
        return ('CS nickname: ' + self.nick + '\n' +
                'microid: ' + repr(self.microid_correct) + '\n'
                'hCard: ' + repr(self.hCard) + '\n'
                'XFN: ' + repr(self.XFN)
                )
    
    def fetch(self):
        self.page = fetch_page(self.url)

    def process(self):
        parser = mHTMLParser()
        parser.feed(self.page)

        if parser.meta['microid']:
            self.microid = microid(self.url, self.email)
            self.microid_correct = parser.meta['microid'] == self.microid

        self.geo_position = parser.meta['geo.position']
        self.XFN = parser.XFN
        self.hCard = parser.hCard
        

class CS_user(mFormatMember):
    def __init__(self, nick, email = None):
        if nick and email:
            self.load_from_CS(nick, email)

    def load_from_CS(self, nick, email):
        self.nick = nick
        self.email = email
        self.url = "http://localhost/people/" + nick + '?all_friends=1'
        self.fetch()
        self.process()

        self.cs_friends = {}
        for f in self.XFN:
            self.cs_friends[cs_decid(f[17:])] = self.XFN[f]

def cs_decid(eid):
    def de_char(c):
        o = ord(c)
        if o < 58:
            return o - 48
        else:
            return o - 55
    l = map(de_char, eid)
    return reduce(lambda x,y: x*35 + y, l) / 12345

def cs_encid(did):
    did = did * 12345
    r = ''
    while did > 0:
        did, char = divmod(did, 35)
        if char < 10:
            r = chr(char + 48) + r
        else:
            r = chr(char + 55) + r
    return r



def main():
    print description
    test()


def test():
    print "Testing...\n"
    member = mMember('amylin', 'amalijaline@gmail.com')
    member = mMember('guaka', 'kasper.souren@gmail.com')
    member.add_CS_profile()
    print member.CS_profile

if False:
    main()
