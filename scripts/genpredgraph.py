from trustlet import *
#from trustlet import PredGraph, AdvogatoNetwork
#from trustlet.helpers import get_name, getTrustMetrics, splittask
#from trustlet.trustmetrics import *


def main(net):
    #A = AdvogatoNetwork( download=True, base_path=path )
    if get_name(net) == 'AdvogatoNetwork':
        trustmetrics = getTrustMetrics( net, trivial=True )
    else:
        trustmetrics = getTrustMetrics( net, advogato=False, trivial=True )

    def eval( tm ):
        if hasattr( trustmetrics[tm].dataset, "lang" ):
            P = WikiPredGraph( trustmetrics[tm] )
        else:
            P = PredGraph( trustmetrics[tm] )
        return None
    
    splittask( eval , [tm for tm in trustmetrics], np=4 )
    
    return None


def check( path ):
    from os.path import split

    if split( path )[0] == path:
        return False

    return True

if __name__ == "__main__":
    import sys,re
    from os.path import split

    l = len(sys.argv)

    if l > 1:
        dataset_path = sys.argv[1]
        type_path = date_path = dataset_path
        type = date = split( dataset_path )[1]
    else:
        print "USAGE: python genpredgraph.py dataset_path [lang]"
        exit(0)

    #try to find type of network
    while( check(type_path) and ( re.match( "[a-zA-Z]+Network", type ) == None ) ):
        type_path,type = split(type_path)

    #try to find date
    while( check(date_path) and ( re.match( "[0-9]{4}-[0-9]{2}-[0-9]{2}", date ) == None ) ):
        date_path,date = split(date_path)

    if not check(date_path):
        print "I cannot be able to find date of network in this path!"
        exit(0)

    if not check(type_path):
        print "I cannot be able to find type of network in this path!"
        exit(0)

    if type == "WikiNetwork":
        if l > 2:
            lang = sys.argv[2]
            A = WikiNetwork( lang,date )
        else:
            print "WikiNetwork must have lang!"
            exit(0)
    elif type == "AdvogatoNetwork":
        A = AdvogatoNetwork( date=date )
        
    if  A == None:
        print "I can't be able to open this dataset"
        exit(0)

        
    main(A)
