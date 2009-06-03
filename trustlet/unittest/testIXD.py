#!/usr/bin/env python
"""
test cache functions.
- save/load
- mmerge
"""

import unittest
import igraphXdigraphMatch as IXD
#import os
#import sys
#import random
#import time


class TestIXD(unittest.TestCase):
    def setUp(self):
        self.g = IXD.igraphDict()
        self.g['dan'] = 1
        self.g['dan']['john'] = 1
        

    def testAssign(self):
        self.assertEqual( self.g['dan']['john'] , 1 )

    def testDelete(self):
        
        self.assertEqual( self.g.g.vcount(), 2 )
        self.assertEqual( self.g.g.ecount(), 1 )

        del self.g['dan']['john']
        
        self.assertEqual( self.g.g.vcount(), 1 ) #here delete only the edge
        self.assertEqual( self.g.g.ecount(), 0 )

        del self.g['dan']
        
        self.assertEqual( self.g.g.vcount(), 0 ) #here delete all the nodes in 'dan' --> 'john'
        self.assertEqual( self.g.g.ecount(), 0 )

        self.g['dan'] = 1
        self.g['dan']['john'] = 1
        del self.g['dan']

        self.assertEqual( self.g.g.vcount(), 0 ) #here delete all the nodes in 'dan' --> 'john'
        self.assertEqual( self.g.g.ecount(), 0 )
        
    def testItems(self):
        
        self.assertEqual( self.g.items()[0][0] , 'dan' )
        self.assertEqual( len( self.g.items() ) , 1 )
        
    def testKey(self):
        
        self.assertEqual( self.g.keys() , ['dan'] )
        self.assertEqual( self.g['dan'].keys(), ['john'] )

    def testValue(self):
        
        self.assertEqual( self.g.values()[0].keys() , ['john'] )
        self.assertEqual( self.g.values()[0].values() , [1] )


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIXD)
    unittest.TextTestRunner(verbosity=2).run(suite)
