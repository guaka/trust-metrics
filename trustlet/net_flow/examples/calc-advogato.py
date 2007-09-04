"""
Use actual advogato certifications to calculate the advogato.org (or
robots.net) trust certifications.
"""
import sys
from advogato import AdvogatoTrustNetwork, RobotsTrustNetwork, \
     read_certs, fill_certs, read_actual
from optparse import OptionParser

#### OPTIONS

parser = OptionParser()

parser.add_option('-r', '--robots', action="store_true", dest="use_robots",
                  help = 'use robots.net parameters', default=False)

#####

(options, args) = parser.parse_args()

if options.use_robots:
    network = RobotsTrustNetwork()
else:
    network = AdvogatoTrustNetwork()

if len(args) != 2:
    sys.stderr.write('ERROR: You must supply certs and actual filenames.\n')
    sys.stderr.write('\nUsage:\n\tcalc-advogato.py [ --robots ] certs.txt actual.txt\n\nSee the data/ directory in the net_flow package for example files.\n\n')
    sys.exit(-1)

###

certs_list = read_certs(open(args[0]))
actual_dict = read_actual(open(args[1]))

print 'read %d certs' % (len(certs_list),)
fill_certs(certs_list, network)

### calculate.

print 'calculating... %d certs, %d users' % (len(certs_list),
                                             len(network.flows[1]),)
network.calculate_levels()

#
# compare the calculated cert levels with the actual levels.
#

calc_counts = {}
for user in network.users:
    cert = network.get_level(user)
    if cert:
        actual = actual_dict.get(user, "Observer")
        if actual != cert and user != '-':
            print 'USER %s: should be %s, is %s' % (user, actual, cert,)
        n = calc_counts.get(cert, 0)
        n += 1
        calc_counts[cert] = n

for (user, level) in actual_dict.items():
    cert = network.get_level(user)
    if cert is None:
        print "NO calculated cert for user %s (%s); what's up with that?" % (user, level,)

#
# compare!
#

print '\ncount:'
for n, i in calc_counts.items():
    print n, i
