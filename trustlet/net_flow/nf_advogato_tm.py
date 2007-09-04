"""
Use actual advogato certifications to calculate the advogato.org (or
robots.net) trust certifications.
"""
import sys, time
from advogato import AdvogatoTrustNetwork, RobotsTrustNetwork, \
     read_certs, fill_certs, read_actual


def test():
    if False:
        network = RobotsTrustNetwork()
    else:
        network = AdvogatoTrustNetwork()

    certs_list = read_certs(open('data/advogato.org-certs.txt'))
    actual_dict = read_actual(open('data/advogato.org-actual.txt'))

    print 'read %d certs' % (len(certs_list),)
    fill_certs(certs_list, network)

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

    print '\ncount:'
    for n, i in calc_counts.items():
        print n, i

t = time.time() 
test()
print time.time() - t
