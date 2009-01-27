#!/usr/bin/env gnuplot
# Title: avg of standard deviation in received trust (in degree=20)
# Date: Tue Jan 27 16:04:07 2009
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
set output "avg of standard deviation in received trust (in degree=20) (2001-06-08 2004-10-28).png"
plot "-" using 1:2 title ""
2001-06-08 0.0
2001-06-15 0.0
2001-06-21 0.0
2001-06-26 0.0
2001-07-04 0.0
2001-07-10 0.0
2001-07-16 0.0
2001-07-22 0.0
2001-08-04 0.0
2001-08-13 0.0
2001-08-22 0.0
2001-08-30 0.0
2001-09-04 0.0
2001-09-15 0.0
2001-09-22 0.0
2001-09-28 0.0
2001-10-03 0.0
2001-10-06 0.0
2001-10-09 0.0
2001-10-18 0.0
2001-10-29 0.0
2001-11-12 0.0
2001-11-15 0.0
2001-11-23 0.0
2001-11-28 0.0
2001-12-02 0.0
2001-12-10 0.0
2001-12-17 0.0
2001-12-26 0.0
2002-01-05 0.0
2002-01-14 0.0
2002-01-19 0.0
2002-01-23 0.0
2002-01-28 0.0
2002-02-02 0.0
2002-02-06 0.0
2002-02-12 0.0
2002-02-20 0.0
2002-02-27 0.0
2002-03-02 0.0
2002-03-18 0.0
2002-03-22 0.0
2002-03-28 0.0
2002-04-02 0.0
2002-04-08 0.0
2002-04-13 0.0
2002-04-18 0.0
2002-04-25 0.0
2002-05-01 0.0
2002-05-06 0.0
2002-05-13 0.0
2002-05-24 0.0
2002-05-30 0.0
2002-06-06 0.0
2002-06-13 0.0
2002-06-21 0.0
2003-03-04 0.0
2003-03-24 0.0
2003-04-10 0.0
2004-07-05 0.0
2004-10-28 None
e
