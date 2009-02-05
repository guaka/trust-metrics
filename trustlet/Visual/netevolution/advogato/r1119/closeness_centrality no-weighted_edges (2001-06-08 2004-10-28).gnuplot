#!/usr/bin/env gnuplot
# Title: closeness_centrality no-weighted_edges
# Date: Wed Feb  4 05:51:15 2009
# eval = avg(nx.closeness_centrality(G,weighted_edges=False).values())

set title "closeness_centrality no-weighted_edges"
set data style linespoint
set xdata time
set timefmt "%Y-%m-%d"
set terminal png
set output "closeness_centrality no-weighted_edges (2001-06-08 2004-10-28).png"
plot "-" using 1:2 title ""
2001-06-08 0.193255338041
2001-06-15 0.194206241593
2001-06-21 0.194834223594
2001-06-26 0.194558857914
2001-07-04 0.194732771847
2001-07-10 0.194012881276
2001-07-16 0.193938092084
2001-07-22 0.193407140928
2001-08-04 0.194395830407
2001-08-13 0.194374238491
2001-08-22 0.194665819396
2001-08-30 0.19421522269
2001-09-04 0.194096572528
2001-09-15 0.193599053815
2001-09-22 0.193622938419
2001-09-28 0.193711055948
2001-10-03 0.192959090476
2001-10-06 0.193205982651
2001-10-09 0.193628597653
2001-10-18 0.193136343355
2001-10-29 0.19347915176
2001-11-12 0.193319716872
2001-11-15 0.193208969585
2001-11-23 0.193169437337
2001-11-28 0.192808257685
2001-12-02 0.192963585375
2001-12-10 0.192069320394
2001-12-17 0.19179635357
2001-12-26 0.191571395877
2002-01-05 0.191076995597
2002-01-14 0.190959068506
2002-01-19 0.1909664707
2002-01-23 0.190854073304
2002-01-28 0.190381712631
2002-02-02 0.190169218195
2002-02-06 0.189933800938
2002-02-12 0.189897317888
2002-02-20 0.190321009322
2002-02-27 0.190313470897
2002-03-02 0.190551474471
2002-03-18 0.190270383611
2002-03-22 0.190302579782
2002-03-28 0.190182585065
2002-04-02 0.189941956714
2002-04-08 0.190113813605
2002-04-13 0.189388092987
2002-04-18 0.188836213532
2002-04-25 0.188975802563
2002-05-01 0.188811971938
2002-05-06 0.188684042824
2002-05-13 0.188476272247
2002-05-24 0.18839975695
2002-05-30 0.18836232301
2002-06-06 0.188682128951
2002-06-13 0.188555507785
2002-06-21 0.18848659959
2003-03-04 0.184223069629
2003-03-24 0.183523467293
2003-04-10 0.183116236484
2004-07-05 0.177910823976
2004-10-28 0.0651902867158
e
