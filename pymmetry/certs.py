#!/usr/bin/env python
"""	certs.py: Certification base classes.
	Copyright (C) 2001 Luke Kenneth Casson Leighton <lkcl@samba-tng.org>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""

class Certifications:

	def cert_keys(self):
		raise NotImplementedError

	def certs_by_type(self, type):
		raise NotImplementedError

	def cert_type_keys(self, type, name):
		raise NotImplementedError

	def add(self, type, name, level):
		raise NotImplementedError

	def remove(self, type, name):
		raise NotImplementedError
		
	def cert_level(self, type, name):
		raise NotImplementedError

class DictCertifications(Certifications):

	def __init__(self):
		self.info = {}

	def cert_keys(self):
		return self.info.keys()

	def certs_by_type(self, type):
		return self.info[type]

	def cert_type_keys(self, type, name):
		return self.info[type].keys()

	def add(self, type, name, level):
		if not self.info.has_key(type):
			self.info[type] = {}
		self.info[type][name] = level

	def remove(self, type, name):
		if self.info.has_key(type) and \
		   self.info.type.has_key(name):
			del self.info[type][name]
		
	def cert_level(self, type, name):
		return self.info[type][name]

class CertInfo:

	def cert_seeds(self, idxn):
		raise NotImplementedError

	def cert_levels(self, idxn):
		raise NotImplementedError

	def cert_level_default(self, idxn):
		raise NotImplementedError

	def cert_level_min(self, idxn):
		raise NotImplementedError

	def cert_tmetric_type(self, idxn):
		raise NotImplementedError


def test():
	print "Hm..." # hmm?

if __name__ == '__main__':
	test()

