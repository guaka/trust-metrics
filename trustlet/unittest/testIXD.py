#!/usr/bin/env python
"""
test cache functions.
- save/load
- mmerge
"""

import unittest
import trustlet.igraphXdigraphMatch as IXD
#import os
#import sys
#import random
#import time


class TestIXD(unittest.TestCase):
	def setUp(self):
		self.g = IXD.SuccDict()
		self.g['dan'] = 1
		self.g['dan']['john'] = 1
		self.g['mas'] = 1
		self.gp = IXD.PredDict(self.g.g)

	def testAssign(self):
		self.assertEqual( self.g['dan']['john'] , 1 )
		self.assert_( 'dan' in self.g )
		self.assert_( 'mas' in self.g )
		self.assert_( 'john' in self.g['dan'] )
		self.assert_( 'john' not in self.g )
		#a predDict cannot modify the edges/nodes
		self.gp['john'] = 1
		self.gp['dan']['john'] = 2
		self.assert_( 'john' not in self.g )
		self.assert_( self.g['dan']['john'], 1 )
		self.assert_( 'john' in self.gp )
		self.assert_( self.gp['john']['dan'], 1 )


	def testDelete(self):
		
		self.assertEqual( self.g.g.vcount(), 3 )
		self.assertEqual( self.g.g.ecount(), 1 )
		
		del self.g['dan']['john']
		
		self.assertEqual( self.g.g.vcount(), 3 ) #here delete only the edge
		self.assertEqual( self.g.g.ecount(), 0 )
		
		self.g['dan']['jon']=1
		del self.g['dan']
		self.assertEqual( self.g.g.vcount(), 3 ) #here delete all the edges in 'dan' --> 'john'
		self.assertEqual( self.g.g.ecount(), 0 ) # and 'dan'

		self.g['dan'] = 1
		self.g['dan']['xxx'] = 1
		self.g['dan']['john'] = 1
		self.g['dan']['pollo'] = 1
		del self.g['dan']

		self.assertEqual( self.g.g.vcount(), 5 ) #here delete all the nodes in 'dan' --> 'john'
		self.assertEqual( self.g.g.ecount(), 0 ) #and dan
	"""	
	def testDeletePrec(self):
		#test gp
		
		del self.g['john']
		self.assertEqual( self.gp.g.vcount(), 2 )
		self.assertEqual( self.gp.g.ecount(), 0 )
		
		self.p['dan']['john'] = 1
		self.p['pollo']['john'] = 2
		self.p['xxx']['john'] = 3
		self.p['pold']['john'] = 4
		self.p['fff']['john'] = 'xxxx'
		
		self.assertEqual( self.gp.g.vcount(), 7 )
		self.assertEqual( self.gp.g.ecount(), 5 )
		
		del self.gp['john']
		self.assertEqual( self.gp.g.vcount(), 6 )
		self.assertEqual( self.gp.g.ecount(), 0 )
		"""
	def testItems(self):
		self.assertEqual( self.g.items()[0][0] , 'dan' )
		self.assertEqual( len( self.g.items() ) , 2 )
		self.assertEqual( self.g['dan'].items()[0][0] , 'john' )
		
	def testKey(self):
		
		self.assertEqual( self.g.keys() , ['dan','mas'] )
		self.assertEqual( self.g['dan'].keys(), ['john'] )

	def testValue(self):
		
		self.assertEqual( self.g.values()[0].keys() , ['john'] )
		self.assertEqual( self.g.values()[0].values() , [1] )

	def testContainTo(self):
		self.g['dan']['max']=1
		self.g['dan']['xxx']=1
		self.gp['dan']['fff']=1

		self.assertEqual( self.g['dan'].values() , [1,1,1] ) 
		self.assertEqual( self.g['dan'].keys(), ['john','max','xxx'] )


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestIXD)
	unittest.TextTestRunner(verbosity=2).run(suite)
