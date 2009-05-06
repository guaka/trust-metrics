#!/usr/bin/env python
"""
test all trustlet
"""

import unittest
import os
import sys

import trustlet

class TestWiki(unittest.TestCase):
    
    def setUp(self):
        sys.setrecursionlimit(1000)
        self.basepath = basepath = os.path.join(os.environ['HOME'],"shared_datasets" )
        self.setInstances = {} #set of {networkname:{dot:networkinstance,c2:networkinstance} }

        for netname in os.listdir( os.path.join(self.basepath,"WikiNetwork")):
            found = False
            data = None

            #find an avaiable network
            for tmpdata in os.listdir( os.path.join(self.basepath,"WikiNetwork",netname) ):
                tmpath = os.path.join( basepath , "WikiNetwork",netname , tmpdata  )
                #skip non present network
                if not os.path.exists( tmpath ):
                    continue
                
                if os.path.exists( os.path.join( tmpath, "graphHistory.c2" ) ):
                    data = tmpdata
                    found = True
                    break

            if not found:
                continue # if for a network I don't found any network, skip it

            self.setInstances[netname+'_'+tmpdata] = trustlet.Dataset.Network.WikiNetwork( lang=netname, date=tmpdata, silent=True )
            
    def testWeights(self):
        print ""
        
        for netname in self.setInstances:
            print "Testing", netname
            net = self.setInstances[netname]
            
            self.assertEqual( len( net.weights_list() ), net.number_of_edges() )
            
    def testPredGraph(self):
        print ""

        for netname in self.setInstances:
            print "Testing", netname
            net = self.setInstances[netname]
            net.silent = True #do not print whatever you do
            t = trustlet.TrustMetric( net, trustlet.ebay_tm )
            p = trustlet.WikiPredGraph( t )
            #test graphcontroversiality
            lt = p.graphcontroversiality()
            
            self.assert_( not any( [el != None and not type(el) is tuple for el in lt] ) )

            lt = p.graphcontroversiality(indegree=1)
            
            self.assert_( not any( [el != None and not type(el) is tuple for el in lt] ) )

            lt = p.graphcontroversiality(cond=trustlet.onlyMaster)
            
            self.assert_( not any( [el != None and not type(el) is tuple for el in lt] ) )
            
            lt = p.graphcontroversiality(toe='mae')
            
            self.assert_( not any( [el != None and not type(el) is tuple for el in lt] ) )
            
    def testLevelMap(self):
        print ""
        for netname in self.setInstances:
            print "Testing", netname
            net = self.setInstances[netname]
            self.assert_( net.level_map )
    
    def testMap(self):
        print ""
        
        for netname in self.setInstances:
            print "Testing", netname
            net = self.setInstances[netname]
            for i in xrange(100):
                self.assert_( (net.map(i) <= 1.0) and (net.map(i) >= 0.0) )
    
    def testBotsBlockedUsers(self):
        print ""

        for netname in self.setInstances:
            print "Testing", netname
            net = self.setInstances[netname]
            
            self.assert_( not ( bool(net.botset) ^ (not net.bots) ) and not ( bool(net.blockedset) ^ (not net.blockedusers) ) ) 
                


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWiki)
    unittest.TextTestRunner(verbosity=2).run(suite)

