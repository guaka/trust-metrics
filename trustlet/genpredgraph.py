from trustlet import *
#from trustlet import PredGraph, AdvogatoNetwork
#from trustlet.helpers import get_name, getTrustMetrics, splittask
#from trustlet.trustmetrics import *


def main(net):
    #A = AdvogatoNetwork( download=True, base_path=path )

    trustmetrics = getTrustMetrics( net )

    def eval( tm ):
        P = PredGraph( trustmetrics[tm] )
        return None
    
    splittask( eval , [tm for tm in trustmetrics], np=4 )
    
    return None


if __name__ == "__main__":
    import sys,re
    from os.path import split
    path = sys.argv[1]
    dataset_path = sys.argv[2]
    dataset = dataset_path
    type = split( dataset )[1]

    #try to find type of network
    while( re.match( "[a-zA-Z]+Network", type ) == None ):
        dataset,type = split(dataset)

    if type == "WikiNetwork":
        if len(sys.argv) > 3:
            lang = sys.argv[3]
            date = sys.argv[4]
            A = WikiNetwork( lang,date, dataset=dataset_path )
        else:
            print "you must specify lang and date for wikinetwork!"
            exit(0)
    elif type == "AdvogatoNetwork":
        if len(sys.argv) > 2:
            date = sys.argv[3]
            A = AdvogatoNetwork( date=date )
        else:
            print "you must specify date for advogatonetwork!"
            exit(0)

    if  A == None:
        print "I can't be able to open this dataset"
        exit(0)

        
    main(A)
