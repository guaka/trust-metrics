#!/usr/bin/env python

from trustlet.helpers import *
from trustlet.Dataset.Network import WeightedNetwork
import re

if __name__ == "__main__":
    import sys

    if "-h" in sys.argv or "--help" in sys.argv:
        print "USAGE: ./dot2c2.py filepath_to_dot savepath_c2 [date,name]"
        exit(0)

    parlen = len(sys.argv )

    if parlen < 3:
        print "Error too few parameter!"
        exit(1)

    dot = sys.argv[1]
    c2 = sys.argv[2]
    date = name = None

    if parlen >= 4:
        date = sys.argv[3]
        if parlen == 5:
            name = sys.argv[4]

    w = dot2c2( dot )

    redate = re.compile( "[0-9]{4}-[0-9]{2}-[0-9]{2}" )
    rename = re.compile( "[a-z_A-Z]+Network" )

    if not date or not name: 
        try:
            date = redate.findall( dot )[0]
            name = rename.findall( dot )[0]
        except IndexError:
            print "Cannot be able to find date and network name in path!"
            print "please set date/name parameter"
            exit(1)

    save( {'network':name,'date':date}, w, path=c2 )

    print "C2 correctly generated"

    exit(0)
