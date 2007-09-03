#!/usr/bin/env python
"""	profile.py: Base classes to evaluate Trust Metrics.
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


	see file_certs.py for a working example on how to
	over-ride Profile, CertClass and CertInfo.
"""

from certs import Certifications

class Profile:

	def __init__(self, name, CertClass):
		self._certs_by_subj = CertClass()
		self._certs_by_issuer = CertClass()

	def add_cert_issuer(self, name, type, level):
		self._certs_by_issuer.add(type, name, level)

	def add_cert_subj(self, name, type, level):
		self._certs_by_subj.add(type, name, level)

	def del_cert_issuer(self, name, type, level):
		self._certs_by_issuer.remove(type, name, level)

	def del_cert_subj(self, name, type, level):
		self._certs_by_subj.remove(type, name, level)

	def get_certs_issuer(self, type):
		try:
			return self._certs_by_issuer.certs_by_type(type)
		except:
			return {}

	def get_certs_subj(self, type):
		try:
			return self._certs_by_subj.certs_by_type(type)
		except:
			return {}

	def get_cert_issuer(self, name, type):
		try:
			return self._certs_by_issuer.add(type, name)
		except:
			return {}

	def get_cert_subj(self, name, type, level):
		try:
			return self._certs_by_subj.add(type, name)
		except:
			return {}

class Profiles:

	def __init__(self, ProfileClass=Profile, CertClass=Certifications):

		self.info = {}
		self.ProfileClass = ProfileClass
		self.CertClass = CertClass
		# adding this to make it easier to import datasets
		self.create_profile_if_needed = True

	def add_profile(self, name):
		profile = self.ProfileClass(name, self.CertClass)
		self.info[name] = profile
		return profile

	def get_profile(self, name):
		if self.create_profile_if_needed and not name in self.info.keys():
			# print "creating new node:", name 
			self.add_profile(name)
		return self.info[name]

	def get_profile_keys(self):
		return self.info.keys()

	def add_cert(self, subj, type, issuer, level):
		self.get_profile(issuer).add_cert_issuer(subj, type, level)
		self.get_profile(subj).add_cert_subj(issuer, type, level)

	def del_cert(self, subj, type, issuer, level):
		get_profile(issuer).del_cert_issuer(self, subj, type, level)
		get_profile(subj).del_cert_subj(self, issuer, type, level)

def test():
	print "hmm..."

if __name__ == '__main__':
	test()

