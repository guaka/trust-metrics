#!/usr/bin/env python
"""	tm_calc.py: Trust Metric Calculation
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


	tm_calc.py is based on virgule.sourceforge.net's
	tm_calc.c, written by Luke Kenneth Casson Leighton,
	which is modified from the original c code,
	tmetric.c:
	Copyright (C) 1999-2000 Raph Levien <raph@acm.org>

	translated into geek-language, Trust Metrics are
	"Cascading (or Hierarchical) Access Controls"

	How To Use This Code:

	p = Profiles(ProfileClass, CertificationsClass)
	c = CertInfoClass()
	t = TrustMetric(c, p)
	r = t.tmetric_calc(certification_type_name, [optional seed list])

	Please see the README.txt for a detailed explanation.

"""

from net_flow import NetFlow, Debug
import traceback

# No profile can have a profile name of None: this is reserved
# as the SUPERSINK.
SUPERSINK = None

class TrustMetric(Debug):
	"""	TrustMetric.  first cut at porting tm_calc.c to python.

		object-orientated-wise, it's a little clumsy.
		but it works :)
	"""

	def __init__(self, certinfo, tree):

		self.certinfo = certinfo
		self.tree = tree

		Debug.__init__(self)

	def tmetric_find_node(self, idxn, info, u):

		if self.default_level < self.min_level:
			self.default_level = self.min_level

		idx = self.flows[self.min_level].netflow_find_node(u)
		if not info.has_key(idx):
		
			info[idx] = self.default_level

			for i in range(self.default_level, self.max_levels):
				if idx != self.flows[i].netflow_find_node(u):
					self.warning("inconsistency in netflow_find_node!\n"
					             "user %s returned index %s\n" % \
								 (str(u), str(idx)))

		return idx

	def tmetric_stage1(self, un, certs, idxn):
		""" when no links to: link to seed, at observer level.
			this sustains the user at a default level
			instead of them dropping to CERT_LEVEL_NONE.
		"""

		if self.min_level > self.default_level:
			return

		if certs and len(certs.keys()) > 0:
			return

		for i in range(self.min_level, self.default_level):
			self.flows[i].netflow_add_edge(SUPERSINK, un)

	def tmetric_stage2(self, un, certs, idxn):
		"""	link a user's certs to level specified by each
			cert _and_ implicitly at every level below
			the specified level.
		"""

		if certs is None:
			return

		for cert_subj in certs.keys():

			self.debug("cert_subj: " + str(cert_subj))

			self.tmetric_find_node(idxn, self.result, un)

			if cert_subj is None:
				continue

			self.tmetric_find_node(idxn, self.result, cert_subj)

			try:
				level_str = certs[cert_subj]
			except:
				level_str = None
			self.debug('level: '+str(level_str))
			try:
				level = self.levels.index(level_str)
			except:
				war = "level not found! %s %s %s" % \
					(idxn, level_str, str(self.levels))
				self.warning(war)
				raise war #"level not found!"

			self.debug("%s %s" % (str(level_str), str(level)))

			#down-flow links to level down to min 
			for i in range(self.min_level, level+1):
				self.flows[i].netflow_add_edge(un, cert_subj)

	def tmetric_add(self, issuer, in_type, idxn):

		if issuer is None:
			return

		profile = self.tree.get_profile(issuer)

		if in_type:
			idxn_certs = profile.get_certs_issuer(idxn)
			idxn_in_certs = profile.get_certs_subj(idxn)
		else:
			idxn_certs = profile.get_certs_subj(idxn)
			idxn_in_certs = profile.get_certs_issuer(idxn)

		if profile is None:
			return

		self.tmetric_find_node(idxn, self.result, issuer)

		# stage 1 is only relevant to down-flows
		self.tmetric_stage1(issuer, idxn_in_certs, idxn)
		self.tmetric_stage2(issuer, idxn_certs, idxn)

	def tmetric_loop(self, in_type, idxn):
		"""
		 * tmetric_loop: Run trust metric.
		 * @vr: The request context.
		 * @seeds: An array of usernames for the seed.
		 * @n_seeds: Size of @seeds.
		 * @caps: Capacity array.
		 * @n_caps: Size of @caps.
		 *
		 * Return value: NodeInfo array.
		"""

		for name in self.tree.get_profile_keys():
			self.tmetric_add(name, in_type, idxn)

	def tmetric_run(self, idxn, seeds, caps, tmetric_type):
		"""
		 * tmetric_run: Run trust metric.
		 * @idxn: the name of the trust metric
		 * @seeds: An array of usernames for the seed.
		 * @caps: Capacity array.
		 * @tmetric_type: the type of the trust metric
		 *
		 * Return value: NodeInfo array.
		"""
		in_type = tmetric_type in ["in", "for", "of"]

		self.flows = []
		for i in range(self.max_levels):
			flow = NetFlow()
			self.flows.append(flow)
			# flow.set_debuglevel(1)

		self.result = {}

		dn_seed = self.tmetric_find_node(idxn, self.result, SUPERSINK)

		for seed_name in seeds:

			self.tmetric_find_node(idxn, self.result, seed_name)

			for i in range(self.min_level, self.max_levels):
				self.flows[i].netflow_add_edge(SUPERSINK, seed_name)

		self.tmetric_loop(in_type, idxn)

		# calculate maximum flow
		for i in range(self.min_level, self.max_levels):

			flow = self.flows[i].netflow_max_flow_extract(dn_seed, caps)
			for idx in self.result.keys():
				if flow[idx] > 0:
					self.result[idx] = i

		del self.flows

	def get_tmetric_results(self):
		return self.result

	def tmetric_calc(self, idxn, seeds=None):
		"""	tmetric_calc.  perform a trust metric evaluation.
		"""

		caps = [ 800, 200, 50, 12, 4, 2, 1 ]
		general_tmetric_calc = 0
		certinfo = self.certinfo

		if seeds is None:
			general_tmetric_calc = 1

		if idxn is None:
			raise "No certification type was requested"

		if general_tmetric_calc:
			seeds = certinfo.cert_seeds(idxn)

		if seeds is None or len(seeds) == 0:
			raise "There are no seeds to calculate the trust metric for %s.\n" \
				  "You will need to specify at least a single seed-name\n" % idxn

		levels = certinfo.cert_levels(idxn)
		self.levels = levels
		self.max_levels = len(levels)
		self.min_level = levels.index(certinfo.cert_level_min(idxn))
		self.default_level = levels.index(certinfo.cert_level_default(idxn))
		tmetric_type = certinfo.cert_tmetric_type(idxn)

		if tmetric_type is None:
			raise "Unknown tmetric type %s" % idxn

		self.tmetric_run(idxn, seeds, caps, tmetric_type)
		nodeinfo = self.get_tmetric_results()

		if not nodeinfo:
			return nodeinfo

		# must delete the "supersink" node.  hope like hell
		# no-one decided to use this as a real name.
		if nodeinfo.has_key(SUPERSINK):
			del nodeinfo[SUPERSINK]

		for i in nodeinfo.keys():

			level = nodeinfo[i]
			if level <= self.default_level and \
				self.default_level <= self.min_level:
				del nodeinfo[i]
				continue

			nodeinfo[i] = levels[level]

		return nodeinfo

def test():

	from certs import CertInfo

	class TestCertInfo(CertInfo):

		def __init__(self):

			self.info = {}
			self.info['like'] = {'levels': ['none', "don't care", 'good',
			                               'best'],
								 'seeds': ['luke', 55],
								 'min level': 'none',
								 'default level': "don't care",
								 'type': 'to'
								}

			self.info['hate'] = {'levels':
								  ['none', "don't care", 'dislike',
								  'looks CAN kill'],
								 'seeds': ['heather', 10],
								 'min level': 'none',
								 'default level': "don't care",
								 'type': 'to'
								}

		def cert_seeds(self, idxn):
			return self.info[idxn]['seeds']

		def cert_levels(self, idxn):
			return self.info[idxn]['levels']

		def cert_level_default(self, idxn):
			return self.info[idxn]['default level']

		def cert_level_min(self, idxn):
			return self.info[idxn]['min level']

		def cert_tmetric_type(self, idxn):
			return self.info[idxn]['type']

	from pprint import pprint
	from profile import Profiles, Profile
	from certs import DictCertifications

	# demonstration showing that numbers can certify and
	# be certified, not just strings.

	p = Profiles(Profile, DictCertifications)

	p.add_profile('luke')
	p.add_profile('heather')
	p.add_profile('bob')
	p.add_profile('mary')
	p.add_profile('lesser fleas')
	p.add_profile('little fleas')
	p.add_profile('fleas')
	p.add_profile('robbie the old crock pony')
	p.add_profile('tart, the flat-faced persian cat')
	p.add_profile('mo the mad orange pony')
	p.add_profile(55)
	p.add_profile(10)
	p.add_profile(2)
	p.add_profile('fleas ad infinitum')

	p.add_cert('luke', 'like', 'heather', 'best')

	p.add_cert('heather', 'like', 'luke', 'best')
	p.add_cert('heather', 'like', 'robbie the old crock pony', 'best')
	p.add_cert('heather', 'like', 'tart, the flat-faced persian cat', 'best')
	p.add_cert('heather', 'like', 'mo the mad orange pony', 'best' )

	p.add_cert('bob', 'like', 'mary', 'good')
	p.add_cert('bob', 'like', 'heather', 'good')

	p.add_cert('mary', 'like', 'bob', 'good')

	p.add_cert('lesser fleas', 'like', 'fleas ad infinitum', 'good')
	p.add_cert('little fleas', 'like', 'lesser fleas', 'good')
	p.add_cert('fleas', 'like', 'little fleas', 'good')
	p.add_cert('robbie the old crock pony', 'like', 'fleas', 'best')
	p.add_cert(55, 'like', 10, 'none')
	p.add_cert(10, 'like', 2, 'best')

	p.add_cert('heather', 'hate', 'bob', 'dislike' )
	p.add_cert('heather', 'hate', 'fleas', 'looks CAN kill' )
	p.add_cert('fleas', 'hate', 'mary', 'dislike')
	p.add_cert(10, 'hate', 55, 'looks CAN kill')

	t = TrustMetric(TestCertInfo(), p)
	r = t.tmetric_calc('like')
	pprint(r)

	r = t.tmetric_calc('like', ['heather'])
	pprint(r)

	r = t.tmetric_calc('hate')
	pprint(r)

if __name__ == '__main__':
	test()

