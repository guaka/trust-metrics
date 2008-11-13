#!/usr/bin/env python

from trustlet.helpers import *
from trustlet.conversion.dot import to_c2
from trustlet.Dataset.Network import WeightedNetwork
import re
from os.path import abspath

if __name__ == "__main__":
    import sys

    if "-h" in sys.argv or "--help" in sys.argv:
        print "USAGE: ./dot2c2.py filepath_dot [savepath_c2 [date [name]]]"
        exit(0)

    parlen = len(sys.argv )

    if parlen < 2:
        print "Error too few parameter!"
        exit(1)

    dot = sys.argv[1]
    if sys.argv[2:]:
        c2 = sys.argv[2]
    else:
        if dot.endswith('.dot'):
            c2 = dot[:-4] + '.c2'
        else:
            c2 = dot + '.c2'

    date = name = None

    if parlen >= 4:
        date = sys.argv[3]
        if parlen == 5:
            name = sys.argv[4]    

    if not date or not name: 
        redate = re.compile( "[0-9]{4}-[0-9]{2}-[0-9]{2}" )
        rename = re.compile( "([a-z_A-Z])+Network" )
        dot = abspath(dot)
        try:
            date = redate.findall( dot )[0]
            name = rename.findall( dot )[0]
        except IndexError:
            print "Cannot be able to find date and network name in path!"
            print "please set date/name parameter"
            exit(1)

    if to_c2(dot,c2,{'network':name,'date':date}):
        print "C2 correctly generated"
    else:
        print "Error"
