#!/usr/bin/env python

from trustlet import *
import os

w = WikiNetwork( 'la', '2008-08-01', current=False)
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


print "The gnuplot and png file were created in", os.path.abspath( "." ), "folder"
prettyplot( gc, "./WikiPredGraphExamples.gnuplot", title="Level of abs error for each level of controversiality", 
            showlines=True, xlabel='controversiality',ylabel='abs error', plotnow=True )

print "WikiPredGraphExamples.gnuplot file created"
