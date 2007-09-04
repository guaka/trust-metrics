from net_flow import TrustNetwork

capacities = [ 20, 7, 2, 1 ]
network = TrustNetwork()

network.add_edge("-", "el_seed")
network.add_edge("el_seed", "test1")
network.add_edge("test1", "test2")
network.add_edge("test3", "test4")
network.add_edge("-", "test4")

network.calculate(capacities)

for user in network:
    print "%-10s\t%s" % (user, network.is_auth(user))
