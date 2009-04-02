#!/usr/bin/env python
"""
test all trustlet
"""

import unittest
import os

import trustlet


class TestAdvogato(unittest.TestCase):
    def setUp(self):
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
            
    def testDotEqualC2(self):
        
        for netname in self.setInstances:
            print "Testing", netname
            c2 = self.setInstances[netname]['c2']
            dot = self.setInstances[netname]['dot']
            #test equal
            self.assertEqual( c2.number_of_edges(), dot.number_of_edges() )
            self.assertEqual( c2.number_of_nodes(), dot.number_of_nodes() )
            self.assertEqual( c2.number_of_connected_components(), dot.number_of_connected_components() )
            self.assertEqual( c2.avg_degree(), dot.avg_degree() )
            
            

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdvogato)
    unittest.TextTestRunner(verbosity=2).run(suite)

