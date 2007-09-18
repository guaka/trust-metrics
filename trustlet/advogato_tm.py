#!/usr/bin/env python

import time
from pprint import pprint

if True:
	from pymmetry.profile import Profiles, Profile
	from pymmetry.certs import DictCertifications, CertInfo
	from pymmetry.net_flow import *
	from pymmetry.tm_calc import *
else:
	from pymmetry.all_in_one import *

class AdvogatoCertInfo(CertInfo):
	def __init__(self, levels = None, minlvl = None, maxlvl = None):
		levels = levels or ['Observer', 'Journeyer', 'Apprentice', 'Master']
		minlvl = minlvl or levels[0]
		maxlvl = maxlvl or levels[-1]
		self.info = {}
		self.info['like'] = {'levels': levels,
				     #'seeds': ['raph', 'federico'],
				     'min level': minlvl,
				     'default level': maxlvl,
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




		

def advogato_tm(G, a, b):
	p = Profiles(Profile, DictCertifications)

	# G.adv_profiles = p  # for testing

	t = time.time()
	print "Start creating profiles"
	p.add_profiles_from_graph(G)
	print "Finished creating profiles", time.time() - t

	levels = G.level_map.items()
	levels.sort(lambda a,b: cmp(a[1], b[1]))  # sort on trust value
	levels = map((lambda x: x[0]), levels)
	t = TrustMetric(AdvogatoCertInfo(levels), p)
	seeds = [a]
        r = t.tmetric_calc('like', seeds)

	# G.results = r  # for testing
	if b in r.keys():
		return G.level_map[r[b]]
	else:
		return None


class AdvogatoTM(TrustMetric):
	"""The advogato trust metric"""

	def __init__(self, G):
		self.G = G
		self.p = Profiles(Profile, DictCertifications)
		self.p.add_profiles_from_graph(G)

		levels = G.level_map.items()
		levels.sort(lambda a,b: cmp(a[1], b[1]))  # sort on trust value
		levels = map((lambda x: x[0]), levels)
		self.t = TrustMetric(AdvogatoCertInfo(levels), p)

	def calc(self, e):
		G = self.G
		t.delete_edge(e)  # needs to be implemented...
		r = self.t.tmetric_calc('like', [e[0]])
		t.add_edge(e)
		if b in r.keys():
			return self.G.level_map[r[b]]
		else:
			return None


		
	
if __name__ == "__main__":
	from Advogato import *
	G = Advogato()
	G.ditch_components(threshold = 7)
	print advogato_tm(G, "God", "rms")
