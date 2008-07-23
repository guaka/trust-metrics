"""
Network classes

In this file, was stored all the class that
wrap the network in DOT format.
Each network supported has it's own class to wrap it.
"""


from trustlet.Table import Table
from trustlet.powerlaw import power_exp_cum_deg_hist
import trustlet

import os,re
from networkx.xdigraph import XDiGraph
from networkx import cluster, path, component

import numpy

average = lambda x: x and float(sum(x)) / len(x)


def dataset_dir(path=None):
    """Create datasets/ directory if needed."""
    if not path:
        path = ''
        if os.environ.has_key('HOME'):
            path = os.environ['HOME']
    dataset_path = os.path.join(path, 'datasets')
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    return dataset_path
        

class Network(XDiGraph):
    """
    Network dataset, extending networkx.xdigraph.XDiGraph
    see https://networkx.lanl.gov/reference/networkx/networkx.xgraph.XDiGraph-class.html
    """
    
    def __init__(self, from_graph = None, make_base_path = True, base_path = None):
        '''
        Create directory for class name if needed
        base_path: the path to put dataset directory
        '''

        XDiGraph.__init__(self, multiedges = False)
        if make_base_path:
            self.path = os.path.join(dataset_dir(base_path), self.__class__.__name__)
            if not os.path.exists(self.path):
                os.mkdir(self.path)

        if from_graph:
            self.paste_graph(from_graph)

    def connected_components(self):
        G = self
        if self.is_directed():
            G = G.to_undirected()
        return component.connected_components(G)

    def connected_components_size(self):
        return map(len, self.connected_components())


    def strongly_connected_components(self):
        G = self
        if self.is_directed():
            G = G.to_undirected()
        return component.connected_components(G)

    def strongly_connected_components_size(self):
        return map(len, self.connected_components())

    def avg_degree(self):
        return average(self.degree())

    def std_in_degree(self):
        return numpy.std(self.in_degree())

    def std_out_degree(self):
        return numpy.std(self.out_degree())

    def degree_histogram(self):
        from networkx import degree_histogram
        return degree_histogram(self)

    def _show_method(self, method, desc = ""):
        if not desc:
            desc = method
        print desc, getattr(self, method)()
        
    def info(self):
        """Show information."""
        XDiGraph.info(self)
        
        for method, desc in [("std_in_degree", "Std deviation of in-degree:"),
                             ("std_out_degree", "Std deviation of out-degree:"),
                             ("average_clustering", "Average clustering coefficient:"),
                             ("link_reciprocity", "Ratio of edges reciprocated:"),
                             ("powerlaw_exponent", "Power exponent of cumulative degree distribution:")]:
            self._show_method(method, desc)
        
    def powerlaw_exponent(self):
        return power_exp_cum_deg_hist(self)

    def is_connected(self):
        if self.is_directed():
            G = self.to_undirected()
            return component.is_connected(G)
        else:
            return component.is_connected(self)

    def is_strongly_connected(self):
        if self.is_directed():
            return component.is_strongly_connected(self)

    def link_reciprocity(self):
        """Calculate the reciprocity of the edges (without paying attention 
        to the value on the edges."""
        return 1.0 * sum([self.has_successor(e[1], e[0]) 
                          for e in self.edges_iter()]) / self.number_of_edges()

    def in_degree_hist(self):
        """in-degree histogram, minor adaptation from 
        networkx.function.degree_histogram"""
        degseq = self.in_degree()
        dmax = max(degseq)+1
        freq = [0 for d in xrange(dmax)]
        for d in degseq:
            freq[d] += 1
        return freq

    def out_degree_hist(self):
        """out-degree histogram, minor adaptation from 
        networkx.function.degree_histogram"""
        degseq = self.out_degree()
        dmax = max(degseq)+1
        freq = [0 for d in xrange(dmax)]
        for d in degseq:
            freq[d] += 1
        return freq

    def download_f_le(self, url, filename):
        '''Download url to filename into the right path '''
        filepath = os.path.join(self.path, filename)
        print "Downloading %s to %s " % (url, filepath)

        import urllib2
        try:
            asock = urllib2.urlopen(url)
            f = open(filepath, 'w')
            f.write(asock.read())
            f.close()
            asock.close()
        except urllib2.HTTPError, e:
            print e.code
            print "Cannot download dataset"


    def _read_dot(self, filepath):
        """Read file."""
        print "Reading", filepath
        #import networkx
        #graph = networkx.read_dot(filepath)
        graph = trustlet.helpers.cached_read_dot(filepath)
        self.paste_graph(graph)
        
    def paste_graph(self, graph):
        """Paste graph into object."""
        for node in graph.nodes_iter():
            self.add_node(node)

        for edge in graph.edges_iter():
            self.add_edge(edge)


    def _paste_graph(self, graph):
        """Deprecated."""
        self.paste_graph(graph)

    def ditch_components(self, threshold = 3):
        """Ditch components with less than [threshold] nodes"""

        undir_graph = self.to_undirected()
        if len(undir_graph):
            concom_subgraphs = component.connected_component_subgraphs(undir_graph)[1:]
            n_remove = 0
            for subgraph in concom_subgraphs:
                if len(subgraph) <= threshold:
                    for node in subgraph:
                        n_remove += 1
                        self.delete_node(node)
            print "Thrown out", n_remove,
            print "nodes, fraction: ", 1.0 * n_remove / len(undir_graph)
        else:
            print "Empty graph, no components to ditch"

    def _sorted_edges(self):
        """sorted edges"""
        edges = self.edges()
        edges.sort()
        return edges

    def _edge_array(self, mapper = None):
        """numpy array of sorted edges, mapper is an optional function
        that will be applied to the edges"""
        return numpy.array(map(mapper, self._sorted_edges()))

    def average_clustering(self):
        """Average clustering coefficient."""
        return average(cluster.clustering(self))

    def transitivity(self):
        """Clustering transitivity coefficient."""
        return cluster.transitivity(self)

    def avg_shortest_distance(self):
        """Average shortest distance between nodes."""
        # TODO: pay attention to the fact there are 2 or more connected component
        pair_distances = path.all_pairs_shortest_path_length(self)
        return average([average(x.values()) for x in pair_distances.values()])

    def min_in_edges(self, num):
        """Nodes with minimum of num incoming edges."""
        return [n for n in self if len(self.in_edges(n)) > num]
    

class WeightedNetwork(Network):
    """A weighted network.

    Things to arrange:
    * weights can be discrete or continuous
    """
    
    def __init__(self, weights = None, has_discrete_weights = True, base_path = None):
        Network.__init__(self, base_path=base_path)
        self._weights = weights
        self.has_discrete_weights = has_discrete_weights
        self.is_weighted = True

    def trust_on_edge(self, edge):
        """
        SHOULD BE: weight_on_edge
        """
        return edge[2]

    def weights(self):
        """
        Return a list with the weight of all edges
        """
        if hasattr(self, "_weights") and self._weights:
            ws = self._weights
        else:
            ws = []
            for n in self.edges_iter():
                x = n[2]
                ws.append( x )
            
            self._weights = ws
        
        return ws
        
    def info(self):
        Network.info(self)
        self.show_reciprocity_matrix()

    def min_weight(self):
        """Minimum weight."""
        return min(self.weights().values())

    def max_weight(self):
        """Maximum weight."""
        return max(self.weights().values())

    def node_controversiality(self, node):
        """Controversiality of node: the standard deviation of incoming weights."""
        return numpy.std(map(self.trust_on_edge,
                             self.in_edges_iter(node)))


    def controversiality(self):
        """Controversiality of nodes."""
        return dict([(n, self.node_controversiality(n))
                     for n in self])
        
    def avg_controversiality(self, min_num_edges = 3):
        """Average controversiality of nodes with at least min_num_edges incoming edges."""
        
        return average([self.node_controversiality(n)
                        for n in self.min_in_edges(min_num_edges)])

    def controversial_nodes(self, min_std = 0.1, min_num_edges = 3):
        """Nodes with at least min_num_edges incoming edges and controversiality > min_std."""
        node_controversy_list = [(n, c)
                                 for (n, c) in self.controversiality().items()
                                 if c >= min_std and len(self.in_edges(n)) >= min_num_edges]
        node_controversy_list.sort(lambda x, y: cmp(x[1], y[1]))
        node_controversy_list.reverse()
        return node_controversy_list
        
    def show_reciprocity_matrix(self):
        if self.has_discrete_weights:
            recp_mtx = self.reciprocity_matrix()
            tbl = Table([12] + [12] * len(self.weights()))
            tbl.printHdr(['reciprocity'] + self.weights().keys())
            tbl.printSep()
            for k, v in recp_mtx.items():
                tbl.printRow([k] + v)

    def reciprocity_matrix(self):
        """Generate a reciprocity table (which is actually a dict)."""
        def value_on_edge(e):
            if type(e) in (int, float):
                return e
            else:
                return e.values()[0]
        
        if self.has_discrete_weights:
            table = {}
            for v in self.weights().keys():
                line = []
                for w in self.weights().keys():
                    line.append(sum([value_on_edge(self.get_edge(e[1], e[0])) == w
                                     for e in self.edges_iter()
                                     if (self.has_edge(e[1], e[0]) and 
                                         value_on_edge(e[2]) == v)]))
                table[v] = line
            return table
        else:
            raise NotImplemented



class MovieLensNetwork(WeightedNetwork):
    """
    MovieLens dataset network
    """
    def __init__(self, base_path = None):
        WeightedNetwork.__init__(self, base_path = base_path)
        
        try:
            #print os.path.join(self.path,"graph.dot")
            self._read_dot( os.path.join(self.path,"graph.dot") )
        except IOError:
            raise IOError("There aren't a dot file on this path:\n "+
                          self.path+"\nplease specify another path or create dot file with movielens.py" )
        

class WikiNetwork(WeightedNetwork):
    """
    Wikipedia Network Handler.
    You must pass to it a string with lang of wikipedia, and a string with the date of dataset. 
    Optionally:
    dataset: path to a dot file that it will load and save in the dataset folder
    upthreshold: number of vote to consider edges max trusted
    current: Default True, if False use the dataset generated by History xml.
    """
        
    def __init__(self, lang, date, base_path = None, dataset = None, upthreshold = 20, force = False, current=True):
        WeightedNetwork.__init__(self,base_path=base_path )
        
        assert re.match('^[\d]{4}-[\d]{2}-[\d]{2}$',date)

        if current:
            filename = "graphCurrent"
        else:
            filename = "graphHistory"

        if upthreshold != 20:
            print "Warning: upthreshold isn't 20. Saved PredGraph might not what you want."

        self.path = os.path.join( self.path, lang )
        if not os.path.exists( self.path ):
            os.mkdir(self.path)
            
        self.path = os.path.join( self.path, date )
        if not os.path.exists( self.path ):
            os.mkdir(self.path)
        
        self.filepath = os.path.join( self.path, filename )
        #self.fix_graphdot()
        self.upthreshold = upthreshold
        
        #load from cache
        print "Reading ", os.path.join(self.path,filename+'.c2')
        cacheddataset = trustlet.helpers.load({'network':'Wiki','lang':lang,'date':date},os.path.join(self.path,filename+'.c2'))
        if cacheddataset:
            for u,v,e in cacheddataset:
                self.add_node(u)
                self.add_node(v)
                self.add_edge(u,v,e)
        else:
            try:
            
                if dataset == None:
                    self._read_dot( os.path.join( self.path,filename+'.dot' ), force )
                else:
                    if os.path.isfile( dataset ):
                        self._read_dot( dataset, force )
                        data = dataset
                    else:
                        data = os.path.join( dataset, filename+'.dot' )
                        self._read_dot( data, force )
                                    
                    #save graph.dot in right folder
                    os.rename( data, os.path.join(self.path,filename+'.dot') )

                #end else

            except IOError:
                                        
                raise IOError("There isn't a dot file on this path:\n "+
                              self.path+"\nplease specify another path or create dot file with wikixml2dot.py" )

        self.weights()
        self.__rescale()
        

    def __map(self, value):
        """
        take a value to rescale in range 0..1
        """
        if type(value) is str:
            value = int(value)

        if value >= self.upthreshold:
            return 1.0
        return 1.0 * value / self.upthreshold

    def __rescale(self):
        """
        take the _weights field and rescale the value
        """

        self._weights = [self.__map(x) for x in self._weights]

        return self._weights

    def trust_on_edge(self,edge):
        """
        return trust on edge passed
        """
        if type(edge[2]) is int:
            return self.__map( edge[2] )

        return self.__map( edge[2].values()[0] )

    def _read_dot(self, filepath, force = False):
        """Read file."""
        print "Reading", filepath
        #import networkx
        #graph = networkx.read_dot(filepath)
        graph = trustlet.helpers.cached_read_dot(filepath,force)
        self.paste_graph(graph)
        
    #fix_graphdot = trustlet.Dataset.Advogato.AdvogatoNetwork.fix_graphdot
    def fix_graphdot(self):
        """Fix syntax of graph.dot (8bit -> blah doesn't work!)"""
        print 'Fixing graph.dot'
        graph_file = open(self.filepath, 'r')
        l_names = graph_file.readlines()
        graph_file.close()
        re_fix = re.compile(' (\w+)')
        fixed_lines = map(lambda s: re_fix.sub(r' "\1"', s), l_names)

        writefile = open(self.filepath, 'w')
        writefile.writelines(fixed_lines)
        writefile.close()
        return self.filepath

if __name__ == "__main__":
    WikiNetwork("vec")
