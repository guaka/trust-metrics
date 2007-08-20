# -*- coding: utf-8 -*-

# Copyright (c) 2004 Guaka
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
wik2dict's Provider classes.

These are an abstraction of wik2dict's retrieval mechanism.
Currently lacking a MySQL Provider.
"""
#
import os
import re
import bz2, gzip
from sets import Set

import pprint
import elementtree.ElementTree as ET

# wik2dict modules

from Counter import Counter
##################################

mwxml = "{http://www.mediawiki.org/xml/export-0.3/}"

class XMLfile_Provider:
  def __init__(self, filename):
	self.filename = filename
	self.tree = ET.parse(filename)

	self.nr_articles = 0
	self.article_titles = Set()
	self.article_redirects = {}
	self.articles = {}
	self.messages = {}
	self.message_redirects = {}
	self.meta_info = {}
	self.categories = {}

	self.namespaces = self._get_namespaces()

	x_pages = self.tree.findall(mwxml + "page")
	for x_page in x_pages:
		title = x_page.find(mwxml + "title").text
		text = x_page.find(mwxml + "revision").find(mwxml + "text").text
		ns, ns_name = 0, ""
		for ns_text in self.namespaces:
			if title[:len(ns_text)] == ns_text:
				ns = self.namespaces[ns_text]
				nsname = ns_text
		if ns == 0:
			self.articles[title] = text
		elif ns == 8:
			self.messages[title] = text
		elif ns == 14:
			self.categories[title] = text

  def _get_namespaces(self):
	namespaces = {}
	x_siteinfo = self.tree.find(mwxml + "siteinfo")
	x_namespaces = x_siteinfo.find(mwxml + "namespaces")
	for x_ns in x_namespaces:
		if x_ns.text is None:
			namespaces[""] = int(x_ns.get('key'))
		else:
			namespaces[x_ns.text] = int(x_ns.get('key'))
	return namespaces

if __name__ == "__main__":
	x = XMLfile_Provider("eswq.xml")
	#x = XMLfile_Provider("liwk.xml")


class Dumpfile_Provider:
	"""
	For 'old style' MediaWiki SQL dumps.
	
	Deprecated. 
	Use wik2dict 0.3.9 if you need it.
	"""
	articles_in_first_pass = True
	meta_info_fields = [
		"Nstab-category", "Nstab-image", "Nstab-template",
		"Wikititlesuffix", "Printsubtitle"]
	def __init__(self, filename):
		self.filename = filename

		self._articles = {}
		self.nr_articles = 0
		self.article_titles = Set()
		self.article_redirects = {}
		self.messages = {}
		self.message_redirects = {}
		self.meta_info = {}
		self.categories = {}

		self.open()
		print "* Parsing", filename + " in",
		if self.articles_in_first_pass:
			print "one pass."
		else:
			print "two passes."
		self.get_everything()

	def reopen(self):
		"""For bz2s this is much quicker than .seek(0)."""
		#GzipFile doesn't know .closed
		#if file.__class__ == gzip.GzipFile or not self.file.closed:
		self.file.close()
		self.open()

	def open(self):
		ext = os.path.splitext(self.filename)[1]
		if ext == ".bz2":
			self.file = bz2.BZ2File(self.filename, "r")
		elif ext == ".gz":
			self.file = gzip.GzipFile(self.filename, "r")
		else:
			self.file = open(self.filename)

	def is_redirect(self, s):
		m = self.re_redirect.search(s)
		return m and m.group(1).replace(" ", "_")


	def pre_process(self, s):
		s = s.replace("\\n", "\n").replace("\\r", "\n")
		return s.replace("\\'", "'").replace('\\"', '"')
	
	re_field = re.compile("\((\d+),(0|8|10|14),'([^']+?)','(.+?)','(.*?)'," +
						  "(\d+),'(.+?),'(\d{14})','(.*?)',(\d+?),(0|1)," +
						  "(0|1),([0|1]),(.*?),'(\d+?)','(\d+?)'\)" +
						  "(?=[,;[^\]])")
	re_redirect = re.compile("#redirect\s*\[\[(.+?)\]\]",
							 re.IGNORECASE + re.DOTALL)
	def get_everything(self):
		def repl(m):
			namespace = int(m.group(2))
			title = m.group(3).replace("_", " ")
			text = self.pre_process(m.group(4))
			redir = self.is_redirect(text)
			#print namespace, title
			
			if namespace == 0:
				if redir:
					redir = redir.replace("_", " ")
					self.article_redirects[title] = redir
					#if "Rad" in redir:
					#	print title, redir + "       "
				elif self.articles_in_first_pass:
					self._articles[title] = text
					self.nr_articles += 1
				else:
					self.article_titles.add(title)
					self.nr_articles += 1
			elif namespace == 10:
				if redir:
					redir = redir.replace("_", " ")
					self.message_redirects[title] = redir
					#print "Message redirect!"
				else:
					self.messages[title.upper()] = text
			elif namespace == 8:
				if title in self.meta_info_fields:
					self.meta_info[title] = text
			elif namespace == 14:
				self.categories[title] = text
			return ""

		counter = Counter(msg = "* Parsing dumpfile  ")
		infofmt = "  %s: %i  "
		show = ""
		for i, l in enumerate(self.file):
			if (l[:23] == "INSERT INTO cur VALUES " or
				l[:25] == "INSERT INTO `cur` VALUES "):
				self.re_field.sub(repl, l)
				show = infofmt % ("articles", self.nr_articles)
				show += infofmt % ("redirects", len(self.article_redirects))
				show += infofmt % ("categories", len(self.categories))
				show += infofmt % ("messages", len(self.messages))
				counter.show(show)
		counter.finish(show)

		self.messages["NUMBEROFARTICLES"] = str(self.nr_articles)

		if self.articles_in_first_pass:
			self.file.close()
			self.article_titles = Set(self._articles)
		else:
			self.reopen()

	def articles(self):
		for index, article in self._articles.items():
			yield index, article

	def get_meta_info(self, field):
		if field in self.meta_info:
			return self.meta_info[field]
		else:
			print "///// WARNING: field not set:", field
			return field

		#"CURRENTYEAR": get_sql("YEAR(MAX(cur_timestamp))"),
		#"CURRENTMONTH": get_sql("MONTH(MAX(cur_timestamp))"),
		#"CURRENTMONTHNAME": get_sql("MONTHNAME(MAX(cur_timestamp))"),
		#"CURRENTDAY": get_sql("DAYOFMONTH(MAX(cur_timestamp))"),
		#"CURRENTDAYNAME": get_sql("DAYNAME(MAX(cur_timestamp))"),
		#"CURRENTTIME": get_sql("DATE_FORMAT(MAX(cur_timestamp), '%H:%i:%s')"),

class Dumpfile_Provider_Twopass(Dumpfile_Provider):
	"""First pass: get everything but the articles."""

	articles_in_first_pass = False

	def articles(self):
		def repl(m):
			namespace = int(m.group(2))
			text = self.pre_process(m.group(4))
			if namespace == 0:
				if not self.is_redirect(text):
					title = m.group(3).replace("_", " ")
					articles.append((title, text))
			return ""

		for i, l in enumerate(self.file):
			if (l[:23] == "INSERT INTO cur VALUES " or
				l[:25] == "INSERT INTO `cur` VALUES "):
				articles = []
				self.re_field.sub(repl, l)
				for title, text in articles:
					yield title, text


