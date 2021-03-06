#!/usr/bin/env python
"""
test cache functions.
- save/load
- mmerge
"""

import unittest
import trustlet.igraphXdigraphMatch as IXD
import networkx as nx
import igraph
import os
#import sys
#import random
#import time


class TestIXD(unittest.TestCase):
	def setUp(self):
		self.g = IXD.XDiGraph()
		self.g.add_edge('dan','mas',{'level':'journeyer'})
		self.g.add_edge('mart','mas',{'level':'journeyer'})
		self.g.add_edge('luc','mas',{'level':'master'})
		self.g.add_edge('dan','luc',{'level':'apprentice'})

	def testDot(self):
		self.assertEqual( self.g.number_of_edges(), 4 )	
		self.assertEqual( self.g.number_of_edges(), 4 )	
		nx.write_dot( self.g, './test.dot' )
		g1 = nx.read_dot( './test.dot' )
		self.assertEqual( g1.number_of_edges(), self.g.number_of_edges() )
		self.assertEqual( g1.number_of_edges(), 4 )
        #os.remove( './test.dot' )
		#first method of loading
		#g2 = igraph.load( 'test~', format='pajek' )
		#g3 = IXD.XDiGraph()
		#self.g3.succ.g = g2
		
		#self.assertEqual( g3.number_of_edges(), self.g.number_of_edges() )
		#second method
		#g1 = nx.read_pajek( './test.net' )
		
		#self.assertEqual( self.g.number_of_edges(), g1.number_of_edges() )
		#self.assertEqual( g3.number_of_edges(), g1.number_of_edges() )
		

	def testValuesOnEdges(self):
		self.assertEqual( self.g.get_edge( 'dan','mas' ) , {'level':'journeyer'} )
		self.assertEqual( self.g.get_edge( 'luc','mas' ) , {'level':'master'} )
		self.assertEqual( self.g.get_edge( 'dan','luc' ) , {'level':'apprentice'} )
		try: #this edge cannot exist
			x = self.g.get_edge( 'luc', 'dan' )
			print ""
			print "unknown edge", ('luc','dan',x)
			self.assert_(False)
		except nx.NetworkXError:
				pass
		
	def testEdges(self):
			self.assertEqual( sorted( self.g.edges() ) , 
							  sorted( [('dan','mas',{'level':'journeyer'}),
									   ('mart','mas',{'level':'journeyer'}),
									   ('luc','mas',{'level':'master'}),
									   ('dan','luc',{'level':'apprentice'})]
									  )
							  )

	def testDelete(self):
			self.assertEqual( self.g.number_of_edges() , len( self.g.succ.g.es ) )
			self.assertEqual( self.g.number_of_edges() , 4 )
			self.assertEqual( self.g.number_of_nodes() , 4 )

			self.g.delete_edge('dan','mas')
			try:
				x=self.g.get_edge('dan','mas')
				self.assert_(False)
			except nx.NetworkXError:
				pass
			
			self.assertEqual( self.g.number_of_edges() , 3 )
			
			self.g.delete_node( 'luc' )

			self.assertEqual( self.g.number_of_edges() , 1 )
			self.assertEqual( self.g.number_of_nodes() , 3 )
			
		
	def testInOutEdges(self):
			self.assertEqual( 
					sorted( self.g.in_edges( 'mas' ) ) , 
					sorted(  
							[ ('dan','mas',{'level':'journeyer'}), ('mart','mas',{'level':'journeyer'}),('luc','mas',{'level':'master'}) ] 
							)
					
					)
		
			self.assertEqual( 
					sorted( self.g.out_edges( 'dan' ) ) , 
					sorted(  
							[ ('dan','mas',{'level':'journeyer'}), ('dan','luc',{'level':'apprentice'})] 
							)
					
					)
		


if __name__ == '__main__':
	suite = unittest.TestLoader().loadTestsFromTestCase(TestIXD)
	unittest.TextTestRunner(verbosity=2).run(suite)

