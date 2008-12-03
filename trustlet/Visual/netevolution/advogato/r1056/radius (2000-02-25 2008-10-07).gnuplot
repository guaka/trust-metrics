#!/usr/bin/env gnuplot
# Title: radius
# Date: Wed Dec  3 09:08:50 2008
# eval = nx.radius(networkx.connected_component_subgraphs(G.to_undirected())[0])

set title "radius"
set data style linespoint
set xdata time
set timefmt "%Y-%m-%d"
set terminal png
set output "radius (2000-02-25 2008-10-07).png"
plot "-" using 1:2 title ""
2000-02-25 4
2000-07-18 4
2000-09-28 4
2001-02-13 5
2001-05-07 5
2001-07-16 5
2001-09-15 5
2001-11-23 5
2002-02-02 5
2002-04-08 5
2002-06-21 5
2003-03-04 5
2004-07-05 5
2004-10-28 5
2005-11-11 5
2006-02-11 5
2006-05-20 29
2006-10-01 29
2006-12-01 5
2007-02-01 5
2007-05-01 5
2007-07-01 5
2007-10-13 5
2007-12-12 5
2008-02-10 5
2008-04-10 5
2008-06-09 5
2008-08-08 5
2008-10-07 5
e
