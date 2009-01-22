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
    if 'lang' in key:
        print "Wikinetwork not supported yet."
        return False

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

def from_c2( pj, c2, key, name=None, wikiHistory=True ):
    """
    parse a c2 with key and save a pajek file

    Parameters:
    key: dictionary in this form:
    {'network':'name','date':date}
    if 'network' is has value 'Wiki' (that mean that you want to load a wikinetwork)
    the key must have another value 'lang':'it/fur/la/de.....', and if you want convert 'current' wiki
    you have to set wikiHistory parameter to False. This parameter is ignored if the network is not wiki.
    that specify the language of the network.
    Warning! the value of the key 'network' could not be 'AdvogatoNetwork' it must be 'Advogato' only
    return True
    """
    
    if 'date' not in key:
        print "'date' not present in key!"
        return False

    edgekey = trustlet.conv.keyOnEdge(key)
    
    if not edgekey:
        print "invalid key"
        return False

    if "lang" in key:
        if wikiHistory:
            w = trustlet.Dataset.Network.WikiNetwork( date=key['date'], lang=key['lang'] )
        else:
            w = trustlet.Dataset.Network.WikiNetwork( date=key['date'], lang=key['lang'], current=True )

        wiki = True
    else:
        wiki = False
        
        if 'network' in key:
            if key['network'] == 'Advogato':
                w = trustlet.Dataset.Advogato.AdvogatoNetwork( date=key['date'] )
            elif key['network'] == 'Kaitiaki':
                w = trustlet.Dataset.Advogato.KaitiakiNetwork( date=key['date'] )
            elif key['network'] == 'Squeakfoundation':
                w = trustlet.Dataset.Advogato.SqueakfoundationNetwork( date=key['date'] )
            elif key['network'] == 'Robots_net':
                w = trustlet.Dataset.Advogato.Robots_netNetwork( date=key['date'] )
            else:
                x = trustlet.helpers.load(key,c2,False)
                if not x:
                    print "Invalid key"
                    return False
                
                w = trustlet.helpers.toNetwork( x, edgekey )
        
        else:
            print "'network' not present in key!"
            return False

    if not w: #unnecessary control if wiki
        print "Incomplete entry in key"
        return False

    if not w.name:
        if wiki:
            #then this is a wiki-like network
            w.name = 'wiki_'+key['lang']+'_'+key['date']
        else:
            w.name = key['network']+'_'+key['date']
            
        if name:
            w.name = name
    """
    #now you must add 'value' key on edge, and set it to level_map['value_on_edge'] (useful for pajek?)
    if hasattr( w, "level_map" ) and (w.level_map != None):
        for edge in w.edges(): #I can't use edges_iter because I modify the edge during loop
            w.delete_edge( edge[0], edge[1] )
            
            edge0 = str( ''.join( map( lambda x: ((ord(x)<127) and x or '?' ) , edge[0]  ) ) ) #avoid Unicode encode Error
            edge1 = str( ''.join( map( lambda x: ((ord(x)<127) and x or '?' ) , edge[1] ) ) )

            if wiki:
                keyvalue = 'rescaled'
            else:
                keyvalue = 'value'
            #                              keyvalue is a numeric value (useful for pajek)  edgekey is the real value on edge in network (can be a string)
            w.add_edge( edge0, edge1, {keyvalue:w.level_map[edge[2].values()[0]],edgekey:edge[2].values()[0]} )
    """
    try:
        write_pajek( w, pj )
    except IOError:
        print "Error! path ",pj,"could not exists! check it."
        return False
    except UnicodeEncodeError:
        print "Decoding to utf-8 failed!"
        return False
    except:
        print "Error while trying to write network! exiting"
        return False

    return True


#warning from_c2 doesn't work! load of a c2 converted doesn't work (even if c2 is correct O.o)
