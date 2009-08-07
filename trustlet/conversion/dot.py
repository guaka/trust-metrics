"""
Module for convert dot files in format c2 (the only readable from trustlet)
and viceversa.
"""

import re
import trustlet
from networkx import read_dot

__all__ = ['to_c2','from_c2']

def to_c2( dot, c2, key ):
    """
    parse a dot and save a WeightedNetwork in a c2 file with key `key`
    NB: work only with dot with Advogato._generic_map edges
        doesn't work with predgraph dot

    Parameters:
       dot: path to dot (ex /home/..../graph.dot)
       c2: path in which save c2 (ex. /home/.../graph.c2)
       key: key of dictionary in c2 that identify the network
       (ex. {'network':'Advogato','date':'2000-01-01'} for Advogato-like network
        and {'network':'Wiki','lang':'it','date':'2000-01-01'} for wiki network)
    """

    ruser = re.compile( '(\w+)' )
    redges = re.compile( '"?(\w+)"?\s*->\s*"?(\w+)"?\s*\[(\w+)="?(\w+)"?\];' )
    w = trustlet.Network.WeightedNetwork()
    
    if trustlet.conv.keyOnEdge(key) != 'value':
        w.level_map = trustlet.Dataset.Advogato._generic_map #contains all the possible value except 'value' that is used only in wikinetwork
        

    f = file( dot )
    lines = []

    for x in f.readlines():
        lines.append( x.strip() ) #clear \x character
        
    f.close()

    if 'digraph' not in lines[0]:
        print "Are you sure this is a dot file?"
        print '(%s)'%lines[0]
        return False

    #delete top and tail
    del lines[0]
    del lines[-1]

    nlines = len(lines)
    chkuser = 0
    chkedges = 0
    chkself = 0
    lnodes = []
    #dict is unashable so I must convert dict in tuple
    wedges = []

    #find all edges
    for j in xrange(nlines):
        res = redges.findall( lines[j] )

        try:
            edges = res[0]
        except IndexError:
            #print lines[j]
            lnodes.append( lines[j] )
            continue

        if type(edges) is tuple:
            indegree = edges[0]
            outdegree = edges[1]
            #skip self edges
            if indegree == outdegree:
                chkself += 1 
                continue

            typeNet = edges[2]
            value = edges[3]

            chkedges += 1
            w.add_edge( indegree, outdegree, trustlet.helpers.pool({typeNet:value}) )
            #only used for checkingfr
            wedges.append( (indegree,outdegree,(typeNet,value)) )
        else:
            print "Warning! output may be checked"

    nlnodes = len(lnodes)

    #find all nodes
    for i in xrange(nlnodes):
        user = ruser.search( lnodes[i] )
        if not user:
            continue
        w.add_node( user.group() )
        chkuser += 1

    if (chkedges+chkuser+chkself) != nlines:
        print "number of edges:",chkedges,"number of self edges:",chkself,"number of users:",chkuser,"number of lines:", nlines
        print "Warning! user+edges+self != number of lines of dot"

    #this is only a check. it slow down the algorithm but maitain the correctness
        
    #check if the dataset is the same as the dataset read with read_dot
    #this check is necessary because we cannot save directly the dataset readed from read_dot for 
    #a pygraphviz bug
    dot = read_dot(dot)
    
    dotnodes = set( dot.nodes() )
    wnodes = set( w.nodes() )
    #make a set of dotedges
    dotedges = set( [(n1,n2,(k,v[k])) for n1,n2,v in dot.edges() for k in v if n1 != n2] )
    #make a set of wedges
    wedges = set( wedges )

    # delete the difference between read_dot result and this algorithm (for edges)
    for e in wedges.difference( dotedges ):
        w.delete_edge(e)

    # delete the difference between read_dot result and this algorithm (for edges)
    for n in wnodes.difference( dotnodes ):
        w.delete_node(n)

    #assert len(dotedges) == w.number_of_edges(), "Error! number of edges different from the dot (dot:"+str(len(dotedges))+",c2:"+str(w.number_of_edges())+")"
    #assert dot.number_of_nodes() == w.number_of_nodes(), "Error! number of nodes different from the dot (dot:"+str(dot.number_of_nodes())+",c2:"+str(w.number_of_nodes())+")"
    
    return trustlet.helpers.save(key,w,c2)


def to_c2_( dot, c2, key ):
    """
    parse a dot and save a WeightedNetwork in a c2 file with key `key`

    Parameters:
       dot: path to dot (ex /home/..../graph.dot)
       c2: path in which save c2 (ex. /home/.../graph.c2)
       key: key of dictionary in c2 that identify the network
       (ex. {'network':'Advogato','date':'2000-01-01'} for Advogato-like network
        and {'network':'Wiki','lang':'it','date':'2000-01-01'} for wiki network)
    """
    
    w = read_dot(dot)

    nodes,edges = trustlet.helpers.toPynetwork(w)

    return trustlet.helpers.save(key,(nodes,edges),c2)


def from_c2( dot, c2, key ):
    """
    parse a c2 with key and save a dot file

    Parameters:
    key: dictionary in this form:
    {'network':'name','date':date}
    if 'network' is has value 'Wiki' (that mean that you want to load a wikinetwork)
    the key must have another value 'lang':'it/fur/la/de.....'
    that specify the language of the network.
    Warning! with the wikiNetwork the conversion could not work.
    Warning! the value of the key 'network' could not be 'AdvogatoNetwork' it must be 'Advogato' only
    """

    w = trustlet.helpers.load( key, c2, fault=False ) #the weighted network stored in c2

    if  not w:
        print "c2 doesn't contain this key! give me the correct key."
        print "if you don't know the key try to use lsc2 script in scripts"
        print "or insert as date the date the dataset, "
        print "and as name the name of the network, like Advogato, Kaitiaki, Wiki.."
        return False

    edgekey = trustlet.conv.keyOnEdge( key )

    if not edgekey:
        print "Invalid key"
        return False

    x = trustlet.helpers.toNetwork( w, edgekey )

    trustlet.write_dot( x, dot )

    return True
