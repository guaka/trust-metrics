#!/usr/bin/env python
"""
test all trustlet
"""

import unittest
import os

import trustlet


class TestAdvogato(unittest.TestCase):
    def __init__(self,methodName='RunTest'):
        unittest.TestCase.__init__(self,methodName=methodName)
        #my code of init
        self.basepath = basepath = os.path.join(os.environ['HOME'],"datasets" )
        self.setInstances = {} #set of {networkname:{dot:networkinstance,c2:networkinstance} }

        #list of network to test
        networks = [trustlet.AdvogatoNetwork, trustlet.KaitiakiNetwork, trustlet.SqueakfoundationNetwork, trustlet.Robots_netNetwork]

        for net in networks:
            netname = net.__name__
            found = False
            data = None

            #find an avaiable network
            for tmpdata in os.listdir( os.path.join( basepath , net.__name__) ):
                tmpath = os.path.join( basepath , net.__name__ , tmpdata  )
                
                if os.path.exists( os.path.join( tmpath, "graph.dot" ) ):
                    data = tmpdata
                    found = True
                    break

            if not found:
                continue # if for a network I don't found any network, skip it

            self.setInstances[netname] = {}
            self.setInstances[netname]['c2'] =  net( date=data )
            self.setInstances[netname]['dot'] = net( date=data, from_dot=True ) 
        
        
    def testReciprocity(self):
        print "" #skip a line
        
        for netname in self.setInstances:
            print "Testing", netname
            
            net = self.setInstances[netname]['dot']
            val = net.reciprocity_matrix(force=True)

            self.assert_( type(val) is dict ) #must be a dict
            for level in val:
                level_tot = sum([val[level][key] for key in val[level]]) #this must be 1 or 0 
                self.assert_( level_tot == 1.0 or level_tot == 0.0 ) #check that the sum of value in dictionary is 1 or 0

    def testDotEqualC2(self):
        print ""
        
        for netname in self.setInstances:
            print "Testing", netname
            c2 = self.setInstances[netname]['c2']
            dot = self.setInstances[netname]['dot']
            #test equal
            self.assertEqual( c2.number_of_edges(), dot.number_of_edges() )
            self.assertEqual( c2.number_of_nodes(), dot.number_of_nodes() )
            self.assertEqual( c2.number_of_connected_components(), dot.number_of_connected_components() )
            self.assertEqual( c2.avg_degree(), dot.avg_degree() )
            
    def testWeights(self):
        print ""
        
        for netname in self.setInstances:
            print "Testing", netname
            net = self.setInstances[netname]['dot']
            
            self.assertEqual( len( net.weights_list() ), net.number_of_edges() )
            
    def testPajek(self):
        print ""

        for netname in self.setInstances:
            print "Testing", netname
            net = self.setInstances[netname]['dot']
            
            net.save_pajek()
            w = trustlet.WeightedNetwork(filepath = net.filepath)
            w.load_pajek()
            
            self.assertEqual( w.number_of_nodes(), net.number_of_nodes() )
            self.assertEqual( w.number_of_edges(), net.number_of_edges() )
            self.assert_( sorted( w.edges() ) == sorted( net.edges() ) )
            self.assert_( sorted( w.nodes() ) == sorted( net.nodes() ) )
            

    def testPredGraph(self):
        print ""

        for netname in self.setInstances:
            print "Testing", netname
            net = self.setInstances[netname]['dot']
            net.silent = True #do not print whatever you do
            t = trustlet.TrustMetric( net, trustlet.ebay_tm )
            p = trustlet.PredGraph( t )
            #test graphcontroversiality
            lt = p.graphcontroversiality()
            
            self.assert_( any( [el == None or type(el) is tuple for el in lt] ) )

            lt = p.graphcontroversiality(indegree=1)
            
            self.assert_( any( [el == None or type(el) is tuple for el in lt] ) )

            lt = p.graphcontroversiality(cond=trustlet.onlyMaster)
            
            self.assert_( any( [el == None or type(el) is tuple for el in lt] ) )

            


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdvogato)
    unittest.TextTestRunner(verbosity=2).run(suite)

