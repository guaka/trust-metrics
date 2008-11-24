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

    return trustlet.helpers.save(key,w,c2)

def from_c2( pj, c2, key ):
    """
    parse a c2 with key and save a pajek file

    Parameters:
    key: dictionary in this form:
    {'network':'name','date':date}
    if 'network' is has value 'Wiki' (that mean that you want to load a wikinetwork)
    the key must have another value 'lang':'it/fur/la/de.....'
    that specify the language of the network.
    Warning! the value of the key 'network' could not be 'AdvogatoNetwork' it must be 'Advogato' only
    """
    
    w = trustlet.helpers.load(key,c2,False)
    
    if not w:
        return False

    return write_pajek(w, pj )
