"""
This module contains some class that subclass 'dict' type.
The goal is to have a dictionary similar to the adiacency dictionary (ad predecessor dictionary)
in networkx, but instead of add data to a dictionary we add data to
an igraph instance, in order to save ram and improve performance,
but maintaining all XDiGraph powerful functions.
"""

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

#TODO
# solve the igraph bug --> solve "my" bug
# this bug imply that if i invoke __contains__ method (on an item k) on a ConnectedTo class,
# this method get back every edges that is connected (to or from) k, instead only the edges connected to k.

def _getVertexFromName(g, k):
	return g.vs.select( lambda v: v.attributes().has_key('name') and v['name'] == k )


#utility class in order to override XDiGraph do not call them directly!
class IgraphDict(dict):
	"""
	this class provide a match from the xdigraph adj/pred lists,
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

	def __len__(self):
			return len(self.keys())

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

	def has_key(self, k ):
		"""D.has_key(k) -> True if D has a key k, else False"""
		return self.__contains__(k)

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
			return self.__getitem__(k)
		except:
			return d

	def items(self):
		return list(self.iteritems())

	def iteritems(self,itercondition):
		for node in self.g.vs:
			if itercondition(node): 
				yield (node['name'],ConnectedTo(node,self.g))

	def __delitem__(self, k, delcond, to=True):
		if not to: #only succdict can delete and set
			return None

		#del the node k, and all his edges
		kidls = _getVertexFromName(self.g, k)
		if not len(kidls) and delcond(kidls[0]):
			raise KeyError("This key ("+str(k)+") is not in the dictionary")

		#connectedTo = self.g.es.select( lambda e: e.source == kidls[0].index )

		#for n in connectedTo:
		#	 print "deleting", n.tuple, "(",self.g.vs[n.source]['name'],self.g.vs[n.target]['name'] ,")"
		#	 self.g.delete_edges( n.tuple )

		try:
			self.g.delete_vertices( kidls[0].index ) #delete also all the edges that contains this vertex
		except ig.core.InternalError:
			raise KeyError( "this node "+str(k)+" with id "+str(kidls[0].index)+" is not in the dictionary" )

		return None

	def __getitem__(self, k, cond, to=True):
		nk = _getVertexFromName(self.g, k )
		if not len(nk):
			raise KeyError( "This key ("+str(k)+") is not in the graph" )

		n = nk[0]

		#if to and cond(n):
		#	return ConnectedTo( n , self.g )
		#elif to:
		#	raise KeyError( "This key ("+str(k)+") is not in this dictionary" )
		#elif not to and cond(n):
		#	return ConnectedFrom( n , self.g )	
		#elif not to:
		#	raise KeyError( "This key ("+str(k)+") is not in this dictionary" )	
		if to:
			return ConnectedTo( n, self.g )
		else:
			return ConnectedFrom( n, self.g )	
		#else:
		#	raise KeyError( "Error on this key ("+str(k)+")" )

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
	"""
	this class represent an adj dictionary (or a succ dictionary) in XDiGraph.
	His goal is to get/set/delete with the same methods of a dictionary the nodes and edges,
	in his igraph istance.
	Particularity:
	  look at this example:
	  id = SuccDict()
	  id['dan']=1
	  id['dan']['john']=1
	  
	  id['john'] #does not raise a keyerror, because john is a node in the network
	             #the __getitem__ method of SuccDict return a ConnectedTo class (see the documentation of ConnectedTo)

	  in conclusion, 
	  id.keys() return all the nodes in the graph
	  id.items() return a list with foreach node: (node,connectedTo(node))
	  id.values() return a list with foreach node: connectedTo(node)
	"""
	def iterkeys(self):
		return IgraphDict.iterkeys(self, lambda n: True )
	def __iter__(self):
					#the same as iterkeys
		return IgraphDict.__iter__(self, lambda n: True )
	def __contains__(self,k):
		#return IgraphDict.__contains__(self,k, lambda n: self.g.outdegree( n.index ) > 0 or self.g.indegree( n.index ) == 0	  )
		return IgraphDict.__contains__(self,k, lambda n: True )	
	def itervalues(self):
		return IgraphDict.itervalues(self, lambda node:True , to=True )
	def get(self, k, d=None):
		return IgraphDict.get(k,d,to=True)
	def iteritems(self):
		return IgraphDict.iteritems(self, lambda node:True )
	def __delitem__(self,k):
		return IgraphDict.__delitem__(self,k, lambda node:True, to=True )
	def __getitem__(self,k):
		return IgraphDict.__getitem__(self, k, lambda node:True, to=True)
	def __setitem__(self,k,v):
		return IgraphDict.__setitem__(self,k,v,reverted=False)

class PredDict(IgraphDict):
	"""
	this class represent a pred dictionary in XDiGraph.
	His goal is to get with the same methods of a dictionary the nodes and edges,
	in his igraph istance.
	Particularity:
	  look at this example:
      id = SuccDict()
	  idp = PredDict(id.g) #id.g is an igraph instance
	  id['dan']=1 #PredDict can't set/delete edges/nodes
	  id['dan']['john']=1
	  
	  idp['dan'] #does not raise a keyerror, because john is a node in the network
	             #the __getitem__ method of PredDict return a ConnectedFrom class (see the documentation of ConnectedFrom)

	  in conclusion, 
	  idp.keys() return all the nodes in the graph
	  idp.items() return a list with foreach node: (node,connectedFrom(node))
	  idp.values() return a list with foreach node: connectedFrom(node)
	"""
		
	def __init__(self, graph):
		if type(graph) is ig.Graph:
			self.g = graph
		else:
			raise Exception("This class cannot be instantiated standalone!")

	def iterkeys(self):
		return IgraphDict.iterkeys(self, lambda n: True )
	def __iter__(self):
					#the same as iterkeys
		return IgraphDict.__iter__(self, lambda n: True )
	def __contains__(self,k):
		#return IgraphDict.__contains__(self,k, lambda n: self.g.indegree( n.index ) > 0 or self.g.outdegree( n.index ) == 0	 )
		return IgraphDict.__contains__(self,k, lambda n: True )	
	def itervalues(self):
		# if there is at least an edge that starts in node, then this node is in the first dictionary, so we had to include it
		# but for the nodes added without outedges? these nodes has indegree == 0..
		return IgraphDict.itervalues(self, lambda node: True , to=False )
	def get(self, k, d=None):
		return IgraphDict.get(k,d,to=False)
	def iteritems(self):
		return IgraphDict.iteritems(self, lambda n : True )
	def __delitem__(self,k):
		return IgraphDict.__delitem__(self,k, lambda node:True, to=False )
	def __getitem__(self,k):
		return IgraphDict.__getitem__(self, k, lambda node:True, to=False)
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

	def __len__(self):
			return len(self.keys())

	def get(k, d=None ):
		try:
			return self.__getitem__(k)
		except KeyError:
			return d

	def has_key(self, k):
		"""D.has_key(k) -> True if D has a key k, else False"""
		return self.__contains__(k)

	def __iter__(self):
		for k in self.iterkeys():
			yield k
						
	def keys(self):
		return list(self.iterkeys())
		
	def iterkeys(self,iterator): 
		for n in iterator():
			yield n['name']
						
	def iterkeys_id(self,iterator):
		for n in iterator():
			yield n.index
												
	def keys_id(self):
		return list(self.iterkeys_id())

	def values(self):
		return list(self.itervalues())
		
	def itervalues(self,iterator):
		for node,eid in iterator():
			yield self.g.es[ eid ]['weight']
			
	def items(self):
		return list(self.iteritems())

	def iteritems(self,iterator):	    
		for node,eid in iterator(): 
			yield (node['name'], self.g.es[ eid ]['weight'] )
				
	def __delitem__(self, k, to):
		kidls = _getVertexFromName(self.g, k)
		if not len( kidls ):
			raise KeyError("This key ("+str(k)+") is not in dictionary")
		
		if to:
			self.g.delete_edges( self.g.get_eid( self.nodevertex.index, kidls[0].index, directed=True ) )
		else:
			self.g.delete_edges( self.g.get_eid( kidls[0].index, self.nodevertex.index, directed=True ) )
		
		return None

	def __getitem__(self, k, to=True):
		kidls = _getVertexFromName(self.g, k)
		if not len( kidls ):
			raise KeyError("This key ("+str(k)+") is not in dictionary")
		
		if to: #the weight of edge me-k
			try:
				eid = self.g.get_eid( self.nodevertex.index, kidls[0].index, directed=True )
			except ig.core.InternalError:
				raise KeyError("the edge from "+str(self.nodename)+" to "+str(k)+" is not in graph")
						
			return self.g.es[ eid ]['weight']
		else:  #the weight of edge k-me
			try:
				eid = self.g.get_eid( kidls[0].index,self.nodevertex.index, directed=True )
			except ig.core.InternalError:
				raise KeyError("the edge from "+str(k)+" to "+str(self.nodename)+" is not in graph")
			
			return self.g.es[ eid ]['weight']

	def __setitem__(self,k,v,revert):
		"""
		set an edge
		"""
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
		self.g.es[ self.g.get_eid( self.nodevertex.index , ve.index, directed=True ) ]['weight'] = v #probably v == {'level':'Journeyer'}, or {'value':1} 
				
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



def _iterconditionTo(graph,nodeStart,condition=False,noEid=False):
	"""
	HELPER FUNCTION DOES NOT USE IT DIRECTLY
	this function takes a igraph, and an igraph.Vertex (nodeStart), 
	and return an function iterator 
	that yield  (igraph.Vertex (nodeEnd) that is connected to nodeStart , the edge id from nodeStart to nodeEnd )
	optional parameters:
	  condition: if set to true instead of the iterator is returned a function that return True if there is an edge
	             between nodeStart and nodeEnd, False otherwise.
	  noEid: the iterator yield only the nodeEnd and not the edge id
	"""
	#there is a way to avoid to invoke two times get_eid??
	def cond(n):
		try:
			x = graph.get_eid( nodeStart.index, n.index, directed=True )
			#print "da", node.attributes()['name'], n.attributes()['name'], "yes"
			return True
		except ig.core.InternalError:
			return False
	
	def iterator():
		for nodeEnd in graph.vs.select( cond ):
			if noEid:
				yield nodeEnd
			else:
				yield (nodeEnd,graph.get_eid( nodeStart.index, nodeEnd.index, directed=True ))	
	
	if condition:
		return cond
	else:
		return iterator

class ConnectedTo(Connected):
	"""
	This class take at init-time an igraph instance (given by SuccDict/PredDict [only SuccDict can instantiate an igraph instance])
	and a string with a node name, or a igraph.Vertex instance, and is able to represent all the out-edges
	of the node passed.

	connected to: every nodes that are the end position of at least an edge that starts in self.nodename
	es. 
	  igraph edges:
	  ciccio -> pippo
	  ciccio -> pluto
	
	  connectedTo( igraph, ciccio ) contains [pippo,pluto]
	"""
	def iterkeys(self):
		return Connected.iterkeys(self,_iterconditionTo(self.g,self.nodevertex,noEid=True) )
	def iterkeys_id(self):
		return Connected.iterkeys_id(self,_iterconditionTo(self.g,self.nodevertex,noEid=True))
	def itervalues(self):
		return Connected.itervalues(self,_iterconditionTo(self.g,self.nodevertex))
	def iteritems(self):
		return Connected.iteritems(self,_iterconditionTo(self.g,self.nodevertex))
	def __delitem__(self,k):
		return Connected.__delitem__(self,k,to=True)
	def __setitem__(self,k,v):
		return Connected.__setitem__(self,k,v,False)
	def __getitem__(self,k):
		return Connected.__getitem__(self,k,to=True)
	def __contains__(self,k):
		return Connected.__contains__(self,k,_iterconditionTo(self.g,self.nodevertex,condition=True))
	

def _iterconditionFrom(graph,nodeEnd,condition=False,noEid=False):
	"""
	HELPER FUNCTION DOES NOT USE IT DIRECTLY
	this function takes a igraph, and an igraph.Vertex (nodeEnd), 
	and return an function iterator 
	that yield  (igraph.Vertex (nodeStart) that is connected from nodeEnd , the edge id from nodeStart to nodeEnd )
	optional parameters:
	  condition: if set to true instead of the iterator is returned a function that return True if there is an edge
	             between nodeStart and nodeEnd, False otherwise.
	  noEid: the iterator yield only the nodeEnd and not the edge id
	"""
	#there is a way to avoid to invoke two times get_eid??
	def cond(n):
		try:
			x = graph.get_eid( n.index, nodeEnd.index, directed=True )
			#print "da", node.attributes()['name'], n.attributes()['name'], "yes"
			return True
		except ig.core.InternalError:
			return False
	
	def iterator():
		for nodeStart in graph.vs.select( cond ):
			if noEid:
				yield nodeStart
			else:
				yield (nodeStart,graph.get_eid( nodeStart.index, nodeEnd.index, directed=True ))	
	
	if condition:
		return cond
	else:
		return iterator

#connectedFrom
class ConnectedFrom(Connected):
	"""
	This class take at init-time an igraph instance (given by SuccDict/PredDict [only SuccDict can instantiate an igraph instance])
	and a string with a node name, or a igraph.Vertex instance, and is able to represent all the in-edges
	of the node passed.

	connected from: every nodes that are the start position of at least an edge that ends in self.nodename
	es. 
	  igraph edges:
	  pippo -> ciccio
	  pluto -> ciccio
	  
	  connectedTo( igraph, ciccio ) contains [pippo,pluto]
	"""
	def iterkeys(self):
		return Connected.iterkeys(self,_iterconditionFrom(self.g,self.nodevertex,noEid=True))
	def iterkeys_id(self):
		return Connected.iterkeys_id(self,_iterconditionFrom(self.g,self.nodevertex,noEid=True))
	def itervalues(self):
		return Connected.itervalues(self,_iterconditionFrom(self.g,self.nodevertex))
	def iteritems(self):
		return Connected.iteritems(self,_iterconditionFrom(self.g,self.nodevertex))
	def __delitem__(self,k):
		return Connected.__delitem__(self,k,False)
	def __setitem__(self,k,v):
		return Connected.__setitem__(self,k,v,True)
	def __getitem__(self,k):
		return Connected.__getitem__(self,k,to=False)
	def __contains__(self,k):
		return Connected.__contains__(self,k,_iterconditionFrom(self.g,self.nodevertex,condition=True))


# ATTENTION! ALL OF THESE CLASS HAS BEEN IMPLEMENTED IN ORDER TO OVERRIDE XDIGRAPH AND MANTAIN ALL ITS FUNCTIONALITY
# BUT JOINING THE POWER OF XDIGRAPH WITH THE EFFICIENCE OF IGRAPH
# add_edge
# add_node
# add_nodes_from
# init
# delete_edge ?
# delete_node


class XDiGraph(nx.XDiGraph):
	"""
	overrided by trustlet, use instead of an adiacency list in order to represent data,
	a fake-dictionary that manage an igraph instance.
	"""
	def __init__(self, data=None, name='', selfloops=False, multiedges=False):
		nx.XDiGraph.__init__(self, data=data, name=name, selfloops=selfloops, multiedges=multiedges)
		self.succ = SuccDict()
		self.pred = PredDict(self.succ.g)
		self.adj = self.succ
		return None

	#this methods are overrided only for avoid useless waste of time
	#in theory this class have to work only with __init__ method overrided
	def add_edge(self, n1, n2=None, x=None):
		nx.XDiGraph.add_edge.__doc__
		
		if n2 is None: # add_edge was called as add_edge(e), with e a tuple
			if len(n1)==3: #case e=(n1,n2,x)
				n1,n2,x=n1
			else:		   # assume e=(n1,n2)
				n1,n2=n1   # x=None

		# if edge exists, quietly return if multiple edges are not allowed
		if not self.multiedges and self.has_edge(n1,n2,x):
			return

		#add nodes 
		self.succ[n1]={}
		self.succ[n2]={}

		# self loop? quietly return if not allowed
		if not self.selfloops and n1==n2: 
			return
		
		if self.multiedges: # append x to the end of the list of objects
							# that defines the edges between n1 and n2
			self.succ[n1][n2]=self.succ[n1].get(n2,[])+ [x]
		else:  # x is the new object assigned to single edge between n1 and n2
			self.succ[n1][n2]=x

	def add_node(self, n):
		nx.DiGraph.add_node.__doc__

		self.succ[n]={}
		
	def add_node_from(self, nlist):
		nx.DiGraph.add_node_from.__doc__

		for n in nlist:
			self.succ[n]={}
		
	def delete_edge(self, n1, n2=None, x=None, all=False):
		nx.XDiGraph.delete_edge.__doc__

		if n2 is None: #  was called as delete_edge(e)
			if len(n1)==3:	#case e=(n1,n2,x)
				n1,n2,x=n1
			else:		   # assume e=(n1,n2)
				n1,n2=n1   # x=None

		if self.multiedges:				 # multiedges are stored as a list
		   if (self.succ.has_key(n1)
			   and self.succ[n1].has_key(n2)
			   and x in self.succ[n1][n2]):
				self.succ[n1][n2].remove(x)	 # remove the edge item from list
				if len(self.succ[n1][n2])==0: # if last edge between n1 and n2
					del self.succ[n1][n2]	  # was deleted, remove all trace
		else:  # delete single edge
			if self.has_successor(n1,n2):
				del self.succ[n1][n2]
		return


	def delete_node(self,n):
		nx.DiGraph.delete_node.__doc__

		#the edges are automatically removed
		try:
			del self.succ[n]		  # remove node from succ
		except KeyError: # NetworkXError if n not in self
			raise NetworkXError, "node %s not in graph"%(n,)

