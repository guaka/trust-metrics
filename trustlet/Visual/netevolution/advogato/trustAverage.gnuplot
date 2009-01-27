#!/usr/bin/env gnuplot
# Title: Trust Average on time
# Date: Mon Jan 26 17:24:46 2009
# Network: Advogato
# >>> trustAverage( fromdate, todate, dpath, noObserver=False )

set title "Trust Average on time"
set data style linespoint
set xlabel "date"
set ylabel "trust average"
set xdata time
set timefmt "%Y-%m-%d"
set terminal png
set output "trustAverage.png"
plot "-" using 1:2 title ""
2000-07-18 1.0
2000-08-11 1.0
2002-05-13 1.0
2008-11-16 1.0
2008-12-31 1.0
e
