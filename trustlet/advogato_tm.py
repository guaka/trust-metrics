#!/usr/bin/env python

"""Wrapper thing around pymmetry."""

import time
from pprint import pprint

from pymmetry.profile import Profiles, Profile
from pymmetry.certs import DictCertifications, CertInfo
from pymmetry.net_flow import *
from pymmetry.tm_calc import *

from helpers import hms


class AdvogatoCertInfo(CertInfo):
    def __init__(self, levels = None, minlvl = None, maxlvl = None):
        levels = levels or ['Observer', 'Journeyer', 'Apprentice', 'Master']
        minlvl = minlvl or levels[0]
        #maxlvl should not be the maximum, otherwise we get that almost all the users are at the maximum level
        #maxlvl = maxlvl or levels[-1]
        #let's try with the min
        maxlvl = maxlvl or levels[0]
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



def advogato_tm(graph, src, dst):
    profiles = Profiles(Profile, DictCertifications)
    # graph.adv_profiles = p  # for testing
    
    start_time = time.time()
    print "Start creating profiles"
    profiles.add_profiles_from_graph(graph)
    print "Finished creating profiles", hms(time.time() - start_time)

    levels = graph.level_map.items()
    levels.sort(lambda a, b: cmp(a[1], b[1]))  # sort on trust value
    levels = map((lambda x: x[0]), levels)
    pymtrustmetric = PymTrustMetric(AdvogatoCertInfo(levels), profiles)
    seeds = [src]
    results = pymtrustmetric.tmetric_calc('like', seeds)
    
    if dst in results.keys():
        return graph.level_map[results[dst]]
    else:
        return None


if __name__ == "__main__":
    import Advogato, PredGraph
    import TrustMetric
    
    G = Advogato.Kaitiaki() #Advogato()
    pg = PredGraph.PredGraph(G, TrustMetric.AdvogatoGlobalTM, True)
    import scipy
    print scipy.mean(pg.pred_trust), scipy.std(pg.pred_trust)
