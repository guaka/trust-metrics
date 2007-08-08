
from pymmetry.net_flow import NetFlow
from trustlet.Advogato import Advogato
import networkx


def test():
    a = Advogato()
    G = networkx.read_dot(a.numbersfilepath)

    if False:
	from pprint import pprint

	# large test of max flow.
	#
	# notes.
	#
	# this test is to double-check that if you have a large
	# group of nodes that are interlinked to each other, and
	# another group that is interlinked to itself and the first
	# group, that none of the second group gets any flow.
	# 
	# it's also quite a good test of the amount of
	# time / memory this takes up (about 1k per node).
	# try 100,000: it's fun!

	from random import randint

	f = NetFlow()
	f.netflow_add_edge("-", 0)
	len = 10000
	for i in range(len):
		f.netflow_add_edge(randint(0, len/4), randint(0, len/4))
		f.netflow_add_edge(randint(len/4+1, len/2), randint(0, len/2))

	e = f.netflow_max_flow_extract("-", [800, 200, 50, 12, 4, 2, 1])

	for x in e.keys():
		if type(x) == type(0) and x > (len/4) and e[x] != 0:
			raise ("untrusted group (%d->%d) linked to trusted (0->%d)\n" % \
					(len/4+1, len/2, len/4))
	
	print "random test passed ok"
	print 

	# pretty test of max flow.
	#
	# notes.
	#
	# mary and bob like each other, but the seeds aren't
	# interested in mary and bob, so they don't show up
	# in the max flow diagram.
	#
	# fleas ad infinitum is so far down from the seeds that
	# despite being linked, no flow reaches it: the
	# available capacity, which is limited in this test to
	# 7 degrees away from the supersink ("-") _anyway_,
	# is all used up.
	#
	# 1: -, 2: seed, 3: heather, 4: rob,
	# 5: fleas, 6: lit-f, 7: less-f - whoops! 8: fad.
	# yeah, that's right.  the capacity chain is only 7-long
	# so anything beyond 7 degrees from the supersink isn't
	# included.  cool.
	
	# the second test is what heather likes, and heather's likes'
	# likes, and heather's likes' likes' likes... etc., up to
	# 7 degrees.  which is why fleas ad infinitum _is_ shown
	# in the flow, this time.  cool.

	f = NetFlow()
	f.set_debuglevel(1)
	f.netflow_add_edge("-", "seed")
	f.netflow_add_edge("-", "seed2")
	f.netflow_add_edge("seed", "heather")
	f.netflow_add_edge("seed2", "heather")
	f.netflow_add_edge("seed", 55)
	f.netflow_add_edge("seed", u"luke")
	f.netflow_add_edge(55, 10)
	f.netflow_add_edge(10, u"luke")
	f.netflow_add_edge(u"luke", "heather")
	f.netflow_add_edge("heather", u"luke")
	f.netflow_add_edge("heather", "flat-faced cat")
	f.netflow_add_edge("flat-faced cat", "heather")
	f.netflow_add_edge("luke", "flat-faced cat")
	f.netflow_add_edge("heather", "mo the mad orange pony")
	f.netflow_add_edge("heather", "robbie the old crock pony")
	f.netflow_add_edge("robbie the old crock pony", "fleas")
	f.netflow_add_edge("fleas", "little fleas")
	f.netflow_add_edge("little fleas", "lesser fleas")
	f.netflow_add_edge("lesser fleas", "fleas ad infinitum")

	f.netflow_add_edge("bob", "heather")
	f.netflow_add_edge("bob", "mary")
	f.netflow_add_edge("mary", "bob")

	print "pretty node graph (yes, the numbers 55 and 10 are nodes):"
	pprint(f.succs)
	print 

	e = f.netflow_max_flow_extract("-", [800, 200, 50, 12, 4, 2, 1])
	print "supersink as seed - avg_capacity:", f.get_avg_capacity()
	pprint(e)
	print 

	e = f.netflow_max_flow_extract("heather", [800, 200, 50, 12, 4, 2, 1])
	print "heather as seed - avg_capacity:", f.get_avg_capacity()
	pprint(e)
	print 


if __name__ == '__main__':
	test()

