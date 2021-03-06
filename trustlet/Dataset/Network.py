# -*- coding: utf-8 -*-
"""
Network classes

In this file, was stored all the class that
wrap the network in DOT format.
Each network supported has it's own class to wrap it.
"""

from networkx.readwrite import read_pajek,write_pajek
#import igraph # fist improve memory usage and speed of igraphXdiGraphMatch

from networkx import read_dot,write_dot
from trustlet.Table import Table
from trustlet.powerlaw import power_exp_cum_deg_hist
import trustlet
import sys
import networkx

import os

from networkx.xdigraph import XDiGraph
#from trustlet.igraphXdigraphMatch import XDiGraph fist improve memory usage and speed of igraphXdiGraphMatch
from networkx import write_pajek,read_pajek

from networkx import cluster, path, component

import numpy
"""
def read_pajek( file ):
	n = trustlet.Dataset.Network.Network()
	n.succ.g = n.succ.g.Read_Pajek( file )
	return n

def write_pajek( network, file ):
	assert network.succ.g.vs[0].attributes().has_key('name')	
	return network.succ.g.write_pajek( file )
"""
average = lambda x: x and float(sum(x)) / len(x)
toU = lambda x: unicode(x) #to unicode
UPBOUNDPERCENTAGE = 95

def dataset_dir(path=None):
	"""Create datasets/ directory if needed."""
	
	if not path:
		path = ''
		if os.environ.has_key('HOME'):
			path = os.environ['HOME']
	dataset_path = os.path.join(path, 'datasets')
	
	trustlet.helpers.mkpath(dataset_path)
	
	return dataset_path
		

class Network(XDiGraph):
	"""
	Network dataset, extending networkx.xdigraph.XDiGraph
	see https://networkx.lanl.gov/reference/networkx/networkx.xgraph.XDiGraph-class.html
	"""
	
	def __init__(self, from_graph = None, make_base_path = True, base_path = None, prefix=None, cachedict=None, filepath = '', date=None, silent=False):
		'''
		Create directory for class name if needed
		base_path: the path to put dataset directory
				   ex. home/../datasets
		prefix:
		   you can specify a prefix in path for the Network folder if you want
		   ex. prefix = '_' --> path = /home/.../datasets/_NetworkName/date/graph.c2
		cachedict:
		   must be a dictionary
		'''

		XDiGraph.__init__(self, multiedges = False)
		self.level_map = {}
		self.silent = silent
		self.date = date
		self.filename = ''
		self.values_on_edges = False
		if cachedict and type(cachedict) is dict:
			self._cachedict = cachedict
		else:
			self._cachedict = None

		self.name = 'generic_network'
		if make_base_path:

			if prefix:
				classpath = prefix+self.__class__.__name__
			else:
				classpath = self.__class__.__name__

			self.path = os.path.join(dataset_dir(base_path), classpath)
			if not os.path.exists(self.path):
				os.mkdir(self.path)

		if filepath:
			self.filepath = filepath
			self.filename = os.path.split(self.filepath)[1]
		else:
			if prefix:
				classpath = prefix+self.__class__.__name__
			else:
				classpath = self.__class__.__name__
				
			self.filepath = os.path.realpath( os.path.join(dataset_dir(base_path), classpath, self.date == None and '.' or self.date   , 'graph' ) )
			self.filename = 'graph'
		

		if from_graph:
			self.paste_graph(from_graph)
		else:
			#direct load of c2 files
			if self._cachedict: 
				self.load_c2(self._cachedict) 

	
	def get_keyOnDataset(self):
		if self._cachedict:
			return self._cachedict.copy()
		else:
			return None
 
	def _load_from(self, function, extension, string_to_weight, decodeUtf8=False):
		#load from a generic format

		if hasattr(self,"filepath") and self.filepath and (os.path.exists(self.filepath) or os.path.exists(self.filepath+extension) or os.path.exists(self.filepath[:-3]+extension) ):
			if self.filepath.endswith( extension ):
				w = function(self.filepath)
			elif os.path.exists(self.filepath+extension):
				w = function(self.filepath+extension)
			elif os.path.exists(self.filepath[:-3]+extension): #if the filename ends with another extension (usually c2)
				w = function(self.filepath[:-3]+extension)
			else:
				sys.stderr.write( "error loading network, filepath does not exists\n" )
				return False
			
			#paste_graph undo the changes for utf8
			self.paste_graph(w,key_to_delete='value', decodeUtf8=decodeUtf8)
			return True
		else:
			sys.stderr.write('Error! filepath is not defined! set first the filepath (ending with ".c2")\n')
			return False

		
	def load_pajek(self, decodeUtf8=False):
		"""
		load a graph in a pajek format.
		we strongly recomend to use c2 format,
		because it implements some cache-mechanism
		and save automatically some important information
		about network (as level_map).
		if you use pajek format remember to set your
		level_map before use some methods (as info or reciprocity_matix for example)
		and to set parameter force to True, if you had to elaborate a function with
		this parameter.
		decodeUtf8 = if true, the nodes and the edges will be automatically decoded
					 into utf8, if false it aren't.
		return False if fail, else return True.
		"""
		def edges(e):
			return e

		return self._load_from( read_pajek, '.net', edges, decodeUtf8 )

	def load_dot(self, decodeUtf8=False, wiki=False):
		"""
		load a graph in a dot format.
		we strongly recomend to use c2 format,
		because it implements some cache-mechanism
		and save automatically some important information
		about network (as level_map).
		if you use dot format remember to set your
		level_map before use some methods (as info or reciprocity_matix for example)
		and to set parameter force to True, if you had to elaborate a function with
		this parameter.
		decodeUtf8 = if true, the nodes and the edges will be automatically decoded
					 into utf8, if false it aren't
		wiki = if True the dot contains a wikinetwork, if False it not.
		return False if fail, else return True.
		"""
		if not wiki:
			def edges(e):
				return e
		else:
			def edges(e):
				if type(e) is dict:
					for k in e.keys():
						e[k] = int(e[k])
					return e
				else:
					return int(e)
		
		return self._load_from( read_dot, '.dot', edges, decodeUtf8 )
 
	def _save_to( self, function, extension, weight_to_string, encodeAscii=False ):
		#save to a generic format
		if hasattr(self,"filepath") and self.filepath:
			#create a new network, encoded with ascii
			if encodeAscii:
				N = trustlet.Dataset.Network.Network() #we lose all the info :(
				for n in self.nodes_iter():
					N.add_node( n.encode('utf-8') )
				for e in self.edges_iter():
					N.add_edge( e[0].encode('utf-8'), e[1].encode('utf-8'), weight_to_string( e[2] ) )
			else:
				# in order to avoid UnicodeDecodeError
				# we replace the unicode character with the ord() of it's .encode('utf-8') value

				#HELPER FUNCTIONS
				#check if a string is in ascii
				#return a string in ascii, (convert the non-ascii char)
				def to_ascii(s):
					newn = ''
					for i in xrange(len(s)):	 # / is replaced with /*exadecimal code of /*
												 # so when we undo this change, / will be replaced with / :-)
						if not ord(s[i]) < 128 or s[i] == '/' or s[i] == '"': # " gives problem with pajek
							fakeUtf8Char = '/' +str( '%.2x'%ord(s[i]) )
							newn += fakeUtf8Char #replace the invalid position with a '?' in order to avoid UnicodeDecodeError
						else:
							newn += s[i]
	
					return newn
				#END HELPER
				N = trustlet.Dataset.Network.Network() #we lose all the info :(
				for n in self.nodes_iter():
					N.add_node( to_ascii(n.encode('utf-8') ) )

				for e in self.edges_iter():
					e0 = to_ascii( e[0].encode('utf-8') )
					e1 = to_ascii( e[1].encode('utf-8') )
								
					N.add_edge( e0, e1, weight_to_string(e[2]) )
			
			if self.filepath.endswith( '.c2' ):
				function(N, self.filepath[:-3]+extension )
			elif self.filepath.endswith( extension ):
				function(N, self.filepath )
			elif self.filepath.endswith( '.c2' ):
				filepath = self.filepath[:-3]
				function(N, filepath+extension )
			else:
				function(N, self.filepath+extension )
			return True
		else:
			sys.stderr.write('Error! filepath is not defined! set first the filepath (ending with ".c2")\n')
			return False
		
	
	def save_pajek(self, encodeAscii=False):
		"""
		save this network in pajek format in `filepath`.net
		we strongly recomend to use c2 format,
		because it implements some cache-mechanism
		and save automatically some important information
		about network (as level_map).
		if you use pajek format remember to set your
		level_map before use some methods (as info or reciprocity_matix for example)
		and to set parameter force to True, if you had to elaborate a function with
		this parameter.
		encodeAscii = if true, the value will be decoded to ascii, before writing them,
					  else it aren't, but
					 in order to avoid UnicodeDecodeError
					 we replace the unicode character with the ord() of it's .encode('utf-8') value
		return False if fail, else return True.
		"""
		def edges(e):
			return e
		return self._save_to( write_pajek, '.net', edges, encodeAscii ) 

	def save_dot(self, encodeAscii=False):
		"""
		save this graph in dot format (in self.filepath)
		we strongly recomend to use c2 format,
		because it implements some cache-mechanism
		and save automatically some important information
		about network (as level_map).
		if you use dot format remember to set your
		level_map before use some methods (as info or reciprocity_matix for example)
		and to set parameter force to True, if you had to elaborate a function with
		this parameter.
		encodeAscii = if true, the value will be decoded to ascii, before writing them,
					  else it aren't, but
					  in order to avoid UnicodeDecodeError
					  we replace the unicode character with the ord() of it's .encode('utf-8') value
		return False if fail, else return True.
		"""
		def edges(e):
			return e
		return self._save_to( write_dot, '.dot', edges, encodeAscii )


	def save_c2(self,cachedict=None ):
		"""
		see load_c2 function. The parameter are the same.
		"""
		if not hasattr(self,"filepath") or self.filepath=='':
			sys.stderr.write( "Error: filepath is not defined!\n" )
			return False
		
		if not self.filepath.endswith('.c2'):
			filepath = self.filepath+'.c2'
		else:
			filepath = self.filepath
		
		if hasattr( self.succ, "g" ):
			tostore = self.succ.g	
		else:
			tostore = self	

		if cachedict:
			return trustlet.helpers.save(cachedict,
										 tostore,
										 filepath)
		elif self.get_keyOnDataset():
			return trustlet.helpers.save(self.get_keyOnDataset(),
										 tostore,
										 filepath)
		else:
			sys.stderr.write( 'Error! you have to set the cachedict parameter, at init-time, passed at save_c2()\n')
			return False
		


	def load_c2(self,cachedict=None, key_dictionary=None, cond_on_edge=None, decodeUtf8=None):
		"""
		load a c2 into this instance of Network.
		
		Parameters:
		cachedict: dictionary that is unique key for c2 network that you would load
				  nb. this parameter must be set, if you haven't set the cachedict parameter at init-time
		key_dictionary: string value used as key for the weight dictionary
					  ex: x=network.edges()[0]
						  x[2]
						  >> {key:weight_on_edge}
		cond_on_edge: function that takes a tuple in this form (string0,string1,dict)
					  string0: the start node
					  string1: the end node
					  dict: weight on edge (ex. {'value':1} on WikiNetwork, {'level':'Master'}, {'color':'violet'}.. )
					  
					  and return False if the edge had to be discarded, else return True.
		decodeUtf8 :  if false add nodes and edges as it is, if true, try to decode it
		               using string.decode('utf-8') default function. 
					   NB: set decodeUtf8 to true, only if this graph contains string
					       saved by save_c2/pajek/dot of trustlet.
		"""
		
		if not hasattr(self,"filepath") or self.filepath == '':
			sys.stderr.write( "Error: filepath is not defined!\n" )
			return False

		if cachedict:
			cachekey = cachedict
		elif self.get_keyOnDataset():
			cachekey = self.get_keyOnDataset()
		else:
			sys.stderr.write( 'Error! you have to set the cachedict parameter, at init-time, passed at save_c2()\n' )
			return False
		
		if not self.filepath.endswith('.c2'):
			self.filepath += '.c2'

		pydataset = trustlet.helpers.load(cachekey, self.filepath)

		if not pydataset and cachekey.has_key('threshold'):
			# retry without thresold
			del cachedict['threshold']
			pydataset = trustlet.helpers.load(cachekey, self.filepath)
			
			if not pydataset:
				sys.stderr.write( 'On this c2 '+self.filepath+' there isn\'t this key '+str(cachekey)+'\n' )	
				return False
	
			#generate dataset with the requested threshold
			if threshold > 1 and type(pydataset) is tuple:
				edges = filter( lambda x: x[2] >= threshold, pydataset[1] )
				pydataset = (pydataset[0],edges)

		if pydataset:
			#now I'm sure that this network is in a c2 file
			self.filename = os.path.split(self.filepath)[1]
		
			try:
				net = trustlet.helpers.toNetwork( pydataset, key_dictionary )
			except IOError:
				if not self.silent:
					print "Warning! c2 is not consistent! The loading of network is failed"
					print "Forcing conversion from dot.."
				try:
					val=trustlet.conversion.dot.to_c2(self.dotpath,self.filepath,cachekey)
				except IOError:
					raise IOError( "Error! dot does not exist. download it from trustlet.org and make sure this path exist "+self.dotpath )
				except AttributeError:
					raise AttributeError( "Error! dotpath or filepath is not set" )

				if not val:
					raise IOError( "Dot file exist but the conversion into c2 failed!" )
				#now retry
				try:
					net = trustlet.helpers.toNetwork( pydataset, key_dictionary )
				except IOError:
					raise IOError( "the conversion module made a non consistent c2." )
			   
			self.paste_graph( net, cond_on_edge=cond_on_edge, decodeUtf8=decodeUtf8 ) #copy the graph loaded in self
		else:
			sys.stderr.write( 'On this c2 '+self.filepath+' there isn\'t this key '+str(cachekey)+'\n')	
			return False

		if not hasattr(self,"level_map") or hasattr(self,"level_map") and  not self.level_map:
			self.level_map = self.weights()
		
		return True

	def _name(self):
		"""
		return name of the network
		"""
		name = self._name_lowered()
		if name:
			return name[0].upper()+name[1:] #up only first letter
		else:
			return name
		
	def _name_lowered(self):
		"""Helper for url."""
		name = self.__class__.__name__.lower()
		if name[-7:] == 'network':
			name = name[:-7]
		return name
		
	def download_file(self, url, filename):
		'''Download url to filename into the right path '''
		filepath = os.path.join(self.path, filename)
		if not self.silent:
			print "Downloading %s to %s " % (url, filepath)

		import urllib2
		try:
			asock = urllib2.urlopen(url)
			f = open(filepath, 'w')
			f.write(asock.read())
			f.close()
			asock.close()
		except urllib2.HTTPError, e:
			try:
				asock = urllib2.urlopen(url+'.bz2')
				f = open(filepath+'.bz2', 'w')
				f.write(asock.read())
				f.close()
				asock.close()
			except urllib2.HTTPError:
				raise IOError( "Cannot download dataset, for a complete list of it, go to "+os.path.split( os.path.split( url )[0] )[0] )

	def add_edge_savememory(self,u,v=None,e=None):
		'''
		like add_edge, but use pool of edges to save memory.
		You *can't modify* edges added with this method
		'''
		if not v:
			u,v,e = u
		self.add_edge(u,v,trustlet.helpers.pool(e))

	def connected_components(self):
		if self.is_directed():
			G = self.to_undirected()
		else:
			G = self
		return component.connected_components(G)

	def number_of_connected_components(self):
		return len(self.connected_components())

	def connected_components_size(self,n=None):
		'''n = number of cc to keep'''
		if n:
			return map(len, self.connected_components()[:n])
		else:
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
		
	def quick_info(self):
		XDiGraph.info(self)

	def info(self,cachedict=None,force=False):
		"""
		Show information.
		NB: using this method after load_distrust, can produce different results,
			because of the additional distrust_edges inserted in the the network by load_distrust.
		
		cachedict: if you use a non-standard network, you had to set cachedict (or set it at init-time)	   
		"""
		
		if self.number_of_edges() == 0:
			XDiGraph.info(self)
			return None

		#cache enabled only if c2
		if self._name() != "Wiki" and self._name() != 'Dummyweighted' and self._name() != 'Dummy' and self._name() and self._name() != 'Weighted': #skip nonstandard net
			tp = trustlet.helpers.relative_path( self.filepath, 'datasets' )
			if tp:
				path = os.path.join( os.path.split(tp[0])[0], 'shared_datasets', tp[1] )
			else:
				raise IOError("Malformed path of dataset! it must contain 'datasets' folder")
		else:
			path = self.filepath #with non standard network, cannot upload info
			if self._name() != 'Wiki' and not cachedict and not self.get_keyOnDataset(): #if cachedict not set
					raise Exception("For non-standard dataset, you must set the cachedict parameter (or if you wouldn't you had to set force parameter to True)")
			
		if not self.filepath.endswith( '.c2' ):
			path += '.c2'

		if cachedict or self.get_keyOnDataset():
			cachekey = ( cachedict != None and cachedict.copy() ) or self.get_keyOnDataset()
			cachekey['function'] = 'info'
		else:
			cachekey = {'network':self._name(),'date':self.date,'function':'info'}
			if self._name() == 'Wiki':
				cachekey['lang'] = self.lang

		if hasattr(self,"cond_on_edge") and self.cond_on_edge:
			cachekey['cond_on_edge']=self.cond_on_edge.__name__

		if not force:	 
			# cache
			data = trustlet.helpers.load( cachekey, path, fault=False)
			
			if data:  # if data is not false
				print data
				return None

		if cachekey.has_key("cond_on_edge") and cachekey['cond_on_edge']=='<lambda>':
			sys.stderr.write( "Warning! cannot save the data about computation, with a lambda condition.\nRemove the 'cond_on_edge' key from your key-dict\n" )
			return None
		
		if force: #if force specified, we had to recalculate also 'function':'info'
			buffer = '' #buffer that contains all the metric with his respective values in plain text. It will be saved in cachedict extended with 'function': 'info'
		stdout = sys.stdout #save stdout
		
		# turn down warning
		stderr = sys.stderr
		sys.stderr = file( '/dev/null', 'w' )
		tmpnam = os.tmpnam()
		sys.stderr = stderr
			
		from trustlet.netevolution import fl
		function_list = fl[:] #copy fl
		self.quick_info()
		
		for method, desc in [("std_in_degree", "Std deviation of in-degree:"),
							 ("std_out_degree", "Std deviation of out-degree:"),
							 ("average_clustering", "Average clustering coefficient:"),
							 ("link_reciprocity", "Ratio of edges reciprocated:"),
							 ("powerlaw_exponent", "Power exponent of cumulative degree distribution:"),
							 ("number_of_connected_components","Number of connected components:"),
							 ("connected_components_size2","Connected component size:"),
							 ]:

			cachekey['method'] = desc[:-1]
			if not force:
				data = trustlet.helpers.load( cachekey, path, fault=False)
				if data:
					print data
					continue
				
			sys.stderr.write( "Evaluating "+desc[:-1]+"\n" )
			tmpfile = file( tmpnam, 'w' ) #set temporary buffer
				
			sys.stdout = tmpfile #save all output in a temporary file

			try:
				self._show_method(method, desc)
				
			except:
				sys.stderr.write( "Warning! "+desc+" not calculated (probably because your network has no level_map)\n" )  
				sys.stdout = stdout #restore stdout
				continue
			
			#each time that we calculate a metric, then we save it
			#this stdout sostitution is made because the metric print result
			#on standard output, in order to unmodify the other functions,
			#this workaround is needed
			tmpfile.close()
			info = file(tmpnam).readline()
			#save in cache
			if not trustlet.helpers.save( cachekey, info, path ):
				sys.stderr.write( "Warning! save of cache about "+desc[:-1]+" failed\n" )
				
			sys.stdout = stdout #restore stdout
			#print on real stdout
			print info 

			if force: #save new data for 'fucntion':'info' key
				buffer += info	
			
		del function_list[2] #number of edges
		del function_list[3] #number of nodes
		del function_list[-1] #number of connected components
		del function_list[9] #betwenness centrality (a type)
		del function_list[10] #betwenness centrality (a type)
		del function_list[11] #betwenness centrality (a type)

		#in order to workaround a check on the date
		if not (hasattr(self,"date") and self.date):
			self.date = '1970-01-01'
			
		#another list of functions
			
		for (f,pf) in function_list.__iter__():
			cachekey['method'] = f.__name__
			if not force:
				data = trustlet.helpers.load( cachekey, path, fault=False)
				if data:
					print data
					continue

			sys.stderr.write( "Evaluating "+f.__name__+"\n" )
				
			try:
				res = f(self,self.date)[1]	
			except:
				sys.stderr.write( "Warning! "+f.__name__+" not calculated (probably because your network has no level_map)\n" )	 
				continue
			
            #print on stdout
			info = f.__name__+" : "+str(res)+"\n"
			print info 
			
			if force: #save new data for 'fucntion':'info' key
				buffer += info	
			#save in cache
			if not trustlet.helpers.save( cachekey, info, path ):
				sys.stderr.write( "Warning! save of cache about "+desc[:-1]+" failed\n" )
		
		del cachekey['method']
		if not trustlet.helpers.save( cachekey, buffer, path ):
			sys.stderr.write( "Warning! save of whole cache failed\n" )
	
		return None
		
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
		if not self.number_of_edges():
			print 'warning: There are 0 edges! Check the consistence of this dataset'
			return 0.0

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

	
	def download_dataset(self, url, filepath ):
		"""
		download a dataset from a url to a filepath, if it not exist
		NB: automatically add filename to url
		"""
		
		filename = os.path.split( filepath )[1] 

		if not os.path.exists(filepath) and not os.path.exists(filepath+'.bz2'):
			self.download_file( os.path.join(url,filename) , filename )


	def _read_dot(self, filepath,force=False):
		"""Read file."""
		if not self.silent:
			print "Reading", filepath
		#import networkx
		#graph = networkx.read_dot(filepath)
		graph = trustlet.helpers.cached_read_dot(filepath,force)
		if hasattr( self, "cond_on_edge" ):
			self.paste_graph(graph,cond_on_edge=self.cond_on_edge)
		else:
			self.paste_graph(graph)
		
	
	def paste_graph(self, graph, avoidset=None,cond_on_edge=None, key_to_delete=None, decodeUtf8=None):
		"""
		Paste graph into object.
		Parameter:
		   graph: the graph
		   avoidset: the set object that contains all the nodes leaved out from the copying
		   key_to_delete: delete specified key in the dictionary on edge, if exist.
		   decodeUtf8: if false add nodes and edges as it is, if true, try to decode it
		               using string.decode('utf-8') default function. 
					   NB: set decodeUtf8 to true, only if this graph contains string
					       saved by save_c2/pajek/dot of trustlet.
		"""
		#helper function BEGIN
		#we have to undo the workaround done in the save, (in order to avoid UnicodedecodeError)

		#HELPER FUNCTIONS
		#check if a string is in ascii
		#return a string in ascii, (convert the non-ascii char)
		def to_utf8(s):
			newn = ''
			# is used to know how many chars to skip
			# after the decode of a utf8-char.
			# ex. /ba --> \0xba charToSkip = 2, so 'ba' are not included as chars
			charToSkip = 0
			for i in xrange(len(s)):
				if charToSkip > 0:
					charToSkip -= 1
					continue

				if s[i] == '/': #the '/' is before the utf8-char
					utf8Char = chr( int( s[i+1:i+3], 16 ) )
					newn += utf8Char #replace the invalid position with a '?' in order to avoid UnicodeDecodeError
					charToSkip = 2
				else:
					newn += s[i]
			return newn				   
		#helper function END

		#optimization function BEGIN
		def iterNode():
		#[x for x in graph.nodes_iter() if x not in avoidset]
			for x in graph.nodes_iter():
				if x not in avoidset:
					yield x


		def iterEdge(cond_on_edge):
		#[x for x in graph.edges_iter() if x[0] not in avoidset and x[1] not in avoidset and cond(x)]
			for x in graph.edges_iter():
				if x[0] not in avoidset and x[1] not in avoidset and cond_on_edge(x):
					yield x
		#optimization function END
		
		if not cond_on_edge:
			cond = lambda e:True # functions that return only true
		else:
			cond = cond_on_edge

		if graph.number_of_edges() and type(graph.edges()[0][2]) is dict and key_to_delete:
			deletekey = True
		else:
			deletekey = False

		if avoidset:

			for edge in iterEdge(cond):
				if type(edge[2]) is dict:
					keys = edge[2].keys()	
					if deletekey and keys != [key_to_delete] and key_to_delete in keys: #if it isn't the only one
						del edge[2][key_to_delete]
				#utf8 decoding
				if not decodeUtf8: 
					self.add_edge(edge )		
				else: #we use our decoding
					e0 = to_utf8(edge[0]).decode('utf-8') 
					e1 = to_utf8(edge[1]).decode('utf-8')	
					self.add_edge( e0, e1, edge[2] )
					
			for node in iterNode():
				if node not in self:
					if not decodeUtf8:	
						self.add_node(node)
					else:
						self.add_node(to_utf8(node).decode('utf8')) 

		else:
			
			for edge in graph.edges_iter():
				# if the conditions is not statisfied, the nodes will be added (because if not, the graph is different from the original)
				if not cond(edge):
					if not decodeUtf8:	
						self.add_node(edge[0])
						self.add_node(edge[1])
					else:
						self.add_node(to_utf8(edge[0]).decode('utf-8'))
						self.add_node(to_utf8(edge[1]).decode('utf-8'))	
				else:
					if type(edge[2]) is dict:	
						keys = edge[2].keys()	
						if deletekey and keys != [key_to_delete] and key_to_delete in keys: #if it isn't the only one 
							del edge[2][key_to_delete]
					#utf8 decoding
					if not decodeUtf8:
						self.add_edge(edge) # if we add an edge the nodes will be automatically added
					else:
						self.add_edge(to_utf8(edge[0]).decode('utf-8') , to_utf8(edge[1]).decode('utf-8'), edge[2]) 

			for node in graph.nodes_iter():
				if node not in self:
					if not decodeUtf8:	
						self.add_node(node)
					else:
						self.add_node(to_utf8(node).decode('utf8')) 



		if hasattr(graph,"level_map") and graph.level_map!={}:
			self.level_map = graph.level_map #override level_map


	def _paste_graph(self, graph, avoidset=None):
		"""Deprecated."""
		self.paste_graph(graph, avoidset)

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
	"""
	A weighted network.

	base_path: the path to put dataset directory
				   ex. home/../datasets
	weights: a dictionary with as key the value on edge, and as value, the integer value of the value on edge
			 ex.
				{'Apprentice':0.6......}
	has_discrete_weights: if set to false, this network is used as extension of network Network class (DEPRECATED)
	filepath: the path to the c2 file in which you would store the data of the graph
	cachedict: a dictionary used as key for the c2 file. See trustlet.org/wiki/Cache_v2_format
			   NB: if you don't set cachedict at init-time you can't set it before! and if you 
				   don't set cachedict parameter you cannot save c2 files.
	prefix:
	   you can specify a prefix in path for the Network folder if you want
	   ex. prefix = '_' --> path = /home/.../datasets/_NetworkName/date/graph.c2
	from_graph = the dataset that you would load. (in a networkx class) 
	"""
	
	def __init__(self, weights = None, has_discrete_weights = True, base_path = None,prefix=None, from_graph=None, filepath='', cachedict=None,date=None,silent=False):
		Network.__init__(self, base_path=base_path,prefix=prefix,from_graph=from_graph,cachedict=cachedict,filepath=os.path.abspath(filepath),date=date,silent=silent)
		self.name= 'generic_weighted_network'
		self.has_discrete_weights = has_discrete_weights
		self.is_weighted = True
		self._weights = weights
		self._weights_list = None
		self._weights_dictionary = None
		#self.level_map = None #this *erase* leve_map
		if not hasattr(self,'level_map'):
			self.level_map = {}		   

	def trust_on_edge(self, edge):
		"""
		SHOULD BE: weight_on_edge
		"""

		if type(edge[2]) is dict and hasattr(self,"level_map") and self.level_map:
			return self.level_map[edge[2].values()[0]]
		elif hasattr(self,"level_map") and self.level_map:
			return self.level_map[edge[2]]
		else:
			return edge[2]
			
	def weights_list(self,force=False):
		"""
		Return a list with the weights of all edges
		"""
		if hasattr(self, "_weights_list") and self._weights_list and not force:
			ws = self._weights_list
		else:		
			ws = list( self.weights(force=True) ) #create self._weights if there isn't
			self._weights_list = ws
			
		return ws
	
	def weights(self,force=False):
		"""
		Return a dictionary with the weights of all edges
		if it return an empty dictionary you probably has not set level_map.
		"""

		if hasattr(self, "_weights_dictionary") and self._weights_dictionary and not force:
			ws = self._weights_dictionary
		elif hasattr( self, "_weights" ) and self._weights and not force:
			ws = self._weights
		else:
			ws = {}
			for n in self.edges_iter():
				x = n[2]
				if type(x) is float or type(x) is int:
					ws[str(x)] = x
				else:
					if hasattr( x, 'keys' ) and hasattr( self, 'level_map' ) and self.level_map:
						ws[x.values()[0]] = self.level_map[ x.values()[0] ]
					elif type(x) is tuple:
						ws[x[0]] = x[1]
					elif type(x) is dict:
						ws[x.values()[0]] = x.values()[0]	
					
			self._weights_dictionary = self._weights = ws
		
		return ws
	
	def min_weight(self):
		"""Minimum weight."""
		return min(self.weights())

	def max_weight(self):
		"""Maximum weight."""
		if type(self.weights()) is dict:
			return [weight for weight in self.weights() if self.weights()[weight] == max(self.weights().values())]
		return max(self.weights())

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
		
	def show_reciprocity_matrix(self,cachedict=None):
		""" show a pretty table with reciprocity_matrix() values, does not work with wikinetwork """
		if self.__class__.__name__ == 'WikiNetwork':
			raise Exception( "Not implemented" )

		if self.has_discrete_weights:
			recp_mtx = self.reciprocity_matrix(cachedict=cachedict)
			tbl = Table( [12] + [12] * (len(self.weights())+1) ) #sum 1 for the nr column
			listKeys = self.weights().keys() #keys are saved in order to keep the order
			listKeys.append( 'nr' )
			tbl.printHdr(['reciprocity'] + listKeys)
			tbl.printSep()
			for k in self.weights().keys(): #avoid nr..
				tbl.printRow([k] + [recp_mtx[k][x] for x in listKeys]) #take the keys in the same order as previous call of .keys()

	def reciprocity_matrix(self,force=False,cachedict=None):
		"""
		Generate a reciprocity table (which is actually a dict) 
		with percentage of edges (and not number of edges) 
		scaled on the total number of edges of the considered level.
		ex.
		edges:
		1 -A> 2
		2 -A> 1
		2 -A> 3
		3 -J> 2
		3 -A> 4

		number_of_edges_that_vote_'A': 4
		number_of_edges_reciprocated_for_'A'_with_'A': 2
		number_of_edges_reciprocated_for_'A'_with_'J': 1
		number_of_edges_non_reciprocated_that_vote_'A': 1
		
		so, number_of_edges_reciprocated_for_'A'_with_'A' result 2/4
		and number_of_edges_reciprocated_for_'A'_with_'J' result 1/4
		number_of_edges_non_reciprocated_that_vote_'A': 1/4
		the sum is always 1.
		"""
		def value_on_edge(e):
			if type(e) in (int, float):
				return e
			elif type(e) is dict:
				if len(e)>1:
					sys.stderr.write( 'I might wrong value on edge\n' )
				return e.values()[0]
			else:
				raise Exception( 'Unknown value on edge' )
				
		assert self.number_of_edges() != 0, "This function has no sense if in the network there aren't edges"
		#setting path
		#only if you would to load from c2 cache, you had to be set cachedict
		if self._name() == 'Weighted' or self._name() == '' or self._name() == 'Dummy' or self._name() =='Dummyweighted':
			if not cachedict and not self.get_keyOnDataset():
				raise Exception("cachedict parameter must be set for generic network (or if you wouldn't you had to set force parameter to True)")
			path = self.filepath
		
		elif self.__class__.__name__ != "WikiNetwork":
			tp = trustlet.helpers.relative_path( self.filepath, 'datasets' )

			if tp:
				path = os.path.join( os.path.split(tp[0])[0], 'shared_datasets', tp[1] )
			else:
				raise IOError("Malformed path of dataset! it must contain 'datasets' folder")
			
		else:
			path = self.filepath
				
		if not cachedict and not self.get_keyOnDataset():
			if self._name() and self.date:
				cachekey = {'network':self._name(),'date':self.date,'function':'reciprocity_matrix'}
			else:
				raise Exception("Error! cachedict not set, and no 'date' attribute on network\n")

			if hasattr( self, "cond_on_edge" ) and self.cond_on_edge:
				cachekey['cond_on_edge']=self.cond_on_edge.__name__ 
							  
		else:
			cachekey = ( cachedict != None and cachedict.copy() ) or self.get_keyOnDataset()
			cachekey['function']='reciprocity_matrix'

		if not path.endswith( '.c2' ): #force file to be a c2
			path += '.c2'

		if not force:		 
			data = trustlet.helpers.load( cachekey, path, fault=False)
			
			if data:				# if data is not false
				return data

		if self.has_discrete_weights:
			table = {}
			levels = self.weights(force=True).keys() #if some other edge has been added, we had to take care about that
			levels.append( 'nr' )#non reciprocated
			
			for v in self.weights().iterkeys():
				line = {}
				#the number of edges that have voted someone level 'v' (we normalize on this value)
				normalization = len([e2 for e0,e1,e2 in self.edges_iter() if str(value_on_edge(e2)) == str(v)])

				if normalization == 0:#that means that there are 0 edges with this value.. so we skip them
					for w in levels:
						line[w] = 0.0
					table[v] = line
					continue

				for w in levels:
					if w != 'nr': #non reciprocated
									   #the number of edges that have voted someone level 'v' and has been voted from someone level 'w'
						line[w] = 1.0 * sum([str(value_on_edge(self.get_edge(e1, e0))) == str(w)
											 for e0,e1,e2 in self.edges_iter()
											 if (self.has_edge(e1, e0) and	   
												 str(value_on_edge(e2)) == str(v))]) / normalization
					else:
						line[w] = 1.0 * len([e2
											 for e0,e1,e2 in self.edges_iter()
											 if (not self.has_edge(e1, e0) and #look at 'not' if nr, the edges hadn't to be reciprocated	 
												 str(value_on_edge(e2)) == str(v))]) / normalization
					
				table[v] = line
				
			if not trustlet.helpers.save( cachekey, table, path ):
				sys.stderr.write( "Warning! save of cache failed\n" )
			
			return table
		else:
			raise Exception( "Not implemented" )


	def get_edge(self,u,v=None):
		XDiGraph.get_edge.__doc__
		
		d = XDiGraph.get_edge(self,u,v)

		if self.values_on_edges:
			if 'color' in d:
				k = 'color'
			elif 'level' in d:
				k = 'level'
			elif 'value' in d:
				k = 'value'
			elif 'distrust' in d:
				k = 'distrust'
			else:
				assert 0,'no key found '+str(d)

			if hasattr(self,'level_map') and self.level_map:
				try:
					return self.level_map[d[k]] # distrust is not in level_map... :(
				except KeyError:
					return d[k]
			else:
				return d[k]

		else:
			return d

class WikiNetwork(WeightedNetwork):
	"""
	Wikipedia Network Handler.
	You must pass to it a string with lang of wikipedia, and a string with the date of the dataset. 
	Optionally:
	dataset: path to a dot file that it will load and save in the dataset folder
	current: Default False use the dataset generated by History xml dump (named graphHistory), if True use the dataset generated by current xml dump
	bots: default False, indicate if you would or not the bots in the network (False == we avoid to include bots in list, True == the bots will be included).
	blockedusers: the same meaning of 'bots', but for blockedusers
	threshold: the minimum weights on edges (1..n)
	silent: if True, the class does not print nothing.

	NB: if you would know what kind of network are hosted on www.trustlet.org invoke getNetworkList() from trustlet.helpers
	"""
	   
	def __init__(self, lang, date, current=False, bots=False, blockedusers=False, base_path = None,
				 dataset = None, 
				 threshold=1, prefix=None, silent=False ):

		WeightedNetwork.__init__(self,base_path=base_path,prefix=prefix,silent=silent)
		
		assert trustlet.helpers.isdate(date),'date: aaaa-mm-dd'
		self.name= 'WikipediaNetwork/'+str(lang)
		self.url = 'http://www.trustlet.org/trustlet_dataset_svn/'
		self.lang = lang
		self.date = date
		self.current = current
		self.threshold = threshold
		self._weights_dictionary = None
		self.__upbound = None
		self.__user_map = None
		self.level_map = None #set in __rescale()

		# booleans for list of special users
		self.blockedusers = blockedusers
		self.bots = bots

		if current:
			self.filename = "graphCurrent.c2"
		else:
			self.filename = "graphHistory.c2"

		base,net = trustlet.helpers.relative_path( self.path, 'datasets' )
		self.path = os.path.join( os.path.split(base)[0], 'shared_datasets', net ) #wiki datasets lies in shared_datasets
		self.path = os.path.join( self.path, lang, date )
		#trustlet.helpers.mkpath(self.path)
		
		self.filepath = os.path.join( self.path, self.filename )

		path,relpath = trustlet.helpers.relative_path( self.filepath, 'shared_datasets' )
		#								   the first value is the name of the file
		self.url = os.path.join( self.url, os.path.split(relpath)[0])

		assert self.load_c2(), 'There isn\'t anything here! ('+self.filepath+')'

		self.__rescale()

	def save_dot(self, encodeAscii=False):
		def edges(e):
			if type(e) is dict:
				for k in e.keys():
					e[k] = str(e[k])
				return e
			else:
				return str(e)

		return self._save_to( write_dot, '.dot', edges, encodeAscii )

	
	def load_dot(self, decodeUtf8=False):
		"""
		load a graph in a dot format.
		we strongly recomend to use c2 format,
		because it implements some cache-mechanism
		and save automatically some important information
		about network (as level_map).
		if you use dot format remember to set your
		level_map before use some methods (as info or reciprocity_matix for example)
		and to set parameter force to True, if you had to elaborate a function with
		this parameter.
		decodeUtf8 = if true, the nodes and the edges will be automatically decoded
					 into utf8, if false it aren't
		return False if fail, else return True.
		"""
		def edges(e):
			if type(e) is dict:
				for k in e.keys():
					e[k] = int(e[k])
				return e
			else:
				return int(e)

		return self._load_from( read_dot, '.dot', edges, decodeUtf8 )


	def load_c2(self):
		"""
		load graph from c2 file.
		automatically called.
		"""

		#load from cache
		if not self.silent:
			print "Reading ", self.filepath
		cachedict = {'network':'Wiki','lang':str(self.lang),'date':str(self.date)}
		if self.threshold > 1:
			cachedict['threshold'] = self.threshold

		#if not bots:
		#	 cachedict['users'] = 'nobots'

		
		pydataset = trustlet.helpers.load(cachedict, self.filepath )
		
		if pydataset == None and self.threshold > 1:
			#try without threshold
			cachedict = {'network':'Wiki','lang':str(self.lang),'date':str(self.date)}
			pydataset = trustlet.helpers.load(cachedict, self.filepath )
			if type(pydataset) is tuple:
			    #calculate manually treshold
				if pydataset:
					edges = pydataset[1]
					edges = filter( lambda x: x[2] >= self.threshold, edges )
					pydataset = (pydataset[0],edges)
			else:
				sys.stderr.write('unrecognized type of network '+str(type(pydataset))+'\n')	
				return False

		if pydataset and type(pydataset) is tuple:
			
			nodes,edges = pydataset
			toU = lambda x: unicode(x) #to unicode
			
			#implement here the nobots control
			cachedict = {'lang':self.lang}
			if not self.bots:
				cachedict['list'] = 'bots'
				botset = trustlet.helpers.load(cachedict, self.filepath )
				if not botset:
					self.bots = True
				self.botset = botset #save botset for future use
			else:
				self.botset = None

			if not self.blockedusers:
				cachedict['list'] = 'blockedusers'
				blockedset = trustlet.helpers.load(cachedict, self.filepath )
				if not blockedset:
					self.blockedusers = True
				self.blockedset = blockedset #save blockset for future use
			else:
				self.blockedset = None
				
			if not self.botset:
				botset = []

			if not self.blockedset:
				blockedset = []

			#begin OPTIMIZATION FUNCTION
			def iterNode():
				#[x for x in nodes if (toU(x) not in botset) and (toU(x) not in blockedset)]
				if botset or blockedset:
					for x in nodes:
						#if bots false x not in botset is always true!
						if (toU(x) not in botset) and (toU(x) not in blockedset):
							yield x
				else:
					for x in nodes:
						yield x

			def iterEdge():
				#[x for x in edges if toU(x[0]) not in botset and toU(x[1]) not in botset and toU(x[0]) not in blockedset and toU(x[1]) not in blockedset]
				if botset or blockedset:
					for x in edges:
						if toU(x[0]) not in botset and toU(x[1]) not in botset and toU(x[0]) not in blockedset and toU(x[1]) not in blockedset:
							yield x
				else:
					for x in edges:
						yield x
			# end OPTIMIZATION FUNCTION

			for u in iterNode():
				self.add_node(u)
			for u,v,e in iterEdge():
				self.add_node(u)
				self.add_node(v)
				self.add_edge( ( u,v,{'value':e} ) )
	   
		else:
			if os.path.exists( self.filepath ):
				print "Warning! the c2 file does not contain the dataset.."
				print "the key used is: ", cachedict
			return False

		return True


	def weights_list(self,force=False):
		"""
		Return a list with the weights of all edges
		"""
		if hasattr(self, "_weights_dictionary") and self._weights_dictionary and not force:
			ws_dict = self._weights_dictionary
		else:
			ws_dict = {}
					
		lendict = len(ws_dict)

		if hasattr(self, "_weights") and self._weights and not force:
			ws = self._weights
		else:
			ws = []
			for n in self.edges_iter():
						
				try:
					x = self.map( float(n[2]['value']) )
				except:
					raise "Cannot read dataset. The edges was malformed.\nThis is a malformed edge:", n
					
				if lendict == 0:
					ws_dict[int(n[2]['value'])] = x
					
				ws.append( x )
							 
			self.level_map = ws_dict
			self._weights_dictionary = ws_dict
			self._weights = ws
		
		return ws

	def weights_dictionary(self):
		"""
		return a dictionary with all the weights in the network
		and it's rescaled value
		"""
		print "Warning! deprecated function. Use weights()"
		return self.weights()

	def upbound(self):
		"""
		return the value greater or equal to the 95% of the edges in the network 
		This value is used to rescale the edges in range 0..1
		"""
		return self.__upbound


	def map(self, value):
		"""
		take a value to rescale in range 0..1
		"""
		from math import log

		if type(value) is str:
			value = int(value)

		#logarithm in base 3 of the value

		if value > self.__upbound:
			return 1.
		else:
			if self.__upbound == 1:
				raise Exception,  "In this network the "+str(UPBOUNDPERCENTAGE)+"% of the users has less than 1 as weight on edges, this network has no meaning" 
			
		try:
			return log( value , 3 ) / log( self.__upbound , 3 )
		except ValueError:
			return 1.0 #workaround

	def __rescale(self):
		"""
		take the _weights field and rescale the value
		"""
		#read upbound
		upbound = trustlet.helpers.load({'network':'Wiki','lang':str(self.lang),'date':str(self.date),'%':UPBOUNDPERCENTAGE}, self.filepath)
		
		if upbound:
			self.__upbound = upbound
		else:
			#create upbound value
			s = sorted( map( lambda x: x[2]['value'] , self.edges() ) )
			wslen = self.number_of_edges()
			maximum = float(wslen) * 5 / 100
			self.__upbound = s[wslen - int(maximum)]
			
		trustlet.helpers.save({'network':'Wiki','lang':str(self.lang),'date':str(self.date),'%':UPBOUNDPERCENTAGE},self.__upbound,self.filepath)

		return self.weights_list()

	def set_upbound(self,up,permanent=False):
		"""
		change the upbound value for this network.
		this modification affected the way in which the edges are rescaled.
		the modification is *not* permanent.
		NB: in order to know what the upbound is, see the doc
			of the method 'upbound'
		"""
		# dangerous! 
		#if not trustlet.helpers.save({'network':'Wiki','lang':str(self.lang),'date':str(self.date),'%':UPBOUNDPERCENTAGE},up,self.filepath):
		#	 sys.stderr.write( "Failed to store the new value! the change will not be permanent." )

		self.__upbound = up
		self.weights_list(force=True) #regen the level_map and the weights_list
		return


	def trust_on_edge(self,edge):
		"""
		return trust on edge passed
		"""
		if type(edge[2]) is int:
			return self.map( edge[2] )

		return self.map( edge[2].values()[0] )

	def ignored_users(self):
		'''
		Users with in_degree and out_degree both equal to 0 aren't returned.
		'''
		return [x for x in self.nodes_iter() if self.out_degree(x) and not self.in_degree(x)]

	def passive_users(self):
		'''
		Users with in_degree and out_degree both equal to 0 aren't returned.
		'''
		return [x for x in self.nodes_iter() if not self.out_degree(x) and self.in_degree(x)]

	
	def plot_weight_edges_histogram(self):
		'''
		Plot the network frequency weights histogram.
		'''
		
		data = {}

		for w in self.edges_iter():
			w = w[2]['value']
			if w in data:
				data[w] += 1
			else:
				data[w] = 1
			
		trustlet.helpers.prettyplot(data.items(),os.path.join(self.path,'weights histogram nolog'),
									xlabel='weights',
									ylabel='frequency',
									title='Frequency weights histogram',
									#log='xy',
									histogram=True)
		if not self.silent:
			print 'Graph saved in',self.path

	def load_distrust(self,onlyLoad=False):
		"""
		This function load the DistrustGraph.c2 if it exist.
		If onlyload is false, the graph is used to correct
		the trust edges present in the network. 
		Else, it will be loaded and added in the network 
		as edges with as weights a dictionary with 'distrust' as key, 
		and a distrust value between 0 and 1.
		"""

		filepath = os.path.join(self.path,'graphDistrust.c2')

		pynet = trustlet.helpers.load({'network':'DistrustWiki','lang':self.lang,'date':self.date}, filepath)
		if not pynet:
			if not self.silent:
				print "Distrust graph doesn't exist"
			return

		nodes,edges = pynet

		if onlyLoad:
			#unuseful, the nodes is already present in the network
			#for n in nodes:
			#	 self.add_node(n)

			for e in edges:
				self.add_node(e[0])
				self.add_node(e[1])
				
				try:
					weight = self.get_edge(e[0],e[1])
				except networkx.NetworkXError:
					weight = {}

				weight['distrust'] = e[2]
				
				self.add_edge(e[0],e[1],weight)

		else:
			#distrust edge
			for de in edges:
				try:
					#trust edge
					te = self.get_edge(de[0],de[1])
				except networkx.NetworkXError:
					#if the edge do not exist, is good
					#because it means that there isn't a trust edge for this distrust edge
					continue
				
				#check!! this algorithm has sense? another algorithm?

				#if the distrust value is higher than trust value, than distrust win
				#we have to correct the network.
				if ( de[2] / 2 ) > te['value']:
					self.delete_edge(de[0],de[1])
				
				


if __name__ == "__main__":
	from trustlet import *
	W = WikiNetwork('fur','2008-06-14')
	W.load_distrust()
