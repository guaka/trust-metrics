#!/usr/bin/env python

from pprint import pprint
from pymmetry.profile import Profiles, Profile
from pymmetry.certs import DictCertifications
from pymmetry.net_flow import *
from pymmetry.tm_calc import *

from pymmetry.certs import CertInfo

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


class AdvogatoCertInfoNumbers(CertInfo):
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

	p = Profiles(Profile, DictCertifications)

	for n in adv_graph:
		p.add_profile(n)
		for e in adv_graph.edges(n):
			p.add_cert(e[0], 'like', e[1], e[2]['level'])
	print "Finished creating profiles"

	t = TrustMetric(AdvogatoCertInfo(), p)
	#r = t.tmetric_calc('like', ['raph', 'federico'])
	seeds = ['raph'] #, 'federico', 'alan', 'miguel']
        r = t.tmetric_calc('like', seeds)
	# the alternative way is to just run the trust metric and set the seeds in AdvogatoCertInfo, self.info['seeds']: ['raph', 'federico']

	pprint(r)


def test(): 
	# demonstration showing that numbers can certify and
	# be certified, not just strings.
	
	p = Profiles(Profile, DictCertifications)
	
	p.add_profile('luke')
	p.add_profile('heather')
	p.add_profile('raph')
	p.add_profile('federico')
	p.add_profile('bob')
	p.add_profile('mary')
	p.add_profile('lesser fleas')
	p.add_profile('little fleas')
	p.add_profile('fleas')
	p.add_profile('robbie the old crock pony')
	p.add_profile('tart, the flat-faced persian cat')
	p.add_profile('mo the mad orange pony')
	p.add_profile('fleas ad infinitum')
	
	p.add_cert('raph', 'like', 'heather', 'Master')
	p.add_cert('raph', 'like', 'mary', 'Apprentice')
	p.add_cert('raph', 'like', 'federico', 'Master')
	p.add_cert('raph', 'like', 'bob', 'Observer')
	
	p.add_cert('federico', 'like', 'raph', 'Master')
	p.add_cert('federico', 'like', 'bob', 'Observer')
	
	p.add_cert('luke', 'like', 'heather', 'Journeyer')
	
	p.add_cert('heather', 'like', 'luke', 'Journeyer')
	p.add_cert('heather', 'like', 'robbie the old crock pony', 'Journeyer')
	p.add_cert('heather', 'like', 'tart, the flat-faced persian cat', 'Journeyer')
	p.add_cert('heather', 'like', 'mo the mad orange pony', 'Journeyer' )
	
	p.add_cert('bob', 'like', 'mary', 'Apprentice')
	p.add_cert('bob', 'like', 'heather', 'Apprentice')
	
	p.add_cert('mary', 'like', 'bob', 'Apprentice')
	
	p.add_cert('lesser fleas', 'like', 'fleas ad infinitum', 'Apprentice')
	p.add_cert('little fleas', 'like', 'lesser fleas', 'Apprentice')
	p.add_cert('fleas', 'like', 'little fleas', 'Apprentice')
	p.add_cert('robbie the old crock pony', 'like', 'fleas', 'Journeyer')
	
	#		p.add_cert('heather', 'hate', 'bob', 'dislike' )
	#		p.add_cert('heather', 'hate', 'fleas', 'looks CAN kill' )
	#		p.add_cert('fleas', 'hate', 'mary', 'dislike')
	
	
	t = TrustMetric(AdvogatoCertInfo(), p)
	r = t.tmetric_calc('like', ['raph', 'federico'])
        #r = t.tmetric_calc('like') # the alternative way is to just run the trust metric and set the seeds in AdvogatoCertInfo, self.info['seeds']: ['raph', 'federico']

	pprint(r)
	
	#		r = t.tmetric_calc('hate')
	#		pprint(r)
	
	
if __name__ == "__main__":
	advogato()
	#test()

            
