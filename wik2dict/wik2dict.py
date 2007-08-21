#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2004-2007 Kasper Souren
#
# wik2dict is free software; you can redistribute it and/or modify it
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

"""
Conversion of MediaWiki SQL dumps into dict files.
Optionally download Wikimedia SQL dumps.

Alpha version for XML dumps
"""

import os, sys, string, re
import pprint
import commands
import dictdlib
from string import ascii_letters
from optparse import OptionParser

from sets import Set
import Providers
from Parser import Parser
import unicode_crap

NS_CATEGORY = 14


def remove_if_exists(file_to_remove):
	"""Remove file if it exists."""
	if os.path.exists(file_to_remove):
		os.remove(file_to_remove)
		print "* Removed", file_to_remove


class Dump2dict:
	"""Convert MediaWiki XML dump into dict."""
	
	def __init__(self, wik_datafile):
		provider = Providers.XMLfile_Provider(wik_datafile)
		name = wik_datafile.split("-")[0]
		print "Converting", wik_datafile, "into DICT format"
		(dictname, dictfilename) = self.get_info(name, provider)
		dict_object = self.create_dict_object(dictfilename)
		self.process_articles(provider, dict_object)
		#dict_object.addentry(GNU_FDL, ["FDL.txt"])
		self.finish_dict(dict_object, provider, dictname)
		self.dictzip(dictfilename)

		del provider

	def process_articles(self, provider, dict_object):
		"""Process the articles."""
		#utf8 = UnicodeProcessor(options.latin1)
		#category_name = provider.namespaces(NS_CATEGORY)
		parser = Parser()
		redirects = provider.article_redirects

		# create reverse mapping
		redirects_rev = dict(map(lambda x: (x[1], x[0]), redirects.items()))
		parser.set_namespaces(provider.namespaces)
		parser.set_messages(provider.messages)

		utf8 = unicode_crap.UnicodeProcessor()

		for count, (index, article) in enumerate(provider.articles.items()):
			if not index in redirects:
				#index = utf8.process(index)
				if type(article) == unicode:
					article = article.encode("utf-8")
				if type(index) == unicode:
					index = index.encode("utf-8")
				indices = Set([index])
				if index in redirects_rev:
					indices.add(redirects_rev[index])
				entry = index + "\n" + \
						parser.wiki_to_dict(index, article)
				#entry = entry.encode("utf-8")
				dict_object.addentry(entry, indices)
		
		#print "* Creating", len(parser.categories), "categories"
		#for (cat, articles) in parser.categories.items():
		#	articles.sort()
		#	index = category_name + ":" + cat
		#	index = utf8.process(index)
		#	cat = utf8.process(cat)
		#	entry = "{" + "}\n{".join(articles) + "}"
		#	if provider.categories.has_key(cat):
		#		entry = utf8.process(index) + "\n" + \
		#				parser.wiki_to_dict(index, provider.categories[cat]) + \
		#				"\n" + "_" * 30 + "\n" + \
		#				entry
		#	dict_object.addentry(entry, [index, cat])

	def get_info(self, name, provider):
		"""Try to get some information from the database dump.	Uses
		the Provider object's get_meta_info method."""
		dictname = name  # provider.get_meta_info("Wikititlesuffix")
		dictname = dictname.strip().replace(" ", "_")
		if dictname == "Wikititlesuffix":
			dictname = name
		elif (dictname.upper() in ["WIKIPEDIA", "WIKIBOOKS",
								   "WIKTIONARY", "WIKIQUOTE"]	
			or not reduce(lambda x,y:
						  x and
						  (y in ascii_letters+"-_"), dictname)):
			dictname = name
		dictfilename = dictname.replace(" ", "-")
		return (dictname, dictfilename)

	def create_dict_object(self, dictfilename):
		"""Create dict object. Delete files if necessary."""
		remove_if_exists(dictfilename + ".dict")
		remove_if_exists(dictfilename + ".dict.dz")
		remove_if_exists(dictfilename + ".index")
		return dictdlib.DictDB(dictfilename, mode = 'write', quiet = True)

	def finish_dict(self, dict_object, provider, dictname):
		"""Set some meta-info about the dict and close the object (and
		hence the files)."""
		match = re.search("http://.*?\.org", "none")
		#		  provider.get_meta_info("Printsubtitle"))
		url = match and match.group(0) + "/" or "http://wikipedia.org/"
		if url.find("http") > 0:
			url = url[url.index("http"):url.index("org")+3]
		dict_object.seturl(url)

		#dict_object.setlonginfo(info)
		dict_object.setshortname(dictname.replace("_", " "))
		dict_object.finish()

	def dictzip(self, dictfilename):
		"""Apply dictzip to dictfilename."""
		print "* Applying dictzip"
		commands.getstatusoutput("dictzip " + dictfilename + ".dict")
		print "* Created", dictfilename + ".dict.dz and",
		print dictfilename + ".index."


def main():
	"""Main routine."""

	opt_parser = OptionParser("")
	(options, args) = opt_parser.parse_args()

	if not args:
		print __doc__
	else:
		for filename in args:
			d2d = Dump2dict(filename)

if __name__ == "__main__":
	main()



