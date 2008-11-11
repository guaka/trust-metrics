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
    '''
    not yet implemented
    '''
    raise NotImplementedError,'try tomorrow'
