#!/usr/bin/env python
""" file_certs.py: File-based Trust Metric Profiles (example code)
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


	File-based Profiles on which certifications (also file-based) can
	be stored and retrieved for evaluation by Trust Metrics.

	...with NO LOCKING!  ...yet.

	unfortunately, type info of non-string profile names
	is lost on the [very basic] file-format.  so, whilst
	the trust metric and net flow evaluation code couldn't
	care less what the type of its nodes is, the file
	storage does.

	*shrug*.  who wants to be a number, anyway.

	WARNING: there is a lot of class-context overloading
	in this demonstration code, particularly DictCertifications
	and FileCertifications get reused rather inappropriately.

	... but it will do, as a simple example.  [i'll get round
	to doing a SQL and an XML one, later, properly].

"""

from certs import DictCertifications, CertInfo
from profile import Profile
from string import join
from os import makedirs, path


# deal with having to store strings as text. *sigh*
def unsafe_str(s):
	s = s.strip()
	if s[0] != "'" and s[0] != '"':
		# paranoia.  don't want code from file evaluated!
		# if someone edits a file and removes the first
		# quote but not the second, TOUGH.
		s = '"""'+s+'"""'
	return eval(s)

# yes, we _do_ want the quotes.
# they get removed by unsafe_str, above, on retrieval.
def safe_str(s):
	return repr(str(s))

class FileCertifications(DictCertifications):
	"""	Certification file of format:
		certname1:	user1=level1, user2=level2, ...
		certname2:	user1=level1, user2=level2, ...
	"""

	def set_filename(self, file):
		self.f = file
		try:
			p, f = path.split(file)
			makedirs(p)
		except:
			pass

	def __read_dict(self):

		self.info = {}
		try:
			f = open(self.f,"rw")
		except:
			return

		for l in f.readlines():
			l = l.strip()
			if len(l) == 0:
				continue
			[ftype, certs] = l.split(":")
			ftype = unsafe_str(ftype)
			certs = certs.split(",")
			for cert in certs:
				[fname, flevel] = cert.split("=")
				l = unsafe_str(flevel)
				fn = unsafe_str(fname)
				DictCertifications.add(self, ftype, fn, l)
		f.close()

	def __write_dict(self):

		f = open(self.f,"w")
		for key in DictCertifications.cert_keys(self):
			l = safe_str(key)+": "
			certs = []
			dict = DictCertifications.certs_by_type(self, key)
			for c in dict.keys():
				certs.append(safe_str(c)+"="+safe_str(dict[c]))
			l += join(certs, ", ") + "\n"
			f.write(l)
		f.close()

	def cert_keys(self):
		self.__read_dict()
		return DictCertifications.cert_keys(self)

	def certs_by_type(self, type):
		self.__read_dict()
		return DictCertifications.certs_by_type(self, type)

	def cert_type_keys(self, type, name):
		self.__read_dict()
		return DictCertifications.certs_type_keys(self, type, name)

	def add(self, type, name, level):
		self.__read_dict()
		DictCertifications.add(self, type, name, level)
		self.__write_dict()

	def remove(self, type, name):
		self.__read_dict()
		DictCertifications.remove(self, type, name, level)
		self.__write_dict()

	def cert_level(self, type, name):
		self.__read_dict()
		return DictCertifications.cert_level(self, type, name)

class FileProfile(Profile):

	def __init__(self, name, CertClass):
		Profile.__init__(self, name, CertClass)
		self._certs_by_subj.set_filename("users/"+str(name)+"/certs.subj")
		self._certs_by_issuer.set_filename("users/"+str(name)+"/certs.issuer")

		# overload meaning of FileCertifications here to store user-profile.
		self.info = FileCertifications()
		self.info.set_filename("users/"+str(name)+"/profile")

	def set_filename(self, file):
		self.info.set_filename(file)

	def info_keys(self):
		return self.info.cert_keys()

	def infos_by_type(self, type):
		return self.info.certs_by_type(type)

	def info_type_keys(self, type, name):
		return self.info.certs_type_keys(type, name)

	def add(self, type, name, level):
		self.info.add(type, name, level)

	def remove(self, type, name):
		self.info.remove(type, name, level)

	def info_index(self, type, name):
		return self.info.cert_level(type, name)


class FileCertInfo(CertInfo):
	"""	This is probably some of the clumsiest code ever written.
		overload DictCertification - because it's been a really
		good, lazy weekend, to store an unordered list (seeds),
		an ordered list (levels) etc.

		yuck.  please, someone shoot me or do a better job,
		_esp._ for example code.
	"""

	def cert_seeds(self, idxn):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		# clumsy usage of a dictionary as an unordered list.  argh.
		d = d.certs_by_type("seeds")
		return d.keys()

	def cert_levels(self, idxn):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		dict = d.certs_by_type("levels")
		# clumsy usage of a dictionary into an ordered list.  argh.
		keys = dict.keys()
		l = [None] * len(keys)
		for idx in keys:
			l[int(idx)] = dict[idx]
		return l

	def cert_level_default(self, idxn):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		[d] = d.certs_by_type("default level").keys()
		return d

	def cert_level_min(self, idxn):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		[d] = d.certs_by_type("min level").keys()
		return d

	def cert_tmetric_type(self, idxn):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		[d] = d.certs_by_type("type").keys()
		return d

	def add_cert_seed(self, idxn, seed):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		# clumsy usage of a dictionary as an unordered list.  argh.
		return d.add("seeds", seed, None)

	def add_cert_level(self, idxn, level, index):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		# clumsy usage of a dictionary as an index-ordered list.  argh.
		return d.add("levels", index, level)

	def set_cert_level_default(self, idxn, dflt_level):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		return d.add("default level", dflt_level, None)

	def set_cert_level_min(self, idxn, min_level):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		return d.add("min level", min_level, None)

	def set_cert_tmetric_type(self, idxn, type):
		d = FileCertifications()
		d.set_filename("certs/"+str(idxn))
		return d.add("type", type, None)

def test():

	from profile import Profiles
	from tm_calc import TrustMetric
	from pprint import pprint

	f = FileCertInfo()

	f.add_cert_seed('like', '55')
	f.add_cert_seed('like', 'luke')

	f.add_cert_level('like', 'none', 0)
	f.add_cert_level('like', "don't care", 1)
	f.add_cert_level('like', 'good', 2)
	f.add_cert_level('like', 'best', 3)

	f.set_cert_level_default('like', "don't care")
	f.set_cert_level_min('like', 'none')
	f.set_cert_tmetric_type('like', 'to')

	f.add_cert_seed('hate', 'heather')
	f.add_cert_seed('hate', '10')

	f.add_cert_level('hate', 'none', 0)
	f.add_cert_level('hate', "don't care", 1)
	f.add_cert_level('hate', 'dislike', 2)
	f.add_cert_level('hate', 'looks CAN kill', 3)

	f.set_cert_level_default('hate', "don't care")
	f.set_cert_level_min('hate', 'none')
	f.set_cert_tmetric_type('hate', 'to')

	p = Profiles(FileProfile, FileCertifications)
	r = p.add_profile('luke')
	r.add("name", 0, "luke")
	r.add("name", 1, "kenneth")
	r.add("name", 2, "casson")
	r.add("name", 3, "leighton")
	r.add("info", 0, "likes python a lot - thinks it's really cool")
	r.add("info", 1, "groks network traffic like he has a built-in headsocket")

	p.add_profile('heather')
	p.add_profile('bob')
	p.add_profile('mary')
	p.add_profile('lesser fleas')
	p.add_profile('little fleas')
	p.add_profile('fleas')
	p.add_profile('robbie the old crock pony')
	p.add_profile('tart the flat-faced persian cat')
	p.add_profile('mo the mad orange pony')
	p.add_profile('55') 
	p.add_profile('10')
	p.add_profile('2')
	p.add_profile('fleas ad infinitum')

	p.add_cert('luke', 'like', 'heather', 'best')

	p.add_cert('heather', 'like', 'luke', 'best')
	p.add_cert('heather', 'like', 'robbie the old crock pony', 'best')
	p.add_cert('heather', 'like', 'tart the flat-faced persian cat', 'best')
	p.add_cert('heather', 'like', 'mo the mad orange pony', 'best' )

	p.add_cert('bob', 'like', 'mary', 'good')
	p.add_cert('bob', 'like', 'heather', 'good')

	p.add_cert('mary', 'like', 'bob', 'good')

	p.add_cert('fleas', 'like', 'little fleas', 'good')
	p.add_cert('little fleas', 'like', 'lesser fleas', 'best')
	p.add_cert('lesser fleas', 'like', 'fleas ad infinitum', 'best')

	p.add_cert('robbie the old crock pony', 'like', 'fleas', 'best')
	p.add_cert('55', 'like', '10', 'none')
	p.add_cert('10', 'like', '2', 'best')

	p.add_cert('heather', 'hate', 'bob', 'dislike' )
	p.add_cert('heather', 'hate', 'fleas', 'looks CAN kill' )
	p.add_cert('fleas', 'hate', 'mary', 'dislike')
	p.add_cert('10', 'hate', '55', 'looks CAN kill')

	t = TrustMetric(f, p)
	r = t.tmetric_calc('like')
	pprint(r)

	r = t.tmetric_calc('like', ['heather'])
	pprint(r)

	r = t.tmetric_calc('hate')
	pprint(r)

if __name__ == '__main__':
	test()

