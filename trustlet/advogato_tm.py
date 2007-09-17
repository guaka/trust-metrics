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

	t = time.time()
	print "Start creating profiles"
	p.add_profiles_from_graph(G)
	print "Finished creating profiles", time.time() - t

	levels = G.level_map.items()
	levels.sort(lambda a,b: cmp(a[1], b[1]))
	levels = map((lambda x: x[0]), levels)
	print levels, p
	t = TrustMetric(AdvogatoCertInfo(levels), p)
	seeds = [a]
        r = t.tmetric_calc('like', seeds)

	#pprint(r)
	if b in r.keys():
		return float(r[b])
	else:
		return None

	
if __name__ == "__main__":
	from Advogato import *
	G = Advogato()
	G.ditch_components(threshold = 7)
	print advogato_tm(G, "God", "rms")
