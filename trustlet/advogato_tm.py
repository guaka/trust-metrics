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
	"""The advogato trust metric."""

	def __init__(self, G):
		self.G = G
		self.p = Profiles(Profile, DictCertifications)
		self.p.add_profiles_from_graph(G)

		self.levels = G.level_map.items()
		self.levels.sort(lambda a,b: cmp(a[1], b[1]))  # sort on trust value
		self.levels = map((lambda x: x[0]), self.levels)
		self.t = TrustMetric(AdvogatoCertInfo(self.levels), self.p)

	def leave_one_out(self, e):
		a, b, level = e
		level = level.values()[0]
		self.p.del_cert(a, 'like', b, level)
		r = self.t.tmetric_calc('like', [e[0]])
		self.p.add_cert(a, 'like', b, level)
		
		if b in r.keys():
			return self.G.level_map[r[b]]
		else:
			return None


class AdvogatoGlobalTM(TrustMetric):
	"""The advogato trust metric, global, seeds: the 4 masters of advogato."""

	def __init__(self, G):
	    self.G = G
	    self.p = Profiles(Profile, DictCertifications)
	    self.p.add_profiles_from_graph(G)
	
	    levels = G.level_map.items()
	    levels.sort(lambda a,b: cmp(a[1], b[1]))  # sort on trust value
	    levels = map((lambda x: x[0]), levels)
	    self.t = TrustMetric(AdvogatoCertInfo(levels), self.p)
	    for s in self.G.advogato_seeds:
	        assert s in G
	    self.pred_trust = self.t.tmetric_calc('like', self.G.advogato_seeds)
	    
	    self.pred_trust_keys = self.pred_trust.keys()

	def leave_one_out(self, e):
	    a, b, level = e
	    # level = level['level']
	    if b in self.pred_trust_keys:
	        return self.G.level_map[self.pred_trust[b]]
	    else:
	        return None


if __name__ == "__main__":
    import Advogato, PredGraph
    
    G = Advogato.Advogato()
    pg = PredGraph.PredGraph(G, AdvogatoGlobalTM, True)
    import scipy
    print scipy.mean(pg.pred_trust), scipy.std(pg.pred_trust)
