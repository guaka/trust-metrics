#set size 0.7,0.7
#set xlabel "in-degree"
#set ylabel "number of nodes"
set logscale x
set logscale y

#set boxwidth 0.3 relative
#set style fill solid 1.0
#set label "CF"  at first 0.95, first 1.18
#set label "1.094"  at first 0.95, first 1.13
set terminal postscript eps
plot [1:700] [1:10000] "deg_in.data" using 1:2 title '' with lines
#plot [0:10000] [0:1.2] "/home/phauly/software/eclipse/workspace/SimilarityMeasuresForRankedLists/bin/osim_both_trust" using 1:2 title 'OSim' with points
#plot [0:131828] [0:1.2] "./osim_data.txt" using 1:2 title 'osim' with points
pause -1
