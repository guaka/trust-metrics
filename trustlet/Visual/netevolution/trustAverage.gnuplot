#!/usr/bin/env gnuplot
# Title: Trust Average on time
# Date: Wed Aug 13 19:45:14 2008
# Network: Advogato
# >>> trustAverage( fromdate, todate, path, noObserver=False )

set title "Trust Average on time"
set data style linespoint
set xlabel "date in seconds"
set ylabel "trust average"
set xdata time
set timefmt "%Y-%m-%d"
set terminal png
set output "trustAverage.png"
plot "-" using 1:2 title ""
2006-10-01 0.815744566676
e
