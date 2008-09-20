#!/usr/bin/env python

from trustlet import *

w = WikiNetwork( 'la', '2008-07-12', current=True)
tm = TrustMetric( w , ebay_tm )
p = WikiPredGraph( tm )

print "Info:"
print ""
print p.info()

print ""
print "abs error of trust metric 'ebay': ", p.abs_error()
print "sqr error of trust metric 'ebay': ", p.sqr_error()
