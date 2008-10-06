#!/usr/bin/env gnuplot
# Title: Level distribution
# Date: Thu Sep 25 18:05:00 2008
# Network: Advogato
# >>> plot_level_distribution(level_distribution(...))

set title "Level distribution"
set data style linespoint
set xlabel "dates (from 2007-12-14 to 2008-09-24)"
set ylabel "percentage of edges"
set xdata time
set timefmt "%Y-%m-%d"
set terminal png
set output "level distribution (2007-12-14 2008-09-24).png"
plot "-" using 1:2 title "Master", "-" using 1:2 title "Journeyer", "-" using 1:2 title "Apprentice", "-" using 1:2 title "Observer"
2007-12-14 0.343106180666
2007-12-15 0.343106180666
2007-12-16 0.343106180666
2007-12-17 0.343106180666
2007-12-18 0.343106180666
2007-12-19 0.343106180666
2007-12-20 0.343106180666
2007-12-21 0.343106180666
2007-12-22 0.343106180666
2007-12-23 0.343106180666
2007-12-24 0.343106180666
2007-12-25 0.34297029703
2007-12-26 0.34297029703
2007-12-27 0.343626286619
2007-12-28 0.343626286619
2007-12-29 0.343626286619
2007-12-30 0.343626286619
2007-12-31 0.343626286619
2008-01-01 0.343626286619
2008-01-02 0.343626286619
2008-01-03 0.343490304709
2008-01-04 0.343490304709
2008-01-05 0.343490304709
2008-01-06 0.343490304709
2008-01-07 0.343490304709
2008-01-08 0.343490304709
2008-01-09 0.343601895735
2008-01-10 0.343601895735
2008-01-11 0.343330702447
2008-01-12 0.343330702447
2008-01-13 0.343330702447
2008-01-14 0.343330702447
2008-01-15 0.343330702447
2008-01-16 0.343330702447
2008-01-17 0.340714840715
2008-01-18 0.34043377227
2008-01-19 0.340891621829
2008-01-20 0.340760660776
2008-01-21 0.340629800307
2008-01-22 0.340629800307
2008-01-23 0.341013824885
2008-01-24 0.340882917466
2008-01-25 0.340882917466
2008-01-26 0.340882917466
2008-01-27 0.341004986575
2008-01-28 0.341257668712
2008-01-29 0.341257668712
2008-01-30 0.341257668712
2008-01-31 0.340865568748
2008-02-01 0.340865568748
2008-02-02 0.340865568748
2008-02-03 0.340865568748
2008-02-04 0.340865568748
2008-02-05 0.340482573727
2008-02-06 0.340482573727
2008-02-07 0.340352220521
2008-02-08 0.340352220521
2008-02-10 0.340352220521
2008-02-11 0.340352220521
2008-02-12 0.340352220521
2008-02-13 0.340221967088
2008-02-14 0.340221967088
2008-02-15 0.340221967088
2008-02-16 0.340221967088
2008-02-17 0.340221967088
2008-02-18 0.340221967088
2008-02-19 0.340221967088
2008-02-20 0.340221967088
2008-02-21 0.341212352268
2008-02-22 0.341834792539
2008-02-23 0.341834792539
2008-02-24 0.341834792539
2008-02-25 0.340917709518
2008-02-26 0.34053030303
2008-02-27 0.341105678827
2008-02-28 0.340721262209
2008-02-29 0.340593315809
2008-03-01 0.340593315809
2008-03-02 0.34107946027
2008-03-03 0.34043348281
2008-03-04 0.34043348281
2008-03-05 0.34043348281
2008-03-06 0.34043348281
2008-03-07 0.340306313037
2008-03-08 0.340306313037
2008-03-09 0.340306313037
2008-03-10 0.340306313037
2008-03-11 0.340552651232
2008-03-12 0.340425531915
2008-03-13 0.340425531915
2008-03-14 0.340425531915
2008-03-15 0.340425531915
2008-03-16 0.340425531915
2008-03-17 0.340425531915
2008-03-18 0.340425531915
2008-03-19 0.340425531915
2008-03-20 0.340425531915
2008-03-21 0.340425531915
2008-03-22 0.340425531915
2008-03-23 0.340298507463
2008-03-24 0.340298507463
2008-03-25 0.340298507463
2008-03-26 0.340298507463
2008-03-27 0.340298507463
2008-03-28 0.340298507463
2008-03-29 0.340298507463
2008-03-30 0.340298507463
2008-03-31 0.340298507463
2008-04-01 0.340298507463
2008-04-02 0.340298507463
2008-04-03 0.340298507463
2008-04-04 0.340298507463
2008-04-06 0.340298507463
2008-04-07 0.340298507463
2008-04-08 0.340298507463
2008-04-09 0.340298507463
2008-04-10 0.340298507463
2008-04-11 0.340298507463
2008-04-12 0.340298507463
2008-04-13 0.340298507463
2008-04-14 0.340298507463
2008-04-15 0.340298507463
2008-04-16 0.340298507463
2008-04-17 0.340298507463
2008-04-18 0.340298507463
2008-04-19 0.339918002236
2008-04-20 0.339791356185
2008-04-21 0.339791356185
2008-04-22 0.339791356185
2008-04-23 0.339791356185
2008-04-24 0.339791356185
2008-04-25 0.339791356185
2008-04-26 0.339791356185
2008-04-27 0.339791356185
2008-04-28 0.339791356185
2008-04-29 0.339791356185
2008-04-30 0.340037243948
2008-05-01 0.340037243948
2008-05-02 0.339910647803
2008-05-03 0.339910647803
2008-05-04 0.339910647803
2008-05-05 0.339910647803
2008-05-06 0.339910647803
2008-05-07 0.339910647803
2008-05-08 0.339910647803
2008-05-09 0.339910647803
2008-05-10 0.339910647803
2008-05-11 0.339910647803
2008-05-12 0.339910647803
2008-05-13 0.339910647803
2008-05-14 0.34015630815
2008-05-15 0.34015630815
2008-05-16 0.34015630815
2008-05-17 0.34015630815
2008-05-18 0.34015630815
2008-05-19 0.34015630815
2008-05-20 0.34015630815
2008-05-21 0.34015630815
2008-05-22 0.341145833333
2008-05-23 0.341145833333
2008-05-24 0.341145833333
2008-05-25 0.341145833333
2008-05-26 0.341145833333
2008-05-27 0.341145833333
2008-05-28 0.341145833333
2008-05-29 0.341145833333
2008-05-30 0.341145833333
2008-05-31 0.341145833333
2008-06-01 0.341635687732
2008-06-02 0.341635687732
2008-06-03 0.341635687732
2008-06-04 0.341508732813
2008-06-05 0.341508732813
2008-06-06 0.341508732813
2008-06-07 0.341508732813
2008-06-08 0.341508732813
2008-06-09 0.341508732813
2008-06-10 0.341508732813
2008-06-11 0.341508732813
2008-06-12 0.341508732813
2008-06-13 0.341508732813
2008-06-14 0.341508732813
2008-06-15 0.341508732813
2008-06-16 0.341508732813
2008-06-17 0.341508732813
2008-06-18 0.341508732813
2008-06-19 0.341508732813
2008-06-20 0.341508732813
2008-06-21 0.341508732813
2008-06-22 0.341508732813
2008-06-23 0.341508732813
2008-06-24 0.341508732813
2008-06-25 0.341508732813
2008-06-26 0.341508732813
2008-06-27 0.341508732813
2008-06-28 0.341508732813
2008-06-29 0.341508732813
2008-06-30 0.341508732813
2008-07-01 0.341508732813
2008-07-02 0.341508732813
2008-07-03 0.341508732813
2008-07-04 0.341508732813
2008-07-05 0.341508732813
2008-07-06 0.341508732813
2008-07-07 0.341508732813
2008-07-08 0.341508732813
2008-07-09 0.341508732813
2008-07-10 0.341508732813
2008-07-11 0.341508732813
2008-07-12 0.341508732813
2008-07-13 0.341508732813
2008-07-14 0.341508732813
2008-07-15 0.341508732813
2008-07-16 0.341508732813
2008-07-17 0.341508732813
2008-07-18 0.341381872214
2008-07-19 0.341381872214
2008-07-21 0.341381872214
2008-07-22 0.341381872214
2008-07-23 0.341381872214
2008-07-24 0.341381872214
2008-07-25 0.341381872214
2008-07-26 0.341381872214
2008-07-27 0.341381872214
2008-07-28 0.341381872214
2008-07-29 0.341381872214
2008-07-30 0.341381872214
2008-07-31 0.341381872214
2008-08-01 0.341381872214
2008-08-02 0.341381872214
2008-08-03 0.341381872214
2008-08-04 0.341381872214
2008-08-05 0.341381872214
2008-08-06 0.341381872214
2008-08-07 0.341381872214
2008-08-08 0.341381872214
2008-08-09 0.341381872214
2008-08-10 0.341381872214
2008-08-11 0.341381872214
2008-08-12 0.341381872214
2008-08-13 0.341381872214
2008-08-14 0.341381872214
2008-08-15 0.341381872214
2008-08-16 0.341381872214
2008-08-17 0.341381872214
2008-08-18 0.341381872214
2008-08-19 0.341381872214
2008-08-20 0.341381872214
2008-08-21 0.341381872214
2008-08-22 0.341381872214
2008-08-23 0.341381872214
2008-08-24 0.341381872214
2008-08-25 0.341381872214
2008-08-26 0.341381872214
2008-08-27 0.341381872214
2008-08-29 0.341381872214
2008-08-30 0.341381872214
2008-08-31 0.341381872214
2008-09-01 0.341381872214
2008-09-02 0.34125510583
2008-09-03 0.34125510583
2008-09-04 0.341499628805
2008-09-05 0.341499628805
2008-09-06 0.341499628805
2008-09-07 0.341499628805
2008-09-08 0.341499628805
2008-09-09 0.341499628805
2008-09-10 0.341499628805
2008-09-11 0.341499628805
2008-09-13 0.341499628805
2008-09-14 0.341499628805
2008-09-15 0.341499628805
2008-09-16 0.341499628805
2008-09-17 0.341499628805
2008-09-18 0.341499628805
2008-09-19 0.341499628805
2008-09-20 0.341499628805
2008-09-21 0.341372912801
2008-09-22 0.341372912801
2008-09-23 0.341372912801
2008-09-24 0.341372912801
e
2007-12-14 0.32765451664
2007-12-15 0.32765451664
2007-12-16 0.32765451664
2007-12-17 0.32765451664
2007-12-18 0.32765451664
2007-12-19 0.32765451664
2007-12-20 0.32765451664
2007-12-21 0.32765451664
2007-12-22 0.32765451664
2007-12-23 0.32765451664
2007-12-24 0.32765451664
2007-12-25 0.327920792079
2007-12-26 0.327920792079
2007-12-27 0.327395091053
2007-12-28 0.327395091053
2007-12-29 0.327395091053
2007-12-30 0.327395091053
2007-12-31 0.327395091053
2008-01-01 0.327395091053
2008-01-02 0.327395091053
2008-01-03 0.327265532252
2008-01-04 0.327265532252
2008-01-05 0.327265532252
2008-01-06 0.327265532252
2008-01-07 0.327265532252
2008-01-08 0.327265532252
2008-01-09 0.327804107425
2008-01-10 0.327804107425
2008-01-11 0.327940015785
2008-01-12 0.327940015785
2008-01-13 0.327940015785
2008-01-14 0.327940015785
2008-01-15 0.327940015785
2008-01-16 0.327940015785
2008-01-17 0.334498834499
2008-01-18 0.334624322231
2008-01-19 0.336664104535
2008-01-20 0.336918939685
2008-01-21 0.337173579109
2008-01-22 0.337173579109
2008-01-23 0.336789554531
2008-01-24 0.337044145873
2008-01-25 0.337044145873
2008-01-26 0.337044145873
2008-01-27 0.337169159954
2008-01-28 0.337039877301
2008-01-29 0.337039877301
2008-01-30 0.337039877301
2008-01-31 0.336652623516
2008-02-01 0.336652623516
2008-02-02 0.336652623516
2008-02-03 0.336652623516
2008-02-04 0.336652623516
2008-02-05 0.337035618537
2008-02-06 0.337035618537
2008-02-07 0.336906584992
2008-02-08 0.336906584992
2008-02-10 0.336906584992
2008-02-11 0.336906584992
2008-02-12 0.336906584992
2008-02-13 0.33677765021
2008-02-14 0.33677765021
2008-02-15 0.33677765021
2008-02-16 0.33677765021
2008-02-17 0.33677765021
2008-02-18 0.33677765021
2008-02-19 0.33677765021
2008-02-20 0.33677765021
2008-02-21 0.336256195196
2008-02-22 0.336124857252
2008-02-23 0.336124857252
2008-02-24 0.336124857252
2008-02-25 0.334470989761
2008-02-26 0.334090909091
2008-02-27 0.335840541557
2008-02-28 0.335462058603
2008-02-29 0.335711603455
2008-03-01 0.335711603455
2008-03-02 0.335457271364
2008-03-03 0.335949177877
2008-03-04 0.335949177877
2008-03-05 0.335949177877
2008-03-06 0.335949177877
2008-03-07 0.335823683227
2008-03-08 0.335823683227
2008-03-09 0.335823683227
2008-03-10 0.335823683227
2008-03-11 0.3356982823
2008-03-12 0.335572974991
2008-03-13 0.335572974991
2008-03-14 0.335572974991
2008-03-15 0.335572974991
2008-03-16 0.335572974991
2008-03-17 0.335572974991
2008-03-18 0.335572974991
2008-03-19 0.335572974991
2008-03-20 0.335572974991
2008-03-21 0.335572974991
2008-03-22 0.335572974991
2008-03-23 0.335447761194
2008-03-24 0.335447761194
2008-03-25 0.335447761194
2008-03-26 0.335447761194
2008-03-27 0.335447761194
2008-03-28 0.335447761194
2008-03-29 0.335447761194
2008-03-30 0.335447761194
2008-03-31 0.335447761194
2008-04-01 0.335447761194
2008-04-02 0.335447761194
2008-04-03 0.335447761194
2008-04-04 0.335447761194
2008-04-06 0.335447761194
2008-04-07 0.335447761194
2008-04-08 0.335447761194
2008-04-09 0.335447761194
2008-04-10 0.335447761194
2008-04-11 0.335447761194
2008-04-12 0.335447761194
2008-04-13 0.335447761194
2008-04-14 0.335447761194
2008-04-15 0.335447761194
2008-04-16 0.335447761194
2008-04-17 0.335447761194
2008-04-18 0.335447761194
2008-04-19 0.335445396944
2008-04-20 0.335320417288
2008-04-21 0.335320417288
2008-04-22 0.335320417288
2008-04-23 0.335320417288
2008-04-24 0.335320417288
2008-04-25 0.335320417288
2008-04-26 0.335320417288
2008-04-27 0.335320417288
2008-04-28 0.335320417288
2008-04-29 0.335320417288
2008-04-30 0.335195530726
2008-05-01 0.335195530726
2008-05-02 0.335443037975
2008-05-03 0.335443037975
2008-05-04 0.335443037975
2008-05-05 0.335443037975
2008-05-06 0.335443037975
2008-05-07 0.335443037975
2008-05-08 0.335443037975
2008-05-09 0.335443037975
2008-05-10 0.335443037975
2008-05-11 0.335443037975
2008-05-12 0.335443037975
2008-05-13 0.335443037975
2008-05-14 0.335318198735
2008-05-15 0.335318198735
2008-05-16 0.335318198735
2008-05-17 0.335318198735
2008-05-18 0.335318198735
2008-05-19 0.335318198735
2008-05-20 0.335318198735
2008-05-21 0.335318198735
2008-05-22 0.334821428571
2008-05-23 0.334821428571
2008-05-24 0.334821428571
2008-05-25 0.334821428571
2008-05-26 0.334821428571
2008-05-27 0.334821428571
2008-05-28 0.334821428571
2008-05-29 0.334821428571
2008-05-30 0.334821428571
2008-05-31 0.334821428571
2008-06-01 0.334572490706
2008-06-02 0.334572490706
2008-06-03 0.334572490706
2008-06-04 0.334448160535
2008-06-05 0.334448160535
2008-06-06 0.334448160535
2008-06-07 0.334448160535
2008-06-08 0.334448160535
2008-06-09 0.334448160535
2008-06-10 0.334448160535
2008-06-11 0.334448160535
2008-06-12 0.334448160535
2008-06-13 0.334448160535
2008-06-14 0.334448160535
2008-06-15 0.334448160535
2008-06-16 0.334448160535
2008-06-17 0.334448160535
2008-06-18 0.334448160535
2008-06-19 0.334448160535
2008-06-20 0.334448160535
2008-06-21 0.334448160535
2008-06-22 0.334448160535
2008-06-23 0.334448160535
2008-06-24 0.334448160535
2008-06-25 0.334448160535
2008-06-26 0.334448160535
2008-06-27 0.334448160535
2008-06-28 0.334448160535
2008-06-29 0.334448160535
2008-06-30 0.334448160535
2008-07-01 0.334448160535
2008-07-02 0.334448160535
2008-07-03 0.334448160535
2008-07-04 0.334448160535
2008-07-05 0.334448160535
2008-07-06 0.334448160535
2008-07-07 0.334448160535
2008-07-08 0.334448160535
2008-07-09 0.334448160535
2008-07-10 0.334448160535
2008-07-11 0.334448160535
2008-07-12 0.334448160535
2008-07-13 0.334448160535
2008-07-14 0.334448160535
2008-07-15 0.334448160535
2008-07-16 0.334448160535
2008-07-17 0.334448160535
2008-07-18 0.334323922734
2008-07-19 0.334323922734
2008-07-21 0.334323922734
2008-07-22 0.334323922734
2008-07-23 0.334323922734
2008-07-24 0.334323922734
2008-07-25 0.334323922734
2008-07-26 0.334323922734
2008-07-27 0.334323922734
2008-07-28 0.334323922734
2008-07-29 0.334323922734
2008-07-30 0.334323922734
2008-07-31 0.334323922734
2008-08-01 0.334323922734
2008-08-02 0.334323922734
2008-08-03 0.334323922734
2008-08-04 0.334323922734
2008-08-05 0.334323922734
2008-08-06 0.334323922734
2008-08-07 0.334323922734
2008-08-08 0.334323922734
2008-08-09 0.334323922734
2008-08-10 0.334323922734
2008-08-11 0.334323922734
2008-08-12 0.334323922734
2008-08-13 0.334323922734
2008-08-14 0.334323922734
2008-08-15 0.334323922734
2008-08-16 0.334323922734
2008-08-17 0.334323922734
2008-08-18 0.334323922734
2008-08-19 0.334323922734
2008-08-20 0.334323922734
2008-08-21 0.334323922734
2008-08-22 0.334323922734
2008-08-23 0.334323922734
2008-08-24 0.334323922734
2008-08-25 0.334323922734
2008-08-26 0.334323922734
2008-08-27 0.334323922734
2008-08-29 0.334323922734
2008-08-30 0.334323922734
2008-08-31 0.334323922734
2008-09-01 0.334323922734
2008-09-02 0.334571110286
2008-09-03 0.334571110286
2008-09-04 0.334446919079
2008-09-05 0.334446919079
2008-09-06 0.334446919079
2008-09-07 0.334446919079
2008-09-08 0.334446919079
2008-09-09 0.334446919079
2008-09-10 0.334446919079
2008-09-11 0.334446919079
2008-09-13 0.334446919079
2008-09-14 0.334446919079
2008-09-15 0.334446919079
2008-09-16 0.334446919079
2008-09-17 0.334446919079
2008-09-18 0.334446919079
2008-09-19 0.334446919079
2008-09-20 0.334446919079
2008-09-21 0.334693877551
2008-09-22 0.334693877551
2008-09-23 0.334693877551
2008-09-24 0.334693877551
e
2007-12-14 0.319334389857
2007-12-15 0.319334389857
2007-12-16 0.319334389857
2007-12-17 0.319334389857
2007-12-18 0.319334389857
2007-12-19 0.319334389857
2007-12-20 0.319334389857
2007-12-21 0.319334389857
2007-12-22 0.319334389857
2007-12-23 0.319334389857
2007-12-24 0.319334389857
2007-12-25 0.319207920792
2007-12-26 0.319207920792
2007-12-27 0.319081551861
2007-12-28 0.319081551861
2007-12-29 0.319081551861
2007-12-30 0.319081551861
2007-12-31 0.319081551861
2008-01-01 0.319081551861
2008-01-02 0.319081551861
2008-01-03 0.319351009102
2008-01-04 0.319351009102
2008-01-05 0.319351009102
2008-01-06 0.319351009102
2008-01-07 0.319351009102
2008-01-08 0.319351009102
2008-01-09 0.318720379147
2008-01-10 0.318720379147
2008-01-11 0.318863456985
2008-01-12 0.318863456985
2008-01-13 0.318863456985
2008-01-14 0.318863456985
2008-01-15 0.318863456985
2008-01-16 0.318863456985
2008-01-17 0.315073815074
2008-01-18 0.315259488768
2008-01-19 0.312836279785
2008-01-20 0.312716096811
2008-01-21 0.312596006144
2008-01-22 0.312596006144
2008-01-23 0.312596006144
2008-01-24 0.312476007678
2008-01-25 0.312476007678
2008-01-26 0.312476007678
2008-01-27 0.31223628692
2008-01-28 0.312116564417
2008-01-29 0.312116564417
2008-01-30 0.312116564417
2008-01-31 0.31290693221
2008-02-01 0.31290693221
2008-02-02 0.31290693221
2008-02-03 0.31290693221
2008-02-04 0.31290693221
2008-02-05 0.31290693221
2008-02-06 0.31290693221
2008-02-07 0.313169984686
2008-02-08 0.313169984686
2008-02-10 0.313169984686
2008-02-11 0.313169984686
2008-02-12 0.313169984686
2008-02-13 0.313432835821
2008-02-14 0.313432835821
2008-02-15 0.313432835821
2008-02-16 0.313432835821
2008-02-17 0.313432835821
2008-02-18 0.313432835821
2008-02-19 0.313432835821
2008-02-20 0.313432835821
2008-02-21 0.313000381243
2008-02-22 0.312523791397
2008-02-23 0.312523791397
2008-02-24 0.312523791397
2008-02-25 0.315130830489
2008-02-26 0.315909090909
2008-02-27 0.313651748778
2008-02-28 0.314425244177
2008-02-29 0.314307172362
2008-03-01 0.314307172362
2008-03-02 0.314092953523
2008-03-03 0.314275037369
2008-03-04 0.314275037369
2008-03-05 0.314275037369
2008-03-06 0.314275037369
2008-03-07 0.314531191632
2008-03-08 0.314531191632
2008-03-09 0.314531191632
2008-03-10 0.314531191632
2008-03-11 0.314413741598
2008-03-12 0.314669652856
2008-03-13 0.314669652856
2008-03-14 0.314669652856
2008-03-15 0.314669652856
2008-03-16 0.314669652856
2008-03-17 0.314669652856
2008-03-18 0.314669652856
2008-03-19 0.314669652856
2008-03-20 0.314669652856
2008-03-21 0.314669652856
2008-03-22 0.314669652856
2008-03-23 0.314925373134
2008-03-24 0.314925373134
2008-03-25 0.314925373134
2008-03-26 0.314925373134
2008-03-27 0.314925373134
2008-03-28 0.314925373134
2008-03-29 0.314925373134
2008-03-30 0.314925373134
2008-03-31 0.314925373134
2008-04-01 0.314925373134
2008-04-02 0.314925373134
2008-04-03 0.314925373134
2008-04-04 0.314925373134
2008-04-06 0.314925373134
2008-04-07 0.314925373134
2008-04-08 0.314925373134
2008-04-09 0.314925373134
2008-04-10 0.314925373134
2008-04-11 0.314925373134
2008-04-12 0.314925373134
2008-04-13 0.314925373134
2008-04-14 0.314925373134
2008-04-15 0.314925373134
2008-04-16 0.314925373134
2008-04-17 0.314925373134
2008-04-18 0.314925373134
2008-04-19 0.315318673127
2008-04-20 0.315573770492
2008-04-21 0.315573770492
2008-04-22 0.315573770492
2008-04-23 0.315573770492
2008-04-24 0.315573770492
2008-04-25 0.315573770492
2008-04-26 0.315573770492
2008-04-27 0.315573770492
2008-04-28 0.315573770492
2008-04-29 0.315573770492
2008-04-30 0.315456238361
2008-05-01 0.315456238361
2008-05-02 0.315338793745
2008-05-03 0.315338793745
2008-05-04 0.315338793745
2008-05-05 0.315338793745
2008-05-06 0.315338793745
2008-05-07 0.315338793745
2008-05-08 0.315338793745
2008-05-09 0.315338793745
2008-05-10 0.315338793745
2008-05-11 0.315338793745
2008-05-12 0.315338793745
2008-05-13 0.315338793745
2008-05-14 0.315221436546
2008-05-15 0.315221436546
2008-05-16 0.315221436546
2008-05-17 0.315221436546
2008-05-18 0.315221436546
2008-05-19 0.315221436546
2008-05-20 0.315221436546
2008-05-21 0.315221436546
2008-05-22 0.314732142857
2008-05-23 0.314732142857
2008-05-24 0.314732142857
2008-05-25 0.314732142857
2008-05-26 0.314732142857
2008-05-27 0.314732142857
2008-05-28 0.314732142857
2008-05-29 0.314732142857
2008-05-30 0.314732142857
2008-05-31 0.314732142857
2008-06-01 0.314498141264
2008-06-02 0.314498141264
2008-06-03 0.314498141264
2008-06-04 0.31475287997
2008-06-05 0.31475287997
2008-06-06 0.31475287997
2008-06-07 0.31475287997
2008-06-08 0.31475287997
2008-06-09 0.31475287997
2008-06-10 0.31475287997
2008-06-11 0.31475287997
2008-06-12 0.31475287997
2008-06-13 0.31475287997
2008-06-14 0.31475287997
2008-06-15 0.31475287997
2008-06-16 0.31475287997
2008-06-17 0.31475287997
2008-06-18 0.31475287997
2008-06-19 0.31475287997
2008-06-20 0.31475287997
2008-06-21 0.31475287997
2008-06-22 0.31475287997
2008-06-23 0.31475287997
2008-06-24 0.31475287997
2008-06-25 0.31475287997
2008-06-26 0.31475287997
2008-06-27 0.31475287997
2008-06-28 0.31475287997
2008-06-29 0.31475287997
2008-06-30 0.31475287997
2008-07-01 0.31475287997
2008-07-02 0.31475287997
2008-07-03 0.31475287997
2008-07-04 0.31475287997
2008-07-05 0.31475287997
2008-07-06 0.31475287997
2008-07-07 0.31475287997
2008-07-08 0.31475287997
2008-07-09 0.31475287997
2008-07-10 0.31475287997
2008-07-11 0.31475287997
2008-07-12 0.31475287997
2008-07-13 0.31475287997
2008-07-14 0.31475287997
2008-07-15 0.31475287997
2008-07-16 0.31475287997
2008-07-17 0.31475287997
2008-07-18 0.315007429421
2008-07-19 0.315007429421
2008-07-21 0.315007429421
2008-07-22 0.315007429421
2008-07-23 0.315007429421
2008-07-24 0.315007429421
2008-07-25 0.315007429421
2008-07-26 0.315007429421
2008-07-27 0.315007429421
2008-07-28 0.315007429421
2008-07-29 0.315007429421
2008-07-30 0.315007429421
2008-07-31 0.315007429421
2008-08-01 0.315007429421
2008-08-02 0.315007429421
2008-08-03 0.315007429421
2008-08-04 0.315007429421
2008-08-05 0.315007429421
2008-08-06 0.315007429421
2008-08-07 0.315007429421
2008-08-08 0.315007429421
2008-08-09 0.315007429421
2008-08-10 0.315007429421
2008-08-11 0.315007429421
2008-08-12 0.315007429421
2008-08-13 0.315007429421
2008-08-14 0.315007429421
2008-08-15 0.315007429421
2008-08-16 0.315007429421
2008-08-17 0.315007429421
2008-08-18 0.315007429421
2008-08-19 0.315007429421
2008-08-20 0.315007429421
2008-08-21 0.315007429421
2008-08-22 0.315007429421
2008-08-23 0.315007429421
2008-08-24 0.315007429421
2008-08-25 0.315007429421
2008-08-26 0.315007429421
2008-08-27 0.315007429421
2008-08-29 0.315007429421
2008-08-30 0.315007429421
2008-08-31 0.315007429421
2008-09-01 0.315007429421
2008-09-02 0.31489045674
2008-09-03 0.31489045674
2008-09-04 0.314773570898
2008-09-05 0.314773570898
2008-09-06 0.314773570898
2008-09-07 0.314773570898
2008-09-08 0.314773570898
2008-09-09 0.314773570898
2008-09-10 0.314773570898
2008-09-11 0.314773570898
2008-09-13 0.314773570898
2008-09-14 0.314773570898
2008-09-15 0.314773570898
2008-09-16 0.314773570898
2008-09-17 0.314773570898
2008-09-18 0.314773570898
2008-09-19 0.314773570898
2008-09-20 0.314773570898
2008-09-21 0.3146567718
2008-09-22 0.3146567718
2008-09-23 0.3146567718
2008-09-24 0.3146567718
e
2007-12-14 0.00990491283677
2007-12-15 0.00990491283677
2007-12-16 0.00990491283677
2007-12-17 0.00990491283677
2007-12-18 0.00990491283677
2007-12-19 0.00990491283677
2007-12-20 0.00990491283677
2007-12-21 0.00990491283677
2007-12-22 0.00990491283677
2007-12-23 0.00990491283677
2007-12-24 0.00990491283677
2007-12-25 0.00990099009901
2007-12-26 0.00990099009901
2007-12-27 0.00989707046714
2007-12-28 0.00989707046714
2007-12-29 0.00989707046714
2007-12-30 0.00989707046714
2007-12-31 0.00989707046714
2008-01-01 0.00989707046714
2008-01-02 0.00989707046714
2008-01-03 0.00989315393748
2008-01-04 0.00989315393748
2008-01-05 0.00989315393748
2008-01-06 0.00989315393748
2008-01-07 0.00989315393748
2008-01-08 0.00989315393748
2008-01-09 0.00987361769352
2008-01-10 0.00987361769352
2008-01-11 0.00986582478295
2008-01-12 0.00986582478295
2008-01-13 0.00986582478295
2008-01-14 0.00986582478295
2008-01-15 0.00986582478295
2008-01-16 0.00986582478295
2008-01-17 0.00971250971251
2008-01-18 0.00968241673122
2008-01-19 0.00960799385088
2008-01-20 0.00960430272762
2008-01-21 0.00960061443932
2008-01-22 0.00960061443932
2008-01-23 0.00960061443932
2008-01-24 0.00959692898273
2008-01-25 0.00959692898273
2008-01-26 0.00959692898273
2008-01-27 0.00958956655159
2008-01-28 0.00958588957055
2008-01-29 0.00958588957055
2008-01-30 0.00958588957055
2008-01-31 0.00957487552662
2008-02-01 0.00957487552662
2008-02-02 0.00957487552662
2008-02-03 0.00957487552662
2008-02-04 0.00957487552662
2008-02-05 0.00957487552662
2008-02-06 0.00957487552662
2008-02-07 0.00957120980092
2008-02-08 0.00957120980092
2008-02-10 0.00957120980092
2008-02-11 0.00957120980092
2008-02-12 0.00957120980092
2008-02-13 0.00956754688098
2008-02-14 0.00956754688098
2008-02-15 0.00956754688098
2008-02-16 0.00956754688098
2008-02-17 0.00956754688098
2008-02-18 0.00956754688098
2008-02-19 0.00956754688098
2008-02-20 0.00956754688098
2008-02-21 0.00953107129241
2008-02-22 0.00951655881233
2008-02-23 0.00951655881233
2008-02-24 0.00951655881233
2008-02-25 0.00948047023132
2008-02-26 0.0094696969697
2008-02-27 0.00940203083866
2008-02-28 0.00939143501127
2008-02-29 0.00938790837401
2008-03-01 0.00938790837401
2008-03-02 0.00937031484258
2008-03-03 0.0093423019432
2008-03-04 0.0093423019432
2008-03-05 0.0093423019432
2008-03-06 0.0093423019432
2008-03-07 0.0093388121031
2008-03-08 0.0093388121031
2008-03-09 0.0093388121031
2008-03-10 0.0093388121031
2008-03-11 0.00933532486931
2008-03-12 0.0093318402389
2008-03-13 0.0093318402389
2008-03-14 0.0093318402389
2008-03-15 0.0093318402389
2008-03-16 0.0093318402389
2008-03-17 0.0093318402389
2008-03-18 0.0093318402389
2008-03-19 0.0093318402389
2008-03-20 0.0093318402389
2008-03-21 0.0093318402389
2008-03-22 0.0093318402389
2008-03-23 0.00932835820896
2008-03-24 0.00932835820896
2008-03-25 0.00932835820896
2008-03-26 0.00932835820896
2008-03-27 0.00932835820896
2008-03-28 0.00932835820896
2008-03-29 0.00932835820896
2008-03-30 0.00932835820896
2008-03-31 0.00932835820896
2008-04-01 0.00932835820896
2008-04-02 0.00932835820896
2008-04-03 0.00932835820896
2008-04-04 0.00932835820896
2008-04-06 0.00932835820896
2008-04-07 0.00932835820896
2008-04-08 0.00932835820896
2008-04-09 0.00932835820896
2008-04-10 0.00932835820896
2008-04-11 0.00932835820896
2008-04-12 0.00932835820896
2008-04-13 0.00932835820896
2008-04-14 0.00932835820896
2008-04-15 0.00932835820896
2008-04-16 0.00932835820896
2008-04-17 0.00932835820896
2008-04-18 0.00932835820896
2008-04-19 0.00931792769288
2008-04-20 0.00931445603577
2008-04-21 0.00931445603577
2008-04-22 0.00931445603577
2008-04-23 0.00931445603577
2008-04-24 0.00931445603577
2008-04-25 0.00931445603577
2008-04-26 0.00931445603577
2008-04-27 0.00931445603577
2008-04-28 0.00931445603577
2008-04-29 0.00931445603577
2008-04-30 0.00931098696462
2008-05-01 0.00931098696462
2008-05-02 0.00930752047655
2008-05-03 0.00930752047655
2008-05-04 0.00930752047655
2008-05-05 0.00930752047655
2008-05-06 0.00930752047655
2008-05-07 0.00930752047655
2008-05-08 0.00930752047655
2008-05-09 0.00930752047655
2008-05-10 0.00930752047655
2008-05-11 0.00930752047655
2008-05-12 0.00930752047655
2008-05-13 0.00930752047655
2008-05-14 0.00930405656866
2008-05-15 0.00930405656866
2008-05-16 0.00930405656866
2008-05-17 0.00930405656866
2008-05-18 0.00930405656866
2008-05-19 0.00930405656866
2008-05-20 0.00930405656866
2008-05-21 0.00930405656866
2008-05-22 0.0093005952381
2008-05-23 0.0093005952381
2008-05-24 0.0093005952381
2008-05-25 0.0093005952381
2008-05-26 0.0093005952381
2008-05-27 0.0093005952381
2008-05-28 0.0093005952381
2008-05-29 0.0093005952381
2008-05-30 0.0093005952381
2008-05-31 0.0093005952381
2008-06-01 0.0092936802974
2008-06-02 0.0092936802974
2008-06-03 0.0092936802974
2008-06-04 0.00929022668153
2008-06-05 0.00929022668153
2008-06-06 0.00929022668153
2008-06-07 0.00929022668153
2008-06-08 0.00929022668153
2008-06-09 0.00929022668153
2008-06-10 0.00929022668153
2008-06-11 0.00929022668153
2008-06-12 0.00929022668153
2008-06-13 0.00929022668153
2008-06-14 0.00929022668153
2008-06-15 0.00929022668153
2008-06-16 0.00929022668153
2008-06-17 0.00929022668153
2008-06-18 0.00929022668153
2008-06-19 0.00929022668153
2008-06-20 0.00929022668153
2008-06-21 0.00929022668153
2008-06-22 0.00929022668153
2008-06-23 0.00929022668153
2008-06-24 0.00929022668153
2008-06-25 0.00929022668153
2008-06-26 0.00929022668153
2008-06-27 0.00929022668153
2008-06-28 0.00929022668153
2008-06-29 0.00929022668153
2008-06-30 0.00929022668153
2008-07-01 0.00929022668153
2008-07-02 0.00929022668153
2008-07-03 0.00929022668153
2008-07-04 0.00929022668153
2008-07-05 0.00929022668153
2008-07-06 0.00929022668153
2008-07-07 0.00929022668153
2008-07-08 0.00929022668153
2008-07-09 0.00929022668153
2008-07-10 0.00929022668153
2008-07-11 0.00929022668153
2008-07-12 0.00929022668153
2008-07-13 0.00929022668153
2008-07-14 0.00929022668153
2008-07-15 0.00929022668153
2008-07-16 0.00929022668153
2008-07-17 0.00929022668153
2008-07-18 0.0092867756315
2008-07-19 0.0092867756315
2008-07-21 0.0092867756315
2008-07-22 0.0092867756315
2008-07-23 0.0092867756315
2008-07-24 0.0092867756315
2008-07-25 0.0092867756315
2008-07-26 0.0092867756315
2008-07-27 0.0092867756315
2008-07-28 0.0092867756315
2008-07-29 0.0092867756315
2008-07-30 0.0092867756315
2008-07-31 0.0092867756315
2008-08-01 0.0092867756315
2008-08-02 0.0092867756315
2008-08-03 0.0092867756315
2008-08-04 0.0092867756315
2008-08-05 0.0092867756315
2008-08-06 0.0092867756315
2008-08-07 0.0092867756315
2008-08-08 0.0092867756315
2008-08-09 0.0092867756315
2008-08-10 0.0092867756315
2008-08-11 0.0092867756315
2008-08-12 0.0092867756315
2008-08-13 0.0092867756315
2008-08-14 0.0092867756315
2008-08-15 0.0092867756315
2008-08-16 0.0092867756315
2008-08-17 0.0092867756315
2008-08-18 0.0092867756315
2008-08-19 0.0092867756315
2008-08-20 0.0092867756315
2008-08-21 0.0092867756315
2008-08-22 0.0092867756315
2008-08-23 0.0092867756315
2008-08-24 0.0092867756315
2008-08-25 0.0092867756315
2008-08-26 0.0092867756315
2008-08-27 0.0092867756315
2008-08-29 0.0092867756315
2008-08-30 0.0092867756315
2008-08-31 0.0092867756315
2008-09-01 0.0092867756315
2008-09-02 0.00928332714445
2008-09-03 0.00928332714445
2008-09-04 0.00927988121752
2008-09-05 0.00927988121752
2008-09-06 0.00927988121752
2008-09-07 0.00927988121752
2008-09-08 0.00927988121752
2008-09-09 0.00927988121752
2008-09-10 0.00927988121752
2008-09-11 0.00927988121752
2008-09-13 0.00927988121752
2008-09-14 0.00927988121752
2008-09-15 0.00927988121752
2008-09-16 0.00927988121752
2008-09-17 0.00927988121752
2008-09-18 0.00927988121752
2008-09-19 0.00927988121752
2008-09-20 0.00927988121752
2008-09-21 0.00927643784787
2008-09-22 0.00927643784787
2008-09-23 0.00927643784787
2008-09-24 0.00927643784787
e
