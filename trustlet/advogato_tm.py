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
	def __init__(self):
		self.info = {}
		self.info['like'] = {'levels': ['Observer', 'Journeyer', 'Apprentice','Master'],
								 #'seeds': ['raph', 'federico'],
				     'min level': 'Observer',
				     'default level': 'Observer',
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


class AdvogatoCertInfoNumbers(AdvogatoCertInfo):
	def __init__(self):
		self.info = {}
		self.info['like'] = {'levels': ['0.4', '0.6', '0.8','1.0'],
								 #'seeds': ['raph', 'federico'],
								 'min level': '0.4',
								 'default level': '0.4',
								 'type': 'to'
								}
		

def advogato():
	from trustlet.Advogato import Advogato
	adv_graph = Advogato("tiny")
	print advogato_tm(adv_graph, "gwm", "rms")

def advogato_tm(G, a, b):
	p = Profiles(Profile, DictCertifications)

	t = time.time()
	print "Start creating profiles"
	p.add_profiles_from_graph(G)
	print "Finished creating profiles", time.time() - t

	t = TrustMetric(AdvogatoCertInfoNumbers(), p)
	seeds = [a]
        r = t.tmetric_calc('like', seeds)

	#pprint(r)
	if b in r.keys():
		return float(r[b])
	else:
		return None

	
if __name__ == "__main__":
	advogato()

            
