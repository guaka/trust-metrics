#!/usr/bin/env gnuplot
# Title: number_connected_components
# Date: Wed Dec  3 09:08:51 2008
# eval = nx.number_connected_components(G.to_undirected())

set title "number_connected_components"
set data style linespoint
set xdata time
set timefmt "%Y-%m-%d"
set terminal png
set output "number_connected_components (2000-02-25 2008-10-07).png"
plot "-" using 1:2 title ""
2000-02-25 22
2000-07-18 200
2000-09-28 380
2001-02-13 557
2001-05-07 638
2001-07-16 698
2001-09-15 743
2001-11-23 801
2002-02-02 857
2002-04-08 915
2002-06-21 976
2003-03-04 1178
2004-07-05 1579
2004-10-28 12719
2005-11-11 14140
2006-02-11 14777
2006-05-20 15286
2006-10-01 7941
2006-12-01 7681
2007-02-01 7745
2007-05-01 7847
2007-07-01 7923
2007-10-13 8050
2007-12-12 8125
2008-02-10 8223
2008-04-10 8274
2008-06-09 8337
2008-08-08 8359
2008-10-07 8384
e
