import igraph as ig
import networkx as nx
import pprint
#methods of networkx to override:

# add_edge
# add_node
# add_nodes_from
# init

#methods of dict to implement:

# setitem
# getitem
# delitem (with del?)
# get() D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
# iteritems
# every iter[.]*
def _getVertexFromName(g, k):
        return g.vs.select( lambda v: v.attributes().has_key('name') and v['name'] == k )


class XDiGraph(nx.XDiGraph):
	def __init__(self, data=None, name='', selfloops=False, multiedges=False):
		nx.XDiGraph.__init__(self, data=data, name=name, selfloops=selfloops, multiedges=multiedges)
		


#utility class in order to override XDiGraph
class igraphDict(dict):
    """
    this class provide a match from the xdigraph adj lists,
    and the igraph library.
    """
    def __init__(self):
        self.g = ig.Graph(n=0,directed=True)
        
    def keys(self):
        return list(self.iterkeys())
    def values(self):
        return list(self.itervalues())

    def iterkeys(self):
        for n in self.g.vs:
            # if there is at least an edge that starts in node, then this node is in the first dictionary, so we had to include it
            # but for the nodes added without outedges? these nodes has indegree == 0..
            if self.g.outdegree( n.index ) > 0 or self.g.indegree( n.index ) == 0:
                yield n['name']
            
    def itervalues(self):
        for node in self.g.vs:
            # if there is at least an edge that starts in node, then this node is in the first dictionary, so we had to include it
            # but for the nodes added without outedges? these nodes has indegree == 0..
            if self.g.outdegree( node.index ) > 0 or self.g.indegree( node.index ) == 0: 
                yield ConnectedTo(node,self.g)

    def get(k, d=None ):
        try:
            return self.__getitem__(k)
        except KeyError:
            return d

    def items(self):
        return list(self.iteritems())
    def iteritems(self):
        for node in self.g.vs:
            # if there is at least an edge that starts in node, then this node is in the first dictionary, so we had to include it
            # but for the nodes added without outedges? these nodes has indegree == 0..
            if self.g.outdegree( node.index ) > 0 or self.g.indegree( node.index ) == 0: 
                yield (node['name'],ConnectedTo(node,self.g))
                
    def __delitem__(self, k):
        #del the node k, and all his edges
        kidls = _getVertexFromName(self.g, k)
        if not len(kidls):
            raise KeyError("This key ("+str(k)+") is not in the dictionary")

        nodesInK = ConnectedTo( k, self.g )
        for n in nodesInK.iterkeys_id():
            self.g.delete_vertices( n )

        self.g.delete_vertices( kidls[0].index ) #delete also all the edges that contains this vertex
        
        return None

    def __getitem__(self, k):
        return ConnectedTo(k,self.g)

    def __setitem__(self,k,v):
        #v is not used!
        #assert hasattr( v, '__name__' ), "This is not a ConnectedTo class!"
        #assert v.__name__ == 'ConnectedTo', "This is not a ConnectedTo class!"
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


class ConnectedTo(dict):
    """
    used to represent the indegree of a node.
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
            #if exist go on 

            self.nodevertex = mynodeIDls[0]
        
        return None

    
    def get(k, d=None ):
        try:
            return self.__getitem__(k)
        except KeyError:
            return d
        
    def keys(self):
        return list(self.iterkeys())

    def iterkeys(self):
        for n in self.g.vs:
            if self.g.indegree( n.index ) > 0:
                yield n['name']
            
    def iterkeys_id(self):
        for n in self.g.vs:
            if self.g.indegree( n.index ) > 0:
                yield n.index
            
    def keys_id(self):
        return list(iterkeys_id)

    def values(self):
        return list(self.itervalues())

    def itervalues(self):
        for node in self.g.vs:
            if self.g.indegree( node.index ) > 0: 
                yield self.g.es[ self.g.get_eid( self.nodevertex.index, node.index ) ]['weight']


    def items(self):
        return list(self.iteritems())

    def iteritems(self):
        for node in self.g.vs:
            if self.g.indegree( node.index ) > 0: 
                yield (node['name'], self.g.es[ self.g.get_eid( self.nodevertex.index, node.index ) ]['weight'] )

    def __delitem__(self, k):
        kidls = _getVertexFromName(self.g, k)
        if not len( kidls ):
            raise KeyError("This key is not in dictionary")
        
        self.g.delete_edges( self.g.get_eid( self.nodevertex.index, kidls[0].index ) )
        self.g.delete_vertices( kidls[0].index ) 
        return None

    def __getitem__(self, k):
        kidls = _getVertexFromName(self.g, k)
        if not len( kidls ):
            raise KeyError("This key ("+str(k)+") is not in dictionary")
        
        return self.g.es[ self.g.get_eid( self.nodevertex.index, kidls[0].index ) ]['weight']

    def __setitem__(self,k,v):
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


    def __str__(self):
        """
        return only some of the data
        """
        return pprint.pformat(self.g.__str__())

