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

print ""
print "Creating graph with controversial users..."
gc = p.graphcontroversiality(indegree=1,toe="mae")

prettyplot( data=gc, path="./WikiPredGraphExamples.gnuplot", title="Level of abs error for each level of controversiality", 
            x_label="controversiality",y_label="abs error", plotnow=True, showlines=True)

print "WikiPredGraphExamples.gnuplot file created"
