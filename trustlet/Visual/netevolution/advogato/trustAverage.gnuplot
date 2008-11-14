#!/usr/bin/env gnuplot
# Title: Trust Average on time
# Date: Wed Nov 12 10:54:23 2008
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
2005-11-11 0.790454859361
2006-02-11 0.81225694496
2006-05-20 0.81398852326
2007-08-27 0.799111520737
2007-10-13 0.793285129975
2007-10-20 0.793370379693
2007-10-21 0.793402636622
2007-10-22 0.793418633011
2007-10-25 0.793432535459
2007-10-28 0.793459678979
2007-10-30 0.793503480278
2007-11-01 0.793531799729
2007-11-02 0.793539781953
2007-11-03 0.793523190844
2007-11-04 0.793527182739
2007-11-05 0.793571331929
2007-11-06 0.793603864734
2007-11-07 0.793655945137
2007-11-08 0.793655945137
2007-11-09 0.793698444895
2007-11-10 0.793717884326
2007-11-11 0.79372573261
2007-11-12 0.793729596075
2007-11-13 0.793734790838
2007-11-14 0.793738774407
2007-11-16 0.793735153821
2007-11-17 0.793747344842
2007-11-18 0.793747586313
2007-11-19 0.793747707042
2007-11-20 0.793779562523
2007-11-21 0.793791625644
2007-11-23 0.793788004556
2007-11-26 0.793784263763
2007-11-27 0.793650793651
2007-11-29 0.793654783079
2007-11-30 0.793658772354
2007-12-01 0.79366675044
2007-12-03 0.793658036698
2007-12-05 0.793684861844
2007-12-06 0.79368062807
2007-12-09 0.793688362919
2007-12-10 0.793688484966
2007-12-12 0.793684373368
2007-12-14 0.793699965193
2007-12-15 0.793700087015
2007-12-16 0.793696219665
2007-12-17 0.793712175409
2007-12-20 0.793658234223
2007-12-22 0.793662231003
2007-12-23 0.793662231003
2007-12-25 0.793666227628
2007-12-27 0.793654606028
2007-12-28 0.793654606028
2007-12-30 0.79365085514
2008-01-02 0.79365485183
2008-01-03 0.79365485183
2008-01-04 0.793654974725
2008-01-06 0.793663297181
2008-01-07 0.793663420123
2008-01-09 0.793667546174
2008-01-10 0.793675551934
2008-01-11 0.793746967609
2008-01-12 0.793743207576
2008-01-13 0.793842455263
2008-01-15 0.793846571412
2008-01-16 0.793970978554
2008-01-18 0.793991632448
2008-01-19 0.793991632448
2008-01-21 0.793991748823
2008-01-22 0.793991981561
2008-01-23 0.793991981561
2008-01-24 0.793991981561
2008-01-25 0.793996087773
2008-01-26 0.793988457218
2008-01-27 0.793988457218
2008-01-30 0.7939847003
2008-01-31 0.7939847003
2008-02-02 0.793991981561
2008-02-04 0.793991981561
2008-02-05 0.793996087773
2008-02-06 0.794021875907
2008-02-07 0.7940238427
2008-02-08 0.794024074002
2008-02-13 0.794039324973
2008-02-14 0.794043541364
2008-02-15 0.794043541364
2008-02-16 0.794043541364
2008-02-17 0.79404365663
2008-02-18 0.79404365663
2008-02-20 0.794047757266
2008-02-21 0.794063812085
2008-02-22 0.794064041792
2008-02-23 0.794064041792
2008-02-26 0.794088288776
2008-02-28 0.79409227198
2008-03-01 0.79409227198
2008-03-03 0.79409227198
2008-03-06 0.794156208304
2008-03-07 0.794156208304
2008-03-08 0.794128113879
2008-03-09 0.794128113879
2008-03-10 0.794144152855
2008-03-12 0.794199760257
2008-03-14 0.794199535963
2008-03-15 0.794240878169
2008-03-16 0.794274787043
2008-03-17 0.794274897628
2008-03-18 0.794270923876
2008-03-20 0.794270923876
2008-03-21 0.794294764084
2008-03-23 0.794302819621
2008-03-24 0.794302819621
2008-03-28 0.794307231824
2008-03-29 0.794315175623
2008-03-30 0.794319147293
2008-04-02 0.794307891332
2008-04-03 0.794311643174
2008-04-04 0.794311643174
2008-04-06 0.794311643174
2008-04-08 0.794324105178
2008-04-09 0.794312741313
2008-04-10 0.794312741313
2008-04-11 0.794312851103
2008-04-12 0.794312851103
2008-04-13 0.794312851103
2008-04-14 0.79431296089
2008-04-15 0.794309209891
2008-04-16 0.794337144623
2008-04-18 0.79443059501
2008-04-23 0.794442726851
2008-04-25 0.79445067048
2008-04-26 0.794454963484
2008-04-28 0.794451099347
2008-04-29 0.794439936633
2008-04-30 0.794492860041
2008-05-01 0.794492753623
2008-05-02 0.794492753623
2008-05-03 0.794504984929
2008-05-04 0.794504984929
2008-05-06 0.794501226887
2008-05-07 0.794501226887
2008-05-08 0.794505197264
2008-05-09 0.794505197264
2008-05-10 0.794505197264
2008-05-11 0.794505197264
2008-05-12 0.795022318409
2008-05-13 0.79450927357
2008-05-14 0.794501864266
2008-05-15 0.794505621885
2008-05-16 0.794505409583
2008-05-20 0.794505515736
2008-05-21 0.794505515736
2008-05-23 0.794505621885
2008-05-24 0.794505621885
2008-05-25 0.794505621885
2008-05-26 0.794505621885
2008-05-27 0.794498106792
2008-05-28 0.794513561549
2008-05-29 0.794513561549
2008-05-30 0.794513667536
2008-06-01 0.794525681392
2008-06-03 0.794525892874
2008-06-05 0.794529967358
2008-06-06 0.794492041697
2008-06-07 0.79449601609
2008-06-09 0.794492361245
2008-06-10 0.794492254733
2008-06-11 0.794492254733
2008-06-12 0.794674910637
2008-06-15 0.794674910637
2008-06-16 0.794674910637
2008-06-17 0.794674910637
2008-06-18 0.794674910637
2008-06-19 0.794674910637
2008-06-25 0.794679246742
2008-06-26 0.794679452479
2008-06-27 0.794679658199
2008-06-28 0.794679658199
2008-06-29 0.794679658199
2008-07-01 0.794708360713
2008-07-02 0.794708360713
2008-07-07 0.794708667504
2008-07-08 0.794708667504
2008-07-09 0.794716601929
2008-07-10 0.794716704027
2008-07-12 0.794720670931
2008-07-13 0.794720670931
2008-07-17 0.794746194854
2008-07-18 0.794810910986
2008-07-19 0.794951111797
2008-07-20 0.794999421676
2008-07-21 0.794999421676
2008-07-22 0.794995662651
2008-07-23 0.794988241644
2008-07-24 0.794988241644
2008-07-26 0.794988241644
2008-07-27 0.794992193373
2008-07-28 0.7949922899
2008-07-29 0.795047978728
2008-07-30 0.795052213788
2008-08-01 0.795306067485
2008-08-03 0.795310907238
2008-08-08 0.795386478538
2008-08-09 0.795339178588
2008-08-10 0.795339178588
2008-08-11 0.795339178588
2008-08-12 0.795335602084
2008-08-13 0.795339805825
2008-08-15 0.795343382296
2008-08-16 0.795343382296
2008-08-18 0.795347317017
2008-08-20 0.795347406468
2008-08-21 0.795347406468
2008-08-22 0.795347406468
2008-08-23 0.795347406468
2008-08-24 0.795347406468
2008-08-25 0.795347406468
2008-08-26 0.795387187914
2008-08-27 0.795305525627
2008-08-29 0.795288683603
2008-08-30 0.795284925232
2008-09-01 0.795374855825
2008-09-02 0.795501776625
2008-09-03 0.795676940486
2008-09-04 0.795718502051
2008-09-05 0.795722417064
2008-09-07 0.795722499042
2008-09-08 0.795722499042
2008-09-10 0.795734242953
2008-09-12 0.79573815729
2008-09-13 0.795741989882
2008-09-14 0.795742071477
2008-09-15 0.795745985513
2008-09-16 0.795769871832
2008-09-17 0.795769871832
2008-09-19 0.795769871832
2008-09-20 0.795769871832
2008-09-21 0.795769871832
2008-09-22 0.795836684668
2008-09-25 0.795810435615
2008-09-26 0.795810435615
2008-09-27 0.795810435615
2008-09-29 0.796128071482
2008-09-30 0.796128145405
2008-10-01 0.796128219325
2008-10-02 0.796128219325
2008-10-03 0.796128219325
2008-10-04 0.796223031875
2008-10-05 0.796219288875
2008-10-06 0.796223175966
2008-10-07 0.796219433106
2008-10-08 0.796223392081
2008-10-09 0.796223392081
2008-10-11 0.796231309124
2008-10-13 0.796227422708
2008-10-14 0.796223536143
2008-10-15 0.796223536143
2008-10-16 0.796235195392
2008-10-19 0.796242967484
2008-10-20 0.796242752518
2008-10-21 0.796250595976
2008-10-22 0.796246924881
2008-10-23 0.796262181284
2008-10-26 0.796266137798
2008-10-27 0.796262252565
2008-10-28 0.796266137798
2008-10-29 0.796266137798
2008-10-30 0.796258652581
2008-11-01 0.796270520716
2008-11-02 0.796270520716
2008-11-03 0.796278289386
2008-11-05 0.796278360343
2008-11-06 0.796278573199
2008-11-07 0.796271089505
2008-11-08 0.796271089505
2008-11-09 0.796271089505
e
