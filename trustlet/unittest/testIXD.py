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
		self.gp = IXD.PredDict(self.g.g, self.g.vertexDict)

	def testAssign(self):
		self.assertEqual( self.g['dan']['john'] , 1 )
		self.assert_( 'dan' in self.g )
		self.assert_( 'mas' in self.g )
		self.assert_( 'john' in self.g['dan'] )
		self.assert_( 'john' not in self.g['mas'] )
		self.assert_( 'dan' in self.gp['john'] )
		#a predDict cannot modify the edges/nodes
		self.gp['john'] = 1
		self.gp['john']['dan'] = 2

		self.assert_( 'john' not in self.g['mas'] )
		self.assert_( 'john' in self.gp )
		
		self.assert_( 'dan' in self.gp )
		self.assert_( 'dan' in self.g )

		self.assert_( self.g['dan']['john'], 1 )
		self.assert_( self.gp['john']['dan'], 1 ) #viceversa
		
	def testReciprocity(self):
			self.g['john']['dan']=2
			
			self.assert_( 'john' in self.g )
			self.assert_( 'dan' in self.g )
			self.assert_( 'john' in self.gp )
			self.assert_( 'dan' in self.gp )


	def testDelete(self):
		
		self.assertEqual( self.g.g.vcount(), 3 )
		self.assertEqual( self.g.g.ecount(), 1 )
		
		del self.g['dan']['john']
		
		self.assertEqual( self.g.g.vcount(), 3 ) #here delete only the edge
		self.assertEqual( self.g.g.ecount(), 0 )
		
		self.g['dan']['jon']=1
		del self.g['dan']
		self.assertEqual( self.g.g.vcount(), 3 ) #here delete all the edges in 'dan' --> 'john'
		self.assertEqual( self.g.g.ecount(), 0 ) # and 'dan' (the vertexs is 3, because we add 'jon')

		self.g['dan'] = 1
		self.g['dan']['xxx'] = 1
		self.g['dan']['john'] = 1
		self.g['dan']['pollo'] = 1
		del self.g['dan']

		self.assertEqual( self.g.g.vcount(), 5 ) #here delete all the nodes in 'dan' --> 'john'
		self.assertEqual( self.g.g.ecount(), 0 ) #and dan
	
		
	def testItems(self):
		self.assertEqual( self.g.items()[0][0] , 'dan' )
		self.assertEqual( len( self.g.items() ) , 3 )
		self.assertEqual( self.g['dan'].items()[0][0] , 'john' )
		self.assertEqual( self.g['john'].items() , [] )
		
	def testKey(self):
		
		self.assertEqual( self.g.keys() , ['dan','john','mas'] )
		self.assertEqual( self.g['dan'].keys(), ['john'] )

	def testValue(self):
		
		self.assertEqual( self.g.values()[0].keys() , ['john'] )
		self.assertEqual( self.g.values()[0].values() , [1] )

	def testContain(self):
		self.g['dan']['max']=1
		self.g['mas']['max']=2
		self.g['dan']['xxx']=1
		self.gp['xxx']['dan']=2

		self.assertEqual( self.g['dan'].values() , [1,1,1] ) 
		self.assertEqual( self.g['dan'].keys(), ['john','max','xxx'] )
		
		#test containfrom
		self.assertEqual( self.gp['max'].values() , [1,2] )
		self.assertEqual( self.gp['max'].keys() , ['dan','mas'] )
		return None
	
	def testHas_key(self):
			self.assert_( self.g.has_key('dan') )
			self.assert_( self.g.has_key('mas') )
			self.assert_( self.gp.has_key('john') )
		#self contain
			
			g = self.g['dan']

			self.assert_( g.has_key('john') )

			gp = self.gp['john']
		
			self.assert_( gp.has_key( 'dan' ) )

	def testMultipleEdge(self):
		self.assert_( self.g.g.ecount(), 1 ) 

		self.g['dan']['mas']=1
		self.g['dan']['mas']=2
		self.g['dan']['mas']=3
		
		self.assert_( self.g.g.ecount(), 2 )
		self.assertEqual( self.g['dan']['mas'], 1 )


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestIXD)
	unittest.TextTestRunner(verbosity=2).run(suite)


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
	
