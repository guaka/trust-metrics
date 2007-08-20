# -*- coding: utf-8 -*-

# Copyright (c) 2004, 2005 Guaka
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
Parse the articles provided by the wik2dict Provider.
"""

import re
import textwrap
from htmlentitydefs import entitydefs
import pprint		

#wik2dict modules
from lang_iso_codes import lang_iso_codes
from unicode_crap import en_utf8, de_latin1
import unicode_crap

##########################

class Parser:
	"""
	Parse MediaWiki layout and convert into dict format.
	"""

	def __init__(self): #, options, cat_string, image_string, utf8, logger):
		
		#self.verbose = options.verbose
		self.width = 60 # options.width
		#self.utf8 = utf8
		self.utf8 = unicode_crap.UnicodeProcessor()
		#self.no_warnings = options.no_warnings
	
		self.PAGENAME = "preprocessing"

		self.wrapper = textwrap.TextWrapper(break_long_words = False) #, width = options.width)
		self.entitydefs = entitydefs
		for entity in self.entitydefs:
			self.entitydefs[entity] = self.process_html(self.entitydefs[entity])

		for lang in lang_iso_codes:
			lang_iso_codes[lang] = self.process_html(lang_iso_codes[lang])
			#if not options.latin1:
			#	lang_iso_codes[lang] = en_utf8(de_latin1(lang_iso_codes[lang]))
			
		#self.repl_intlink_with_desc = lambda m: "{" + m.group(2) + "}"
		self.repl_intlink_no_desc = lambda m: "{" + m.group(1) + "}"
		self.extlinks_nodesc_func = lambda x: x.group(2)
		self.extlinks_desc_func = lambda x: "{" + x.group(3) + " (" + x.group(2) + ")}"
		#self.repl_interwiki = lambda m: (lang_iso_codes[m.group(1)] + 
		#								 ": {" + m.group(2).replace("_", " ") + "}")
		self.repl_interwiki3 = lambda m: "{" + m.group(2).replace("_", " ") + "}"

		self.categories = {}

	def repl_category(self, m):
		cat = m.group(2).capitalize()
		if not cat in self.categories:
			self.categories[cat] = []
		self.categories[cat].append(self.PAGENAME)
		return "{" + m.group(1) + ":" + m.group(2) + "} "

	def repl_intlink_with_desc(self, match):
		desc = match.group(2)
		link = match.group(1).replace("_", " ")
		if link[0] == "#":
			return desc
		elif desc.upper() == link.upper():
			return "{" + desc + "}"
		else:
			return desc + " ({" + link + "})"

	def set_namespaces(self, namespaces):
		self.namespaces = namespaces
		namespaces_rev = dict(map(lambda x: (x[1], x[0]), namespaces.items()))
		self.image_string = namespaces_rev[6]
		self.cat_string = namespaces_rev[14]
		self.re_drop_imgs = re.compile("\[\[(" + self.image_string + "):(.+?)\]\]",
									   re.IGNORECASE + re.DOTALL)
		self.re_category = re.compile("\[\[(" + self.cat_string + "):(.+?)(\|.+?)?\]\]",
									  re.IGNORECASE)
		

	def set_messages(self, messages):
		self.messages = messages
		if False:
     		  for m in self.messages:
			self.PAGENAME = m
			msg = (self.messages[m])
			#msg = self.process_html(self.messages[m])
			msg = self.replace_messages(msg)
			msg = self.process_links(msg)
			msg = self.process_tables(msg)
			self.messages[m] = msg

	re_msg = re.compile("({{)(.+?)(}})")
	def repl_message(self, match_obj):
		m = match_obj.group(2)
		k = m.upper().replace("MSG:", "").replace("_", " ")
		if k in self.messages:
			return self.messages[k]
		elif k == "PAGENAME" and hasattr(self, "PAGENAME"):
			return self.PAGENAME
		else:
			if False:
				#something for the logger
				#print "Message", m, "not found in", self.PAGENAME
				pass
			return m # "{{" + m + "}}"

	def replace_messages(self, s):
		return self.re_msg.sub(self.repl_message, s)

	def test_regexp(self, regexp, s):
		for l in s.split("\n"):
			m = regexp.search(l)
			if m:
				print
				print self.PAGENAME
				print l
				for i, g in enumerate(m.groups()):
					print g

	langcodes_restr = reduce(lambda x, y: x+"|"+y, lang_iso_codes)
	re_interwiki = re.compile("\[\[(" + langcodes_restr + "):([^]][^|]*?)\]\]")
	re_interwiki2 = re.compile("\[\[(" + langcodes_restr + "):\]\]")
	re_interwiki3 = re.compile("\[\[(w:" + langcodes_restr + "):([^]][^|]*?)\]\]")

	re_intlink_with_desc = re.compile("\[\[([^]]+?)\|(.+?)\]\]", re.DOTALL)
	re_intlink_no_desc = re.compile("\[\[([^]]+?)\]\]", re.DOTALL)
	def process_links(self, s):
		#could use subn to add "interwikilinks: " or so
		s_orig = s
		s = s.replace("[[]]", "")
		#s = self.re_interwiki.sub(self.repl_interwiki, s)
		s = self.re_interwiki2.sub("", s)
		s = self.re_interwiki3.sub(self.repl_interwiki3, s)
		#s = self.re_drop_cats_n_imgs.sub("", s)
		s = self.re_drop_imgs.sub("", s)
		s = self.re_category.sub(self.repl_category, s)
		n = 1
		#while n:
		#	(s, n) = self.re_remove_stuff_before_dp.subn("", s) #such as "w:en:"
		#if s1 != s:
		#	self.test_regexp(self.re_remove_stuff_before_dp, s_orig)
		s = self.re_intlink_with_desc.sub(self.repl_intlink_with_desc, s)
		s = self.re_intlink_no_desc.sub(self.repl_intlink_no_desc, s)
		sdb_pos = s.find("[[")
		if sdb_pos > 0:
			s_orig_sdb_pos = s_orig.find(s[sdb_pos:sdb_pos + 6])

			warning = "problem with processing wikilinks in " + self.PAGENAME + "\n"
			warning += "_________probably here_________"
			for line in s_orig[max(0, s_orig_sdb_pos-100):s_orig_sdb_pos+100].split("\n"):
				warning += "\t\t" + line + "\n"
			warning += "_________processed version_____"
			for line in s[max(0, sdb_pos-100):sdb_pos+100].split("\n"):
				warning += "\t\t" + line + "\n"
			warning += "_______________________________"
			#self.logger.warning(warning)
			
		s = self.re_extlinks_nodesc.sub(self.extlinks_nodesc_func, s)
		return self.re_extlinks_desc.sub(self.extlinks_desc_func, s)

	re_htmlentity = re.compile("&([^#]+?);")
	def repl_htmlentities(self, match_obj):
		k = match_obj.group(1)
		if k in self.entitydefs:
			return self.entitydefs[k]
		#if k[0] == "#":
		#	# print k[1:], #unichr(int(k[1:]))
		#	#return unichr(int(k[1:])) #
		#	#return "\u" + k[1:]
		#	return match_obj.group(0)
		else:
			return k

	re_comment = re.compile("<!--.*?-->", re.DOTALL)
	re_html = re.compile("<.+?>", re.DOTALL)
	def process_html(self, s):
		#pprint.pprint(s)
		s = self.re_comment.sub("", s) #first remove HTML comments
		s = self.re_html.sub("", s) #then remove other HTML stuff
		return self.re_htmlentity.sub(self.repl_htmlentities, s)

	def process_tables(self, s):
		#elif line[:2] == "|+":  CAPTION  ??
		# 	line = "_______"

		# should only process {|.*?|}
		table_split = re.split(re.compile("{\|(.*?)\|}", re.DOTALL), s)

		if table_split > 1:
			#  [ no_table, table, no_table ...]

			r = []
			for line in filter(None, s.split("\n")):
				if line[:2] == "{|" or line[:2] == "|}":
					line = ""
				elif line[:2] == "|-":
					line = "_______"
				elif line[0] == "|" or line[0] == "!":
					line = "|" + line[1:].replace("!!", "||")

					split = line.split("|")
					if len(split) > 2:
						line = " ".join(split[2:])
					else:
						line = split[1]
				r.append(line)
			s = "\n".join(r)
		return s

	bullets = "*#*-" + "." * 160
	re_bullets = re.compile("^(\*+)")  # or \S?
	def process_line(self, line):
		firstchar = line[0]
		if firstchar == "#":
			self.numbering += 1
		else:
			self.numbering = 0

		if firstchar == "=":
			line = "\n  " + line.replace("=", "")

		elif line[:4] == "----":
			line = "   " + (self.width - 3) * "_" + "\n"

		else:
			m_bullets = self.re_bullets.match(line)
			line = self.utf8.process(line)
			if m_bullets:
				bullet = self.bullets[len(m_bullets.group(1)) - 1]
				l = len(m_bullets.group(1))
				line = self.re_bullets.sub("", line)
				self.wrapper.initial_indent    = " " * l + bullet + " "
				self.wrapper.subsequent_indent = " " * (l+3)
			elif self.numbering:
				nr = str(self.numbering) + ") "
				line = line[1:]
				if self.numbering < 10:
					nr = " " + nr
				self.wrapper.initial_indent    = nr
				self.wrapper.subsequent_indent = len(nr) * " "
			elif line[0] == ":":
				line = line[1:]
				self.wrapper.initial_indent    = "    "
				self.wrapper.subsequent_indent = "    "
			else:
				self.wrapper.initial_indent    = ""
				self.wrapper.subsequent_indent = ""
			line = self.wrapper.fill(line)
		return line

	def add_space_if_link_on_2_lines(self, line):
		"""Add space if a link is split by the wrapper."""
		l, r = line.rfind("{"), line.rfind("}")
		#print l, r, line[l:r+1]
		if l > r:
			return line + " "
		return line

	re_notoc_etc = re.compile("__(START|NOTOC|TOC|END|NOEDITSECTION)__")
	re_extlinks_nodesc = re.compile("(\[)(\S*?)(\])")
	re_extlinks_desc = re.compile("(\[)(.*?) (.*?)(\])")
	def wiki_to_dict(self, pagename, s):
		self.PAGENAME = pagename
		if s is None:
			return ""
		s = self.process_html(s)
		s = self.re_notoc_etc.sub("", s)
		s = self.replace_messages(s)  #self.re_msg.sub(self.repl_message, s)
		s = self.process_links(s)
		s = self.process_tables(s)
		
		self.numbering = 0
		lines = filter(None, s.split("\n"))
		lines = map(self.process_line, lines)
		text = "\n".join(lines)
		lines = filter(None, text.split("\n"))
		lines = map(self.add_space_if_link_on_2_lines, lines)
		return "\n".join(lines)

