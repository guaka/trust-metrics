"""
this module is useful to convert c2 files to pajek format and viceversa.
"""

from networkx.readwrite import read_pajek,write_pajek
import trustlet

def to_c2( pj, c2, key ):
    """
    parse a pajek and save a WeightedNetwork in a c2 file with key `key`

    Parameters:
       pj: path to pajek (ex /home/..../graph.dot)
       c2: path in which save c2 (ex. /home/.../graph.c2)
       key: key of dictionary in c2 that identify the network
       (ex. {'network':'Advogato','date':'2000-01-01'} for Advogato-like network
        and {'network':'Wiki','lang':'it','date':'2000-01-01'} for wiki network)
    """
    try:
        w = read_pajek( pj )
    except:
        return False

    #now I had to delete all key 'value' on all edges
    for edge in w.edges_iter():
        try:
            del edge[2]['value']
        except KeyError:
            continue
    
    return trustlet.helpers.save(key,w,c2)

def from_c2( pj, c2, key, name=None ):
    """
    parse a c2 with key and save a pajek file

    Parameters:
    key: dictionary in this form:
    {'network':'name','date':date}
    if 'network' is has value 'Wiki' (that mean that you want to load a wikinetwork)
    the key must have another value 'lang':'it/fur/la/de.....'
    that specify the language of the network.
    Warning! the value of the key 'network' could not be 'AdvogatoNetwork' it must be 'Advogato' only
    return True
    """
    
    x = trustlet.helpers.load(key,c2,False)
    if not x:
        print "Invalid key"
        return False

    #if c2 contains a list of tuple
    edgekey = trustlet.conv.keyOnEdge(key)
    if not edgekey:
        print "invalid key"
        return False

    w = trustlet.helpers.toNetwork( x, edgekey )
    
    if not w or 'date' not in key:
        print "Incomplete entry in key"
        return False

    if not w.name:
        if hasattr(w,"lang"):
            #then this is a wiki-like network
            w.name = 'wiki_'+key['lang']+'_'+key['date']
        else:
            w.name = key['network']+'_'+key['date']
            
        if name:
            w.name = name

    #now you must add 'value' key on edge, and set it to level_map['value_on_edge']
    for edge in w.edges_iter():
        try:
            edge[2]['value'] = w.level_map[edgekey]
        except:
            print "Warning! output may be incosistent. Level map not defined!!"
            continue

    try:
        write_pajek(w, pj )
    except:
        return False

    return True


#warning to_c2 doesn't work! test
