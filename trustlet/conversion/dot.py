"""
Module for convert dot files in format c2 (the only readable from trustlet)
and viceversa.
"""

import re
import trustlet

def to_c2( dot, c2, key ):
    """
    parse a dot and save a WeightedNetwork in a c2 file with key `key`
    """
    
    ruser = re.compile( "[^ \/*]+" )
    redges = re.compile( '([^ ]+) -> ([^ ]+) \[([a-z]+)=\"([A-Za-z]+)\"\];' )
    w = trustlet.Network.WeightedNetwork()

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

    #find all nodes
    for i in xrange(nlines):
        user = ruser.findall( lines[i] )[0]
        w.add_node( user )
        #find all edges
        for j in xrange(i+1,nlines):
            res = redges.findall( lines[j] )
            
            try:
                edges = res[0]
            except IndexError:
                break
            
            if type(edges) is tuple:
                indegree = edges[0]
                outdegree = edges[1]
                typeNet = edges[2]
                value = edges[3]
                
                w.add_edge(indegree, outdegree, trustlet.helpers.pool({typeNet:value}) )
            else:
                print "Warning! output may be checked"

    return trustlet.helpers.save(key,w,c2)

def from_c2( dot, c2, key ):
    """
    parse a c2 with key and save a dot file
    parameters:
    key: dictionary in this form:
    {'network':'name','date':date}
    if 'network' is has value 'Wiki' (that mean that you want to load a wikinetwork)
    the key must have another value 'lang':'it/fur/la/de.....'
    that specify the language of the network.
    Warning! with the wikiNetwork the conversion could not work.
    """

    w = trustlet.helpers.load( key, c2, fault=False ) #the weighted network stored in c2

    if  not w:
        print "c2 doesn't contain this key! give me the correct key."
        print "if you don't know the key try to use lsc2 script in scripts"
        print "or insert as date the date the dataset, "
        print "and as name the name of the network, like Advogato, Kaitiaki, Wiki.."
        return False

    x = trustlet.helpers.toNetwork( w )

    trustlet.write_dot( x, dot )

    return True

