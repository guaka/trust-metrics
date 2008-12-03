#!/usr/bin/env gnuplot
# Title: avg of standard deviation in received trust (in degree=20)
# Date: Wed Dec  3 09:08:51 2008
# cont = [] # controversiality array
# 
# for n in K.nodes_iter():
#     in_edges = K.in_edges(n)
# 
#     # min_in_degree -> written in name of function
#     if len(in_edges)<min_in_degree:
#         continue
# 
#     cont.append(
#         numpy.std([_obs_app_jour_mas_map[x[2]['level']] for x in in_edges])
#     )
# 
# return avg(cont)

set title "avg of standard deviation in received trust (in degree=20)"
set data style linespoint
set xdata time
set timefmt "%Y-%m-%d"
set terminal png
set output "avg of standard deviation in received trust (in degree=20) (2000-02-25 2008-10-07).png"
plot "-" using 1:2 title ""
2000-02-25 0.0801850688611
2000-07-18 0.101372414546
2000-09-28 0.101818435306
2001-02-13 0.109058454597
2001-05-07 0.114272182387
2001-07-16 0.115474703475
2001-09-15 0.119933041106
2001-11-23 0.122687002694
2002-02-02 0.123478428388
2002-04-08 0.124146908111
2002-06-21 0.125081218589
2003-03-04 0.130692568567
2004-07-05 0.135985301749
2004-10-28 0.13629712542
2005-11-11 0.135177322975
2006-02-11 0.129485041554
2006-05-20 0.129383514733
2006-10-01 0.128278719585
2006-12-01 0.137947269158
2007-02-01 0.137594184248
2007-05-01 0.137817449191
2007-07-01 0.135974885517
2007-10-13 0.136080899096
2007-12-12 0.136331544886
2008-02-10 0.136565707937
2008-04-10 0.136535472372
2008-06-09 0.136476337342
2008-08-08 0.136299685457
2008-10-07 0.13600252239
e
