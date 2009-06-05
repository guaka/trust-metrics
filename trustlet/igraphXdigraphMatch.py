import igraph as ig
import networkx as nx
import pprint
#methods of networkx to override:

# add_edge
# add_node
# add_nodes_from
# init
# delete_edge ?
# delete_node

#methods of dict to implement:

# setitem
# __contains__
# getitem
# delitem (with del?)
# get() D.get(k[,d]) -> D[k] if k in D, else d.	 d defaults to None.
# iteritems
# every iter[.]*

def _getVertexFromName(g, k):
		return g.vs.select( lambda v: v.attributes().has_key('name') and v['name'] == k )


class XDiGraph(nx.XDiGraph):
		def __init__(self, data=None, name='', selfloops=False, multiedges=False):
				nx.XDiGraph.__init__(self, data=data, name=name, selfloops=selfloops, multiedges=multiedges)
				self.succ = SuccDict()
				self.pred = PredDict()


#utility Class in order to override XDiGraph
class IgraphDict(dict):
		"""
		this class provide a match from the xdigraph adj lists,
		and the igraph library.
		this is an abstract function, in order to use this
		functionality, you have to use his sub-classes. (SuccDict and PredDict)
		graph: use the igraph passed as storage system.
		"""
		def __init__(self, graph=None):
				if self.__class__.__name__ == 'IgraphDict':
						raise Exception( "This class cannot be istantiated! you must instantiate only the subclasses" )

				if graph and type(graph) is ig.Graph:
						self.g = graph
				else:
						self.g = ig.Graph(n=0,directed=True)
		
		def keys(self):
				return list(self.iterkeys())
		def values(self):
				return list(self.itervalues())

		def iterkeys(self, itercondition):
				for n in self.g.vs:
						if itercondition(n):
								yield n['name']

		def __iter__(self,itercondition):
				for k in self.iterkeys(itercondition):
						yield k
								
		def __contains__(self,k,containscondition):
				kidls = _getVertexFromName( self.g , k )
		#if exists		  and if is the start of some edges	 
				if len(kidls) > 0 and containscondition( kidls[0] ):
						return True
				else:
						return False


		def itervalues(self,itercondition,to=True):
				for node in self.g.vs:
						if itercondition(node): 
								if to:
										yield ConnectedTo(node,self.g)
								else:
										yield ConnectedFrom(node,self.g)
								
		def get(k, to=True, d=None ):
		#to means, i have to return the vertex connected to k, or viceversa 
				kidls = _getVertexFromName( self.g , k )
				try:
						if to:
								return ConnectedTo( self.g, k )
						else:
								return ConnectedFrom( self.g, k )
				except:
						return d

		def items(self):
				return list(self.iteritems())
		def iteritems(self,itercondition):
				for node in self.g.vs:
						if itercondition(node): 
								yield (node['name'],ConnectedTo(node,self.g))
		
		def __delitem__(self, k, delcond, to=True):
	#del the node k, and all his edges
				kidls = _getVertexFromName(self.g, k)
				if not len(kidls) and delcond(kidls[0]):
						raise KeyError("This key ("+str(k)+") is not in the dictionary")
				
				if to:
						nodesConnectedK = ConnectedTo( k, self.g )
				else:
						nodesConnectedK = ConnectedFrom( k, self.g )

				for n in nodesConnectedK.iterkeys_id():
						self.g.delete_vertices( n )
						
				self.g.delete_vertices( kidls[0].index ) #delete also all the edges that contains this vertex
				
				return None

		def __getitem__(self, k, to=True):
				if to:
						return ConnectedTo(k,self.g)
				else:
						return ConnectedFrom(k,self.g)

		def __setitem__(self,k,v, reverted=True):
		#v is not used!
				if reverted: #if reverted we cannot add nothing! only normal graph can add nodes
						return None

				kidls = _getVertexFromName(self.g, k)

		#check if node is already in graph
				if len(kidls) == 1:
						return None #set nothing
		
				self.g.add_vertices(1) #add a vertex
				ve = self.g.vs[self.g.vcount()-1] #the vertex just added
				ve['name'] = k #set name of the vertex
		#when the user use getitem to get this value,
		#i return a connectedTo class instantiated with 'k'
				return None

		def __str__(self):
				"""
				return only some of the data
				"""
				return pprint.pformat(self.g.__str__())

# -------------------------------------------------------------------------------------------------------------------------------
# SUBCLASSES!!!

class SuccDict(IgraphDict):
		def iterkeys(self):
				# if there is at least an edge that starts in node, then this node is in the first dictionary, so we had to include it
				# but for the nodes added without outedges? these nodes has indegree == 0..
				return IgraphDict.iterkeys(self, lambda n: self.g.outdegree( n.index ) > 0 or self.g.indegree( n.index ) == 0 )
		def __iter__(self):
				#the same as iterkeys
				return IgraphDict.__iter__(self, lambda n: self.g.outdegree( n.index ) > 0 or self.g.indegree( n.index ) == 0 )
		def __contains__(self,k):
				return IgraphDict.__contains__(self,k, lambda n: self.g.outdegree( n.index ) > 0 or self.g.indegree( n.index ) == 0   )
		def itervalues(self):
				# if there is at least an edge that starts in node, then this node is in the first dictionary, so we had to include it
				# but for the nodes added without outedges? these nodes has indegree == 0..
				return IgraphDict.itervalues(self, lambda node: self.g.outdegree( node.index ) > 0 or self.g.indegree( node.index ) == 0 , to=True )
		def get(self, k, d=None):
				return IgraphDict.get(k,d,to=True)
		def iteritems(self):
				return IgraphDict.iteritems(self, lambda node:self.g.outdegree( node.index ) > 0 or self.g.indegree( node.index ) == 0 )
		def __delitem__(self,k):
				return IgraphDict.__delitem__(self,k, lambda node:self.g.outdegree( node.index) > 0 or self.g.indegree( node.index ) == 0, to=True )
		def __getitem__(self,k):
				return IgraphDict.__getitem__(self, k, to=True)
		def __setitem__(self,k,v):
				return IgraphDict.__setitem__(self,k,v,reverted=False)

class PredDict(IgraphDict):
		def __init__(self, graph):
				if graph and type(graph) is ig.Graph:
						self.g = graph
				else:
						raise Exception("This class cannot be instantiated standalone!")

		def iterkeys(self):
				return IgraphDict.iterkeys(self, lambda n: self.g.indegree( n.index ) > 0 or self.g.outdegree( n.index ) == 0 )
		def __iter__(self):
				#the same as iterkeys
				return IgraphDict.__iter__(self, lambda n: self.g.indegree( n.index ) > 0 or self.g.outdegree( n.index ) == 0 )
		def __contains__(self,k):
				return IgraphDict.__contains__(self,k, lambda n: self.g.indegree( n.index ) > 0 or self.g.outdegree( n.index ) == 0  )
		def itervalues(self):
				# if there is at least an edge that starts in node, then this node is in the first dictionary, so we had to include it
				# but for the nodes added without outedges? these nodes has indegree == 0..
				return IgraphDict.itervalues(self, lambda node: self.g.indegree( node.index ) > 0 or self.g.outdegree( node.index ) == 0 , to=False )
		def get(self, k, d=None):
				return IgraphDict.get(k,d,to=False)
		def iteritems(self):
				return IgraphDict.iteritems(self, lambda node:self.g.indegree( node.index ) > 0 or self.g.outdegree( node.index ) == 0 )
		def __delitem__(self,k):
				return IgraphDict.__delitem__(self,k, lambda node:self.g.indegree( node.index) > 0 or self.g.outdegree( node.index ) == 0, to=False )
		def __getitem__(self,k):
				return IgraphDict.__getitem__(self, k, to=False)
		def __setitem__(self,k,v):
				#preddict cannot modify the igraph.Graph instance
				return IgraphDict.__setitem__(self,k,v,reverted=True)

# END
# ----------------------------------------------------------------------------------------------------------------------------------

#this class is a superclass for the ConnectedTo and ConnectedFrom classes
class Connected(dict):
		"""
		used to represent the in/outdegree of a node.
		"""
		def __init__(self, mynode, igraph):
		#check if the node exist, else raise an error
				self.g = igraph

				if type(mynode) is ig.Vertex:
						self.nodevertex = mynode
						self.nodename = mynode.attributes().has_key( 'name' ) and mynode['name']
						if not self.nodename:
								raise KeyError("This key ("+str(mynode)+") is not contained in this dictionary")
				else:
			#if mynode is a string
						self.nodename = mynode
						mynodeIDls = _getVertexFromName(igraph, mynode)

						if not len( mynodeIDls ):
								raise KeyError("This key ("+str(mynode)+") is not contained in this dictionary")

						self.nodevertex = mynodeIDls[0]
		
				return None

		def get(k, d=None ):
				try:
						return self.__getitem__(k)
				except KeyError:
						return d
		
		def __iter__(self):
				for k in self.iterkeys():
						yield k
						
		def keys(self):
				return list(self.iterkeys())
		
		def iterkeys(self,itercondition):
				for n in self.g.vs:
						if itercondition(n):
								yield n['name']
						
		def iterkeys_id(self,itercondition):
				for n in self.g.vs:
						if itercondition(n):
								yield n.index
												
		def keys_id(self):
				return list(self.iterkeys_id())

		def values(self):
				return list(self.itervalues())
		
		def itervalues(self,itercondition):
				for node in self.g.vs:
						if itercondition(node): 
								yield self.g.es[ self.g.get_eid( self.nodevertex.index, node.index ) ]['weight']

								
		def items(self):
				return list(self.iteritems())

		def iteritems(self,itercondition):
				for node in self.g.vs:
						if itercondition(node): 
								yield (node['name'], self.g.es[ self.g.get_eid( self.nodevertex.index, node.index ) ]['weight'] )
								
		def __delitem__(self, k, to=True):
				kidls = _getVertexFromName(self.g, k)
				if not len( kidls ):
						raise KeyError("This key ("+str(k)+") is not in dictionary")
		
				if to:
						self.g.delete_edges( self.g.get_eid( self.nodevertex.index, kidls[0].index ) )
				else:
						self.g.delete_edges( self.g.get_eid( kidls[0].index, self.nodevertex.index ) )
				
				self.g.delete_vertices( kidls[0].index )

				return None

		def __getitem__(self, k, to=True):
				kidls = _getVertexFromName(self.g, k)
				if not len( kidls ):
						raise KeyError("This key ("+str(k)+") is not in dictionary")
		
				if to: #the weight of edge me-k
						try:
								eid = self.g.get_eid( self.nodevertex.index, kidls[0].index )
						except ig.core.InternalError:
								raise KeyError("the edge from "+str(k)+" to "+str(self.nodename)+" is not in graph")
						
						return self.g.es[ eid ]['weight']
				else:  #the weight of edge k-me
						try:
								eid = self.g.get_eid( kidls[0].index,self.nodevertex.index )
						except ig.core.InternalError:
								raise KeyError("the edge from "+str(k)+" to "+str(self.nodename)+" is not in graph")
						
						return self.g.es[ eid ]['weight']

		def __setitem__(self,k,v,revert=False):
				if revert: #reverted graph cannot change the weights
						return None

				kidls = _getVertexFromName(self.g, k)
		#check if node is already in graph
				if not len( kidls ):
						self.g.add_vertices(1) #add a vertex
						ve = self.g.vs[self.g.vcount()-1] #the vertex just added
						ve['name'] = k #set name of the vertex
				else:
						ve = kidls[0] 
		
		#add an edge from the node of this instance to the node passed by setitem 
				self.g.add_edges( (self.nodevertex.index , ve.index)  )
				self.g.es[ self.g.get_eid( self.nodevertex.index , ve.index ) ]['weight'] = v #probably v == {'level':'Journeyer'}, or {'value':1} 
				
				return None

		def __contains__(self,k,condition):
				kidls = _getVertexFromName( self.g , k )
		#if exists		  and if is the end of some edges  
				if len(kidls) > 0 and condition( kidls[0] ):
						return True
				else:
						return False

		def __str__(self):
				"""
				return only some of the data
				"""
				return pprint.pformat(self.g.__str__())

class ConnectedTo(Connected):
		"""
		connected to: every nodes that are the end position of at least an edge that starts in self.nodename
		es. 
		   igraph edges:
		    ciccio -> pippo
		    ciccio -> pluto

			connectedTo( igraph, ciccio ) contains [pippo,pluto]
		"""
		def iterkeys(self):
				return Connected.iterkeys(self,lambda n:self.g.indegree( n.index ) > 0)
		def iterkeys_id(self):
				return Connected.iterkeys_id(self,lambda n:self.g.indegree( n.index ) > 0)
		def itervalues(self):
				return Connected.itervalues(self,lambda node:self.g.indegree( node.index ) > 0)
		def iteritems(self):
				return Connected.iteritems(self,lambda node:self.g.indegree( node.index ) > 0 )
		def __delitem__(self,k):
				return Connected.__delitem__(self,k,to=True)
		def __setitem__(self,k,v):
				return Connected.__setitem__(self,k,v,revert=False)
		def __getitem__(self,k):
				return Connected.__getitem__(self,k,to=True)
		def __contains__(self,k):
				return Connected.__contains__(self,k,lambda n:self.g.indegree( n.index ) > 0)
		
#connectedFrom
class ConnectedFrom(Connected):
		"""
		connected from: every nodes that are the start position of at least an edge that ends in self.nodename
		es. 
		   igraph edges:
		    pippo -> ciccio
		    pluto -> ciccio

			connectedTo( igraph, ciccio ) contains [pippo,pluto]
		"""
		def iterkeys(self):
				return Connected.iterkeys(self,lambda n:self.g.outdegree( n.index ) > 0)
		def iterkeys_id(self):
				return Connected.iterkeys_id(self,lambda n:self.g.outdegree( n.index ) > 0)
		def itervalues(self):
				return Connected.itervalues(self,lambda node:self.g.outdegree( node.index ) > 0)
		def iteritems(self):
				return Connected.iteritems(self,lambda node:self.g.outdegree( node.index ) > 0 )
		def __delitem__(self,k):
				return Connected.__delitem__(self,k,to=False)
		def __setitem__(self,k,v):
				return Connected.__setitem__(self,k,v,revert=True)
		def __getitem__(self,k):
				return Connected.__getitem__(self,k,to=False)
		def __contains__(self,k):
				return Connected.__contains__(self,k,lambda n:self.g.outdegree( n.index ) > 0)
				
