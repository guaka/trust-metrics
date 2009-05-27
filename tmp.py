from trustlet import *

t = sys.stdout

sys.stdout = file( 'risultati', 'w' )

networks = ['vec','nap','la','fur','it']
dates = ['2008-06-25','2008-07-14','2008-10-16','2008-06-14','2008-06-26']

for i in xrange(len(networks)):
    print networks[i]+" at date "+dates[i]
    WikiNetwork( networks[i], dates[i]).info()
    print ""

sys.stdout = t

