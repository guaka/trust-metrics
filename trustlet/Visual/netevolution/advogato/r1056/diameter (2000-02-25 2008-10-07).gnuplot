#!/usr/bin/env gnuplot
# Title: diameter
# Date: Wed Dec  3 09:08:50 2008
# eval = nx.diameter(networkx.connected_component_subgraphs(G.to_undirected())[0])

set title "diameter"
set data style linespoint
set xdata time
set timefmt "%Y-%m-%d"
set terminal png
set output "diameter (2000-02-25 2008-10-07).png"
plot "-" using 1:2 title ""
2000-02-25 6
2000-07-18 7
2000-09-28 8
2001-02-13 8
2001-05-07 9
2001-07-16 9
2001-09-15 9
2001-11-23 9
2002-02-02 9
2002-04-08 9
2002-06-21 9
2003-03-04 9
2004-07-05 9
2004-10-28 9
2005-11-11 9
2006-02-11 9
2006-05-20 36
2006-10-01 36
2006-12-01 9
2007-02-01 9
2007-05-01 9
2007-07-01 9
2007-10-13 9
2007-12-12 9
2008-02-10 9
2008-04-10 9
2008-06-09 9
2008-08-08 9
2008-10-07 9
e
